from pydantic import BaseModel
from typing import Optional, Any, List, Dict

class GenericResponse(BaseModel):
    success: bool = True
    message: Optional[str] = None
    data: Optional[Any] = None

class ErrorResponse(BaseModel):
    success: bool = False
    detail: str
    error_code: Optional[str] = None

class UploadResponse(GenericResponse):
    filename: str
    file_url: str
    content_type: Optional[str] = None
    size: Optional[int] = None

class AssetListResponse(GenericResponse):
    assets: List[Dict[str, Any]]

class NodeTypeListResponse(BaseModel):
    node_types: Dict[str, Any]
