import datetime

from sqlalchemy import ForeignKey, Table, Column
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
  pass

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

class User(Base):
  __tablename__ = "users"

  user_id: Mapped[int] = mapped_column(primary_key=True)
  user_name: Mapped[str] = mapped_column(unique=True, index=True)
  email: Mapped[str] = mapped_column(unique=True, index=True)
  password: Mapped[str]
  full_name: Mapped[str]
  is_active: Mapped[bool] = mapped_column(default=True)
  is_superuser: Mapped[bool] = mapped_column(default=False)
  created_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now)
  updated_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now)

  # One-to-many relationship with UserLoginHistory
  user_login_history: Mapped[list["UserLoginHistory"]] = relationship(back_populates="user")
  # One-to-many relationship with Item
  items: Mapped[list["Item"]] = relationship(back_populates="user")
  # One-to-many relationship with Deck
  decks: Mapped[list["Deck"]] = relationship(back_populates="user")
  # One-to-many relationship with Test
  tests: Mapped[list["Test"]] = relationship(back_populates="user")


class UserLoginHistory(Base):
  __tablename__ = "user_login_history"

  user_login_history_id: Mapped[int] = mapped_column(primary_key=True)
  user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
  login_timestamp: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now)
  logout_timestamp: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now)
  ip_address: Mapped[str]

  # Many-to-one relationship with User
  user: Mapped[User] = relationship(back_populates="user_login_history")


class Item(Base):
  __tablename__ = "items"

  item_id: Mapped[int] = mapped_column(primary_key=True)
  user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
  english: Mapped[str]
  japanese: Mapped[str]
  grade: Mapped[int]
  created_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now)
  updated_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now)

  # Many-to-one relationship with User
  user: Mapped[User] = relationship(back_populates="items")
  # Many-to-many relationship with Genre
  genres: Mapped[list["Genre"]] = relationship(
    secondary=item_genre_mapper_table,
    back_populates="items",
  )
  # Many-to-many relationship with Deck
  decks: Mapped[list["Deck"]] = relationship(
    secondary=item_deck_mapper_table,
    back_populates="items",
  )
  # One-to-many relationship with TestItem
  test_items: Mapped[list["TestItem"]] = relationship(back_populates="item")

class Genre(Base):
  __tablename__ = "genres"

  genre_id: Mapped[int] = mapped_column(primary_key=True)
  genre_name: Mapped[str] = mapped_column(unique=True, index=True)

  # Many-to-many relationship with Item
  items: Mapped[list[Item]] = relationship(
    secondary=item_genre_mapper_table,
    back_populates="genres",
  )

class Deck(Base):
  __tablename__ = "decks"

  deck_id: Mapped[int] = mapped_column(primary_key=True)
  user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
  deck_name: Mapped[str]

  # Many-to-many relationship with Item
  items: Mapped[list[Item]] = relationship(
    secondary=item_deck_mapper_table,
    back_populates="decks",
  )
  # Many-to-one relationship with User
  user: Mapped[User] = relationship(back_populates="decks")
  # One-to-many relationship with Test
  tests: Mapped[list["Test"]] = relationship(back_populates="deck")


class TestItem(Base):
  __tablename__ = "test_items"

  test_item_id: Mapped[int] = mapped_column(primary_key=True)
  test_id: Mapped[int] = mapped_column(ForeignKey("tests.test_id"))
  item_id: Mapped[int] = mapped_column(ForeignKey("items.item_id"))
  question_number: Mapped[int]
  choice_item_ids: Mapped[list[int]]
  correct_answer: Mapped[int]
  user_answer: Mapped[int]
  answer_time: Mapped[int]

  # Many-to-one relationship with Test
  test: Mapped["Test"] = relationship(back_populates="test_items")
  # Many-to-one relationship with Item
  item: Mapped[Item] = relationship(back_populates="test_items")


class Test(Base):
  __tablename__ = "tests"

  test_id: Mapped[int] = mapped_column(primary_key=True)
  user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
  deck_id: Mapped[int] = mapped_column(ForeignKey("decks.deck_id"))
  test_type: Mapped[str]
  test_timestamp: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now)

  # One-to-many relationship with TestItem
  test_items: Mapped[list[TestItem]] = relationship(back_populates="test")
  # Many-to-one relationship with User
  user: Mapped[User] = relationship(back_populates="tests")
  # Many-to-one relationship with Deck
  deck: Mapped[Deck] = relationship(back_populates="tests")