import uuid
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.repo.base_repo import BaseRepository
from app.models.prompt import Prompt


class PromptRepository(BaseRepository[Prompt]):
    def __init__(self, db: AsyncSession):
        super().__init__(Prompt, db)

    async def get_by_file_id(
        self,
        file_id: uuid.UUID,
        video_number: Optional[int] = None
    ) -> List[Prompt]:
        stmt = select(self.model).filter(self.model.file_id == file_id)

        if video_number is not None:
            stmt = stmt.filter(self.model.video_number == video_number)

        result = await self.db.execute(stmt)
        return result.scalars().all()
