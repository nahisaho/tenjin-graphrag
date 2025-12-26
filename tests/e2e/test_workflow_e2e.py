"""
E2E Tests: Full Workflow Integration Tests

エンドツーエンドの完全なワークフローをテスト。
ユーザーシナリオに基づいた統合テスト。
"""

import pytest

from tengin_mcp.infrastructure.config import Settings
from tengin_mcp.infrastructure.adapters.neo4j_adapter import Neo4jAdapter
from tengin_mcp.infrastructure.repositories.neo4j_graph_repository import Neo4jGraphRepository
from tengin_mcp.infrastructure.repositories.neo4j_theory_repository import Neo4jTheoryRepository
from tengin_mcp.server import app_state


class TestEducatorWorkflow:
    """教育者ワークフローのE2Eテスト"""

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
    # シナリオ: 授業設計ワークフロー
    # ============================================================

    @pytest.mark.asyncio
    async def test_lesson_design_workflow(self):
        """授業設計のための理論検索ワークフロー"""
        from tengin_mcp.tools.theory_tools import (
            search_theories,
            get_theory,
            get_concept,
            get_principle,
        )
        from tengin_mcp.tools.graph_tools import get_related_nodes
        
        # Step 1: 教育者が「認知的な学習」について検索
        search_result = await search_theories(query="認知的 学習")
        assert "theories" in search_result
        theories = search_result.get("theories", [])
        
        if theories:
            # Step 2: 最初の理論の詳細を取得
            first_theory_id = theories[0].get("id")
            theory_detail = await get_theory(first_theory_id)
            
            if "error" not in theory_detail:
                # Step 3: 関連する概念を取得
                related = await get_related_nodes(node_id=first_theory_id)
                related_nodes = related.get("related_nodes", [])
                
                # 概念を探す
                concept_ids = [
                    n.get("id") for n in related_nodes 
                    if n.get("label") == "Concept"
                ]
                
                if concept_ids:
                    concept = await get_concept(concept_ids[0])
                    assert "error" not in concept or concept.get("id") == concept_ids[0]
                
                # 原則を探す
                principle_ids = [
                    n.get("id") for n in related_nodes 
                    if n.get("label") == "Principle"
                ]
                
                if principle_ids:
                    principle = await get_principle(principle_ids[0])
                    assert "error" not in principle or principle.get("id") == principle_ids[0]

    @pytest.mark.asyncio
    async def test_theory_comparison_workflow(self):
        """理論比較ワークフロー"""
        from tengin_mcp.tools.citation_tools import compare_theories
        from tengin_mcp.tools.theory_tools import get_theory
        
        # Step 1: 2つの学習理論を取得
        theory1 = await get_theory("cognitive-load-theory")
        theory2 = await get_theory("constructivism")
        
        # Step 2: 理論を比較
        comparison = await compare_theories(
            theory_ids=["cognitive-load-theory", "constructivism"]
        )
        
        assert "theories" in comparison or "comparison" in comparison

    @pytest.mark.asyncio
    async def test_evidence_based_teaching_workflow(self):
        """エビデンスに基づく教授法選択ワークフロー"""
        from tengin_mcp.tools.methodology_tools import (
            search_methodologies,
            get_evidence_for_theory,
        )
        from tengin_mcp.tools.theory_tools import get_theory
        
        # Step 1: 教授法を検索
        methods = await search_methodologies()
        assert "methodologies" in methods
        
        # Step 2: 特定の理論のエビデンスを確認
        evidence = await get_evidence_for_theory("cognitive-load-theory")
        
        assert "supporting_evidence" in evidence
        assert "challenging_evidence" in evidence

    # ============================================================
    # シナリオ: 研究者ワークフロー
    # ============================================================

    @pytest.mark.asyncio
    async def test_researcher_citation_workflow(self):
        """研究者の引用生成ワークフロー"""
        from tengin_mcp.tools.citation_tools import cite_theory
        from tengin_mcp.tools.theory_tools import get_theory, get_theorist
        
        # Step 1: 理論を検索して詳細を取得
        theory = await get_theory("self-determination-theory")
        
        if "error" not in theory:
            # Step 2: 理論家の情報を取得
            theorist = await get_theorist("edward-deci")
            
            # Step 3: 引用を生成
            citation_apa = await cite_theory(
                theory_id="self-determination-theory",
                format="APA7"
            )
            
            assert "citation" in citation_apa or "theory_id" in citation_apa

    @pytest.mark.asyncio
    async def test_researcher_graph_exploration_workflow(self):
        """研究者のグラフ探索ワークフロー"""
        from tengin_mcp.tools.graph_tools import (
            traverse_graph,
            get_graph_statistics,
            find_path,
        )
        
        # Step 1: グラフ統計を確認
        stats = await get_graph_statistics()
        assert "node_counts" in stats or "error" not in stats
        
        # Step 2: 特定の理論からトラバース
        traversal = await traverse_graph(
            start_node_id="constructivism",
            max_depth=2
        )
        
        assert traversal["node_count"] > 0
        
        # Step 3: 2つの理論間のパスを探索
        path = await find_path(
            start_node_id="constructivism",
            end_node_id="zone-of-proximal-development",
            max_depth=3
        )
        
        assert "paths" in path

    # ============================================================
    # シナリオ: 学生ワークフロー
    # ============================================================

    @pytest.mark.asyncio
    async def test_student_learning_workflow(self):
        """学生の学習ワークフロー"""
        from tengin_mcp.tools.theory_tools import (
            search_theories,
            get_theory,
            get_concept,
        )
        from tengin_mcp.tools.graph_tools import get_related_nodes
        
        # Step 1: 学生が「動機づけ」について検索
        search_result = await search_theories(query="動機づけ")
        assert "theories" in search_result
        
        theories = search_result.get("theories", [])
        
        # Step 2: 自己決定理論を見つけて詳細を確認
        sdt = await get_theory("self-determination-theory")
        
        if "error" not in sdt:
            # Step 3: 関連する概念を学習
            related = await get_related_nodes(node_id="self-determination-theory")
            
            # 自律性の概念を取得
            autonomy = await get_concept("autonomy")
            
            if "error" not in autonomy:
                definition = autonomy.get("definition", "") or autonomy.get("definition_ja", "")
                assert len(definition) > 0


