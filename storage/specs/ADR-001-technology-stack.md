# ADR-001: 技術スタック選定

**Status**: Accepted
**Date**: 2025-12-25
**Deciders**: Development Team
**Related**: REQ-001, DESIGN-001

---

## Context

教育理論GraphRAGシステムを構築するにあたり、以下の技術選定が必要：

1. プログラミング言語
2. グラフデータベース
3. ベクトルデータベース
4. Web APIフレームワーク
5. LLM統合

## Decision Drivers

- 開発効率とエコシステムの成熟度
- GraphRAG実装の実績
- ローカル開発の容易さ
- 本番環境でのスケーラビリティ
- コミュニティサポート

---

## Decisions

### Decision 1: プログラミング言語 → Python 3.11+

**選択肢検討:**

| 選択肢 | 長所 | 短所 |
|--------|------|------|
| Python | ML/AIエコシステム充実、GraphRAG実装多数 | 実行速度 |
| TypeScript | 型安全、フルスタック統一 | ML/GraphRAGライブラリ少 |
| Rust | 高速、安全 | 開発速度、エコシステム |

**決定**: Python 3.11+

**理由**:
- LangChain, LlamaIndex等のGraphRAGフレームワークがPython主体
- Neo4j, ChromaDB等のクライアントが最も充実
- Sentence-Transformers等のEmbeddingライブラリ
- 開発チームの経験

---

### Decision 2: グラフデータベース → Neo4j

**選択肢検討:**

| 選択肢 | 長所 | 短所 |
|--------|------|------|
| Neo4j | 最も成熟、Cypher言語、可視化充実 | 商用ライセンス（大規模時） |
| Memgraph | Neo4j互換、高速 | エコシステム小 |
| Amazon Neptune | マネージド、スケーラブル | AWSロックイン、ローカル開発困難 |
| ArangoDB | マルチモデル | グラフ専用でない |

**決定**: Neo4j (Community Edition / AuraDB)

**理由**:
- 教育理論の関係性表現に最適なグラフモデル
- Cypher言語による直感的なクエリ
- Neo4j Bloom/Browserによる可視化
- Pythonドライバの成熟度
- Community Editionで開発開始、必要に応じてAuraDB

---

### Decision 3: ベクトルデータベース → ChromaDB (ローカル) / Qdrant (本番)

**選択肢検討:**

| 選択肢 | 長所 | 短所 |
|--------|------|------|
| ChromaDB | 軽量、Python native、ローカル開発最適 | 大規模時の制限 |
| Qdrant | 高性能、フィルタリング強力 | セットアップ |
| Pinecone | フルマネージド、スケーラブル | コスト、ロックイン |
| Weaviate | GraphQL、ハイブリッド検索 | 複雑性 |

**決定**: 
- 開発/小規模: ChromaDB
- 本番/大規模: Qdrant

**理由**:
- ChromaDBはローカル開発で即座に使用可能
- Qdrantはセルフホスト可能でフィルタリング機能が強力
- 抽象化レイヤー（Port/Adapter）で切り替え可能に設計

---

### Decision 4: Web APIフレームワーク → FastAPI

**選択肢検討:**

| 選択肢 | 長所 | 短所 |
|--------|------|------|
| FastAPI | 非同期、型ヒント、OpenAPI自動生成 | - |
| Flask | シンプル、実績 | 非同期弱い、手動設定多い |
| Django | フルスタック | オーバースペック |

**決定**: FastAPI

**理由**:
- 非同期処理によるLLM API呼び出しの効率化
- Pydanticによる自動バリデーション
- OpenAPI (Swagger) ドキュメント自動生成
- 型ヒントによる開発体験向上

---

### Decision 5: LLM統合 → OpenAI API (GPT-4) with 抽象化

**選択肢検討:**

| 選択肢 | 長所 | 短所 |
|--------|------|------|
| OpenAI GPT-4 | 最高品質、広く使用 | コスト、API依存 |
| Azure OpenAI | エンタープライズ、SLA | Azure契約必要 |
| Claude (Anthropic) | 長文コンテキスト | API安定性 |
| Ollama (ローカル) | プライバシー、コスト無料 | 品質、リソース |

**決定**: OpenAI API (GPT-4) をデフォルト、LLMPort抽象化で切り替え可能

**理由**:
- 教育コンテンツ生成において最高品質が求められる
- 抽象化レイヤーにより、Azure OpenAI、Anthropic等への切り替えを容易に
- 将来的にOllamaでのローカル実行もサポート可能

---

### Decision 6: CLIフレームワーク → Typer

**決定**: Typer

**理由**:
- FastAPIと同じ開発者（Sebastián Ramírez）
- 型ヒントベースで自動補完・ヘルプ生成
- Click互換で拡張性あり

---

## Consequences

### Good

- Pythonエコシステムの豊富なライブラリを活用可能
- GraphRAGの実装パターンを参照可能
- ローカル開発が容易（Neo4j Desktop, ChromaDB）
- Port/Adapterパターンによる柔軟性

### Bad

- Pythonの実行速度制限（必要に応じてRustで最適化）
- Neo4jの商用ライセンスコスト（大規模時）
- OpenAI APIへの依存（代替の抽象化で緩和）

### Risks

- LLM APIのコスト増加 → レート制限、キャッシュで対応
- Neo4jスキーマ変更の困難さ → 初期設計を慎重に

---

## 変更履歴

| バージョン | 日付 | 変更内容 |
|-----------|------|---------|
| 1.0 | 2025-12-25 | 初版作成 |
