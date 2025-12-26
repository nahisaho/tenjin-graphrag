"""
統合テスト - Neo4jアダプタとリポジトリ

実際のNeo4jデータベースに接続してテストを実行します。
実行前に: docker compose up -d && uv run python -m tengin_mcp.scripts.seed_data
"""

import pytest
from tengin_mcp.infrastructure.config import Settings
from tengin_mcp.infrastructure.adapters.neo4j_adapter import Neo4jAdapter


@pytest.fixture
async def neo4j_adapter():
    """Neo4jアダプタのフィクスチャ"""
    settings = Settings()
    adapter = Neo4jAdapter(settings)
    await adapter.connect()
    yield adapter
    await adapter.close()


@pytest.mark.asyncio
async def test_neo4j_connection(neo4j_adapter: Neo4jAdapter):
    """Neo4j接続テスト"""
    result = await neo4j_adapter.execute_query("RETURN 1 as value")
    assert len(result) == 1
    assert result[0]["value"] == 1


@pytest.mark.asyncio
async def test_get_all_theories(neo4j_adapter: Neo4jAdapter):
    """全理論取得テスト"""
    result = await neo4j_adapter.execute_query(
        "MATCH (t:Theory) RETURN t.id as id, t.name as name ORDER BY t.name"
    )
    assert len(result) >= 8  # サンプルデータに8件
    
    # 認知負荷理論が存在するか
    theory_ids = [r["id"] for r in result]
    assert "cognitive-load-theory" in theory_ids


@pytest.mark.asyncio
async def test_get_theory_by_id(neo4j_adapter: Neo4jAdapter):
    """IDで理論を取得"""
    result = await neo4j_adapter.execute_query(
        "MATCH (t:Theory {id: $id}) RETURN t",
        parameters={"id": "cognitive-load-theory"}
    )
    assert len(result) == 1
    theory = result[0]["t"]
    assert theory["name"] == "認知負荷理論"
    assert theory["name_en"] == "Cognitive Load Theory"


@pytest.mark.asyncio
async def test_get_theorists(neo4j_adapter: Neo4jAdapter):
    """理論家取得テスト"""
    result = await neo4j_adapter.execute_query(
        "MATCH (t:Theorist) RETURN t.id as id, t.name as name"
    )
    assert len(result) >= 8
    
    names = [r["name"] for r in result]
    assert "ジョン・スウェラー" in names


@pytest.mark.asyncio
async def test_get_concepts(neo4j_adapter: Neo4jAdapter):
    """概念取得テスト"""
    result = await neo4j_adapter.execute_query(
        "MATCH (c:Concept) RETURN c.id as id, c.name as name"
    )
    assert len(result) >= 8


@pytest.mark.asyncio
async def test_get_methodologies(neo4j_adapter: Neo4jAdapter):
    """方法論取得テスト"""
    result = await neo4j_adapter.execute_query(
        "MATCH (m:Methodology) RETURN m.id as id, m.name as name"
    )
    assert len(result) >= 8


@pytest.mark.asyncio
async def test_get_evidence(neo4j_adapter: Neo4jAdapter):
    """エビデンス取得テスト"""
    result = await neo4j_adapter.execute_query(
        "MATCH (e:Evidence) RETURN e.id as id, e.title as title"
    )
    assert len(result) >= 5


@pytest.mark.asyncio
async def test_get_relationships(neo4j_adapter: Neo4jAdapter):
    """関係性取得テスト"""
    result = await neo4j_adapter.execute_query(
        "MATCH ()-[r]->() RETURN type(r) as type, count(r) as count"
    )
    assert len(result) > 0
    
    # 関係タイプの確認
    rel_types = {r["type"] for r in result}
    assert "PROPOSED" in rel_types


@pytest.mark.asyncio
async def test_graph_traversal(neo4j_adapter: Neo4jAdapter):
    """グラフ探索テスト - 理論から関連ノードを取得"""
    result = await neo4j_adapter.execute_query(
        """
        MATCH (t:Theory {id: $theory_id})-[r]->(related)
        RETURN type(r) as rel_type, labels(related)[0] as label, related.id as id
        """,
        parameters={"theory_id": "cognitive-load-theory"}
    )
    assert len(result) > 0


@pytest.mark.asyncio
async def test_search_theories_by_category(neo4j_adapter: Neo4jAdapter):
    """カテゴリで理論を検索"""
    result = await neo4j_adapter.execute_query(
        "MATCH (t:Theory) WHERE t.category = $category RETURN t.id as id, t.name as name",
        parameters={"category": "learning"}
    )
    assert len(result) > 0


@pytest.mark.asyncio
async def test_graph_statistics(neo4j_adapter: Neo4jAdapter):
    """グラフ統計テスト"""
    result = await neo4j_adapter.execute_query(
        """
        MATCH (n)
        RETURN labels(n)[0] as label, count(n) as count
        ORDER BY label
        """
    )
    
    stats = {r["label"]: r["count"] for r in result}
    assert stats.get("Theory", 0) >= 8
    assert stats.get("Theorist", 0) >= 8
    assert stats.get("Concept", 0) >= 8
    assert stats.get("Methodology", 0) >= 8
    assert stats.get("Evidence", 0) >= 5
