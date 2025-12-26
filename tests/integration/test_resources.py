"""
リソースの統合テスト

theory_resources モジュールのテスト
"""

import pytest

from tengin_mcp.infrastructure.config import Settings
from tengin_mcp.infrastructure.adapters.neo4j_adapter import Neo4jAdapter
from tengin_mcp.infrastructure.repositories.neo4j_theory_repository import Neo4jTheoryRepository
from tengin_mcp.infrastructure.repositories.neo4j_graph_repository import Neo4jGraphRepository
from tengin_mcp.server import app_state


@pytest.fixture
async def setup_repositories():
    """リポジトリのセットアップ"""
    settings = Settings()
    adapter = Neo4jAdapter(settings)
    await adapter.connect()
    
    # アプリケーション状態にリポジトリを設定
    app_state.theory_repository = Neo4jTheoryRepository(adapter)
    app_state.graph_repository = Neo4jGraphRepository(adapter)
    
    yield adapter
    
    await adapter.close()
    app_state.theory_repository = None
    app_state.graph_repository = None


class TestTheoryResource:
    """理論リソースのテスト"""

    @pytest.mark.asyncio
    async def test_get_theory_resource(self, setup_repositories):
        """理論リソースの取得"""
        from tengin_mcp.resources.theory_resources import get_theory_resource
        
        result = await get_theory_resource("cognitive-load-theory")
        
        assert isinstance(result, str)
        assert "認知負荷理論" in result
        assert "Category:" in result

    @pytest.mark.asyncio
    async def test_get_theory_resource_not_found(self, setup_repositories):
        """存在しない理論リソースの取得"""
        from tengin_mcp.resources.theory_resources import get_theory_resource
        
        result = await get_theory_resource("non-existent-theory")
        
        assert "Error" in result

    @pytest.mark.asyncio
    async def test_get_theory_resource_no_repository(self):
        """リポジトリなしでの理論リソース取得"""
        from tengin_mcp.resources.theory_resources import get_theory_resource
        
        app_state.theory_repository = None
        result = await get_theory_resource("cognitive-load-theory")
        
        assert "Error" in result
        assert "not initialized" in result


class TestConceptResource:
    """概念リソースのテスト"""

    @pytest.mark.asyncio
    async def test_get_concept_resource(self, setup_repositories):
        """概念リソースの取得"""
        from tengin_mcp.resources.theory_resources import get_concept_resource
        
        result = await get_concept_resource("cognitive-load")
        
        assert isinstance(result, str)
        assert "認知負荷" in result or "Cognitive Load" in result or "cognitive load" in result.lower()

    @pytest.mark.asyncio
    async def test_get_concept_resource_not_found(self, setup_repositories):
        """存在しない概念リソースの取得"""
        from tengin_mcp.resources.theory_resources import get_concept_resource
        
        result = await get_concept_resource("non-existent-concept")
        
        assert "Error" in result

    @pytest.mark.asyncio
    async def test_get_concept_resource_no_repository(self):
        """リポジトリなしでの概念リソース取得"""
        from tengin_mcp.resources.theory_resources import get_concept_resource
        
        app_state.theory_repository = None
        result = await get_concept_resource("cognitive-load")
        
        assert "Error" in result
        assert "not initialized" in result


class TestTheoristResource:
    """理論家リソースのテスト"""

    @pytest.mark.asyncio
    async def test_get_theorist_resource(self, setup_repositories):
        """理論家リソースの取得"""
        from tengin_mcp.resources.theory_resources import get_theorist_resource
        
        result = await get_theorist_resource("sweller")
        
        assert isinstance(result, str)
        assert "スウェラー" in result or "Sweller" in result

    @pytest.mark.asyncio
    async def test_get_theorist_resource_not_found(self, setup_repositories):
        """存在しない理論家リソースの取得"""
        from tengin_mcp.resources.theory_resources import get_theorist_resource
        
        result = await get_theorist_resource("non-existent-theorist")
        
        assert "Error" in result

    @pytest.mark.asyncio
    async def test_get_theorist_resource_no_repository(self):
        """リポジトリなしでの理論家リソース取得"""
        from tengin_mcp.resources.theory_resources import get_theorist_resource
        
        app_state.theory_repository = None
        result = await get_theorist_resource("sweller")
        
        assert "Error" in result
        assert "not initialized" in result


class TestEvidenceResource:
    """エビデンスリソースのテスト"""

    @pytest.mark.asyncio
    async def test_get_evidence_resource(self, setup_repositories):
        """エビデンスリソースの取得"""
        from tengin_mcp.resources.theory_resources import get_evidence_resource
        
        # まず存在するエビデンスIDを取得
        adapter = setup_repositories
        result = await adapter.execute_query(
            "MATCH (e:Evidence) RETURN e.id as id LIMIT 1"
        )
        if result:
            evidence_id = result[0]["id"]
            resource = await get_evidence_resource(evidence_id)
            
            assert isinstance(resource, str)
            # リソースが取得できた（エラーでない）
            assert "Error" not in resource or evidence_id in resource

    @pytest.mark.asyncio
    async def test_get_evidence_resource_not_found(self, setup_repositories):
        """存在しないエビデンスリソースの取得"""
        from tengin_mcp.resources.theory_resources import get_evidence_resource
        
        result = await get_evidence_resource("non-existent-evidence")
        
        assert "Error" in result

    @pytest.mark.asyncio
    async def test_get_evidence_resource_no_repository(self):
        """リポジトリなしでのエビデンスリソース取得"""
        from tengin_mcp.resources.theory_resources import get_evidence_resource
        
        app_state.theory_repository = None
        result = await get_evidence_resource("test-evidence")
        
        assert "Error" in result
        assert "not initialized" in result


class TestGraphStatisticsResource:
    """グラフ統計リソースのテスト"""

    @pytest.mark.asyncio
    async def test_get_graph_statistics_resource(self, setup_repositories):
        """グラフ統計リソースの取得"""
        from tengin_mcp.resources.theory_resources import get_graph_statistics_resource
        
        result = await get_graph_statistics_resource()
        
        assert isinstance(result, str)
        assert "Statistics" in result
        assert "Node Counts" in result

    @pytest.mark.asyncio
    async def test_get_graph_statistics_resource_no_repository(self):
        """リポジトリなしでのグラフ統計リソース取得"""
        from tengin_mcp.resources.theory_resources import get_graph_statistics_resource
        
        app_state.graph_repository = None
        result = await get_graph_statistics_resource()
        
        assert "Error" in result
        assert "not initialized" in result
