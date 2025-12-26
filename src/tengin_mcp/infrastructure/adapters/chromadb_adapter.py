"""Infrastructure: ChromaDB Adapter."""

import logging
from pathlib import Path
from typing import Any

import chromadb
from chromadb.config import Settings as ChromaSettings

from tengin_mcp.infrastructure.config import Settings

logger = logging.getLogger(__name__)


class ChromaDBAdapter:
    """ChromaDB ベクトルデータベースアダプター。"""

    COLLECTION_NAME = "education_theories"

    def __init__(self, settings: Settings) -> None:
        """
        ChromaDBアダプターを初期化。

        Args:
            settings: アプリケーション設定
        """
        self._settings = settings
        self._client: chromadb.ClientAPI | None = None
        self._collection: chromadb.Collection | None = None

    async def connect(self) -> None:
        """ChromaDBに接続（永続化モード）。"""
        try:
            # ディレクトリを作成
            db_path = Path(self._settings.chromadb_path)
            db_path.mkdir(parents=True, exist_ok=True)

            # 永続化クライアントを作成
            self._client = chromadb.PersistentClient(
                path=str(db_path),
                settings=ChromaSettings(anonymized_telemetry=False),
            )

            # コレクションを取得または作成
            self._collection = self._client.get_or_create_collection(
                name=self.COLLECTION_NAME,
                metadata={"description": "Education theory embeddings"},
            )

            logger.info("Connected to ChromaDB at %s", db_path)
        except Exception as e:
            logger.error("Failed to connect to ChromaDB: %s", e)
            raise

    async def close(self) -> None:
        """接続を閉じる（ChromaDBは自動永続化）。"""
        self._collection = None
        self._client = None
        logger.info("Disconnected from ChromaDB")

    @property
    def collection(self) -> chromadb.Collection:
        """コレクションを取得。"""
        if not self._collection:
            raise RuntimeError("ChromaDB not connected")
        return self._collection

    async def add_documents(
        self,
        ids: list[str],
        documents: list[str],
        embeddings: list[list[float]] | None = None,
        metadatas: list[dict[str, Any]] | None = None,
    ) -> None:
        """
        ドキュメントを追加。

        Args:
            ids: ドキュメントID
            documents: ドキュメントテキスト
            embeddings: 埋め込みベクトル（オプション）
            metadatas: メタデータ（オプション）
        """
        kwargs: dict[str, Any] = {
            "ids": ids,
            "documents": documents,
        }
        if embeddings:
            kwargs["embeddings"] = embeddings
        if metadatas:
            kwargs["metadatas"] = metadatas

        self.collection.add(**kwargs)

    async def search(
        self,
        query_embedding: list[float],
        n_results: int = 5,
        where: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        ベクトル検索。

        Args:
            query_embedding: クエリの埋め込みベクトル
            n_results: 返す結果数
            where: フィルタ条件

        Returns:
            検索結果
        """
        kwargs: dict[str, Any] = {
            "query_embeddings": [query_embedding],
            "n_results": n_results,
            "include": ["documents", "metadatas", "distances"],
        }
        if where:
            kwargs["where"] = where

        results = self.collection.query(**kwargs)
        return results

    async def search_by_text(
        self,
        query_text: str,
        n_results: int = 5,
        where: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        テキストで検索（ChromaDBの内蔵埋め込みを使用）。

        Args:
            query_text: 検索クエリ
            n_results: 返す結果数
            where: フィルタ条件

        Returns:
            検索結果
        """
        kwargs: dict[str, Any] = {
            "query_texts": [query_text],
            "n_results": n_results,
            "include": ["documents", "metadatas", "distances"],
        }
        if where:
            kwargs["where"] = where

        results = self.collection.query(**kwargs)
        return results

    async def get_count(self) -> int:
        """コレクション内のドキュメント数を取得。"""
        return self.collection.count()
