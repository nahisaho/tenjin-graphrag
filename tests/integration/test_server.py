"""Integration Tests: server - MCPサーバーの統合テスト"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch


class TestAppState:
    """AppStateクラスのテスト"""

    def test_app_state_initialization(self):
        """AppStateの初期化"""
        from tengin_mcp.server import AppState

        state = AppState()

        assert state.settings is not None
        assert state.neo4j_adapter is None
        assert state.chromadb_adapter is None
        assert state.embedding_adapter is None
        assert state.theory_repository is None
        assert state.graph_repository is None

    def test_app_state_has_settings(self):
        """AppStateが設定を持つ"""
        from tengin_mcp.server import AppState

        state = AppState()

        # 設定オブジェクトの属性を確認
        assert hasattr(state.settings, 'neo4j_uri')
        assert hasattr(state.settings, 'chromadb_path')


class TestLifespan:
    """lifespanコンテキストマネージャのテスト"""

    @pytest.mark.asyncio
    async def test_lifespan_context_manager(self):
        """lifespanコンテキストマネージャの基本的なテスト"""
        from tengin_mcp.server import lifespan, app_state
        from unittest.mock import MagicMock

        # モックサーバー
        mock_server = MagicMock()

        # モックアダプター
        with patch('tengin_mcp.server.Neo4jAdapter') as mock_neo4j, \
             patch('tengin_mcp.server.ChromaDBAdapter') as mock_chromadb, \
             patch('tengin_mcp.server.EmbeddingAdapter') as mock_embedding, \
             patch('tengin_mcp.server.Neo4jTheoryRepository'), \
             patch('tengin_mcp.server.Neo4jGraphRepository'):

            # モックの設定
            mock_neo4j_instance = AsyncMock()
            mock_chromadb_instance = AsyncMock()
            mock_embedding_instance = AsyncMock()

            mock_neo4j.return_value = mock_neo4j_instance
            mock_chromadb.return_value = mock_chromadb_instance
            mock_embedding.return_value = mock_embedding_instance

            # lifespanを実行
            async with lifespan(mock_server) as deps:
                # 依存関係が返されることを確認
                assert 'settings' in deps
                assert 'neo4j' in deps
                assert 'chromadb' in deps
                assert 'embedding' in deps
                assert 'theory_repo' in deps
                assert 'graph_repo' in deps

                # 接続が呼ばれたことを確認
                mock_neo4j_instance.connect.assert_called_once()
                mock_chromadb_instance.connect.assert_called_once()
                mock_embedding_instance.connect.assert_called_once()

            # クローズが呼ばれたことを確認
            mock_neo4j_instance.close.assert_called_once()
            mock_chromadb_instance.close.assert_called_once()
            mock_embedding_instance.close.assert_called_once()

    @pytest.mark.asyncio
    async def test_lifespan_cleanup_on_error(self):
        """エラー時のクリーンアップ"""
        from tengin_mcp.server import lifespan
        from unittest.mock import MagicMock

        mock_server = MagicMock()

        with patch('tengin_mcp.server.Neo4jAdapter') as mock_neo4j, \
             patch('tengin_mcp.server.ChromaDBAdapter') as mock_chromadb, \
             patch('tengin_mcp.server.EmbeddingAdapter') as mock_embedding:

            mock_neo4j_instance = AsyncMock()
            mock_chromadb_instance = AsyncMock()
            mock_embedding_instance = AsyncMock()

            # 接続時にエラーを発生させる
            mock_neo4j_instance.connect.side_effect = Exception("Connection failed")

            mock_neo4j.return_value = mock_neo4j_instance
            mock_chromadb.return_value = mock_chromadb_instance
            mock_embedding.return_value = mock_embedding_instance

            with pytest.raises(Exception):
                async with lifespan(mock_server):
                    pass

            # クリーンアップが呼ばれることを確認
            mock_neo4j_instance.close.assert_called_once()


class TestMCPInstance:
    """MCPインスタンスのテスト"""

    def test_mcp_instance_exists(self):
        """MCPインスタンスが存在する"""
        from tengin_mcp.server import mcp

        assert mcp is not None
        assert mcp.name == "TENGIN Education Theory GraphRAG"

    def test_mcp_is_fastmcp_instance(self):
        """MCPがFastMCPインスタンスである"""
        from tengin_mcp.server import mcp
        from mcp.server.fastmcp import FastMCP

        assert isinstance(mcp, FastMCP)


class TestToolsRegistration:
    """ツール登録のテスト"""

    def test_theory_tools_imported(self):
        """理論ツールがインポートされている"""
        import tengin_mcp.tools.theory_tools

        assert tengin_mcp.tools.theory_tools is not None

    def test_graph_tools_imported(self):
        """グラフツールがインポートされている"""
        import tengin_mcp.tools.graph_tools

        assert tengin_mcp.tools.graph_tools is not None

    def test_citation_tools_imported(self):
        """引用ツールがインポートされている"""
        import tengin_mcp.tools.citation_tools

        assert tengin_mcp.tools.citation_tools is not None


class TestResourcesRegistration:
    """リソース登録のテスト"""

    def test_theory_resources_imported(self):
        """理論リソースがインポートされている"""
        import tengin_mcp.resources.theory_resources

        assert tengin_mcp.resources.theory_resources is not None


class TestPromptsRegistration:
    """プロンプト登録のテスト"""

    def test_education_prompts_imported(self):
        """教育プロンプトがインポートされている"""
        import tengin_mcp.prompts.education_prompts

        assert tengin_mcp.prompts.education_prompts is not None
