"""Value Objects: Theory Category Enum."""

from enum import Enum


class TheoryCategory(str, Enum):
    """教育理論のカテゴリ分類。"""

    LEARNING = "learning"
    """学習理論（行動主義、認知主義、構成主義など）"""

    INSTRUCTIONAL = "instructional"
    """教授理論（ガニェ、メリル、ARCSなど）"""

    DEVELOPMENTAL = "developmental"
    """発達理論（ピアジェ、ヴィゴツキーなど）"""

    MOTIVATION = "motivation"
    """動機付け理論（自己決定理論、フロー理論など）"""

    EDTECH = "edtech"
    """教育工学（ADDIE、UDLなど）"""

    ADULT_LEARNING = "adult_learning"
    """成人学習理論（アンドラゴジー、変容的学習理論など）"""

    INTELLIGENCE = "intelligence"
    """知能理論（多重知能理論など）"""

    def __str__(self) -> str:
        return self.value

    @classmethod
    def from_string(cls, value: str) -> "TheoryCategory":
        """文字列からカテゴリを取得。"""
        try:
            return cls(value.lower())
        except ValueError as e:
            valid = ", ".join(c.value for c in cls)
            raise ValueError(f"Invalid category: {value}. Valid categories: {valid}") from e
