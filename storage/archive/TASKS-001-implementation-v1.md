# タスク分解: 教育理論GraphRAGシステム

**ID**: TASKS-001
**Feature**: Education Theory GraphRAG System
**Version**: 1.0
**Created**: 2025-12-25
**Status**: Ready for Implementation
**Related**: REQ-001, DESIGN-001, ADR-001, ADR-002

---

## 実装フェーズ概要

| Phase | 名称 | タスク数 | 見積もり |
|-------|------|---------|---------|
| 1 | プロジェクト初期化 | 5 | 2h |
| 2 | ドメイン層実装 | 6 | 4h |
| 3 | インフラ層実装 | 6 | 6h |
| 4 | 教育理論データ作成 | 4 | 8h |
| 5 | アプリケーション層実装 | 6 | 8h |
| 6 | API実装 | 5 | 4h |
| 7 | CLI実装 | 4 | 3h |
| 8 | テスト・検証 | 4 | 4h |

**合計**: 40タスク, 約39時間

---

## Phase 1: プロジェクト初期化

### TASK-1.1: Pythonプロジェクト構造作成
**Priority**: P0 (Critical)
**Estimate**: 30min
**Dependencies**: None

```
作業内容:
- [ ] lib/graphrag-core/ ディレクトリ作成
- [ ] lib/education-theories-data/ ディレクトリ作成
- [ ] api/ ディレクトリ作成
- [ ] cli/ ディレクトリ作成
- [ ] ルートpyproject.toml作成
```

**完了条件**:
- ディレクトリ構造がDESIGN-001に準拠
- Article I (Library-First) に準拠

---

### TASK-1.2: Poetry依存関係設定
**Priority**: P0 (Critical)
**Estimate**: 20min
**Dependencies**: TASK-1.1

```
作業内容:
- [ ] lib/graphrag-core/pyproject.toml 作成
- [ ] 依存関係定義（neo4j, chromadb, openai, pydantic, etc.）
- [ ] 開発依存関係定義（pytest, ruff, mypy）
- [ ] poetry install 実行
```

**完了条件**:
- `poetry install` が成功
- 仮想環境が作成される

---

### TASK-1.3: 開発ツール設定
**Priority**: P1 (High)
**Estimate**: 20min
**Dependencies**: TASK-1.2

```
作業内容:
- [ ] ruff.toml 設定（Linter/Formatter）
- [ ] mypy.ini 設定（型チェック）
- [ ] .pre-commit-config.yaml 設定
- [ ] .gitignore 更新
```

**完了条件**:
- `ruff check .` がパス
- `mypy .` がパス

---

### TASK-1.4: Docker環境構築
**Priority**: P1 (High)
**Estimate**: 30min
**Dependencies**: TASK-1.1

```
作業内容:
- [ ] docker-compose.yml 作成（Neo4j, API）
- [ ] Dockerfile 作成（API用）
- [ ] .env.example 作成
- [ ] docker compose up で起動確認
```

**完了条件**:
- Neo4jがlocalhost:7474でアクセス可能
- Neo4j Browserで接続確認

---

### TASK-1.5: CI/CD基盤設定
**Priority**: P2 (Medium)
**Estimate**: 20min
**Dependencies**: TASK-1.3

```
作業内容:
- [ ] .github/workflows/ci.yml 作成
- [ ] テスト、Lint、型チェックのジョブ定義
```

**完了条件**:
- GitHub Actionsが正常に実行

---

## Phase 2: ドメイン層実装

### TASK-2.1: 基本エンティティ定義
**Priority**: P0 (Critical)
**Estimate**: 45min
**Dependencies**: TASK-1.2

```
ファイル: lib/graphrag-core/src/domain/entities/

作業内容:
- [ ] theory.py - Theoryエンティティ
- [ ] concept.py - Conceptエンティティ
- [ ] theorist.py - Theoristエンティティ
- [ ] __init__.py - エクスポート
```

**完了条件**:
- Pydantic BaseModelで定義
- 型ヒント完備
- 単体テストパス

---

### TASK-2.2: 追加エンティティ定義
**Priority**: P0 (Critical)
**Estimate**: 30min
**Dependencies**: TASK-2.1

```
ファイル: lib/graphrag-core/src/domain/entities/

作業内容:
- [ ] principle.py - Principleエンティティ
- [ ] evidence.py - Evidenceエンティティ
- [ ] application_context.py - ApplicationContextエンティティ
```

