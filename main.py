from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi import status
from contextlib import asynccontextmanager

from app.api.router import router
from app.core.config import settings
from app.db.db import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
  print("🚀 앱 시작됨: DB 초기화 중...")
  await init_db()
  print("✅ DB 초기화 완료!")
  yield
  print("👋 앱 종료됨")

def create_app() -> FastAPI:
  app = FastAPI(
    title=settings.PROJECT_NAME,
    description="FitPet 관리 API 서버",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
  )

  app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
  )

  app.include_router(router, prefix="/api")

  return app

app = create_app()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
  print("❌ 요청 검증 에러 발생!")
  print("요청 바디:", await request.body())
  print("에러 상세:", exc.errors())
  return JSONResponse(
      status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
      content={"detail": exc.errors()},
  )
