"""TENGIN MCP Server: Main entry point."""

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

from mcp.server.fastmcp import FastMCP

from tengin_mcp.infrastructure import (
    ChromaDBAdapter,
    EmbeddingAdapter,
    Neo4jAdapter,
    Neo4jGraphRepository,
    Neo4jTheoryRepository,
    get_settings,
)

# ロギング設定
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


# アプリケーション状態
class AppState:
    """アプリケーション状態を管理。"""

    def __init__(self) -> None:
        self.settings = get_settings()
        self.neo4j_adapter: Neo4jAdapter | None = None
        self.chromadb_adapter: ChromaDBAdapter | None = None
        self.embedding_adapter: EmbeddingAdapter | None = None
        self.theory_repository: Neo4jTheoryRepository | None = None
        self.graph_repository: Neo4jGraphRepository | None = None


app_state = AppState()


@asynccontextmanager
async def lifespan(server: FastMCP) -> AsyncIterator[dict[str, Any]]:
    """
    MCPサーバーのライフサイクル管理。

    Args:
        server: FastMCPサーバーインスタンス

    Yields:
        依存関係を含む辞書
    """
    logger.info("Starting TENGIN MCP Server...")

    # アダプターを初期化
    app_state.neo4j_adapter = Neo4jAdapter(app_state.settings)
    app_state.chromadb_adapter = ChromaDBAdapter(app_state.settings)
    app_state.embedding_adapter = EmbeddingAdapter(app_state.settings)

    try:
        # 接続
        await app_state.neo4j_adapter.connect()
        await app_state.chromadb_adapter.connect()
        await app_state.embedding_adapter.connect()

        # リポジトリを初期化
        app_state.theory_repository = Neo4jTheoryRepository(app_state.neo4j_adapter)
        app_state.graph_repository = Neo4jGraphRepository(app_state.neo4j_adapter)

        logger.info("All connections established")

        yield {
            "settings": app_state.settings,
            "neo4j": app_state.neo4j_adapter,
            "chromadb": app_state.chromadb_adapter,
            "embedding": app_state.embedding_adapter,
            "theory_repo": app_state.theory_repository,
            "graph_repo": app_state.graph_repository,
        }

    finally:
        # クリーンアップ
        logger.info("Shutting down TENGIN MCP Server...")
        if app_state.embedding_adapter:
            await app_state.embedding_adapter.close()
        if app_state.chromadb_adapter:
            await app_state.chromadb_adapter.close()
        if app_state.neo4j_adapter:
            await app_state.neo4j_adapter.close()
        logger.info("All connections closed")


# FastMCPサーバーを作成
mcp = FastMCP(
    "TENGIN Education Theory GraphRAG",
    lifespan=lifespan,
)

# Tools, Resources, Prompts を登録（デコレータ経由）
# これらのインポートは mcp インスタンス作成後に行う必要がある
import tengin_mcp.prompts.education_prompts  # noqa: E402, F401
import tengin_mcp.resources.theory_resources  # noqa: E402, F401
import tengin_mcp.tools.citation_tools  # noqa: E402, F401
import tengin_mcp.tools.graph_tools  # noqa: E402, F401
import tengin_mcp.tools.theory_tools  # noqa: E402, F401


def main() -> None:
    """MCPサーバーを起動。"""

    logger.info("Starting TENGIN MCP Server on stdio...")
    mcp.run()


if __name__ == "__main__":
    main()
