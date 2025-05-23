import reflex as rx
from typing import Dict, Any, Optional, List
from ...states.workflow_state import WorkflowState

def node_property_field(prop_name: str, prop_config: Dict[str, Any], current_value: Any = None):
    if prop_config["type"] == "text":
        return rx.vstack(
            rx.text(prop_name.replace("_", " ").title(), size="2", weight="medium"),
            rx.input(
                placeholder=f"Enter {prop_name}",
                value=current_value or "",
                on_change=lambda value: WorkflowState.update_node_property(prop_name, value),
                width="100%"
            ),
            spacing="1",
            width="100%"
        )

    elif prop_config["type"] == "textarea":
        return rx.vstack(
            rx.text(prop_name.replace("_", " ").title(), size="2", weight="medium"),
            rx.text_area(
                placeholder=f"Enter {prop_name}",
                value=current_value or "",
                on_change=lambda value: WorkflowState.update_node_property(prop_name, value),
                width="100%",
                min_height="80px"
            ),
            spacing="1",
            width="100%"
        )

    elif prop_config["type"] == "select":
        return rx.vstack(
            rx.text(prop_name.replace("_", " ").title(), size="2", weight="medium"),
            rx.select(
                prop_config["options"],
                value=current_value or prop_config["options"][0],
                on_change=lambda value: WorkflowState.update_node_property(prop_name, value),
                width="100%"
            ),
            spacing="1",
            width="100%"
        )

    elif prop_config["type"] == "number":
        return rx.vstack(
            rx.text(prop_name.replace("_", " ").title(), size="2", weight="medium"),
            rx.number_input(
                value=current_value or prop_config.get("default", 0),
                on_change=lambda value: WorkflowState.update_node_property(prop_name, value),
                width="100%"
            ),
            spacing="1",
            width="100%"
        )

    elif prop_config["type"] == "slider":
        return rx.vstack(
            rx.hstack(
                rx.text(prop_name.replace("_", " ").title(), size="2", weight="medium"),
                rx.text(str(current_value or prop_config.get("default", 0)), size="2", color="gray"),
                justify="between",
                width="100%"
            ),
            rx.slider(
                value=[current_value or prop_config.get("default", 0)],
                min=prop_config.get("min", 0),
                max=prop_config.get("max", 100),
                step=prop_config.get("step", 1),
                on_change=lambda value: WorkflowState.update_node_property(prop_name, value[0]),
                width="100%"
            ),
            spacing="1",
            width="100%"
        )

    elif prop_config["type"] == "color":
        return rx.vstack(
            rx.text(prop_name.replace("_", " ").title(), size="2", weight="medium"),
            rx.input(
                type="color",
                value=current_value or prop_config.get("default", "#000000"),
                on_change=lambda value: WorkflowState.update_node_property(prop_name, value),
                width="100%"
            ),
            spacing="1",
            width="100%"
        )

    elif prop_config["type"] == "file":
        return rx.vstack(
            rx.text(prop_name.replace("_", " ").title(), size="2", weight="medium"),
            rx.upload(
                rx.button("Upload File", size="2"),
                accept="image/*",
                on_upload=lambda files: WorkflowState.handle_file_upload(prop_name, files),
                width="100%"
            ),
            spacing="1",
            width="100%"
        )

    else:
        return rx.text(f"Unknown property type: {prop_config['type']}")

def node_inspector_panel():
    return rx.box(
        rx.cond(
            WorkflowState.selected_node.is_some(),
            rx.vstack(
                rx.hstack(
                    rx.heading(
                        "Node Inspector",
                        size="4",
                        weight="bold"
                    ),
                    rx.button(
                        rx.icon("x"),
                        size="1",
                        variant="ghost",
                        on_click=WorkflowState.clear_selection,
                        position="absolute",
                        top="12px",
                        right="12px"
                    ),
                    justify="between",
                    width="100%",
                    position="relative"
                ),

                rx.divider(),

                rx.vstack(
                    rx.text(
                        f"Node: {WorkflowState.selected_node.id}",
                        size="2",
                        weight="medium",
                        color="gray"
                    ),
                    rx.text(
                        f"Type: {WorkflowState.selected_node.type}",
                        size="2",
                        weight="medium",
                        color="gray"
                    ),
                    spacing="1",
                    width="100%"
                ),

                rx.divider(),

                rx.vstack(
                    rx.heading("Properties", size="3", weight="bold"),
                    rx.foreach(
                        WorkflowState.selected_node_properties,
                        lambda prop: node_property_field(
                            prop["name"],
                            prop["config"],
                            prop["value"]
                        )
                    ),
                    spacing="3",
                    width="100%"
                ),

                rx.divider(),

                rx.vstack(
                    rx.heading("Actions", size="3", weight="bold"),
                    rx.button(
                        "Execute Node",
                        size="2",
                        width="100%",
                        on_click=WorkflowState.execute_selected_node,
                        color_scheme="blue"
                    ),
                    rx.button(
                        "Duplicate Node",
                        size="2",
                        width="100%",
                        on_click=WorkflowState.duplicate_selected_node,
                        variant="outline"
                    ),
                    rx.button(
                        "Delete Node",
                        size="2",
                        width="100%",
                        on_click=WorkflowState.delete_selected_node,
                        color_scheme="red",
                        variant="outline"
                    ),
                    spacing="2",
                    width="100%"
                ),

                spacing="4",
                width="100%",
                padding="20px"
            ),
            rx.center(
                rx.vstack(
                    rx.icon("mouse-pointer", size=32, color="gray"),
                    rx.text(
                        "Select a node to view its properties",
                        size="3",
                        color="gray",
                        text_align="center"
                    ),
                    spacing="3"
                ),
                width="100%",
                height="100%"
            )
        ),
        width="350px",
        height="100%",
        border_left="1px solid var(--border)",
        background="var(--surface)",
        overflow_y="auto"
    )
