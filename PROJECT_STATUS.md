# Project Status & Documentation

## Overview
This project is a **Course Visual Pipeline** designed to automate the conversion of text-based course scripts (in Arabic `.docx`, `.pdf`, `.txt`, `.md` format) into visual video content. The system uses a pipeline approach to extract text, generate structured AI prompts, and finally produce images and videos using external AI services.

## Architecture
- **Framework**: FastAPI (Python)
- **Database**: Supabase (PostgreSQL)
- **AI Integration**: OpenAI (Prompt Engineering), Higgs/Kling (Media Generation)

---

## ✅ Working Well (Implemented & Verified)

The following modules are fully implemented and function as expected:

### 1. File Upload & Extraction (`/files/extract`)
This module handles the initial ingestion of course scripts.
- **Functionality**:
    - Accepts `.docx`, `.txt`, and `.md` files.
    - **Parsing**: Converts `.docx` content to raw text.
    - **Intelligent Segmentation**: Uses Regex to identify video sections based on Arabic ordinal indicators (e.g., "الفيديو الأول", "الفيديو الثاني").
    - **Storyboard Builder**: Currently uses a deterministic algorithm (`_build_storyboard_json`) to generate a preliminary JSON structure (Videos -> Shots -> Frames) with placeholders for scenes and prompts.
    - **Persistence**: Saves file metadata to the database.
- **Status**: **stable** and able to parse structured documents correctly.

### 2. Data Validation (`/validate/storyboard`)
Ensures data integrity between pipeline steps.
- **Functionality**:
    - Validates the complex nested JSON structure of the storyboard.
    - **Checks**:
        - Ensures root existence of `result: "success"`.
        - Verifies correct hierarchy: `Videos` list -> `Shots` (4 per video) -> `Frames` (3 per shot).
        - Validates presence of critical keys like `frame_number`, `frame_code`, and `frame_prompt`.
- **Status**: **Working**. successfully catches malformed data before it reaches the AI generation step.

### 3. Prompt Generation (`/prompts/generate`)
Refines the storyboard using Large Language Models (LLM).
- **Functionality**:
    - **Input**: Takes the raw parsed storyboard from the previous step.
    - **Processing**: Constructs a context-rich prompt for OpenAI, including the course name, video number, and specific shot details.
    - **Structured Output**: Uses OpenAI's `response_format` (with Pydantic models) to guarantee that the LLM returns valid, machine-readable JSON matching the `StoryboardOutput` schema.
    - **Storage**: Saves the refined, ultra-realistic image prompts to the database.
- **Status**: **Working**. Produce detailed visual descriptions ready for image generation.

---

## 🚧 Not Tested Yet / In Progress

The following modules have been coded but require rigorous testing or full integration verification:

### 1. Image Generation (`/generation/images`)
Intended to generate the actual visual frames.
- **Current State**:
    - The service (`image_generation_service.py`) is set up to receive requests.
    - It successfully generates a unique `video_id` and creates a `pending` job record in the `GenerationRepository`.
    - **Gap**: The current code snippet in the service primarily handles Database entry creation. The actual async call to an external image generation API (or the connection to a background worker to process this "pending" job) needs validation to ensure images are actually created and returned.

### 2. Video Generation (`/generation/video`)
Intended to animate the static images.
- **Current State**:
    - The service (`video_generation_service.py`) contains logic to call `higgs.generate_kling_video`.
    - It accepts `image_url_1`, `image_url_2` (end frame), and a `prompt`.
- **Gap**:
    - This feature has not been end-to-end tested.
    - Reliance on the `HiggsService` means valid API keys and correct upstream API behavior are critical.
    - Handling of the asynchronous response from the video provider (polling or webhook) likely needs verification.

---

## Next Steps for Development
1.  **Implement Image Generation Worker**: Connect the "pending" Image Generation jobs to the actual `HiggsService` to trigger generation.
2.  **End-to-End Testing**: Run a full cycle from `.docx` upload -> Prompt Gen -> Image Gen -> Video Gen.
3.  **Error Handling**: specifically for the external API calls in the generation phase.
