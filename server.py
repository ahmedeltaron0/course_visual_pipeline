import re
from io import BytesIO
from typing import List, Dict

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from docx import Document
import urllib.parse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------------------
# 1) خريطة الكلمات الترتيبية العربية لأرقام
# ----------------------------------------

ARABIC_ORDINALS = {
    "الأول": 1,
    "الاول": 1,
    "الثاني": 2,
    "الثالث": 3,
    "الرابع": 4,
    "الخامس": 5,
    "السادس": 6,
    "السابع": 7,
    "الثامن": 8,
    "التاسع": 9,
    "العاشر": 10,
    "الحادي عشر": 11,
    "الثاني عشر": 12,
}

# ----------------------------------------
# 2) تحويل docx إلى نص
# ----------------------------------------

def docx_to_text(file_obj) -> str:
    document = Document(file_obj)
    paragraphs = [p.text for p in document.paragraphs]
    return "\n".join(paragraphs)

# ----------------------------------------
# 3) استخراج مقاطع الفيديو بدعم (الفيديو الأول)
# ----------------------------------------

def extract_videos_sections(full_text: str) -> List[Dict]:
    """
    يقطع النص على شكل:
    الفيديو الأول
    الفيديو الثاني
    الفيديو الثالث
    ...
    """

    # نعمل regex يدعم الكلمات الترتيبية
    ordinal_pattern = "|".join(ARABIC_ORDINALS.keys())
    video_regex = rf"(الفيديو)\s+({ordinal_pattern})\s*"
    pattern = re.compile(video_regex)

    matches = list(pattern.finditer(full_text))

    if not matches:
        return []

    sections = []

    for i, match in enumerate(matches):
        ordinal_word = match.group(2)
        video_number = ARABIC_ORDINALS.get(ordinal_word, None)

        start_index = match.start()

        if i + 1 < len(matches):
            end_index = matches[i + 1].start()
        else:
            end_index = len(full_text)

        video_text = full_text[start_index:end_index].strip()

        sections.append({
            "video_number": video_number,
            "ordinal": ordinal_word,
            "raw_section_text": video_text
        })

    return sections

# ----------------------------------------
# 4) Endpoint: .docx → .txt (فيديوهات فقط)
# ----------------------------------------

@app.post("/extract-script-txt")
async def extract_script_txt(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".docx"):
        raise HTTPException(status_code=400, detail="Please upload a .docx file")

    try:
        contents = await file.read()
        full_text = docx_to_text(BytesIO(contents))

        # 0) قص أي شيء بعد Story Board
        marker = "Story Board"
        idx = full_text.find(marker)
        if idx != -1:
            full_text = full_text[:idx]

        # 1) استخراج الفيديوهات
        videos = extract_videos_sections(full_text)
        if not videos:
            raise HTTPException(
                status_code=400,
                detail="No video sections found using 'الفيديو الأول / الثاني ...'."
            )

        # 2) دمج المقاطع
        merged = "\n\n".join(v["raw_section_text"] for v in videos)

        # 3) تحويل UTF-8
        txt_bytes = merged.encode("utf-8")
        txt_stream = BytesIO(txt_bytes)

        # 4) اسم الملف نفس اسم الإدخال
        orig_name = file.filename.rsplit(".", 1)[0]
        download_utf8 = f"{orig_name}.txt"

        # ASCII fallback
        ascii_name = re.sub(r"[^A-Za-z0-9_\-\.]+", "_", download_utf8)
        encoded_utf8_name = urllib.parse.quote(download_utf8)

        headers = {
            "Content-Disposition":
                f"attachment; filename={ascii_name}; filename*=UTF-8''{encoded_utf8_name}"
        }

        return StreamingResponse(
            txt_stream,
            media_type="text/plain; charset=utf-8",
            headers=headers,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
