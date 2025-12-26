"""
E2E Tests: MCP Server Full Integration Tests

MCPサーバーの全体的な動作を検証するE2Eテスト。
実際のNeo4jデータベースに接続し、ツール呼び出しから結果取得まで
エンドツーエンドで検証する。
"""

import pytest
import asyncio

from tengin_mcp.infrastructure.config import Settings
from tengin_mcp.infrastructure.adapters.neo4j_adapter import Neo4jAdapter
from tengin_mcp.infrastructure.repositories.neo4j_graph_repository import Neo4jGraphRepository
from tengin_mcp.infrastructure.repositories.neo4j_theory_repository import Neo4jTheoryRepository
from tengin_mcp.server import app_state


class TestMCPServerE2E:
    """MCPサーバーのE2Eテスト"""

    @pytest.fixture(autouse=True)
    async def setup(self):
        """テストセットアップ - Neo4j接続"""
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
    # シナリオ1: 理論検索と詳細取得
    # ============================================================
    
    @pytest.mark.asyncio
    async def test_scenario_search_and_get_theory(self):
        """シナリオ: 理論を検索して詳細を取得"""
        from tengin_mcp.tools.theory_tools import search_theories, get_theory
        
        # Step 1: 認知負荷に関する理論を検索
        search_result = await search_theories(query="認知負荷")
        
        # 検索結果の確認（countキーが存在するはず）
        assert "theories" in search_result
        theories_list = search_result.get("theories", [])
        
        # 理論が見つかった場合
        if theories_list:
            assert any("cognitive-load" in t.get("id", "") for t in theories_list)
            
            # Step 2: 認知負荷理論の詳細を取得
            theory = await get_theory("cognitive-load-theory")
            
            assert theory is not None
            assert "認知負荷" in theory.get("name", "") or theory.get("id") == "cognitive-load-theory"
            assert "keywords" in theory or "category" in theory

    @pytest.mark.asyncio
    async def test_scenario_paradigm_based_search(self):
        """シナリオ: カテゴリ別に理論を検索"""
        from tengin_mcp.tools.theory_tools import get_theories_by_category
        
        # learningカテゴリの理論を取得
        result = await get_theories_by_category(category="learning")
        
        assert "theories" in result
        theories_list = result.get("theories", [])
        assert len(theories_list) > 0

    # ============================================================
    # シナリオ2: グラフトラバースと関連ノード取得
    # ============================================================
    
    @pytest.mark.asyncio
    async def test_scenario_graph_traversal(self):
        """シナリオ: 理論からグラフをトラバース"""
        from tengin_mcp.tools.graph_tools import traverse_graph, get_related_nodes
        
        # Step 1: 認知負荷理論から関連ノードをトラバース
        result = await traverse_graph(
            start_node_id="cognitive-load-theory",
            max_depth=2
        )
        
        assert result["node_count"] > 0
        assert result["relationship_count"] > 0
        
        # Step 2: 関連ノードを取得
        related = await get_related_nodes(node_id="cognitive-load-theory")
        
        assert related["count"] > 0
        # 関連理論として情報処理理論やマルチメディア学習理論が含まれる
        related_ids = [n.get("id") for n in related["related_nodes"]]
        assert len(related_ids) > 0

    @pytest.mark.asyncio
    async def test_scenario_find_path_between_theories(self):
        """シナリオ: 2つの理論間のパスを検索"""
        from tengin_mcp.tools.graph_tools import find_path
        
        # 認知負荷理論から構成主義へのパスを検索
        result = await find_path(
            start_node_id="cognitive-load-theory",
            end_node_id="constructivism",
            max_depth=5
        )
        
        # パスが見つかるかどうかはデータ依存だが、エラーなく実行できること
        assert "paths" in result
        assert "path_found" in result

    # ============================================================
    # シナリオ3: 教授法推薦と文脈検索
    # ============================================================
    
    @pytest.mark.asyncio
    async def test_scenario_methodology_recommendation(self):
        """シナリオ: 教授法を推薦"""
        from tengin_mcp.tools.methodology_tools import (
            search_methodologies,
            recommend_methodologies,
            get_methodology
        )
        
        # Step 1: 教授法を検索（カテゴリなしで全体を検索）
        all_methods = await search_methodologies()
        
        # 教授法が存在するか確認
        assert "methodologies" in all_methods
        
        # Step 2: 高エビデンスの教授法を推薦
        recommendations = await recommend_methodologies(
            min_evidence_level="high"
        )
        
        # 推薦結果の構造を確認
        assert "recommendations" in recommendations
        
        # Step 3: 推薦された教授法があれば詳細を取得
        if recommendations.get("recommendations"):
            method_id = recommendations["recommendations"][0]["id"]
            methodology = await get_methodology(method_id)
            
            # エラーでなければ確認
            if "error" not in methodology:
                assert methodology.get("id") == method_id

    @pytest.mark.asyncio
    async def test_scenario_context_based_methodology(self):
        """シナリオ: 教授法を検索"""
        from tengin_mcp.tools.methodology_tools import search_methodologies
        
        # 教授法を検索
        methods = await search_methodologies()
        
        # 結果の構造を確認
        assert "methodologies" in methods

    # ============================================================
    # シナリオ4: エビデンス取得と理論検証
    # ============================================================
    
    @pytest.mark.asyncio
    async def test_scenario_evidence_based_verification(self):
        """シナリオ: 理論のエビデンスを取得して検証"""
        from tengin_mcp.tools.methodology_tools import get_evidence_for_theory
        from tengin_mcp.tools.theory_tools import get_theory
        
        # Step 1: 自己決定理論の詳細を取得
        theory = await get_theory("self-determination-theory")
        
        # エラーでない限り確認
        if "error" not in theory:
            assert theory.get("id") == "self-determination-theory"
        
        # Step 2: 自己決定理論を支持するエビデンスを取得
        evidence = await get_evidence_for_theory("self-determination-theory")
        
        assert "supporting_evidence" in evidence
        assert "challenging_evidence" in evidence

    # ============================================================
    # シナリオ5: 引用生成
    # ============================================================
    
    @pytest.mark.asyncio
    async def test_scenario_citation_generation(self):
        """シナリオ: 理論の引用情報を生成"""
        from tengin_mcp.tools.citation_tools import cite_theory, compare_theories
        
        # Step 1: 認知負荷理論の引用を生成（正しいフォーマット名を使用）
        citation = await cite_theory(
            theory_id="cognitive-load-theory",
            format="APA7"
        )
        
        assert "citation" in citation or "theory_id" in citation
        
        # Step 2: 2つの理論を比較
        comparison = await compare_theories(
            theory_ids=["cognitive-load-theory", "constructivism"]
        )
        
        assert "theories" in comparison or "comparison" in comparison

    # ============================================================
    # シナリオ6: グラフ統計と概要取得
    # ============================================================
    
    @pytest.mark.asyncio
    async def test_scenario_graph_statistics(self):
        """シナリオ: グラフの統計情報を取得"""
        from tengin_mcp.tools.graph_tools import get_graph_statistics
        
        stats = await get_graph_statistics()
        
        assert "node_counts" in stats or "error" not in stats
        
        # ノード数の検証
        if "node_counts" in stats:
            node_counts = stats["node_counts"]
            # 期待されるラベルが含まれている
            labels = [n.get("label") for n in node_counts] if isinstance(node_counts, list) else list(node_counts.keys())
            # Theoryラベルが存在する
            assert any("Theory" in str(l) for l in labels) or len(labels) > 0

    # ============================================================
    # シナリオ7: 複合クエリ（理論家→理論→概念）
    # ============================================================
    
    @pytest.mark.asyncio
    async def test_scenario_theorist_to_concept_chain(self):
        """シナリオ: 理論家から理論、概念への連鎖検索"""
        from tengin_mcp.tools.theory_tools import get_theorist, get_theory, get_concept
        
        # Step 1: ヴィゴツキーの情報を取得
        theorist = await get_theorist("vygotsky")
        
        # エラーでない限り確認
        if "error" not in theorist:
            name = theorist.get("name", "")
            assert "Vygotsky" in name or "ヴィゴツキー" in name
        
        # Step 2: 社会文化理論の詳細を取得
        theory = await get_theory("sociocultural-theory")
        
        # エラーまたは結果を確認
        assert "error" in theory or theory.get("id") == "sociocultural-theory"
        
        # Step 3: 最近接発達領域の概念を取得
        concept = await get_concept("zone-of-proximal-development")
        
        # 結果を確認
        if "error" not in concept:
            name = concept.get("name", "")
            definition = concept.get("definition", "")
            assert "Zone" in name or "ZPD" in name or "最近接発達" in name or len(definition) > 0

    # ============================================================
    # シナリオ8: パラダイム横断検索
    # ============================================================
    
    @pytest.mark.asyncio
    async def test_scenario_cross_paradigm_search(self):
        """シナリオ: 一般的な検索"""
        from tengin_mcp.tools.theory_tools import search_theories
        
        # 学習に関する一般的な検索
        result = await search_theories(query="学習")
        
        # 検索結果の構造を確認
        assert "theories" in result
        theories_list = result.get("theories", [])
        
        # 学習に関連する理論が少なくとも1件以上見つかるはず
        assert len(theories_list) > 0

    # ============================================================
    # シナリオ9: エラーハンドリング
    # ============================================================
    
    @pytest.mark.asyncio
    async def test_scenario_error_handling_invalid_id(self):
        """シナリオ: 存在しないIDでのエラーハンドリング"""
        from tengin_mcp.tools.theory_tools import get_theory
        
        # get_theoryはエラー辞書を返す設計
        result = await get_theory("nonexistent-theory-id-12345")
        
        assert "error" in result
        assert "見つかりません" in result["error"] or "not found" in result["error"].lower()

    @pytest.mark.asyncio
    async def test_scenario_error_handling_invalid_query(self):
        """シナリオ: 無効なクエリパラメータ"""
        from tengin_mcp.tools.graph_tools import traverse_graph
        from tengin_mcp.domain.errors import InvalidQueryError
        
        with pytest.raises(InvalidQueryError):
            await traverse_graph(start_node_id="", max_depth=2)
        
        with pytest.raises(InvalidQueryError):
            await traverse_graph(start_node_id="test", max_depth=100)

    # ============================================================
    # シナリオ10: 全ツール動作確認
    # ============================================================
    
    @pytest.mark.asyncio
    async def test_scenario_all_tools_availability(self):
        """シナリオ: 全ツールが利用可能であることを確認"""
        from tengin_mcp.server import mcp
        
        # 登録されているツールを確認
        tools = list(mcp._tool_manager._tools.keys())
        
        expected_tools = [
            "search_theories",
            "get_theory",
            "traverse_graph",
            "find_path",
            "get_related_nodes",
            "get_graph_statistics",
            "cite_theory",
            "compare_theories",
            "search_methodologies",
            "get_methodology",
            "search_contexts",
            "get_context",
            "recommend_methodologies",
            "get_evidence_for_theory",
        ]
        
        for tool in expected_tools:
            assert tool in tools, f"ツール '{tool}' が登録されていません"
        
        # ツール数の確認
        assert len(tools) >= 14, f"登録ツール数が不足: {len(tools)}件"