**完了条件**:
- ADR-002のスキーマに準拠
- 単体テストパス

---

### TASK-2.3: Value Objects定義
**Priority**: P1 (High)
**Estimate**: 30min
**Dependencies**: TASK-2.1

```
ファイル: lib/graphrag-core/src/domain/value_objects/

作業内容:
- [ ] theory_category.py - TheoryCategory Enum
- [ ] evidence_level.py - EvidenceLevel Enum
- [ ] relationship_type.py - RelationshipType Enum
```

**完了条件**:
- Enumで定義
- バリデーション付き

---

### TASK-2.4: リレーションシップ定義
**Priority**: P1 (High)
**Estimate**: 30min
**Dependencies**: TASK-2.1, TASK-2.3

```
ファイル: lib/graphrag-core/src/domain/entities/relationship.py

作業内容:
- [ ] Relationshipベースクラス
- [ ] 各リレーションシップタイプ（PROPOSED_BY, BASED_ON, etc.）
- [ ] リレーションシップファクトリ
```

**完了条件**:
- ADR-002の全リレーションシップをサポート
- 型安全なリレーション作成

---

### TASK-2.5: リポジトリインターフェース定義
**Priority**: P0 (Critical)
**Estimate**: 45min
**Dependencies**: TASK-2.1, TASK-2.4

```
ファイル: lib/graphrag-core/src/domain/repositories/

作業内容:
- [ ] theory_repository.py - TheoryRepository Protocol
- [ ] concept_repository.py - ConceptRepository Protocol
- [ ] graph_repository.py - GraphRepository Protocol
```

**完了条件**:
- Python Protocol で定義
- CRUD + 検索メソッド定義
- Article III準拠（テスト先行）

---

### TASK-2.6: ドメインエラー定義
**Priority**: P1 (High)
**Estimate**: 20min
**Dependencies**: TASK-2.1

```
ファイル: lib/graphrag-core/src/domain/errors.py

作業内容:
- [ ] TheoryNotFoundError
- [ ] InvalidRelationshipError
- [ ] DuplicateEntityError
- [ ] GraphTraversalError
```

**完了条件**:
- カスタム例外クラス定義
- エラーコード付与

---

## Phase 3: インフラ層実装

### TASK-3.1: Neo4jアダプター基盤
**Priority**: P0 (Critical)
**Estimate**: 60min
**Dependencies**: TASK-2.5, TASK-1.4

```
ファイル: lib/graphrag-core/src/infrastructure/adapters/neo4j_adapter.py

作業内容:
- [ ] Neo4jConnection クラス
- [ ] 接続プール管理
- [ ] トランザクション管理
- [ ] Cypher実行ヘルパー
```

**完了条件**:
- Neo4jへの接続成功
- 統合テストパス（実Neo4j使用 - Article IX）

---

### TASK-3.2: Neo4jリポジトリ実装
**Priority**: P0 (Critical)
**Estimate**: 90min
**Dependencies**: TASK-3.1

```
ファイル: lib/graphrag-core/src/infrastructure/repositories/

作業内容:
- [ ] neo4j_theory_repository.py
- [ ] neo4j_concept_repository.py
- [ ] neo4j_graph_repository.py
- [ ] Cypherクエリ実装
```

**完了条件**:
- CRUD操作の実装
- グラフトラバーサル実装
- 統合テストパス

---

### TASK-3.3: ChromaDBアダプター
**Priority**: P0 (Critical)
**Estimate**: 60min
**Dependencies**: TASK-1.2

```
ファイル: lib/graphrag-core/src/infrastructure/adapters/chromadb_adapter.py

作業内容:
- [ ] ChromaDBConnection クラス
- [ ] コレクション管理
- [ ] ベクトル検索実装
```

**完了条件**:
- ベクトル追加・検索が動作
- 統合テストパス

---

### TASK-3.4: Embeddingサービス
**Priority**: P0 (Critical)
**Estimate**: 45min
**Dependencies**: TASK-1.2

```
ファイル: lib/graphrag-core/src/infrastructure/embeddings/embedding_service.py

作業内容:
- [ ] EmbeddingService インターフェース
- [ ] OpenAIEmbedding 実装
- [ ] SentenceTransformerEmbedding 実装（ローカル用）
```

**完了条件**:
- テキストから埋め込みベクトル生成
- 複数プロバイダ切り替え可能

