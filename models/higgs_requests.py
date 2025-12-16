import uuid
from sqlalchemy import Column, Integer, Text, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from core.database import Base


class HiggsRequest(Base):
    __tablename__ = "higgs_requests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    frame_id = Column(UUID(as_uuid=True), ForeignKey("frames.id"), nullable=False)
    request_id = Column(UUID(as_uuid=True), nullable=False)
    file_name = Column(Text)
    video_number = Column(Integer, nullable=False)
    shot_number = Column(Integer, nullable=False)
    frame_number = Column(Integer, nullable=False)

    status_url = Column(Text)
    cancel_url = Column(Text)
    status = Column(Text)
    request_body = Column(JSONB)
    response_body = Column(JSONB)
    prompt = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    frame = relationship("Frame", back_populates="higgs_requests")
