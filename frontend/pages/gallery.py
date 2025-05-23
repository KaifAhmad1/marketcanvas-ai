import reflex as rx
from ..states.app_state import AppState

def gallery_item(image_url: str, title: str, description: str):
    return rx.box(
        rx.vstack(
            rx.image(
                src=image_url,
                width="100%",
                height="200px",
                object_fit="cover",
                border_radius="12px 12px 0 0"
            ),
            rx.vstack(
                rx.heading(title, size="3", weight="bold"),
                rx.text(description, size="2", color="gray"),
                spacing="2",
                align="start",
                padding="16px"
            ),
            spacing="0",
            width="100%"
        ),
        border_radius="12px",
        border="1px solid var(--border)",
        background="var(--surface)",
        overflow="hidden",
        _hover={
            "transform": "translateY(-4px)",
            "box_shadow": "0 8px 32px var(--shadow)"
        },
        transition="all 0.3s ease",
        cursor="pointer"
    )

def index():
    sample_items = [
        {
            "image_url": "https://images.unsplash.com/photo-1547036967-23d11aacaee0?w=400",
            "title": "Abstract Art",
            "description": "AI-generated abstract composition"
        },
        {
            "image_url": "https://images.unsplash.com/photo-1541701494587-cb58502866ab?w=400",
            "title": "Digital Portrait",
            "description": "Stylized portrait with AI enhancement"
        },
        {
            "image_url": "https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=400",
            "title": "Nature Scene",
            "description": "Enhanced landscape photography"
        }
    ] * 6

    return rx.fragment(
        rx.box(
            rx.hstack(
                rx.hstack(
                    rx.button(
                        rx.icon("arrow-left"),
                        variant="ghost",
                        size="2",
                        on_click=rx.redirect("/")
                    ),
                    rx.heading("Gallery", size="6", weight="bold"),
                    spacing="3",
                    align="center"
                ),
                rx.hstack(
                    rx.input(
                        placeholder="Search gallery...",
                        width="300px"
                    ),
                    rx.button(
                        rx.icon("filter"),
                        variant="outline",
                        size="2"
                    ),
                    spacing="2"
                ),
                justify="between",
                width="100%",
                padding="0 40px"
            ),
            padding="20px 0",
            border_bottom="1px solid var(--border)",
            background="var(--background)"
        ),

        rx.main(
            rx.container(
                rx.grid(
                    *[
                        gallery_item(
                            item["image_url"],
                            item["title"],
                            item["description"]
                        )
                        for item in sample_items
                    ],
                    columns="4",
                    spacing="6",
                    width="100%"
                ),
                max_width="1200px",
                padding="40px 20px"
            )
        )
    )
