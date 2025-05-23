import reflex as rx
from ..components.reactflow.reactflow_wrapper import react_flow, background, controls, minimap, panel
from ..components.ui.toolbar import main_toolbar
from ..components.ui.node_inspector import node_inspector_panel
from ..components.ui.style_presets import style_presets_panel
from ..components.ui.theme_selector import theme_selector
from ..states.workflow_state import WorkflowState
from ..states.ui_state import UIState
from ..states.app_state import AppState

def top_menu_bar():
    return rx.box(
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

            rx.hstack(
                rx.button(
                    rx.icon("play"),
                    "Execute",
                    size="2",
                    color_scheme="green",
                    loading=WorkflowState.is_executing,
                    on_click=WorkflowState.execute_workflow
                ),
                rx.button(
                    rx.icon("square"),
                    "Stop",
                    size="2",
                    variant="outline",
                    disabled=~WorkflowState.is_executing
                ),
                rx.divider(orientation="vertical", height="20px"),
                rx.button(
                    rx.icon("save"),
                    "Save",
                    size="2",
                    variant="outline"
                ),
                rx.button(
                    rx.icon("upload"),
                    "Load",
                    size="2",
                    variant="outline"
                ),
                spacing="2",
                align="center"
            ),

            rx.hstack(
                rx.button(
                    rx.icon("panel-left"),
                    size="2",
                    variant="ghost",
                    on_click=UIState.toggle_toolbar
                ),
                rx.button(
                    rx.icon("panel-right"),
                    size="2",
                    variant="ghost",
                    on_click=UIState.toggle_inspector
                ),
                rx.button(
                    rx.icon("palette"),
                    size="2",
                    variant="ghost",
                    on_click=UIState.toggle_style_panel
                ),
                rx.divider(orientation="vertical", height="20px"),
                rx.button(
                    rx.icon("settings"),
                    size="2",
                    variant="ghost",
                    on_click=UIState.open_settings_dialog
                ),
                theme_selector(),
                spacing="2",
                align="center"
            ),

            justify="between",
            width="100%",
            padding="0 20px"
        ),
        width="100%",
        height="60px",
        padding="10px 0",
        border_bottom="1px solid var(--border)",
        background="var(--background)",
        display="flex",
        align_items="center"
    )

def workflow_canvas():
    return rx.box(
        react_flow(
            nodes=WorkflowState.nodes,
            edges=WorkflowState.edges,
            on_nodes_change=lambda changes: WorkflowState.handle_nodes_change(changes),
            on_edges_change=lambda changes: WorkflowState.handle_edges_change(changes),
            on_connect=lambda connection: WorkflowState.add_edge(
                connection["source"],
                connection["target"]
            ),
            on_node_click=lambda evt, node: WorkflowState.select_node(node["id"]),
            on_edge_click=lambda evt, edge: WorkflowState.select_edge(edge["id"]),
            on_pane_click=lambda evt: WorkflowState.clear_selection(),
            fit_view=True,
            snap_to_grid=True,
            snap_grid=[15, 15],
            children=[
                background(variant="dots", gap=20),
                controls(show_zoom=True, show_fit_view=True),
                rx.cond(
                    UIState.show_minimap,
                    minimap(position="bottom-right")
                ),
                panel(
                    rx.hstack(
                        rx.text(f"Nodes: {WorkflowState.nodes.length()}", size="1"),
                        rx.text(f"Edges: {WorkflowState.edges.length()}", size="1"),
                        rx.text(
                            rx.cond(
                                WorkflowState.is_executing,
                                "Executing...",
                                "Ready"
                            ),
                            size="1",
                            color=rx.cond(
                                WorkflowState.is_executing,
                                "orange",
                                "green"
                            )
                        ),
                        spacing="4"
                    ),
                    position="top-left"
                )
            ]
        ),
        width="100%",
        height="100%",
        position="relative"
    )

def index():
    return rx.fragment(
        top_menu_bar(),

        rx.hstack(
            rx.cond(
                UIState.show_toolbar,
                main_toolbar()
            ),

            rx.box(
                workflow_canvas(),
                flex="1",
                height="calc(100vh - 60px)",
                overflow="hidden"
            ),

            rx.hstack(
                rx.cond(
                    UIState.show_style_panel,
                    style_presets_panel()
                ),
                rx.cond(
                    UIState.show_inspector,
                    node_inspector_panel()
                ),
                spacing="0"
            ),

            spacing="0",
            width="100%",
            height="calc(100vh - 60px)"
        ),

        width="100%",
        height="100vh",
        overflow="hidden"
    )
