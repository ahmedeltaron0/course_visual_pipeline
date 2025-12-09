import uuid
from datetime import datetime
from typing import List, Optional, Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from models.higgs_requests import HiggsRequest
from repositories.base_repo import BaseRepository


class HiggsRepository(BaseRepository[HiggsRequest]):
    def __init__(self, db: AsyncSession):
        super().__init__(HiggsRequest, db)

