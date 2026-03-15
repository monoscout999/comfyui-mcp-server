---
name: ComfyUI Agent Operations
description: How to efficiently work with ComfyUI via MCP servers — workflow execution, node discovery, model management, and image generation.
---

# ComfyUI Agent Operations

> **Read this FIRST** before doing anything with ComfyUI. This replaces any ad-hoc approaches (curl, python scripts, manual JSON editing).

---

## Key Facts

- **ComfyUI Desktop** runs at `http://127.0.0.1:8000`
- **Workspace**: `C:/Users/aguse/Documents/ComfyUI`
- **Two MCP servers** are available (see below for when to use each)
- **User workflows** are at `user/default/workflows/` (SINGLE SOURCE OF TRUTH)
- **Models** are at `models/` (checkpoints, loras, vae, controlnet, etc.)
- **Input images** go to `input/`
- **Output images** go to `output/`

---

## Which MCP Server to Use

### `comfyui-builder` (PRIMARY — use for almost everything)

This is the **Node.js MCP server** (`mcp-comfy-ui-builder`). It has 50+ tools and is the most capable.

**Use for:**
- Building workflows (templates or dynamic)
- Executing workflows (`execute_workflow`, `execute_workflow_sync`)
- Exploring nodes (`search_nodes`, `get_node_info`, `get_node_inputs`)
- Managing models (`list_models`, `check_model_exists`, `install_model`)
- Chaining workflows (`execute_chain`)
- Downloading outputs (`download_output`, `download_by_filename`)
- Inspecting workflow structure (`list_workflow_nodes`)
- System resources check (`get_system_resources`)
- Installing custom nodes (`install_custom_node`) — requires `COMFYUI_PATH`
- Restarting ComfyUI (`reload_comfyui`)

**Environment variables** (set in `.mcp.json`):
- `COMFYUI_HOST` = `http://127.0.0.1:8000` — ComfyUI API endpoint
- `COMFYUI_PATH` = `C:/Users/aguse/Documents/ComfyUI` — enables install_model, install_custom_node

### `comfyui-mcp-server` (SECONDARY — generation shortcuts only)

This is the **Python HTTP server** on port 9000. It must be started manually via `start_mcp_server.bat` (ComfyUI Desktop must be running first).

**Use ONLY for:**
- Quick `generate_image` with just a prompt (no workflow building needed)
- `regenerate` an existing asset with tweaks
- `publish_asset` to a web project
- `view_image` inline

> **RULE**: If you need to build, inspect, or execute a workflow → use `comfyui-builder`.
> If you just need a quick image from a prompt → `comfyui-mcp-server` is fine.

---

## ⚡ Common Tasks (Step-by-Step)

### 1. Execute an Existing Workflow JSON File

**DO NOT** read the file and paste it as a string. Use the tools:

```
1. load_workflow(name_or_path)     → returns workflow JSON
2. check_workflow_models(workflow)  → verify all models exist
3. execute_workflow_sync(workflow)  → run and wait for result
4. download_by_filename(filename, dest_path) → save output locally
```

For workflows in `user/default/workflows/`, use the full path:
```
load_workflow("C:/Users/aguse/Documents/ComfyUI/user/default/workflows/myworkflow.json")
```

### 2. Generate an Image (txt2img)

```
1. get_system_resources()                    → check GPU/VRAM limits
2. list_models(type="checkpoint")            → find available checkpoints
3. build_workflow("txt2img", { prompt: "...", ckpt_name: "...", width: N, height: N })
4. execute_workflow_sync(workflow)
5. download_by_filename(filename, dest_path) → save result
```

### 3. Execute a Large/Complex Workflow (e.g. Wan2.2, video)

For workflows with group nodes or 50+ nodes:

```
1. load_workflow(path)                      → load from file
2. list_workflow_nodes(workflow)             → inspect all nodes (expands groups!)
3. check_workflow_models(workflow)           → verify models
4. execute_workflow_sync(workflow, timeout_ms=600000)  → longer timeout for video
5. get_last_output()                         → if sync timed out
6. download_by_filename(filename, dest_path)
```

> **TIP**: `list_workflow_nodes` expands group nodes automatically — no need for external scripts.

### 4. Modify Parameters in an Existing Workflow

Don't manually edit JSON. After loading:

```
1. load_workflow(path)              → get workflow JSON
2. list_workflow_nodes(workflow)    → find node IDs and their class_types
3. Parse the JSON, find the node ID you need to change
4. Modify the input value in the workflow JSON dict
5. execute_workflow_sync(modified_workflow)
```

Or if building from scratch:
```
1. create_workflow()                → get workflow_id
2. add_node(workflow_id, "NodeClass", { inputs... })  → add nodes
3. connect_nodes(workflow_id, from, idx, to, input)   → wire them
4. finalize_workflow(workflow_id)     → get JSON
5. execute_workflow_sync(workflow)
```

### 5. Explore Available Nodes

