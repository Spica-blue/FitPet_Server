from sqlmodel import SQLModel, Field
from datetime import date as dt_date

class PedometerRecord(SQLModel, table=True):
  __tablename__ = "pedometer"

  email: str = Field(foreign_key="users.email", primary_key=True)
  step_count: int
  date: dt_date = Field(primary_key=True)

