"""Domain Entity: Theory - 教育理論."""

from datetime import datetime

from pydantic import BaseModel, Field

from tengin_mcp.domain.value_objects.evidence_level import EvidenceLevel
from tengin_mcp.domain.value_objects.theory_category import TheoryCategory


class Theory(BaseModel):
    """教育理論エンティティ。"""

    id: str = Field(..., description="理論の一意識別子")
    name: str = Field(..., description="理論名（日本語）")
    name_en: str = Field(..., description="理論名（英語）")
    description: str = Field(..., description="理論の説明")
    category: TheoryCategory = Field(..., description="理論のカテゴリ")
    year: int | None = Field(None, description="理論が提唱された年")
    evidence_level: EvidenceLevel = Field(
        default=EvidenceLevel.THEORETICAL,
        description="エビデンスレベル",
    )
    keywords: list[str] = Field(default_factory=list, description="キーワード")
    summary: str = Field(default="", description="簡潔な要約")
    created_at: datetime = Field(default_factory=datetime.now, description="作成日時")
    updated_at: datetime = Field(default_factory=datetime.now, description="更新日時")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "cognitive-load-theory",
                "name": "認知負荷理論",
                "name_en": "Cognitive Load Theory",
                "description": "ワーキングメモリの制限が学習に与える影響を説明する理論。",
                "category": "learning",
                "year": 1988,
                "evidence_level": "strong",
                "keywords": ["認知負荷", "ワーキングメモリ", "内的負荷", "外的負荷"],
                "summary": "学習者のワーキングメモリには限界があり、教材設計では認知負荷を適切に管理することが重要。",
            }
        }
    }


class TheorySummary(BaseModel):
    """理論の要約情報（一覧表示用）。"""

    id: str
    name: str
    name_en: str | None = None
    category: TheoryCategory
    year: int | None = None
    evidence_level: EvidenceLevel = EvidenceLevel.THEORETICAL
    summary: str = ""

    @classmethod
    def from_theory(cls, theory: Theory) -> "TheorySummary":
        """Theoryエンティティから要約を作成。"""
        return cls(
            id=theory.id,
            name=theory.name,
            name_en=theory.name_en,
            category=theory.category,
            year=theory.year,
            evidence_level=theory.evidence_level,
            summary=theory.summary,
        )
