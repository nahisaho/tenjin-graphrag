"""MCP Tools: 教授法・文脈に関するツール"""

from tengin_mcp.domain.errors import EntityNotFoundError, InvalidQueryError
from tengin_mcp.server import app_state, mcp


@mcp.tool()
async def search_methodologies(
    query: str | None = None,
    category: str | None = None,
    evidence_level: str | None = None,
    theory_id: str | None = None,
    limit: int = 10,
) -> dict:
    """
    教授法を検索します。

    キーワード、カテゴリ、エビデンスレベル、理論的基盤で
    教授法を検索できます。

    Args:
        query: 検索キーワード（オプション）
        category: カテゴリでフィルタ（direct-instruction, cooperative, discovery,
                  experiential, project-based, adaptive, formative等）
        evidence_level: エビデンスレベルでフィルタ（high, moderate, emerging等）
        theory_id: 理論的基盤の理論IDでフィルタ（オプション）
        limit: 最大結果数（デフォルト: 10）

    Returns:
        マッチした教授法のリスト
    """
    if not app_state.graph_repository:
        return {"error": "Graph repository not initialized", "methodologies": []}

    # Neo4jで教授法を検索
    filters: list[str] = []
    params: dict[str, str | int] = {"limit": limit}

    if query:
        filters.append(
            "(m.name CONTAINS $query OR m.name_en CONTAINS $query OR m.description CONTAINS $query)"
        )
        params["query"] = query

    if category:
        filters.append("m.category = $category")
        params["category"] = category

    if evidence_level:
        filters.append("m.evidence_level = $evidence_level")
        params["evidence_level"] = evidence_level

    where_clause = " AND ".join(filters) if filters else "true"

    if theory_id:
        cypher = f"""
        MATCH (m:Methodology)-[:THEORETICALLY_GROUNDED_IN]->(t:Theory {{id: $theory_id}})
        WHERE {where_clause}
        RETURN m.id as id, m.name as name, m.name_en as name_en,
               m.category as category, m.description as description,
               m.evidence_level as evidence_level, m.effect_size as effect_size
        LIMIT $limit
        """
        params["theory_id"] = theory_id
    else:
        cypher = f"""
        MATCH (m:Methodology)
        WHERE {where_clause}
        RETURN m.id as id, m.name as name, m.name_en as name_en,
               m.category as category, m.description as description,
               m.evidence_level as evidence_level, m.effect_size as effect_size
        LIMIT $limit
        """

    result = await app_state.graph_repository.execute_cypher(cypher, params)
    methodologies = [dict(record) for record in result]

    return {
        "query": query,
        "category": category,
        "evidence_level": evidence_level,
        "theory_id": theory_id,
        "count": len(methodologies),
        "methodologies": methodologies,
    }


@mcp.tool()
async def get_methodology(methodology_id: str) -> dict:
    """
    指定した教授法の詳細情報を取得します。

    教授法のプロシージャ、理論的基盤、エビデンスレベル、
    効果量、適用場面などの詳細情報を返します。

    Args:
        methodology_id: 教授法のID（例: "scaffolding", "think-pair-share"）

    Returns:
        教授法の詳細情報（関連する理論・文脈を含む）
    """
    if not methodology_id:
        raise InvalidQueryError("methodology_idは必須です")

    if not app_state.graph_repository:
        return {"error": "Graph repository not initialized"}

    # 教授法の詳細を取得
    cypher = """
    MATCH (m:Methodology {id: $id})
    OPTIONAL MATCH (m)-[:THEORETICALLY_GROUNDED_IN]->(t:Theory)
    OPTIONAL MATCH (m)-[:APPLICABLE_IN]->(c:Context)
    RETURN m, collect(distinct t.id) as grounded_theories, collect(distinct c.id) as applicable_contexts
    """
    result = await app_state.graph_repository.execute_cypher(cypher, {"id": methodology_id})

    if not result:
        raise EntityNotFoundError("Methodology", methodology_id)

    record = result[0]
    methodology_data = dict(record["m"])
    methodology_data["grounded_theories"] = record["grounded_theories"]
    methodology_data["applicable_contexts"] = record["applicable_contexts"]

    return methodology_data


