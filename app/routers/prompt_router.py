from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schema.prompt_schema import (
    GeneratePromptRequestSchema,
    GeneratePromptResponseSchema,
)
from app.service.prompt_service import generate_prompts_service

router = APIRouter(
    prefix="/prompts",
    tags=["Prompts"],
)


@router.post(
    "/generate",
    response_model=GeneratePromptResponseSchema,
)
async def generate_prompts(
    payload: GeneratePromptRequestSchema,
    db: AsyncSession = Depends(get_db),
):
    return await generate_prompts_service(
        db=db,
        file_id=payload.file_id,
        video_number=payload.video_number,
        num_of_shots=payload.num_of_shots,
    )
