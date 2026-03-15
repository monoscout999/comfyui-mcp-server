import json

from comfyui_mcp_server.managers.workflow_manager import WorkflowManager
from pathlib import Path

wf_dir = Path(r"C:\Users\aguse\Documents\ComfyUI\comfyui-mcp-server\workflows")
wm = WorkflowManager(wf_dir)

wf = wm.load_workflow("wan22_SVI_Pro_cyborg_GGUF")
print("Workflow keys:", wf.keys())
try:
    print("Extracting parameters...")
    params = wm._extract_parameters(wf)
    print("Success. Extracted params length:", len(params))
except Exception as e:
    import traceback
    traceback.print_exc()