@mcp.tool()
async def search_contexts(
    education_level: str | None = None,
    subject_area: str | None = None,
    effective_for_theory: str | None = None,
    limit: int = 10,
) -> dict:
    """
    教育文脈を検索します。

    教育段階、科目領域、有効な理論でフィルタできます。

    Args:
        education_level: 教育段階でフィルタ（k12, higher-education,
                        professional, corporate等）
        subject_area: 科目領域でフィルタ（general, stem, humanities,
                     language, skill-based等）
        effective_for_theory: この理論が有効な文脈を検索（theory ID）
        limit: 最大結果数（デフォルト: 10）

    Returns:
        マッチした教育文脈のリスト
    """
    if not app_state.graph_repository:
        return {"error": "Graph repository not initialized", "contexts": []}

    filters: list[str] = []
    params: dict[str, str | int] = {"limit": limit}

    if education_level:
        filters.append("c.education_level = $education_level")
        params["education_level"] = education_level

    if subject_area:
        filters.append("c.subject_area = $subject_area")
        params["subject_area"] = subject_area

    where_clause = " AND ".join(filters) if filters else "true"

    if effective_for_theory:
        cypher = f"""
        MATCH (t:Theory {{id: $theory_id}})-[:EFFECTIVE_FOR]->(c:Context)
        WHERE {where_clause}
        RETURN c.id as id, c.name as name, c.name_en as name_en,
               c.education_level as education_level, c.subject_area as subject_area,
               c.description as description
        LIMIT $limit
        """
        params["theory_id"] = effective_for_theory
    else:
        cypher = f"""
        MATCH (c:Context)
        WHERE {where_clause}
        RETURN c.id as id, c.name as name, c.name_en as name_en,
               c.education_level as education_level, c.subject_area as subject_area,
               c.description as description
        LIMIT $limit
        """

    result = await app_state.graph_repository.execute_cypher(cypher, params)
    contexts = [dict(record) for record in result]

    return {
        "education_level": education_level,
        "subject_area": subject_area,
        "effective_for_theory": effective_for_theory,
        "count": len(contexts),
        "contexts": contexts,
    }


@mcp.tool()
async def get_context(context_id: str) -> dict:
    """
    指定した教育文脈の詳細情報を取得します。

    文脈の特性、有効な理論・教授法、課題などの詳細を返します。

    Args:
        context_id: 文脈のID（例: "higher-education", "k12-stem"）

    Returns:
        文脈の詳細情報（有効な理論・教授法を含む）
    """
    if not context_id:
        raise InvalidQueryError("context_idは必須です")

    if not app_state.graph_repository:
        return {"error": "Graph repository not initialized"}

    # 文脈の詳細を取得
    cypher = """
    MATCH (c:Context {id: $id})
    OPTIONAL MATCH (t:Theory)-[:EFFECTIVE_FOR]->(c)
    OPTIONAL MATCH (m:Methodology)-[:APPLICABLE_IN]->(c)
    RETURN c, collect(distinct {id: t.id, name: t.name}) as effective_theories,
           collect(distinct {id: m.id, name: m.name}) as applicable_methodologies
    """
    result = await app_state.graph_repository.execute_cypher(cypher, {"id": context_id})

    if not result:
        raise EntityNotFoundError("Context", context_id)

    record = result[0]
    context_data = dict(record["c"])
    context_data["effective_theories_detail"] = [
        t for t in record["effective_theories"] if t["id"] is not None
    ]
    context_data["applicable_methodologies_detail"] = [
        m for m in record["applicable_methodologies"] if m["id"] is not None
    ]

    return context_data


