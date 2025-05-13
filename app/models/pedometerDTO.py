from pydantic import BaseModel
from datetime import date

class PedometerCreate(BaseModel):
  email: str
  step_count: int

class PedometerRead(BaseModel):
  email: str
  step_count: int
  date: date
