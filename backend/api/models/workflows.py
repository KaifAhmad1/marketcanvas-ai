from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from .nodes import Node, Edge

class WorkflowRequest(BaseModel):
    nodes: List[Node]
    edges: List[Edge]
    api_keys: Dict[str, str] = Field(default_factory=dict, description="API keys for various providers, e.g., {'openai': 'sk-...', 'fal': 'fal-key-...'}")
    name: Optional[str] = None
    description: Optional[str] = None

class WorkflowExecutionResult(BaseModel):
    node_id: str
    image_url: str
    format: str
    source_path: Optional[str] = None

class WorkflowResponse(BaseModel):
    success: bool
    result: Optional[Dict[str, WorkflowExecutionResult]] = Field(None, description="Dictionary of results from 'output' nodes, keyed by output node ID")
    message: Optional[str] = None
    execution_id: Optional[str] = None
    timestamp: Optional[str] = None
    error_details: Optional[Any] = None
