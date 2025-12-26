"""
E2E Tests: System Tools Integration Tests

システム管理ツールの統合テスト。
キャッシュ管理、ヘルスチェック、システム情報取得を検証。
"""

import pytest

from tengin_mcp.infrastructure.config import Settings
from tengin_mcp.infrastructure.adapters.neo4j_adapter import Neo4jAdapter
from tengin_mcp.infrastructure.repositories.neo4j_graph_repository import Neo4jGraphRepository
from tengin_mcp.infrastructure.repositories.neo4j_theory_repository import Neo4jTheoryRepository
from tengin_mcp.server import app_state


class TestSystemToolsE2E:
    """システムツールのE2Eテスト"""

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
    # キャッシュ統計テスト
    # ============================================================

    @pytest.mark.asyncio
    async def test_get_cache_stats(self):
        """キャッシュ統計情報を取得できる"""
        from tengin_mcp.tools.system_tools import get_cache_stats
        
        stats = await get_cache_stats()
        
        # 必須フィールドの存在確認
        assert "theory_cache" in stats
        assert "graph_cache" in stats
        assert "total" in stats
        
        # theory_cache の構造確認
        theory_cache = stats["theory_cache"]
        assert "hits" in theory_cache
        assert "misses" in theory_cache
        assert "hit_rate" in theory_cache
        assert "size" in theory_cache
        
        # graph_cache の構造確認
        graph_cache = stats["graph_cache"]
        assert "hits" in graph_cache
        assert "misses" in graph_cache
        assert "hit_rate" in graph_cache
        assert "size" in graph_cache
        
        # total の構造確認
        total = stats["total"]
        assert "hits" in total
        assert "misses" in total
        assert "hit_rate" in total

    @pytest.mark.asyncio
    async def test_cache_stats_after_operations(self):
        """操作後のキャッシュ統計更新を確認"""
        from tengin_mcp.tools.system_tools import get_cache_stats, clear_cache
        from tengin_mcp.tools.theory_tools import search_theories
        
        # キャッシュをクリア
        await clear_cache("all")
        
        # 初期統計を取得
        initial_stats = await get_cache_stats()
        initial_total = initial_stats["total"]["hits"] + initial_stats["total"]["misses"]
        
        # 検索を実行（キャッシュミス発生）
        await search_theories(query="認知負荷")
        
        # 統計を再取得
        after_stats = await get_cache_stats()
        after_total = after_stats["total"]["hits"] + after_stats["total"]["misses"]
        
        # 何らかの操作が記録されている（ミスまたはヒット）
        assert after_total >= initial_total

    # ============================================================
    # キャッシュクリアテスト
    # ============================================================

    @pytest.mark.asyncio
    async def test_clear_all_cache(self):
        """全キャッシュをクリアできる"""
        from tengin_mcp.tools.system_tools import clear_cache
        
        result = await clear_cache()
        
        assert result["cleared"] == "all"
        assert "message" in result

    @pytest.mark.asyncio
    async def test_clear_theory_cache(self):
        """Theoryキャッシュのみクリアできる"""
        from tengin_mcp.tools.system_tools import clear_cache
        
        result = await clear_cache("theory")
        
        assert result["cleared"] == "theory"
        assert "message" in result

    @pytest.mark.asyncio
    async def test_clear_graph_cache(self):
        """Graphキャッシュのみクリアできる"""
        from tengin_mcp.tools.system_tools import clear_cache
        
        result = await clear_cache("graph")
        
        assert result["cleared"] == "graph"
        assert "message" in result

    # ============================================================
    # ヘルスチェックテスト
    # ============================================================

    @pytest.mark.asyncio
    async def test_health_check_returns_status(self):
        """ヘルスチェックがステータスを返す"""
        from tengin_mcp.tools.system_tools import health_check
        
        status = await health_check()
        
        assert "status" in status
        assert status["status"] in ["healthy", "degraded", "unhealthy"]
        assert "components" in status

    @pytest.mark.asyncio
    async def test_health_check_components(self):
        """ヘルスチェックが全コンポーネントを検証"""
        from tengin_mcp.tools.system_tools import health_check
        
        status = await health_check()
        components = status["components"]
        
        # 必須コンポーネントの存在確認
        assert "theory_repository" in components
        assert "graph_repository" in components
        assert "cache" in components
        
        # theory_repository の検証
        theory_repo = components["theory_repository"]
        assert "status" in theory_repo
        if theory_repo["status"] == "healthy":
            assert "theory_count" in theory_repo
            assert theory_repo["theory_count"] > 0
        
        # graph_repository の検証
        graph_repo = components["graph_repository"]
        assert "status" in graph_repo
        if graph_repo["status"] == "healthy":
            assert "node_count" in graph_repo
            assert "relationship_count" in graph_repo
        
        # cache の検証
        cache = components["cache"]
        assert cache["status"] == "healthy"
        assert "theory_cache_size" in cache
        assert "graph_cache_size" in cache

    @pytest.mark.asyncio
    async def test_health_check_healthy_status(self):
        """正常接続時にhealthyステータスを返す"""
        from tengin_mcp.tools.system_tools import health_check
        
        status = await health_check()
        
        # 正しく接続されていればhealthy
        assert status["status"] == "healthy"

    # ============================================================
    # システム情報テスト
    # ============================================================

    @pytest.mark.asyncio
    async def test_get_system_info(self):
        """システム情報を取得できる"""
        from tengin_mcp.tools.system_tools import get_system_info
        
        info = await get_system_info()
        
        # 基本情報の存在確認
        assert "name" in info
        assert "version" in info
        assert "mcp_version" in info
        assert "features" in info
        assert "capabilities" in info

    @pytest.mark.asyncio
    async def test_system_info_features(self):
        """システム情報のfeatures構造を確認"""
        from tengin_mcp.tools.system_tools import get_system_info
        
        info = await get_system_info()
        features = info["features"]
        
        assert "tools" in features
        assert "resources" in features
        assert "prompts" in features
        
        # 機能数が妥当
        assert features["tools"] >= 10
        assert features["resources"] >= 1
        assert features["prompts"] >= 1

    @pytest.mark.asyncio
    async def test_system_info_capabilities(self):
        """システム情報のcapabilities確認"""
        from tengin_mcp.tools.system_tools import get_system_info
        
        info = await get_system_info()
        capabilities = info["capabilities"]
        
        # 主要機能が含まれる
        expected_capabilities = [
            "theory_search",
            "graph_traversal",
            "citation_generation",
        ]
        
        for cap in expected_capabilities:
            assert cap in capabilities

    @pytest.mark.asyncio
    async def test_system_info_supported_categories(self):
        """サポートされるカテゴリ確認"""
        from tengin_mcp.tools.system_tools import get_system_info
        
        info = await get_system_info()
        categories = info["supported_categories"]
        
        # 主要カテゴリが含まれる
        expected_categories = ["learning", "instructional", "motivation"]
        
        for cat in expected_categories:
            assert cat in categories

    @pytest.mark.asyncio
    async def test_system_info_citation_formats(self):
        """サポートされる引用形式確認"""
        from tengin_mcp.tools.system_tools import get_system_info
        
        info = await get_system_info()
        formats = info["supported_citation_formats"]
        
        # 主要形式が含まれる
        expected_formats = ["APA7", "MLA9", "Chicago"]
        
        for fmt in expected_formats:
            assert fmt in formats


