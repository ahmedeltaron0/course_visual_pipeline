from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import engine
from app.models.base import Base

from app.routers.file_router import router as file_router
from app.routers.prompt_router import router as prompt_router
from app.routers.image_generation_router import router as image_generation_router
from app.routers.video_generation_router import router as video_generation_router
from app.routers.status_router import router as status_router

app = FastAPI(title="Course Visual Pipeline", version="1.0.0")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # change in production
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(file_router)
app.include_router(prompt_router)
app.include_router(image_generation_router)
app.include_router(video_generation_router)
app.include_router(status_router)

@app.get("/health")
async def health():
    return {"status": "ok"}
