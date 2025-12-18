from pydantic import BaseModel
from typing import List
import uuid


class GeneratePromptRequestSchema(BaseModel):
    file_id: uuid.UUID
    video_number: int
    num_of_shots: int


class FramePromptSchema(BaseModel):
    frame_number: int
    frame_code: str
    prompt: str


class ShotPromptSchema(BaseModel):
    shot_number: int
    scene: str
    frames: List[FramePromptSchema]


class GeneratePromptResponseSchema(BaseModel):
    result: str
    file_id: uuid.UUID
    video_number: int
    shots: List[ShotPromptSchema]
