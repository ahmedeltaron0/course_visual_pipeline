import uuid
from sqlalchemy import Column, Integer, String, JSON, ForeignKey, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.models.base import Base


class Higgs(Base):
    __tablename__ = "higgs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    file_id = Column(UUID(as_uuid=True), ForeignKey("files.id"), nullable=False)
    video_number = Column(Integer, nullable=True)
    shot_number = Column(Integer, nullable=True)
    frame_number = Column(Integer, nullable=True)
    prompt = Column(JSON, nullable=True)
    response = Column(JSON, nullable=True)
    status = Column(String, nullable=True)

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
