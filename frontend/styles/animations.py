import reflex as rx

ANIMATION_DEFINITIONS = {
    "float": {
        "animation_name": "float",
        "animation_duration": "3s",
        "animation_timing_function": "ease-in-out",
        "animation_iteration_count": "infinite",
    },
    "pulse_slow": {
        "animation_name": "pulse",
        "animation_duration": "4s",
        "animation_timing_function": "cubic-bezier(0.4, 0, 0.6, 1)",
        "animation_iteration_count": "infinite",
    },
    "gradient_bg_animated": {
        "background": "linear-gradient(135deg, #667eea 0%, #764ba2 50%, #667eea 100%)",
        "background_size": "200% 200%",
        "animation_name": "gradient",
        "animation_duration": "3s",
        "animation_timing_function": "ease",
        "animation_iteration_count": "infinite",
    }
}

def animated_box(*children, animation_name: str = "float", **props) -> rx.Component:
    style = props.pop("style", {})
    style["animation"] = f"{animation_name} 3s ease-in-out infinite"

    if animation_name in ANIMATION_DEFINITIONS:
        props["class_name"] = props.get("class_name", "") + f" animate-{animation_name.replace('_', '-')}"

    return rx.box(
        *children,
        style=style,
        **props
    )
