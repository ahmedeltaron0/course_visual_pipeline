import uuid
from sqlalchemy import Column, String, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.models.base import Base


class GenerationJob(Base):
    __tablename__ = "generation_jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    file_id = Column(UUID(as_uuid=True), ForeignKey("files.id"), nullable=False)
    prompt_id = Column(UUID(as_uuid=True), ForeignKey("prompts.id"), nullable=False)
    video_id = Column(UUID(as_uuid=True), unique=True, default=uuid.uuid4)
    status = Column(String, default="pending", nullable=False)

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
