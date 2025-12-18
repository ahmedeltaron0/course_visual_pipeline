import json
from typing import Optional, List
import httpx

from sqlalchemy.ext.asyncio import AsyncSession

from app.config.settings import settings
from app.schema.ai_schema import StoryboardOutput
from app.repo.prompt_repo import PromptRepository
from app.repo.higgs_repo import HiggsRepository
from app.repo.generation_repo import GenerationRepository


class HiggsService:
    """
    Handles image generation (Higgs) and video generation (Kling).
    """

    def __init__(
        self,
        db: AsyncSession,
        prompt_repo: PromptRepository,
        higgs_repo: HiggsRepository,
        generation_repo: GenerationRepository,
    ):
        self.db = db
        self.prompt_repo = prompt_repo
        self.higgs_repo = higgs_repo
        self.generation_repo = generation_repo
        self.base_url = "https://platform.higgsfield.ai"

    # -------------------------------------------------
    # Internal: Send image request to Higgs
    # -------------------------------------------------
    async def _send_higgs_request(self, frame_prompt: dict) -> dict:
        url = f"{self.base_url}/nano-banana-pro"

        headers = {
            "Content-Type": "application/json",
            "hf-api-key": settings.HF_API_KEY,
            "hf-secret": settings.HF_API_SECRET,
        }

        payload = {
            "num_images": 1,
            "resolution": "2k",
            "aspect_ratio": "16:9",
            "output_format": "png",
            "prompt": json.dumps(frame_prompt),
        }

        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()

    # -------------------------------------------------
    # Generate images for a file (main pipeline step)
    # -------------------------------------------------
    async def generate_images_for_file(
        self,
        file_id,
        video_number: Optional[int] = None,
    ) -> List[dict]:
        """
        Generate images for all frames in a file or a specific video.
        """

        prompts = await self.prompt_repo.get_by_file_id(
            file_id=file_id,
            video_number=video_number,
        )

        results: List[dict] = []

        for prompt_record in prompts:
            storyboard = StoryboardOutput.model_validate(prompt_record.prompt)

            for shot in storyboard.shots:
                for frame in shot.frames:
                    higgs_response = await self._send_higgs_request(
                        frame.frame_prompt.model_dump()
                    )

                    await self.higgs_repo.create({
                        "file_id": file_id,
                        "video_number": storyboard.video_number,
                        "shot_number": shot.shot_number,
                        "frame_number": frame.frame_number,
                        "prompt": frame.frame_prompt.model_dump(),
                        "response": higgs_response,
                        "status": higgs_response.get("status"),
                    })

                    results.append(higgs_response)

        await self.db.commit()
        return results

    # -------------------------------------------------
    # Generate video using Kling
    # -------------------------------------------------
    async def generate_kling_video(
        self,
        image_url: str,
        last_image_url: Optional[str] = None,
        prompt: Optional[str] = "",
    ) -> dict:
        """
        Generate video from image(s) using Kling API.
        """

        url = f"{self.base_url}/kling-video/v2.5-turbo/pro/image-to-video"

        payload = {
            "prompt": prompt or "",
            "duration": 5,
            "cfg_scale": 0.5,
            "image_url": image_url,
            "last_image_url": last_image_url or "",
            "negative_prompt": "",
        }

        headers = {
            "Content-Type": "application/json",
            "hf-api-key": settings.HF_API_KEY,
            "hf-secret": settings.HF_API_SECRET,
        }

        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
