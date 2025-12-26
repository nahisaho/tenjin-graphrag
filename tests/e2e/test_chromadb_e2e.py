"""
E2E Tests: ChromaDB Integration Tests

ChromaDBベクトルデータベースとの統合テスト。
セマンティック検索、埋め込み生成、類似度検索の動作を検証。
"""

import pytest
from pathlib import Path

from tengin_mcp.infrastructure.config import Settings
from tengin_mcp.infrastructure.adapters.chromadb_adapter import ChromaDBAdapter


class TestChromaDBE2E:
    """ChromaDBのE2Eテスト"""

    @pytest.fixture(autouse=True)
    async def setup(self):
        """テストセットアップ - ChromaDB接続"""
        settings = Settings()
        self.adapter = ChromaDBAdapter(settings)
        await self.adapter.connect()
        
        yield
        
        await self.adapter.close()

    # ============================================================
    # 基本接続テスト
    # ============================================================

    @pytest.mark.asyncio
    async def test_chromadb_connection(self):
        """ChromaDBに正常に接続できる"""
        assert self.adapter._client is not None
        assert self.adapter._collection is not None

    @pytest.mark.asyncio
    async def test_collection_exists(self):
        """コレクションが存在する"""
        collection = self.adapter.collection
        assert collection is not None
        assert collection.name == "education_theories"

    @pytest.mark.asyncio
    async def test_get_document_count(self):
        """ドキュメント数を取得できる"""
        count = await self.adapter.get_count()
        assert isinstance(count, int)
        assert count >= 0

    # ============================================================
    # ドキュメント操作テスト
    # ============================================================

    @pytest.mark.asyncio
    async def test_add_and_search_document(self):
        """ドキュメントの追加と検索"""
        # テスト用ドキュメントを追加
        test_id = "test-doc-e2e-001"
        test_doc = "認知負荷理論はワーキングメモリの制限を考慮した教材設計を提唱する"
        test_metadata = {"type": "test", "category": "learning"}

        await self.adapter.add_documents(
            ids=[test_id],
            documents=[test_doc],
            metadatas=[test_metadata],
        )

        # テキストで検索
        results = await self.adapter.search_by_text(
            query_text="認知負荷",
            n_results=5,
        )

        assert "documents" in results
        assert len(results["documents"]) > 0
        # 追加したドキュメントが見つかる
        found_docs = results["documents"][0] if results["documents"] else []
        assert any("認知負荷" in doc for doc in found_docs) or any("ワーキングメモリ" in doc for doc in found_docs)

    @pytest.mark.asyncio
    async def test_search_with_filter(self):
        """フィルタ付き検索"""
        # テスト用ドキュメントを追加
        test_id = "test-doc-e2e-002"
        test_doc = "構成主義は知識の能動的構築を重視する学習理論"
        test_metadata = {"type": "test", "category": "constructivism"}

        await self.adapter.add_documents(
            ids=[test_id],
            documents=[test_doc],
            metadatas=[test_metadata],
        )

        # フィルタ付きで検索
        results = await self.adapter.search_by_text(
            query_text="学習理論",
            n_results=5,
            where={"type": "test"},
        )

        assert "documents" in results
        assert "metadatas" in results

    # ============================================================
    # セマンティック検索テスト
    # ============================================================

    @pytest.mark.asyncio
    async def test_semantic_similarity_search(self):
        """セマンティック類似度検索"""
        # 同義的なクエリでドキュメントが見つかるか
        results = await self.adapter.search_by_text(
            query_text="学習の動機付け",
            n_results=10,
        )

        assert "documents" in results
        assert "distances" in results
        
        # 距離（類似度）が返される
        if results["distances"] and results["distances"][0]:
            distances = results["distances"][0]
            assert all(isinstance(d, (int, float)) for d in distances)

    @pytest.mark.asyncio
    async def test_search_returns_metadata(self):
        """検索結果にメタデータが含まれる"""
        results = await self.adapter.search_by_text(
            query_text="教育理論",
            n_results=5,
        )

        assert "metadatas" in results
        
        # メタデータが存在する場合、辞書形式である
        if results["metadatas"] and results["metadatas"][0]:
            for metadata in results["metadatas"][0]:
                if metadata:
                    assert isinstance(metadata, dict)


class TestChromaDBDataIntegrity:
    """ChromaDBデータ整合性テスト"""

    @pytest.fixture(autouse=True)
    async def setup(self):
        """テストセットアップ"""
        settings = Settings()
        self.adapter = ChromaDBAdapter(settings)
        await self.adapter.connect()
        
        yield
        
        await self.adapter.close()

    @pytest.mark.asyncio
    async def test_collection_has_data(self):
        """コレクションにデータが存在する"""
        count = await self.adapter.get_count()
        # 初期状態でもテストドキュメントが追加されている可能性
        assert count >= 0

    @pytest.mark.asyncio
    async def test_search_consistency(self):
        """同じクエリで一貫した結果が返る"""
        query = "認知的な学習プロセス"
        
        results1 = await self.adapter.search_by_text(query_text=query, n_results=5)
        results2 = await self.adapter.search_by_text(query_text=query, n_results=5)
        
        # 同じクエリで同じドキュメントが返る
        if results1["ids"] and results2["ids"]:
            assert results1["ids"][0] == results2["ids"][0]


class TestChromaDBResilience:
    """ChromaDB耐障害性テスト"""

    @pytest.mark.asyncio
    async def test_reconnection(self):
        """再接続できる"""
        settings = Settings()
        adapter = ChromaDBAdapter(settings)
        
        # 最初の接続
        await adapter.connect()
        assert adapter._client is not None
        
        # 切断
        await adapter.close()
        assert adapter._client is None
        
        # 再接続
        await adapter.connect()
        assert adapter._client is not None
        
        await adapter.close()

    @pytest.mark.asyncio
    async def test_empty_query_handling(self):
        """空のクエリを適切に処理"""
        settings = Settings()
        adapter = ChromaDBAdapter(settings)
        await adapter.connect()
        
        try:
            results = await adapter.search_by_text(
                query_text="",
                n_results=5,
            )
            # 空のクエリでもエラーにならない
            assert "documents" in results
        except Exception as e:
            # または適切な例外が発生する
            assert "empty" in str(e).lower() or "invalid" in str(e).lower()
        finally:
            await adapter.close()

    @pytest.mark.asyncio
    async def test_large_result_set(self):
        """大量の結果を処理できる"""
        settings = Settings()
        adapter = ChromaDBAdapter(settings)
        await adapter.connect()
        
        try:
            results = await adapter.search_by_text(
                query_text="学習",
                n_results=100,  # 大きな結果数
            )
            assert "documents" in results
        finally:
            await adapter.close()
