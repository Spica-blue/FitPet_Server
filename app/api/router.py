from fastapi import APIRouter
from app.api.endpoints import users

router = APIRouter()

# 사용자 관련 API
router.include_router(users.router, prefix="/users", tags=["users"])
