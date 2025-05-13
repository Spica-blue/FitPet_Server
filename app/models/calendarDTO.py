from pydantic import BaseModel
from datetime import date as dt_date, datetime

class CalendarCreate(BaseModel):
  email: str
  date: dt_date
  note: str | None = None
  workout_success: bool = False

class CalendarRead(BaseModel):
  email: str
  date: dt_date
  note: str | None
  workout_success: bool
  created_at: datetime