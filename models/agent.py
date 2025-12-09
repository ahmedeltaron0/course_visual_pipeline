import uuid
from sqlalchemy import Column, TIMESTAMP, Integer, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from core.database import Base


class Agent(Base):
    __tablename__ = "agent"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    prompt = Column(JSONB, nullable=True)
    filename = Column(Text, nullable=True)
    video_number = Column(Integer, nullable=False)
    file_id = Column(UUID(as_uuid=True), foreign_key="doc_files.id" ,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)

class DocFiles(Base):
    __tablename__ = "doc_files"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)

