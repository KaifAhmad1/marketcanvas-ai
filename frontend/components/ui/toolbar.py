import reflex as rx
from typing import List, Dict, Any
from ...states.workflow_state import WorkflowState
from ...states.ui_state import UIState

def add_node_button(node_type: str, node_config: Dict[str, Any]):
    return rx.button(
        rx.vstack(
            rx.icon(
                node_config.get("icon", "square"),
                size=16
            ),
            rx.text(
                node_config["name"],
                size="1",
                text_align="center"
            ),
            spacing="1",
            align="center"
        ),
        size="2",
        variant="outline",
        on_click=lambda: WorkflowState.add_node(node_type),
        width="80px",
        height="60px",
        padding="8px"
    )

def toolbar_section(title: str, nodes: List[tuple]):
    return rx.vstack(
        rx.text(title, size="2", weight="bold", color="gray"),
        rx.hstack(
            *[add_node_button(node_type, config) for node_type, config in nodes],
            spacing="2",
            wrap="wrap"
        ),
        spacing="2",
        width="100%"
    )

def main_toolbar():

    input_nodes = [
        ("image_input", {"name": "Image Input", "icon": "image"}),
        ("text_input", {"name": "Text Input", "icon": "type"}),
        ("number_input", {"name": "Number", "icon": "hash"}),
    ]

    generation_nodes = [
        ("text_to_image", {"name": "Text to Image", "icon": "wand"}),
        ("image_to_image", {"name": "Image to Image", "icon": "shuffle"}),
        ("upscale", {"name": "Upscale", "icon": "zoom-in"}),
    ]

    manipulation_nodes = [
        ("crop_resize", {"name": "Crop & Resize", "icon": "crop"}),
        ("text_overlay", {"name": "Text Overlay", "icon": "text-cursor"}),
        ("filter", {"name": "Filter", "icon": "filter"}),
        ("style_transfer", {"name": "Style Transfer", "icon": "palette"}),
    ]

    output_nodes = [
        ("output", {"name": "Output", "icon": "download"}),
        ("preview", {"name": "Preview", "icon": "eye"}),
    ]

    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.heading("Toolkit", size="4", weight="bold"),
                rx.button(
                    rx.icon("panel-left-close"),
                    size="1",
                    variant="ghost",
                    on_click=UIState.toggle_toolbar,
                ),
                justify="between",
                width="100%"
            ),

            rx.divider(),

            rx.input(
                placeholder="Search nodes...",
                value=UIState.search_query,
                on_change=UIState.set_search_query,
                width="100%"
            ),

            rx.divider(),

            toolbar_section("Input", input_nodes),
            toolbar_section("Generation", generation_nodes),
            toolbar_section("Manipulation", manipulation_nodes),
            toolbar_section("Output", output_nodes),

            rx.divider(),

            rx.vstack(
                rx.text("Templates", size="2", weight="bold", color="gray"),
                rx.button(
                    "Social Media Post",
                    size="2",
                    variant="outline",
                    width="100%",
                    on_click=lambda: WorkflowState.load_template("social_media")
                ),
                rx.button(
                    "Product Showcase",
                    size="2",
                    variant="outline",
                    width="100%",
                    on_click=lambda: WorkflowState.load_template("product_showcase")
                ),
                rx.button(
                    "Logo Design",
                    size="2",
                    variant="outline",
                    width="100%",
                    on_click=lambda: WorkflowState.load_template("logo_design")
                ),
                spacing="2",
                width="100%"
            ),

            spacing="4",
            width="100%",
            padding="20px"
        ),
        width="280px",
        height="100%",
        border_right="1px solid var(--border)",
        background="var(--surface)",
        overflow_y="auto",
        display=rx.cond(UIState.show_toolbar, "block", "none")
    )
