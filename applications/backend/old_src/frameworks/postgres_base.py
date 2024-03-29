import os
import re
from contextlib import contextmanager
from datetime import datetime
from typing import Any, Generic, TypeVar, Union, cast

import psycopg2
from psycopg2.extensions import connection
from psycopg2.extras import DictCursor
from psycopg2.sql import SQL, Identifier
from pydantic import PositiveInt

from old_src.adapter.gateway import RDBRepositoryGateway
from old_src.utils import get_my_logger

logger = get_my_logger(__name__)

PY2SQL_TYPE_DICT = {
    str: "text",
    int: "bigint",
    float: "numeric",
    datetime: "timestamp",
    bool: "boolean",
    PositiveInt: "bigint",
}

T = TypeVar("T")


@contextmanager
def get_db() -> connection:
    """Establish a connection to the database and yield the session."""
    session = PostgreSQL.create_connection()
    try:
        yield session
    finally:
        session.close()


class PostgreSQL(RDBRepositoryGateway, Generic[T]):
    def __init__(
        self,
        db_name: str,
        target_class: T,
        pk: Union[str, list[str]],
        fk: dict[str, dict[str, str]],
        sort_key: str | None = None,
        py2sql: dict[str, str] = {},
        fk_constraint: str = "ON DELETE CASCADE",
        schema: str = "test",
        connection: connection | None = None,
    ) -> None:
        super().__init__(
            db_name=db_name,
            fk=fk,
        )
        self.conn = connection or self.create_connection()
        self.conn.autocommit = True
        self.schema = schema
        self.target_class = target_class
        self.feature = target_class.__annotations__
        self.pk = [pk] if isinstance(pk, str) else pk
        self.sort_key = sort_key
        self.py2sql = py2sql
        self.fk_constraint = fk_constraint

        self._validate_db_name_and_features()

    @classmethod
    def create_connection(cls) -> connection:
        """Establish and return a connection to the database."""
        return psycopg2.connect(
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
        )

    @classmethod
    def recreate_schema(cls, conn: connection, schema: str = "test") -> None:
        """Drop all tables in the schema and recreate the schema."""
        with conn.cursor() as cursor:
            query = SQL(
                """
                drop schema if exists {} cascade;
                create schema {};
                """
            ).format(Identifier(schema), Identifier(schema))

            cursor.execute(query)
        logger.info(f"Dropped and recreated schema: {schema}")

    def _validate_db_name_and_features(self) -> None:
        """Check if db_name and features are valid."""
        reserved_words = [
            "select",
            "from",
            "where",
            "join",
            "like",
            "and",
            "or",
            "not",
            "insert",
            "update",
            "delete",
        ]

        invalid_name_msg = (
            "'{}' is an invalid column name: Only lowercase alphabets are allowed."
        )
        reserved_word_msg = (
            "'{}' is a reserved word in PostgreSQL and cannot be used as an identifier."
        )

        for name in [self.db_name] + list(self.feature.keys()):
            if not re.match("^[a-z_-]*$", name):
                raise ValueError(invalid_name_msg.format(name))
            if name in reserved_words:
                raise ValueError(reserved_word_msg.format(name))

    def _pytype_to_sqltype(self, pytype: Any) -> str:
        """Convert a Python type to an SQL type."""
        if pytype in PY2SQL_TYPE_DICT:
            return PY2SQL_TYPE_DICT[pytype]
        if pytype in self.py2sql:
            return self.py2sql[pytype]
        raise ValueError(f"Unsupported Python data type: {pytype}")

    def create_table(self) -> None:
        with self.conn.cursor() as cursor:
            # Custom type creation
            type_creation_prompt = ""
            var_prompt = ""
            for k, v in self.feature.items():
                type_in_sql = self.py2sql.get(k)
                if type_in_sql:
                    type_creation_prompt += f"""
                    DO $$
                    BEGIN
                        IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = '{k}_type') THEN
                            EXECUTE 'CREATE TYPE {k}_type AS {type_in_sql}';
                        END IF;
                    END
                    $$;
                    """
                    var_prompt += f"{k} {k}_type, "
                else:
                    sql_type = PY2SQL_TYPE_DICT.get(v)
                    if not sql_type:
                        raise ValueError(f"{k} cannot be converted to SQL type")
                    var_prompt += f"{k} {sql_type}, "

            # Foreign key constraints
            fk_prompt = ""
            for k, v in self.fk.items():
                table_name = v.get("table")
                var_name = v.get("var")
                if not table_name or not var_name:
                    raise ValueError(f"Invalid FK definition for {k}")
                fk_prompt += f"FOREIGN KEY ({k}) REFERENCES {self.schema}.{table_name}({var_name}) {self.fk_constraint}, "

            # Primary key definition
            primary_key = ", ".join(self.pk)
            var_prompt += f"PRIMARY KEY ({primary_key})"

            table_creation_query = f"""
            {type_creation_prompt}
            CREATE TABLE IF NOT EXISTS {self.schema}.{self.db_name} (
                {var_prompt}
                {fk_prompt.rstrip(', ')}
            );
            """
            cursor.execute(table_creation_query)

    def is_exist(self, conditions: dict[str, Any]) -> bool:
        """Check if data exists in the table based on provided conditions."""
        with self.conn.cursor() as cur:
            conditions_str = " AND ".join([f"{key} = %s" for key in conditions.keys()])
            select_cmd = f"SELECT EXISTS (SELECT 1 FROM {self.schema}.{self.db_name} WHERE {conditions_str});"
            cur.execute(select_cmd, list(conditions.values()))
            return cast(bool, cur.fetchone()[0])

    def get_new_id(self) -> int:
        """Get a new ID for insertion. Assumes ID column contains integer values."""
        if len(self.pk) > 1:
            return 0
        with self.conn.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT {self.pk[0]}
                FROM {self.schema}.{self.db_name}
                ORDER BY {self.pk[0]} DESC
                LIMIT 1
                """
            )
            last_id = cursor.fetchone()
            if last_id:
                return cast(int, last_id[0] + 1)
            return 1

    def insert_or_update_data(self, data: T) -> None:
        """Insert data into the table. If conflict, update the data."""
        with self.conn.cursor() as cur:
            columns = ", ".join(data.__dict__.keys())
            values = list(data.__dict__.values())
            placeholders = ", ".join(["%s"] * len(values))

            # Prepare for ON CONFLICT clause
            pks_str = ", ".join(self.pk)
            update_statements = [
                f"{column} = EXCLUDED.{column}" for column in data.__dict__.keys()
            ]
            update_prompt = ", ".join(update_statements)

            insert_cmd = f"""
                INSERT INTO {self.schema}.{self.db_name} ({columns})
                VALUES ({placeholders})
                ON CONFLICT ({pks_str})
                DO UPDATE SET {update_prompt};
            """

            cur.execute(insert_cmd, values)

    def delete_data(self, conditions: dict[str, Any]) -> None:
        """Delete data from the table based on provided conditions."""
        with self.conn.cursor() as cur:
            conditions_str = " AND ".join([f"{key} = %s" for key in conditions.keys()])
            delete_cmd = (
                f"DELETE FROM {self.schema}.{self.db_name} WHERE {conditions_str};"
            )
            cur.execute(delete_cmd, list(conditions.values()))

    def select_data(self, conditions: dict[str, Any] = {}) -> list[T]:
        """Select data from the table based on provided conditions."""
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            if conditions:
                conditions_str = " AND ".join(
                    [f"{key} = %s" for key in conditions.keys()]
                )
                select_cmd = f"SELECT * FROM {self.schema}.{self.db_name} WHERE {conditions_str};"
                cur.execute(select_cmd, list(conditions.values()))
            else:
                select_cmd = f"SELECT * FROM {self.schema}.{self.db_name};"
                cur.execute(select_cmd)
            records = cur.fetchall()

        # Convert records to dictionaries
        records_as_dicts = [dict(record) for record in records]

        # Convert dictionaries to instances of the target class
        return [self.target_class(**record) for record in records_as_dicts]  # type: ignore

    def __del__(self) -> None:
        """Destructor to ensure that the connection is closed."""
        if self.conn:
            self.conn.close()