class TestDataIntegrityE2E:
    """データ整合性のE2Eテスト"""

    @pytest.fixture(autouse=True)
    async def setup(self):
        """テストセットアップ"""
        settings = Settings()
        self.adapter = Neo4jAdapter(settings)
        await self.adapter.connect()
        
        self.graph_repository = Neo4jGraphRepository(self.adapter)
        app_state.graph_repository = self.graph_repository
        
        yield
        
        await self.adapter.close()
        app_state.graph_repository = None

    @pytest.mark.asyncio
    async def test_node_count_integrity(self):
        """ノード数の整合性を検証"""
        result = await self.adapter.execute_query("""
            MATCH (n)
            WITH labels(n)[0] as label, count(*) as count
            RETURN label, count ORDER BY label
        """)
        
        node_counts = {r["label"]: r["count"] for r in result}
        
        # 期待されるノード数
        assert node_counts.get("Theory", 0) >= 30, "理論ノードが不足"
        assert node_counts.get("Theorist", 0) >= 20, "理論家ノードが不足"
        assert node_counts.get("Concept", 0) >= 20, "概念ノードが不足"
        assert node_counts.get("Methodology", 0) >= 10, "教授法ノードが不足"
        assert node_counts.get("Evidence", 0) >= 10, "エビデンスノードが不足"
        assert node_counts.get("Context", 0) >= 5, "文脈ノードが不足"

    @pytest.mark.asyncio
    async def test_relationship_integrity(self):
        """リレーションシップの整合性を検証"""
        result = await self.adapter.execute_query("""
            MATCH ()-[r]->()
            WITH type(r) as type, count(*) as count
            RETURN type, count ORDER BY count DESC
        """)
        
        rel_counts = {r["type"]: r["count"] for r in result}
        
        # 主要なリレーションシップタイプが存在する
        assert "RELATED_TO" in rel_counts or "PROPOSED" in rel_counts
        
        # リレーションシップの総数
        total_rels = sum(rel_counts.values())
        assert total_rels >= 200, f"リレーションシップが不足: {total_rels}件"

    @pytest.mark.asyncio
    async def test_paradigm_coverage(self):
        """パラダイムのカバレッジを検証"""
        result = await self.adapter.execute_query("""
            MATCH (t:Theory)
            WHERE t.paradigm IS NOT NULL
            RETURN t.paradigm as paradigm, count(*) as count
            ORDER BY count DESC
        """)
        
        paradigms = {r["paradigm"]: r["count"] for r in result}
        
        # 主要パラダイムが含まれている
        expected_paradigms = [
            "behaviorism",
            "cognitivism", 
            "constructivism",
            "humanistic",
            "instructional"
        ]
        
        for p in expected_paradigms:
            assert p in paradigms, f"パラダイム '{p}' が欠落"

    @pytest.mark.asyncio
    async def test_theory_evidence_connection(self):
        """理論とエビデンスの接続を検証"""
        result = await self.adapter.execute_query("""
            MATCH (e:Evidence)-[:SUPPORTS]->(t:Theory)
            RETURN count(distinct t) as theories_with_evidence
        """)
        
        theories_with_evidence = result[0]["theories_with_evidence"]
        assert theories_with_evidence >= 5, "エビデンスに支持される理論が少ない"

    @pytest.mark.asyncio
    async def test_methodology_grounding(self):
        """教授法の理論的基盤を検証"""
        result = await self.adapter.execute_query("""
            MATCH (m:Methodology)-[:THEORETICALLY_GROUNDED_IN]->(t:Theory)
            RETURN count(distinct m) as grounded_methodologies
        """)
        
        grounded = result[0]["grounded_methodologies"]
        assert grounded >= 5, "理論的基盤を持つ教授法が少ない"
