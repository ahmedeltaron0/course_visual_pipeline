import re
from io import BytesIO
from typing import List, Dict
from docx import Document
from fastapi import UploadFile, HTTPException

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
            "raw_section_text": text[start:end].strip()
        })
    return sections

async def extract_file_videos_service(file: UploadFile):
    content = await file.read()
    text = _docx_to_text(BytesIO(content))

    videos = _extract_video_sections(text)
    if not videos:
        raise HTTPException(400, "No video sections found")

    return videos