---

### TASK-3.5: LLMクライアント
**Priority**: P0 (Critical)
**Estimate**: 45min
**Dependencies**: TASK-1.2

```
ファイル: lib/graphrag-core/src/infrastructure/adapters/llm_client.py

作業内容:
- [ ] LLMClient Protocol定義
- [ ] OpenAIClient 実装
- [ ] プロンプトテンプレート管理
```

**完了条件**:
- OpenAI APIへの接続成功
- ストリーミングレスポンス対応

---

### TASK-3.6: グラフスキーマ初期化
**Priority**: P1 (High)
**Estimate**: 30min
**Dependencies**: TASK-3.1

```
ファイル: lib/graphrag-core/src/infrastructure/migrations/

作業内容:
- [ ] init_schema.py - 制約・インデックス作成
- [ ] ADR-002のスキーマを実装
```

**完了条件**:
- Neo4jにスキーマが適用される
- マイグレーションスクリプト実行可能

---

## Phase 4: 教育理論データ作成

### TASK-4.1: データスキーマ定義
**Priority**: P0 (Critical)
**Estimate**: 30min
**Dependencies**: TASK-2.1

```
ファイル: lib/education-theories-data/data/schema/

作業内容:
- [ ] theory_schema.json - JSON Schema定義
- [ ] relationship_schema.json
```

**完了条件**:
- JSON Schemaでバリデーション可能

---

### TASK-4.2: 学習理論データ作成
**Priority**: P0 (Critical)
**Estimate**: 120min
**Dependencies**: TASK-4.1

```
ファイル: lib/education-theories-data/data/theories/learning_theories.json

作業内容:
- [ ] 行動主義（Pavlov, Skinner, Bandura）
- [ ] 認知主義（情報処理, スキーマ, 認知負荷）
- [ ] 構成主義（Piaget, Vygotsky, Bruner）
- [ ] 接続主義（Siemens）
```

**完了条件**:
- 15以上の理論を定義
- 各理論に概念・原則を関連付け

---

### TASK-4.3: 教授・発達・動機付け理論データ
**Priority**: P0 (Critical)
**Estimate**: 180min
**Dependencies**: TASK-4.1

```
ファイル: lib/education-theories-data/data/theories/

作業内容:
- [ ] instructional_theories.json（ガニェ, メリル, ARCS, Bloom）
- [ ] developmental_theories.json（Piaget, Vygotsky, Erikson）
- [ ] motivation_theories.json（自己決定, フロー, 達成目標）
```

**完了条件**:
- 各カテゴリ8-10理論
- エビデンスレベル付与

---

### TASK-4.4: リレーションシップデータ作成
**Priority**: P0 (Critical)
**Estimate**: 90min
**Dependencies**: TASK-4.2, TASK-4.3

```
ファイル: lib/education-theories-data/data/relationships/theory_relationships.json

作業内容:
- [ ] BASED_ON リレーション
- [ ] EXTENDS リレーション
- [ ] CONTRADICTS リレーション
- [ ] PROPOSED_BY リレーション
```

**完了条件**:
- 理論間の関係が定義される
- グラフとして整合性あり

---

## Phase 5: アプリケーション層実装

### TASK-5.1: DTOs定義
**Priority**: P1 (High)
**Estimate**: 30min
**Dependencies**: TASK-2.1

```
ファイル: lib/graphrag-core/src/application/dto/

作業内容:
- [ ] query_request.py - QueryRequest
- [ ] query_response.py - QueryResponse
- [ ] theory_dto.py - TheoryDTO
```

**完了条件**:
- Pydantic BaseModelで定義
- シリアライズ/デシリアライズ可能

---

### TASK-5.2: QueryService実装
**Priority**: P0 (Critical)
**Estimate**: 90min
**Dependencies**: TASK-3.3, TASK-3.4

```
ファイル: lib/graphrag-core/src/application/services/query_service.py

作業内容:
- [ ] セマンティック検索実装
- [ ] ハイブリッド検索（キーワード + ベクトル）
- [ ] リランキング実装
```

**完了条件**:
- FR-007準拠
- 関連度スコア付き結果

---

### TASK-5.3: GraphService実装
**Priority**: P0 (Critical)
**Estimate**: 90min
**Dependencies**: TASK-3.2

