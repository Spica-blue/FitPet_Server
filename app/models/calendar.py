from sqlmodel import SQLModel, Field
from typing import Optional
from sqlalchemy import Column, DateTime, func
from datetime import date as dt_date, datetime

class CalendarRecord(SQLModel, table=True):
  __tablename__ = 'calendar'

  email: str = Field(foreign_key='users.email', primary_key=True)
  date: dt_date = Field(primary_key=True)
  note: str | None = Field(default=None)
  workout_success: bool = Field(default=False)
  created_at: Optional[datetime] = Field(sa_column=Column(DateTime(timezone=False), server_default=func.now()))