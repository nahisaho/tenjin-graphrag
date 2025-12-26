"""MCP Prompts."""

# Prompts are registered via decorators in server.py
# Import modules to register prompts
from tengin_mcp.prompts import education_prompts

__all__ = [
    "education_prompts",
]
