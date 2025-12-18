from sqlalchemy.ext.asyncio import AsyncSession

from app.repo.base_repo import BaseRepository
from app.models.higgs import Higgs


class HiggsRepository(BaseRepository[Higgs]):
    """
    Repository for Higgs image/video generation records.
    """

    def __init__(self, db: AsyncSession):
        super().__init__(Higgs, db)
