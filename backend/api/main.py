from fastapi import FastAPI, HTTPException, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from typing import List, Dict, Any, Optional
import uuid
import json
from datetime import datetime

from .routers import image_generation, workflows, assets
from ..services.workflow_engine import WorkflowEngine
from ..models.workflows import WorkflowRequest, WorkflowResponse
from ..models.nodes import NodeType, NodeData

app = FastAPI(
    title="MarketCanvas AI API",
    description="Backend API for MarketCanvas AI visual workflow editor",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(image_generation.router, prefix="/api/v1/generate", tags=["generation"])
app.include_router(workflows.router, prefix="/api/v1/workflows", tags=["workflows"])
app.include_router(assets.router, prefix="/api/v1/assets", tags=["assets"])

workflow_engine = WorkflowEngine()

@app.get("/")
async def root():
    return {
        "message": "MarketCanvas AI API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/api/v1/execute-workflow")
async def execute_workflow(request: WorkflowRequest) -> WorkflowResponse:
    try:
        result = await workflow_engine.execute_workflow(
            nodes=request.nodes,
            edges=request.edges,
            api_keys=request.api_keys
        )

        return WorkflowResponse(
            success=True,
            result=result,
            execution_id=str(uuid.uuid4()),
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/node-types")
async def get_node_types():
    return {
        "image_input": {
            "name": "Image Input",
            "category": "input",
            "inputs": [],
            "outputs": ["image"],
            "properties": {
                "source_type": {"type": "select", "options": ["upload", "url"]},
                "url": {"type": "text", "condition": "source_type=url"},
                "file": {"type": "file", "condition": "source_type=upload"}
            }
        },
        "text_to_image": {
            "name": "Text to Image",
            "category": "generation",
            "inputs": ["prompt"],
            "outputs": ["image"],
            "properties": {
                "provider": {"type": "select", "options": ["openai", "fal", "stability"]},
                "model": {"type": "select", "dynamic": True},
                "prompt": {"type": "textarea"},
                "width": {"type": "number", "default": 1024},
                "height": {"type": "number", "default": 1024},
                "steps": {"type": "number", "default": 30},
                "guidance_scale": {"type": "number", "default": 7.5}
            }
        },
        "image_to_image": {
            "name": "Image to Image",
            "category": "generation",
            "inputs": ["image", "prompt"],
            "outputs": ["image"],
            "properties": {
                "provider": {"type": "select", "options": ["openai", "fal", "stability"]},
                "prompt": {"type": "textarea"},
                "strength": {"type": "slider", "min": 0, "max": 1, "default": 0.8}
            }
        },
        "style_transfer": {
            "name": "Style Transfer",
            "category": "transformation",
            "inputs": ["image"],
            "outputs": ["image"],
            "properties": {
                "style": {"type": "select", "options": ["vintage", "neon", "watercolor", "oil_painting"]},
                "intensity": {"type": "slider", "min": 0, "max": 1, "default": 0.7}
            }
        },
        "text_overlay": {
            "name": "Text Overlay",
            "category": "manipulation",
            "inputs": ["image"],
            "outputs": ["image"],
            "properties": {
                "text": {"type": "text"},
                "position": {"type": "select", "options": ["top", "center", "bottom"]},
                "font_size": {"type": "number", "default": 32},
                "font_color": {"type": "color", "default": "#ffffff"},
                "background_color": {"type": "color", "default": "transparent"}
            }
        },
        "crop_resize": {
            "name": "Crop & Resize",
            "category": "manipulation",
            "inputs": ["image"],
            "outputs": ["image"],
            "properties": {
                "width": {"type": "number"},
                "height": {"type": "number"},
                "crop_type": {"type": "select", "options": ["center", "smart", "manual"]}
            }
        },
        "output": {
            "name": "Output",
            "category": "output",
            "inputs": ["image"],
            "outputs": [],
            "properties": {
                "format": {"type": "select", "options": ["png", "jpg", "webp"]},
                "quality": {"type": "slider", "min": 1, "max": 100, "default": 90}
            }
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
