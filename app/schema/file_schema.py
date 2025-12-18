from pydantic import BaseModel
from typing import List, Dict, Any


class FrameSchema(BaseModel):
    frame_number: int
    frame_code: str
    frame_prompt: Dict[str, Any]


class ShotSchema(BaseModel):
    shot_number: int
    scene: str
    frames: List[FrameSchema]


class VideoSchema(BaseModel):
    video_number: int
    shots: List[ShotSchema]


class FileExtractResponseSchema(BaseModel):
    result: str
    data: List[VideoSchema]
