from sqlalchemy.ext.asyncio import AsyncSession
from openai import OpenAI

from app.config.settings import settings
from app.prompts.default_prompts import DefaultPrompts
from app.repo.prompt_repo import PromptRepository
from app.schema.ai_schema import StoryboardOutput


client = OpenAI(api_key=settings.OPENAI_API_KEY)


async def generate_prompts_service(
    db: AsyncSession,
    file_id,
    video_number: int,
    num_of_shots: int,
):
    """
    Generate ultra-realistic frame prompts using OpenAI
    """

    prompt_repo = PromptRepository(db)

    # 1️⃣ Load storyboard JSON previously generated
    storyboard = await prompt_repo.get_storyboard_by_file_and_video(
        file_id=file_id,
        video_number=video_number,
    )

    if not storyboard:
        raise ValueError("Storyboard not found for this file/video")

    shots = storyboard["shots"][:num_of_shots]

    # 2️⃣ Build USER message for OpenAI
    user_message = f"""
Course name (Arabic): {storyboard.get("course_name", "")}
Video number: {video_number}

Storyboard:
"""

    for shot in shots:
        user_message += f"""
Shot {shot['shot_number']}:
Scene: {shot['scene']}
"""
        for frame in shot["frames"]:
            user_message += f"Frame {frame['frame_number']} ({frame['frame_code']})\n"

    # 3️⃣ Call OpenAI (structured output)
    response = client.chat.completions.parse(
        model=settings.OPENAI_MODEL,
        messages=[
            {
                "role": "system",
                "content": DefaultPrompts.SHOT_DESCIPTION_SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": user_message,
            },
        ],
        response_format=StoryboardOutput,
        temperature=0.4,
    )

    structured_output: StoryboardOutput = response.choices[0].message.parsed

    # 4️⃣ Save prompts in DB
    await prompt_repo.create({
        "file_id": file_id,
        "video_number": video_number,
        "prompt": structured_output.model_dump(),
    })

    await db.commit()

    # 5️⃣ Return response
    return {
        "result": "success",
        "file_id": file_id,
        "video_number": video_number,
        "shots": structured_output.shots,
    }
