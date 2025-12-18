from fastapi import APIRouter
import uuid
from app.service.status_service import get_generation_status

router = APIRouter(prefix="/generation/status", tags=["Status"])


@router.get("/{video_id}")
async def get_status(video_id: uuid.UUID):
    return {
        "video_id": video_id,
        "status": await get_generation_status(video_id),
    }
