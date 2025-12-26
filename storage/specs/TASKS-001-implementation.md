# タスク分解: 教育理論GraphRAG MCPサーバー

**ID**: TASKS-001
**Feature**: Education Theory GraphRAG MCP Server
**Version**: 2.0
**Created**: 2025-12-25
**Updated**: 2025-12-26
**Status**: ✅ Complete
**Related**: REQ-001 v2.0, DESIGN-001 v2.0, ADR-001, ADR-002

---

## 実装フェーズ概要

| Phase | 名称 | タスク数 | 見積もり | 状態 |
|-------|------|---------|---------|------|
| 1 | プロジェクト初期化 | 4 | 1.5h | ✅ 完了 |
| 2 | ドメイン層実装 | 5 | 3h | ✅ 完了 |
| 3 | インフラ層実装 | 4 | 4h | ✅ 完了 |
| 4 | MCPサーバー基盤 | 3 | 2h | ✅ 完了 |
| 5 | MCP Tools実装 | 4 | 5h | ✅ 完了 |
| 6 | MCP Resources実装 | 2 | 2h | ✅ 完了 |
| 7 | MCP Prompts実装 | 2 | 2h | ✅ 完了 |
| 8 | 教育理論データ作成 | 3 | 6h | ✅ 完了 |
| 9 | テスト・検証 | 3 | 3h | ✅ 完了 |

**合計**: 30タスク, 約28.5時間 → **全タスク完了**

---

## Phase 1: プロジェクト初期化

### TASK-1.1: プロジェクト構造作成
**Priority**: P0 (Critical)
**Estimate**: 20min
**Dependencies**: None

```
作業内容:
- [ ] src/tengin_mcp/ ディレクトリ構造作成
- [ ] data/ ディレクトリ構造作成
- [ ] tests/ ディレクトリ構造作成
```

**完了条件**:
- DESIGN-001のディレクトリ構造に準拠

---

### TASK-1.2: pyproject.toml作成（uv）
**Priority**: P0 (Critical)
**Estimate**: 20min
**Dependencies**: TASK-1.1

```
作業内容:
- [ ] pyproject.toml 作成
- [ ] MCP SDK依存関係 (mcp[cli])
- [ ] Neo4j, ChromaDB, OpenAI依存関係
- [ ] 開発依存関係（pytest, ruff, mypy）
- [ ] uv sync 実行
```

**完了条件**:
- `uv sync` が成功
- `uv run python -c "import mcp"` が動作

---

### TASK-1.3: 開発ツール設定
**Priority**: P1 (High)
**Estimate**: 15min
**Dependencies**: TASK-1.2

```
作業内容:
- [ ] ruff設定（pyproject.toml内）
- [ ] mypy設定
- [ ] .gitignore更新
```

**完了条件**:
- `uv run ruff check .` がパス
- `uv run mypy .` がパス

---

### TASK-1.4: Docker環境構築
**Priority**: P1 (High)
**Estimate**: 30min
**Dependencies**: TASK-1.1

```
作業内容:
- [ ] docker-compose.yml 作成（Neo4j）
- [ ] .env.example 作成
- [ ] docker compose up で起動確認
```

**完了条件**:
- Neo4jがlocalhost:7474でアクセス可能

---

## Phase 2: ドメイン層実装

### TASK-2.1: 基本エンティティ定義
**Priority**: P0 (Critical)
**Estimate**: 40min
**Dependencies**: TASK-1.2

```
ファイル: src/tengin_mcp/domain/entities/

作業内容:
- [ ] theory.py - Theory dataclass
- [ ] concept.py - Concept dataclass
- [ ] theorist.py - Theorist dataclass
- [ ] __init__.py - エクスポート
```

**完了条件**:
- Pydantic BaseModelで定義
- 型ヒント完備

---

### TASK-2.2: 追加エンティティ定義
**Priority**: P0 (Critical)
**Estimate**: 30min
**Dependencies**: TASK-2.1

```
ファイル: src/tengin_mcp/domain/entities/

作業内容:
- [ ] principle.py - Principle dataclass
- [ ] evidence.py - Evidence dataclass
```

**完了条件**:
- ADR-002のスキーマに準拠

---

### TASK-2.3: Value Objects定義
**Priority**: P1 (High)
**Estimate**: 20min
**Dependencies**: TASK-2.1