class TestSystemToolsEdgeCases:
    """システムツールのエッジケーステスト"""

    @pytest.mark.asyncio
    async def test_health_check_without_repositories(self):
        """リポジトリ未設定時のヘルスチェック"""
        from tengin_mcp.tools.system_tools import health_check
        
        # リポジトリを一時的にクリア
        original_theory = app_state.theory_repository
        original_graph = app_state.graph_repository
        
        app_state.theory_repository = None
        app_state.graph_repository = None
        
        try:
            status = await health_check()
            
            # not_initialized ステータスが返る
            assert status["components"]["theory_repository"]["status"] == "not_initialized"
            assert status["components"]["graph_repository"]["status"] == "not_initialized"
        finally:
            # 元に戻す
            app_state.theory_repository = original_theory
            app_state.graph_repository = original_graph

    @pytest.mark.asyncio
    async def test_cache_stats_type_validation(self):
        """キャッシュ統計の型検証"""
        from tengin_mcp.tools.system_tools import get_cache_stats
        
        stats = await get_cache_stats()
        
        # 数値型の検証
        assert isinstance(stats["theory_cache"]["hits"], int)
        assert isinstance(stats["theory_cache"]["misses"], int)
        assert isinstance(stats["theory_cache"]["hit_rate"], (int, float))
        assert isinstance(stats["theory_cache"]["size"], int)

    @pytest.mark.asyncio
    async def test_clear_cache_invalid_type(self):
        """無効なキャッシュタイプ指定"""
        from tengin_mcp.tools.system_tools import clear_cache
        
        # 無効なタイプはallとして扱われる
        result = await clear_cache("invalid_type")
        
        assert result["cleared"] == "all"
