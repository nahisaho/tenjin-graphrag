"""Domain Entity: Concept - 概念."""

from pydantic import BaseModel, Field


class Concept(BaseModel):
    """教育理論における概念エンティティ。"""

    id: str = Field(..., description="概念の一意識別子")
    name: str = Field(..., description="概念名（日本語）")
    name_en: str = Field(..., description="概念名（英語）")
    definition: str = Field(..., description="概念の定義")
    examples: list[str] = Field(default_factory=list, description="具体例")
    related_theory_ids: list[str] = Field(default_factory=list, description="関連する理論のID")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "intrinsic-load",
                "name": "内的負荷",
                "name_en": "Intrinsic Load",
                "definition": "学習内容そのものの複雑さに起因する認知負荷。要素間の相互作用の多さによって決まる。",
                "examples": [
                    "外国語の文法規則を学ぶ際の負荷",
                    "物理学の複数の概念を同時に理解する負荷",
                ],
                "related_theory_ids": ["cognitive-load-theory"],
            }
        }
    }


class ConceptSummary(BaseModel):
    """概念の要約情報。"""

    id: str
    name: str
    name_en: str
    definition: str
