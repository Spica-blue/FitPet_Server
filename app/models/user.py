from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime, func
from typing import Optional
from datetime import datetime


class SocialUser(SQLModel, table=True):
  __tablename__ = "users"

  id: str = Field(primary_key=True)   # 카카오 / 네이버의 고유 id
  login_type: str   # "kakao" 또는 "naver"
  nickname: Optional[str] = None
  email: Optional[str] = Field(default=None, index=True)
  profile_image: Optional[str] = None
  created_at: Optional[datetime] = Field(sa_column=Column(DateTime(timezone=False), server_default=func.now()))
  last_login_at: Optional[datetime] = Field(sa_column=Column(DateTime(timezone=False), onupdate=func.now()))

