"""
Neo4j Graph Repository の統合テスト

traverse, find_path, get_statistics などのテスト
"""

import pytest

from tengin_mcp.infrastructure.config import Settings
from tengin_mcp.infrastructure.adapters.neo4j_adapter import Neo4jAdapter
from tengin_mcp.infrastructure.repositories.neo4j_graph_repository import Neo4jGraphRepository


@pytest.fixture
async def graph_repository():
    """グラフリポジトリのフィクスチャ"""
    settings = Settings()
    adapter = Neo4jAdapter(settings)
    await adapter.connect()
    
    repo = Neo4jGraphRepository(adapter)
    
    yield repo
    
    await adapter.close()


class TestGraphTraversal:
    """グラフ探索のテスト"""

    @pytest.mark.asyncio
    async def test_traverse_from_theory(self, graph_repository):
        """理論からの探索"""
        result = await graph_repository.traverse_extended(
            start_node_id="cognitive-load-theory",
            relationship_types=None,
            max_depth=1,
            direction="outgoing",
        )
        
        assert isinstance(result, dict)
        assert "nodes" in result or "relationships" in result

    @pytest.mark.asyncio
    async def test_traverse_with_relationship_filter(self, graph_repository):
        """関係タイプでフィルタリングした探索"""
        result = await graph_repository.traverse_extended(
            start_node_id="cognitive-load-theory",
            relationship_types=["INCLUDES_CONCEPT"],
            max_depth=1,
            direction="outgoing",
        )
        
        assert isinstance(result, dict)

    @pytest.mark.asyncio
    async def test_traverse_incoming(self, graph_repository):
        """入方向の探索"""
        result = await graph_repository.traverse_extended(
            start_node_id="cognitive-load-theory",
            relationship_types=None,
            max_depth=1,
            direction="incoming",
        )
        
        assert isinstance(result, dict)

    @pytest.mark.asyncio
    async def test_traverse_both_directions(self, graph_repository):
        """双方向の探索"""
        result = await graph_repository.traverse_extended(
            start_node_id="cognitive-load-theory",
            relationship_types=None,
            max_depth=1,
            direction="both",
        )
        
        assert isinstance(result, dict)

    @pytest.mark.asyncio
    async def test_traverse_interface_method(self, graph_repository):
        """インターフェースメソッドでの探索"""
        result = await graph_repository.traverse(
            start_theory_id="cognitive-load-theory",
            depth=1,
            relation_types=None,
        )
        
        assert isinstance(result, dict)


class TestFindPath:
    """パス検索のテスト"""

    @pytest.mark.asyncio
    async def test_find_path_between_theories(self, graph_repository):
        """理論間のパス検索"""
        result = await graph_repository.find_path(
            start_node_id="cognitive-load-theory",
            end_node_id="multimedia-learning-theory",
            max_depth=3,
        )
        
        assert isinstance(result, list)

    @pytest.mark.asyncio
    async def test_find_path_with_max_depth(self, graph_repository):
        """深さ指定でのパス検索"""
        result = await graph_repository.find_path(
            start_node_id="cognitive-load-theory",
            end_node_id="multimedia-learning-theory",
            max_depth=5,
        )
        
        assert isinstance(result, list)


class TestGetRelatedTheories:
    """関連理論取得のテスト"""

    @pytest.mark.asyncio
    async def test_get_related_theories(self, graph_repository):
        """関連理論の取得"""
        result = await graph_repository.get_related_theories(
            theory_id="cognitive-load-theory",
            relation_type="RELATED_TO",
        )
        
        assert isinstance(result, list)


class TestGraphStatistics:
    """グラフ統計のテスト"""

    @pytest.mark.asyncio
    async def test_get_statistics(self, graph_repository):
        """統計情報の取得（get_statistics）"""
        result = await graph_repository.get_statistics()
        
        assert isinstance(result, dict)
        assert "node_counts" in result
        assert "relationship_counts" in result

    @pytest.mark.asyncio
    async def test_get_stats(self, graph_repository):
        """統計情報の取得（get_stats）"""
        result = await graph_repository.get_stats()
        
        assert isinstance(result, dict)
        assert "node_counts" in result
        assert "relationship_counts" in result

    @pytest.mark.asyncio
    async def test_statistics_include_expected_labels(self, graph_repository):
        """期待されるラベルが含まれること"""
        result = await graph_repository.get_statistics()
        
        node_counts = result.get("node_counts", [])
        if isinstance(node_counts, list):
            labels = [item.get("label") for item in node_counts]
        else:
            labels = list(node_counts.keys())
        
        # 少なくともTheoryが含まれる
        assert "Theory" in labels


class TestGraphSchema:
    """グラフスキーマのテスト"""

    @pytest.mark.asyncio
    async def test_get_schema(self, graph_repository):
        """スキーマ情報の取得"""
        result = await graph_repository.get_schema()
        
        assert isinstance(result, dict)
        assert "labels" in result
        assert "relationship_types" in result
        
        # Theoryラベルが存在
        assert "Theory" in result["labels"]


class TestExecuteCypher:
    """Cypher実行のテスト"""

    @pytest.mark.asyncio
    async def test_execute_cypher(self, graph_repository):
        """Cypherクエリの実行"""
        result = await graph_repository.execute_cypher(
            "MATCH (t:Theory) RETURN count(t) as count"
        )
        
        assert isinstance(result, list)
        assert len(result) > 0
        assert result[0]["count"] >= 8

    @pytest.mark.asyncio
    async def test_execute_cypher_with_params(self, graph_repository):
        """パラメータ付きCypherクエリの実行"""
        result = await graph_repository.execute_cypher(
            "MATCH (t:Theory {id: $id}) RETURN t.name as name",
            {"id": "cognitive-load-theory"},
        )
        
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]["name"] == "認知負荷理論"