```
ファイル: lib/graphrag-core/src/application/services/graph_service.py

作業内容:
- [ ] グラフCRUD操作
- [ ] グラフトラバーサル（BFS/DFS）
- [ ] サブグラフ抽出
- [ ] インポート/エクスポート
```

**完了条件**:
- FR-005, FR-008準拠
- 任意の深度でトラバーサル可能

---

### TASK-5.4: RAGOrchestrator実装
**Priority**: P0 (Critical)
**Estimate**: 120min
**Dependencies**: TASK-5.2, TASK-5.3, TASK-3.5

```
ファイル: lib/graphrag-core/src/application/services/rag_orchestrator.py

作業内容:
- [ ] クエリパーサー
- [ ] コンテキストビルダー
- [ ] レスポンスジェネレーター
- [ ] 引用トラッカー
```

**完了条件**:
- FR-009, FR-010, FR-011, FR-012準拠
- エンドツーエンドのRAGパイプライン

---

### TASK-5.5: プロンプトテンプレート作成
**Priority**: P1 (High)
**Estimate**: 60min
**Dependencies**: TASK-5.4

```
ファイル: lib/graphrag-core/src/application/prompts/

作業内容:
- [ ] rag_system_prompt.txt
- [ ] theory_citation_prompt.txt
- [ ] context_formatting.py
```

**完了条件**:
- 理論引用を促すプロンプト
- Jinja2テンプレート形式

---

### TASK-5.6: エラーハンドリング実装
**Priority**: P1 (High)
**Estimate**: 30min
**Dependencies**: TASK-5.4

```
ファイル: lib/graphrag-core/src/application/services/

作業内容:
- [ ] 検索結果なし時の処理（FR-013）
- [ ] エビデンス不足時の処理（FR-014）
- [ ] 信頼度スコア計算
```

**完了条件**:
- FR-013, FR-014準拠
- 適切なエラーレスポンス

---

## Phase 6: API実装

### TASK-6.1: FastAPIアプリケーション基盤
**Priority**: P0 (Critical)
**Estimate**: 30min
**Dependencies**: TASK-1.2

```
ファイル: api/src/

作業内容:
- [ ] main.py - FastAPIアプリ初期化
- [ ] config.py - 設定管理
- [ ] dependencies.py - DI設定
```

**完了条件**:
- `uvicorn api.src.main:app` で起動
- /docs でSwagger UI表示

---

### TASK-6.2: RAGエンドポイント実装
**Priority**: P0 (Critical)
**Estimate**: 60min
**Dependencies**: TASK-6.1, TASK-5.4

```
ファイル: api/src/routes/query_routes.py

作業内容:
- [ ] POST /api/v1/rag/query
- [ ] リクエストバリデーション
- [ ] レスポンスフォーマット
```

**完了条件**:
- FR-010準拠
- OpenAPI仕様準拠

---

### TASK-6.3: Theoryエンドポイント実装
**Priority**: P1 (High)
**Estimate**: 45min
**Dependencies**: TASK-6.1, TASK-5.3

```
ファイル: api/src/routes/theory_routes.py

作業内容:
- [ ] GET /api/v1/theories
- [ ] GET /api/v1/theories/{id}
- [ ] POST /api/v1/theories
- [ ] GET /api/v1/concepts
```

**完了条件**:
- CRUD操作可能
- ページネーション対応

---

### TASK-6.4: Graphエンドポイント実装
**Priority**: P1 (High)
**Estimate**: 45min
**Dependencies**: TASK-6.1, TASK-5.3

```
ファイル: api/src/routes/graph_routes.py

作業内容:
- [ ] GET /api/v1/graph/traverse
- [ ] POST /api/v1/graph/import
- [ ] GET /api/v1/graph/export
```

**完了条件**:
- グラフ操作API完備
- インポート/エクスポート動作

---

### TASK-6.5: ミドルウェア・認証
**Priority**: P2 (Medium)
**Estimate**: 30min
**Dependencies**: TASK-6.1

```
ファイル: api/src/middleware/

作業内容:
- [ ] auth.py - API Key認証
- [ ] logging.py - リクエストログ
- [ ] error_handler.py - 例外ハンドラ
```

**完了条件**:
- NFR-005準拠
- 統一されたエラーレスポンス

---

## Phase 7: CLI実装

### TASK-7.1: CLI基盤
**Priority**: P1 (High)
**Estimate**: 30min
**Dependencies**: TASK-1.2

