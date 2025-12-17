import uuid

from app.db.database import SessionLocal
from app.repo.generation_repo import GenerationRepository


async def get_generation_status(video_id: uuid.UUID) -> str:
    """
    Get the current status of a generation job by video_id.
    """
    db = SessionLocal()
    try:
        repo = GenerationRepository(db)

        job = await repo.get_by_video_id(video_id)

        if not job:
            return "unknown"

        return job.status

    finally:
        await db.close()
