from .base import BaseAIProvider, GenerationRequest, GenerationResponse
from typing import List, Dict, Any
import httpx

class GroqProvider(BaseAIProvider):
    def __init__(self, api_key: str):
        super().__init__(api_key)

    async def text_to_image(self, request: GenerationRequest) -> GenerationResponse:
        return GenerationResponse(
            success=False,
            error="Groq provider does not support text-to-image generation at this time."
        )

    async def image_to_image(self, request: GenerationRequest) -> GenerationResponse:
        return GenerationResponse(
            success=False,
            error="Groq provider does not support image-to-image transformation at this time."
        )

    async def generate_text(self, prompt: str, model: str = "mixtral-8x7b-32768") -> Dict[str, Any]:
        return {"text": f"Groq text generation for prompt '{prompt}' using model '{model}' would happen here."}

    def get_available_models(self) -> List[str]:
        return [
            "mixtral-8x7b-32768",
            "llama3-70b-8192",
            "llama3-8b-8192",
            "gemma-7b-it",
        ]
