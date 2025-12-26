"""Integration Tests: theory_tools - 理論ツール統合テスト"""

import pytest

from tengin_mcp.domain.errors import InvalidQueryError
from tengin_mcp.server import app_state
from tengin_mcp.infrastructure.config import Settings
from tengin_mcp.infrastructure.adapters.neo4j_adapter import Neo4jAdapter
from tengin_mcp.infrastructure.repositories.neo4j_theory_repository import (
    Neo4jTheoryRepository,
)


@pytest.fixture
async def setup_theory_tools():
    """理論ツール用のセットアップ"""
    settings = Settings()
    adapter = Neo4jAdapter(settings)
    await adapter.connect()

    repository = Neo4jTheoryRepository(adapter)
    app_state.theory_repository = repository

    yield adapter

    await adapter.close()
    app_state.theory_repository = None


class TestSearchTheoriesTool:
    """search_theories ツールのテスト"""

    @pytest.mark.asyncio
    async def test_search_theories_basic(self, setup_theory_tools):
        """基本的な検索"""
        from tengin_mcp.tools.theory_tools import search_theories

        result = await search_theories(query="認知")

        assert "error" not in result
        assert "theories" in result
        assert isinstance(result["theories"], list)
        assert result["count"] == len(result["theories"])

    @pytest.mark.asyncio
    async def test_search_theories_with_category(self, setup_theory_tools):
        """カテゴリ指定での検索"""
        from tengin_mcp.tools.theory_tools import search_theories

        result = await search_theories(query="理論", category="learning", limit=5)

        assert "error" not in result
        assert result["category"] == "learning"
        assert len(result["theories"]) <= 5

    @pytest.mark.asyncio
    async def test_search_theories_with_limit(self, setup_theory_tools):
        """リミット指定での検索"""
        from tengin_mcp.tools.theory_tools import search_theories

        result = await search_theories(query="理論", limit=3)

        assert len(result["theories"]) <= 3

    @pytest.mark.asyncio
    async def test_search_theories_invalid_query(self, setup_theory_tools):
        """無効なクエリでのエラー"""
        from tengin_mcp.tools.theory_tools import search_theories

        with pytest.raises(InvalidQueryError):
            await search_theories(query="a")  # 2文字未満

    @pytest.mark.asyncio
    async def test_search_theories_invalid_category(self, setup_theory_tools):
        """無効なカテゴリでのエラー"""
        from tengin_mcp.tools.theory_tools import search_theories

        with pytest.raises(InvalidQueryError):
            await search_theories(query="認知", category="invalid_category")

    @pytest.mark.asyncio
    async def test_search_theories_no_repository(self):
        """リポジトリなしでの検索"""
        from tengin_mcp.tools.theory_tools import search_theories

        app_state.theory_repository = None
        result = await search_theories(query="認知")

        assert "error" in result
        assert result["theories"] == []


class TestGetTheoryTool:
    """get_theory ツールのテスト"""

    @pytest.mark.asyncio
    async def test_get_theory_existing(self, setup_theory_tools):
        """存在する理論の取得"""
        from tengin_mcp.tools.theory_tools import get_theory

        result = await get_theory(theory_id="cognitive-load-theory")

        assert "error" not in result
        assert result["id"] == "cognitive-load-theory"
        assert "name" in result
        assert "description" in result

    @pytest.mark.asyncio
    async def test_get_theory_not_found(self, setup_theory_tools):
        """存在しない理論の取得"""
        from tengin_mcp.tools.theory_tools import get_theory

        result = await get_theory(theory_id="non-existent-theory")

        assert "error" in result

    @pytest.mark.asyncio
    async def test_get_theory_invalid_id(self, setup_theory_tools):
        """無効なIDでのエラー"""
        from tengin_mcp.tools.theory_tools import get_theory

        with pytest.raises(InvalidQueryError):
            await get_theory(theory_id="")

    @pytest.mark.asyncio
    async def test_get_theory_no_repository(self):
        """リポジトリなしでの取得"""
        from tengin_mcp.tools.theory_tools import get_theory

        app_state.theory_repository = None
        result = await get_theory(theory_id="cognitive-load-theory")

        assert "error" in result


class TestGetTheoriesByCategoryTool:
    """get_theories_by_category ツールのテスト"""

    @pytest.mark.asyncio
    async def test_get_learning_theories(self, setup_theory_tools):
        """学習理論の取得"""
        from tengin_mcp.tools.theory_tools import get_theories_by_category

        result = await get_theories_by_category(category="learning")

        assert "error" not in result
        assert "theories" in result
        assert result["category"] == "learning"

    @pytest.mark.asyncio
    async def test_get_motivation_theories(self, setup_theory_tools):
        """動機づけ理論の取得"""
        from tengin_mcp.tools.theory_tools import get_theories_by_category

        result = await get_theories_by_category(category="motivation", limit=5)

        assert "error" not in result
        assert len(result["theories"]) <= 5

    @pytest.mark.asyncio
    async def test_get_theories_invalid_category(self, setup_theory_tools):
        """無効なカテゴリでのエラー"""
        from tengin_mcp.tools.theory_tools import get_theories_by_category

        with pytest.raises(InvalidQueryError):
            await get_theories_by_category(category="invalid")

    @pytest.mark.asyncio
    async def test_get_theories_no_repository(self):
        """リポジトリなしでの取得"""
        from tengin_mcp.tools.theory_tools import get_theories_by_category

        app_state.theory_repository = None
        result = await get_theories_by_category(category="learning")

        assert "error" in result


