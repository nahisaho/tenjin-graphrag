"""Unit Tests: chromadb_adapter - ChromaDBアダプターのユニットテスト"""

import pytest
from unittest.mock import MagicMock, patch, AsyncMock


def create_mock_settings(**kwargs):
    """テスト用のモックSettings作成"""
    settings = MagicMock()
    settings.chromadb_path = kwargs.get("chromadb_path", "./data/chromadb")
    return settings


class TestChromaDBAdapterInit:
    """ChromaDBAdapterの初期化テスト"""

    def test_init(self):
        """初期化のテスト"""
        from tengin_mcp.infrastructure.adapters.chromadb_adapter import ChromaDBAdapter

        settings = create_mock_settings()
        adapter = ChromaDBAdapter(settings)

        assert adapter._settings == settings
        assert adapter._client is None
        assert adapter._collection is None

    def test_collection_name(self):
        """コレクション名の確認"""
        from tengin_mcp.infrastructure.adapters.chromadb_adapter import ChromaDBAdapter

        assert ChromaDBAdapter.COLLECTION_NAME == "education_theories"


class TestChromaDBAdapterConnection:
    """接続/切断のテスト"""

    @pytest.mark.asyncio
    async def test_connect_success(self):
        """接続成功のテスト"""
        from tengin_mcp.infrastructure.adapters.chromadb_adapter import ChromaDBAdapter

        settings = create_mock_settings(chromadb_path="/tmp/test_chromadb")
        adapter = ChromaDBAdapter(settings)

        mock_client = MagicMock()
        mock_collection = MagicMock()
        mock_client.get_or_create_collection.return_value = mock_collection

        with patch('tengin_mcp.infrastructure.adapters.chromadb_adapter.chromadb.PersistentClient') as mock_persistent:
            mock_persistent.return_value = mock_client

            await adapter.connect()

            mock_persistent.assert_called_once()
            mock_client.get_or_create_collection.assert_called_once_with(
                name="education_theories",
                metadata={"description": "Education theory embeddings"},
            )
            assert adapter._client == mock_client
            assert adapter._collection == mock_collection

    @pytest.mark.asyncio
    async def test_connect_failure(self):
        """接続失敗のテスト"""
        from tengin_mcp.infrastructure.adapters.chromadb_adapter import ChromaDBAdapter

        settings = create_mock_settings(chromadb_path="/tmp/test_chromadb")
        adapter = ChromaDBAdapter(settings)

        with patch('tengin_mcp.infrastructure.adapters.chromadb_adapter.chromadb.PersistentClient') as mock_persistent:
            mock_persistent.side_effect = Exception("Connection failed")

            with pytest.raises(Exception, match="Connection failed"):
                await adapter.connect()

    @pytest.mark.asyncio
    async def test_close(self):
        """クローズのテスト"""
        from tengin_mcp.infrastructure.adapters.chromadb_adapter import ChromaDBAdapter

        settings = create_mock_settings()
        adapter = ChromaDBAdapter(settings)
        adapter._client = MagicMock()
        adapter._collection = MagicMock()

        await adapter.close()

        assert adapter._client is None
        assert adapter._collection is None


class TestChromaDBAdapterCollection:
    """コレクションプロパティのテスト"""

    def test_collection_not_connected(self):
        """未接続時にエラー"""
        from tengin_mcp.infrastructure.adapters.chromadb_adapter import ChromaDBAdapter

        settings = create_mock_settings()
        adapter = ChromaDBAdapter(settings)

        with pytest.raises(RuntimeError, match="ChromaDB not connected"):
            _ = adapter.collection

    def test_collection_connected(self):
        """接続時にコレクション返却"""
        from tengin_mcp.infrastructure.adapters.chromadb_adapter import ChromaDBAdapter

        settings = create_mock_settings()
        adapter = ChromaDBAdapter(settings)
        mock_collection = MagicMock()
        adapter._collection = mock_collection

        assert adapter.collection == mock_collection


