"""Integration Tests: graph_tools - グラフツール統合テスト"""

import pytest

from tengin_mcp.domain.errors import InvalidQueryError
from tengin_mcp.server import app_state
from tengin_mcp.infrastructure.config import Settings
from tengin_mcp.infrastructure.adapters.neo4j_adapter import Neo4jAdapter
from tengin_mcp.infrastructure.repositories.neo4j_graph_repository import (
    Neo4jGraphRepository,
)


@pytest.fixture
async def setup_graph_tools():
    """グラフツール用のセットアップ"""
    settings = Settings()
    adapter = Neo4jAdapter(settings)
    await adapter.connect()

    repository = Neo4jGraphRepository(adapter)
    app_state.graph_repository = repository

    yield adapter

    await adapter.close()
    app_state.graph_repository = None


class TestTraverseGraphTool:
    """traverse_graph ツールのテスト"""

    @pytest.mark.asyncio
    async def test_traverse_graph_basic(self, setup_graph_tools):
        """基本的なグラフトラバース"""
        from tengin_mcp.tools.graph_tools import traverse_graph

        result = await traverse_graph(start_node_id="cognitive-load-theory")

        assert "error" not in result
        assert "nodes" in result
        assert "relationships" in result
        assert result["start_node_id"] == "cognitive-load-theory"

    @pytest.mark.asyncio
    async def test_traverse_graph_with_depth(self, setup_graph_tools):
        """深度指定でのトラバース"""
        from tengin_mcp.tools.graph_tools import traverse_graph

        result = await traverse_graph(
            start_node_id="cognitive-load-theory",
            max_depth=1,
        )

        assert "error" not in result
        assert result["max_depth"] == 1

    @pytest.mark.asyncio
    async def test_traverse_graph_with_direction_outgoing(self, setup_graph_tools):
        """出方向でのトラバース"""
        from tengin_mcp.tools.graph_tools import traverse_graph

        result = await traverse_graph(
            start_node_id="cognitive-load-theory",
            direction="outgoing",
            max_depth=2,
        )

        assert "error" not in result
        assert result["direction"] == "outgoing"

    @pytest.mark.asyncio
    async def test_traverse_graph_with_direction_incoming(self, setup_graph_tools):
        """入方向でのトラバース"""
        from tengin_mcp.tools.graph_tools import traverse_graph

        result = await traverse_graph(
            start_node_id="cognitive-load-theory",
            direction="incoming",
            max_depth=2,
        )

        assert "error" not in result
        assert result["direction"] == "incoming"

    @pytest.mark.asyncio
    async def test_traverse_graph_with_relationship_types(self, setup_graph_tools):
        """リレーションシップタイプ指定でのトラバース"""
        from tengin_mcp.tools.graph_tools import traverse_graph

        result = await traverse_graph(
            start_node_id="cognitive-load-theory",
            relationship_types=["INCLUDES_CONCEPT"],
            max_depth=1,
        )

        assert "error" not in result

    @pytest.mark.asyncio
    async def test_traverse_graph_invalid_node_id(self, setup_graph_tools):
        """無効なノードIDでのエラー"""
        from tengin_mcp.tools.graph_tools import traverse_graph

        with pytest.raises(InvalidQueryError):
            await traverse_graph(start_node_id="")

    @pytest.mark.asyncio
    async def test_traverse_graph_invalid_depth_low(self, setup_graph_tools):
        """深度が小さすぎる場合のエラー"""
        from tengin_mcp.tools.graph_tools import traverse_graph

        with pytest.raises(InvalidQueryError):
            await traverse_graph(
                start_node_id="cognitive-load-theory",
                max_depth=0,
            )

    @pytest.mark.asyncio
    async def test_traverse_graph_invalid_depth_high(self, setup_graph_tools):
        """深度が大きすぎる場合のエラー"""
        from tengin_mcp.tools.graph_tools import traverse_graph

        with pytest.raises(InvalidQueryError):
            await traverse_graph(
                start_node_id="cognitive-load-theory",
                max_depth=11,
            )

    @pytest.mark.asyncio
    async def test_traverse_graph_invalid_direction(self, setup_graph_tools):
        """無効な方向指定でのエラー"""
        from tengin_mcp.tools.graph_tools import traverse_graph

        with pytest.raises(InvalidQueryError):
            await traverse_graph(
                start_node_id="cognitive-load-theory",
                direction="invalid",
            )

    @pytest.mark.asyncio
    async def test_traverse_graph_no_repository(self):
        """リポジトリなしでのトラバース"""
        from tengin_mcp.tools.graph_tools import traverse_graph

        app_state.graph_repository = None
        result = await traverse_graph(start_node_id="cognitive-load-theory")

        assert "error" in result


