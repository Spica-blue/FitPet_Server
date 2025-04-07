from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime, func
from typing import Optional
from datetime import datetime

class GPTRecommendation(SQLModel, table=True):
  email: str = Field(primary_key=True, foreign_key="users.email")
  recommendations: dict
  created_at: Optional[datetime] = Field(sa_column=Column(DateTime(timezone=False), server_default=func.now()))

