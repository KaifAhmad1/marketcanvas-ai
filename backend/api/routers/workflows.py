from fastapi import APIRouter, HTTPException, Body, Depends
from typing import List, Dict, Any
import uuid
from datetime import datetime

from ..models.workflows import WorkflowRequest, WorkflowResponse
from ..models.responses import GenericResponse, ErrorResponse
from ..main import workflow_engine

router = APIRouter()

@router.post("/save", response_model=GenericResponse, responses={500: {"model": ErrorResponse}})
async def save_workflow(workflow_data: WorkflowRequest = Body(...)):
    workflow_id = workflow_data.name or str(uuid.uuid4())

    try:
        import json
        import os
        save_dir = "saved_workflows"
        os.makedirs(save_dir, exist_ok=True)
        filepath = os.path.join(save_dir, f"{workflow_id}.json")
        with open(filepath, "w") as f:
            json.dump(workflow_data.model_dump(), f, indent=2)

        return GenericResponse(message=f"Workflow '{workflow_id}' saved successfully.", data={"workflow_id": workflow_id})
    except Exception as e:
        print(f"Error saving workflow: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to save workflow: {str(e)}")

@router.get("/{workflow_id}", response_model=WorkflowRequest, responses={404: {"model": ErrorResponse}})
async def load_workflow(workflow_id: str):
    try:
        import json
        import os
        save_dir = "saved_workflows"
        filepath = os.path.join(save_dir, f"{workflow_id}.json")
        if not os.path.exists(filepath):
            raise HTTPException(status_code=404, detail=f"Workflow '{workflow_id}' not found.")

        with open(filepath, "r") as f:
            data = json.load(f)
        return WorkflowRequest(**data)
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error loading workflow: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to load workflow: {str(e)}")

@router.get("/", response_model=GenericResponse)
async def list_saved_workflows():
    try:
        import os
        save_dir = "saved_workflows"
        if not os.path.isdir(save_dir):
            return GenericResponse(data={"workflows": []})

        workflows = []
        for filename in os.listdir(save_dir):
            if filename.endswith(".json"):
                workflows.append({"id": filename[:-5], "name": filename[:-5]})

        return GenericResponse(data={"workflows": workflows})
    except Exception as e:
        print(f"Error listing workflows: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to list workflows: {str(e)}")
