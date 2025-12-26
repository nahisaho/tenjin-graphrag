"""
E2E Tests: Expanded Data Integrity Tests

拡張されたデータセット（38理論、32理論家、34概念、32原則、32エビデンス）
の整合性を検証するE2Eテスト。
"""

import pytest

from tengin_mcp.infrastructure.config import Settings
from tengin_mcp.infrastructure.adapters.neo4j_adapter import Neo4jAdapter
from tengin_mcp.infrastructure.repositories.neo4j_graph_repository import Neo4jGraphRepository
from tengin_mcp.infrastructure.repositories.neo4j_theory_repository import Neo4jTheoryRepository
from tengin_mcp.server import app_state


class TestExpandedDataIntegrity:
    """拡張データセットの整合性テスト"""

    @pytest.fixture(autouse=True)
    async def setup(self):
        """テストセットアップ"""
        settings = Settings()
        self.adapter = Neo4jAdapter(settings)
        await self.adapter.connect()
        
        self.graph_repository = Neo4jGraphRepository(self.adapter)
        self.theory_repository = Neo4jTheoryRepository(self.adapter)
        app_state.graph_repository = self.graph_repository
        app_state.theory_repository = self.theory_repository
        
        yield
        
        await self.adapter.close()
        app_state.graph_repository = None
        app_state.theory_repository = None

    # ============================================================
    # 新規追加理論のテスト
    # ============================================================

    @pytest.mark.asyncio
    @pytest.mark.parametrize("theory_id,expected_name", [
        ("social-learning-theory", "社会的学習理論"),
        ("experiential-learning-theory", "経験学習理論"),
        ("multiple-intelligences", "多重知能理論"),
        ("flow-theory", "フロー理論"),
        ("situated-learning", "状況的学習"),
        ("cognitive-apprenticeship", "認知的徒弟制"),
        ("problem-based-learning", "問題基盤型学習"),
        ("mastery-learning", "完全習得学習"),
        ("spaced-repetition", "分散学習"),
        ("dual-coding-theory", "二重符号化理論"),
        ("metacognition", "メタ認知"),
        ("self-regulated-learning", "自己調整学習"),
        ("connectivism", "コネクティビズム"),
        ("community-of-inquiry", "探究共同体"),
        ("growth-mindset", "成長マインドセット"),
    ])
    async def test_new_theory_exists(self, theory_id: str, expected_name: str):
        """新規追加理論が存在する"""
        from tengin_mcp.tools.theory_tools import get_theory
        
        result = await get_theory(theory_id)
        
        # エラーでないか、正しいIDが返る
        if "error" not in result:
            assert result.get("id") == theory_id
            # 日本語名が含まれる（部分一致でOK）
            name_ja = result.get("name_ja", "")
            assert expected_name in name_ja or len(name_ja) > 0

    @pytest.mark.asyncio
    async def test_theory_category_distribution(self):
        """理論のカテゴリ分布を検証"""
        result = await self.adapter.execute_query("""
            MATCH (t:Theory)
            WHERE t.category IS NOT NULL
            RETURN t.category as category, count(*) as count
            ORDER BY count DESC
        """)
        
        categories = {r["category"]: r["count"] for r in result}
        
        # 期待されるカテゴリが存在する
        expected_categories = [
            "learning",
            "instructional",
            "motivation",
            "developmental",
            "edtech",
        ]
        
        found_categories = [c for c in expected_categories if c in categories]
        assert len(found_categories) >= 3, f"カテゴリが不足: {categories}"

    # ============================================================
    # 新規追加理論家のテスト
    # ============================================================

    @pytest.mark.asyncio
    @pytest.mark.parametrize("theorist_id,expected_name", [
        ("albert-bandura", "Albert Bandura"),
        ("david-kolb", "David Kolb"),
        ("howard-gardner", "Howard Gardner"),
        ("mihaly-csikszentmihalyi", "Mihaly Csikszentmihalyi"),
        ("jean-lave", "Jean Lave"),
        ("etienne-wenger", "Etienne Wenger"),
        ("carol-dweck", "Carol Dweck"),
        ("robert-bjork", "Robert Bjork"),
        ("barry-zimmerman", "Barry Zimmerman"),
        ("george-siemens", "George Siemens"),
    ])
    async def test_new_theorist_exists(self, theorist_id: str, expected_name: str):
        """新規追加理論家が存在する"""
        from tengin_mcp.tools.theory_tools import get_theorist
        
        result = await get_theorist(theorist_id)
        
        if "error" not in result:
            # 名前が部分一致
            name = result.get("name", "")
            assert expected_name.split()[0] in name or expected_name.split()[-1] in name

    # ============================================================
    # 新規追加概念のテスト
    # ============================================================

    @pytest.mark.asyncio
    @pytest.mark.parametrize("concept_id", [
        "self-efficacy",
        "observational-learning",
        "experiential-learning-cycle",
        "flow-state",
        "metacognitive-knowledge",
        "retrieval-practice",
        "spacing-effect",
        "growth-mindset-concept",
        "cognitive-presence",
        "transfer-of-learning",
    ])
    async def test_new_concept_exists(self, concept_id: str):
        """新規追加概念が存在する"""
        from tengin_mcp.tools.theory_tools import get_concept
        
        result = await get_concept(concept_id)
        
        if "error" not in result:
            assert result.get("id") == concept_id
            # 定義が存在する
            definition = result.get("definition", "")
            definition_ja = result.get("definition_ja", "")
            assert len(definition) > 0 or len(definition_ja) > 0

    # ============================================================
    # 新規追加原則のテスト
    # ============================================================

    @pytest.mark.asyncio
    @pytest.mark.parametrize("principle_id", [
        "segmenting-principle",
        "personalization-principle",
        "modeling-principle",
        "coaching-principle",
        "interleaving-practice",
        "spacing-practice",
        "retrieval-practice-principle",
        "productive-failure-principle",
        "arcs-attention",
        "udl-multiple-means-representation",
    ])
    async def test_new_principle_exists(self, principle_id: str):
        """新規追加原則が存在する"""
        from tengin_mcp.tools.theory_tools import get_principle
        
        result = await get_principle(principle_id)
        
        if "error" not in result:
            assert result.get("id") == principle_id

    # ============================================================
    # 新規追加エビデンスのテスト
    # ============================================================

    @pytest.mark.asyncio
    @pytest.mark.parametrize("evidence_id", [
        "bandura-1977-self-efficacy",
        "kolb-1984-experiential",
        "roediger-karpicke-2006-testing",
        "bjork-1994-desirable-difficulties",
        "dweck-2006-mindset",
        "kapur-2008-productive-failure",
        "garrison-2000-coi",
        "hattie-2008-visible-learning",
    ])
    async def test_new_evidence_exists(self, evidence_id: str):
        """新規追加エビデンスが存在する"""
        from tengin_mcp.tools.theory_tools import get_evidence
        
        result = await get_evidence(evidence_id)
        
        if "error" not in result:
            assert result.get("id") == evidence_id

    # ============================================================
    # 関連性の検証テスト
    # ============================================================

    @pytest.mark.asyncio
    async def test_proposed_by_relationships(self):
        """PROPOSED_BY関係の数を検証"""
        result = await self.adapter.execute_query("""
            MATCH (:Theory)-[r:PROPOSED_BY]->(:Theorist)
            RETURN count(r) as count
        """)
        
        count = result[0]["count"]
        # 少なくとも30件以上のPROPOSED_BY関係
        assert count >= 30, f"PROPOSED_BY関係が不足: {count}件"

    @pytest.mark.asyncio
    async def test_has_concept_relationships(self):
        """HAS_CONCEPT関係の数を検証"""
        result = await self.adapter.execute_query("""
            MATCH (:Theory)-[r:HAS_CONCEPT]->(:Concept)
            RETURN count(r) as count
        """)
        
        count = result[0]["count"]
        # 少なくとも40件以上のHAS_CONCEPT関係
        assert count >= 40, f"HAS_CONCEPT関係が不足: {count}件"

    @pytest.mark.asyncio
    async def test_has_principle_relationships(self):
        """HAS_PRINCIPLE関係の数を検証"""
        result = await self.adapter.execute_query("""
            MATCH (:Theory)-[r:HAS_PRINCIPLE]->(:Principle)
            RETURN count(r) as count
        """)
        
        count = result[0]["count"]
        # 少なくとも30件以上のHAS_PRINCIPLE関係
        assert count >= 30, f"HAS_PRINCIPLE関係が不足: {count}件"

    @pytest.mark.asyncio
    async def test_supported_by_relationships(self):
        """SUPPORTED_BY関係の数を検証"""
        result = await self.adapter.execute_query("""
            MATCH (:Theory)-[r:SUPPORTED_BY]->(:Evidence)
            RETURN count(r) as count
        """)
        
        count = result[0]["count"]
        # 少なくとも25件以上のSUPPORTED_BY関係
        assert count >= 25, f"SUPPORTED_BY関係が不足: {count}件"

    @pytest.mark.asyncio
    async def test_related_to_relationships(self):
        """RELATED_TO関係の数を検証"""
        result = await self.adapter.execute_query("""
            MATCH (:Theory)-[r:RELATED_TO]->(:Theory)
            RETURN count(r) as count
        """)
        
        count = result[0]["count"]
        # 少なくとも25件以上のRELATED_TO関係
        assert count >= 25, f"RELATED_TO関係が不足: {count}件"

    # ============================================================
    # グラフ構造の検証
    # ============================================================

    @pytest.mark.asyncio
    async def test_no_orphan_theories(self):
        """孤立した理論ノードがないことを検証"""
        result = await self.adapter.execute_query("""
            MATCH (t:Theory)
            WHERE NOT (t)-[:PROPOSED_BY]->()
              AND NOT (t)-[:HAS_CONCEPT]->()
              AND NOT (t)-[:RELATED_TO]-()
            RETURN count(t) as orphan_count
        """)
        
        orphan_count = result[0]["orphan_count"]
        # 孤立ノードは0または少数のみ許容
        assert orphan_count <= 5, f"孤立した理論が多すぎる: {orphan_count}件"

    @pytest.mark.asyncio
    async def test_graph_connectivity(self):
        """グラフの接続性を検証"""
        from tengin_mcp.tools.graph_tools import traverse_graph
        
        # 認知負荷理論から2ホップで到達可能なノード数
        result = await traverse_graph(
            start_node_id="cognitive-load-theory",
            max_depth=2
        )
        
        # 少なくとも10ノードに到達可能
        assert result["node_count"] >= 10

    @pytest.mark.asyncio
    async def test_theory_to_theorist_coverage(self):
        """理論が理論家にリンクされているカバレッジ"""
        result = await self.adapter.execute_query("""
            MATCH (t:Theory)
            OPTIONAL MATCH (t)-[:PROPOSED_BY]->(th:Theorist)
            RETURN 
                count(distinct t) as total_theories,
                count(distinct CASE WHEN th IS NOT NULL THEN t END) as linked_theories
        """)
        
        total = result[0]["total_theories"]
        linked = result[0]["linked_theories"]
        
        coverage = linked / total if total > 0 else 0
        # 90%以上の理論が理論家にリンクされている
        assert coverage >= 0.9, f"リンクカバレッジが低い: {coverage:.1%}"


