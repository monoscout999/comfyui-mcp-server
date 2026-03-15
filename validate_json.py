import json
wf_path = r"C:\Users\aguse\Documents\ComfyUI\comfyui-mcp-server\workflows\wan22_SVI_Pro_cyborg_GGUF.json"
with open(wf_path, "r", encoding="utf-8") as f:
    wf = json.load(f)

for k, v in wf.items():
    if not isinstance(v, dict):
        print(f"Key '{k}' has a value of type {type(v).__name__}: {v}")
    elif "class_type" not in v:
        print(f"Key '{k}' is missing class_type: {v}")

print("Validation completed.")
