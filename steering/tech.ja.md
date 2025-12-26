# Technology Stack

**Project**: TENGIN-GraphRAG
**Last Updated**: 2025-12-26
**Status**: 実装済み (ADR-001)

---

## Overview

教育理論GraphRAGシステムのための技術スタック。MCPサーバーとしてLLMアプリケーションとの統合を実現。GraphRAG実装の実績とPythonエコシステムの成熟度を重視して選定。

## 技術スタック概要

| カテゴリ | 技術 | バージョン | 用途 |
|---------|------|-----------|------|
| 言語 | Python | 3.11+ | メイン開発言語 |
| MCP Framework | FastMCP (mcp[cli]) | 1.0+ | MCPサーバー実装（23ツール） |
| Graph DB | Neo4j | 5.x | ナレッジグラフ格納（130ノード、303関係） |
| Vector DB | ChromaDB | 0.4+ | ベクトル検索 |
| Embedding | Esperanto | 2.9+ | マルチプロバイダー埋め込み |
| Data Validation | Pydantic | 2.0+ | データバリデーション |
| Caching | SimpleCache | - | インメモリTTLキャッシュ |
| Testing | pytest | 7.0+ | テストフレームワーク（391テスト、96%カバレッジ） |
| Linting | ruff | 0.1+ | コード品質 |
| Container | Docker Compose | latest | 開発環境 |

---

## 詳細

### プログラミング言語

**Python 3.11+**

```
理由:
- ML/AIエコシステムが最も充実
- GraphRAG実装（LangChain, LlamaIndex）がPython主体
- Neo4j, ChromaDB等のクライアントが最も成熟
- 開発チームの経験
```

主要ライブラリ:
- `neo4j` - Neo4j Python Driver
- `chromadb` - Vector Database
- `openai` - OpenAI API Client
- `sentence-transformers` - Embedding Models
- `pydantic` - Data Validation
- `typer` - CLI Framework

---

### グラフデータベース

**Neo4j 5.x**

```
理由:
- 最も成熟したグラフDB
- Cypher言語による直感的なクエリ
- Neo4j Bloom/Browserによる可視化
- Community Editionで開発可能
```

開発環境:
- Neo4j Desktop (ローカル)
- Neo4j AuraDB Free (クラウド開発)

本番環境:
- Neo4j AuraDB Professional
- セルフホスト (Docker)

---

### ベクトルデータベース

**ChromaDB (開発) / Qdrant (本番)**

```
ChromaDB:
- 軽量でPython native
- ローカル開発で即座に使用可能
- Embeddingのストレージ

Qdrant:
- 高性能、フィルタリング強力
- セルフホスト可能
- 本番環境でのスケーラビリティ
```

---

### Web APIフレームワーク

**FastAPI**

```
理由:
- 非同期処理（LLM API呼び出しに最適）
- Pydanticによる自動バリデーション
- OpenAPI (Swagger) 自動生成
- 型ヒントによる開発体験向上
```

---

### LLM統合

**OpenAI API (GPT-4)**

```
プロバイダ:
- OpenAI API (デフォルト)
- Azure OpenAI Service (エンタープライズ)
- Anthropic Claude (オプション)
- Ollama (ローカル開発)

埋め込みモデル:
- text-embedding-3-small (OpenAI)
- sentence-transformers (ローカル)
```

---

### 開発ツール

| ツール | 用途 |
|--------|------|
| Poetry | 依存関係管理 |
| Ruff | Linter / Formatter |
| mypy | 静的型チェック |
| Docker Compose | ローカル環境構築 |

---

## 依存関係

### pyproject.toml (主要依存)

```toml
[project]
name = "tengin-mcp"
version = "0.1.0"
requires-python = ">=3.11"

dependencies = [
    # MCP SDK
    "mcp[cli]>=1.0.0",
    
    # Data validation
    "pydantic>=2.0.0",
    "pydantic-settings>=2.0.0",
    
    # Database - Graph
    "neo4j>=5.0.0",
    
    # Database - Vector
    "chromadb>=0.4.0",
    
    # LLM/Embeddings - Multi-provider support
    "esperanto>=2.9.0",
    
    # Async support
    "httpx>=0.25.0",
    
    # Utilities
    "python-dotenv>=1.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
    "pytest-cov>=4.0.0",
    "ruff>=0.1.0",
    "mypy>=1.0.0",
]
```

---

## 環境構成

### 開発環境

```yaml
# docker-compose.yml
services:
  neo4j:
    image: neo4j:5-community
    ports:
      - "7474:7474"  # Browser
      - "7687:7687"  # Bolt
    environment:
      NEO4J_AUTH: neo4j/password
```

### 環境変数

```env
# .env.example
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password

# Embedding Provider (esperanto)
EMBEDDING_PROVIDER=openai
OPENAI_API_KEY=sk-xxx

CHROMA_PERSIST_DIR=./data/chromadb

LOG_LEVEL=INFO
```

### MCPサーバー起動

```bash
# 開発環境での起動
cd /path/to/TENGIN-GraphRAG
uv run mcp run src/tengin_mcp/server.py
```

---

## 関連ADR

- [ADR-001: 技術スタック選定](../storage/specs/ADR-001-technology-stack.md)
- [ADR-002: グラフスキーマ設計](../storage/specs/ADR-002-graph-schema.md)

---

*技術スタックの詳細な決定理由はADR-001を参照*
