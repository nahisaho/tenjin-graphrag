"""MCP Tools: Citation generation tools."""

from tengin_mcp.domain.errors import InvalidQueryError, TheoryNotFoundError
from tengin_mcp.domain.value_objects import CitationFormat
from tengin_mcp.server import app_state, mcp


def _generate_apa7_citation(theory: dict, theorist: dict | None) -> str:
    """APA7形式の引用を生成。"""
    author = theorist["name"] if theorist else "Unknown"
    year = theory.get("year_introduced", "n.d.")
    title = theory["name"]

    return f"{author} ({year}). {title}."


def _generate_mla9_citation(theory: dict, theorist: dict | None) -> str:
    """MLA9形式の引用を生成。"""
    author = theorist["name"] if theorist else "Unknown"
    title = theory["name"]
    year = theory.get("year_introduced", "n.d.")

    return f'{author}. "{title}." {year}.'


def _generate_chicago_citation(theory: dict, theorist: dict | None) -> str:
    """Chicago形式の引用を生成。"""
    author = theorist["name"] if theorist else "Unknown"
    title = theory["name"]
    year = theory.get("year_introduced", "n.d.")

    return f'{author}. "{title}," {year}.'


def _generate_harvard_citation(theory: dict, theorist: dict | None) -> str:
    """Harvard形式の引用を生成。"""
    author = theorist["name"] if theorist else "Unknown"
    year = theory.get("year_introduced", "n.d.")
    title = theory["name"]

    return f"{author} ({year}) {title}."


def _generate_ieee_citation(theory: dict, theorist: dict | None) -> str:
    """IEEE形式の引用を生成。"""
    author = theorist["name"] if theorist else "Unknown"
    title = theory["name"]
    year = theory.get("year_introduced", "n.d.")

    return f'{author}, "{title}," {year}.'


@mcp.tool()
async def cite_theory(
    theory_id: str,
    format: str = "APA7",
) -> dict:
    """
    教育理論の学術引用を生成します。

    指定した形式（APA7, MLA9, Chicago, Harvard, IEEE）で
    理論を引用するためのテキストを生成します。

    Args:
        theory_id: 引用する理論のID
        format: 引用形式（APA7, MLA9, Chicago, Harvard, IEEE）

    Returns:
        生成された引用テキスト
    """
    if not theory_id:
        raise InvalidQueryError("theory_idは必須です")

    # フォーマットの検証
    try:
        citation_format = CitationFormat(format)
    except ValueError:
        valid_formats = [f.value for f in CitationFormat]
        raise InvalidQueryError(f"無効な引用形式: {format}。有効な値: {valid_formats}") from None

    if not app_state.theory_repository:
        return {"error": "Theory repository not initialized"}

    # 理論を取得
    try:
        theory = await app_state.theory_repository.get_theory_by_id(theory_id)
    except TheoryNotFoundError:
        return {"error": f"理論が見つかりません: {theory_id}"}

    theory_dict = {
        "name": theory.name,
        "year_introduced": theory.year,
    }

    # 理論家を取得（オプション）
    theorist_dict = None
    # Note: 将来的には理論と理論家の関連を取得

    # 引用を生成
    citation_generators = {
        CitationFormat.APA7: _generate_apa7_citation,
        CitationFormat.MLA9: _generate_mla9_citation,
        CitationFormat.CHICAGO: _generate_chicago_citation,
        CitationFormat.HARVARD: _generate_harvard_citation,
        CitationFormat.IEEE: _generate_ieee_citation,
    }

    generator = citation_generators[citation_format]
    citation = generator(theory_dict, theorist_dict)

    return {
        "theory_id": theory_id,
        "theory_name": theory.name,
        "format": format,
        "citation": citation,
    }


@mcp.tool()
async def compare_theories(
    theory_ids: list[str],
) -> dict:
    """
    複数の教育理論を比較します。

    指定した理論の共通点、相違点、適用場面などを
    比較分析します。

    Args:
        theory_ids: 比較する理論のIDリスト（2〜5個）

    Returns:
        理論の比較結果
    """
    if not theory_ids or len(theory_ids) < 2:
        raise InvalidQueryError("比較には少なくとも2つの理論IDが必要です")

    if len(theory_ids) > 5:
        raise InvalidQueryError("一度に比較できる理論は5つまでです")

    if not app_state.theory_repository:
        return {"error": "Theory repository not initialized", "theories": []}

    theories = []
    for tid in theory_ids:
        try:
            theory = await app_state.theory_repository.get_theory_by_id(tid)
            theories.append(
                {
                    "id": theory.id,
                    "name": theory.name,
                    "name_en": theory.name_en,
                    "description": theory.description,
                    "category": theory.category.value,
                    "year": theory.year,
                    "keywords": theory.keywords,
                    "evidence_level": theory.evidence_level.value,
                }
            )
        except TheoryNotFoundError:
            theories.append({"id": tid, "error": "Not found"})

    # カテゴリの分析
    categories = [t.get("category") for t in theories if t.get("category")]
    same_category = len(set(categories)) == 1 if categories else False

    # キーワードの共通性
    all_keywords = [set(t.get("keywords", [])) for t in theories if t.get("keywords")]
    common_keywords = (
        list(set.intersection(*all_keywords)) if all_keywords and len(all_keywords) > 1 else []
    )

    return {
        "theory_count": len(theories),
        "theories": theories,
        "analysis": {
            "same_category": same_category,
            "categories": list(set(categories)),
            "common_keywords": common_keywords,
        },
    }
