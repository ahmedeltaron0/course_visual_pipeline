from io import BytesIO
import os
import re
from typing import List, Dict

from fastapi import UploadFile, HTTPException
from docx import Document

from app.db.database import SessionLocal
from app.repo.file_repo import FileRepository
from app.models.file import File
from app.config.settings import settings


ARABIC_ORDINALS = {
    "الأول": 1, "الاول": 1, "الثاني": 2, "الثالث": 3,
    "الرابع": 4, "الخامس": 5, "السادس": 6,
    "السابع": 7, "الثامن": 8, "التاسع": 9, "العاشر": 10
}


# ---------- Helpers ----------

def _docx_to_text(file_obj) -> str:
    document = Document(file_obj)
    return "\n".join(p.text.strip() for p in document.paragraphs if p.text.strip())


def _extract_video_sections(text: str) -> List[Dict]:
    ordinal_pattern = "|".join(ARABIC_ORDINALS.keys())
    pattern = re.compile(rf"(الفيديو)\s+({ordinal_pattern})")

    matches = list(pattern.finditer(text))
    if not matches:
        return []

    sections = []
    for i, match in enumerate(matches):
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        ordinal = match.group(2)

        sections.append({
            "video_number": ARABIC_ORDINALS[ordinal],
            "raw_text": text[start:end].strip(),
        })

    return sections


def _build_storyboard_json(videos: List[Dict]) -> List[Dict]:
    """
    Temporary deterministic storyboard builder.
    This will be replaced by AI later.
    """

    storyboard = []

    for video in videos:
        video_number = video["video_number"]

        shots = []
        for shot_number in range(1, 5):  # 4 shots
            frames = []

            for frame_number in range(1, 4):  # 3 frames
                frames.append({
                    "frame_number": frame_number,
                    "frame_code": f"v{video_number}s{shot_number}f{frame_number}",
                    "frame_prompt": {
                        "style": "Ultra-realistic cinematic style",
                        "camera_lens": "35mm",
                        "environment": "Training environment",
                        "characters": "Safety trainer",
                        "scene": f"Video {video_number}, Shot {shot_number}, Frame {frame_number}",
                        "camera": "16:9",
                        "lighting": "Soft industrial lighting",
                        "details": "Educational safe setup",
                        "extra_details": "Consistent visuals"
                    }
                })

            shots.append({
                "shot_number": shot_number,
                "scene": f"Scene description for shot {shot_number}",
                "frames": frames
            })

        storyboard.append({
            "video_number": video_number,
            "shots": shots
        })

    return storyboard


# ---------- Main Service ----------

async def extract_file_videos_service(file: UploadFile) -> dict:
    """
    Upload file → extract content → persist metadata
    → return storyboard JSON
    """

    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is missing")

    _, ext = os.path.splitext(file.filename.lower())
    if ext not in settings.ALLOWED_FILE_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File type '{ext}' is not supported",
        )

    content = await file.read()

    if ext == ".docx":
        text = _docx_to_text(BytesIO(content))
    elif ext in {".txt", ".md"}:
        text = content.decode("utf-8", errors="ignore")
    else:
        raise HTTPException(
            status_code=400,
            detail=f"Parsing for '{ext}' is not implemented yet",
        )

    videos = _extract_video_sections(text)
    if not videos:
        raise HTTPException(status_code=400, detail="No video sections found")

    # ---- Persist file metadata ----
    db = SessionLocal()
    try:
        repo = FileRepository(db)
        file_record: File = await repo.create({
            "filename": file.filename
        })
        await db.commit()
    finally:
        await db.close()

    # ---- Build final output ----
    storyboard_data = _build_storyboard_json(videos)

    return {
        "result": "success",
        "data": storyboard_data
    }
