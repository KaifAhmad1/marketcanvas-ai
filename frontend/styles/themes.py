import reflex as rx
from typing import Dict, Any

ACCENT_COLORS = [
    "tomato", "red", "ruby", "crimson", "pink", "plum", "purple", "violet",
    "iris", "indigo", "blue", "cyan", "teal", "jade", "green", "grass",
    "brown", "orange", "sky", "mint", "lime", "yellow", "amber", "gold",
    "bronze", "gray"
]

def get_theme_styles(theme_name: str = "light", accent_color: str = "indigo") -> Dict[str, Any]:
    radix_theme_props = {
        "accent_color": accent_color if accent_color in ACCENT_COLORS else "indigo",
        "gray_color": "slate",
        "panel_background": "solid",
        "radius": "medium",
        "scaling": "100%",
    }

    return radix_theme_props
