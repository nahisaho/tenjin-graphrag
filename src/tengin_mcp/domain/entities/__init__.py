"""Domain Entities."""

from tengin_mcp.domain.entities.concept import Concept, ConceptSummary
from tengin_mcp.domain.entities.evidence import Evidence, EvidenceSummary
from tengin_mcp.domain.entities.principle import Principle, PrincipleSummary
from tengin_mcp.domain.entities.theorist import Theorist, TheoristSummary
from tengin_mcp.domain.entities.theory import Theory, TheorySummary

__all__ = [
    "Theory",
    "TheorySummary",
    "Theorist",
    "TheoristSummary",
    "Concept",
    "ConceptSummary",
    "Principle",
    "PrincipleSummary",
    "Evidence",
    "EvidenceSummary",
]
