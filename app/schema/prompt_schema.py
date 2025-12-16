from pydantic import BaseModel
from typing import List
import uuid
from datetime import datetime

from app.schema.ai_schema import StoryboardOutput


class PromptResponseSchema(BaseModel):
    """
    Response schema for prompt generation endpoint.
    """

    id: uuid.UUID
    filename: str
    file_id: uuid.UUID
    video_number: int
    prompt: StoryboardOutput
    created_at: datetime
