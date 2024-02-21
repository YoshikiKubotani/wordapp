import datetime
from typing import Optional

from sqlalchemy import JSON, Column, ForeignKey, MetaData, Table
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from src.core.config import settings


def orm_object_to_dict(model):
    return {c.key: getattr(model, c.key) for c in inspect(model).mapper.column_attrs}


class Base(DeclarativeBase, AsyncAttrs):
    type_annotation_map = {
        list[str]: JSON().with_variant(JSONB(), "postgresql"),
    }
    metadata = MetaData(schema=settings.POSTGRES_SCHEMA)


item_genre_mapper_table = Table(
    "item_genre_mapper",
    Base.metadata,
    Column("item_id", ForeignKey("items.item_id"), primary_key=True),
    Column("genre_id", ForeignKey("genres.genre_id"), primary_key=True),
)

item_deck_mapper_table = Table(
    "item_deck_mapper",
    Base.metadata,
    Column("item_id", ForeignKey("items.item_id"), primary_key=True),
    Column("deck_id", ForeignKey("decks.deck_id"), primary_key=True),
)


class SQLAlchemyUser(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str] = mapped_column(unique=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[str]
    full_name: Mapped[Optional[str]]
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now)
    updated_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now)

    # One-to-many relationship with UserLoginHistory
    user_login_history: Mapped[list["SQLAlchemyUserLoginHistory"]] = relationship(
        back_populates="user"
    )
    # One-to-many relationship with Item
    items: Mapped[list["SQLAlchemyItem"]] = relationship(back_populates="user")
    # One-to-many relationship with Deck
    decks: Mapped[list["SQLAlchemyDeck"]] = relationship(back_populates="user")
    # One-to-many relationship with Quiz
    quizzes: Mapped[list["SQLAlchemyQuiz"]] = relationship(back_populates="user")


class SQLAlchemyUserLoginHistory(Base):
    __tablename__ = "user_login_history"

    user_login_history_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    login_timestamp: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.now
    )
    logout_timestamp: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.now
    )
    ip_address: Mapped[str]

    # Many-to-one relationship with User
    user: Mapped[SQLAlchemyUser] = relationship(back_populates="user_login_history")


class SQLAlchemyItem(Base):
    __tablename__ = "items"

    item_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    english: Mapped[str]
    japanese: Mapped[str]
    grade: Mapped[int]
    created_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now)
    updated_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now)

    # Many-to-one relationship with User
    user: Mapped[SQLAlchemyUser] = relationship(back_populates="items")
    # Many-to-many relationship with Genre
    genres: Mapped[list["SQLAlchemyGenre"]] = relationship(
        secondary=item_genre_mapper_table,
        back_populates="items",
    )
    # Many-to-many relationship with Deck
    decks: Mapped[list["SQLAlchemyDeck"]] = relationship(
        secondary=item_deck_mapper_table,
        back_populates="items",
    )
    # One-to-many relationship with QuizItem
    quiz_items: Mapped[list["SQLAlchemyQuizItem"]] = relationship(back_populates="item")


class SQLAlchemyGenre(Base):
    __tablename__ = "genres"

    genre_id: Mapped[int] = mapped_column(primary_key=True)
    genre_name: Mapped[str] = mapped_column(unique=True, index=True)

    # Many-to-many relationship with Item
    items: Mapped[list[SQLAlchemyItem]] = relationship(
        secondary=item_genre_mapper_table,
        back_populates="genres",
    )


class SQLAlchemyDeck(Base):
    __tablename__ = "decks"

    deck_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    deck_name: Mapped[str]

    # Many-to-many relationship with Item
    items: Mapped[list[SQLAlchemyItem]] = relationship(
        secondary=item_deck_mapper_table,
        back_populates="decks",
    )
    # Many-to-one relationship with User
    user: Mapped[SQLAlchemyUser] = relationship(back_populates="decks")
    # One-to-many relationship with Quiz
    quizzes: Mapped[list["SQLAlchemyQuiz"]] = relationship(back_populates="deck")


class SQLAlchemyQuizItem(Base):
    __tablename__ = "quiz_items"

    quiz_item_id: Mapped[int] = mapped_column(primary_key=True)
    quiz_id: Mapped[int] = mapped_column(ForeignKey("quizzes.quiz_id"))
    item_id: Mapped[int] = mapped_column(ForeignKey("items.item_id"))
    question_number: Mapped[int]
    choice_item_ids: Mapped[list[str]]
    correct_answer: Mapped[int]
    user_answer: Mapped[Optional[int]]
    answer_time: Mapped[Optional[int]]

    # Many-to-one relationship with Quiz
    quiz: Mapped["SQLAlchemyQuiz"] = relationship(back_populates="quiz_items")
    # Many-to-one relationship with Item
    item: Mapped[SQLAlchemyItem] = relationship(back_populates="quiz_items")


class SQLAlchemyQuiz(Base):
    __tablename__ = "quizzes"

    quiz_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    deck_id: Mapped[int] = mapped_column(ForeignKey("decks.deck_id"))
    quiz_type: Mapped[str]
    quiz_timestamp: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.now
    )

    # One-to-many relationship with QuizItem
    quiz_items: Mapped[list[SQLAlchemyQuizItem]] = relationship(back_populates="quiz")
    # Many-to-one relationship with User
    user: Mapped[SQLAlchemyUser] = relationship(back_populates="quizzes")
    # Many-to-one relationship with Deck
    deck: Mapped[SQLAlchemyDeck] = relationship(back_populates="quizzes")
