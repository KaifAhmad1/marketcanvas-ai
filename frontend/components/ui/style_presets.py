import reflex as rx
from typing import Dict, Any, List
from ...states.workflow_state import WorkflowState

STYLE_PRESETS = {
    "vintage": {
        "name": "Vintage",
        "description": "Classic retro aesthetic with warm tones",
        "preview": "🎞️",
        "parameters": {
            "color_temperature": "warm",
            "saturation": 0.8,
            "contrast": 1.2,
            "vignette": 0.3,
            "grain": 0.2
        }
    },
    "neon_glow": {
        "name": "Neon Glow",
        "description": "Cyberpunk inspired with glowing effects",
        "preview": "🌈",
        "parameters": {
            "glow_intensity": 0.8,
            "color_palette": ["#ff00ff", "#00ffff", "#ffff00"],
            "bloom": 0.6,
            "contrast": 1.5
        }
    },
    "watercolor": {
        "name": "Watercolor",
        "description": "Soft artistic watercolor painting style",
        "preview": "🎨",
        "parameters": {
            "brush_softness": 0.9,
            "color_bleeding": 0.7,
            "paper_texture": 0.4,
            "transparency": 0.3
        }
    },
    "oil_painting": {
        "name": "Oil Painting",
        "description": "Rich textured oil painting effect",
        "preview": "🖼️",
        "parameters": {
            "brush_size": "medium",
            "texture_intensity": 0.8,
            "color_richness": 1.3,
            "impasto": 0.5
        }
    },
    "minimalist": {
        "name": "Minimalist",
        "description": "Clean, simple, modern aesthetic",
        "preview": "⚪",
        "parameters": {
            "color_palette": ["#ffffff", "#000000", "#f0f0f0"],
            "contrast": 1.1,
            "saturation": 0.3,
            "noise_reduction": 0.9
        }
    },
    "dramatic": {
        "name": "Dramatic",
        "description": "High contrast cinematic look",
        "preview": "🎭",
        "parameters": {
            "contrast": 2.0,
            "highlights": -0.3,
            "shadows": 0.5,
            "clarity": 0.8,
            "vignette": 0.4
        }
    }
}

def style_preset_card(preset_id: str, preset_config: Dict[str, Any]):
    return rx.box(
        rx.vstack(
            rx.center(
                rx.text(
                    preset_config["preview"],
                    size="6",
                    style={"font-size": "2rem"}
                ),
                width="100%",
                height="60px",
                border_radius="8px",
                background="var(--background)",
                border="1px solid var(--border)"
            ),
            rx.vstack(
                rx.text(
                    preset_config["name"],
                    size="2",
                    weight="bold"
                ),
                rx.text(
                    preset_config["description"],
                    size="1",
                    color="gray",
                    text_align="center",
                    line_height="1.3"
                ),
                spacing="1",
                align="center",
                width="100%"
            ),
            rx.button(
                "Apply Style",
                size="1",
                width="100%",
                on_click=lambda: WorkflowState.apply_style_preset(preset_id)
            ),
            spacing="3",
            align="center",
            width="100%"
        ),
        padding="12px",
        border_radius="12px",
        border="1px solid var(--border)",
        background="var(--surface)",
        cursor="pointer",
        _hover={
            "border_color": "var(--primary)",
            "transform": "translateY(-2px)",
            "box_shadow": "0 4px 20px var(--shadow)"
        },
        transition="all 0.2s ease",
        width="140px"
    )

def style_presets_panel():
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.heading("Style Presets", size="4", weight="bold"),
                rx.button(
                    rx.icon("plus"),
                    size="1",
                    variant="ghost",
                    on_click=WorkflowState.open_custom_style_dialog
                ),
                justify="between",
                width="100%"
            ),

            rx.divider(),

            rx.vstack(
                rx.text("Quick Styles", size="2", weight="medium", color="gray"),
                rx.grid(
                    *[
                        style_preset_card(preset_id, config)
                        for preset_id, config in STYLE_PRESETS.items()
                    ],
                    columns="2",
                    spacing="3",
                    width="100%"
                ),
                spacing="3",
                width="100%"
            ),

            rx.divider(),

            rx.vstack(
                rx.text("Custom Styles", size="2", weight="medium", color="gray"),
                rx.cond(
                    WorkflowState.custom_styles.length() > 0,
                    rx.grid(
                        rx.foreach(
                            WorkflowState.custom_styles,
                            lambda style: style_preset_card(style.id, style.config)
                        ),
                        columns="2",
                        spacing="3",
                        width="100%"
                    ),
                    rx.center(
                        rx.text(
                            "No custom styles yet",
                            size="2",
                            color="gray"
                        ),
                        padding="20px"
                    )
                ),
                spacing="3",
                width="100%"
            ),

            spacing="4",
            width="100%",
            padding="20px"
        ),
        width="320px",
        height="100%",
        border_left="1px solid var(--border)",
        background="var(--surface)",
        overflow_y="auto"
    )