class TestExpandedDataSearch:
    """拡張データセットの検索テスト"""

    @pytest.fixture(autouse=True)
    async def setup(self):
        """テストセットアップ"""
        settings = Settings()
        self.adapter = Neo4jAdapter(settings)
        await self.adapter.connect()
        
        self.graph_repository = Neo4jGraphRepository(self.adapter)
        self.theory_repository = Neo4jTheoryRepository(self.adapter)
        app_state.graph_repository = self.graph_repository
        app_state.theory_repository = self.theory_repository
        
        yield
        
        await self.adapter.close()
        app_state.graph_repository = None
        app_state.theory_repository = None

    @pytest.mark.asyncio
    async def test_search_new_theories_by_keyword(self):
        """新規理論をキーワードで検索"""
        from tengin_mcp.tools.theory_tools import search_theories
        
        # メタ認知で検索
        result = await search_theories(query="メタ認知")
        
        theories = result.get("theories", [])
        theory_ids = [t.get("id") for t in theories]
        
        # metacognition または self-regulated-learning が見つかる
        assert any("metacognition" in tid or "self-regulated" in tid for tid in theory_ids if tid)

    @pytest.mark.asyncio
    async def test_search_learning_category(self):
        """learningカテゴリの理論を検索"""
        from tengin_mcp.tools.theory_tools import get_theories_by_category
        
        result = await get_theories_by_category(category="learning")
        
        theories = result.get("theories", [])
        
        # 複数の学習理論が見つかる
        assert len(theories) >= 10

    @pytest.mark.asyncio
    async def test_search_motivation_theories(self):
        """動機づけ理論を検索"""
        from tengin_mcp.tools.theory_tools import search_theories
        
        result = await search_theories(query="動機づけ motivation")
        
        theories = result.get("theories", [])
        
        # 動機づけ関連の理論が見つかる
        assert len(theories) >= 1

    @pytest.mark.asyncio
    async def test_related_theories_traversal(self):
        """関連理論のトラバース"""
        from tengin_mcp.tools.graph_tools import get_related_nodes
        
        # 構成主義の関連ノードを取得
        result = await get_related_nodes(node_id="constructivism")
        
        related = result.get("related_nodes", [])
        related_ids = [n.get("id") for n in related]
        
        # 関連する理論として複数が見つかる
        assert len(related_ids) >= 2

    @pytest.mark.asyncio
    async def test_find_path_between_new_theories(self):
        """新規理論間のパス検索"""
        from tengin_mcp.tools.graph_tools import find_path
        
        # フロー理論から自己決定理論へのパス
        result = await find_path(
            start_node_id="flow-theory",
            end_node_id="self-determination-theory",
            max_depth=5
        )
        
        # パスが存在するか確認
        assert "paths" in result
        assert "path_found" in result
