import uuid
from datetime import datetime
from typing import List, Optional, Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from models.agent import Agent
from repositories.base_repo import BaseRepository
from schema.ai_schema import AgentResponse


class AgentRepository(BaseRepository[Agent]):
    def __init__(self, db: AsyncSession):
        super().__init__(Agent, db)

    async def get_prompts_by_file_id(
        self, file_id: uuid.UUID, video_number: Optional[int] = None
    ) -> List[AgentResponse]:
        # Base query using file_id
        stmt = select(self.model).filter(self.model.file_id == file_id)

        # If video_number is provided → apply extra filter
        if video_number is not None:
            stmt = stmt.filter(self.model.video_number == video_number)

        result = await self.db.execute(stmt)
        return result.scalars().all()