from typing import List
from fastapi import UploadFile
from openai import OpenAI
from core.config import Settings
from pydantic import BaseModel
from prompts.default_prompts import DefaultPrompts
from repositories.agent_repo import AgentRepository
from repositories.doc_files_repo import DocFilesRepository
from repositories.higgs_repo import HiggsRepository
from sqlalchemy.ext.asyncio import AsyncSession

from schema.ai_schema import StoryboardOutput
import langgraph
settings = Settings()

class AgentService:
    def __init__(self,
                 db: AsyncSession,
                 agent_repo: AgentRepository,
                 doc_files_repo: DocFilesRepository
                 ):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.db = db
        self.agent_repo = agent_repo
        self.doc_files_repo = doc_files_repo

    async def save_file(self, file: UploadFile):
        result = await self.doc_files_repo.create({"filename": file.filename})
        return result


    async def poke_agent(self, messages: List[dict], structured_output_format: StoryboardOutput, file :UploadFile):
        file_data = await self.save_file(file)
        responses = []
        for message in messages:
            response = self.client.chat.completions.parse(
                model=settings.OPENAI_MODEL,
                messages=[
                    {
                        "role": "system", 
                        "content": DefaultPrompts.SHOT_DESCIPTION_SYSTEM_PROMPT + "\n\nIMPORTANT NUMBERING RULES:\n- Shot numbers must start at 1 for EACH video and increment independently (1, 2, 3, 4...)\n- Frame numbers must start at 1 for EACH shot and increment independently (1, 2, 3...)\n- Do NOT continue numbering from previous videos or shots\n- Each video's first shot is always shot_number: 1\n- Each shot's first frame is always frame_number: 1"
                    },
                    {"role": "user", "content": f"{message}"}
                ],
                response_format=structured_output_format,
                temperature=0.7
            )
            structured_response : StoryboardOutput = response.choices[0].message.parsed
            db_response = await self.agent_repo.create({"prompt":structured_response.model_dump(),
                                                        "filename":file.filename,
                                                        "video_number" : structured_response.video_number,
                                                        "file_id": file_data.id
                                                        })
            print(db_response)
            responses.append(response.choices[0].message.parsed)
            await self.db.commit()
        return {"result": "success",
                "data": responses,
                "file_id": file_data.id}

#

# response = poke_agent("I love the battery but hate the camera.", AnalysisOutput)
# print(response)
# # THE REAL TYPED RESULT
# result: AnalysisOutput = response.choices[0].message.parsed

# print(result)
# print(" ")
# print(result.summary)
# print(" ")
# print(result.sentiment)
# print(" ")
# print(result.score)
# print(" ")
# print(result.important_phrases)
# print(" ")
