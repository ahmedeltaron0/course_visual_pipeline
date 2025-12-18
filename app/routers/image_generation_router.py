from fastapi import APIRouter, Depends
from app.config.container import get_higgs_service
from app.service.higgs_service import HiggsService
from app.schema.image_generation_schema import (
    ImageGenerationCreateSchema as GenerationCreateSchema,
    ImageGenerationResponseSchema as GenerationResponseSchema,
)

router = APIRouter(prefix="/generation/images", tags=["Generation"])


@router.post("", response_model=GenerationResponseSchema)
async def generate_images(
    payload: GenerationCreateSchema,
    higgs_service: HiggsService = Depends(get_higgs_service),
):
    return await higgs_service.generate_images_for_file(
        file_id=payload.file_id,
        video_number=None,
    )