class TestGetTheoristTool:
    """get_theorist ツールのテスト"""

    @pytest.mark.asyncio
    async def test_get_theorist_existing(self, setup_theory_tools):
        """存在する理論家の取得"""
        from tengin_mcp.tools.theory_tools import get_theorist

        result = await get_theorist(theorist_id="sweller")

        assert "error" not in result
        assert result["id"] == "sweller"
        assert "name" in result

    @pytest.mark.asyncio
    async def test_get_theorist_not_found(self, setup_theory_tools):
        """存在しない理論家の取得"""
        from tengin_mcp.tools.theory_tools import get_theorist

        result = await get_theorist(theorist_id="non-existent")

        assert "error" in result

    @pytest.mark.asyncio
    async def test_get_theorist_invalid_id(self, setup_theory_tools):
        """無効なIDでのエラー"""
        from tengin_mcp.tools.theory_tools import get_theorist

        with pytest.raises(InvalidQueryError):
            await get_theorist(theorist_id="")

    @pytest.mark.asyncio
    async def test_get_theorist_no_repository(self):
        """リポジトリなしでの取得"""
        from tengin_mcp.tools.theory_tools import get_theorist

        app_state.theory_repository = None
        result = await get_theorist(theorist_id="sweller")

        assert "error" in result


class TestGetConceptTool:
    """get_concept ツールのテスト"""

    @pytest.mark.asyncio
    async def test_get_concept_existing(self, setup_theory_tools):
        """存在する概念の取得"""
        from tengin_mcp.tools.theory_tools import get_concept

        result = await get_concept(concept_id="cognitive-load")

        assert "error" not in result
        assert result["id"] == "cognitive-load"
        assert "name" in result
        assert "definition" in result

    @pytest.mark.asyncio
    async def test_get_concept_not_found(self, setup_theory_tools):
        """存在しない概念の取得"""
        from tengin_mcp.tools.theory_tools import get_concept

        result = await get_concept(concept_id="non-existent")

        assert "error" in result

    @pytest.mark.asyncio
    async def test_get_concept_invalid_id(self, setup_theory_tools):
        """無効なIDでのエラー"""
        from tengin_mcp.tools.theory_tools import get_concept

        with pytest.raises(InvalidQueryError):
            await get_concept(concept_id="")

    @pytest.mark.asyncio
    async def test_get_concept_no_repository(self):
        """リポジトリなしでの取得"""
        from tengin_mcp.tools.theory_tools import get_concept

        app_state.theory_repository = None
        result = await get_concept(concept_id="cognitive-load")

        assert "error" in result


class TestGetPrincipleTool:
    """get_principle ツールのテスト"""

    @pytest.mark.asyncio
    async def test_get_principle_existing(self, setup_theory_tools):
        """存在する原則の取得"""
        from tengin_mcp.tools.theory_tools import get_principle

        # まず存在する原則IDを取得
        adapter = setup_theory_tools
        result = await adapter.execute_query(
            "MATCH (p:Principle) RETURN p.id as id LIMIT 1"
        )
        if result:
            principle_id = result[0]["id"]
            principle = await get_principle(principle_id=principle_id)

            assert "error" not in principle
            assert principle["id"] == principle_id

    @pytest.mark.asyncio
    async def test_get_principle_not_found(self, setup_theory_tools):
        """存在しない原則の取得"""
        from tengin_mcp.tools.theory_tools import get_principle

        result = await get_principle(principle_id="non-existent")

        assert "error" in result

    @pytest.mark.asyncio
    async def test_get_principle_invalid_id(self, setup_theory_tools):
        """無効なIDでのエラー"""
        from tengin_mcp.tools.theory_tools import get_principle

        with pytest.raises(InvalidQueryError):
            await get_principle(principle_id="")

    @pytest.mark.asyncio
    async def test_get_principle_no_repository(self):
        """リポジトリなしでの取得"""
        from tengin_mcp.tools.theory_tools import get_principle

        app_state.theory_repository = None
        result = await get_principle(principle_id="some-principle")

        assert "error" in result


class TestGetEvidenceTool:
    """get_evidence ツールのテスト"""

    @pytest.mark.asyncio
    async def test_get_evidence_existing(self, setup_theory_tools):
        """存在するエビデンスの取得"""
        from tengin_mcp.tools.theory_tools import get_evidence

        # まず存在するエビデンスIDを取得
        adapter = setup_theory_tools
        result = await adapter.execute_query(
            "MATCH (e:Evidence) RETURN e.id as id LIMIT 1"
        )
        if result:
            evidence_id = result[0]["id"]
            evidence = await get_evidence(evidence_id=evidence_id)

            assert "error" not in evidence
            assert evidence["id"] == evidence_id

    @pytest.mark.asyncio
    async def test_get_evidence_not_found(self, setup_theory_tools):
        """存在しないエビデンスの取得"""
        from tengin_mcp.tools.theory_tools import get_evidence

        result = await get_evidence(evidence_id="non-existent")

        assert "error" in result

    @pytest.mark.asyncio
    async def test_get_evidence_invalid_id(self, setup_theory_tools):
        """無効なIDでのエラー"""
        from tengin_mcp.tools.theory_tools import get_evidence

        with pytest.raises(InvalidQueryError):
            await get_evidence(evidence_id="")

    @pytest.mark.asyncio
    async def test_get_evidence_no_repository(self):
        """リポジトリなしでの取得"""
        from tengin_mcp.tools.theory_tools import get_evidence

        app_state.theory_repository = None
        result = await get_evidence(evidence_id="some-evidence")

        assert "error" in result
