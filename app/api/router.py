from fastapi import APIRouter
from app.api.endpoints import users, gpt_recommend

router = APIRouter()

# 사용자 관련 API
router.include_router(users.router, prefix="/users")
router.include_router(gpt_recommend.router, prefix="/gpt")
