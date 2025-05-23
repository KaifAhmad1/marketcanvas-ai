import reflex as rx
from ..components.ui.theme_selector import theme_selector
from ..states.app_state import AppState
from ..states.ui_state import UIState

def hero_section():
    return rx.section(
        rx.vstack(
            rx.center(
                rx.vstack(
                    rx.heading(
                        "MarketCanvas AI",
                        size="9",
                        weight="bold",
                        background="linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #ec4899 100%)",
                        background_clip="text",
                        style={"-webkit-background-clip": "text", "color": "transparent"}
                    ),
                    rx.text(
                        "Create stunning visuals with AI-powered workflows",
                        size="5",
                        color="gray",
                        text_align="center",
                        max_width="600px"
                    ),
                    rx.hstack(
                        rx.button(
                            "Start Creating",
                            size="4",
                            color_scheme="blue",
                            on_click=rx.redirect("/editor")
                        ),
                        rx.button(
                            "View Gallery",
                            size="4",
                            variant="outline",
                            on_click=rx.redirect("/gallery")
                        ),
                        spacing="4"
                    ),
                    spacing="6",
                    align="center"
                ),
                width="100%",
                min_height="60vh"
            ),
            spacing="8"
        ),
        width="100%",
        padding="40px 20px"
    )

def features_section():
    features = [
        {
            "icon": "wand-2",
            "title": "AI-Powered Generation",
            "description": "Generate stunning images from text prompts using multiple AI providers"
        },
        {
            "icon": "workflow",
            "title": "Visual Workflows",
            "description": "Build complex image processing pipelines with drag-and-drop simplicity"
        },
        {
            "icon": "palette",
            "title": "Style Presets",
            "description": "Apply professional styles and effects with one click"
        },
        {
            "icon": "layers",
            "title": "Multi-Provider Support",
            "description": "Use OpenAI, Stability AI, Fal.ai, and more in a single workflow"
        },
        {
            "icon": "download",
            "title": "Export & Share",
            "description": "Export your creations in multiple formats and share workflows"
        },
        {
            "icon": "zap",
            "title": "Real-time Processing",
            "description": "See results instantly with optimized processing pipelines"
        }
    ]

    return rx.section(
        rx.vstack(
            rx.center(
                rx.vstack(
                    rx.heading("Powerful Features", size="7", weight="bold"),
                    rx.text(
                        "Everything you need to create professional visuals",
                        size="4",
                        color="gray",
                        text_align="center"
                    ),
                    spacing="4",
                    align="center"
                )
            ),
            rx.grid(
                *[
                    rx.box(
                        rx.vstack(
                            rx.center(
                                rx.icon(
                                    feature["icon"],
                                    size=32,
                                    color="var(--primary)"
                                ),
                                width="64px",
                                height="64px",
                                border_radius="16px",
                                background="var(--surface)",
                                border="1px solid var(--border)"
                            ),
                            rx.heading(feature["title"], size="4", weight="bold"),
                            rx.text(
                                feature["description"],
                                size="3",
                                color="gray",
                                text_align="center",
                                line_height="1.5"
                            ),
                            spacing="4",
                            align="center"
                        ),
                        padding="24px",
                        border_radius="16px",
                        border="1px solid var(--border)",
                        background="var(--surface)",
                        _hover={
                            "transform": "translateY(-4px)",
                            "box_shadow": "0 8px 32px var(--shadow)"
                        },
                        transition="all 0.3s ease"
                    )
                    for feature in features
                ],
                columns="3",
                spacing="6",
                width="100%"
            ),
            spacing="12",
            width="100%"
        ),
        padding="80px 20px"
    )

def cta_section():
    return rx.section(
        rx.center(
            rx.box(
                rx.vstack(
                    rx.heading(
                        "Ready to Create?",
                        size="7",
                        weight="bold",
                        color="white"
                    ),
                    rx.text(
                        "Join thousands of creators using MarketCanvas AI",
                        size="4",
                        color="rgba(255, 255, 255, 0.8)",
                        text_align="center"
                    ),
                    rx.button(
                        "Get Started Now",
                        size="4",
                        color_scheme="white",
                        variant="solid",
                        on_click=rx.redirect("/editor")
                    ),
                    spacing="6",
                    align="center"
                ),
                padding="60px 40px",
                border_radius="24px",
                background="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                width="100%",
                max_width="800px"
            )
        ),
        padding="80px 20px"
    )

def index():
    return rx.fragment(
        rx.box(
            rx.hstack(
                rx.hstack(
                    rx.icon("palette", size=24, color="var(--primary)"),
                    rx.heading("MarketCanvas AI", size="5", weight="bold"),
                    spacing="2",
                    align="center"
                ),
                rx.hstack(
                    rx.button(
                        "Editor",
                        variant="ghost",
                        on_click=rx.redirect("/editor")
                    ),
                    rx.button(
                        "Gallery",
                        variant="ghost",
                        on_click=rx.redirect("/gallery")
                    ),
                    theme_selector(),
                    spacing="2"
                ),
                justify="between",
                width="100%",
                padding="0 40px"
            ),
            padding="20px 0",
            border_bottom="1px solid var(--border)",
            background="var(--background)",
            position="sticky",
            top="0",
            z_index="50"
        ),

        rx.main(
            hero_section(),
            features_section(),
            cta_section(),
            width="100%"
        ),

        rx.footer(
            rx.center(
                rx.text(
                    "© 2024 MarketCanvas AI. Built with Reflex.",
                    size="2",
                    color="gray"
                )
            ),
            padding="40px 20px",
            border_top="1px solid var(--border)",
            background="var(--surface)"
        )
    )
