import reflex as rx
from typing import Dict, Any, Optional

class UIState(rx.State):
    show_toolbar: bool = True
    show_inspector: bool = True
    show_style_panel: bool = False
    show_minimap: bool = True
    current_theme: str = "light"
    accent_color: str = "#6366f1"
    search_query: str = ""
    show_api_keys_dialog: bool = False
    show_export_dialog: bool = False
    show_settings_dialog: bool = False
    canvas_zoom: float = 1.0
    canvas_position: Dict[str, float] = {"x": 0, "y": 0}
    enable_animations: bool = True
    auto_save: bool = True

    @rx.event
    def toggle_toolbar(self):
        self.show_toolbar = not self.show_toolbar

    @rx.event
    def toggle_inspector(self):
        self.show_inspector = not self.show_inspector

    @rx.event
    def toggle_style_panel(self):
        self.show_style_panel = not self.show_style_panel

    @rx.event
    def toggle_minimap(self):
        self.show_minimap = not self.show_minimap

    @rx.event
    def set_theme(self, theme: str):
        self.current_theme = theme

    @rx.event
    def set_accent_color(self, color: str):
        self.accent_color = color

    @rx.event
    def set_search_query(self, query: str):
        self.search_query = query

    @rx.event
    def open_api_keys_dialog(self):
        self.show_api_keys_dialog = True

    @rx.event
    def close_api_keys_dialog(self):
        self.show_api_keys_dialog = False

    @rx.event
    def open_export_dialog(self):
        self.show_export_dialog = True

    @rx.event
    def close_export_dialog(self):
        self.show_export_dialog = False

    @rx.event
    def open_settings_dialog(self):
        self.show_settings_dialog = True

    @rx.event
    def close_settings_dialog(self):
        self.show_settings_dialog = False

    @rx.event
    def set_canvas_zoom(self, zoom: float):
        self.canvas_zoom = max(0.1, min(3.0, zoom))

    @rx.event
    def set_canvas_position(self, x: float, y: float):
        self.canvas_position = {"x": x, "y": y}

    @rx.event
    def reset_canvas_view(self):
        self.canvas_zoom = 1.0
        self.canvas_position = {"x": 0, "y": 0}