class TestFindPathTool:
    """find_path ツールのテスト"""

    @pytest.mark.asyncio
    async def test_find_path_basic(self, setup_graph_tools):
        """基本的なパス検索"""
        from tengin_mcp.tools.graph_tools import find_path

        result = await find_path(
            start_node_id="cognitive-load-theory",
            end_node_id="multimedia-learning-theory",
        )

        assert "error" not in result
        assert result["start_node_id"] == "cognitive-load-theory"
        assert result["end_node_id"] == "multimedia-learning-theory"

    @pytest.mark.asyncio
    async def test_find_path_with_depth(self, setup_graph_tools):
        """深度指定でのパス検索"""
        from tengin_mcp.tools.graph_tools import find_path

        result = await find_path(
            start_node_id="cognitive-load-theory",
            end_node_id="multimedia-learning-theory",
            max_depth=3,
        )

        assert "error" not in result

    @pytest.mark.asyncio
    async def test_find_path_invalid_start(self, setup_graph_tools):
        """開始ノードIDがない場合のエラー"""
        from tengin_mcp.tools.graph_tools import find_path

        with pytest.raises(InvalidQueryError):
            await find_path(start_node_id="", end_node_id="multimedia-learning-theory")

    @pytest.mark.asyncio
    async def test_find_path_invalid_end(self, setup_graph_tools):
        """終了ノードIDがない場合のエラー"""
        from tengin_mcp.tools.graph_tools import find_path

        with pytest.raises(InvalidQueryError):
            await find_path(start_node_id="cognitive-load-theory", end_node_id="")

    @pytest.mark.asyncio
    async def test_find_path_same_node(self, setup_graph_tools):
        """同じノード指定でのエラー"""
        from tengin_mcp.tools.graph_tools import find_path

        with pytest.raises(InvalidQueryError):
            await find_path(
                start_node_id="cognitive-load-theory",
                end_node_id="cognitive-load-theory",
            )

    @pytest.mark.asyncio
    async def test_find_path_invalid_depth_low(self, setup_graph_tools):
        """深度が小さすぎる場合のエラー"""
        from tengin_mcp.tools.graph_tools import find_path

        with pytest.raises(InvalidQueryError):
            await find_path(
                start_node_id="cognitive-load-theory",
                end_node_id="multimedia-learning-theory",
                max_depth=0,
            )

    @pytest.mark.asyncio
    async def test_find_path_invalid_depth_high(self, setup_graph_tools):
        """深度が大きすぎる場合のエラー"""
        from tengin_mcp.tools.graph_tools import find_path

        with pytest.raises(InvalidQueryError):
            await find_path(
                start_node_id="cognitive-load-theory",
                end_node_id="multimedia-learning-theory",
                max_depth=11,
            )

    @pytest.mark.asyncio
    async def test_find_path_no_repository(self):
        """リポジトリなしでのパス検索"""
        from tengin_mcp.tools.graph_tools import find_path

        app_state.graph_repository = None
        result = await find_path(
            start_node_id="cognitive-load-theory",
            end_node_id="multimedia-learning-theory",
        )

        assert "error" in result


class TestGetRelatedNodesTool:
    """get_related_nodes ツールのテスト"""

    @pytest.mark.asyncio
    async def test_get_related_nodes_basic(self, setup_graph_tools):
        """基本的な関連ノード取得"""
        from tengin_mcp.tools.graph_tools import get_related_nodes

        result = await get_related_nodes(node_id="cognitive-load-theory")

        assert "error" not in result
        assert "related_nodes" in result
        assert result["node_id"] == "cognitive-load-theory"

    @pytest.mark.asyncio
    async def test_get_related_nodes_with_relationship_type(self, setup_graph_tools):
        """リレーションシップタイプ指定での関連ノード取得"""
        from tengin_mcp.tools.graph_tools import get_related_nodes

        result = await get_related_nodes(
            node_id="cognitive-load-theory",
            relationship_type="INCLUDES_CONCEPT",
        )

        assert "error" not in result
        assert result["relationship_type"] == "INCLUDES_CONCEPT"

    @pytest.mark.asyncio
    async def test_get_related_nodes_with_node_type(self, setup_graph_tools):
        """ノードタイプ指定での関連ノード取得"""
        from tengin_mcp.tools.graph_tools import get_related_nodes

        result = await get_related_nodes(
            node_id="cognitive-load-theory",
            node_type="Concept",
        )

        assert "error" not in result
        assert result["node_type"] == "Concept"

    @pytest.mark.asyncio
    async def test_get_related_nodes_invalid_id(self, setup_graph_tools):
        """無効なノードIDでのエラー"""
        from tengin_mcp.tools.graph_tools import get_related_nodes

        with pytest.raises(InvalidQueryError):
            await get_related_nodes(node_id="")

    @pytest.mark.asyncio
    async def test_get_related_nodes_no_repository(self):
        """リポジトリなしでの関連ノード取得"""
        from tengin_mcp.tools.graph_tools import get_related_nodes

        app_state.graph_repository = None
        result = await get_related_nodes(node_id="cognitive-load-theory")

        assert "error" in result


class TestGetGraphStatisticsTool:
    """get_graph_statistics ツールのテスト"""

    @pytest.mark.asyncio
    async def test_get_graph_statistics(self, setup_graph_tools):
        """グラフ統計の取得"""
        from tengin_mcp.tools.graph_tools import get_graph_statistics

        result = await get_graph_statistics()

        assert "error" not in result
        assert "node_counts" in result
        assert "relationship_counts" in result

    @pytest.mark.asyncio
    async def test_get_graph_statistics_no_repository(self):
        """リポジトリなしでの統計取得"""
        from tengin_mcp.tools.graph_tools import get_graph_statistics

        app_state.graph_repository = None
        result = await get_graph_statistics()

        assert "error" in result