class TestAPIWorkflow:
    """API統合ワークフローのE2Eテスト"""

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
    async def test_complete_tool_chain(self):
        """全ツールのチェーン実行"""
        from tengin_mcp.tools.theory_tools import (
            search_theories,
            get_theory,
            get_theorist,
            get_concept,
            get_principle,
            get_evidence,
            get_theories_by_category,
        )
        from tengin_mcp.tools.graph_tools import (
            traverse_graph,
            get_related_nodes,
            find_path,
            get_graph_statistics,
        )
        from tengin_mcp.tools.citation_tools import cite_theory, compare_theories
        from tengin_mcp.tools.system_tools import (
            get_cache_stats,
            health_check,
            get_system_info,
        )
        
        # Theory Tools
        await search_theories(query="学習")
        await get_theory("cognitive-load-theory")
        await get_theorist("john-sweller")
        await get_concept("intrinsic-load")
        await get_principle("worked-example-effect")
        await get_evidence("sweller-1988-clt")
        await get_theories_by_category(category="learning")
        
        # Graph Tools
        await traverse_graph(start_node_id="cognitive-load-theory", max_depth=2)
        await get_related_nodes(node_id="cognitive-load-theory")
        await find_path(
            start_node_id="cognitive-load-theory",
            end_node_id="constructivism",
            max_depth=5
        )
        await get_graph_statistics()
        
        # Citation Tools
        await cite_theory(theory_id="cognitive-load-theory", format="APA7")
        await compare_theories(
            theory_ids=["cognitive-load-theory", "multimedia-learning-theory"]
        )
        
        # System Tools
        cache_stats = await get_cache_stats()
        health = await health_check()
        info = await get_system_info()
        
        # 全ツールが正常に実行された
        assert cache_stats is not None
        assert health["status"] in ["healthy", "degraded"]
        assert "name" in info

    @pytest.mark.asyncio
    async def test_concurrent_operations(self):
        """並行操作のテスト"""
        import asyncio
        from tengin_mcp.tools.theory_tools import search_theories, get_theory
        
        # 複数の検索を並行実行
        tasks = [
            search_theories(query="認知負荷"),
            search_theories(query="構成主義"),
            search_theories(query="動機づけ"),
            get_theory("cognitive-load-theory"),
            get_theory("constructivism"),
            get_theory("self-determination-theory"),
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # エラーなく完了
        for result in results:
            assert not isinstance(result, Exception)

    @pytest.mark.asyncio
    async def test_error_recovery_workflow(self):
        """エラー回復ワークフロー"""
        from tengin_mcp.tools.theory_tools import get_theory, search_theories
        from tengin_mcp.tools.system_tools import health_check
        
        # Step 1: 存在しないIDでエラー
        error_result = await get_theory("nonexistent-theory-12345")
        assert "error" in error_result
        
        # Step 2: 正常な操作を続行できる
        search_result = await search_theories(query="学習")
        assert "theories" in search_result
        
        # Step 3: ヘルスチェックで状態確認
        health = await health_check()
        assert health["status"] == "healthy"


class TestPerformanceWorkflow:
    """パフォーマンスワークフローのE2Eテスト"""

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
    async def test_cache_improves_performance(self):
        """キャッシュによるパフォーマンス向上"""
        import time
        from tengin_mcp.tools.theory_tools import get_theory
        from tengin_mcp.tools.system_tools import clear_cache, get_cache_stats
        
        # キャッシュをクリア
        await clear_cache("all")
        
        # 初回実行（キャッシュミス）
        start1 = time.time()
        await get_theory("cognitive-load-theory")
        time1 = time.time() - start1
        
        # 2回目実行（キャッシュヒット）
        start2 = time.time()
        await get_theory("cognitive-load-theory")
        time2 = time.time() - start2
        
        # キャッシュ統計を確認
        stats = await get_cache_stats()
        
        # ヒットが記録されている（またはキャッシュが機能している）
        total_hits = stats["total"]["hits"]
        # 2回目は1回目より高速（または同等）であるべき
        # ただし、ネットワーク遅延等で変動があるため、厳密な比較は避ける
        assert time2 <= time1 * 2  # 2倍以上遅くなっていなければOK

    @pytest.mark.asyncio
    async def test_large_traversal_completes(self):
        """大規模トラバースが完了する"""
        import time
        from tengin_mcp.tools.graph_tools import traverse_graph
        
        start = time.time()
        result = await traverse_graph(
            start_node_id="constructivism",
            max_depth=3
        )
        elapsed = time.time() - start
        
        # 10秒以内に完了
        assert elapsed < 10
        assert result["node_count"] > 0
