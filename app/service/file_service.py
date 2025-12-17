from io import BytesIO
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

def _docx_to_text(file_obj) -> str:
    document = Document(file_obj)
    return "\n".join(p.text for p in document.paragraphs)


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
            "video_number": ARABIC_ORDINALS.get(ordinal),
            "ordinal": ordinal,
            "raw_section_text": text[start:end].strip(),
        })

    return sections



async def extract_file_videos_service(file: UploadFile) -> dict:
    """
    Validate file type, extract video sections,
    and persist file metadata in the database.
    """

    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is missing")

    filename = file.filename.lower()
    _, ext = os.path.splitext(filename)

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

    db = SessionLocal()
    try:
        repo = FileRepository(db)

        file_record: File = await repo.create({
            "filename": file.filename,
        })

        await db.commit()

    finally:
        await db.close()

    return {
        "file_id": file_record.id,
        "videos": videos,
    }