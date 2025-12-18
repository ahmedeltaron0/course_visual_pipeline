from sqlalchemy.ext.asyncio import AsyncSession

from app.repo.base_repo import BaseRepository
from app.models.file import File


class FileRepository(BaseRepository[File]):
    def __init__(self, db: AsyncSession):
        super().__init__(File, db)
