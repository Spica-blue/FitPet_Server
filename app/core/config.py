from pydantic_settings import BaseSettings

class Settings(BaseSettings):
  PROJECT_NAME: str = "FitPet API"

  # Database 설정
  DATABASE_URL: str
  
  # 포트 설정
  PORT: int = 8883

  class Config:
    env_file = ".env"
    env_file_encoding = "utf-8"

settings = Settings()
  