class TestChromaDBAdapterDocuments:
    """ドキュメント操作のテスト"""

    @pytest.mark.asyncio
    async def test_add_documents_basic(self):
        """基本的なドキュメント追加"""
        from tengin_mcp.infrastructure.adapters.chromadb_adapter import ChromaDBAdapter

        settings = create_mock_settings()
        adapter = ChromaDBAdapter(settings)
        mock_collection = MagicMock()
        adapter._collection = mock_collection

        await adapter.add_documents(
            ids=["id1", "id2"],
            documents=["doc1", "doc2"],
        )

        mock_collection.add.assert_called_once_with(
            ids=["id1", "id2"],
            documents=["doc1", "doc2"],
        )

    @pytest.mark.asyncio
    async def test_add_documents_with_embeddings(self):
        """埋め込み付きドキュメント追加"""
        from tengin_mcp.infrastructure.adapters.chromadb_adapter import ChromaDBAdapter

        settings = create_mock_settings()
        adapter = ChromaDBAdapter(settings)
        mock_collection = MagicMock()
        adapter._collection = mock_collection

        await adapter.add_documents(
            ids=["id1"],
            documents=["doc1"],
            embeddings=[[0.1, 0.2, 0.3]],
        )

        mock_collection.add.assert_called_once_with(
            ids=["id1"],
            documents=["doc1"],
            embeddings=[[0.1, 0.2, 0.3]],
        )

    @pytest.mark.asyncio
    async def test_add_documents_with_metadatas(self):
        """メタデータ付きドキュメント追加"""
        from tengin_mcp.infrastructure.adapters.chromadb_adapter import ChromaDBAdapter

        settings = create_mock_settings()
        adapter = ChromaDBAdapter(settings)
        mock_collection = MagicMock()
        adapter._collection = mock_collection

        await adapter.add_documents(
            ids=["id1"],
            documents=["doc1"],
            metadatas=[{"category": "learning"}],
        )

        mock_collection.add.assert_called_once_with(
            ids=["id1"],
            documents=["doc1"],
            metadatas=[{"category": "learning"}],
        )

    @pytest.mark.asyncio
    async def test_add_documents_full(self):
        """全オプション付きドキュメント追加"""
        from tengin_mcp.infrastructure.adapters.chromadb_adapter import ChromaDBAdapter

        settings = create_mock_settings()
        adapter = ChromaDBAdapter(settings)
        mock_collection = MagicMock()
        adapter._collection = mock_collection

        await adapter.add_documents(
            ids=["id1"],
            documents=["doc1"],
            embeddings=[[0.1, 0.2]],
            metadatas=[{"key": "value"}],
        )

        mock_collection.add.assert_called_once_with(
            ids=["id1"],
            documents=["doc1"],
            embeddings=[[0.1, 0.2]],
            metadatas=[{"key": "value"}],
        )


class TestChromaDBAdapterSearch:
    """検索のテスト"""

    @pytest.mark.asyncio
    async def test_search_basic(self):
        """基本的なベクトル検索"""
        from tengin_mcp.infrastructure.adapters.chromadb_adapter import ChromaDBAdapter

        settings = create_mock_settings()
        adapter = ChromaDBAdapter(settings)
        mock_collection = MagicMock()
        mock_collection.query.return_value = {"ids": [["id1"]], "documents": [["doc1"]]}
        adapter._collection = mock_collection

        result = await adapter.search(
            query_embedding=[0.1, 0.2, 0.3],
            n_results=5,
        )

        mock_collection.query.assert_called_once_with(
            query_embeddings=[[0.1, 0.2, 0.3]],
            n_results=5,
            include=["documents", "metadatas", "distances"],
        )
        assert result == {"ids": [["id1"]], "documents": [["doc1"]]}

    @pytest.mark.asyncio
    async def test_search_with_where(self):
        """フィルタ付きベクトル検索"""
        from tengin_mcp.infrastructure.adapters.chromadb_adapter import ChromaDBAdapter

        settings = create_mock_settings()
        adapter = ChromaDBAdapter(settings)
        mock_collection = MagicMock()
        mock_collection.query.return_value = {"ids": [["id1"]]}
        adapter._collection = mock_collection

        await adapter.search(
            query_embedding=[0.1, 0.2],
            n_results=10,
            where={"category": "learning"},
        )

        mock_collection.query.assert_called_once_with(
            query_embeddings=[[0.1, 0.2]],
            n_results=10,
            include=["documents", "metadatas", "distances"],
            where={"category": "learning"},
        )

    @pytest.mark.asyncio
    async def test_search_by_text_basic(self):
        """基本的なテキスト検索"""
        from tengin_mcp.infrastructure.adapters.chromadb_adapter import ChromaDBAdapter

        settings = create_mock_settings()
        adapter = ChromaDBAdapter(settings)
        mock_collection = MagicMock()
        mock_collection.query.return_value = {"ids": [["id1"]], "documents": [["doc1"]]}
        adapter._collection = mock_collection

        result = await adapter.search_by_text(
            query_text="constructivism",
            n_results=5,
        )

        mock_collection.query.assert_called_once_with(
            query_texts=["constructivism"],
            n_results=5,
            include=["documents", "metadatas", "distances"],
        )

    @pytest.mark.asyncio
    async def test_search_by_text_with_where(self):
        """フィルタ付きテキスト検索"""
        from tengin_mcp.infrastructure.adapters.chromadb_adapter import ChromaDBAdapter

        settings = create_mock_settings()
        adapter = ChromaDBAdapter(settings)
        mock_collection = MagicMock()
        mock_collection.query.return_value = {"ids": [["id1"]]}
        adapter._collection = mock_collection

        await adapter.search_by_text(
            query_text="piaget",
            n_results=3,
            where={"category": "developmental"},
        )

        mock_collection.query.assert_called_once_with(
            query_texts=["piaget"],
            n_results=3,
            include=["documents", "metadatas", "distances"],
            where={"category": "developmental"},
        )


class TestChromaDBAdapterCount:
    """カウントのテスト"""

    @pytest.mark.asyncio
    async def test_get_count(self):
        """ドキュメント数取得"""
        from tengin_mcp.infrastructure.adapters.chromadb_adapter import ChromaDBAdapter

        settings = create_mock_settings()
        adapter = ChromaDBAdapter(settings)
        mock_collection = MagicMock()
        mock_collection.count.return_value = 42
        adapter._collection = mock_collection

        count = await adapter.get_count()

        mock_collection.count.assert_called_once()
        assert count == 42
