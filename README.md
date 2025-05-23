# MarketCanvas AI 🎨✨

MarketCanvas AI is a powerful visual workflow editor designed for creating stunning marketing visuals and creative content using a variety of AI-powered image generation and manipulation tools. It provides a node-based interface (powered by ReactFlow) to build complex image processing pipelines, integrating with multiple AI providers like OpenAI, Fal.ai, and Stability AI.

**Live Demo (Conceptual):** While this is a local project, imagine a live version at `your-marketcanvas-ai-url.com`

## Table of Contents

1.  [Overview](#overview)
2.  [Features](#features)
3.  [Tech Stack](#tech-stack)
4.  [Folder Structure](#folder-structure)
5.  [Prerequisites](#prerequisites)
6.  [Installation & Setup](#installation--setup)
7.  [Running the Application](#running-the-application)
8.  [Environment Variables](#environment-variables)
9.  [Key Backend Components](#key-backend-components)
10. [Key Frontend Components](#key-frontend-components)
11. [API Endpoints](#api-endpoints)
12. [Testing](#testing)
13. [Future Enhancements](#future-enhancements)
14. [Contributing](#contributing)
15. [License](#license)

## Overview

MarketCanvas AI empowers users to:

*   **Visually Design AI Workflows:** Drag and drop nodes representing different AI models, image inputs, processing steps, and outputs.
*   **Leverage Multiple AI Providers:** Seamlessly switch between and combine capabilities from OpenAI (DALL-E), Fal.ai (Fast SDXL, Img2Img), and Stability AI (SDXL, SD3).
*   **Generate and Manipulate Images:** Create images from text, transform existing images, apply style transfers, add text overlays, crop, resize, and more.
*   **Streamline Creative Production:** Build reusable templates and workflows for common marketing tasks like social media posts, product showcases, or logo ideation.
*   **Customize and Control:** Fine-tune parameters for each AI model and processing step through an intuitive inspector panel.

## Features

### Core Workflow Engine:
*   **Node-Based Visual Editor:** Intuitive drag-and-drop interface using ReactFlow.
*   **Workflow Execution:** Backend engine processes nodes sequentially based on connections.
*   **Dynamic Node Properties:** Configure node parameters (prompts, models, dimensions, etc.) in real-time.
*   **API Key Management:** Securely store and use API keys for different AI providers (managed in `AppState` and passed to backend).
*   **Workflow Templates:** Pre-defined workflows (e.g., "Social Media Post", "Product Showcase") for quick starts.
*   **Save/Load Workflows:** Persist and retrieve workflow designs.

### AI Image Generation & Manipulation:
*   **Text-to-Image:**
    *   OpenAI DALL-E 3 / DALL-E 2
    *   Fal.ai (e.g., Fast SDXL, Flux, Stable Diffusion v3 Medium)
    *   Stability AI (e.g., Stable Diffusion XL, Stable Diffusion 3 Core/Ultra)
*   **Image-to-Image:**
    *   Fal.ai (e.g., SDXL Img2Img)
    *   Stability AI (e.g., Stable Diffusion XL, Stable Diffusion 3 Core/Ultra)
*   **Style Transfer:** Apply artistic styles like Vintage, Neon, Watercolor, Oil Painting.
*   **Text Overlay:** Add text to images with customizable font, size, color, and position.
*   **Crop & Resize:** Multiple cropping strategies (center, smart, manual) and resizing.
*   **Output Configuration:** Specify output format (PNG, JPG, WEBP) and quality.

### User Interface & Experience:
*   **Responsive UI Panels:**
    *   **Toolbar:** Add new nodes, search nodes, access templates.
    *   **Node Inspector:** View and edit properties of selected nodes.
    *   **Style Presets Panel:** Quickly apply pre-defined or custom visual styles.
*   **Theming:** Light, Dark, and custom themes with accent color selection.
*   **Minimap:** For easy navigation of large workflows.
*   **Canvas Controls:** Zoom, fit view.
*   **Gallery Page:** Showcase generated images (currently static example).
*   **Home Page:** Landing page with project overview and features.

### Backend & Services:
*   **FastAPI Backend:** Robust API for workflow execution, asset management, and AI provider interaction.
*   **Modular AI Providers:** Abstracted base class for easy addition of new AI services.
*   **File Handling:** Manages uploads, downloads, and temporary files generated during workflows.
*   **Image Processing:** Utilizes Pillow and OpenCV for image manipulations.
*   **LangChain Integration (Experimental):** Services for prompt enhancement and creative brief generation (can be further integrated into nodes).

### Asset Management:
*   **Upload Assets:** Upload images to be used as inputs in workflows.
*   **List & Download Assets:** Browse and retrieve uploaded assets.
*   **Categorization:** Organize assets by category.

## Tech Stack

*   **Frontend:**
    *   [Reflex](https://reflex.dev/): Python framework for building web UIs (compiles to Next.js/React).
    *   [ReactFlow](https://reactflow.dev/): Library for building node-based editors.
*   **Backend:**
    *   [FastAPI](https://fastapi.tiangolo.com/): High-performance Python web framework.
    *   [Uvicorn](https://www.uvicorn.org/): ASGI server.
*   **AI Providers SDKs/APIs:**
    *   `openai`
    *   `fal-client`
    *   `stability-sdk`
    *   `groq` (for text generation, not currently used for images in workflows)
*   **Image Processing:**
    *   `Pillow`
    *   `opencv-python`
*   **Language Model Integration:**
    *   `langchain`, `langchain-openai`
*   **Database (for .env example):**
    *   `SQLAlchemy` (though not heavily used in provided code snippets for primary data, `DATABASE_URL` suggests potential use).
*   **General Python:**
    *   `httpx` (for async HTTP requests)
    *   `pydantic` (for data validation)
    *   `python-dotenv`

## Folder Structure
```
marketcanvas-ai/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── main.py # Main Reflex app entry point
├── backend/
│ ├── init.py
│ ├── api/
│ │ ├── init.py
│ │ ├── main.py # FastAPI app entry point & core routes
│ │ ├── routers/ # API route definitions
│ │ │ ├── init.py
│ │ │ ├── image_generation.py
│ │ │ ├── workflows.py
│ │ │ └── assets.py
│ │ └── models/ # Pydantic models for API requests/responses
│ │ ├── init.py
│ │ ├── nodes.py
│ │ ├── workflows.py
│ │ └── responses.py
│ ├── services/
│ │ ├── init.py
│ │ ├── ai_providers/ # Logic for interacting with different AI APIs
│ │ │ ├── init.py
│ │ │ ├── base.py
│ │ │ ├── openai_provider.py
│ │ │ ├── fal_provider.py
│ │ │ ├── stability_provider.py
│ │ │ └── groq_provider.py
│ │ ├── workflow_engine.py # Core logic for executing workflows
│ │ └── langchain_integration.py # Services for LLM-based tasks
│ └── utils/
│ ├── init.py
│ ├── file_handler.py # Utilities for file I/O
│ └── image_processor.py # Utilities for image manipulation
├── frontend/
│ ├── init.py
│ ├── components/ # Reusable Reflex UI components
│ │ ├── init.py
│ │ ├── reactflow/ # ReactFlow wrapper and custom nodes
│ │ │ ├── init.py
│ │ │ ├── reactflow_wrapper.py
│ │ │ └── custom_nodes.py
│ │ ├── ui/ # General UI elements (sidebar, toolbar, etc.)
│ │ │ ├── init.py
│ │ │ ├── sidebar.py
│ │ │ ├── toolbar.py
│ │ │ ├── node_inspector.py
│ │ │ ├── style_presets.py
│ │ │ └── theme_selector.py
│ │ └── layout/ # Main page layout structure
│ │ ├── init.py
│ │ └── main_layout.py
│ ├── pages/ # Top-level pages for the Reflex app
│ │ ├── init.py
│ │ ├── home.py
│ │ ├── editor.py
│ │ └── gallery.py
│ ├── states/ # Reflex state management
│ │ ├── init.py
│ │ ├── app_state.py
│ │ ├── workflow_state.py
│ │ └── ui_state.py
│ └── styles/ # Styling and themes
│ ├── init.py
│ ├── themes.py
│ └── animations.py
├── assets/ # Static assets (images, icons, templates)
│ ├── images/
│ ├── icons/
│ └── templates/
└── tests/ # Unit and integration tests
├── init.py
├── test_api/
│ └── test_main_endpoints.py
├── test_services/
│ └── test_workflow_engine.py
└── test_components/
```


## Prerequisites

*   Python (3.8+ recommended)
*   `pip` (Python package installer)
*   Node.js and `npm` (implicitly required by Reflex for frontend compilation, usually handled by Reflex itself)

## Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd marketcanvas_ai
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    *   Copy the example `.env` file:
        ```bash
        cp .env.example .env
        ```
    *   Edit the `.env` file and add your API keys for OpenAI, Fal.ai, Stability AI, and Groq:
        ```
        OPENAI_API_KEY=your_openai_key_here
        FAL_API_KEY=your_fal_key_here
        STABILITY_API_KEY=your_stability_key_here
        GROQ_API_KEY=your_groq_key_here
        # ... other variables
        ```

5.  **Initialize Reflex project (if it's the first time or you get errors):**
    ```bash
    reflex init
    ```

## Running the Application

The application consists of a FastAPI backend and a Reflex frontend. You need to run them separately.

1.  **Start the Backend (FastAPI):**
    Open a terminal, navigate to the project root (`marketcanvas_ai/`), and run:
    ```bash
    # Option 1: Using Uvicorn directly (recommended for backend development)
    cd backend
    uvicorn api.main:app --reload --port 8000
    # Navigate back to root if needed: cd ..

    # Option 2: Running the backend's main.py (if configured for uvicorn.run)
    # python backend/api/main.py
    ```
    The backend API will be available at `http://localhost:8000`.

2.  **Start the Frontend (Reflex):**
    Open another terminal, navigate to the project root (`marketcanvas_ai/`), and run:
    ```bash
    reflex run --frontend-port 3000
    ```
    The frontend application will be available at `http://localhost:3000`.

    *Note: The `main.py` in the root directory is configured to compile the Reflex app and defines an `async run_servers()` function for the FastAPI backend. However, standard practice is to run them as separate processes for development.*
    *The Reflex `config` in `main.py` sets `api_url="http://localhost:8000"`, so the frontend will automatically try to connect to the backend at this address.*

## Environment Variables

The following environment variables are used (defined in `.env.example`):

*   `OPENAI_API_KEY`: Your API key for OpenAI services (DALL-E).
*   `FAL_API_KEY`: Your API key for Fal.ai services.
*   `STABILITY_API_KEY`: Your API key for Stability AI services.
*   `GROQ_API_KEY`: Your API key for Groq services (for LLM tasks).
*   `DEBUG`: Set to `True` for debug mode (default: `True`).
*   `LOG_LEVEL`: Logging level (default: `INFO`).
*   `UPLOAD_DIR`: Directory for user uploads (default: `./uploads`).
*   `MAX_FILE_SIZE`: Maximum file size for uploads in bytes (default: `10485760` - 10MB).
*   `DATABASE_URL`: Connection string for the database (default: `sqlite:///./marketcanvas.db`).

## Key Backend Components

*   **`backend/api/main.py`:** Entry point for the FastAPI application. Defines global middleware, mounts static files, and includes API routers.
*   **`backend/api/routers/`:** Contains routers for different API functionalities:
    *   `image_generation.py`: Direct text-to-image and image-to-image endpoints.
    *   `workflows.py`: Endpoints for saving, loading, and executing workflows.
    *   `assets.py`: Endpoints for uploading, listing, and managing assets.
*   **`backend/services/workflow_engine.py`:** The core logic for interpreting and executing the node-based workflows. It handles node dependencies, data flow, and calls to AI providers or image processors.
*   **`backend/services/ai_providers/`:** Modules for interacting with specific AI APIs (OpenAI, Fal, Stability). Each provider implements a common `BaseAIProvider` interface.
*   **`backend/utils/file_handler.py`:** Manages file operations like saving uploaded files, downloading images from URLs, and generating public URLs for served files.
*   **`backend/utils/image_processor.py`:** Performs image manipulations like style transfer, text overlay, and cropping/resizing using Pillow.
*   **`backend/services/langchain_integration.py`:** Provides services for leveraging LangChain, such as prompt enhancement or generating creative briefs (can be expanded and integrated more deeply).

## Key Frontend Components

*   **`frontend/pages/`:** Defines the main views of the application:
    *   `home.py`: The landing page.
    *   `editor.py`: The main visual workflow editor interface.
    *   `gallery.py`: A page to display generated images.
*   **`frontend/states/`:** Manages the application's state using Reflex's state management:
    *   `app_state.py`: Global application state (API keys, loading indicators, logs).
    *   `workflow_state.py`: State specific to the workflow editor (nodes, edges, selected elements, execution results).
    *   `ui_state.py`: State for UI elements (panel visibility, theme, search queries).
*   **`frontend/components/reactflow/`:**
    *   `reactflow_wrapper.py`: Reflex component wrapping the ReactFlow library.
    *   `custom_nodes.py`: Definitions for custom node appearances in the ReactFlow canvas.
*   **`frontend/components/ui/`:** Contains various UI elements:
    *   `toolbar.py`: The sidebar for adding nodes and templates.
    *   `node_inspector.py`: The panel for editing selected node properties.
    *   `style_presets.py`: Panel for applying style presets.
    *   `theme_selector.py`: Component for changing the application theme.
*   **`frontend/components/layout/main_layout.py`:** Defines the overall page structure including navbar and footer.

## API Endpoints

The backend exposes several API endpoints under the `/api/v1/` prefix. Key endpoints include:

*   `GET /`: Root API endpoint, returns API status.
*   `GET /health`: Health check endpoint.
*   `POST /api/v1/execute-workflow`: Executes a given workflow (nodes and edges).
*   `GET /api/v1/node-types`: Returns a list of available node types and their configurations.
*   **Generation Router (`/api/v1/generate`):**
    *   `POST /text-to-image`: Directly generates an image from text using a specified provider.
    *   `POST /image-to-image`: Directly transforms an image using a specified provider.
    *   `GET /providers`: Lists available AI providers and their models/capabilities.
*   **Workflows Router (`/api/v1/workflows`):**
    *   `POST /save`: Saves a workflow definition.
    *   `GET /{workflow_id}`: Loads a specific workflow definition.
    *   `GET /`: Lists all saved workflows.
*   **Assets Router (`/api/v1/assets`):**
    *   `POST /upload`: Uploads an asset file.
    *   `GET /`: Lists available assets.
    *   `GET /download/{category}/{filename}`: Downloads a specific asset.
    *   `DELETE /{category}/{filename}`: Deletes a specific asset.

Refer to `backend/api/main.py` and the files in `backend/api/routers/` for detailed request/response models.

## Testing

Basic tests are included in the `tests/` directory. Pytest is used as the test runner.

To run tests:
1.  Ensure you have `pytest` and `httpx` (for async client testing) installed (they are in `requirements.txt`).
2.  Navigate to the project root.
3.  Run:
    ```bash
    pytest
    ```
    *Note: Some tests might require dummy files or specific setup (e.g., the `test_simple_workflow_execution` expects a `sample_input.png`). Ensure these are handled or mocked appropriately for reliable CI/CD.*

## Future Enhancements

*   **User Authentication & Accounts:** Allow users to save their workflows and assets securely.
*   **Database Integration:** More robust storage for workflows, user data, and generated assets.
*   **Advanced LangChain/LangGraph Nodes:** Integrate more sophisticated LLM chains or agentic workflows directly as nodes.
*   **More AI Providers:** Add support for other image/video/audio AI services.
*   **Real-time Collaboration:** Allow multiple users to work on the same workflow.
*   **Version History for Workflows:** Track changes and allow rollbacks.
*   **Batch Processing:** Run workflows on multiple inputs.
*   **Improved Error Handling & Logging:** More detailed feedback to the user and comprehensive server logs.
*   **Cloud Deployment:** Instructions and configurations for deploying to services like AWS, Google Cloud, or Heroku.
*   **Video/Audio Nodes:** Extend beyond image generation.

## Contributing

Contributions are welcome! Please follow these steps:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature-name`).
3.  Make your changes.
4.  Write tests for your changes.
5.  Ensure all tests pass (`pytest`).
6.  Commit your changes (`git commit -m 'Add some feature'`).
7.  Push to the branch (`git push origin feature/your-feature-name`).
8.  Open a Pull Request.

Please ensure your code adheres to existing styling and linting practices (e.g., using Black and Flake8).

## License

This project is licensed under the MIT License - see the `LICENSE` file for details (assuming MIT, please add a LICENSE file if one doesn't exist).
