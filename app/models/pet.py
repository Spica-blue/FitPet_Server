from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class Pet(SQLModel, table=True):
  __tablename__ = "pet"

  email: str = Field(foreign_key="users.email", primary_key=True)
  pet_type: str
  satiety: int = Field(default=50, ge=0, le=100)
  created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)