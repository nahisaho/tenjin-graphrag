"""Unit tests for system_tools."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest


class TestGetCacheStats:
    """get_cache_stats のテスト。"""

    @pytest.mark.asyncio
    async def test_get_cache_stats(self) -> None:
        """キャッシュ統計取得のテスト。"""
        from tengin_mcp.tools.system_tools import get_cache_stats

        result = await get_cache_stats()

        assert "theory_cache" in result
        assert "graph_cache" in result
        assert "total" in result
        assert "hits" in result["theory_cache"]
        assert "misses" in result["theory_cache"]
        assert "hit_rate" in result["theory_cache"]


class TestClearCache:
    """clear_cache のテスト。"""

    @pytest.mark.asyncio
    async def test_clear_all_cache(self) -> None:
        """全キャッシュクリアのテスト。"""
        from tengin_mcp.tools.system_tools import clear_cache

        result = await clear_cache()
        assert result["cleared"] == "all"

    @pytest.mark.asyncio
    async def test_clear_theory_cache(self) -> None:
        """Theory キャッシュクリアのテスト。"""
        from tengin_mcp.tools.system_tools import clear_cache

        result = await clear_cache("theory")
        assert result["cleared"] == "theory"

    @pytest.mark.asyncio
    async def test_clear_graph_cache(self) -> None:
        """Graph キャッシュクリアのテスト。"""
        from tengin_mcp.tools.system_tools import clear_cache

        result = await clear_cache("graph")
        assert result["cleared"] == "graph"


class TestHealthCheck:
    """health_check のテスト。"""

    @pytest.mark.asyncio
    async def test_health_check_not_initialized(self) -> None:
        """初期化前のヘルスチェック。"""
        from tengin_mcp.tools.system_tools import health_check

        with patch("tengin_mcp.tools.system_tools.app_state") as mock_state:
            mock_state.theory_repository = None
            mock_state.graph_repository = None
            mock_state.vector_repository = None

            result = await health_check()

            assert result["status"] == "healthy"
            assert "components" in result
            assert result["components"]["theory_repository"]["status"] == "not_initialized"
            assert result["components"]["graph_repository"]["status"] == "not_initialized"
            assert result["components"]["vector_repository"]["status"] == "not_initialized"

    @pytest.mark.asyncio
    async def test_health_check_healthy(self) -> None:
        """正常なヘルスチェック。"""
        from tengin_mcp.tools.system_tools import health_check

        with patch("tengin_mcp.tools.system_tools.app_state") as mock_state:
            # Theory Repository
            mock_theory_repo = AsyncMock()
            mock_theory_repo.get_all.return_value = [MagicMock(), MagicMock()]
            mock_state.theory_repository = mock_theory_repo

            # Graph Repository
            mock_graph_repo = AsyncMock()
            mock_graph_repo.get_statistics.return_value = {
                "total_nodes": 100,
                "total_relationships": 200,
            }
            mock_state.graph_repository = mock_graph_repo

            # Vector Repository
            mock_state.vector_repository = MagicMock()

            result = await health_check()

            assert result["status"] == "healthy"
            assert result["components"]["theory_repository"]["status"] == "healthy"
            assert result["components"]["theory_repository"]["theory_count"] == 2
            assert result["components"]["graph_repository"]["status"] == "healthy"
            assert result["components"]["graph_repository"]["node_count"] == 100
            assert result["components"]["vector_repository"]["status"] == "healthy"

    @pytest.mark.asyncio
    async def test_health_check_degraded(self) -> None:
        """劣化状態のヘルスチェック。"""
        from tengin_mcp.tools.system_tools import health_check

        with patch("tengin_mcp.tools.system_tools.app_state") as mock_state:
            # Theory Repository が例外を投げる
            mock_theory_repo = AsyncMock()
            mock_theory_repo.get_all.side_effect = Exception("Connection failed")
            mock_state.theory_repository = mock_theory_repo

            mock_state.graph_repository = None
            mock_state.vector_repository = None

            result = await health_check()

            assert result["status"] == "degraded"
            assert result["components"]["theory_repository"]["status"] == "unhealthy"
            assert "Connection failed" in result["components"]["theory_repository"]["error"]


class TestGetSystemInfo:
    """get_system_info のテスト。"""

    @pytest.mark.asyncio
    async def test_get_system_info(self) -> None:
        """システム情報取得のテスト。"""
        from tengin_mcp.tools.system_tools import get_system_info

        result = await get_system_info()

        assert result["name"] == "TENGIN Education Theory MCP Server"
        assert "version" in result
        assert "features" in result
        assert "capabilities" in result
        assert "supported_categories" in result
        assert "supported_evidence_levels" in result
        assert "supported_citation_formats" in result

    @pytest.mark.asyncio
    async def test_system_info_features_count(self) -> None:
        """機能数の確認。"""
        from tengin_mcp.tools.system_tools import get_system_info

        result = await get_system_info()

        assert result["features"]["tools"] == 23
        assert result["features"]["resources"] == 5
        assert result["features"]["prompts"] == 3
