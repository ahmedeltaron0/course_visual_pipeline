from fastapi import APIRouter, Depends
from typing import Optional
from app.config.container import get_higgs_service
from app.service.video_generation_service import generate_video_service
from app.service.higgs_service import HiggsService

router = APIRouter(prefix="/generation/video", tags=["Generation"])

@router.post("")
async def generate_video(
    image_url_1: str,
    image_url_2: Optional[str] = None,
    prompt: Optional[str] = None,
    higgs: HiggsService = Depends(get_higgs_service),
):
    return await generate_video_service(image_url_1, image_url_2, prompt, higgs)
