from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.feedInventoryDTO import FeedInventoryCreate, FeedInventoryRead, FeedInventoryUpdate
from app.services.feedInventory_service import FeedInventoryService
from app.db.db import get_session

router = APIRouter()

@router.post(
  "/",
  response_model=FeedInventoryRead,
  summary="Feed Inventory 최초 생성",
  tags=["feed_inventory"]
)
async def create_inventory(
  payload: FeedInventoryCreate,
  session: AsyncSession = Depends(get_session),
):
  svc = FeedInventoryService(session)
  inv = await svc.create_inventory(payload.email)
  return inv

@router.get(
  "/{email}",
  response_model=FeedInventoryRead,
  summary="특정 유저의 Feed Inventory 조회",
  tags=["feed_inventory"]
)
async def read_inventory(
  email: str,
  session: AsyncSession = Depends(get_session),
):
  svc = FeedInventoryService(session)
  inv = await svc.get_inventory(email)
  if not inv:
    raise HTTPException(404, "Inventory not found")
  return inv

@router.patch(
  "/{email}",
  response_model=FeedInventoryRead,
  summary="Feed Inventory 업데이트 (먹이 획득/사용)",
  tags=["feed_inventory"]
)
async def update_inventory(
  email: str,
  payload: FeedInventoryUpdate,
  session: AsyncSession = Depends(get_session),
):
  svc = FeedInventoryService(session)
  inv = await svc.update_inventory(email, payload.dict(exclude_unset=True))
  if not inv:
    raise HTTPException(404, "Inventory not found")
  return inv