@mcp.tool()
async def recommend_methodologies(
    context_id: str | None = None,
    theory_id: str | None = None,
    min_evidence_level: str = "moderate",
) -> dict:
    """
    指定した文脈や理論に基づいて教授法を推薦します。

    エビデンスレベル、効果量、適合性を考慮して
    最適な教授法を推薦します。

    Args:
        context_id: 文脈ID（オプション、教育環境で絞り込み）
        theory_id: 理論ID（オプション、この理論に基づく教授法）
        min_evidence_level: 最低エビデンスレベル（high, moderate, emerging）

    Returns:
        推薦される教授法のリスト（スコア付き）
    """
    if not app_state.graph_repository:
        return {"error": "Graph repository not initialized", "recommendations": []}

    evidence_order = {"high": 3, "moderate": 2, "emerging": 1}
    min_level = evidence_order.get(min_evidence_level, 2)

    if context_id and theory_id:
        cypher = """
        MATCH (m:Methodology)-[:APPLICABLE_IN]->(c:Context {id: $context_id})
        MATCH (m)-[:THEORETICALLY_GROUNDED_IN]->(t:Theory {id: $theory_id})
        RETURN m.id as id, m.name as name, m.name_en as name_en,
               m.evidence_level as evidence_level, m.effect_size as effect_size,
               m.description as description, m.best_for as best_for
        """
        params = {"context_id": context_id, "theory_id": theory_id}
    elif context_id:
        cypher = """
        MATCH (m:Methodology)-[:APPLICABLE_IN]->(c:Context {id: $context_id})
        RETURN m.id as id, m.name as name, m.name_en as name_en,
               m.evidence_level as evidence_level, m.effect_size as effect_size,
               m.description as description, m.best_for as best_for
        """
        params = {"context_id": context_id}
    elif theory_id:
        cypher = """
        MATCH (m:Methodology)-[:THEORETICALLY_GROUNDED_IN]->(t:Theory {id: $theory_id})
        RETURN m.id as id, m.name as name, m.name_en as name_en,
               m.evidence_level as evidence_level, m.effect_size as effect_size,
               m.description as description, m.best_for as best_for
        """
        params = {"theory_id": theory_id}
    else:
        cypher = """
        MATCH (m:Methodology)
        RETURN m.id as id, m.name as name, m.name_en as name_en,
               m.evidence_level as evidence_level, m.effect_size as effect_size,
               m.description as description, m.best_for as best_for
        """
        params = {}

    result = await app_state.graph_repository.execute_cypher(cypher, params)

    # フィルタリングとスコアリング
    recommendations = []
    for record in result:
        rec = dict(record)
        level = rec.get("evidence_level", "emerging")
        if evidence_order.get(level, 0) >= min_level:
            # スコア計算: エビデンスレベル + 効果量
            score = evidence_order.get(level, 0) * 10
            if rec.get("effect_size"):
                score += rec["effect_size"] * 20
            rec["recommendation_score"] = round(score, 2)
            recommendations.append(rec)

    # スコアでソート
    recommendations.sort(key=lambda x: x.get("recommendation_score", 0), reverse=True)

    return {
        "context_id": context_id,
        "theory_id": theory_id,
        "min_evidence_level": min_evidence_level,
        "count": len(recommendations),
        "recommendations": recommendations,
    }


@mcp.tool()
async def get_evidence_for_theory(
    theory_id: str,
    include_challenges: bool = True,
) -> dict:
    """
    指定した理論を支持または挑戦するエビデンスを取得します。

    メタ分析、実証研究、効果量などのエビデンス情報を返します。

    Args:
        theory_id: 理論のID
        include_challenges: 挑戦するエビデンスも含めるか（デフォルト: True）

    Returns:
        支持・挑戦するエビデンスのリスト
    """
    if not theory_id:
        raise InvalidQueryError("theory_idは必須です")

    if not app_state.graph_repository:
        return {"error": "Graph repository not initialized"}

    # 支持するエビデンス
    supports_cypher = """
    MATCH (e:Evidence)-[:SUPPORTS]->(t:Theory {id: $theory_id})
    RETURN e.id as id, e.name as name, e.type as type, e.year as year,
           e.title as title, e.findings as findings, e.effect_size as effect_size,
           e.sample_size as sample_size, e.evidence_quality as evidence_quality,
           'supports' as relation_type
    """

    supports_result = await app_state.graph_repository.execute_cypher(
        supports_cypher, {"theory_id": theory_id}
    )
    supports = [dict(record) for record in supports_result]

    challenges = []
    if include_challenges:
        challenges_cypher = """
        MATCH (e:Evidence)-[:CHALLENGES]->(t:Theory {id: $theory_id})
        RETURN e.id as id, e.name as name, e.type as type, e.year as year,
               e.title as title, e.findings as findings, e.effect_size as effect_size,
               e.sample_size as sample_size, e.evidence_quality as evidence_quality,
               'challenges' as relation_type
        """
        challenges_result = await app_state.graph_repository.execute_cypher(
            challenges_cypher, {"theory_id": theory_id}
        )
        challenges = [dict(record) for record in challenges_result]

    return {
        "theory_id": theory_id,
        "supporting_evidence": supports,
        "challenging_evidence": challenges,
        "total_supports": len(supports),
        "total_challenges": len(challenges),
    }
