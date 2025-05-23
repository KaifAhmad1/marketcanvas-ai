import reflex as rx
from typing import Any, Dict, List, Union, Optional

class ReactFlowLib(rx.Component):
    library = "reactflow"

    def _get_custom_code(self) -> str:
        return """
import 'reactflow/dist/style.css';
import '@reactflow/node-resizer/dist/style.css';
import '@reactflow/minimap/dist/style.css';
"""

class ReactFlow(ReactFlowLib):
    tag = "ReactFlow"

    nodes: rx.Var[List[Dict[str, Any]]]
    edges: rx.Var[List[Dict[str, Any]]]

    fit_view: rx.Var[bool] = True
    fit_view_options: rx.Var[Dict[str, Any]] = {"padding": 0.2}

    nodes_draggable: rx.Var[bool] = True
    nodes_connectable: rx.Var[bool] = True
    nodes_focusable: rx.Var[bool] = True

    edges_updatable: rx.Var[bool] = True

    multi_selection_key_code: rx.Var[str] = "Meta"

    zoom_on_scroll: rx.Var[bool] = True
    zoom_on_pinch: rx.Var[bool] = True
    pan_on_scroll: rx.Var[bool] = False
    pan_on_drag: rx.Var[bool] = True

    snap_to_grid: rx.Var[bool] = True
    snap_grid: rx.Var[List[int]] = [15, 15]

    connection_mode: rx.Var[str] = "strict"

    on_nodes_change: rx.EventHandler[lambda changes: [changes]]
    on_edges_change: rx.EventHandler[lambda changes: [changes]]
    on_connect: rx.EventHandler[lambda connection: [connection]]
    on_connect_start: rx.EventHandler[lambda event, params: [event, params]]
    on_connect_end: rx.EventHandler[lambda event: [event]]
    on_click: rx.EventHandler[lambda event: [event]]
    on_node_click: rx.EventHandler[lambda event, node: [event, node]]
    on_edge_click: rx.EventHandler[lambda event, edge: [event, edge]]
    on_node_double_click: rx.EventHandler[lambda event, node: [event, node]]
    on_pane_click: rx.EventHandler[lambda event: [event]]
    on_pane_context_menu: rx.EventHandler[lambda event: [event]]
    on_selection_change: rx.EventHandler[lambda params: [params]]

class Background(ReactFlowLib):
    tag = "Background"

    color: rx.Var[str] = "#f1f5f9"
    variant: rx.Var[str] = "dots"
    gap: rx.Var[int] = 20
    size: rx.Var[int] = 1
    offset: rx.Var[int] = 2

class Controls(ReactFlowLib):
    tag = "Controls"

    show_zoom: rx.Var[bool] = True
    show_fit_view: rx.Var[bool] = True
    show_interactive: rx.Var[bool] = False
    fit_view_options: rx.Var[Dict[str, Any]] = {"padding": 0.1}

class MiniMap(ReactFlowLib):
    tag = "MiniMap"

    node_stroke_color: rx.Var[str] = "#555"
    node_color: rx.Var[str] = "#fff"
    node_border_radius: rx.Var[int] = 2
    mask_color: rx.Var[str] = "rgb(240, 242, 247, 0.7)"
    position: rx.Var[str] = "bottom-right"

class Panel(ReactFlowLib):
    tag = "Panel"

    position: rx.Var[str] = "top-left"

def create_custom_node_type(node_type: str, component_func):
    return {
        "type": node_type,
        "component": component_func
    }

def create_node(
    id: str,
    node_type: str,
    position: Dict[str, float],
    data: Dict[str, Any],
    **kwargs
) -> Dict[str, Any]:
    return {
        "id": id,
        "type": node_type,
        "position": position,
        "data": data,
        "draggable": kwargs.get("draggable", True),
        "selectable": kwargs.get("selectable", True),
        "deletable": kwargs.get("deletable", True),
        "width": kwargs.get("width"),
        "height": kwargs.get("height"),
        "style": kwargs.get("style", {}),
        "className": kwargs.get("className", ""),
        **{k: v for k, v in kwargs.items() if k not in [
            "draggable", "selectable", "deletable", "width", "height", "style", "className"
        ]}
    }

def create_edge(
    id: str,
    source: str,
    target: str,
    source_handle: Optional[str] = None,
    target_handle: Optional[str] = None,
    **kwargs
) -> Dict[str, Any]:
    edge = {
        "id": id,
        "source": source,
        "target": target,
        "animated": kwargs.get("animated", False),
        "style": kwargs.get("style", {}),
        "type": kwargs.get("type", "default"),
        "label": kwargs.get("label"),
        "labelStyle": kwargs.get("labelStyle", {}),
        "labelShowBg": kwargs.get("labelShowBg", True),
        "labelBgStyle": kwargs.get("labelBgStyle", {}),
    }

    if source_handle:
        edge["sourceHandle"] = source_handle
    if target_handle:
        edge["targetHandle"] = target_handle

    return edge

class NodeResizer(ReactFlowLib):
    tag = "NodeResizer"
    library = "@reactflow/node-resizer"

    color: rx.Var[str] = "#ff0071"
    is_visible: rx.Var[bool] = True
    min_width: rx.Var[int] = 10
    min_height: rx.Var[int] = 10
    max_width: rx.Var[int] = float('inf')
    max_height: rx.Var[int] = float('inf')
    keep_aspect_ratio: rx.Var[bool] = False

node_resizer = NodeResizer.create
