# Course Visual Pipeline

A FastAPI-based backend pipeline designed to automate the creation of visual assets for courses. It extracts video scripts from Word documents (`.docx`), generates storyboard prompts using AI, and produces images and videos using external generative AI services (Higgs/Kling).

## Features

- **Script Extraction**: Automatically parses Arabic `.docx` course scripts to identify and extract video sections (e.g., "الفيديو الأول", "الفيديو الثاني").
- **AI Prompt Generation**: Automates the conversion of extracted scripts into detailed visual prompts/storyboards via an AI Agent.
- **Image Generation**: Integrates with Higgs Service to generate images based on prompts.
- **Video Generation**: Creates video clips from start/end images using Kling AI (via Higgs Service).
- **Asynchronous Processing**: Uses `asyncio` for non-blocking I/O operations.
- **Database Integration**: Built with SQLAlchemy (Async) and PostgreSQL for robust data management of files, prompts, and generation jobs.
- **Structured Data**: Uses Pydantic schemas for strict request/response validation.

## Project Structure

```
course_visual_pipeline/
├── app/
│   ├── config/         # Configuration (Environment variables, Container)
│   ├── db/             # Database connection & Session management
│   ├── models/         # SQLAlchemy ORM Models (Files, Prompts, Jobs)
│   ├── repo/           # Repository Pattern implementations
│   ├── routers/        # FastAPI Routes (Files, Prompts, Generation)
│   ├── schema/         # Pydantic Schemas (Input/Output validation)
│   ├── service/        # Business Logic (File parsing, AI integration)
│   └── main.py         # Application Entry Point
├── .env                # Environment Variables (Not verified in git)
├── requirements.txt    # Project Dependencies
└── README.md           # Project Documentation
```

## Prerequisites

- Python 3.9+
- PostgreSQL Database
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
    Create a `.env` file in the root directory and add the following configuration variables:
    ```ini
    DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/dbname
    OPENAI_API_KEY=your_openai_key
    HIGGS_API_KEY=your_higgs_key
    ```

## Usage

1.  **Start the Server**:
    ```bash
    uvicorn app.main:app --reload
    ```
    The API will be available at `http://localhost:8000`.

2.  **API Documentation**:
    Visit `http://localhost:8000/docs` to view the interactive Swagger UI.

### Key Endpoints

#### 1. File Extraction
- **POST** `/files/extract`
- Upload a `.docx` file to parse and save video scripts to the database.

#### 2. Prompt Generation
- **POST** `/prompts/generate`
- Generate AI storyboards/prompts for the extracted video scripts.

#### 3. Image Generation
- **POST** `/generation/images`
- Trigger image generation from a specific prompt.

#### 4. Video Generation
- **POST** `/generation/video`
- Generate a video using a start image (and optional end image).

#### 5. Status Check
- **GET** `/generation/status/{video_id}`
- Check the progress of a background generation job.

## Development

- **Database Migrations**: Ensure your PostgreSQL database is running and accessible via `DATABASE_URL` before starting the app. The app attempts to create tables on startup (dev mode).
- **Architecture**: The project follows a layered architecture: `Router -> Service -> Repository -> Database`.

## Troubleshooting

- **"ModuleNotFoundError"**: Ensure you are running the command from the root directory and your virtual environment is active.
- **Database Connection**: Verify `DATABASE_URL` in `.env` matches your local PostgreSQL credentials.
