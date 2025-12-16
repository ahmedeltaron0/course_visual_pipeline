from fastapi import APIRouter, UploadFile, File, HTTPException
from app.service.file_service import extract_file_videos_service
from app.schema.file_schema import FileExtractResponseSchema

router = APIRouter(prefix="/files", tags=["Files"])

@router.post("/extract", response_model=FileExtractResponseSchema)
async def extract_file(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".docx"):
        raise HTTPException(status_code=400, detail="Only .docx files allowed")

    result = await extract_file_videos_service(file)
    return {"videos": result}
