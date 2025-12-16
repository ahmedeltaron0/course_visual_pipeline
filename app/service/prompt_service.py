from fastapi import UploadFile
from app.service.ai_service import AgentService
from app.schema.ai_schema import StoryboardOutput
from app.service.file_service import extract_file_videos_service

async def generate_prompts_service(file: UploadFile, agent: AgentService):
    videos = await extract_file_videos_service(file)
    return await agent.poke_agent(
        messages=videos,
        structured_output_format=StoryboardOutput,
        file=file
    )
