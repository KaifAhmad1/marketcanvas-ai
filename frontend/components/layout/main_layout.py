import reflex as rx
from typing import Optional

from ..ui.theme_selector import theme_selector
from ...states.ui_state import UIState

def main_layout(
    *children,
    title: str = "MarketCanvas AI",
    show_navbar: bool = True,
    show_footer: bool = False,
    sidebar_content: Optional[rx.Component] = None,
    inspector_content: Optional[rx.Component] = None,
) -> rx.Component:

    navbar = rx.cond(
        show_navbar,
        rx.box(
            rx.hstack(
                rx.hstack(
                    rx.button(
                        rx.icon("home"),
                        variant="ghost",
                        size="2",
                        on_click=rx.redirect("/")
                    ),
                    rx.divider(orientation="vertical", height="20px"),
                    rx.text("MarketCanvas AI", size="3", weight="bold"),
                    spacing="3",
                    align="center"
                ),
                rx.spacer(),
                theme_selector(),
                spacing="3",
                align_items="center",
            ),
            padding="1rem 2rem",
            border_bottom="1px solid var(--border)",
            background="var(--background)",
            position="sticky",
            top="0",
            z_index="1000",
            width="100%",
        )
    )

    footer = rx.cond(
        show_footer,
        rx.box(
            rx.center(
                rx.text("© 2024 MarketCanvas AI. All rights reserved.", size="2", color="var(--text-muted)")
            ),
            padding="2rem",
            border_top="1px solid var(--border)",
            background="var(--surface)",
            width="100%",
        )
    )

    main_content_area = rx.hstack(
        rx.cond(sidebar_content, sidebar_content, rx.fragment()),
        rx.box(
            *children,
            flex_grow="1",
            padding="1.5rem",
            overflow_y="auto",
            height="calc(100vh - 60px)" if show_navbar else "100vh"
        ),
        rx.cond(inspector_content, inspector_content, rx.fragment()),
        spacing="0",
        align_items="stretch",
        width="100%",
        height="calc(100vh - 60px)" if show_navbar else "100vh"
    )

    return rx.box(
        navbar,
        main_content_area,
        footer,
        width="100vw",
        min_height="100vh",
        overflow_x="hidden",
    )
