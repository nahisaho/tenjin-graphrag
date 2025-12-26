"""
MCPツールの動作確認スクリプト

使用方法:
    uv run python -m tengin_mcp.scripts.verify_tools

このスクリプトはNeo4jに接続し、各MCPツールの動作を確認します。
"""

import asyncio
import json
from typing import Any

from tengin_mcp.infrastructure.adapters.chromadb_adapter import ChromaDBAdapter
from tengin_mcp.infrastructure.adapters.embedding_adapter import EmbeddingAdapter
from tengin_mcp.infrastructure.adapters.neo4j_adapter import Neo4jAdapter
from tengin_mcp.infrastructure.config import Settings


def print_section(title: str) -> None:
    """セクションヘッダーを表示"""
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}")


def print_result(name: str, result: Any, max_items: int = 3) -> None:
    """結果を表示"""
    print(f"\n[{name}]")
    if isinstance(result, list):
        print(f"  件数: {len(result)}")
        for i, item in enumerate(result[:max_items]):
            if isinstance(item, dict):
                preview = json.dumps(item, ensure_ascii=False)[:200]
                print(f"  [{i + 1}] {preview}...")
            else:
                print(f"  [{i + 1}] {item}")
        if len(result) > max_items:
            print(f"  ... 他 {len(result) - max_items} 件")
    elif isinstance(result, dict):
        print(f"  {json.dumps(result, ensure_ascii=False, indent=4)[:500]}")
    else:
        print(f"  {result}")


async def verify_theory_queries(neo4j: Neo4jAdapter) -> None:
    """理論関連クエリの動作確認"""
    print_section("理論クエリ動作確認")

    # 1. 全理論を取得
    theories = await neo4j.execute_query(
        "MATCH (t:Theory) RETURN t.id as id, t.name as name, t.category as category LIMIT 10"
    )
    print_result("全理論一覧", theories)

    # 2. IDで理論を取得
    theory = await neo4j.execute_query(
        "MATCH (t:Theory {id: $id}) RETURN t", parameters={"id": "cognitive-load-theory"}
    )
    if theory:
        print_result("認知負荷理論の詳細", theory[0]["t"])

    # 3. カテゴリで検索
    by_category = await neo4j.execute_query(
        "MATCH (t:Theory) WHERE t.category = $cat RETURN t.id, t.name",
        parameters={"cat": "learning"},
    )
    print_result("カテゴリ 'learning' の理論", by_category)

    # 4. 理論家を取得
    theorists = await neo4j.execute_query(
        "MATCH (t:Theorist) RETURN t.id as id, t.name as name, t.nationality as nationality LIMIT 5"
    )
    print_result("理論家一覧", theorists)

    # 5. 概念を取得
    concepts = await neo4j.execute_query(
        "MATCH (c:Concept) RETURN c.id as id, c.name as name, c.name_en as name_en LIMIT 5"
    )
    print_result("概念一覧", concepts)

    # 6. 原則を取得
    principles = await neo4j.execute_query(
        "MATCH (p:Principle) RETURN p.id as id, p.name as name LIMIT 5"
    )
    print_result("原則一覧", principles)

    # 7. エビデンスを取得
    evidence = await neo4j.execute_query(
        "MATCH (e:Evidence) RETURN e.id as id, e.title as title, e.year as year LIMIT 5"
    )
    print_result("エビデンス一覧", evidence)


async def verify_graph_queries(neo4j: Neo4jAdapter) -> None:
    """グラフ関連クエリの動作確認"""
    print_section("グラフクエリ動作確認")

    # 1. グラフ統計
    stats = await neo4j.execute_query(
        """
        MATCH (n)
        RETURN labels(n)[0] as label, count(n) as count
        ORDER BY count DESC
        """
    )
    stats_dict = {r["label"]: r["count"] for r in stats}
    print_result("グラフ統計", stats_dict)

    # 2. 関係タイプ統計
    rel_stats = await neo4j.execute_query(
        "MATCH ()-[r]->() RETURN type(r) as type, count(r) as count ORDER BY count DESC"
    )
    print_result("関係タイプ統計", rel_stats)

    # 3. グラフ探索 - 認知負荷理論からの関連
    traversal = await neo4j.execute_query(
        """
        MATCH (t:Theory {id: $id})-[r]->(related)
        RETURN type(r) as rel_type, labels(related)[0] as label, related.id as id, related.name as name
        """,
        parameters={"id": "cognitive-load-theory"},
    )
    print_result("認知負荷理論からの関連ノード", traversal)


