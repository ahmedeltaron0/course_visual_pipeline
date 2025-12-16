from typing import Optional
from app.service.higgs_service import HiggsService

async def generate_video_service(
    image_url_1: str,
    image_url_2: Optional[str],
    prompt: Optional[str],
    higgs: HiggsService
):
    return await higgs.generate_kling_video(
        image_url=image_url_1,
        last_image_url=image_url_2,
        prompt=prompt
    )
