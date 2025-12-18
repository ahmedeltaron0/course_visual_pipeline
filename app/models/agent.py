import uuid
from sqlalchemy import Column, Integer, Text, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func

from app.models.base import Base


class Agent(Base):
    __tablename__ = "agents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    prompt = Column(JSONB, nullable=True)
    filename = Column(Text, nullable=True)
    video_number = Column(Integer, nullable=False)

    file_id = Column(UUID(as_uuid=True), ForeignKey("files.id"), nullable=False)

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
