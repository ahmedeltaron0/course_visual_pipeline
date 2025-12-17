import uuid
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.repo.base_repo import BaseRepository
from app.models.generation_job import GenerationJob


class GenerationRepository(BaseRepository[GenerationJob]):
    def __init__(self, db: AsyncSession):
        super().__init__(GenerationJob, db)

    async def create_generation_job(
        self,
        video_id: uuid.UUID,
        file_id: uuid.UUID,
        prompt_id: uuid.UUID,
        status: str
    ) -> GenerationJob:
        return await self.create({
            "video_id": video_id,
            "file_id": file_id,
            "prompt_id": prompt_id,
            "status": status,
        })

    async def update_status(
        self,
        video_id: uuid.UUID,
        status: str
    ) -> Optional[GenerationJob]:
        stmt = select(self.model).filter(self.model.video_id == video_id)
        result = await self.db.execute(stmt)
        job = result.scalars().first()

        if not job:
            return None

        job.status = status
        await self.db.flush()
        await self.db.refresh(job)
        return job

    async def get_by_video_id(
        self,
        video_id: uuid.UUID
    ) -> Optional[GenerationJob]:
        stmt = select(self.model).filter(self.model.video_id == video_id)
        result = await self.db.execute(stmt)
        return result.scalars().first()