async def verify_chromadb(adapter: ChromaDBAdapter, embedding: EmbeddingAdapter | None) -> None:
    """ChromaDBの動作確認"""
    print_section("ChromaDB + Embedding 動作確認")

    # コレクションを取得
    collection = adapter.collection
    print(f"  Collection: {collection.name}")
    print(f"  Document count: {collection.count()}")

    if embedding is None:
        print("  ⚠ OpenAI APIキーが設定されていないため、埋め込みテストをスキップします")
        print("  ヒント: OPENAI_API_KEY環境変数を設定してください")
        return

    # テストドキュメントを追加
    test_docs = [
        "認知負荷理論はワーキングメモリの制限が学習に与える影響を説明します。",
        "構成主義は学習者が能動的に知識を構築するという考え方です。",
        "発達の最近接領域は独力と支援による達成の間の領域を指します。",
    ]

    try:
        # 埋め込みを生成
        embeddings = await embedding.embed_texts(test_docs)
        print(f"  Generated {len(embeddings)} embeddings")
        print(f"  Embedding dimension: {len(embeddings[0])}")

        # ドキュメントを追加（既存の場合はスキップ）
        if collection.count() == 0:
            ids = [f"test-doc-{i}" for i in range(len(test_docs))]
            await adapter.add_documents(ids=ids, documents=test_docs, embeddings=embeddings)
            print(f"  Added {len(test_docs)} documents")
        else:
            print(f"  Documents already exist: {collection.count()}")

        # 検索テスト
        query = "学習者の記憶容量について"
        query_embedding = await embedding.embed_text(query)
        results = await adapter.search(query_embedding=query_embedding, n_results=2)
        docs = results.get("documents", [[]])[0]
        print_result(f"Search: '{query}'", docs)
    except Exception as e:
        print(f"  ⚠ 埋め込みエラー: {e}")


async def main():
    """メイン関数"""
    print("=" * 60)
    print("  TENGIN GraphRAG - MCPツール動作確認")
    print("=" * 60)

    settings = Settings()

    # Neo4j接続
    neo4j = Neo4jAdapter(settings)
    await neo4j.connect()
    print("✓ Neo4jに接続しました")

    # ChromaDB接続
    chromadb = ChromaDBAdapter(settings)
    await chromadb.connect()
    print("✓ ChromaDBに接続しました")

    # Embedding初期化（esperantoによるマルチプロバイダー対応）
    embedding: EmbeddingAdapter | None = None
    provider = settings.embedding_provider

    # プロバイダーに応じたAPIキーチェック
    can_use_embedding = False
    if provider == "ollama":
        # Ollamaはローカルなのでキー不要
        can_use_embedding = True
    elif provider == "transformers":
        # Transformersはローカルなのでキー不要
        can_use_embedding = True
    elif provider == "openai":
        can_use_embedding = bool(
            settings.openai_api_key and settings.openai_api_key != "your-openai-api-key-here"
        )
    elif provider == "google":
        can_use_embedding = bool(settings.google_api_key)
    elif provider == "mistral":
        can_use_embedding = bool(settings.mistral_api_key)
    elif provider == "voyage":
        can_use_embedding = bool(settings.voyage_api_key)
    elif provider == "jina":
        can_use_embedding = bool(settings.jina_api_key)
    elif provider == "azure":
        can_use_embedding = bool(settings.azure_openai_api_key and settings.azure_openai_endpoint)
    elif provider == "openai-compatible":
        can_use_embedding = bool(settings.openai_compatible_base_url)

    if can_use_embedding:
        try:
            embedding = EmbeddingAdapter(settings)
            await embedding.connect()
            print(
                f"✓ Embeddingアダプタを初期化しました (provider={embedding.provider}, model={embedding.model})"
            )
        except Exception as e:
            print(f"⚠ Embeddingアダプタの初期化に失敗: {e}")
            embedding = None
    else:
        print(f"⚠ プロバイダー '{provider}' のAPIキーが未設定のため、埋め込み機能はスキップします")
        print("  ヒント: OllamaやTransformersはローカルで動作します（APIキー不要）")
        print("    EMBEDDING_PROVIDER=ollama")
        print("    EMBEDDING_MODEL=nomic-embed-text")

    try:
        # 動作確認
        await verify_theory_queries(neo4j)
        await verify_graph_queries(neo4j)
        await verify_chromadb(chromadb, embedding)

        print_section("動作確認完了")
        print("✓ すべてのツールが正常に動作しています！")

    finally:
        if embedding:
            await embedding.close()
        await chromadb.close()
        await neo4j.close()
        print("\n✓ すべての接続を閉じました")


if __name__ == "__main__":
    asyncio.run(main())
