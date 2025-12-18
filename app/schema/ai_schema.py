from pydantic import BaseModel
from typing import List


class FramePrompt(BaseModel):
    """
    Structured visual prompt for one frame.
    This is what gets sent to Higgs.
    """
    style: str
    camera_lens: str
    environment: str
    characters: str
    scene: str
    camera: str
    lighting: str
    details: str
    extra_details: str = ""


class Frame(BaseModel):
    """
    Single frame inside a shot.
    """
    frame_number: int
    frame_prompt: FramePrompt


class Shot(BaseModel):
    """
    Shot containing multiple frames.
    """
    shot_number: int
    frames: List[Frame]


class StoryboardOutput(BaseModel):
    """
    AI output for one video storyboard.
    """
    video_number: int
    shots: List[Shot]
