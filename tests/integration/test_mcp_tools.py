"""
MCPツールの統合テスト

実際のNeo4jとChromaDBを使用してMCPツールの動作を確認します。
"""

import pytest

from tengin_mcp.infrastructure.config import Settings
from tengin_mcp.infrastructure.adapters.neo4j_adapter import Neo4jAdapter
from tengin_mcp.infrastructure.adapters.chromadb_adapter import ChromaDBAdapter
from tengin_mcp.infrastructure.adapters.embedding_adapter import EmbeddingAdapter


# --- Fixtures ---


@pytest.fixture
async def settings():
    """テスト用設定"""
    return Settings()


@pytest.fixture
async def neo4j_adapter(settings):
    """Neo4jアダプター"""
    adapter = Neo4jAdapter(settings)
    await adapter.connect()
    yield adapter
    await adapter.close()


@pytest.fixture
async def chromadb_adapter(settings):
    """ChromaDBアダプター"""
    adapter = ChromaDBAdapter(settings)
    await adapter.connect()
    yield adapter
    await adapter.close()


@pytest.fixture
async def embedding_adapter(settings):
    """Embeddingアダプター（Ollamaが利用可能な場合のみ）"""
    if settings.embedding_provider == "ollama":
        adapter = EmbeddingAdapter(settings)
        try:
            await adapter.connect()
            yield adapter
            await adapter.close()
        except Exception:
            pytest.skip("Ollama not available")
    else:
        pytest.skip("Embedding provider not configured")


# --- Theory Tools Tests ---


class TestTheoryTools:
    """理論関連ツールのテスト"""

    async def test_get_all_theories(self, neo4j_adapter):
        """全理論取得テスト"""
        result = await neo4j_adapter.execute_query(
            "MATCH (t:Theory) RETURN t.id as id, t.name as name ORDER BY t.name"
        )
        
        assert len(result) > 0
        assert all("id" in r for r in result)
        assert all("name" in r for r in result)
        
        # 認知負荷理論が含まれているか
        ids = [r["id"] for r in result]
        assert "cognitive-load-theory" in ids

    async def test_get_theory_by_id(self, neo4j_adapter):
        """ID指定で理論取得テスト"""
        result = await neo4j_adapter.execute_query(
            """
            MATCH (t:Theory {id: $id})
            RETURN t.id as id, t.name as name, t.description as description,
                   t.category as category, t.evidence_level as evidence_level
            """,
            parameters={"id": "cognitive-load-theory"}
        )
        
        assert len(result) == 1
        theory = result[0]
        assert theory["id"] == "cognitive-load-theory"
        assert theory["name"] == "認知負荷理論"
        assert theory["category"] == "learning"
        assert theory["evidence_level"] == "strong"
        assert "ワーキングメモリ" in theory["description"]

    async def test_get_theory_with_related_nodes(self, neo4j_adapter):
        """理論と関連ノードの取得テスト"""
        result = await neo4j_adapter.execute_query(
            """
            MATCH (t:Theory {id: $id})
            OPTIONAL MATCH (t)-[:INCLUDES_CONCEPT]->(c:Concept)
            OPTIONAL MATCH (th:Theorist)-[:PROPOSED]->(t)
            RETURN t.name as theory_name,
                   collect(DISTINCT c.name) as concepts,
                   collect(DISTINCT th.name) as theorists
            """,
            parameters={"id": "cognitive-load-theory"}
        )
        
        assert len(result) == 1
        data = result[0]
        assert data["theory_name"] == "認知負荷理論"
        assert len(data["concepts"]) > 0

    async def test_search_theories_by_category(self, neo4j_adapter):
        """カテゴリで理論検索テスト"""
        result = await neo4j_adapter.execute_query(
            """
            MATCH (t:Theory)
            WHERE t.category = $category
            RETURN t.id as id, t.name as name
            ORDER BY t.name
            """,
            parameters={"category": "learning"}
        )
        
        assert len(result) >= 2
        names = [r["name"] for r in result]
        assert "認知負荷理論" in names
        assert "構成主義" in names

    async def test_get_theory_not_found(self, neo4j_adapter):
        """存在しない理論IDでの検索テスト"""
        result = await neo4j_adapter.execute_query(
            "MATCH (t:Theory {id: $id}) RETURN t",
            parameters={"id": "non-existent-theory"}
        )
        
        assert len(result) == 0


