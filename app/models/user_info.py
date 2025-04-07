from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime, func
from sqlalchemy.dialects.postgresql import JSONB
from typing import List, Optional
from datetime import datetime, date

class UserInfo(SQLModel, table=True):
  __tablename__ = "user_info"

  email: str = Field(primary_key=True, index=True, foreign_key="users.email")
  gender: str
  age: int
  height: float
  activity_level: str
  current_weight: float
  target_weight: float
  target_date: Optional[date]
  target_calories: int
  diet_type: str
  diet_intensity: Optional[str] = None
  allergy: Optional[List[str]] = Field(default_factory=list, sa_column=Column(JSONB))
  created_at: Optional[datetime] = Field(sa_column=Column(DateTime(timezone=False), server_default=func.now()))
  updated_at: Optional[datetime] = Field(sa_column=Column(DateTime(timezone=False), server_default=func.now(), onupdate=func.now()))

