from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional, Union
from enum import Enum

class NodeTypeEnum(str, Enum):
    IMAGE_INPUT = "image_input"
    TEXT_TO_IMAGE = "text_to_image"
    IMAGE_TO_IMAGE = "image_to_image"
    STYLE_TRANSFER = "style_transfer"
    TEXT_OVERLAY = "text_overlay"
    CROP_RESIZE = "crop_resize"
    OUTPUT = "output"
    TEXT_INPUT = "text_input"
    NUMBER_INPUT = "number_input"
    UPSCALE = "upscale"
    BACKGROUND_REMOVE = "background_remove"
    FILTER = "filter"
    PREVIEW = "preview"

class NodePosition(BaseModel):
    x: float
    y: float

class NodeData(BaseModel):
    label: Optional[str] = None
    source_type: Optional[str] = Field(None, description="e.g., 'upload' or 'url'")
    url: Optional[str] = Field(None, description="URL if source_type is 'url'")
    file: Optional[str] = Field(None, description="File path if source_type is 'upload'")
    provider: Optional[str] = Field(None, description="AI provider like 'openai', 'fal', 'stability'")
    model: Optional[str] = Field(None, description="Specific model from the provider")
    prompt: Optional[str] = Field(None, description="Text prompt for generation")
    width: Optional[int] = Field(None, description="Image width")
    height: Optional[int] = Field(None, description="Image height")
    steps: Optional[int] = Field(None, description="Number of inference steps")
    guidance_scale: Optional[float] = Field(None, description="Guidance scale for generation")
    strength: Optional[float] = Field(None, description="Strength for image-to-image tasks (0.0 to 1.0)")
    style: Optional[str] = Field(None, description="e.g., 'vintage', 'neon'")
    intensity: Optional[float] = Field(None, description="Intensity of the style effect (0.0 to 1.0)")
    text: Optional[str] = Field(None, description="Text content for overlay")
    crop_type: Optional[str] = Field(None, description="e.g., 'center_crop', 'smart_crop', 'resize_only'")
    format: Optional[str] = Field(None, description="e.g., 'png', 'jpg', 'webp'")
    quality: Optional[int] = Field(None, description="Output quality (1-100)")
    value: Optional[Union[str, int, float]] = Field(None, description="Value for input nodes")

    class Config:
        extra = "allow"

class Node(BaseModel):
    id: str
    type: str
    position: NodePosition
    data: NodeData = Field(default_factory=dict)
    width: Optional[int] = None
    height: Optional[int] = None
    selected: Optional[bool] = None
    dragging: Optional[bool] = None

class Edge(BaseModel):
    id: str
    source: str
    target: str
    sourceHandle: Optional[str] = None
    targetHandle: Optional[str] = None
    animated: Optional[bool] = False
    type: Optional[str] = Field("default", description="Edge type, e.g., 'default', 'smoothstep'")
    label: Optional[str] = None
