"""Value Objects: Evidence Level Enum."""

from enum import Enum


class EvidenceLevel(str, Enum):
    """エビデンスの強度レベル。"""

    STRONG = "strong"
    """強いエビデンス（メタ分析、複数のRCTによる支持）"""

    MODERATE = "moderate"
    """中程度のエビデンス（RCTや準実験的研究による支持）"""

    LIMITED = "limited"
    """限定的なエビデンス（質的研究や事例研究による支持）"""

    THEORETICAL = "theoretical"
    """理論的（主に理論的枠組み、実証研究が少ない）"""

    EMERGING = "emerging"
    """発展中（新しい理論、研究が進行中）"""

    def __str__(self) -> str:
        return self.value

    @property
    def strength_order(self) -> int:
        """エビデンスの強さを数値で返す（比較用）。"""
        order_map = {
            EvidenceLevel.STRONG: 5,
            EvidenceLevel.MODERATE: 4,
            EvidenceLevel.LIMITED: 3,
            EvidenceLevel.THEORETICAL: 2,
            EvidenceLevel.EMERGING: 1,
        }
        return order_map[self]

    def __lt__(self, other: "EvidenceLevel") -> bool:
        return self.strength_order < other.strength_order

    def __le__(self, other: "EvidenceLevel") -> bool:
        return self.strength_order <= other.strength_order
