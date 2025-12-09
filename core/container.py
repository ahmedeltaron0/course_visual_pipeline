from typing import Any, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import Database
from models.agent import Agent, DocFiles
from models.frames import Frame
from models.shots import Shot
from models.videos import Video
from models.courses import Course
from models.higgs_requests import HiggsRequest
from repositories.agent_repo import AgentRepository
from repositories.doc_files_repo import DocFilesRepository
from repositories.higgs_repo import HiggsRepository
from service.ai_service import AgentService
from service.higgs_service import HiggsService

db = Database()

async def get_db_session() -> AsyncGenerator[AsyncSession, Any]:
    async for session in db.get_session():
        yield session

async def get_higgs_repository(
        session: AsyncSession = Depends(get_db_session),
) -> AsyncGenerator[HiggsRequest, Any]:
    yield HiggsRepository(session)


async def get_agent_repository(
        session: AsyncSession = Depends(get_db_session),
) -> AsyncGenerator[Agent, Any]:
    yield AgentRepository(session)

async def get_doc_files_repository(
        session: AsyncSession = Depends(get_db_session),
) -> AsyncGenerator[DocFiles, Any]:
    yield DocFilesRepository(session)




async def get_agent_service(
        db: AsyncSession = Depends(get_db_session),
        agent_repo: AgentRepository = Depends(get_agent_repository),
        doc_files_repo: DocFilesRepository = Depends(get_doc_files_repository),
) -> AsyncGenerator["AgentService", Any]:
    yield AgentService(db=db,
                    agent_repo=agent_repo,
                    doc_files_repo=doc_files_repo)
    
async def get_higgs_service(
        db: AsyncSession = Depends(get_db_session),
        higgs_repo: HiggsRepository = Depends(get_higgs_repository),
        agent_repo : AgentRepository = Depends(get_agent_repository),
) -> AsyncGenerator["HiggsService", Any]:
    yield HiggsService(db=db,
                       higgs_repo=higgs_repo,
                       agent_repo=agent_repo
                        )       