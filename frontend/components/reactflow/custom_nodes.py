import reflex as rx
from typing import Dict, Any, List, Optional, Callable
from reflex.vars import Var

class CustomNodeWrapper(rx.Component):
    library = "reactflow"

    id: Var[str]
    data: Var[Dict[str, Any]]
    selected: Var[bool]
    type: Var[str]

    node_style = {
        "border": "1px solid var(--border)",
        "border_radius": "8px",
        "padding": "10px 15px",
        "background_color": "var(--surface)",
        "min_width": "200px",
        "box_shadow": "var(--shadow-sm)",
    }
    selected_style = {
        "border": "2px solid var(--primary)",
        "box_shadow": "0 0 0 3px var(--primary-transparent, #6366f133)",
    }

    def _get_custom_code(self) -> str:
        return """
        import 'reactflow/dist/style.css';
        const Handle = ReactFlow.Handle;
        """

    def _handle(self, type: str, position: str, id: Optional[str] = None, style: Optional[Dict] = None):
        handle_style = {
            "width": "10px", "height": "10px",
            "background": "var(--accent)",
            "border_radius": "3px",
        }
        if style:
            handle_style.update(style)

        return rx.el. शाळा(
            _name="Handle",
            type=type,
            position=position,
            id=id,
            style=handle_style,
            is_connectable=True
        )

class ImageInputNode(CustomNodeWrapper):
    tag = "ImageInputNode"

    def render(self):
        return rx.box(
            rx.vstack(
                rx.hstack(
                    rx.icon("image", size=16, color="var(--text-muted)"),
                    rx.text(self.data.get("label", "Image Input"), weight="medium"),
                    align="center", spacing="2"
                ),
                rx.cond(
                    self.data.get("source_type") == "url",
                    rx.text(self.data.get("url", "No URL set"), size="1", no_of_lines=1, color="var(--text-muted)"),
                    rx.text(self.data.get("file", "No file uploaded"), size="1", no_of_lines=1, color="var(--text-muted)")
                ),
                spacing="1",
                align="start"
            ),
            self._handle(type="source", position="right", id="image"),
            style=rx.cond(self.selected, {**self.node_style, **self.selected_style}, self.node_style)
        )

class TextToImageNode(CustomNodeWrapper):
    tag = "TextToImageNode"

    def render(self):
        return rx.box(
            rx.vstack(
                rx.hstack(
                    rx.icon("wand", size=16, color="var(--text-muted)"),
                    rx.text(self.data.get("label", "Text to Image"), weight="medium"),
                    align="center", spacing="2"
                ),
                rx.text(
                    self.data.get("prompt", "No prompt"),
                    size="1", no_of_lines=2, color="var(--text-muted)"
                ),
                rx.text(
                    f"Provider: {self.data.get('provider', 'N/A')}",
                    size="1", color="var(--text-muted)"
                ),
                spacing="1",
                align="start"
            ),
            self._handle(type="target", position="left", id="prompt"),
            self._handle(type="source", position="right", id="image"),
            style=rx.cond(self.selected, {**self.node_style, **self.selected_style}, self.node_style)
        )

class OutputNode(CustomNodeWrapper):
    tag = "OutputNode"

    def render(self):
        image_url = self.data.get("result_image_url")

        return rx.box(
            rx.vstack(
                rx.hstack(
                    rx.icon("download", size=16, color="var(--text-muted)"),
                    rx.text(self.data.get("label", "Output"), weight="medium"),
                    align="center", spacing="2"
                ),
                rx.cond(
                    image_url,
                    rx.image(src=image_url, width="100%", height="auto", max_height="100px", object_fit="contain", border_radius="4px", margin_top="5px"),
                    rx.text(f"Format: {self.data.get('format', 'png')}", size="1", color="var(--text-muted)")
                ),
                spacing="1",
                align="start"
            ),
            self._handle(type="target", position="left", id="image"),
            style=rx.cond(self.selected, {**self.node_style, **self.selected_style}, self.node_style)
        )

class GenericConfigurableNode(CustomNodeWrapper):
    tag = "GenericConfigurableNode"

    def render(self):
        node_type = self.type
        label = self.data.get("label", node_type.replace("_", " ").title())
        icon_name = self.data.get("icon", "box")

        return rx.box(
            rx.vstack(
                rx.hstack(
                    rx.icon(icon_name, size=16, color="var(--text-muted)"),
                    rx.text(label, weight="medium"),
                    align="center", spacing="2"
                ),
                rx.foreach(
                    Var.range(min(3, self.data.length())),
                    lambda i: rx.text(
                        f"{list(self.data.keys())[i]}: {str(list(self.data.values())[i])[:20]}",
                        size="1", color="var(--text-muted)", no_of_lines=1
                    )
                ),
                spacing="1",
                align="start"
            ),
            self._handle(type="target", position="left", id="input_default"),
            self._handle(type="source", position="right", id="output_default"),
            style=rx.cond(self.selected, {**self.node_style, **self.selected_style}, self.node_style)
        )

image_input_node = ImageInputNode.create
text_to_image_node = TextToImageNode.create
output_node = OutputNode.create
generic_configurable_node = GenericConfigurableNode.create

DEFAULT_NODE_TYPES = {
    "image_input": image_input_node,
    "text_input": generic_configurable_node,
    "number_input": generic_configurable_node,
    "text_to_image": text_to_image_node,
    "image_to_image": generic_configurable_node,
    "upscale": generic_configurable_node,
    "crop_resize": generic_configurable_node,
    "text_overlay": generic_configurable_node,
    "filter": generic_configurable_node,
    "style_transfer": generic_configurable_node,
    "output": output_node,
    "preview": generic_configurable_node,
}
