import reflex as rx
from typing import Dict, Any, List, Optional, Tuple
import json
import uuid
import httpx
from datetime import datetime

class WorkflowState(rx.State):
    nodes: List[Dict[str, Any]] = []
    edges: List[Dict[str, Any]] = []
    selected_node_id: Optional[str] = None
    selected_edge_id: Optional[str] = None
    node_types: Dict[str, Dict[str, Any]] = {}
    execution_results: Dict[str, Any] = {}
    is_executing: bool = False
    workflow_templates: Dict[str, Dict[str, Any]] = {}
    custom_styles: List[Dict[str, Any]] = []

    def __init__(self):
        super().__init__()
        self.load_node_types()
        self.load_workflow_templates()

    @rx.event
    async def load_node_types(self):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get("http://localhost:8000/api/v1/node-types")
                if response.status_code == 200:
                    self.node_types = response.json()
        except Exception as e:
            print(f"Failed to load node types: {e}")

    @rx.event
    def load_workflow_templates(self):
        self.workflow_templates = {
            "social_media": {
                "name": "Social Media Post",
                "description": "Create engaging social media content",
                "nodes": [
                    {
                        "id": "text_input_1",
                        "type": "text_input",
                        "position": {"x": 100, "y": 100},
                        "data": {"label": "Text Input", "value": ""}
                    },
                    {
                        "id": "text_to_image_1",
                        "type": "text_to_image",
                        "position": {"x": 300, "y": 100},
                        "data": {"label": "Generate Image", "prompt": ""}
                    },
                    {
                        "id": "text_overlay_1",
                        "type": "text_overlay",
                        "position": {"x": 500, "y": 100},
                        "data": {"label": "Add Text", "text": ""}
                    },
                    {
                        "id": "output_1",
                        "type": "output",
                        "position": {"x": 700, "y": 100},
                        "data": {"label": "Output"}
                    }
                ],
                "edges": [
                    {"id": "e1", "source": "text_input_1", "target": "text_to_image_1"},
                    {"id": "e2", "source": "text_to_image_1", "target": "text_overlay_1"},
                    {"id": "e3", "source": "text_overlay_1", "target": "output_1"}
                ]
            },
            "product_showcase": {
                "name": "Product Showcase",
                "description": "Create product marketing visuals",
                "nodes": [
                    {
                        "id": "image_input_1",
                        "type": "image_input",
                        "position": {"x": 100, "y": 100},
                        "data": {"label": "Product Image"}
                    },
                    {
                        "id": "background_remove_1",
                        "type": "background_remove",
                        "position": {"x": 300, "y": 100},
                        "data": {"label": "Remove Background"}
                    },
                    {
                        "id": "style_transfer_1",
                        "type": "style_transfer",
                        "position": {"x": 500, "y": 100},
                        "data": {"label": "Apply Style", "style": "minimalist"}
                    },
                    {
                        "id": "output_1",
                        "type": "output",
                        "position": {"x": 700, "y": 100},
                        "data": {"label": "Output"}
                    }
                ],
                "edges": [
                    {"id": "e1", "source": "image_input_1", "target": "background_remove_1"},
                    {"id": "e2", "source": "background_remove_1", "target": "style_transfer_1"},
                    {"id": "e3", "source": "style_transfer_1", "target": "output_1"}
                ]
            }
        }

    @rx.computed
    def selected_node(self) -> Optional[Dict[str, Any]]:
        if not self.selected_node_id:
            return None
        return next((node for node in self.nodes if node["id"] == self.selected_node_id), None)

    @rx.computed
    def selected_node_properties(self) -> List[Dict[str, Any]]:
        if not self.selected_node:
            return []

        node_type = self.selected_node["type"]
        if node_type not in self.node_types:
            return []

        properties = []
        node_config = self.node_types[node_type]

        for prop_name, prop_config in node_config.get("properties", {}).items():
            current_value = self.selected_node["data"].get(prop_name)
            properties.append({
                "name": prop_name,
                "config": prop_config,
                "value": current_value
            })

        return properties

    @rx.event
    def add_node(self, node_type: str):
        if node_type not in self.node_types:
            return
        node_config = self.node_types[node_type]
        node_id = f"{node_type}_{str(uuid.uuid4())[:8]}"

        x = (len(self.nodes) % 4) * 250 + 100
        y = (len(self.nodes) // 4) * 150 + 100

        new_node = {
            "id": node_id,
            "type": node_type,
            "position": {"x": x, "y": y},
            "data": {
                "label": node_config["name"],
                **{prop: config.get("default", "") for prop, config in node_config.get("properties", {}).items()}
            }
        }

        self.nodes.append(new_node)

    @rx.event
    def delete_node(self, node_id: str):
        self.nodes = [node for node in self.nodes if node["id"] != node_id]
        self.edges = [edge for edge in self.edges if edge["source"] != node_id and edge["target"] != node_id]

        if self.selected_node_id == node_id:
            self.selected_node_id = None

    @rx.event
    def update_node_position(self, node_id: str, x: float, y: float):
        for node in self.nodes:
            if node["id"] == node_id:
                node["position"] = {"x": x, "y": y}
                break

    @rx.event
    def update_node_property(self, prop_name: str, value: Any):
        if not self.selected_node_id:
            return

        for node in self.nodes:
            if node["id"] == self.selected_node_id:
                node["data"][prop_name] = value
                break

    @rx.event
    def select_node(self, node_id: str):
        self.selected_node_id = node_id
        self.selected_edge_id = None

    @rx.event
    def select_edge(self, edge_id: str):
        self.selected_edge_id = edge_id
        self.selected_node_id = None

    @rx.event
    def clear_selection(self):
        self.selected_node_id = None
        self.selected_edge_id = None

    @rx.event
    def add_edge(self, source: str, target: str):
        edge_id = f"e_{source}_{target}"

        existing_edge = next((edge for edge in self.edges if edge["source"] == source and edge["target"] == target), None)
        if existing_edge:
            return

        new_edge = {
            "id": edge_id,
            "source": source,
            "target": target,
            "animated": False
        }

        self.edges.append(new_edge)

    @rx.event
    def delete_edge(self, edge_id: str):
        self.edges = [edge for edge in self.edges if edge["id"] != edge_id]

        if self.selected_edge_id == edge_id:
            self.selected_edge_id = None

    @rx.event
    async def execute_workflow(self):
        if not self.nodes:
            return

        try:
            self.is_executing = True

            workflow_data = {
                "nodes": self.nodes,
                "edges": self.edges,
                "api_keys": {}
            }

            async with httpx.AsyncClient(timeout=300.0) as client:
                response = await client.post(
                    "http://localhost:8000/api/v1/execute-workflow",
                    json=workflow_data
                )

                if response.status_code == 200:
                    result = response.json()
                    self.execution_results = result["result"]
                else:
                    print(f"Execution failed: {response.text}")

        except Exception as e:
            print(f"Workflow execution error: {e}")
        finally:
            self.is_executing = False

    @rx.event
    async def execute_selected_node(self):
        if not self.selected_node_id:
            return

    @rx.event
    def duplicate_selected_node(self):
        if not self.selected_node:
            return

        new_node = self.selected_node.copy()
        new_node["id"] = f"{new_node['type']}_{str(uuid.uuid4())[:8]}"
        new_node["position"] = {
            "x": new_node["position"]["x"] + 50,
            "y": new_node["position"]["y"] + 50
        }

        self.nodes.append(new_node)

    @rx.event
    def delete_selected_node(self):
        if self.selected_node_id:
            self.delete_node(self.selected_node_id)

    @rx.event
    def load_template(self, template_id: str):
        if template_id not in self.workflow_templates:
            return

        template = self.workflow_templates[template_id]
        self.nodes = template["nodes"].copy()
        self.edges = template["edges"].copy()
        self.clear_selection()

    @rx.event
    def save_as_template(self, name: str, description: str):
        template_id = name.lower().replace(" ", "_")
        self.workflow_templates[template_id] = {
            "name": name,
            "description": description,
            "nodes": self.nodes.copy(),
            "edges": self.edges.copy()
        }

    @rx.event
    def apply_style_preset(self, preset_id: str):
        if not self.selected_node_id:
            return

    @rx.event
    def clear_workflow(self):
        self.nodes = []
        self.edges = []
        self.clear_selection()
        self.execution_results = {}

    @rx.event
    def handle_nodes_change(self, changes: List[Dict[str, Any]]):
        for change in changes:
            if change["type"] == "position" and "position" in change and "id" in change:
                node_id = change["id"]
                pos = change["position"]
                for i, node in enumerate(self.nodes):
                    if node["id"] == node_id:
                        updated_node = self.nodes[i].copy()
                        updated_node["position"] = pos
                        if "dragging" in change:
                            updated_node["dragging"] = change["dragging"]
                        self.nodes[i] = updated_node
                        break
            elif change["type"] == "select" and "id" in change:
                node_id = change["id"]
                selected = change["selected"]
                for i, node in enumerate(self.nodes):
                    if node["id"] == node_id:
                        updated_node = self.nodes[i].copy()
                        updated_node["selected"] = selected
                        self.nodes[i] = updated_node
                        if selected:
                            self.selected_node_id = node_id
                        elif self.selected_node_id == node_id and not selected:
                            self.selected_node_id = None
                        break
            elif change["type"] == "remove" and "id" in change:
                self.delete_node(change["id"])
        self.nodes = list(self.nodes)

    @rx.event
    def handle_edges_change(self, changes: List[Dict[str, Any]]):
        for change in changes:
            if change["type"] == "select" and "id" in change:
                edge_id = change["id"]
                selected = change["selected"]
                for i, edge in enumerate(self.edges):
                    if edge["id"] == edge_id:
                        updated_edge = self.edges[i].copy()
                        updated_edge["selected"] = selected
                        self.edges[i] = updated_edge
                        if selected:
                            self.selected_edge_id = edge_id
                        elif self.selected_edge_id == edge_id and not selected:
                            self.selected_edge_id = None
                        break
            elif change["type"] == "remove" and "id" in change:
                self.delete_edge(change["id"])
        self.edges = list(self.edges)

    @rx.event
    def open_custom_style_dialog(self):
        print("Dialog for custom styles would open here.")
