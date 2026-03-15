"""Shared helpers for consistent MCP tool error payloads."""

from typing import Any, Dict, Optional


def tool_error(
    message: str,
    code: str = "TOOL_ERROR",
    *,
    hint: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None,
    status: str = "error",
) -> Dict[str, Any]:
    """Build a structured error payload while keeping backward compatibility."""
    payload: Dict[str, Any] = {
        "status": status,
        "error": message,
        "error_code": code,
        "message": message,
    }
    if hint:
        payload["hint"] = hint
    if details:
        payload["details"] = details
    return payload


def exception_error(
    exc: Exception,
    code: str = "TOOL_ERROR",
    *,
    hint: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Convert an exception into a structured error payload."""
    return tool_error(str(exc), code=code, hint=hint, details=details)