```
ファイル: src/tengin_mcp/domain/value_objects/

作業内容:
- [ ] theory_category.py - TheoryCategory Enum
- [ ] evidence_level.py - EvidenceLevel Enum
- [ ] citation_format.py - CitationFormat Enum
```

**完了条件**:
- Enumで定義

---

### TASK-2.4: リポジトリインターフェース定義
**Priority**: P0 (Critical)
**Estimate**: 30min
**Dependencies**: TASK-2.1

```
ファイル: src/tengin_mcp/domain/repositories/

作業内容:
- [ ] theory_repository.py - TheoryRepository Protocol
- [ ] graph_repository.py - GraphRepository Protocol
```

**完了条件**:
- Python Protocol で定義
- 非同期メソッド（async）

---

### TASK-2.5: ドメインエラー定義
**Priority**: P1 (High)
**Estimate**: 15min
**Dependencies**: TASK-2.1

```
ファイル: src/tengin_mcp/domain/errors.py

作業内容:
- [ ] TheoryNotFoundError
- [ ] InvalidQueryError
- [ ] GraphTraversalError
```

**完了条件**:
- カスタム例外クラス定義

---

## Phase 3: インフラ層実装

### TASK-3.1: Neo4jアダプター実装
**Priority**: P0 (Critical)
**Estimate**: 60min
**Dependencies**: TASK-2.4, TASK-1.4

```
ファイル: src/tengin_mcp/infrastructure/adapters/neo4j_adapter.py

作業内容:
- [ ] Neo4jAdapter クラス
- [ ] 接続管理（async context manager）
- [ ] Cypherクエリ実行
```

**完了条件**:
- Neo4jへの接続成功
- 基本クエリ実行可能

---

### TASK-3.2: Neo4jリポジトリ実装
**Priority**: P0 (Critical)
**Estimate**: 60min
**Dependencies**: TASK-3.1

```
ファイル: src/tengin_mcp/infrastructure/repositories/

作業内容:
- [ ] neo4j_theory_repository.py
- [ ] neo4j_graph_repository.py
- [ ] Cypherクエリ実装
```

**完了条件**:
- TheoryRepository実装
- グラフトラバーサル実装

---

### TASK-3.3: ChromaDBアダプター実装
**Priority**: P0 (Critical)
**Estimate**: 45min
**Dependencies**: TASK-1.2

```
ファイル: src/tengin_mcp/infrastructure/adapters/chromadb_adapter.py

作業内容:
- [ ] ChromaDBAdapter クラス
- [ ] コレクション管理
- [ ] ベクトル検索実装
```

**完了条件**:
- ベクトル追加・検索が動作

---

### TASK-3.4: Embeddingアダプター実装
**Priority**: P0 (Critical)
**Estimate**: 30min
**Dependencies**: TASK-1.2

```
ファイル: src/tengin_mcp/infrastructure/adapters/embedding_adapter.py

作業内容:
- [ ] EmbeddingAdapter クラス
- [ ] OpenAI Embedding API呼び出し
```

**完了条件**:
- テキストから埋め込みベクトル生成

---

## Phase 4: MCPサーバー基盤

### TASK-4.1: MCPサーバーエントリーポイント
**Priority**: P0 (Critical)
**Estimate**: 45min
**Dependencies**: TASK-1.2

```
ファイル: src/tengin_mcp/server.py

作業内容:
- [ ] FastMCP インスタンス作成
- [ ] サーバー設定
- [ ] main() エントリーポイント
- [ ] pyproject.toml に scripts 追加
```

**完了条件**:
- `uv run tengin-server` で起動
- `mcp dev src/tengin_mcp/server.py` で動作確認

---

### TASK-4.2: 設定管理
**Priority**: P1 (High)
**Estimate**: 20min
**Dependencies**: TASK-4.1

```
ファイル: src/tengin_mcp/infrastructure/config.py

作業内容:
- [ ] Settings クラス（pydantic-settings）
- [ ] 環境変数読み込み
- [ ] Neo4j, ChromaDB, OpenAI設定
```

**完了条件**:
- 環境変数から設定読み込み

---

### TASK-4.3: 依存性注入設定
**Priority**: P1 (High)
**Estimate**: 30min
**Dependencies**: TASK-4.1, TASK-3.1, TASK-3.3

```
ファイル: src/tengin_mcp/server.py

作業内容:
- [ ] lifespan でDB接続初期化
- [ ] サービスインスタンス管理
```

