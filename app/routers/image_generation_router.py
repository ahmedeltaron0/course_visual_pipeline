from fastapi import APIRouter
from app.schema.image_generation_schema import (
    GenerationCreateSchema,
    GenerationResponseSchema
)
from app.service.image_generation_service import generate_images_service

router = APIRouter(prefix="/generation/images", tags=["Generation"])


@router.post("", response_model=GenerationResponseSchema)
async def generate_images(payload: GenerationCreateSchema):
    return await generate_images_service(payload)
