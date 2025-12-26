"""MCP Tools: Theory search and retrieval tools."""

from tengin_mcp.domain.errors import InvalidQueryError, TheoryNotFoundError
from tengin_mcp.domain.value_objects import TheoryCategory
from tengin_mcp.server import app_state, mcp


@mcp.tool()
async def search_theories(
    query: str,
    category: str | None = None,
    limit: int = 10,
) -> dict:
    """
    教育理論をキーワードで検索します。

    自然言語クエリに基づいて関連する教育理論を検索し、
    各理論の基本情報を返します。

    Args:
        query: 検索キーワード（理論名、概念、キーワードなど）
        category: 理論カテゴリでフィルタ（learning, instructional, developmental, motivation, edtech）
        limit: 返す結果の最大数（デフォルト: 10）

    Returns:
        検索結果の理論リスト
    """
    if not query or len(query.strip()) < 2:
        raise InvalidQueryError("検索クエリは2文字以上必要です")

    if not app_state.theory_repository:
        return {"error": "Theory repository not initialized", "theories": []}

    # カテゴリの変換
    cat = None
    if category:
        try:
            cat = TheoryCategory(category)
        except ValueError:
            valid_cats = [c.value for c in TheoryCategory]
            raise InvalidQueryError(f"無効なカテゴリ: {category}。有効な値: {valid_cats}") from None

    theories = await app_state.theory_repository.search_theories(
        query=query.strip(),
        category=cat,
        limit=limit,
    )

    return {
        "query": query,
        "category": category,
        "count": len(theories),
        "theories": [
            {
                "id": t.id,
                "name": t.name,
                "name_en": t.name_en,
                "category": t.category.value,
            }
            for t in theories
        ],
    }


@mcp.tool()
async def get_theory(theory_id: str) -> dict:
    """
    指定IDの教育理論の詳細情報を取得します。

    理論の説明、提唱者、関連概念、原則、エビデンスなど
    包括的な情報を返します。

    Args:
        theory_id: 取得する理論のID

    Returns:
        理論の詳細情報
    """
    if not theory_id:
        raise InvalidQueryError("theory_idは必須です")

    if not app_state.theory_repository:
        return {"error": "Theory repository not initialized"}

    try:
        theory = await app_state.theory_repository.get_theory_by_id(theory_id)
    except TheoryNotFoundError:
        return {"error": f"理論が見つかりません: {theory_id}"}

    return {
        "id": theory.id,
        "name": theory.name,
        "name_en": theory.name_en,
        "description": theory.description,
        "category": theory.category.value,
        "year": theory.year,
        "evidence_level": theory.evidence_level.value,
        "keywords": theory.keywords,
        "summary": theory.summary,
    }


@mcp.tool()
async def get_theories_by_category(
    category: str,
    limit: int = 10,
) -> dict:
    """
    カテゴリ別に教育理論を取得します。

    Args:
        category: 理論カテゴリ（learning, instructional, developmental, motivation, edtech）
        limit: 返す結果の最大数（デフォルト: 10）

    Returns:
        指定カテゴリの理論リスト
    """
    if not app_state.theory_repository:
        return {"error": "Theory repository not initialized", "theories": []}

    try:
        cat = TheoryCategory(category)
    except ValueError:
        valid_cats = [c.value for c in TheoryCategory]
        raise InvalidQueryError(f"無効なカテゴリ: {category}。有効な値: {valid_cats}") from None

    theories = await app_state.theory_repository.get_theories_by_category(
        category=cat,
        limit=limit,
    )

    return {
        "category": category,
        "count": len(theories),
        "theories": [
            {
                "id": t.id,
                "name": t.name,
                "name_en": t.name_en,
                "category": t.category.value,
            }
            for t in theories
        ],
    }


@mcp.tool()
async def get_theorist(theorist_id: str) -> dict:
    """
    指定IDの理論家の詳細情報を取得します。

    Args:
        theorist_id: 取得する理論家のID

    Returns:
        理論家の詳細情報
    """
    if not theorist_id:
        raise InvalidQueryError("theorist_idは必須です")

    if not app_state.theory_repository:
        return {"error": "Theory repository not initialized"}

    try:
        theorist = await app_state.theory_repository.get_theorist_by_id(theorist_id)
    except TheoryNotFoundError:
        return {"error": f"理論家が見つかりません: {theorist_id}"}

    return {
        "id": theorist.id,
        "name": theorist.name,
        "name_en": theorist.name_en,
        "birth_year": theorist.birth_year,
        "death_year": theorist.death_year,
        "nationality": theorist.nationality,
        "affiliation": theorist.affiliation,
        "biography": theorist.biography,
        "major_works": theorist.major_works,
    }


@mcp.tool()
async def get_concept(concept_id: str) -> dict:
    """
    指定IDの概念の詳細情報を取得します。

    Args:
        concept_id: 取得する概念のID

    Returns:
        概念の詳細情報
    """
    if not concept_id:
        raise InvalidQueryError("concept_idは必須です")

    if not app_state.theory_repository:
        return {"error": "Theory repository not initialized"}

    try:
        concept = await app_state.theory_repository.get_concept_by_id(concept_id)
    except TheoryNotFoundError:
        return {"error": f"概念が見つかりません: {concept_id}"}

    return {
        "id": concept.id,
        "name": concept.name,
        "name_en": concept.name_en,
        "definition": concept.definition,
        "examples": concept.examples,
        "related_theory_ids": concept.related_theory_ids,
    }


@mcp.tool()
async def get_principle(principle_id: str) -> dict:
    """
    指定IDの原則の詳細情報を取得します。

    Args:
        principle_id: 取得する原則のID

    Returns:
        原則の詳細情報
    """
    if not principle_id:
        raise InvalidQueryError("principle_idは必須です")

    if not app_state.theory_repository:
        return {"error": "Theory repository not initialized"}

    try:
        principle = await app_state.theory_repository.get_principle_by_id(principle_id)
    except TheoryNotFoundError:
        return {"error": f"原則が見つかりません: {principle_id}"}

    return {
        "id": principle.id,
        "name": principle.name,
        "description": principle.description,
        "application_guide": principle.application_guide,
        "examples": principle.examples,
        "source_theory_id": principle.source_theory_id,
    }


@mcp.tool()
async def get_evidence(evidence_id: str) -> dict:
    """
    指定IDのエビデンスの詳細情報を取得します。

    Args:
        evidence_id: 取得するエビデンスのID

    Returns:
        エビデンスの詳細情報
    """
    if not evidence_id:
        raise InvalidQueryError("evidence_idは必須です")

    if not app_state.theory_repository:
        return {"error": "Theory repository not initialized"}

    try:
        evidence = await app_state.theory_repository.get_evidence_by_id(evidence_id)
    except TheoryNotFoundError:
        return {"error": f"エビデンスが見つかりません: {evidence_id}"}

    return {
        "id": evidence.id,
        "title": evidence.title,
        "authors": evidence.authors,
        "year": evidence.year,
        "evidence_type": evidence.evidence_type,
        "sample_size": evidence.sample_size,
        "findings": evidence.findings,
        "methodology": evidence.methodology,
        "doi": evidence.doi,
        "supported_theory_ids": evidence.supported_theory_ids,
    }