# --- Graph Tools Tests ---


class TestGraphTools:
    """グラフ関連ツールのテスト"""

    async def test_traverse_from_theory(self, neo4j_adapter):
        """理論からのグラフ探索テスト"""
        result = await neo4j_adapter.execute_query(
            """
            MATCH (t:Theory {id: $id})-[r]->(related)
            RETURN type(r) as relationship, 
                   labels(related)[0] as node_type,
                   related.id as node_id,
                   related.name as node_name
            """,
            parameters={"id": "cognitive-load-theory"}
        )
        
        assert len(result) > 0
        
        # 関係タイプの確認
        rel_types = set(r["relationship"] for r in result)
        assert "INCLUDES_CONCEPT" in rel_types or "RELATED_TO" in rel_types

    async def test_find_related_theories(self, neo4j_adapter):
        """関連理論の検索テスト"""
        result = await neo4j_adapter.execute_query(
            """
            MATCH (t1:Theory {id: $id})-[:RELATED_TO]-(t2:Theory)
            RETURN t2.id as id, t2.name as name
            """,
            parameters={"id": "cognitive-load-theory"}
        )
        
        # マルチメディア学習理論が関連しているはず
        if len(result) > 0:
            ids = [r["id"] for r in result]
            assert "multimedia-learning-theory" in ids

    async def test_get_concept_usage(self, neo4j_adapter):
        """概念の使用状況テスト"""
        result = await neo4j_adapter.execute_query(
            """
            MATCH (c:Concept {id: $id})<-[:INCLUDES_CONCEPT]-(t:Theory)
            RETURN t.id as theory_id, t.name as theory_name
            """,
            parameters={"id": "cognitive-load"}
        )
        
        assert len(result) > 0
        theory_ids = [r["theory_id"] for r in result]
        assert "cognitive-load-theory" in theory_ids

    async def test_get_graph_statistics(self, neo4j_adapter):
        """グラフ統計テスト"""
        result = await neo4j_adapter.execute_query(
            """
            MATCH (n)
            RETURN labels(n)[0] as label, count(*) as count
            ORDER BY count DESC
            """
        )
        
        stats = {r["label"]: r["count"] for r in result}
        
        assert stats.get("Theory", 0) >= 8
        assert stats.get("Theorist", 0) >= 5
        assert stats.get("Concept", 0) >= 5
        assert stats.get("Evidence", 0) >= 5
        assert stats.get("Methodology", 0) >= 5


# --- Citation Tools Tests ---


class TestCitationTools:
    """引用関連ツールのテスト"""

    async def test_get_evidence_for_theory(self, neo4j_adapter):
        """理論のエビデンス取得テスト"""
        result = await neo4j_adapter.execute_query(
            """
            MATCH (e:Evidence)-[:SUPPORTS]->(t:Theory {id: $id})
            RETURN e.id as id, e.title as title, e.authors as authors,
                   e.year as year
            """,
            parameters={"id": "cognitive-load-theory"}
        )
        
        assert len(result) > 0
        evidence = result[0]
        assert evidence["year"] >= 1988

    async def test_get_theorist_info(self, neo4j_adapter):
        """理論家情報取得テスト"""
        result = await neo4j_adapter.execute_query(
            """
            MATCH (th:Theorist {id: $id})
            OPTIONAL MATCH (th)-[:PROPOSED]->(t:Theory)
            RETURN th.name as name, th.nationality as nationality,
                   th.field as field, collect(t.name) as theories
            """,
            parameters={"id": "sweller"}
        )
        
        assert len(result) == 1
        theorist = result[0]
        assert theorist["name"] == "ジョン・スウェラー"
        assert "認知負荷理論" in theorist["theories"]


