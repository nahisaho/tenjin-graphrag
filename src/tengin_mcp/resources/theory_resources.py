"""MCP Resources: Theory and graph resource handlers."""

from tengin_mcp.domain.errors import TheoryNotFoundError
from tengin_mcp.server import app_state, mcp


@mcp.resource("theory://{theory_id}")
async def get_theory_resource(theory_id: str) -> str:
    """
    教育理論リソースを取得します。

    Args:
        theory_id: 理論のID

    Returns:
        理論の詳細情報（テキスト形式）
    """
    if not app_state.theory_repository:
        return "Error: Theory repository not initialized"

    try:
        theory = await app_state.theory_repository.get_theory_by_id(theory_id)
    except TheoryNotFoundError:
        return f"Error: Theory not found: {theory_id}"

    lines = [
        f"# {theory.name}",
        f"({theory.name_en})" if theory.name_en else "",
        "",
        f"**Category:** {theory.category.value}",
        f"**Year:** {theory.year or 'Unknown'}",
        "",
        "## Description",
        theory.description,
        "",
    ]

    if theory.keywords:
        lines.extend(
            [
                "## Keywords",
                ", ".join(theory.keywords),
                "",
            ]
        )

    return "\n".join(lines)


@mcp.resource("concept://{concept_id}")
async def get_concept_resource(concept_id: str) -> str:
    """
    概念リソースを取得します。

    Args:
        concept_id: 概念のID

    Returns:
        概念の詳細情報（テキスト形式）
    """
    if not app_state.theory_repository:
        return "Error: Theory repository not initialized"

    try:
        concept = await app_state.theory_repository.get_concept_by_id(concept_id)
    except TheoryNotFoundError:
        return f"Error: Concept not found: {concept_id}"

    lines = [
        f"# {concept.name}",
        f"({concept.name_en})" if concept.name_en else "",
        "",
        "## Definition",
        concept.definition,
        "",
    ]

    return "\n".join(lines)


@mcp.resource("theorist://{theorist_id}")
async def get_theorist_resource(theorist_id: str) -> str:
    """
    理論家リソースを取得します。

    Args:
        theorist_id: 理論家のID

    Returns:
        理論家の詳細情報（テキスト形式）
    """
    if not app_state.theory_repository:
        return "Error: Theory repository not initialized"

    try:
        theorist = await app_state.theory_repository.get_theorist_by_id(theorist_id)
    except TheoryNotFoundError:
        return f"Error: Theorist not found: {theorist_id}"

    lines = [
        f"# {theorist.name}",
        f"({theorist.name_en})" if theorist.name_en else "",
        "",
    ]

    if theorist.birth_year or theorist.death_year:
        birth = theorist.birth_year or "?"
        death = theorist.death_year or "present"
        lines.extend(
            [
                f"**Lifespan:** {birth} - {death}",
                "",
            ]
        )

    if theorist.nationality:
        lines.extend(
            [
                f"**Nationality:** {theorist.nationality}",
                "",
            ]
        )

    if theorist.biography:
        lines.extend(
            [
                "## Biography",
                theorist.biography,
                "",
            ]
        )

    return "\n".join(lines)


@mcp.resource("evidence://{evidence_id}")
async def get_evidence_resource(evidence_id: str) -> str:
    """
    エビデンスリソースを取得します。

    Args:
        evidence_id: エビデンスのID

    Returns:
        エビデンスの詳細情報（テキスト形式）
    """
    if not app_state.theory_repository:
        return "Error: Theory repository not initialized"

    try:
        evidence = await app_state.theory_repository.get_evidence_by_id(evidence_id)
    except TheoryNotFoundError:
        return f"Error: Evidence not found: {evidence_id}"

    lines = [
        f"# {evidence.title}",
        "",
    ]

    if evidence.authors:
        lines.extend(
            [
                f"**Authors:** {', '.join(evidence.authors)}",
            ]
        )

    if evidence.year:
        lines.append(f"**Year:** {evidence.year}")

    if evidence.evidence_type:
        lines.append(f"**Evidence Type:** {evidence.evidence_type}")

    lines.append("")

    if evidence.methodology:
        lines.append(f"**Methodology:** {evidence.methodology}")

    if evidence.sample_size:
        lines.append(f"**Sample Size:** {evidence.sample_size}")

    lines.extend(
        [
            "",
            "## Findings",
            evidence.findings,
            "",
        ]
    )

    if evidence.doi:
        lines.extend(
            [
                f"**DOI:** {evidence.doi}",
                "",
            ]
        )

    return "\n".join(lines)


@mcp.resource("graph://statistics")
async def get_graph_statistics_resource() -> str:
    """
    グラフ統計リソースを取得します。

    Returns:
        グラフ統計情報（テキスト形式）
    """
    if not app_state.graph_repository:
        return "Error: Graph repository not initialized"

    stats = await app_state.graph_repository.get_statistics()

    lines = [
        "# Knowledge Graph Statistics",
        "",
        "## Node Counts",
    ]

    for node_stat in stats.get("node_counts", []):
        lines.append(f"- {node_stat.get('label', 'Unknown')}: {node_stat.get('count', 0)}")

    lines.extend(
        [
            "",
            "## Relationship Counts",
        ]
    )

    for rel_stat in stats.get("relationship_counts", []):
        lines.append(f"- {rel_stat.get('type', 'Unknown')}: {rel_stat.get('count', 0)}")

    return "\n".join(lines)
