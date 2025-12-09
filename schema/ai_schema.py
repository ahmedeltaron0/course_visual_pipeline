from pydantic import BaseModel
from typing import List

from pydantic import BaseModel, Field

class FramePrompt(BaseModel):
    style: str = Field(..., example="ultra-realistic 8K, cinematic, enhanced facial and material micro-details")
    camera_lens : str = Field(..., description="specific camera lens like 50mm")
    environment: str = Field(..., example="modern radiation lab with stainless steel surfaces, hazard signs, clean instruments")
    characters: str = Field(..., example="Arab male worker wearing full PPE (yellow reflective vest, hard helmet, protective gloves, safety shoes) standing near a radiation detector")
    scene: str = Field(..., example="worker demonstrating safe distance from the device")
    camera: str = Field(..., example="vertical 9:16, 50mm lens, shallow depth of field")
    lighting: str = Field(..., example="soft directional industrial lighting with subtle reflections")
    details: str = Field(..., example="crisp textures, realistic skin pores, accurate metal reflections")
    extra_details: str = Field(..., description="extra details for generation that makes all shots related together and to the scene.")

class Frame(BaseModel):
    frame_number: int
    frame_code: str   # e.g., "الاشعاع v1s1f1"
    frame_prompt: FramePrompt


class Shot(BaseModel):
    shot_number: int
    scene: str
    frames: List[Frame]

class StoryboardOutput(BaseModel):
    video_number: int
    shots: List[Shot]
