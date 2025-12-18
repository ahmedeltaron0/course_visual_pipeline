from app.schema.file_schema import FileExtractResponseSchema
from fastapi import APIRouter, File, UploadFile
from app.service.file_service import extract_file_videos_service

router = APIRouter(prefix="/files", tags=["Files"])

@router.post("/extract", response_model=FileExtractResponseSchema)
async def extract_by_params(file: UploadFile = File(...)):
    return await extract_file_videos_service(file)
