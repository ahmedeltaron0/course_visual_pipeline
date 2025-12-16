from pydantic import BaseModel
import uuid


class GenerationStatusResponseSchema(BaseModel):
    video_id: uuid.UUID
    status: str
