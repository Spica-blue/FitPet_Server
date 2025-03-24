from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder
from passlib.context import CryptContext
from sqlmodel import select

from db.db import get_session, init_db
from schemas import RegisterRequest
from model.models import User

app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.on_event("startup")
async def on_startup():
  await init_db()

@app.post("/register")
async def register_user(data: RegisterRequest, session: AsyncSession = Depends(get_session)):
  # 이메일 중복 확인
  result = await session.execute(
    select(User).where(User.email == data.email)
  )
  existing = result.scalars().first()
  if existing:
    raise HTTPException(status_code=400, detail="이미 등록된 이메일입니다")
  
  user = User(
    name=data.name,
    email=data.email,
    password=pwd_context.hash(data.password),
  )
  
  session.add(user)
  await session.commit()
  await session.refresh(user)

  user_dict = jsonable_encoder(user)
  user_dict.pop("password")
  return user_dict
  

