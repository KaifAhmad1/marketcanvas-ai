from .base import BaseAIProvider, GenerationRequest, GenerationResponse
from typing import List, Dict, Any, Optional
import httpx
import io
import base64

class StabilityProvider(BaseAIProvider):
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.base_url = "https://api.stability.ai/v1/generation"
        self.sd3_url = "https://api.stability.ai/v2beta/stable-image/generate/ultra"
        self.sd3_core_url = "https://api.stability.ai/v2beta/stable-image/generate/core"

    async def _request_sdxl(self, engine_id: str, payload: Dict[str, Any]) -> GenerationResponse:
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Accept": "application/json",
                "Content-Type": "application/json"
            }

            api_url = f"{self.base_url}/{engine_id}/text-to-image"

            response = await self.client.post(api_url, headers=headers, json=payload)

            if response.status_code == 200:
                data = response.json()
                if data.get("artifacts") and len(data["artifacts"]) > 0:
                    artifact = data["artifacts"][0]
                    if artifact.get("base64"):
                        image_url_data_uri = f"data:image/png;base64,{artifact['base64']}"
                        return GenerationResponse(
                            success=True,
                            image_url=image_url_data_uri,
                            metadata={"provider": "stability", "model": engine_id, "seed": artifact.get("seed")}
                        )
                    else:
                        return GenerationResponse(success=False, error="No base64 image data in artifact.")
                else:
                    return GenerationResponse(success=False, error="No artifacts returned from Stability API.")
            else:
                try:
                    error_data = response.json()
                    error_message = error_data.get("message", response.text)
                except:
                    error_message = response.text
                return GenerationResponse(
                    success=False,
                    error=f"Stability API error ({response.status_code}): {error_message}"
                )
        except httpx.RequestError as e:
            return GenerationResponse(success=False, error=f"Stability provider HTTP request error: {str(e)}")
        except Exception as e:
            return GenerationResponse(success=False, error=f"Stability provider error: {str(e)}")

    async def _request_sd3_core_or_ultra(self, api_url: str, payload: Dict[str, Any]) -> GenerationResponse:
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Accept": "image/*"
            }
            files = {}
            data_fields = {}

            for key, value in payload.items():
                if key == "image" and value is not None:
                    if isinstance(value, str) and value.startswith(('http://', 'https://')):
                        async with httpx.AsyncClient() as client:
                            img_response = await client.get(value)
                            img_response.raise_for_status()
                            files['image'] = ('input_image.png', img_response.content, 'image/png')
                    elif isinstance(value, bytes):
                         files['image'] = ('input_image.png', value, 'image/png')
                    else:
                        with open(value, "rb") as f:
                            files['image'] = ('input_image.png', f.read(), 'image/png')
                else:
                    data_fields[key] = str(value)

            response = await self.client.post(api_url, headers=headers, data=data_fields, files=files if files else None)

            if response.status_code == 200:
                image_data = response.content
                base64_image = base64.b64encode(image_data).decode('utf-8')
                image_url_data_uri = f"data:image/png;base64,{base64_image}"

                seed = response.headers.get("finish-reason")
                return GenerationResponse(
                    success=True,
                    image_url=image_url_data_uri,
                    metadata={"provider": "stability", "model": "sd3-ultra" if "ultra" in api_url else "sd3-core", "seed": seed}
                )
            else:
                try:
                    error_data = response.json()
                    error_message = f"{error_data.get('name')}: {error_data.get('errors')}"
                except:
                    error_message = response.text
                return GenerationResponse(
                    success=False,
                    error=f"Stability API v2 error ({response.status_code}): {error_message}"
                )
        except httpx.RequestError as e:
            return GenerationResponse(success=False, error=f"Stability provider HTTP request error (v2): {str(e)}")
        except Exception as e:
            return GenerationResponse(success=False, error=f"Stability provider error (v2): {str(e)}")

    async def text_to_image(self, request: GenerationRequest) -> GenerationResponse:
        engine_id = "stable-diffusion-xl-1024-v1-0"
        model_requested = request.metadata.get("model", engine_id) if request.metadata else engine_id

        if model_requested.lower() in ["sd3-ultra", "stable-diffusion-3-ultra"]:
            payload = {
                "prompt": request.prompt,
                "aspect_ratio": f"{request.width}:{request.height}",
                "output_format": "png"
            }
            return await self._request_sd3_core_or_ultra(self.sd3_url, payload)
        elif model_requested.lower() in ["sd3-core", "stable-diffusion-3-core", "stable-diffusion-3-medium"]:
             payload = {
                "prompt": request.prompt,
                "aspect_ratio": f"{request.width}:{request.height}",
                "output_format": "png"
            }
             return await self._request_sd3_core_or_ultra(self.sd3_core_url, payload)

        payload = {
            "text_prompts": [{"text": request.prompt, "weight": 1.0}],
            "width": request.width,
            "height": request.height,
            "steps": request.steps,
            "cfg_scale": request.guidance_scale,
            "samples": 1,
        }
        return await self._request_sdxl(engine_id, payload)

    async def image_to_image(self, request: GenerationRequest) -> GenerationResponse:
        if not request.image_url:
            return GenerationResponse(success=False, error="Image URL is required for image-to-image.")

        engine_id = "stable-diffusion-xl-1024-v1-0"
        model_requested = request.metadata.get("model", engine_id) if request.metadata else engine_id

        if model_requested.lower() in ["sd3-ultra", "stable-diffusion-3-ultra"]:
            payload = {
                "prompt": request.prompt,
                "image": request.image_url,
                "mode": "image-to-image",
                "strength": request.strength,
                "output_format": "png"
            }
            return await self._request_sd3_core_or_ultra(self.sd3_url, payload)
        elif model_requested.lower() in ["sd3-core", "stable-diffusion-3-core", "stable-diffusion-3-medium"]:
             payload = {
                "prompt": request.prompt,
                "image": request.image_url,
                "mode": "image-to-image",
                "strength": request.strength,
                "output_format": "png"
            }
             return await self._request_sd3_core_or_ultra(self.sd3_core_url, payload)

        try:
            async with httpx.AsyncClient() as client_img:
                img_response = await client_img.get(request.image_url)
                img_response.raise_for_status()
                init_image_bytes = img_response.content
        except Exception as e:
            return GenerationResponse(success=False, error=f"Failed to download init image: {str(e)}")

        api_url = f"{self.base_url}/{engine_id}/image-to-image"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json"
        }

        form_data = {
            "init_image_mode": "IMAGE_STRENGTH",
            "image_strength": str(request.strength),
            "text_prompts[0][text]": request.prompt,
            "text_prompts[0][weight]": "1.0",
            "cfg_scale": str(request.guidance_scale),
            "steps": str(request.steps),
            "samples": "1",
        }
        files = {"init_image": ("init_image.png", init_image_bytes, "image/png")}

        try:
            response = await self.client.post(api_url, headers=headers, data=form_data, files=files)
            if response.status_code == 200:
                data = response.json()
                if data.get("artifacts") and len(data["artifacts"]) > 0:
                    artifact = data["artifacts"][0]
                    if artifact.get("base64"):
                        image_url_data_uri = f"data:image/png;base64,{artifact['base64']}"
                        return GenerationResponse(
                            success=True,
                            image_url=image_url_data_uri,
                            metadata={"provider": "stability", "model": engine_id, "seed": artifact.get("seed")}
                        )
                    else:
                        return GenerationResponse(success=False, error="No base64 image data in artifact for i2i.")
                else:
                    return GenerationResponse(success=False, error="No artifacts returned from Stability API for i2i.")
            else:
                try:
                    error_data = response.json()
                    error_message = error_data.get("message", response.text)
                except:
                    error_message = response.text
                return GenerationResponse(
                    success=False,
                    error=f"Stability API error (i2i, {response.status_code}): {error_message}"
                )
        except httpx.RequestError as e:
            return GenerationResponse(success=False, error=f"Stability provider HTTP request error (i2i): {str(e)}")
        except Exception as e:
            return GenerationResponse(success=False, error=f"Stability provider error (i2i): {str(e)}")

    def get_available_models(self) -> List[str]:
        return [
            "stable-diffusion-xl-1024-v1-0",
            "stable-diffusion-v1-6",
            "stable-diffusion-xl-beta-v2-2-2",
            "stable-diffusion-3-medium",
            "stable-diffusion-3-ultra"
        ]
