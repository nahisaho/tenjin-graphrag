# TENGIN Education Theory MCP Server

教育理論ナレッジグラフを提供するMCPサーバー。

## 概要

TENGIN Education Theory MCP Serverは、教育理論のナレッジグラフをModel Context Protocol (MCP)を通じて提供します。Claude Desktop、VS Code、その他のMCP対応AIアプリケーションから、教育理論に基づいたエビデンスベースのコンテンツ生成が可能になります。

## 機能

### MCP Tools
- `search_theories` - 教育理論をセマンティック検索
- `get_theory` - 特定の理論の詳細を取得
- `traverse_graph` - 理論間の関係をトラバース
- `find_applicable_theories` - コンテキストに適用可能な理論を検索
- `cite_theory` - 理論の引用情報を生成
- `compare_theories` - 複数理論を比較
- `get_evidence` - 理論のエビデンスを取得
- `get_principles` - 理論の原則・原理を取得

### MCP Resources
- `theory://list` - 全理論のリスト
- `theory://{id}` - 特定理論の詳細
- `concept://{id}` - 概念の詳細
- `graph://schema` - グラフスキーマ情報

### MCP Prompts
- `design_lesson` - 理論に基づいた授業設計
- `create_assessment` - 評価方法の設計
- `explain_theory` - 理論の分かりやすい説明生成

### マルチプロバイダー対応 (esperanto)

[esperanto](https://github.com/lfnovo/esperanto)ライブラリを使用し、様々なLLM/埋め込みプロバイダーをサポート:

| プロバイダー | モデル例 | APIキー |
|------------|---------|--------|
| **OpenAI** | text-embedding-3-small, text-embedding-3-large | 必要 |
| **Google** | text-embedding-004, embedding-001 | 必要 |
| **Ollama** | nomic-embed-text, mxbai-embed-large | 不要（ローカル） |
| **Mistral** | mistral-embed | 必要 |
| **Voyage** | voyage-3, voyage-2 | 必要 |
| **Jina** | jina-embeddings-v3 | 必要 |
| **Azure OpenAI** | text-embedding-3-small | 必要 |
| **Transformers** | BAAI/bge-small-en-v1.5 | 不要（ローカル） |
| **OpenAI互換** | LM Studio, vLLM等 | エンドポイント依存 |

## セットアップ

### 前提条件
- Python 3.11+
- Docker（Neo4j用）
- uv（パッケージマネージャー）

### インストール

```bash
# リポジトリをクローン
git clone https://github.com/your-org/TENGIN-GraphRAG.git
cd TENGIN-GraphRAG

# 依存関係をインストール
uv sync

# 環境変数を設定
cp .env.example .env
# .envファイルを編集してAPIキーを設定

# Neo4jを起動
docker compose up -d
```

### 埋め込みプロバイダーの設定

`.env`ファイルで使用するプロバイダーを指定:

```bash
# OpenAI（クラウド）
EMBEDDING_PROVIDER=openai
EMBEDDING_MODEL=text-embedding-3-small
OPENAI_API_KEY=sk-xxx

# Ollama（ローカル、APIキー不要）
EMBEDDING_PROVIDER=ollama
EMBEDDING_MODEL=nomic-embed-text
OLLAMA_BASE_URL=http://localhost:11434

# Google Gemini
EMBEDDING_PROVIDER=google
EMBEDDING_MODEL=text-embedding-004
GOOGLE_API_KEY=xxx

# Transformers（ローカル、自動ダウンロード）
EMBEDDING_PROVIDER=transformers
EMBEDDING_MODEL=BAAI/bge-small-en-v1.5
```

### データのシーディング

初回セットアップ時にサンプルデータをNeo4jに投入します：

```bash
# サンプルデータを投入
uv run python -m tengin_mcp.scripts.seed_data
```

投入されるデータ:
- 教育理論 8件（認知負荷理論、構成主義、発達の最近接領域など）
- 理論家 8名（ジョン・スウェラー、ジャン・ピアジェなど）
- 概念 8件（内的負荷、外的負荷など）
- 原則 8件（分割注意効果、冗長性効果など）
- エビデンス 5件（研究論文）
- 関係 20+件

### サーバー起動

```bash
# STDIOモード（Claude Desktop/VS Code用）
uv run tengin-server

# 開発モード（MCP Inspector）
uv run mcp dev src/tengin_mcp/server.py
```

### 動作確認

```bash
# MCPツールの動作検証
uv run python -m tengin_mcp.scripts.verify_tools
```

## Claude Desktop連携

`claude_desktop_config.json`に以下を追加:

```json
{
  "mcpServers": {
    "tengin-education": {
      "command": "uv",
      "args": ["--directory", "/path/to/TENGIN-GraphRAG", "run", "tengin-server"],
      "env": {
        "NEO4J_URI": "bolt://localhost:7687",
        "NEO4J_USER": "neo4j",
        "NEO4J_PASSWORD": "password"
      }
    }
  }
}
```

詳細な連携方法については [docs/MCP_INTEGRATION.md](docs/MCP_INTEGRATION.md) を参照してください。

## 開発

```bash
# テスト実行
uv run pytest

# 統合テスト実行（Neo4jが起動している状態で）
uv run pytest tests/integration/

# 型チェック
uv run mypy src/

# Lint
uv run ruff check src/
```

## プロジェクト構造

```
src/tengin_mcp/
├── domain/                 # ドメイン層
│   ├── entities/           # エンティティ（Theory, Theorist等）
│   ├── repositories/       # リポジトリインターフェース
│   └── value_objects/      # 値オブジェクト
├── infrastructure/         # インフラ層
│   └── adapters/           # Neo4j, ChromaDB, Embedding
├── mcp/                    # MCP層
│   ├── tools/              # MCPツール
│   ├── resources/          # MCPリソース
│   └── prompts/            # MCPプロンプト
├── scripts/                # ユーティリティスクリプト
│   ├── seed_data.py        # データシーディング
│   └── verify_tools.py     # ツール動作検証
└── server.py               # MCPサーバーエントリーポイント
```

## ドキュメント

| ドキュメント | 説明 |
|------------|------|
| [API リファレンス](docs/API_REFERENCE.md) | 全19ツール・5リソース・3プロンプトの詳細仕様 |
| [使用ガイド](docs/USAGE_GUIDE.md) | 実践的なユースケース別ガイド |
| [MCP 統合ガイド](docs/MCP_INTEGRATION.md) | Claude Desktop・VS Code等との連携設定 |
| [教育理論概要](docs/EDUCATION_THEORIES.md) | 収録されている教育理論の概要 |

## ライセンス

MIT License
