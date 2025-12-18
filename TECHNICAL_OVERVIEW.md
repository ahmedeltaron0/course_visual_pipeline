# Technical Overview & Architecture

## 1. Project Concept
The **Course Visual Pipeline** is an automated backend system designed to transform text-based course scripts into visual video content. It acts as an intelligent bridge between raw documents and generative AI video engines.

**Core Goal:** To minimize manual effort in video production by automating the "Script -> Storyboard -> Prompt -> Video" lifecycle.

## 2. Core Entities (Data Model)
The system is built around a few specific entities that represent the lifecycle of a video creation job.

| Entity | Description | Storage |
| :--- | :--- | :--- |
| **File** | Represents the uploaded source document (e.g., `course_script.docx`). | `files` table (PostgreSQL) |
| **Video Section** | A logical segment of the course text (e.g., "Video 1"). Parsed from the file. | *Currently Transient (in-memory)* |
| **Storyboard** | A structured JSON plan of shots and frames for a specific video. | *Currently Transient (in-memory/API response)* |
| **Prompt** | The refined, AI-generated descriptive text used to generate images. | `prompts` table |
| **Generation Job** | Tracks the status of an asynchronous image/video generation task. | `generation_jobs` table |

## 3. Detailed Workflow

The pipeline operates in four distinct stages:

### Stage A: Ingestion & Segmentation
**Endpoint:** `POST /files/extract`
1.  **Parsing**: The system reads the `.docx` file and extracts raw text.
2.  **Logic**: Regex patterns identify headers like "الفيديو الأول" (First Video) to split the text into logical `Video` units.
3.  **Storyboard Construction**: A deterministic algorithm breaks each video into `Shots` (4 per video) and `Frames` (3 per shot).
4.  **Output**: Returns a JSON object representing the `Storyboard` structure.
5.  **Tested**: ✅

### Stage B: Prompt Refinement (AI Agent)
**Endpoint:** `POST /prompts/generate`
1.  **Input**: Receives `file_id` and `video_number`.
2.  **Retrieval**: *Intended* to fetch the storyboard context (Note: Currently requires data persistence adjustment to work fully).
3.  **AI Processing**: Sends the scene descriptions to OpenAI.
4.  **Transformation**: The AI converts simple scene descriptions into professional, "ultra-realistic" image generation prompts (e.g., specifying camera lens, lighting, style).
5.  **Persistence**: Saves the generated prompts to the `prompts` table.
6.  **Tested**: ✅

### Stage C: Image Generation
**Endpoint:** `POST /generation/images`
1.  **Trigger**: User requests images for a specific Prompt ID.
2.  **Job Creation**: Creates a `GenerationJob` record with status `pending`.
3.  **Execution**: *Planned* to trigger the Higgs API to generate the actual image assets.
4.  **Tested**: Not Yet

### Stage D: Video Generation
**Endpoint:** `POST /generation/video`
1.  **Input**: Start Image URL + (Optional) End Image URL + Prompt.
2.  **Execution**: Calls the Kling AI video model (via Higgs service) to animate the images.
3.  **Tested**: Not Yet

## 4. Component Architecture
The application follows a strict **Layered Architecture** to ensure separation of concerns:

-   **Routers (`app/routers`)**:
    -   Handle HTTP Request/Response.
    -   Validate input using Pydantic Schemas (`app/schema`).
    -   Delegate work to Services.

-   **Services (`app/service`)**:
    -   Contain the core Business Logic.
    -   Coordinate between Repositories and External APIs (OpenAI, Higgs).
    -   *Example*: `prompt_service.py` manages the conversation with OpenAI.

-   **Repositories (`app/repo`)**:
    -   Abstract the Database interactions.
    -   Perform CRUD operations using SQLAlchemy models.
    -   *Example*: `FileRepository` handles specific queries for `File` records.

-   **Models (`app/models`)**:
    -   Define the Database Schema mapping (ORM).

## 5. Technology Stack
-   **Runtime**: Python 3.9+
-   **Web Framework**: FastAPI (High performance, Async).
-   **Database**: PostgreSQL with `asyncpg` driver.
-   **ORM**: SQLAlchemy (Async).
-   **Validation**: Pydantic.
-   **AI Integration**: OpenAI SDK (LLM), HTTP Client (Media Gen).

## 6. Current Data Flow Note
*Observation:* There is currently a logical disconnect between **Stage A** and **Stage B**.
-   **Stage A** produces a Storyboard but returns it to the client without saving it to a database table.
-   **Stage B** attempts to load a Storyboard from the database to generate prompts.
-   **Resolution Needed**: A temporary store or a `Storyboards` table should be introduced to persist the output of Stage A so Stage B can retrieve it.