```
1. search_nodes(query="depth")           → find nodes by name/description
2. get_node_info("NodeClassName")        → full info about a node
3. get_node_inputs("NodeClassName")      → detailed input definitions (with enum values)
4. get_node_outputs("NodeClassName")     → output types
5. check_compatibility("NodeA", "NodeB") → can they connect?
```

### 6. Check and Install Models

```
1. list_models(type="checkpoint")        → see what's available
2. check_model_exists("model.safetensors", "checkpoint") → verify specific model
3. install_model(url, model_type)        → download and install (needs COMFYUI_PATH)
```

### 7. Chain Workflows (txt2img → upscale → img2img)

```
execute_chain(steps=[
  { workflow: txt2img_workflow },
  { workflow: upscale_workflow, inputFrom: { step: 0, outputNode: "9", outputIndex: 0 }, outputTo: "image" },
  { workflow: img2img_workflow, inputFrom: { step: 1, outputNode: "3", outputIndex: 0 }, outputTo: "image" }
])
```

---

## ❌ Things to NEVER Do

| Bad Practice | Use Instead |
|-------------|-------------|
| `curl http://127.0.0.1:8000/prompt ...` | `execute_workflow_sync(workflow)` |
| `python server.py` or manual server start | MCP servers are already configured in `.mcp.json` |
| Manually parse/edit large workflow JSON | `list_workflow_nodes` + targeted edits |
| Create a .py script to extract nodes | `list_workflow_nodes(workflow)` does this |
| `pip install` or `npm install` inside ComfyUI | `install_custom_node` or ask user |
| Guess model filenames | `list_models(type)` to see exact names |
| Run workflow with wrong resolution | `get_system_resources()` first |
| Store workflows in workspace root | Use `user/default/workflows/` only |

---

## 📁 Workspace Map

```
C:/Users/aguse/Documents/ComfyUI/
├── .mcp.json                          # MCP server config (SINGLE SOURCE OF TRUTH)
├── .agents/                           # Agent workflows and skills
│   ├── skills/comfyui/SKILL.md        # This file
│   └── workflows/                     # /run-workflow, /create-image, etc.
├── start_mcp_server.bat               # Manual start for Python MCP server
├── input/                             # Input images for workflows
├── output/                            # Generated outputs
├── models/
│   ├── checkpoints/                   # SD, SDXL, Flux checkpoints
│   ├── loras/                         # LoRA models
│   ├── vae/                           # VAE models
│   ├── controlnet/                    # ControlNet models
│   └── ...
├── user/default/workflows/            # ★ ALL user workflows go here
├── custom_nodes/                      # Installed ComfyUI custom nodes
├── comfyui-mcp-server/                # Python MCP server (port 9000)
│   └── workflows/                     # ONLY PARAM_* templates for this server
├── mcp-comfy-ui-builder/              # Node.js MCP server (primary)
│   ├── doc/                           # Full documentation
│   │   ├── AI-ASSISTANT-GUIDE.md      # Detailed guide (read if confused)
│   │   └── workflow-builder.md        # Template reference
│   └── knowledge/                     # Node knowledge base
└── .venv/                             # Python virtual environment
```

---

## ⚙️ Configuration Reference

| Variable | Server | Value | Purpose |
|----------|--------|-------|---------|
| `COMFYUI_HOST` | Builder (Node.js) | `http://127.0.0.1:8000` | ComfyUI API URL |
| `COMFYUI_PATH` | Builder (Node.js) | `C:/Users/aguse/Documents/ComfyUI` | Install models/nodes |
| `COMFYUI_URL` | Python server | `http://127.0.0.1:8000` | Set in `start_mcp_server.bat` |

> **NOTE**: The Python server uses `COMFYUI_URL` (not `COMFYUI_HOST`). Both default to 8188 in code but are set to 8000 to match ComfyUI Desktop.

---

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| Tool returns error about COMFYUI_HOST | ComfyUI Desktop must be running (port 8000) |
| `install_model` fails | Verify `COMFYUI_PATH` is set in `.mcp.json` |
| Model not found | Run `list_models(type)` to see exact filename |
| Workflow too large for context | Use `list_workflow_nodes` to inspect, modify specific nodes |
| `execute_workflow_sync` timed out | Use `get_last_output()` then `download_by_filename()` |
| Don't know what nodes exist | `search_nodes(query)` or `suggest_nodes(task_description)` |
| Group nodes in workflow | `list_workflow_nodes` expands them automatically |
| Python MCP server not responding | Run `start_mcp_server.bat` (ComfyUI must be running first) |

---

## 📚 Deep Reference

If you need more detail on any tool, read:
- `C:/Users/aguse/Documents/ComfyUI/mcp-comfy-ui-builder/doc/AI-ASSISTANT-GUIDE.md`
- `C:/Users/aguse/Documents/ComfyUI/mcp-comfy-ui-builder/doc/workflow-builder.md`
- `C:/Users/aguse/Documents/ComfyUI/comfyui-mcp-server/README.md`
