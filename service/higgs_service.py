import json
from typing import List, Optional, Union
from fastapi import UploadFile
import httpx
from openai import OpenAI
import requests
from core.config import Settings
from pydantic import BaseModel
from prompts.default_prompts import DefaultPrompts
from repositories.agent_repo import AgentRepository
from repositories.doc_files_repo import DocFilesRepository
from repositories.higgs_repo import HiggsRepository
from sqlalchemy.ext.asyncio import AsyncSession

from schema.ai_schema import AgentResponse, StoryboardOutput

settings = Settings()

class HiggsService:
    def __init__(self,
                 db: AsyncSession,
                 higgs_repo: HiggsRepository,
                 agent_repo: AgentRepository,
                 ):
        self.db = db
        self.higgs_repo = higgs_repo
        self.agent_repo = agent_repo
        self.higgs_base_url = "https://platform.higgsfield.ai"

    async def send_higgs_request(self, 
                                prompt: Union[dict, str],
                                num_images: int = 1,
                                resolution: str = "2k",
                                aspect_ratio: str = "16:9",
                                output_format: str = "png",
                                end_point: str = "/text-to-image"):

        headers = {
            "Content-Type": "application/json",
            "hf-api-key": settings.HF_API_KEY,
            "hf-secret": settings.HF_API_SECRET
        }

        data = {
            "num_images": num_images,
            "resolution": resolution,
            "aspect_ratio": aspect_ratio,
            "output_format": output_format,
            "prompt": str(prompt)
        }
        response = requests.post(self.higgs_base_url+"/nano-banana-pro", headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            result = response.json()
            print("Success:", result)
        else:
            print("Error:", response.status_code, response.text)
        return response.json()

    async def generate_images_for_file(self, file_id: str, video_number: Optional[int] = None, num_of_shots: Optional[int] = None):
        # Get prompts from DB (still dict inside prompt field)
        prompts: List[AgentResponse] = await self.agent_repo.get_prompts_by_file_id(
            file_id=file_id,
            video_number=video_number
        )
        
        higgs_prompts = []
        shots_processed_count = 0

        for prompt in prompts:
            # Convert the dict into Pydantic StoryboardOutput
            storyboard: StoryboardOutput = StoryboardOutput.model_validate(prompt.prompt)

            for shot in storyboard.shots:
                # Check if we reached the limit
                if num_of_shots is not None and shots_processed_count >= num_of_shots:
                    break
                
                shots_processed_count += 1

                for frame in shot.frames:
                    # Convert frame_prompt to dict to send to Higgs
                    higgs_prompts.append(frame.frame_prompt.model_dump())

                    higgs_req = await self.send_higgs_request(prompt= frame.frame_prompt.model_dump())

                    await self.higgs_repo.create({"prompt": str(frame.frame_prompt.model_dump()),
                                                    "file_name": prompt.filename,
                                                    "video_number": storyboard.video_number,
                                                    "shot_number": shot.shot_number,
                                                    "frame_number": frame.frame_number,
                                                    "status_url": higgs_req['status_url'],
                                                    "cancel_url": higgs_req['cancel_url'],
                                                    "status": higgs_req['status'],
                                                    "request_body": None,
                                                    "response_body": higgs_req
                                                    })
                    await self.db.commit()
            
            # Break outer loop if limit reached
            if num_of_shots is not None and shots_processed_count >= num_of_shots:
                break
        
        print(higgs_prompts)
        return higgs_prompts



    async def generate_kling_video(
        self,
        image_url: str,
        last_image_url: Optional[str] = None,
        prompt: Optional[str] = ""
    ):
        url = f"{self.higgs_base_url}/kling-video/v2.5-turbo/pro/image-to-video"

        if prompt is None:
            prompt = ""

        payload = {
            "prompt": prompt,
            "duration": 5,
            "cfg_scale": 0.5,
            "image_url": image_url,
            "last_image_url": last_image_url or "",
            "negative_prompt": ""
        }

        headers = {
            "Content-Type": "application/json",
            "hf-api-key": settings.HF_API_KEY,
            "hf-secret": settings.HF_API_SECRET
        }

        async with httpx.AsyncClient(timeout=60) as client:
            try:
                response = await client.post(url, json=payload, headers=headers)
                response.raise_for_status()
                data = response.json()
                print("Higgsfield response:", data)
                return data
            except httpx.HTTPStatusError as e:
                print("Request payload:", payload)
                print("Response text:", e.response.text)
                raise