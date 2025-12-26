"""MCP Resources."""

# Resources are registered via decorators in server.py
# Import modules to register resources
from tengin_mcp.resources import theory_resources

__all__ = [
    "theory_resources",
]
