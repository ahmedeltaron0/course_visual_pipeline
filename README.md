# Course Visual Pipeline

A FastAPI-based application designed to streamline the creation of visual content for courses. This pipeline automates the process of extracting content from documents, generating prompts, creating images, and producing videos using AI services.

## Features

- **Document Processing**: Extract video identifiers and content from `.docx` files.
- **AI Prompt Generation**: Generate detailed image/video prompts from text content using an Agent service.
- **Image Generation**: Create images based on generated prompts.
- **Video Generation**: Generate videos from images and prompts using the Higgs service.
- **Status Tracking**: Monitor the status of video generation tasks.

## Prerequisites

- Python 3.8+
- [Git](https://git-scm.com/)

## Installation

1.  **Clone the repository** (if applicable):
    ```bash
    git clone <repository-url>
    cd update_course_visual_pipline
    ```

2.  **Create a virtual environment**:
    ```bash
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1.  Create a `.env` file in the root directory.
2.  Add the necessary environment variables required by the services (e.g., OpenAI API keys, Database credentials, Service URLs).
    *Note: Refer to `app/config` or the codebase for specific variable names like `OPENAI_API_KEY`, etc.*

## Usage

Start the server using `uvicorn`:

```bash
uvicorn app.main:app --reload
```

The application will be available at `http://localhost:8000`.

### API Documentation

Interactive API Key documentation (Swagger UI) is available at:
`http://localhost:8000/docs`

#### Key Endpoints

-   **Files**
    -   `POST /files/extract`: Extract video content from a `.docx` file.

-   **Prompts**
    -   `POST /prompts/generate`: Generate prompts for visual content using the AI Agent.

-   **Image Generation**
    -   `POST /generation/images`: Generate images based on provided prompts.

-   **Video Generation**
    -   `POST /generation/video`: Generate a video from an image and prompt.

-   **Status**
    -   `GET /generation/status/{video_id}`: Check the generation status of a specific video.

## Project Structure

```
.
├── app/
│   ├── config/         # Configuration files
│   ├── repo/           # Database repositories
│   ├── routers/        # API route handlers
│   ├── schema/         # Pydantic models
│   ├── service/        # Business logic services
│   └── main.py         # Application entry point
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

## Troubleshooting

-   **Import Errors**: Ensure all dependencies are installed.
-   **File Not Found Errors**: Verify the existence of `app/routers/video_generation_router.py`. Note that `main.py` expects this file, but it might be named `video_generation.py` in your local setup. Rename it if necessary.
