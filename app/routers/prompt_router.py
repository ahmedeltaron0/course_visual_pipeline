from fastapi import APIRouter, UploadFile, File, Depends
from typing import List

from app.service.prompt_service import generate_prompts_service
from app.config.container import get_agent_service
from app.service.ai_service import AgentService
from app.schema.prompt_schema import PromptResponseSchema

router = APIRouter(prefix="/prompts", tags=["Prompts"])


@router.post("/generate", response_model=List[PromptResponseSchema])
async def generate_prompts(
    file: UploadFile = File(...),
    agent: AgentService = Depends(get_agent_service)
):
    return await generate_prompts_service(file, agent)
