import uvicorn
from main import app
from app.core.config import settings

if __name__ == "__main__":
  uvicorn.run("main:app", host="0.0.0.0", port=settings.PORT, reload=True)

