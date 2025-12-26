"""Infrastructure: Neo4j Graph Repository."""

from typing import Any

from tengin_mcp.infrastructure.adapters.neo4j_adapter import Neo4jAdapter


class Neo4jGraphRepository:
    """Neo4j を使用した GraphRepository 実装。"""

    def __init__(self, adapter: Neo4jAdapter) -> None:
        """
        リポジトリを初期化。

        Args:
            adapter: Neo4j アダプター
        """
        self._adapter = adapter

    async def execute_cypher(self, query: str, params: dict | None = None) -> list[dict]:
        """
        Cypherクエリを直接実行。

        Args:
            query: Cypherクエリ文字列
            params: クエリパラメータ

        Returns:
            結果のリスト
        """
        return await self._adapter.execute_query(query, params or {})

    # --- Interface methods (GraphRepository Protocol) ---

    async def traverse(
        self,
        start_theory_id: str,
        depth: int = 2,
        relation_types: list[str] | None = None,
    ) -> dict:
        """
        理論からグラフをトラバース（インターフェース実装）。

        Returns:
            {
                "nodes": [{"id": ..., "name": ..., "type": ...}, ...],
                "edges": [{"from": ..., "to": ..., "type": ...}, ...]
            }
        """
        return await self.traverse_extended(
            start_node_id=start_theory_id,
            max_depth=depth,
            relationship_types=relation_types,
        )

    async def get_related_theories(
        self,
        theory_id: str,
        relation_type: str,
    ) -> list:
        """特定のリレーションタイプで関連する理論を取得。"""
        query = f"""
        MATCH (t1:Theory {{id: $theory_id}})-[:{relation_type}]-(t2:Theory)
        RETURN t2.id as id, t2.name as name, t2.category as category
        """
        results = await self._adapter.execute_query(query, {"theory_id": theory_id})
        return [{"id": r["id"], "name": r["name"], "category": r["category"]} for r in results]

    async def get_schema(self) -> dict:
        """グラフスキーマ情報を取得。"""
        # ノードラベル取得
        labels_query = "CALL db.labels()"
        labels_result = await self._adapter.execute_query(labels_query)
        labels = [r["label"] for r in labels_result] if labels_result else []

        # リレーションシップタイプ取得
        rel_query = "CALL db.relationshipTypes()"
        rel_result = await self._adapter.execute_query(rel_query)
        rel_types = [r["relationshipType"] for r in rel_result] if rel_result else []

        return {"labels": labels, "relationship_types": rel_types}

    async def get_stats(self) -> dict:
        """グラフの統計情報を取得。"""
        query = """
        MATCH (n)
        WITH labels(n)[0] as label, count(*) as count
        RETURN collect({label: label, count: count}) as node_counts
        """
        results = await self._adapter.execute_query(query)

        node_counts = {}
        if results and results[0].get("node_counts"):
            for item in results[0]["node_counts"]:
                if item.get("label"):
                    node_counts[item["label"]] = item["count"]

        rel_query = """
        MATCH ()-[r]->()
        WITH type(r) as type, count(*) as count
        RETURN collect({type: type, count: count}) as rel_counts
        """
        rel_results = await self._adapter.execute_query(rel_query)

        rel_counts = {}
        if rel_results and rel_results[0].get("rel_counts"):
            for item in rel_results[0]["rel_counts"]:
                if item.get("type"):
                    rel_counts[item["type"]] = item["count"]

        return {"node_counts": node_counts, "relationship_counts": rel_counts}

    # --- Extended methods ---

    async def traverse_extended(
        self,
        start_node_id: str,
        relationship_types: list[str] | None = None,
        max_depth: int = 3,
        direction: str = "both",
    ) -> dict[str, Any]:
        """グラフをトラバース。"""
        # 方向の設定
        if direction == "outgoing":
            rel_pattern = "-[r]->"
        elif direction == "incoming":
            rel_pattern = "<-[r]-"
        else:
            rel_pattern = "-[r]-"

        # リレーションシップタイプのフィルタ
        rel_filter = ""
        if relationship_types:
            types = "|".join(relationship_types)
            rel_pattern = rel_pattern.replace("[r]", f"[r:{types}]")

        query = """
        MATCH (start {id: $start_id})
        CALL apoc.path.subgraphAll(start, {
            maxLevel: $max_depth,
            relationshipFilter: $rel_filter
        })
        YIELD nodes, relationships
        RETURN nodes, relationships
        """

        # APOCがない場合の代替クエリ
        fallback_query = f"""
        MATCH path = (start {{id: $start_id}}){rel_pattern}*(end)
        WHERE length(path) <= $max_depth
        WITH nodes(path) as pathNodes, relationships(path) as pathRels
        UNWIND pathNodes as n
        UNWIND pathRels as r
        WITH collect(DISTINCT n) as nodes, collect(DISTINCT r) as relationships
        RETURN nodes, relationships
        """

        try:
            results = await self._adapter.execute_query(
                query,
                {
                    "start_id": start_node_id,
                    "max_depth": max_depth,
                    "rel_filter": rel_filter,
                },
            )
        except Exception:
            # APOCがない場合、フォールバッククエリを使用
            results = await self._adapter.execute_query(
                fallback_query,
                {"start_id": start_node_id, "max_depth": max_depth},
            )

        if not results:
            return {"nodes": [], "relationships": []}

        record = results[0]
        nodes = []
        relationships = []

        for node in record.get("nodes", []):
            if node:
                nodes.append(
                    {
                        "id": node.get("id"),
                        "labels": list(node.labels) if hasattr(node, "labels") else [],
                        "properties": dict(node),
                    }
                )

        for rel in record.get("relationships", []):
            if rel:
                try:
                    rel_type = rel.type if hasattr(rel, "type") else str(type(rel).__name__)
                    start_id = None
                    end_id = None
                    props = {}

                    # Neo4jリレーションシップオブジェクトの場合
                    if hasattr(rel, "start_node"):
                        start_id = rel.start_node.get("id") if rel.start_node else None
                    if hasattr(rel, "end_node"):
                        end_id = rel.end_node.get("id") if rel.end_node else None

                    # プロパティの取得（辞書として）
                    if hasattr(rel, "items"):
                        props = dict(rel.items())
                    elif hasattr(rel, "_properties"):
                        props = dict(rel._properties)

                    relationships.append(
                        {
                            "type": rel_type,
                            "start_node_id": start_id,
                            "end_node_id": end_id,
                            "properties": props,
                        }
                    )
                except Exception:
                    # エラーが発生した場合は最小限の情報のみ
                    relationships.append(
                        {
                            "type": str(rel),
                            "start_node_id": None,
                            "end_node_id": None,
                            "properties": {},
                        }
                    )

        return {"nodes": nodes, "relationships": relationships}

    async def find_path(
        self,
        start_node_id: str,
        end_node_id: str,
        max_depth: int = 5,
    ) -> list[dict[str, Any]]:
        """2ノード間のパスを検索。"""
        # shortestPathは可変パラメータを直接サポートしないため、
        # max_depthに基づいて動的にクエリを構築
        query = f"""
        MATCH path = shortestPath(
            (start {{id: $start_id}})-[*1..{max_depth}]-(end {{id: $end_id}})
        )
        RETURN [n IN nodes(path) | {{
            id: n.id,
            labels: labels(n),
            name: n.name
        }}] as nodes,
        [r IN relationships(path) | {{
            type: type(r),
            properties: properties(r)
        }}] as relationships
        """
        results = await self._adapter.execute_query(
            query,
            {
                "start_id": start_node_id,
                "end_id": end_node_id,
            },
        )

        if not results:
            return []

        paths = []
        for record in results:
            paths.append(
                {
                    "nodes": record.get("nodes", []),
                    "relationships": record.get("relationships", []),
                }
            )

        return paths

    async def get_related_nodes(
        self,
        node_id: str,
        relationship_type: str | None = None,
        node_type: str | None = None,
    ) -> list[dict[str, Any]]:
        """関連ノードを取得。"""
        # クエリを動的に構築
        rel_pattern = f"-[:{relationship_type}]-" if relationship_type else "-[]-"
        node_pattern = f"(related:{node_type})" if node_type else "(related)"

        query = f"""
        MATCH (start {{id: $node_id}}){rel_pattern}{node_pattern}
        RETURN related
        """
        results = await self._adapter.execute_query(query, {"node_id": node_id})

        related_nodes = []
        for record in results:
            node = record.get("related")
            if node:
                related_nodes.append(
                    {
                        "id": node.get("id"),
                        "labels": list(node.labels) if hasattr(node, "labels") else [],
                        "properties": dict(node),
                    }
                )

        return related_nodes

    async def get_statistics(self) -> dict[str, Any]:
        """グラフ統計を取得。"""
        query = """
        MATCH (n)
        WITH labels(n) as nodeLabels, count(*) as count
        UNWIND nodeLabels as label
        WITH label, sum(count) as nodeCount
        RETURN collect({label: label, count: nodeCount}) as nodeCounts
        """
        node_results = await self._adapter.execute_query(query)

        rel_query = """
        MATCH ()-[r]->()
        WITH type(r) as relType, count(*) as count
        RETURN collect({type: relType, count: count}) as relCounts
        """
        rel_results = await self._adapter.execute_query(rel_query)

        return {
            "node_counts": node_results[0].get("nodeCounts", []) if node_results else [],
            "relationship_counts": rel_results[0].get("relCounts", []) if rel_results else [],
        }
