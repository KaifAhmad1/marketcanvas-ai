import reflex as rx
from ...states.ui_state import UIState

def theme_selector():
    return rx.popover.root(
        rx.popover.trigger(
            rx.button(
                rx.icon("palette"),
                rx.text("Theme"),
                size="2",
                variant="outline"
            )
        ),
        rx.popover.content(
            rx.vstack(
                rx.text("Choose Theme", size="3", weight="bold"),

                rx.divider(),

                rx.vstack(
                    rx.button(
                        rx.hstack(
                            rx.box(
                                width="16px",
                                height="16px",
                                border_radius="50%",
                                background="linear-gradient(135deg, #ffffff 0%, #f8fafc 100%)",
                                border="1px solid #e2e8f0"
                            ),
                            rx.text("Light", size="2"),
                            justify="start",
                            spacing="2"
                        ),
                        width="100%",
                        variant="ghost" if UIState.current_theme != "light" else "solid",
                        on_click=lambda: UIState.set_theme("light")
                    ),

                    rx.button(
                        rx.hstack(
                            rx.box(
                                width="16px",
                                height="16px",
                                border_radius="50%",
                                background="linear-gradient(135deg, #0f172a 0%, #1e293b 100%)",
                                border="1px solid #334155"
                            ),
                            rx.text("Dark", size="2"),
                            justify="start",
                            spacing="2"
                        ),
                        width="100%",
                        variant="ghost" if UIState.current_theme != "dark" else "solid",
                        on_click=lambda: UIState.set_theme("dark")
                    ),

                    rx.button(
                        rx.hstack(
                            rx.box(
                                width="16px",
                                height="16px",
                                border_radius="50%",
                                background="linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
                            ),
                            rx.text("Cosmic", size="2"),
                            justify="start",
                            spacing="2"
                        ),
                        width="100%",
                        variant="ghost" if UIState.current_theme != "cosmic" else "solid",
                        on_click=lambda: UIState.set_theme("cosmic")
                    ),

                    rx.button(
                        rx.hstack(
                            rx.box(
                                width="16px",
                                height="16px",
                                border_radius="50%",
                                background="linear-gradient(135deg, #ff6b6b 0%, #4ecdc4 100%)"
                            ),
                            rx.text("Sunset", size="2"),
                            justify="start",
                            spacing="2"
                        ),
                        width="100%",
                        variant="ghost" if UIState.current_theme != "sunset" else "solid",
                        on_click=lambda: UIState.set_theme("sunset")
                    ),

                    spacing="1",
                    width="100%"
                ),

                rx.divider(),

                rx.vstack(
                    rx.text("Customization", size="2", weight="medium", color="gray"),
                    rx.hstack(
                        rx.text("Accent Color", size="2"),
                        rx.input(
                            type="color",
                            value=UIState.accent_color,
                            on_change=UIState.set_accent_color,
                            width="40px",
                            height="30px"
                        ),
                        justify="between",
                        width="100%"
                    ),
                    spacing="2",
                    width="100%"
                ),

                spacing="3",
                width="200px",
                padding="4px"
            ),
            side="bottom",
            align="center"
        )
    )
