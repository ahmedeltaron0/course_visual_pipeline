import uuid
from sqlalchemy import (
    Column, Text, TIMESTAMP, Integer, ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from core.database import Base


class Frame(Base):
    __tablename__ = "frames"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    shot_id = Column(UUID(as_uuid=True), ForeignKey("shots.id"), nullable=False)
    frame_number = Column(Integer, nullable=False)
    frame_code = Column(Text, nullable=False)
    gpt_prompt = Column(Text)
    status = Column(Text, default="draft")
    higgs_request_id = Column(Text)
    higgs_status_url = Column(Text)
    higgs_cancel_url = Column(Text)
    higgs_last_status = Column(Text)
    image_url = Column(Text)
    image_storage_path = Column(Text)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    shot = relationship("Shot", back_populates="frames")
    higgs_requests = relationship(
        "HiggsRequest", back_populates="frame",
        cascade="all, delete-orphan"
    )
