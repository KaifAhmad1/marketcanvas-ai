from .base import BaseAIProvider, GenerationRequest, GenerationResponse
from typing import List

class FalProvider(BaseAIProvider):
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.base_url = "https://fal.run/fal-ai"

    async def text_to_image(self, request: GenerationRequest) -> GenerationResponse:
        try:
            headers = {
                "Authorization": f"Key {self.api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "prompt": request.prompt,
                "image_size": f"{request.width}x{request.height}",
                "num_inference_steps": request.steps,
                "guidance_scale": request.guidance_scale,
                "num_images": 1
            }

            response = await self.client.post(
                f"{self.base_url}/fast-sdxl",
                headers=headers,
                json=payload
            )

            if response.status_code == 200:
                data = response.json()
                return GenerationResponse(
                    success=True,
                    image_url=data["images"][0]["url"],
                    metadata={"provider": "fal", "model": "fast-sdxl"}
                )
            else:
                return GenerationResponse(
                    success=False,
                    error=f"Fal.ai API error: {response.text}"
                )

        except Exception as e:
            return GenerationResponse(
                success=False,
                error=f"Fal.ai provider error: {str(e)}"
            )

    async def image_to_image(self, request: GenerationRequest) -> GenerationResponse:
        try:
            headers = {
                "Authorization": f"Key {self.api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "prompt": request.prompt,
                "image_url": request.image_url,
                "strength": request.strength,
                "num_inference_steps": request.steps,
                "guidance_scale": request.guidance_scale
            }

            response = await self.client.post(
                f"{self.base_url}/sdxl-img2img",
                headers=headers,
                json=payload
            )

            if response.status_code == 200:
                data = response.json()
                return GenerationResponse(
                    success=True,
                    image_url=data["images"][0]["url"],
                    metadata={"provider": "fal", "model": "sdxl-img2img"}
                )
            else:
                return GenerationResponse(
                    success=False,
                    error=f"Fal.ai API error: {response.text}"
                )

        except Exception as e:
            return GenerationResponse(
                success=False,
                error=f"Fal.ai provider error: {str(e)}"
            )

    def get_available_models(self) -> List[str]:
        return [
            "fast-sdxl",
            "sdxl-img2img",
            "flux-dev",
            "flux-schnell",
            "stable-diffusion-v3-medium"
        ]
