from fastapi import APIRouter, Depends
from app.config.container import get_higgs_service
from app.service.higgs_service import HiggsService

router = APIRouter(prefix="/generation/videos", tags=["Generation"])


@router.post("")
async def generate_video(
    image_url: str,
    higgs_service: HiggsService = Depends(get_higgs_service),
):
    return await higgs_service.generate_kling_video(image_url=image_url)
