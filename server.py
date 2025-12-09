import re
from io import BytesIO
from typing import List, Dict, Optional
import uuid

from fastapi import Depends, FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from docx import Document
import urllib.parse

from core.container import get_agent_service, get_higgs_service
from schema.ai_schema import StoryboardOutput
from service.ai_service import AgentService
from service.higgs_service import HiggsService

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
async def extract_text(file: UploadFile) -> StreamingResponse:
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
        return videos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.post("/generate_file_prompts")
async def generate_file_prompts(file: UploadFile = File(...),
                             agent_service: AgentService = Depends(get_agent_service),
                             ):
    if not file.filename.lower().endswith(".docx"):
        raise HTTPException(status_code=400, detail="Please upload a .docx file")
    results = await extract_text(file) 

    videos_prompts = await agent_service.poke_agent(messages= results,
                                    structured_output_format=StoryboardOutput,
                                    file = file)
    return videos_prompts

@app.post("/generate_images_for_file")
async def generate_images_for_file(file_id: uuid.UUID,
                                   video_number: Optional[int] = None,
                                    higgs_service: HiggsService = Depends(get_higgs_service),
                                    ):

    result = await higgs_service.generate_images_for_file(file_id=file_id, video_number=video_number)
    return result

@app.post("/generate_videos_from_images")
async def generate_images_for_file( image_url_1: str,
                                    image_url_2: str | None = None,
                                    prompt: str | None = None,
                                    higgs_service: HiggsService = Depends(get_higgs_service),
                                    ):

    result = await higgs_service.generate_kling_video(image_url=image_url_1,
                                                      last_image_url=image_url_2,
                                                      prompt=prompt)
    return result

