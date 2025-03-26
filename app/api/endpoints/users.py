from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.db import get_session
from app.models.userDTO import SocialUserRequest
from app.services.user_service import UserService
from app.models.user import SocialUser

router = APIRouter()

@router.get(
  "/{email}",
  response_model=SocialUser,
  summary="이메일로 사용자 조회",
  description="주어진 이메일로 사용자를 조회합니다.",
  tags=["users"]
)
async def get_user_by_email(
  email: str,
  session: AsyncSession = Depends(get_session)
):
  try:
    user_service = UserService(db=session)
    user = await user_service.get_by_email(email)

    if not user:
      print(f"[NOT FOUND] '{email}' 에 해당하는 사용자 없음")
      raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

    print(f"[GET USER] 이메일로 조회됨: {user.email}")
    return user
  
  except HTTPException as e:
    raise e
  
  except Exception as e:
    print("[ERROR] 사용자 조회 중 서버 에러:", str(e))
    raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post(
  "/",
  response_model=SocialUser,
  summary="소셜 로그인 사용자 등록",
  description="소셜 로그인으로 새로 가입한 사용자를 저장합니다.",
  tags=["users"]
)
async def create_user(
  user_data: SocialUserRequest,
  session: AsyncSession = Depends(get_session)
):
  try:
    user_service = UserService(db=session)
    existing_user = await user_service.get_by_id(user_data.id)

    if existing_user:
      raise HTTPException(status_code=400, detail="이미 가입된 사용자입니다.")

    user = await user_service.create_user(user_data)
    print(f"✅ [CREATE] 유저 '{user.id}' 생성 완료")
    return user
  except Exception as e:
    print("❌ create_user error:", str(e))
    raise HTTPException(status_code=500, detail="Internal Server Error")

# 기존 사용자 로그인(갱신) 
@router.post(
  "/login",
  response_model=SocialUser,
  summary="소셜 로그인 사용자 로그인",
  description="이미 존재하는 사용자의 마지막 로그인 시간을 갱신합니다.",
  tags=["users"]
)
async def login_user(
  user_data: SocialUserRequest,
  session: AsyncSession = Depends(get_session)
):
  try:
    user_service = UserService(db=session)
    user = await user_service.update_last_login(user_data.id)

    if not user:
      raise HTTPException(status_code=404, detail="가입되지 않은 사용자입니다.")

    print(f"♻️ [LOGIN] 유저 '{user.id}' 로그인 시간 갱신 완료")
    return user
  except Exception as e:
    print("❌ login_user error:", str(e))
    raise HTTPException(status_code=500, detail="Internal Server Error")
  
@router.delete(
  "/{email}",
  response_model=dict,
  summary="이메일로 사용자 삭제",
  description="이메일을 기반으로 사용자를 삭제합니다.",
  tags=["users"]
)
async def delete_user_by_email(
  email: str,
  session: AsyncSession = Depends(get_session)
):
  try:
    user_service = UserService(db=session)
    user = await user_service.get_by_email(email)

    if not user:
      print(f"[DELETE] '{email}' 에 해당하는 사용자 없음")
      raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    
    await user_service.delete(user)
    print(f"[DELETE] 사용자 '{email}' 삭제 완료")
    return {"message": f"{email} 삭제 완료"}
  
  except HTTPException as e:
    raise e

  except Exception as e:
    print("delete_user_by_email error:", str(e))
    raise HTTPException(status_code=500, detail="Internal Server Error")
