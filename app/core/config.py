from pydantic_settings import BaseSettings

class Settings(BaseSettings):
  DATABASE_URL: str
  
  PORT: int = 8883

  class Config:
    env_file = ".env"
    env_file_encoding = "utf-8"

settings = Settings()
  

