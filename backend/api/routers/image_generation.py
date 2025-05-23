from fastapi import APIRouter, HTTPException, Depends, Body
from typing import Dict, Any, Optional

from ..models.responses import GenericResponse, ErrorResponse
from ...services.ai_providers.base import GenerationRequest, GenerationResponse, BaseAIProvider
from ...services.workflow_engine import WorkflowEngine
from ...utils.file_handler import FileHandler
from ..main import workflow_engine

router = APIRouter()
file_handler = FileHandler()

async def get_provider_from_request(provider_name: str, api_keys: Dict[str, str]) -> BaseAIProvider:
    try:
        return await workflow_engine._get_ai_provider(provider_name, api_keys)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

class DirectGenerationPayload(BaseModel):
    provider: str
    api_keys: Dict[str, str]
    prompt: str
    width: Optional[int] = 1024
    height: Optional[int] = 1024
    steps: Optional[int] = 30
    guidance_scale: Optional[float] = 7.5
    image_url: Optional[str] = None
    strength: Optional[float] = 0.8

@router.post("/text-to-image", response_model=GenericResponse, responses={500: {"model": ErrorResponse}})
async def generate_text_to_image(payload: DirectGenerationPayload = Body(...)):
    try:
        async with await get_provider_from_request(payload.provider, payload.api_keys) as ai_provider:
            gen_req = GenerationRequest(
                prompt=payload.prompt,
                width=payload.width,
                height=payload.height,
                steps=payload.steps,
                guidance_scale=payload.guidance_scale
            )
            gen_res: GenerationResponse = await ai_provider.text_to_image(gen_req)

        if not gen_res.success or not gen_res.image_url:
            raise HTTPException(status_code=500, detail=gen_res.error or "Image generation failed with provider.")

        adhoc_execution_id = "direct_gen"
        adhoc_node_id = payload.provider
        local_image_path = await file_handler.save_image_from_url(gen_res.image_url, adhoc_execution_id, adhoc_node_id, sub_dir_override="direct_generations")
        local_image_url = file_handler.get_url_for_file(local_image_path)

        return GenericResponse(
            message="Image generated successfully.",
            data={
                "image_url": local_image_url,
                "provider_image_url": gen_res.image_url,
                "metadata": gen_res.metadata
            }
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error in /text-to-image: {e}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@router.post("/image-to-image", response_model=GenericResponse, responses={500: {"model": ErrorResponse}})
async def generate_image_to_image(payload: DirectGenerationPayload = Body(...)):
    if not payload.image_url:
        raise HTTPException(status_code=400, detail="Missing 'image_url' for image-to-image generation.")

    try:
        async with await get_provider_from_request(payload.provider, payload.api_keys) as ai_provider:
            gen_req = GenerationRequest(
                prompt=payload.prompt,
                image_url=payload.image_url,
                strength=payload.strength,
                width=payload.width,
                height=payload.height,
                steps=payload.steps,
                guidance_scale=payload.guidance_scale
            )
            gen_res: GenerationResponse = await ai_provider.image_to_image(gen_req)

        if not gen_res.success or not gen_res.image_url:
            raise HTTPException(status_code=500, detail=gen_res.error or "Image-to-image transformation failed.")

        adhoc_execution_id = "direct_i2i"
        adhoc_node_id = payload.provider
        local_image_path = await file_handler.save_image_from_url(gen_res.image_url, adhoc_execution_id, adhoc_node_id, sub_dir_override="direct_generations")
        local_image_url = file_handler.get_url_for_file(local_image_path)

        return GenericResponse(
            message="Image transformed successfully.",
            data={
                "image_url": local_image_url,
                "provider_image_url": gen_res.image_url,
                "metadata": gen_res.metadata
            }
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error in /image-to-image: {e}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@router.get("/providers", response_model=GenericResponse)
async def list_available_providers():
    providers_info = {
        "openai": {"models": OpenAIProvider("dummy").get_available_models(), "capabilities": ["text-to-image"]},
        "fal": {"models": FalProvider("dummy").get_available_models(), "capabilities": ["text-to-image", "image-to-image"]},
        "stability": {"models": StabilityProvider("dummy").get_available_models(), "capabilities": ["text-to-image", "image-to-image"]},
    }
    return GenericResponse(data=providers_info)