**完了条件**:
- サーバー起動時にDB接続
- サーバー終了時にクリーンアップ

---

## Phase 5: MCP Tools実装

### TASK-5.1: 検索系Tools実装
**Priority**: P0 (Critical)
**Estimate**: 90min
**Dependencies**: TASK-4.1, TASK-3.2, TASK-3.3

```
ファイル: src/tengin_mcp/tools/search.py

作業内容:
- [ ] @mcp.tool() search_theories
- [ ] @mcp.tool() find_applicable_theories
- [ ] SearchService実装
```

**完了条件**:
- TOOL-001, TOOL-004 準拠
- セマンティック検索動作

---

### TASK-5.2: 理論系Tools実装
**Priority**: P0 (Critical)
**Estimate**: 60min
**Dependencies**: TASK-4.1, TASK-3.2

```
ファイル: src/tengin_mcp/tools/theory.py

作業内容:
- [ ] @mcp.tool() get_theory
- [ ] @mcp.tool() get_principles
- [ ] @mcp.tool() get_evidence
```

**完了条件**:
- TOOL-002, TOOL-007, TOOL-008 準拠

---

### TASK-5.3: グラフ系Tools実装
**Priority**: P0 (Critical)
**Estimate**: 60min
**Dependencies**: TASK-4.1, TASK-3.2

```
ファイル: src/tengin_mcp/tools/graph.py

作業内容:
- [ ] @mcp.tool() traverse_graph
- [ ] GraphService実装
```

**完了条件**:
- TOOL-003 準拠
- BFS/DFSトラバーサル

---

### TASK-5.4: 引用・比較系Tools実装
**Priority**: P1 (High)
**Estimate**: 60min
**Dependencies**: TASK-4.1, TASK-3.2

```
ファイル: 
- src/tengin_mcp/tools/citation.py
- src/tengin_mcp/tools/compare.py

作業内容:
- [ ] @mcp.tool() cite_theory
- [ ] @mcp.tool() compare_theories
- [ ] CitationService実装
```

**完了条件**:
- TOOL-005, TOOL-006 準拠
- APA7, MLA9, Chicago形式対応

---

## Phase 6: MCP Resources実装

### TASK-6.1: Theory/Concept Resources
**Priority**: P1 (High)
**Estimate**: 60min
**Dependencies**: TASK-4.1, TASK-3.2

```
ファイル:
- src/tengin_mcp/resources/theory_resources.py
- src/tengin_mcp/resources/concept_resources.py

作業内容:
- [ ] @mcp.resource() theory://list
- [ ] @mcp.resource() theory://{category}/list
- [ ] @mcp.resource() theory://{id}
- [ ] @mcp.resource() concept://{id}
- [ ] @mcp.resource() theorist://{id}
- [ ] @mcp.resource() evidence://{theory_id}
```

**完了条件**:
- URI templateでリソース取得

---

### TASK-6.2: Graph Resources
**Priority**: P2 (Medium)
**Estimate**: 30min
**Dependencies**: TASK-4.1, TASK-3.2

```
ファイル: src/tengin_mcp/resources/graph_resources.py

作業内容:
- [ ] @mcp.resource() graph://schema
- [ ] @mcp.resource() graph://stats
```

**完了条件**:
- グラフメタ情報取得

---

## Phase 7: MCP Prompts実装

### TASK-7.1: 授業設計系Prompts
**Priority**: P1 (High)
**Estimate**: 60min
**Dependencies**: TASK-4.1

```
ファイル:
- src/tengin_mcp/prompts/lesson_prompts.py
- src/tengin_mcp/prompts/assessment_prompts.py

作業内容:
- [ ] @mcp.prompt() design_lesson
- [ ] @mcp.prompt() create_assessment
- [ ] @mcp.prompt() curriculum_plan
```

**完了条件**:
- PROMPT-001, PROMPT-002, PROMPT-005 準拠

---

### TASK-7.2: 理論系Prompts
**Priority**: P1 (High)
**Estimate**: 45min
**Dependencies**: TASK-4.1

```
ファイル: src/tengin_mcp/prompts/theory_prompts.py

作業内容:
- [ ] @mcp.prompt() explain_theory
- [ ] @mcp.prompt() apply_theory
- [ ] @mcp.prompt() troubleshoot_learning
```

