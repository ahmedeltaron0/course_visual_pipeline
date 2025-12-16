from pydantic import BaseModel
import uuid


class ImageGenerationCreateSchema(BaseModel):
    """
    Request schema to start image/video generation
    """
    file_id: uuid.UUID
    prompt_id: uuid.UUID


class ImageGenerationResponseSchema(BaseModel):
    """
    Response schema for a generation job
    """
    file_id: uuid.UUID
    video_id: uuid.UUID
    status: str
