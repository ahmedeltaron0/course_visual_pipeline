from pydantic import BaseModel
from typing import List


class VideoSectionSchema(BaseModel):
    video_number: int
    ordinal: str
    raw_section_text: str


class FileExtractResponseSchema(BaseModel):
    videos: List[VideoSectionSchema]
