"""Domain Entity: Evidence - エビデンス（研究成果）."""

from pydantic import BaseModel, Field


class EvidenceType(str):
    """エビデンスの種類。"""

    META_ANALYSIS = "meta-analysis"
    """メタ分析"""

    RCT = "rct"
    """ランダム化比較試験"""

    QUASI_EXPERIMENTAL = "quasi-experimental"
    """準実験"""

    QUALITATIVE = "qualitative"
    """質的研究"""

    REVIEW = "review"
    """レビュー論文"""


class Evidence(BaseModel):
    """研究エビデンスエンティティ。"""

    id: str = Field(..., description="エビデンスの一意識別子")
    title: str = Field(..., description="研究タイトル")
    authors: list[str] = Field(..., description="著者リスト")
    year: int = Field(..., description="発表年")
    source: str = Field(default="", description="出典（ジャーナル名等）")
    doi: str | None = Field(None, description="DOI")
    evidence_type: str = Field(default="review", description="エビデンスの種類")
    methodology: str = Field(default="", description="研究方法")
    findings: str = Field(..., description="主な発見・結果")
    sample_size: int | None = Field(None, description="サンプルサイズ")
    effect_size: str | None = Field(None, description="効果量")
    supported_theory_ids: list[str] = Field(
        default_factory=list, description="この研究がサポートする理論のID"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "sweller-1988-clt",
                "title": "Cognitive Load During Problem Solving: Effects on Learning",
                "authors": ["John Sweller"],
                "year": 1988,
                "source": "Cognitive Science",
                "doi": "10.1207/s15516709cog1202_4",
                "evidence_type": "quasi-experimental",
                "methodology": "複数の実験を通じて、問題解決時の認知負荷が学習に与える影響を検証",
                "findings": "目標なし問題は従来の問題よりも効果的にスキーマ獲得を促進する",
                "supported_theory_ids": ["cognitive-load-theory"],
            }
        }
    }


class EvidenceSummary(BaseModel):
    """エビデンスの要約情報。"""

    id: str
    title: str
    authors: list[str]
    year: int
    evidence_type: str
    findings: str