# --- Embedding Tests ---


class TestEmbeddingTools:
    """埋め込み関連ツールのテスト（Ollamaが利用可能な場合）"""

    async def test_embed_single_text(self, embedding_adapter):
        """単一テキストの埋め込みテスト"""
        text = "認知負荷理論は学習者のワーキングメモリを考慮した教育設計の理論です。"
        embedding = await embedding_adapter.embed_text(text)
        
        assert isinstance(embedding, list)
        assert len(embedding) > 0
        assert all(isinstance(v, float) for v in embedding)

    async def test_embed_multiple_texts(self, embedding_adapter):
        """複数テキストの埋め込みテスト"""
        texts = [
            "認知負荷理論",
            "構成主義",
            "発達の最近接領域",
        ]
        embeddings = await embedding_adapter.embed_texts(texts)
        
        assert len(embeddings) == 3
        assert all(len(e) > 0 for e in embeddings)
        
        # すべて同じ次元であること
        dims = [len(e) for e in embeddings]
        assert dims[0] == dims[1] == dims[2]

    async def test_chromadb_add_and_search(self, chromadb_adapter, embedding_adapter):
        """ChromaDBへの追加と検索テスト"""
        # テストデータ
        docs = [
            "認知負荷理論はワーキングメモリの制限を考慮する",
            "構成主義は学習者が知識を構築する",
            "足場かけは支援を段階的に減らす",
        ]
        
        # 埋め込み生成
        embeddings = await embedding_adapter.embed_texts(docs)
        
        # テスト用コレクションに追加（既存データをクリア）
        collection = chromadb_adapter.collection
        
        # 新しいIDで追加
        test_ids = [f"test-search-{i}" for i in range(len(docs))]
        
        # 既存のテストデータを削除
        try:
            collection.delete(ids=test_ids)
        except Exception:
            pass
        
        # 追加
        await chromadb_adapter.add_documents(
            ids=test_ids,
            documents=docs,
            embeddings=embeddings,
        )
        
        # 検索
        query = "メモリと学習"
        query_embedding = await embedding_adapter.embed_text(query)
        results = await chromadb_adapter.search(
            query_embedding=query_embedding,
            n_results=2
        )
        
        assert "documents" in results
        assert len(results["documents"][0]) > 0
        
        # クリーンアップ
        try:
            collection.delete(ids=test_ids)
        except Exception:
            pass


# --- Compare Tools Tests ---


class TestCompareTools:
    """比較ツールのテスト"""

    async def test_compare_two_theories(self, neo4j_adapter):
        """2つの理論の比較テスト"""
        result = await neo4j_adapter.execute_query(
            """
            MATCH (t:Theory)
            WHERE t.id IN $ids
            RETURN t.id as id, t.name as name, t.category as category,
                   t.description as description, t.evidence_level as evidence_level
            """,
            parameters={"ids": ["cognitive-load-theory", "constructivism"]}
        )
        
        assert len(result) == 2
        
        theories = {r["id"]: r for r in result}
        
        # 両方の理論が取得できていること
        assert "cognitive-load-theory" in theories
        assert "constructivism" in theories
        
        # 同じカテゴリであること
        assert theories["cognitive-load-theory"]["category"] == "learning"
        assert theories["constructivism"]["category"] == "learning"

    async def test_find_common_concepts(self, neo4j_adapter):
        """共通概念の検索テスト"""
        result = await neo4j_adapter.execute_query(
            """
            MATCH (t1:Theory {id: $id1})-[:INCLUDES_CONCEPT]->(c:Concept)<-[:INCLUDES_CONCEPT]-(t2:Theory {id: $id2})
            RETURN c.id as id, c.name as name
            """,
            parameters={
                "id1": "cognitive-load-theory",
                "id2": "multimedia-learning-theory"
            }
        )
        
        # 共通概念がある場合
        if len(result) > 0:
            assert all("id" in r for r in result)
            assert all("name" in r for r in result)
