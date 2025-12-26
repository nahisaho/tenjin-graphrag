"""Domain Entity: Theorist - 理論家（教育学者）."""

from pydantic import BaseModel, Field


class Theorist(BaseModel):
    """理論家（教育学者）エンティティ。"""

    id: str = Field(..., description="理論家の一意識別子")
    name: str = Field(..., description="氏名（日本語またはカタカナ）")
    name_en: str = Field(..., description="氏名（英語）")
    birth_year: int | None = Field(None, description="生年")
    death_year: int | None = Field(None, description="没年（存命の場合はNone）")
    nationality: str = Field(default="", description="国籍")
    affiliation: str = Field(default="", description="所属機関")
    biography: str = Field(default="", description="略歴")
    major_works: list[str] = Field(default_factory=list, description="主要著作")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "john-sweller",
                "name": "ジョン・スウェラー",
                "name_en": "John Sweller",
                "birth_year": 1946,
                "nationality": "オーストラリア",
                "affiliation": "ニューサウスウェールズ大学",
                "biography": "教育心理学者。認知負荷理論の提唱者として知られる。",
                "major_works": ["Cognitive Load Theory (2011)"],
            }
        }
    }


class TheoristSummary(BaseModel):
    """理論家の要約情報。"""

    id: str
    name: str
    name_en: str
    birth_year: int | None = None
    nationality: str = ""
