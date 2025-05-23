import asyncio
import os
import uuid
from typing import Dict, Any, List, Optional, Tuple
from collections import deque
import httpx
from PIL import Image

from ..services.ai_providers.base import BaseAIProvider, GenerationRequest
from ..services.ai_providers.openai_provider import OpenAIProvider
from ..services.ai_providers.fal_provider import FalProvider
from ..services.ai_providers.stability_provider import StabilityProvider
from ..utils.file_handler import FileHandler
from ..utils.image_processor import ImageProcessor

class WorkflowEngine:
    def __init__(self):
        self.file_handler = FileHandler()
        self.image_processor = ImageProcessor(self.file_handler)
        self.node_type_configs = self._get_default_node_type_configs()

    def _get_default_node_type_configs(self) -> Dict[str, Any]:
        return {
            "image_input": {"outputs": ["image"], "properties": {"source_type":{}, "url":{}, "file":{}}},
            "text_to_image": {"inputs": ["prompt"], "outputs": ["image"], "properties": {"provider":{}, "model":{}, "prompt":{}, "width":{}, "height":{}, "steps":{}, "guidance_scale":{}}},
            "image_to_image": {"inputs": ["image", "prompt"], "outputs": ["image"], "properties": {"provider":{}, "prompt":{}, "strength":{}}},
            "style_transfer": {"inputs": ["image"], "outputs": ["image"], "properties": {"style":{}, "intensity":{}}},
            "text_overlay": {"inputs": ["image"], "outputs": ["image"], "properties": {"text":{}, "position":{}, "font_size":{}, "font_color":{}, "background_color":{}}},
            "crop_resize": {"inputs": ["image"], "outputs": ["image"], "properties": {"width":{}, "height":{}, "crop_type":{}}},
            "output": {"inputs": ["image"], "outputs": [], "properties": {"format":{}, "quality":{}}},
        }

    async def _get_ai_provider(self, provider_name: str, api_keys: Dict[str, str]) -> BaseAIProvider:
        api_key = api_keys.get(provider_name.lower())
        if not api_key:
            api_key = api_keys.get(provider_name.upper() + "_API_KEY")
            if not api_key:
                 raise ValueError(f"API key for {provider_name} not found. Ensure it's set in the UI and passed correctly.")

        provider_name_lower = provider_name.lower()
        if provider_name_lower == "openai":
            return OpenAIProvider(api_key)
        elif provider_name_lower == "fal":
            return FalProvider(api_key)
        elif provider_name_lower == "stability":
            return StabilityProvider(api_key)
        else:
            raise ValueError(f"Unknown AI provider: {provider_name}")

    async def _execute_node(
        self,
        node: Dict[str, Any],
        node_inputs: Dict[str, Any],
        api_keys: Dict[str, str],
        execution_id: str
    ) -> Dict[str, Any]:
        node_type = node["type"]
        node_data_properties = node["data"]
        outputs = {}

        current_node_params = {**node_data_properties, **node_inputs}

        if node_type == "image_input":
            source_type = current_node_params.get("source_type", "upload")
            if source_type == "url":
                image_url_param = current_node_params.get("url")
                if not image_url_param: raise ValueError("Image Input node (URL) is missing 'url' parameter.")
                image_path = await self.file_handler.save_image_from_url(image_url_param, execution_id, node["id"])
            else:
                image_path_param = current_node_params.get("file")
                if not image_path_param:
                    raise ValueError(f"Image Input node (upload) is missing 'file' parameter.")

                if not os.path.isabs(image_path_param) and not image_path_param.startswith(self.file_handler.base_upload_dir):
                    full_image_path = os.path.join(self.file_handler.base_upload_dir, image_path_param.lstrip('/\\'))
                else:
                    full_image_path = image_path_param

                if not os.path.exists(full_image_path):
                     raise ValueError(f"Image Input node (upload) file not found at resolved path: {full_image_path} (original: {image_path_param})")
                image_path = full_image_path
            outputs["image"] = image_path

        elif node_type == "text_to_image":
            provider_name = current_node_params.get("provider")
            prompt_val = current_node_params.get("prompt")
            if not provider_name or not prompt_val:
                raise ValueError("Text-to-Image node missing 'provider' or 'prompt'.")

            async with await self._get_ai_provider(provider_name, api_keys) as provider:
                req = GenerationRequest(
                    prompt=prompt_val,
                    width=int(current_node_params.get("width", 1024)),
                    height=int(current_node_params.get("height", 1024)),
                    steps=int(current_node_params.get("steps", 30)),
                    guidance_scale=float(current_node_params.get("guidance_scale", 7.5))
                )
                res = await provider.text_to_image(req)

            if not res.success or not res.image_url:
                raise RuntimeError(f"Text-to-Image generation failed for provider {provider_name}: {res.error}")

            image_path = await self.file_handler.save_image_from_url(res.image_url, execution_id, node["id"])
            outputs["image"] = image_path

        elif node_type == "image_to_image":
            provider_name = current_node_params.get("provider")
            prompt_val = current_node_params.get("prompt")
            input_image_path = current_node_params.get("image")
            if not provider_name or not prompt_val or not input_image_path:
                raise ValueError("Image-to-Image node missing 'provider', 'prompt', or input 'image'.")
            if not os.path.exists(input_image_path):
                raise ValueError(f"Image-to-Image node: input image path does not exist: {input_image_path}")

            base_api_url_for_uploads = "http://localhost:8000/uploads"
            input_image_public_url = self.file_handler.get_url_for_file(input_image_path, api_base_url=base_api_url_for_uploads)

            img_pil = Image.open(input_image_path)
            original_width, original_height = img_pil.size
            img_pil.close()

            async with await self._get_ai_provider(provider_name, api_keys) as provider:
                req = GenerationRequest(
                    prompt=prompt_val,
                    image_url=input_image_public_url,
                    strength=float(current_node_params.get("strength", 0.8)),
                    width=int(current_node_params.get("width", original_width)),
                    height=int(current_node_params.get("height", original_height)),
                    steps=int(current_node_params.get("steps", 30)),
                )
                res = await provider.image_to_image(req)

            if not res.success or not res.image_url:
                raise RuntimeError(f"Image-to-Image generation failed for provider {provider_name}: {res.error}")

            image_path = await self.file_handler.save_image_from_url(res.image_url, execution_id, node["id"])
            outputs["image"] = image_path

        elif node_type == "style_transfer":
            input_image_path = current_node_params.get("image")
            style = current_node_params.get("style")
            intensity = float(current_node_params.get("intensity", 0.7))
            if not input_image_path or not style:
                 raise ValueError("Style Transfer node missing input 'image' or 'style'.")
            if not os.path.exists(input_image_path):
                raise ValueError(f"Style Transfer node: input image path does not exist: {input_image_path}")

            processed_image_path = await self.image_processor.apply_style_transfer(
                input_image_path, style, intensity, execution_id, node["id"]
            )
            outputs["image"] = processed_image_path

        elif node_type == "text_overlay":
            input_image_path = current_node_params.get("image")
            text_content = str(current_node_params.get("text", ""))
            if not input_image_path:
                raise ValueError("Text Overlay node missing input 'image'.")
            if not os.path.exists(input_image_path):
                raise ValueError(f"Text Overlay node: input image path does not exist: {input_image_path}")

            processed_image_path = await self.image_processor.apply_text_overlay(
                input_image_path,
                text_content,
                str(current_node_params.get("position", "center")),
                int(current_node_params.get("font_size", 32)),
                str(current_node_params.get("font_color", "#ffffff")),
                str(current_node_params.get("background_color", "transparent")),
                execution_id, node["id"]
            )
            outputs["image"] = processed_image_path

        elif node_type == "crop_resize":
            input_image_path = current_node_params.get("image")
            if not input_image_path:
                raise ValueError("Crop & Resize node missing input 'image'.")
            if not os.path.exists(input_image_path):
                raise ValueError(f"Crop & Resize node: input image path does not exist: {input_image_path}")

            width_param = current_node_params.get("width")
            height_param = current_node_params.get("height")

            processed_image_path = await self.image_processor.crop_resize_image(
                input_image_path,
                int(width_param) if width_param else None,
                int(height_param) if height_param else None,
                str(current_node_params.get("crop_type", "resize_only")),
                execution_id, node["id"]
            )
            outputs["image"] = processed_image_path

        elif node_type == "output":
            input_image_path = current_node_params.get("image")
            if not input_image_path:
                raise ValueError("Output node missing input 'image'.")
            if not os.path.exists(input_image_path):
                raise ValueError(f"Output node: input image path does not exist: {input_image_path}")

            final_image_path = await self.image_processor.convert_image_format(
                input_image_path,
                str(current_node_params.get("format", "png")),
                int(current_node_params.get("quality", 90)),
                execution_id, node["id"]
            )
            outputs["final_image_path"] = final_image_path
            base_api_url_for_uploads = "http://localhost:8000/uploads"
            outputs["final_image_url"] = self.file_handler.get_url_for_file(final_image_path, api_base_url=base_api_url_for_uploads)

        else:
            outputs = {**node_inputs}

        return outputs

    async def execute_workflow(
        self,
        nodes: List[Dict[str, Any]],
        edges: List[Dict[str, Any]],
        api_keys: Dict[str, str]
    ) -> Dict[str, Any]:
        execution_id = str(uuid.uuid4())

        adj: Dict[str, List[Tuple[str, Optional[str], Optional[str]]]] = {node["id"]: [] for node in nodes}
        in_degree: Dict[str, int] = {node["id"]: 0 for node in nodes}
        node_map: Dict[str, Dict[str, Any]] = {node["id"]: node for node in nodes}

        for edge in edges:
            source_id, target_id = edge["source"], edge["target"]
            source_handle = edge.get("sourceHandle")
            target_handle = edge.get("targetHandle")

            if source_id in node_map and target_id in node_map:
                adj[source_id].append((target_id, source_handle, target_handle))
                in_degree[target_id] += 1
            else:
                print(f"Warning: Edge references non-existent node. Source: {source_id}, Target: {target_id}")

        queue = deque([node_id for node_id, degree in in_degree.items() if degree == 0])

        node_execution_outputs: Dict[str, Dict[str, Any]] = {}
        executed_count = 0

        while queue:
            current_node_id = queue.popleft()
            current_node_obj = node_map[current_node_id]
            executed_count += 1

            inputs_for_current_node: Dict[str, Any] = {}

            for N_id, N_degree in in_degree.items():
                for neighbor_id, s_handle, t_handle in adj[N_id]:
                    if neighbor_id == current_node_id:
                        source_node_id = N_id

                        if not t_handle:
                            node_config = self.node_type_configs.get(current_node_obj["type"], {})
                            expected_inputs = node_config.get("inputs", [])
                            if len(expected_inputs) == 1:
                                t_handle = expected_inputs[0]
                            else:
                                print(f"Warning: Edge from {source_node_id} to {current_node_id} missing targetHandle, and target node expects multiple or zero named inputs. Skipping this input.")
                                continue

                        if source_node_id in node_execution_outputs:
                            source_all_outputs = node_execution_outputs[source_node_id]

                            if s_handle and s_handle in source_all_outputs:
                                inputs_for_current_node[t_handle] = source_all_outputs[s_handle]
                            elif not s_handle and len(source_all_outputs) == 1:
                                inputs_for_current_node[t_handle] = list(source_all_outputs.values())[0]
                            elif not s_handle and t_handle in source_all_outputs:
                                inputs_for_current_node[t_handle] = source_all_outputs[t_handle]
                            else:
                                print(f"Warning: Could not map output from {source_node_id} (handle: {s_handle}) to input {t_handle} of {current_node_id}. Available source outputs: {list(source_all_outputs.keys())}")
                        else:
                            print(f"Error: Source node {source_node_id} has no outputs recorded when trying to feed {current_node_id}.")

            try:
                current_node_generated_outputs = await self._execute_node(
                    current_node_obj,
                    inputs_for_current_node,
                    api_keys,
                    execution_id
                )
                node_execution_outputs[current_node_id] = current_node_generated_outputs
            except Exception as e:
                print(f"Error executing node {current_node_id} ({current_node_obj['type']}): {e}")
                raise RuntimeError(f"Workflow execution failed at node {current_node_id} ({current_node_obj['type']}): {str(e)}") from e

            for neighbor_id, _, _ in adj[current_node_id]:
                in_degree[neighbor_id] -= 1
                if in_degree[neighbor_id] == 0:
                    queue.append(neighbor_id)

        if executed_count < len(nodes):
            not_executed = [nid for nid, deg in in_degree.items() if deg > 0]
            print(f"Error: Workflow execution incomplete. Possible cycle or disconnected components. Nodes not executed (due to pending inputs): {not_executed}")
            raise RuntimeError("Cycle detected in workflow graph or disconnected components, not all nodes executed.")

        final_results: Dict[str, Any] = {}
        for node_id_loop, exec_outputs_loop in node_execution_outputs.items():
            if node_map[node_id_loop]["type"] == "output":
                if "final_image_url" in exec_outputs_loop:
                    final_results[node_id_loop] = {
                        "node_id": node_id_loop,
                        "image_url": exec_outputs_loop["final_image_url"],
                        "format": node_map[node_id_loop]["data"].get("format", "png"),
                        "source_path": exec_outputs_loop.get("final_image_path")
                    }
        return final_results
