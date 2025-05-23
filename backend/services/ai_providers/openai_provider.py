from .base import BaseAIProvider, GenerationRequest, GenerationResponse
from typing import List
import base64
import io

class OpenAIProvider(BaseAIProvider):
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.base_url = "https://api.openai.com/v1"

    async def text_to_image(self, request: GenerationRequest) -> GenerationResponse:
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": "dall-e-3",
                "prompt": request.prompt,
                "n": 1,
                "size": f"{request.width}x{request.height}",
                "quality": "hd",
                "response_format": "url"
            }

            response = await self.client.post(
                f"{self.base_url}/images/generations",
                headers=headers,
                json=payload
            )

            if response.status_code == 200:
                data = response.json()
                return GenerationResponse(
                    success=True,
                    image_url=data["data"][0]["url"],
                    metadata={"provider": "openai", "model": "dall-e-3"}
                )
            else:
                return GenerationResponse(
                    success=False,
                    error=f"OpenAI API error: {response.text}"
                )

        except Exception as e:
            return GenerationResponse(
                success=False,
                error=f"OpenAI provider error: {str(e)}"
            )

    async def image_to_image(self, request: GenerationRequest) -> GenerationResponse:
        try:
            return GenerationResponse(
                success=False,
                error="Image-to-image not directly supported by DALL-E"
            )

        except Exception as e:
            return GenerationResponse(
                success=False,
                error=f"OpenAI provider error: {str(e)}"
            )

    def get_available_models(self) -> List[str]:
        return ["dall-e-3", "dall-e-2"]
