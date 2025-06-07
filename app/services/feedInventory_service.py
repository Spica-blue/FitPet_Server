from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.models.feed_inventory import FeedInventory 

class FeedInventoryService:
  def __init__(self, db: AsyncSession):
    self.db = db

  async def get_inventory(self, email: str) -> FeedInventory | None:
    stmt = select(FeedInventory).where(FeedInventory.email == email)
    result = await self.db.execute(stmt)
    return result.scalar_one_or_none()

  async def create_inventory(self, email: str) -> FeedInventory:
    """
    최초 한 번, email로 feed_inventory 레코드를 생성합니다.
    이미 있으면 기존 레코드를 반환합니다.
    """
    # 중복 시 IntegrityError 발생 방지
    existing = await self.get_inventory(email)
    if existing:
      return existing

    new = FeedInventory(email=email)
    self.db.add(new)

    try:
      # INSERT SQL 실행
      await self.db.flush()
      # 커밋해서 영속화
      await self.db.commit()
      # 객체에 디폴트 값 등을 채워서 새로고침
      await self.db.refresh(new)
      return new
    except IntegrityError:
      await self.db.rollback()
      # race condition 으로 이미 생성된 경우 다시 조회
      return await self.get_inventory(email)

  async def update_inventory(self, email: str, payload: dict) -> FeedInventory | None:
    stmt = (
      update(FeedInventory)
      .where(FeedInventory.email == email)
      .values(**payload)
      .returning(FeedInventory)
    )
    result = await self.db.execute(stmt)
    await self.db.commit()
    updated = result.fetchone()
    return updated[0] if updated else None