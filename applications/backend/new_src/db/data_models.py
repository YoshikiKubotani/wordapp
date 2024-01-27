import datetime

from sqlalchemy import ForeignKey, String, Integer, Boolean, DateTime, Column
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
  pass

class User(Base):
  __tablename__ = "users"

  user_id: Mapped[int] = mapped_column(primary_key=True, index=True)
  user_name: Mapped[str] = mapped_column(unique=True, index=True)
  email: Mapped[str] = mapped_column(unique=True, index=True)
  password: Mapped[str]
  full_name: Mapped[str]
  is_active: Mapped[bool] = mapped_column(default=True)
  is_superuser: Mapped[bool] = mapped_column(default=False)
  created_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now)
  updated_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now)

class Item(Base):
  __tablename__ = "items"

  item_id: Mapped[int] = mapped_column(primary_key=True, index=True)
  user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
  english: Mapped[str]
  japanese: Mapped[str]
  grade: Mapped[int]
  created_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now)
  updated_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now)