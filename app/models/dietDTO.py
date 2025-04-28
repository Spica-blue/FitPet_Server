from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class DietRequest(BaseModel):
  email: str
  date: date
  breakfast: Optional[str] = None
  lunch: Optional[str] = None
  dinner: Optional[str] = None

class DietResponse(BaseModel):
  email: str
  date: date
  breakfast: Optional[str]
  lunch: Optional[str]
  dinner: Optional[str]
  created_at: datetime

  class Config:
    orm_mode = True
