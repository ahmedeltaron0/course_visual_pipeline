import uuid

# Temporary in-memory store (will be replaced by DB later)
GENERATION_STATUS_STORE = {}


def set_generation_status(video_id: uuid.UUID, status: str) -> None:
    GENERATION_STATUS_STORE[str(video_id)] = status


def get_generation_status(video_id: uuid.UUID) -> str:
    return GENERATION_STATUS_STORE.get(str(video_id), "unknown")
