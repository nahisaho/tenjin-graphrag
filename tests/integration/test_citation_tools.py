"""Integration Tests: citation_tools - 引用ツール統合テスト"""

import pytest

from tengin_mcp.domain.errors import InvalidQueryError, TheoryNotFoundError
from tengin_mcp.server import app_state
from tengin_mcp.infrastructure.config import Settings
from tengin_mcp.infrastructure.adapters.neo4j_adapter import Neo4jAdapter
from tengin_mcp.infrastructure.repositories.neo4j_theory_repository import (
    Neo4jTheoryRepository,
)


@pytest.fixture
async def setup_citation_tools():
    """引用ツール用のセットアップ"""
    settings = Settings()
    adapter = Neo4jAdapter(settings)
    await adapter.connect()

    repository = Neo4jTheoryRepository(adapter)
    app_state.theory_repository = repository

    yield adapter

    await adapter.close()
    app_state.theory_repository = None


class TestCiteTheoryTool:
    """cite_theory ツールのテスト"""

    @pytest.mark.asyncio
    async def test_cite_theory_apa7(self, setup_citation_tools):
        """APA7形式での引用生成"""
        from tengin_mcp.tools.citation_tools import cite_theory

        result = await cite_theory(
            theory_id="cognitive-load-theory",
            format="APA7",
        )

        assert "error" not in result
        assert result["theory_id"] == "cognitive-load-theory"
        assert result["format"] == "APA7"
        assert "citation" in result

    @pytest.mark.asyncio
    async def test_cite_theory_mla9(self, setup_citation_tools):
        """MLA9形式での引用生成"""
        from tengin_mcp.tools.citation_tools import cite_theory

        result = await cite_theory(
            theory_id="cognitive-load-theory",
            format="MLA9",
        )

        assert "error" not in result
        assert result["format"] == "MLA9"
        assert "citation" in result

    @pytest.mark.asyncio
    async def test_cite_theory_chicago(self, setup_citation_tools):
        """Chicago形式での引用生成"""
        from tengin_mcp.tools.citation_tools import cite_theory

        result = await cite_theory(
            theory_id="cognitive-load-theory",
            format="Chicago",
        )

        assert "error" not in result
        assert result["format"] == "Chicago"
        assert "citation" in result

    @pytest.mark.asyncio
    async def test_cite_theory_harvard(self, setup_citation_tools):
        """Harvard形式での引用生成"""
        from tengin_mcp.tools.citation_tools import cite_theory

        result = await cite_theory(
            theory_id="cognitive-load-theory",
            format="Harvard",
        )

        assert "error" not in result
        assert result["format"] == "Harvard"
        assert "citation" in result

    @pytest.mark.asyncio
    async def test_cite_theory_ieee(self, setup_citation_tools):
        """IEEE形式での引用生成"""
        from tengin_mcp.tools.citation_tools import cite_theory

        result = await cite_theory(
            theory_id="cognitive-load-theory",
            format="IEEE",
        )

        assert "error" not in result
        assert result["format"] == "IEEE"
        assert "citation" in result

    @pytest.mark.asyncio
    async def test_cite_theory_invalid_id(self, setup_citation_tools):
        """無効なIDでエラー"""
        from tengin_mcp.tools.citation_tools import cite_theory

        with pytest.raises(InvalidQueryError):
            await cite_theory(theory_id="")

    @pytest.mark.asyncio
    async def test_cite_theory_invalid_format(self, setup_citation_tools):
        """無効な引用形式でエラー"""
        from tengin_mcp.tools.citation_tools import cite_theory

        with pytest.raises(InvalidQueryError):
            await cite_theory(
                theory_id="cognitive-load-theory",
                format="InvalidFormat",
            )

    @pytest.mark.asyncio
    async def test_cite_theory_not_found(self, setup_citation_tools):
        """存在しない理論の引用"""
        from tengin_mcp.tools.citation_tools import cite_theory

        result = await cite_theory(theory_id="non-existent-theory")

        assert "error" in result

    @pytest.mark.asyncio
    async def test_cite_theory_no_repository(self):
        """リポジトリなしでの引用生成"""
        from tengin_mcp.tools.citation_tools import cite_theory

        app_state.theory_repository = None
        result = await cite_theory(theory_id="cognitive-load-theory")

        assert "error" in result


class TestCompareTheoriesTool:
    """compare_theories ツールのテスト"""

    @pytest.mark.asyncio
    async def test_compare_theories_two(self, setup_citation_tools):
        """2つの理論を比較"""
        from tengin_mcp.tools.citation_tools import compare_theories

        result = await compare_theories(
            theory_ids=["cognitive-load-theory", "multimedia-learning-theory"],
        )

        assert "error" not in result
        assert result["theory_count"] == 2
        assert "theories" in result
        assert "analysis" in result

    @pytest.mark.asyncio
    async def test_compare_theories_three(self, setup_citation_tools):
        """3つの理論を比較"""
        from tengin_mcp.tools.citation_tools import compare_theories

        result = await compare_theories(
            theory_ids=[
                "cognitive-load-theory",
                "multimedia-learning-theory",
                "zone-of-proximal-development",
            ],
        )

        assert "error" not in result
        assert result["theory_count"] == 3

    @pytest.mark.asyncio
    async def test_compare_theories_with_not_found(self, setup_citation_tools):
        """存在しない理論を含む比較"""
        from tengin_mcp.tools.citation_tools import compare_theories

        result = await compare_theories(
            theory_ids=["cognitive-load-theory", "non-existent-theory"],
        )

        assert "error" not in result
        assert result["theory_count"] == 2
        # 存在しない理論にはエラーマークがある
        theories = result["theories"]
        found_error = any(t.get("error") == "Not found" for t in theories)
        assert found_error

    @pytest.mark.asyncio
    async def test_compare_theories_too_few(self, setup_citation_tools):
        """理論が少なすぎる場合のエラー"""
        from tengin_mcp.tools.citation_tools import compare_theories

        with pytest.raises(InvalidQueryError):
            await compare_theories(theory_ids=["cognitive-load-theory"])

    @pytest.mark.asyncio
    async def test_compare_theories_too_many(self, setup_citation_tools):
        """理論が多すぎる場合のエラー"""
        from tengin_mcp.tools.citation_tools import compare_theories

        with pytest.raises(InvalidQueryError):
            await compare_theories(
                theory_ids=[
                    "theory1",
                    "theory2",
                    "theory3",
                    "theory4",
                    "theory5",
                    "theory6",
                ]
            )

    @pytest.mark.asyncio
    async def test_compare_theories_empty_list(self, setup_citation_tools):
        """空のリストでエラー"""
        from tengin_mcp.tools.citation_tools import compare_theories

        with pytest.raises(InvalidQueryError):
            await compare_theories(theory_ids=[])

    @pytest.mark.asyncio
    async def test_compare_theories_no_repository(self):
        """リポジトリなしでの比較"""
        from tengin_mcp.tools.citation_tools import compare_theories

        app_state.theory_repository = None
        result = await compare_theories(
            theory_ids=["cognitive-load-theory", "multimedia-learning-theory"],
        )

        assert "error" in result
        assert result["theories"] == []

    @pytest.mark.asyncio
    async def test_compare_theories_analysis(self, setup_citation_tools):
        """比較分析の確認"""
        from tengin_mcp.tools.citation_tools import compare_theories

        result = await compare_theories(
            theory_ids=["cognitive-load-theory", "multimedia-learning-theory"],
        )

        assert "analysis" in result
        analysis = result["analysis"]
        assert "same_category" in analysis
        assert "categories" in analysis
        assert "common_keywords" in analysis
