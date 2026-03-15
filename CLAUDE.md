# Agent Instructions: comfyui-mcp-server

## Goal
- Keep MCP workflows and tool contracts predictable for AI agents.

## Change Rules
- Keep path-safety checks intact in publish and workflow loading code.
- Do not bypass `AssetRegistry` for asset identity or lookup.
- If you change tool responses, update `docs/REFERENCE.md` and tests.

## Validation
- Run `python -m pytest tests -q` before finishing.
- Prefer deterministic tests (no network dependency unless explicitly integration-marked).

## Error Handling
- Return `error`, `error_code`, and a clear `message` when failing.
- Keep human-readable hints short and actionable.

## Documentation
- Keep `README.md`, `docs/REFERENCE.md`, and `docs/ARCHITECTURE.md` consistent.
