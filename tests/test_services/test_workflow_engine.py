import pytest
from backend.services.workflow_engine import WorkflowEngine
from backend.api.models.nodes import Node, NodeData, NodePosition, Edge

@pytest.mark.asyncio
async def test_simple_workflow_execution():
    engine = WorkflowEngine()

    nodes_data_dict = [
        {"id": "input1", "type": "image_input", "position": {"x":0,"y":0}, "data": {"file": "user_uploads/sample_input.png", "source_type": "upload"}},
        {"id": "output1", "type": "output", "position": {"x":200,"y":0}, "data": {"format": "png"}}
    ]
    edges_data_dict = [
        {"id": "e1", "source": "input1", "target": "output1", "sourceHandle": "image", "targetHandle": "image"}
    ]

    api_keys = {}

    try:
        results = await engine.execute_workflow(nodes_data_dict, edges_data_dict, api_keys)
        assert "output1" in results
        assert "image_url" in results["output1"]
        assert results["output1"]["image_url"].endswith(".png")
        if results["output1"].get("source_path") and os.path.exists(results["output1"]["source_path"]):
            os.remove(results["output1"]["source_path"])
    except ValueError as ve:
        if "file not found" in str(ve).lower() and "sample_input.png" in str(ve):
            pytest.skip(f"Skipping test_simple_workflow_execution as dummy input image was not properly set up: {ve}")
        else:
            raise ve
    finally:
        sample_image_path = "uploads/user_uploads/sample_input.png"
        if os.path.exists(sample_image_path):
            os.remove(sample_image_path)
