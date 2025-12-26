"""Infrastructure: Neo4j Adapter."""

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

from neo4j import AsyncDriver, AsyncGraphDatabase, AsyncSession

from tengin_mcp.domain.errors import DatabaseConnectionError
from tengin_mcp.infrastructure.config import Settings

logger = logging.getLogger(__name__)


class Neo4jAdapter:
    """Neo4j データベースアダプター。"""

    def __init__(self, settings: Settings) -> None:
        """
        Neo4jアダプターを初期化。

        Args:
            settings: アプリケーション設定
        """
        self._settings = settings
        self._driver: AsyncDriver | None = None

    async def connect(self) -> None:
        """Neo4jに接続。"""
        try:
            self._driver = AsyncGraphDatabase.driver(
                self._settings.neo4j_uri,
                auth=(self._settings.neo4j_user, self._settings.neo4j_password),
            )
            # 接続テスト
            async with self._driver.session() as session:
                await session.run("RETURN 1")
            logger.info("Connected to Neo4j at %s", self._settings.neo4j_uri)
        except Exception as e:
            raise DatabaseConnectionError(f"Failed to connect to Neo4j: {e}") from e

    async def close(self) -> None:
        """接続を閉じる。"""
        if self._driver:
            await self._driver.close()
            self._driver = None
            logger.info("Disconnected from Neo4j")

    @asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        """セッションのコンテキストマネージャ。"""
        if not self._driver:
            raise DatabaseConnectionError("Not connected to Neo4j")
        async with self._driver.session() as session:
            yield session

    async def execute_query(
        self,
        query: str,
        parameters: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """
        Cypherクエリを実行。

        Args:
            query: Cypherクエリ文字列
            parameters: クエリパラメータ

        Returns:
            結果のリスト
        """
        async with self.session() as session:
            result = await session.run(query, parameters or {})
            records = await result.data()
            return records

    async def execute_write(
        self,
        query: str,
        parameters: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        書き込みクエリを実行。

        Args:
            query: Cypherクエリ文字列
            parameters: クエリパラメータ

        Returns:
            実行結果のサマリ
        """
        async with self.session() as session:
            result = await session.run(query, parameters or {})
            summary = await result.consume()
            return {
                "nodes_created": summary.counters.nodes_created,
                "nodes_deleted": summary.counters.nodes_deleted,
                "relationships_created": summary.counters.relationships_created,
                "relationships_deleted": summary.counters.relationships_deleted,
                "properties_set": summary.counters.properties_set,
            }
