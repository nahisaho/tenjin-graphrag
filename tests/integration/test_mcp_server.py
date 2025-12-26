"""
MCPサーバーの統合テスト

FastMCPサーバーの動作を検証します。
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch


# --- MCP Server Import Test ---


class TestMCPServerImport:
    """MCPサーバーのインポートテスト"""

    def test_import_server_module(self):
        """サーバーモジュールがインポート可能"""
        from tengin_mcp import server
        assert hasattr(server, "mcp")
        assert hasattr(server, "main")

    def test_import_mcp_instance(self):
        """MCPインスタンスが正しく作成されている"""
        from tengin_mcp.server import mcp
        assert mcp is not None
        assert hasattr(mcp, "name")

    def test_import_tools_module(self):
        """ツールモジュールがインポート可能"""
        from tengin_mcp.tools import theory_tools, graph_tools, citation_tools
        assert theory_tools is not None
        assert graph_tools is not None
        assert citation_tools is not None

    def test_import_resources_module(self):
        """リソースモジュールがインポート可能"""
        from tengin_mcp.resources import theory_resources
        assert theory_resources is not None

    def test_import_prompts_module(self):
        """プロンプトモジュールがインポート可能"""
        from tengin_mcp.prompts import education_prompts
        assert education_prompts is not None


# --- Theory Tools Function Tests ---


class TestTheoryToolsFunctions:
    """theory_tools.pyの関数テスト"""

    def test_search_theories_function_exists(self):
        """search_theories関数が存在する"""
        from tengin_mcp.tools import theory_tools
        assert hasattr(theory_tools, "search_theories")

    def test_get_theory_function_exists(self):
        """get_theory関数が存在する"""
        from tengin_mcp.tools import theory_tools
        assert hasattr(theory_tools, "get_theory")

    def test_get_theorist_function_exists(self):
        """get_theorist関数が存在する"""
        from tengin_mcp.tools import theory_tools
        assert hasattr(theory_tools, "get_theorist")

    def test_get_theories_by_category_function_exists(self):
        """get_theories_by_category関数が存在する"""
        from tengin_mcp.tools import theory_tools
        assert hasattr(theory_tools, "get_theories_by_category")

    def test_get_concept_function_exists(self):
        """get_concept関数が存在する"""
        from tengin_mcp.tools import theory_tools
        assert hasattr(theory_tools, "get_concept")

    def test_get_principle_function_exists(self):
        """get_principle関数が存在する"""
        from tengin_mcp.tools import theory_tools
        assert hasattr(theory_tools, "get_principle")

    def test_get_evidence_function_exists(self):
        """get_evidence関数が存在する"""
        from tengin_mcp.tools import theory_tools
        assert hasattr(theory_tools, "get_evidence")


# --- Graph Tools Function Tests ---


class TestGraphToolsFunctions:
    """graph_tools.pyの関数テスト"""

    def test_traverse_graph_function_exists(self):
        """traverse_graph関数が存在する"""
        from tengin_mcp.tools import graph_tools
        assert hasattr(graph_tools, "traverse_graph")

    def test_get_graph_stats_function_exists(self):
        """get_graph_statistics関数が存在する"""
        from tengin_mcp.tools import graph_tools
        assert hasattr(graph_tools, "get_graph_statistics")


# --- Citation Tools Function Tests ---


class TestCitationToolsFunctions:
    """citation_tools.pyの関数テスト"""

    def test_cite_theory_function_exists(self):
        """cite_theory関数が存在する"""
        from tengin_mcp.tools import citation_tools
        assert hasattr(citation_tools, "cite_theory")

    def test_compare_theories_function_exists(self):
        """compare_theories関数が存在する"""
        from tengin_mcp.tools import citation_tools
        assert hasattr(citation_tools, "compare_theories")


# --- Resource Function Tests ---


class TestResourceFunctions:
    """リソース関数のテスト"""

    def test_get_theory_resource_exists(self):
        """get_theory_resource関数が存在する"""
        from tengin_mcp.resources import theory_resources
        assert hasattr(theory_resources, "get_theory_resource")

    def test_get_theorist_resource_exists(self):
        """get_theorist_resource関数が存在する"""
        from tengin_mcp.resources import theory_resources
        assert hasattr(theory_resources, "get_theorist_resource")

    def test_get_concept_resource_exists(self):
        """get_concept_resource関数が存在する"""
        from tengin_mcp.resources import theory_resources
        assert hasattr(theory_resources, "get_concept_resource")

    def test_get_evidence_resource_exists(self):
        """get_evidence_resource関数が存在する"""
        from tengin_mcp.resources import theory_resources
        assert hasattr(theory_resources, "get_evidence_resource")

    def test_get_graph_statistics_resource_exists(self):
        """get_graph_statistics_resource関数が存在する"""
        from tengin_mcp.resources import theory_resources
        assert hasattr(theory_resources, "get_graph_statistics_resource")


# --- Prompt Function Tests ---


class TestPromptFunctions:
    """プロンプト関数のテスト"""

    def test_design_lesson_exists(self):
        """design_lesson関数が存在する"""
        from tengin_mcp.prompts import education_prompts
        assert hasattr(education_prompts, "design_lesson")

    def test_explain_theory_exists(self):
        """explain_theory関数が存在する"""
        from tengin_mcp.prompts import education_prompts
        assert hasattr(education_prompts, "explain_theory")

    def test_apply_theory_exists(self):
        """apply_theory関数が存在する"""
        from tengin_mcp.prompts import education_prompts
        assert hasattr(education_prompts, "apply_theory")

    def test_create_assessment_exists(self):
        """create_assessment関数が存在する"""
        from tengin_mcp.prompts import education_prompts
        assert hasattr(education_prompts, "create_assessment")

    def test_curriculum_plan_exists(self):
        """curriculum_plan関数が存在する"""
        from tengin_mcp.prompts import education_prompts
        assert hasattr(education_prompts, "curriculum_plan")

    def test_troubleshoot_learning_exists(self):
        """troubleshoot_learning関数が存在する"""
        from tengin_mcp.prompts import education_prompts
        assert hasattr(education_prompts, "troubleshoot_learning")


# --- Configuration Tests ---


class TestConfiguration:
    """設定のテスト"""

    def test_settings_loads(self):
        """Settingsがロードできる"""
        from tengin_mcp.infrastructure.config import Settings
        settings = Settings()
        assert settings is not None

    def test_settings_has_neo4j_config(self):
        """Neo4j設定が存在する"""
        from tengin_mcp.infrastructure.config import Settings
        settings = Settings()
        assert hasattr(settings, "neo4j_uri")
        assert hasattr(settings, "neo4j_user")
        assert hasattr(settings, "neo4j_password")

    def test_settings_has_chromadb_config(self):
        """ChromaDB設定が存在する"""
        from tengin_mcp.infrastructure.config import Settings
        settings = Settings()
        assert hasattr(settings, "chromadb_path")

    def test_settings_has_embedding_config(self):
        """Embedding設定が存在する"""
        from tengin_mcp.infrastructure.config import Settings
        settings = Settings()
        assert hasattr(settings, "embedding_provider")
        assert hasattr(settings, "embedding_model")


# --- Adapter Tests ---


class TestAdapters:
    """アダプターのテスト"""

    def test_neo4j_adapter_import(self):
        """Neo4jAdapterがインポートできる"""
        from tengin_mcp.infrastructure.adapters.neo4j_adapter import Neo4jAdapter
        assert Neo4jAdapter is not None

    def test_chromadb_adapter_import(self):
        """ChromaDBAdapterがインポートできる"""
        from tengin_mcp.infrastructure.adapters.chromadb_adapter import ChromaDBAdapter
        assert ChromaDBAdapter is not None

    def test_embedding_adapter_import(self):
        """EmbeddingAdapterがインポートできる"""
        from tengin_mcp.infrastructure.adapters.embedding_adapter import EmbeddingAdapter
        assert EmbeddingAdapter is not None


# --- Domain Entity Tests ---


class TestDomainEntities:
    """ドメインエンティティのテスト"""

    def test_theory_entity_import(self):
        """Theoryエンティティがインポートできる"""
        from tengin_mcp.domain.entities import Theory
        assert Theory is not None

    def test_theorist_entity_import(self):
        """Theoristエンティティがインポートできる"""
        from tengin_mcp.domain.entities import Theorist
        assert Theorist is not None

    def test_concept_entity_import(self):
        """Conceptエンティティがインポートできる"""
        from tengin_mcp.domain.entities import Concept
        assert Concept is not None

    def test_principle_entity_import(self):
        """Principleエンティティがインポートできる"""
        from tengin_mcp.domain.entities import Principle
        assert Principle is not None

    def test_evidence_entity_import(self):
        """Evidenceエンティティがインポートできる"""
        from tengin_mcp.domain.entities import Evidence
        assert Evidence is not None
