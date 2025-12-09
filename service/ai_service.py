from typing import List
from openai import OpenAI
from core.config import Settings
from pydantic import BaseModel
from prompts.default_prompts import DefaultPrompts

settings = Settings()

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def poke_agent(message: List[dict], structured_output_format: BaseModel):
    print(message)
    response = client.chat.completions.parse(
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
    return response.choices[0].message.parsed

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
