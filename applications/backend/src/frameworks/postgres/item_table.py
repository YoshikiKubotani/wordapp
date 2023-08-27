from typing import Any

from psycopg2.extensions import connection

from src.domain.entity import ItemEntity
from src.frameworks import PostgreSQL


class ItemTable(PostgreSQL):
    def __init__(self, connection: connection | None = None, schema: str = "test"):
        super().__init__(
            connection=connection,
            db_name="item",
            target_class=ItemEntity,
            pk="item_id",
            fk={},
            py2sql={},
            fk_constraint="ON DELETE RESTRICT",
            schema=schema,
        )

    def select_data(self, conditions: dict[str, Any]) -> list[ItemEntity]:
        return super().select_data(conditions=conditions)
