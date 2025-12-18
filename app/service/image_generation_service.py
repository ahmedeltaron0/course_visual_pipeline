import uuid

from app.schema.image_generation_schema import GenerationCreateSchema
from app.repo.generation_repo import GenerationRepository
from app.db.database import SessionLocal


async def generate_images_service(
    payload: GenerationCreateSchema
) -> dict:
    """
    Start a new image generation job.
    """

    # Generate a new video_id
    video_id = uuid.uuid4()

    # Open DB session
    db = SessionLocal()
    try:
        repo = GenerationRepository(db)

        # Create generation job with initial status
        await repo.create_generation_job(
            video_id=video_id,
            file_id=payload.file_id,
            prompt_id=payload.prompt_id,
            status="pending"
        )

        # Commit transaction
        await db.commit()

    finally:
        # Always close DB session
        await db.close()

    # Return response (matches schema)
    return {
        "file_id": payload.file_id,
        "video_id": video_id,
        "status": "pending"
    }
