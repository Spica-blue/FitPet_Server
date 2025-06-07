from fastapi import APIRouter
from app.api.endpoints import users, gpt_recommend, pedometer, diet, calendar, pet, feed_inventory

router = APIRouter()

# 사용자 관련 API
router.include_router(users.router, prefix="/users")
router.include_router(gpt_recommend.router, prefix="/gpt")
router.include_router(pedometer.router, prefix="/pedometer")
router.include_router(diet.router, prefix="/diet")
router.include_router(calendar.router, prefix="/calendar")
router.include_router(pet.router, prefix="/pet")
router.include_router(feed_inventory.router, prefix="/feed_inventory")
