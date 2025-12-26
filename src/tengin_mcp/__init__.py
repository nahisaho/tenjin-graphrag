"""TENGIN Education Theory MCP Server.

教育理論ナレッジグラフを提供するMCPサーバー。
"""

__version__ = "0.1.0"

# Domain layer exports
from tengin_mcp.domain import (
    # Value Objects
    CitationFormat,
    # Entities
    Concept,
    ConceptSummary,
    # Errors
    DatabaseConnectionError,
    Evidence,
    EvidenceLevel,
    EvidenceSummary,
    GraphRAGError,
    # Repositories
    GraphRepository,
    InvalidQueryError,
    Principle,
    PrincipleSummary,
    Theorist,
    TheoristSummary,
    Theory,
    TheoryCategory,
    TheoryNotFoundError,
    TheoryRepository,
    TheorySummary,
)

__all__ = [
    "__version__",
    # Entities
    "Concept",
    "ConceptSummary",
    "Evidence",
    "EvidenceSummary",
    "Principle",
    "PrincipleSummary",
    "Theorist",
    "TheoristSummary",
    "Theory",
    "TheorySummary",
    # Value Objects
    "CitationFormat",
    "EvidenceLevel",
    "TheoryCategory",
    # Repositories
    "GraphRepository",
    "TheoryRepository",
    # Errors
    "DatabaseConnectionError",
    "GraphRAGError",
    "InvalidQueryError",
    "TheoryNotFoundError",
]
