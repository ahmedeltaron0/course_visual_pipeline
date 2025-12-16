# Course Visual Pipeline

A FastAPI-based backend pipeline designed to automate the creation of visual assets for courses. It extracts video scripts from Word documents (`.docx`), generates storyboard prompts using AI, and produces images and videos using external generative AI services (Higgs/Kling).

## Features

- **Script Extraction**: automatically parses Arabic `.docx` course scripts to identify and extract video sections (e.g., "الفيديو الأول", "الفيديو الثاني").
- **AI Prompt Generation**: Uses an AI agent to convert extracted scripts into detailed visual prompts/storyboards.
- **Image Generation**: Integrates with Higgs Service to generate images based on prompts.
- **Video Generation**: Creates video clips from images using Kling AI (via Higgs Service).
- **Database Integration**: SQLAlchemy & Pydantic models for managing file and generation states.

## Project Structure

```
course_visual_pipeline/
├── core/               # Core configuration and dependency injection container
├── exceptions/         # Custom exception handlers
├── models/             # Database models (SQLAlchemy)
├── prompts/            # AI System prompts
├── repositories/       # Database access layer
├── schema/             # Pydantic data schemas
├── scripts/            # Utility scripts
├── service/            # Business logic (AI Service, Higgs Service)
├── server.py           # Main FastAPI application entry point
├── requirements.txt    # Python dependencies
└── .env                # Environment variables (not included in repo)
```

## Prerequisites

- Python 3.9+
- PostgreSQL
- API Keys for:
    - OpenAI (or compatible LLM provider)
    - Higgs / Kling AI Service

## Installation

1.  **Clone the repository**:
    ```bash
    git clone <repository_url>
    cd course_visual_pipeline
    ```

2.  **Create and activate a virtual environment**:
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Linux/Mac
    source venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Environment Configuration**:
    Create a `.env` file in the root directory and add configuration variables (refer to `core/config.py` for required fields, typically including DB credentials and API keys).

## Usage

1.  **Start the Server**:
    ```bash
    uvicorn server:app --reload
    ```
    The API will be available at `http://localhost:8000`.

2.  **API Documentation**:
    Visit `http://localhost:8000/docs` to view the interactive Swagger UI.

### Key Endpoints

-   `POST /generate_file_prompts`: Upload a `.docx` file to extract text and generate storyboard prompts.
-   `POST /generate_images_for_file`: Trigger image generation for a specific file or video section.
-   `POST /generate_videos_from_images`: Generate a video from a start image (and optional end image) using a prompt.

## Development

-   **Database**: Uses `asyncpg` and `sqlalchemy`. Ensure your database migration/setup is complete before running.
-   **Services**: `AgentService` handles LLM interactions, while `HiggsService` handles media generation.
