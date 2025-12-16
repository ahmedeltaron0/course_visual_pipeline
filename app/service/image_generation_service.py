from uuid import UUID
from typing import Optional
from app.service.higgs_service import HiggsService

async def generate_images_service(
    file_id: UUID,
    video_number: Optional[int],
    higgs: HiggsService
):
    return await higgs.generate_images_for_file(file_id, video_number)
