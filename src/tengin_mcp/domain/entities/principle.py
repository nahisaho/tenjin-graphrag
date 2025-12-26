"""Domain Entity: Principle - 原理・原則."""

from pydantic import BaseModel, Field


class Principle(BaseModel):
    """教育理論から導出される原理・原則エンティティ。"""

    id: str = Field(..., description="原則の一意識別子")
    name: str = Field(..., description="原則名")
    description: str = Field(..., description="原則の説明")
    application_guide: str = Field(default="", description="適用ガイド")
    examples: list[str] = Field(default_factory=list, description="具体的な適用例")
    source_theory_id: str = Field(..., description="この原則の元となる理論のID")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "split-attention-effect",
                "name": "分割注意効果",
                "description": "複数の情報源を統合する必要がある場合、それらを物理的に統合して提示することで学習効果が向上する。",
                "application_guide": "図と説明文は近接して配置し、学習者が視線を大きく動かす必要がないようにする。",
                "examples": [
                    "図の中に直接ラベルを入れる（別の凡例を参照させない）",
                    "数学の問題と解法を同じ画面に表示する",
                ],
                "source_theory_id": "cognitive-load-theory",
            }
        }
    }


class PrincipleSummary(BaseModel):
    """原則の要約情報。"""

    id: str
    name: str
    description: str
    source_theory_id: str
