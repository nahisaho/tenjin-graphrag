# Claude Desktop / Cursor 統合設定

TENGIN GraphRAG MCPサーバーをClaude DesktopやCursorと統合するための設定方法です。

## Claude Desktop の設定

### macOS
`~/Library/Application Support/Claude/claude_desktop_config.json` を編集：

```json
{
  "mcpServers": {
    "tengin-graphrag": {
      "command": "uv",
      "args": ["run", "tengin-server"],
      "cwd": "/path/to/TENGIN-GraphRAG",
      "env": {
        "NEO4J_URI": "bolt://localhost:7687",
        "NEO4J_USER": "neo4j",
        "NEO4J_PASSWORD": "password",
        "CHROMADB_PATH": "./data/chromadb",
        "OPENAI_API_KEY": "your-openai-api-key"
      }
    }
  }
}
```

### Windows
`%APPDATA%\Claude\claude_desktop_config.json` を編集：

```json
{
  "mcpServers": {
    "tengin-graphrag": {
      "command": "uv",
      "args": ["run", "tengin-server"],
      "cwd": "C:\\path\\to\\TENGIN-GraphRAG",
      "env": {
        "NEO4J_URI": "bolt://localhost:7687",
        "NEO4J_USER": "neo4j",
        "NEO4J_PASSWORD": "password",
        "CHROMADB_PATH": "./data/chromadb",
        "OPENAI_API_KEY": "your-openai-api-key"
      }
    }
  }
}
```

## Cursor の設定

`.cursor/mcp.json` を編集：

```json
{
  "mcpServers": {
    "tengin-graphrag": {
      "command": "uv",
      "args": ["run", "tengin-server"],
      "cwd": "/path/to/TENGIN-GraphRAG"
    }
  }
}
```

## VS Code Agent の設定

`.vscode/settings.json` に追加：

```json
{
  "mcp": {
    "servers": {
      "tengin-graphrag": {
        "command": "uv",
        "args": ["run", "tengin-server"],
        "cwd": "${workspaceFolder}"
      }
    }
  }
}
```

## 利用可能な機能

### Tools (ツール)
- `search_theories` - 理論の検索（キーワード、カテゴリ、エビデンスレベル）
- `get_theory` - 特定の理論の詳細取得
- `get_theories_by_category` - カテゴリ別理論一覧
- `get_theorist` - 理論家の詳細取得
- `get_concept` - 概念の詳細取得
- `get_principle` - 原則の詳細取得
- `get_evidence` - エビデンスの詳細取得
- `traverse_graph` - グラフの探索（関連ノード取得）
- `find_path` - 2ノード間の経路探索
- `get_related_nodes` - 関連ノードの取得
- `get_graph_statistics` - グラフ統計情報
- `cite_theory` - 引用文生成（APA7, MLA9, Chicago, Harvard, IEEE）
- `compare_theories` - 理論の比較分析

### Resources (リソース)
- `theory://{theory_id}` - 理論の詳細情報
- `concept://{concept_id}` - 概念の情報
- `theorist://{theorist_id}` - 理論家の情報
- `evidence://{evidence_id}` - エビデンスの情報
- `graph://statistics` - グラフ統計情報

### Prompts (プロンプト)
- `design_lesson` - 授業設計支援
- `create_assessment` - 評価設計支援
- `explain_theory` - 理論の説明生成
- `apply_theory` - 理論の適用ガイド
- `curriculum_plan` - カリキュラム計画支援
- `troubleshoot_learning` - 学習問題の診断

## 使用例

### 理論検索
```
認知負荷理論について教えてください
```

### 授業設計
```
「分数の足し算」について、小学4年生向けの45分の授業を設計してください
```

### 理論の比較
```
構成主義と認知負荷理論の違いを比較してください
```

## トラブルシューティング

### サーバーが起動しない場合
1. Neo4jが起動しているか確認: `docker compose ps`
2. `.env` ファイルが正しく設定されているか確認
3. 依存関係をインストール: `uv sync --all-extras`

### データが見つからない場合
1. データ投入スクリプトを実行: `uv run python -m tengin_mcp.scripts.seed_data`

### 接続エラーの場合
1. Neo4jのポート(7687)が開いているか確認
2. ファイアウォール設定を確認
