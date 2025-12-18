from typing import List
from fastapi import UploadFile
from openai import OpenAI
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.settings import settings
from app.prompts.default_prompts import DefaultPrompts
from app.schema.ai_schema import StoryboardOutput
from app.repo.file_repo import FileRepository
from app.repo.prompt_repo import PromptRepository


class AgentService:
    """
    Handles AI prompt generation using OpenAI.
    """

    def __init__(
        self,
        db: AsyncSession,
        file_repo: FileRepository,
        prompt_repo: PromptRepository,
    ):
        self.client = OpenAI(api_key=settings.OPENAI_API)
        self.db = db
        self.file_repo = file_repo
        self.prompt_repo = prompt_repo

    async def _save_file(self, file: UploadFile):
        """
        Persist uploaded file metadata.
        """
        return await self.file_repo.create({
            "filename": file.filename
        })

    async def poke_agent(
        self,
        messages: List[dict],
        structured_output_format: type[StoryboardOutput],
        file: UploadFile,
    ):
        """
        Generate storyboard prompts using OpenAI
        and persist them in the database.
        """

        file_record = await self._save_file(file)

        responses: List[StoryboardOutput] = []

        for message in messages:
            response = self.client.chat.completions.parse(
                model=settings.OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            DefaultPrompts.SHOT_DESCIPTION_SYSTEM_PROMPT
                            + "\n\nIMPORTANT NUMBERING RULES:\n"
                            "- Shot numbers start at 1 for EACH video\n"
                            "- Frame numbers start at 1 for EACH shot\n"
                            "- Do NOT continue numbering across videos\n"
                        ),
                    },
                    {
                        "role": "user",
                        "content": str(message),
                    },
                ],
                response_format=structured_output_format,
                temperature=0.7,
            )

            parsed: StoryboardOutput = response.choices[0].message.parsed

            await self.prompt_repo.create({
                "file_id": file_record.id,
                "video_number": parsed.video_number,
                "prompt": parsed.model_dump(),
            })

            responses.append(parsed)

        await self.db.commit()

        return {
            "result": "success",
            "file_id": file_record.id,
            "data": responses,
        }
