"""Integration tests for methodology tools."""

import pytest

from tengin_mcp.tools.methodology_tools import (
    search_methodologies,
    get_methodology,
    search_contexts,
    get_context,
    recommend_methodologies,
    get_evidence_for_theory,
)


@pytest.mark.integration
class TestMethodologyTools:
    """教授法ツールの統合テスト"""

    @pytest.mark.asyncio
    async def test_search_methodologies_all(self, initialized_app_state):
        """全教授法を検索"""
        result = await search_methodologies()
        
        assert "methodologies" in result
        assert result["count"] > 0
        
        # 最初の結果を確認
        first = result["methodologies"][0]
        assert "id" in first
        assert "name" in first

    @pytest.mark.asyncio
    async def test_search_methodologies_by_category(self, initialized_app_state):
        """カテゴリで教授法を検索"""
        result = await search_methodologies(category="cooperative")
        
        assert "methodologies" in result
        # カテゴリでフィルタされている

    @pytest.mark.asyncio
    async def test_search_methodologies_by_evidence_level(self, initialized_app_state):
        """エビデンスレベルで教授法を検索"""
        result = await search_methodologies(evidence_level="high")
        
        assert "methodologies" in result
        for m in result["methodologies"]:
            assert m.get("evidence_level") == "high"

    @pytest.mark.asyncio
    async def test_get_methodology_existing(self, initialized_app_state):
        """存在する教授法の詳細を取得"""
        # まず検索して存在するIDを取得
        search_result = await search_methodologies(limit=1)
        if search_result["count"] > 0:
            method_id = search_result["methodologies"][0]["id"]
            
            result = await get_methodology(method_id)
            
            assert result is not None
            assert result.get("id") == method_id

    @pytest.mark.asyncio
    async def test_get_methodology_not_found(self, initialized_app_state):
        """存在しない教授法でエラー"""
        from tengin_mcp.domain.errors import EntityNotFoundError
        
        with pytest.raises(EntityNotFoundError):
            await get_methodology("nonexistent-methodology-id")

    @pytest.mark.asyncio
    async def test_search_contexts_all(self, initialized_app_state):
        """全文脈を検索"""
        result = await search_contexts()
        
        assert "contexts" in result
        assert result["count"] > 0

    @pytest.mark.asyncio
    async def test_search_contexts_by_education_level(self, initialized_app_state):
        """教育段階で文脈を検索"""
        result = await search_contexts(education_level="higher-education")
        
        assert "contexts" in result

    @pytest.mark.asyncio
    async def test_get_context_existing(self, initialized_app_state):
        """存在する文脈の詳細を取得"""
        search_result = await search_contexts(limit=1)
        if search_result["count"] > 0:
            context_id = search_result["contexts"][0]["id"]
            
            result = await get_context(context_id)
            
            assert result is not None
            assert result.get("id") == context_id

    @pytest.mark.asyncio
    async def test_recommend_methodologies(self, initialized_app_state):
        """教授法の推薦"""
        result = await recommend_methodologies(min_evidence_level="moderate")
        
        assert "recommendations" in result
        # スコアでソートされている
        if len(result["recommendations"]) > 1:
            scores = [r.get("recommendation_score", 0) for r in result["recommendations"]]
            assert scores == sorted(scores, reverse=True)

    @pytest.mark.asyncio
    async def test_recommend_methodologies_with_context(self, initialized_app_state):
        """文脈を指定して教授法を推薦"""
        # まず文脈を取得
        contexts = await search_contexts(limit=1)
        if contexts["count"] > 0:
            context_id = contexts["contexts"][0]["id"]
            
            result = await recommend_methodologies(context_id=context_id)
            
            assert "recommendations" in result
            assert result["context_id"] == context_id

    @pytest.mark.asyncio
    async def test_get_evidence_for_theory(self, initialized_app_state):
        """理論に対するエビデンスを取得"""
        # 存在する理論IDを使用
        result = await get_evidence_for_theory("cognitive-load-theory")
        
        assert "supporting_evidence" in result
        assert "challenging_evidence" in result
        assert result["theory_id"] == "cognitive-load-theory"

    @pytest.mark.asyncio
    async def test_get_evidence_for_theory_supports_only(self, initialized_app_state):
        """支持するエビデンスのみ取得"""
        result = await get_evidence_for_theory(
            "cognitive-load-theory", 
            include_challenges=False
        )
        
        assert "supporting_evidence" in result
        assert result["challenging_evidence"] == []

    @pytest.mark.asyncio
    async def test_get_evidence_for_theory_missing_id(self, initialized_app_state):
        """理論IDなしでエラー"""
        from tengin_mcp.domain.errors import InvalidQueryError
        
        with pytest.raises(InvalidQueryError, match="theory_idは必須です"):
            await get_evidence_for_theory("")

    @pytest.mark.asyncio
    async def test_search_methodologies_by_query(self, initialized_app_state):
        """クエリで教授法を検索"""
        result = await search_methodologies(query="協同")
        
        assert "methodologies" in result
        assert result["query"] == "協同"

    @pytest.mark.asyncio
    async def test_search_methodologies_by_theory(self, initialized_app_state):
        """理論IDで教授法を検索"""
        result = await search_methodologies(theory_id="cognitive-load-theory")
        
        assert "methodologies" in result
        assert result["theory_id"] == "cognitive-load-theory"

    @pytest.mark.asyncio
    async def test_search_contexts_by_subject_area(self, initialized_app_state):
        """教科領域で文脈を検索"""
        result = await search_contexts(subject_area="STEM")
        
        assert "contexts" in result
        assert result["subject_area"] == "STEM"

    @pytest.mark.asyncio
    async def test_search_contexts_by_theory(self, initialized_app_state):
        """理論の効果的文脈を検索"""
        result = await search_contexts(effective_for_theory="cognitive-load-theory")
        
        assert "contexts" in result
        assert result["effective_for_theory"] == "cognitive-load-theory"

    @pytest.mark.asyncio
    async def test_get_context_not_found(self, initialized_app_state):
        """存在しない文脈でエラー"""
        from tengin_mcp.domain.errors import EntityNotFoundError
        
        with pytest.raises(EntityNotFoundError):
            await get_context("nonexistent-context-id")

    @pytest.mark.asyncio
    async def test_recommend_methodologies_by_theory(self, initialized_app_state):
        """理論を指定して教授法を推薦"""
        result = await recommend_methodologies(theory_id="cognitive-load-theory")
        
        assert "recommendations" in result
        assert result["theory_id"] == "cognitive-load-theory"

    @pytest.mark.asyncio
    async def test_recommend_methodologies_by_context_and_theory(self, initialized_app_state):
        """文脈と理論を指定して教授法を推薦"""
        # まず文脈を取得
        contexts = await search_contexts(limit=1)
        if contexts["count"] > 0:
            context_id = contexts["contexts"][0]["id"]
            
            result = await recommend_methodologies(
                context_id=context_id,
                theory_id="cognitive-load-theory"
            )
            
            assert "recommendations" in result
            assert result["context_id"] == context_id
            assert result["theory_id"] == "cognitive-load-theory"

    @pytest.mark.asyncio
    async def test_recommend_methodologies_all(self, initialized_app_state):
        """条件なしで教授法を推薦"""
        result = await recommend_methodologies()
        
        assert "recommendations" in result
        assert result["context_id"] is None
        assert result["theory_id"] is None