```
ファイル: cli/src/main.py

作業内容:
- [ ] Typerアプリ初期化
- [ ] サブコマンド構造
- [ ] 設定読み込み
```

**完了条件**:
- `tengin --help` で使い方表示
- Article II (CLI Mandate) 準拠

---

### TASK-7.2: クエリコマンド
**Priority**: P1 (High)
**Estimate**: 45min
**Dependencies**: TASK-7.1, TASK-5.4

```
ファイル: cli/src/commands/query.py

作業内容:
- [ ] tengin query "クエリ文"
- [ ] オプション（深度、理論数、etc.）
- [ ] 結果表示フォーマット
```

**完了条件**:
- CLIからRAGクエリ実行可能
- 引用情報表示

---

### TASK-7.3: グラフ操作コマンド
**Priority**: P1 (High)
**Estimate**: 45min
**Dependencies**: TASK-7.1, TASK-5.3

```
ファイル: cli/src/commands/graph.py

作業内容:
- [ ] tengin graph import <file>
- [ ] tengin graph export <file>
- [ ] tengin graph stats
```

**完了条件**:
- JSON/CSVインポート可能
- グラフ統計表示

---

### TASK-7.4: 管理コマンド
**Priority**: P2 (Medium)
**Estimate**: 30min
**Dependencies**: TASK-7.1

```
ファイル: cli/src/commands/admin.py

作業内容:
- [ ] tengin init-db（スキーマ初期化）
- [ ] tengin seed（初期データ投入）
- [ ] tengin health（ヘルスチェック）
```

**完了条件**:
- 初期セットアップがCLIで完結

---

## Phase 8: テスト・検証

### TASK-8.1: ユニットテスト
**Priority**: P0 (Critical)
**Estimate**: 60min
**Dependencies**: Phase 2, 5

```
作業内容:
- [ ] ドメインエンティティテスト
- [ ] サービステスト（モック使用）
- [ ] カバレッジ80%以上
```

**完了条件**:
- Article III準拠
- pytest --cov で80%以上

---

### TASK-8.2: 統合テスト
**Priority**: P0 (Critical)
**Estimate**: 60min
**Dependencies**: Phase 3, 6

```
作業内容:
- [ ] Neo4j統合テスト（実DB）
- [ ] ChromaDB統合テスト
- [ ] API統合テスト
```

**完了条件**:
- Article IX準拠（実サービス使用）
- docker-compose で環境構築

---

### TASK-8.3: E2Eテスト
**Priority**: P1 (High)
**Estimate**: 60min
**Dependencies**: TASK-8.2

```
作業内容:
- [ ] RAGパイプラインE2Eテスト
- [ ] CLIコマンドE2Eテスト
- [ ] シナリオベーステスト
```

**完了条件**:
- 主要ユースケースをカバー
- CI/CDで実行

---

### TASK-8.4: トレーサビリティ検証
**Priority**: P1 (High)
**Estimate**: 30min
**Dependencies**: TASK-8.1, TASK-8.2

```
作業内容:
- [ ] 要件 ↔ テストのマッピング
- [ ] REQ-001の全FRに対応するテスト確認
- [ ] トレーサビリティマトリクス更新
```

**完了条件**:
- Article V準拠
- 100%トレーサビリティ

---

## 優先度定義

| Priority | 説明 |
|----------|------|
| P0 (Critical) | MVP必須、他タスクの依存元 |
| P1 (High) | MVP必須 |
| P2 (Medium) | MVP後でも可 |
| P3 (Low) | Nice to have |

---

## 依存関係グラフ

```
Phase 1 (初期化)
    │
    ├─► Phase 2 (ドメイン)
    │       │
    │       ├─► Phase 3 (インフラ)
    │       │       │
    │       │       └─► Phase 5 (アプリ)
    │       │               │
    │       │               ├─► Phase 6 (API)
    │       │               │
    │       │               └─► Phase 7 (CLI)
    │       │
    │       └─► Phase 4 (データ)
    │
    └─► Phase 8 (テスト) ─────────────────────►
```

---

## 実装開始チェックリスト

- [ ] TASK-1.1 から順番に実行
- [ ] 各タスク完了時にテスト実行
- [ ] Article III (Test-First) に従う
- [ ] PRごとにレビュー

---

## 変更履歴

| バージョン | 日付 | 変更者 | 変更内容 |
|-----------|------|--------|---------|
| 1.0 | 2025-12-25 | GitHub Copilot | 初版作成 |
