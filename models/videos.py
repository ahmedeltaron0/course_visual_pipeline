import uuid
from sqlalchemy import Column, Text, TIMESTAMP, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from core.database import Base


class Video(Base):
    __tablename__ = "videos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id"), nullable=False)
    video_number = Column(Integer, nullable=False)
    title = Column(Text)
    script_original = Column(Text)
    script_clean = Column(Text)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    course = relationship("Course", back_populates="videos")
    shots = relationship("Shot", back_populates="video", cascade="all, delete-orphan")
