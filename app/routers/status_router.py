from fastapi import APIRouter
import uuid

from app.schema.status_schema import GenerationStatusResponseSchema
from app.service.status_service import get_generation_status

router = APIRouter(prefix="/generation/status", tags=["Generation Status"])


@router.get("/{video_id}", response_model=GenerationStatusResponseSchema)
async def get_status(video_id: uuid.UUID):
    status = get_generation_status(video_id)
    return {
        "video_id": video_id,
        "status": status
    }
