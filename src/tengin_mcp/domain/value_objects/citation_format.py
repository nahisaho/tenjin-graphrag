"""Value Objects: Citation Format Enum."""

from enum import Enum


class CitationFormat(str, Enum):
    """引用形式。"""

    APA7 = "APA7"
    """APA 7th Edition"""

    MLA9 = "MLA9"
    """MLA 9th Edition"""

    CHICAGO = "Chicago"
    """Chicago Manual of Style"""

    HARVARD = "Harvard"
    """Harvard Referencing"""

    IEEE = "IEEE"
    """IEEE Citation Style"""

    def __str__(self) -> str:
        return self.value
