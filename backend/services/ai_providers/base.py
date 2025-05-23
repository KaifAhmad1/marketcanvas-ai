from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
import httpx

class GenerationRequest(BaseModel):
    prompt: str
    width: Optional[int] = 1024
    height: Optional[int] = 1024
    steps: Optional[int] = 30
    guidance_scale: Optional[float] = 7.5
    image_url: Optional[str] = None
    strength: Optional[float] = 0.8

class GenerationResponse(BaseModel):
    success: bool
    image_url: Optional[str] = None
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class BaseAIProvider(ABC):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = httpx.AsyncClient(timeout=300.0)

    @abstractmethod
    async def text_to_image(self, request: GenerationRequest) -> GenerationResponse:
        pass

    @abstractmethod
    async def image_to_image(self, request: GenerationRequest) -> GenerationResponse:
        pass

    @abstractmethod
    def get_available_models(self) -> List[str]:
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
