"""MCP Tools: Graph traversal and analysis tools."""

from tengin_mcp.domain.errors import InvalidQueryError
from tengin_mcp.server import app_state, mcp


@mcp.tool()
async def traverse_graph(
    start_node_id: str,
    relationship_types: list[str] | None = None,
    max_depth: int = 3,
    direction: str = "both",
) -> dict:
    """
    知識グラフをトラバースして関連ノードを取得します。

    指定したノードから始めて、関連するノードとリレーションシップを
    グラフ構造として返します。

    Args:
        start_node_id: 開始ノードのID
        relationship_types: フィルタするリレーションシップタイプ（オプション）
        max_depth: 最大トラバース深度（デフォルト: 3）
        direction: トラバース方向（outgoing, incoming, both）

    Returns:
        ノードとリレーションシップを含むグラフ構造
    """
    if not start_node_id:
        raise InvalidQueryError("start_node_idは必須です")

    if max_depth < 1 or max_depth > 10:
        raise InvalidQueryError("max_depthは1〜10の範囲で指定してください")

    if direction not in ["outgoing", "incoming", "both"]:
        raise InvalidQueryError("directionはoutgoing, incoming, bothのいずれかを指定してください")

    if not app_state.graph_repository:
        return {"error": "Graph repository not initialized", "nodes": [], "relationships": []}

    result = await app_state.graph_repository.traverse_extended(
        start_node_id=start_node_id,
        relationship_types=relationship_types,
        max_depth=max_depth,
        direction=direction,
    )

    return {
        "start_node_id": start_node_id,
        "max_depth": max_depth,
        "direction": direction,
        "node_count": len(result.get("nodes", [])),
        "relationship_count": len(result.get("relationships", [])),
        "nodes": result.get("nodes", []),
        "relationships": result.get("relationships", []),
    }


@mcp.tool()
async def find_path(
    start_node_id: str,
    end_node_id: str,
    max_depth: int = 5,
) -> dict:
    """
    2つのノード間の最短パスを検索します。

    理論間、概念間、または異なるタイプのノード間の
    関係性を探索します。

    Args:
        start_node_id: 開始ノードのID
        end_node_id: 終了ノードのID
        max_depth: 最大パス長（デフォルト: 5）

    Returns:
        パス情報（ノードとリレーションシップのシーケンス）
    """
    if not start_node_id or not end_node_id:
        raise InvalidQueryError("start_node_idとend_node_idは必須です")

    if start_node_id == end_node_id:
        raise InvalidQueryError("開始ノードと終了ノードは異なる必要があります")

    if max_depth < 1 or max_depth > 10:
        raise InvalidQueryError("max_depthは1〜10の範囲で指定してください")

    if not app_state.graph_repository:
        return {"error": "Graph repository not initialized", "paths": []}

    paths = await app_state.graph_repository.find_path(
        start_node_id=start_node_id,
        end_node_id=end_node_id,
        max_depth=max_depth,
    )

    return {
        "start_node_id": start_node_id,
        "end_node_id": end_node_id,
        "path_found": len(paths) > 0,
        "paths": paths,
    }


@mcp.tool()
async def get_related_nodes(
    node_id: str,
    relationship_type: str | None = None,
    node_type: str | None = None,
) -> dict:
    """
    指定ノードに関連するノードを取得します。

    Args:
        node_id: 対象ノードのID
        relationship_type: フィルタするリレーションシップタイプ（オプション）
        node_type: フィルタするノードタイプ（Theory, Concept, Theorist等）（オプション）

    Returns:
        関連ノードのリスト
    """
    if not node_id:
        raise InvalidQueryError("node_idは必須です")

    if not app_state.graph_repository:
        return {"error": "Graph repository not initialized", "related_nodes": []}

    related = await app_state.graph_repository.get_related_nodes(
        node_id=node_id,
        relationship_type=relationship_type,
        node_type=node_type,
    )

    return {
        "node_id": node_id,
        "relationship_type": relationship_type,
        "node_type": node_type,
        "count": len(related),
        "related_nodes": related,
    }


@mcp.tool()
async def get_graph_statistics() -> dict:
    """
    知識グラフの統計情報を取得します。

    ノード数、リレーションシップ数、各タイプの分布など
    グラフ全体の概要を返します。

    Returns:
        グラフ統計情報
    """
    if not app_state.graph_repository:
        return {"error": "Graph repository not initialized"}

    stats = await app_state.graph_repository.get_statistics()

    return {
        "node_counts": stats.get("node_counts", []),
        "relationship_counts": stats.get("relationship_counts", []),
    }
