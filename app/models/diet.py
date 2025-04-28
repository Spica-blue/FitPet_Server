from sqlmodel import SQLModel, Field, Column
from sqlalchemy import Date, DateTime, func, TEXT

from typing import Optional
from datetime import date as date_, datetime

class Diet(SQLModel, table=True):
  __tablename__ = "diet"

  email: str = Field(foreign_key="users.email", primary_key=True)
  date: date_ = Field(primary_key=True, nullable=False)
  breakfast: Optional[str] = Field(default=None, sa_column=Column(TEXT, nullable=True))
  lunch: Optional[str] = Field(default=None, sa_column=Column(TEXT, nullable=True))
  dinner: Optional[str] = Field(default=None, sa_column=Column(TEXT, nullable=True))
  created_at: Optional[datetime] = Field(sa_column=Column(DateTime(timezone=False), server_default=func.now()))
  updated_at: Optional[datetime] = Field(sa_column=Column(DateTime(timezone=False), server_default=func.now(), onupdate=func.now()))