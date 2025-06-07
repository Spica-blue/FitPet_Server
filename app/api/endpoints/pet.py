from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.petDTO import PetCreate, PetRead, PetUpdate
from app.services.pet_service import PetService
from app.db.db import get_session

router = APIRouter()

@router.post(
  "/",
  response_model=PetRead,
  summary="새 Pet 생성",
  status_code=201,
  tags=["pet"]
)
async def create_pet(
  payload: PetCreate,
  db: AsyncSession = Depends(get_session)
):
  svc = PetService(db)
  existing = await svc.get_pet(payload.email)

  if existing:
    raise HTTPException(status_code=400, detail="Pet already exists")
  
  pet = await svc.create_pet(payload)
  return pet

@router.get(
  "/{email}",
  response_model=PetRead,
  summary="Pet 조회",
  tags=["pet"]
)
async def read_pet(
  email: str,
  db: AsyncSession = Depends(get_session)
):
  pet = await PetService(db).get_pet(email)
  
  if not pet:
    raise HTTPException(status_code=404, detail="Pet not found")
  
  return pet

@router.put(
  "/{email}",
  response_model=PetRead,
  summary="Pet 정보 업데이트",
  tags=["pet"]
)
async def update_pet(
  email: str,
  payload: PetUpdate,
  db: AsyncSession = Depends(get_session),
):
  pet = await PetService(db).update_pet(email, payload)

  if not pet:
    raise HTTPException(status_code=404, detail="Pet not found")
  
  return pet