**完了条件**:
- PROMPT-003, PROMPT-004, PROMPT-006 準拠

---

## Phase 8: 教育理論データ作成

### TASK-8.1: データスキーマ定義
**Priority**: P0 (Critical)
**Estimate**: 30min
**Dependencies**: TASK-2.1

```
ファイル: data/schema/theory_schema.json

作業内容:
- [ ] JSON Schema定義
```

**完了条件**:
- バリデーション可能

---

### TASK-8.2: 教育理論データ作成
**Priority**: P0 (Critical)
**Estimate**: 240min (4h)
**Dependencies**: TASK-8.1

```
ファイル: data/theories/

作業内容:
- [ ] learning_theories.json（行動主義、認知主義、構成主義）
- [ ] instructional_theories.json（ガニェ、メリル、ARCS）
- [ ] developmental_theories.json（ピアジェ、ヴィゴツキー）
- [ ] motivation_theories.json（自己決定、フロー）
```

**完了条件**:
- 各カテゴリ5-10理論
- 概念・原則・エビデンス含む

---

### TASK-8.3: リレーションシップデータ作成
**Priority**: P0 (Critical)
**Estimate**: 90min
**Dependencies**: TASK-8.2

```
ファイル: data/relationships/theory_relationships.json

作業内容:
- [ ] BASED_ON, EXTENDS, CONTRADICTS リレーション
- [ ] PROPOSED_BY リレーション
```

**完了条件**:
- 理論間の関係定義

---

## Phase 9: テスト・検証

### TASK-9.1: ユニットテスト
**Priority**: P0 (Critical)
**Estimate**: 60min
**Dependencies**: Phase 5, 6, 7

```
作業内容:
- [ ] ドメインエンティティテスト
- [ ] サービステスト（モック使用）
- [ ] Toolsテスト
```

**完了条件**:
- pytest --cov で70%以上

---

### TASK-9.2: 統合テスト
**Priority**: P0 (Critical)
**Estimate**: 60min
**Dependencies**: TASK-9.1

```
作業内容:
- [ ] Neo4j統合テスト
- [ ] MCP Inspector でのテスト
```

**完了条件**:
- `mcp dev` で全Tools動作確認

---

### TASK-9.3: Claude Desktop連携テスト
**Priority**: P1 (High)
**Estimate**: 45min
**Dependencies**: TASK-9.2

```
作業内容:
- [ ] claude_desktop_config.json 作成
- [ ] Claude Desktopで動作確認
- [ ] 全Tools/Resources/Prompts確認
```

**完了条件**:
- Claude Desktopから全機能利用可能

---

## 依存関係グラフ

```
Phase 1 (初期化)
    │
    ├─► Phase 2 (ドメイン)
    │       │
    │       ├─► Phase 3 (インフラ)
    │       │       │
    │       │       └─► Phase 4 (MCP基盤)
    │       │               │
    │       │               ├─► Phase 5 (Tools)
    │       │               ├─► Phase 6 (Resources)
    │       │               └─► Phase 7 (Prompts)
    │       │
    │       └─► Phase 8 (データ)
    │
    └─► Phase 9 (テスト) ─────────────────────►
```

---

## 実装順序

```
TASK-1.1 → TASK-1.2 → TASK-1.3 → TASK-1.4
                │
                ▼
        TASK-2.1 → TASK-2.2 → TASK-2.3 → TASK-2.4 → TASK-2.5
                │
                ▼
        TASK-3.1 → TASK-3.2 ─┐
        TASK-3.3 → TASK-3.4 ─┤
                             │
                             ▼
                     TASK-4.1 → TASK-4.2 → TASK-4.3
                             │
                             ▼
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
    TASK-5.1~5.4       TASK-6.1~6.2        TASK-7.1~7.2
        │                    │                    │
        └────────────────────┼────────────────────┘
                             │
                             ▼
                     TASK-8.1 → TASK-8.2 → TASK-8.3
                             │
                             ▼
                     TASK-9.1 → TASK-9.2 → TASK-9.3
```

---

## 変更履歴

| バージョン | 日付 | 変更者 | 変更内容 |
|-----------|------|--------|---------|
| 1.0 | 2025-12-25 | GitHub Copilot | 初版（REST API版） |
| 2.0 | 2025-12-25 | GitHub Copilot | MCP準拠に再構成 |
