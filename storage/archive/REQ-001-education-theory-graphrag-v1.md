# 要件仕様書: 教育理論GraphRAGシステム

**ID**: REQ-001
**Feature**: Education Theory GraphRAG System
**Version**: 1.0
**Created**: 2025-12-25
**Status**: Draft
**Author**: GitHub Copilot

---

## 1. 概要

### 1.1 背景

生成AIが教育コンテンツを生成する際、教育理論に基づいたエビデンスベースのコンテンツを生成することが求められている。しかし、既存のLLMは教育理論の体系的な知識を持たず、理論的根拠のないコンテンツを生成する可能性がある。

### 1.2 目的

教育理論のナレッジグラフを構築し、GraphRAG（Graph-based Retrieval Augmented Generation）を用いて、生成AIが理論に基づいた教育コンテンツを生成できるようにする。

### 1.3 スコープ

| 項目 | スコープ内 | スコープ外 |
|------|-----------|-----------|
| 教育理論データベース | ✅ | |
| ナレッジグラフ構築 | ✅ | |
| GraphRAG検索エンジン | ✅ | |
| LLM統合API | ✅ | |
| コンテンツ生成UI | | ❌ (Phase 2) |
| 多言語対応 | | ❌ (Phase 2) |

---

## 2. ドメインモデル

### 2.1 教育理論の分類体系

```
教育理論 (Education Theory)
├── 学習理論 (Learning Theories)
│   ├── 行動主義 (Behaviorism)
│   │   ├── 古典的条件付け (Classical Conditioning) - Pavlov
│   │   ├── オペラント条件付け (Operant Conditioning) - Skinner
│   │   └── 社会的学習理論 (Social Learning Theory) - Bandura
│   ├── 認知主義 (Cognitivism)
│   │   ├── 情報処理理論 (Information Processing Theory)
│   │   ├── スキーマ理論 (Schema Theory) - Piaget
│   │   ├── 有意味学習理論 (Meaningful Learning) - Ausubel
│   │   └── 認知負荷理論 (Cognitive Load Theory) - Sweller
│   ├── 構成主義 (Constructivism)
│   │   ├── 認知的構成主義 (Cognitive Constructivism) - Piaget
│   │   ├── 社会的構成主義 (Social Constructivism) - Vygotsky
│   │   └── 発見学習 (Discovery Learning) - Bruner
│   └── 接続主義 (Connectivism) - Siemens
│
├── 教授理論 (Instructional Theories)
│   ├── ガニェの9教授事象 (Gagné's Nine Events)
│   ├── メリルの第一原理 (Merrill's First Principles)
│   ├── ARCS動機付けモデル (ARCS Model) - Keller
│   ├── 完全習得学習 (Mastery Learning) - Bloom
│   └── 足場かけ (Scaffolding) - Wood, Bruner, Ross
│
├── 発達理論 (Developmental Theories)
│   ├── 認知発達段階 (Cognitive Development) - Piaget
│   ├── 発達の最近接領域 (ZPD) - Vygotsky
│   ├── 心理社会的発達 (Psychosocial Development) - Erikson
│   └── 道徳性発達 (Moral Development) - Kohlberg
│
├── 動機付け理論 (Motivation Theories)
│   ├── 内発的/外発的動機付け (Intrinsic/Extrinsic) - Deci & Ryan
│   ├── 自己決定理論 (Self-Determination Theory)
│   ├── 達成目標理論 (Achievement Goal Theory)
│   ├── 期待価値理論 (Expectancy-Value Theory)
│   └── フロー理論 (Flow Theory) - Csikszentmihalyi
│
└── 教育工学・デザイン (Educational Technology & Design)
    ├── ADDIEモデル
    ├── SAMモデル
    ├── バックワードデザイン (Backward Design) - Wiggins & McTighe
    └── ユニバーサルデザイン学習 (UDL)
```

### 2.2 ナレッジグラフのエンティティ

| エンティティ | 説明 | 属性 |
|-------------|------|------|
| Theory | 教育理論 | id, name, description, year, category |
| Theorist | 理論家 | id, name, biography, affiliation |
| Concept | 概念 | id, name, definition, examples |
| Principle | 原理・原則 | id, name, description, evidence_level |
| Application | 適用方法 | id, name, context, procedure |
| Evidence | エビデンス | id, source, year, methodology, findings |

### 2.3 ナレッジグラフのリレーション

| リレーション | From | To | 説明 |
|-------------|------|-----|------|
| PROPOSED_BY | Theory | Theorist | 理論の提唱者 |
| BASED_ON | Theory | Theory | 理論の基盤 |
| CONTRADICTS | Theory | Theory | 対立する理論 |
| EXTENDS | Theory | Theory | 発展・拡張 |
| CONTAINS | Theory | Concept | 含まれる概念 |
| DERIVES | Principle | Theory | 原理の導出元 |
| SUPPORTED_BY | Theory | Evidence | 支持するエビデンス |
| APPLICABLE_TO | Application | Concept | 適用対象 |
| EFFECTIVE_FOR | Theory | LearningContext | 効果的な文脈 |

---

## 3. 機能要件 (EARS形式)

### 3.1 教育理論データ管理

#### FR-001: 理論の登録
**Type**: Ubiquitous
```
The system SHALL allow users to register education theories with name, description, 
category, proposer, and year of proposal.
```
**Acceptance Criteria**:
- [ ] 理論名（必須）、説明、カテゴリ、提唱者、提唱年を入力できる
- [ ] 登録された理論にユニークIDが付与される
- [ ] 重複する理論名の場合、警告を表示する

#### FR-002: 概念の登録
**Type**: Ubiquitous
```
The system SHALL allow users to register concepts with name, definition, 
examples, and related theories.
```
**Acceptance Criteria**:
- [ ] 概念名（必須）、定義、例、関連理論を入力できる
- [ ] 概念と理論の関連付けができる

#### FR-003: リレーションの作成
**Type**: Ubiquitous
```
The system SHALL allow users to create relationships between entities 
(theories, concepts, theorists, evidence) with relationship type and description.
```
**Acceptance Criteria**:
- [ ] 定義済みリレーションタイプから選択できる
- [ ] 双方向のリレーションが正しく作成される

---

### 3.2 ナレッジグラフ構築

#### FR-004: グラフデータベース格納
**Type**: Ubiquitous
```
The system SHALL store all entities and relationships in a graph database 
that supports Cypher or equivalent query language.
```
**Acceptance Criteria**:
- [ ] Neo4jまたは互換のグラフDBを使用
- [ ] エンティティとリレーションが永続化される
- [ ] Cypherクエリで検索できる

#### FR-005: グラフ自動構築
**Type**: Event-driven
```
WHEN a user uploads a structured data file (JSON/CSV), 
the system SHALL automatically parse and create corresponding graph entities and relationships.
```
**Acceptance Criteria**:
- [ ] JSON形式のインポートに対応
- [ ] CSV形式のインポートに対応
- [ ] インポート結果のサマリを表示

#### FR-006: グラフ可視化
**Type**: Optional
```
WHERE graph visualization is enabled, 
the system SHALL display the knowledge graph as an interactive network diagram.
```
**Acceptance Criteria**:
- [ ] ノード（エンティティ）を視覚的に表示
- [ ] エッジ（リレーション）を線で表示
- [ ] ズーム、パン、フィルタリングが可能

---

### 3.3 GraphRAG検索

#### FR-007: 意味検索
**Type**: Event-driven
```
WHEN a user submits a natural language query, 
the system SHALL retrieve relevant theories, concepts, and relationships 
using semantic similarity search.
```
**Acceptance Criteria**:
- [ ] 自然言語クエリを受け付ける
- [ ] ベクトル埋め込みを使用した類似検索
- [ ] 関連度スコア付きで結果を返す

#### FR-008: グラフトラバーサル検索
**Type**: Event-driven
```
WHEN a semantic search returns initial results, 
the system SHALL expand the results by traversing related nodes in the graph 
up to a configurable depth.
```
**Acceptance Criteria**:
- [ ] 初期結果から関連ノードを探索
- [ ] 探索深度を設定可能（デフォルト: 2ホップ）
- [ ] 関連度に基づいてランキング

#### FR-009: コンテキスト生成
**Type**: Event-driven
```
WHEN graph traversal completes, 
the system SHALL generate a structured context containing theories, concepts, 
relationships, and evidence for LLM consumption.
```
**Acceptance Criteria**:
- [ ] 構造化されたコンテキストJSON/テキストを生成
- [ ] 理論間の関係を明示
- [ ] エビデンスレベルを含める

---

### 3.4 LLM統合API

#### FR-010: RAGエンドポイント
**Type**: Ubiquitous
```
The system SHALL provide a REST API endpoint that accepts a query and returns 
an LLM response augmented with retrieved educational theory context.
```
**Acceptance Criteria**:
- [ ] POST /api/v1/rag/query エンドポイント
- [ ] クエリ、コンテキスト設定を受け付ける
- [ ] 理論に基づいた回答を返す

#### FR-011: プロンプトテンプレート
**Type**: Ubiquitous
```
The system SHALL use configurable prompt templates that instruct the LLM 
to cite educational theories and provide evidence-based responses.
```
**Acceptance Criteria**:
- [ ] カスタマイズ可能なプロンプトテンプレート
- [ ] 理論の引用を促すインストラクション
- [ ] エビデンスレベルの明示を要求

#### FR-012: 引用・出典追跡
**Type**: Ubiquitous
```
The system SHALL track and return the educational theories and sources 
used to generate each response.
```
**Acceptance Criteria**:
- [ ] 使用した理論のリストを返す
- [ ] 各理論の出典情報を含める
- [ ] 引用箇所とのマッピング

---

### 3.5 エラーハンドリング

#### FR-013: 検索結果なし
**Type**: Unwanted behavior
```
IF no relevant theories are found for a query, 
THEN the system SHALL return a response indicating insufficient knowledge 
and suggest alternative queries.
```
**Acceptance Criteria**:
- [ ] 適切なエラーメッセージを返す
- [ ] 代替クエリの提案
- [ ] 一般的な回答にフォールバックしない

#### FR-014: エビデンス不足
**Type**: Unwanted behavior
```
IF retrieved theories lack sufficient evidence, 
THEN the system SHALL flag the response with low confidence 
and indicate the evidence level.
```
**Acceptance Criteria**:
- [ ] 信頼度スコアを計算・表示
- [ ] エビデンスレベルを明示
- [ ] 追加調査の必要性を示唆

---

## 4. 非機能要件

### NFR-001: パフォーマンス
```
The system SHALL return search results within 2 seconds for 95% of queries.
```
- レスポンスタイム: < 2秒 (P95)
- スループット: > 100 queries/minute

### NFR-002: スケーラビリティ
```
The system SHALL support a knowledge graph with up to 10,000 theories 
and 100,000 relationships.
```
- ノード数: 最大10,000
- エッジ数: 最大100,000
- 同時ユーザー: 50

### NFR-003: データ品質
```
The system SHALL maintain data integrity with validated relationships 
and prevent orphan nodes.
```
- 参照整合性の維持
- データバリデーション
- 孤立ノードの防止

### NFR-004: 拡張性
```
The system SHALL support addition of new entity types and relationship types 
without schema changes.
```
- スキーマレス設計
- プラグイン機構
- API拡張可能

### NFR-005: セキュリティ
```
The system SHALL authenticate API requests and authorize access 
based on user roles.
```
- API認証 (API Key / JWT)
- ロールベースアクセス制御
- 入力サニタイズ

---

## 5. データ要件

### 5.1 初期データセット

本システムには以下の教育理論データを初期搭載する：

| カテゴリ | 理論数 | 概念数 | 主要な理論 |
|---------|--------|--------|-----------|
| 学習理論 | 15+ | 50+ | 行動主義、認知主義、構成主義 |
| 教授理論 | 10+ | 30+ | ガニェ、メリル、ARCS |
| 発達理論 | 8+ | 25+ | ピアジェ、ヴィゴツキー |
| 動機付け理論 | 10+ | 35+ | 自己決定理論、フロー理論 |
| 教育工学 | 8+ | 20+ | ADDIE、UDL |

### 5.2 データソース

- 学術論文・教科書からの抽出
- 教育学百科事典
- オープン教育リソース
- 専門家レビュー

---

## 6. 制約事項

### 6.1 技術的制約
- グラフDBはNeo4jまたはMemgraph互換
- ベクトルDBはPinecone/Qdrant/Chromaのいずれか
- LLM APIはOpenAI互換インターフェース

### 6.2 ビジネス制約
- 著作権のある資料は直接引用しない
- 理論の解釈は複数視点を提示

### 6.3 規制制約
- 個人情報を含まない
- 教育内容の中立性を維持

---

## 7. トレーサビリティ

| 要件ID | 設計文書 | 実装 | テスト |
|--------|---------|------|--------|
| FR-001 | - | - | - |
| FR-002 | - | - | - |
| ... | - | - | - |

*実装後に更新*

---

## 8. 承認

| 役割 | 名前 | 日付 | 署名 |
|------|------|------|------|
| プロダクトオーナー | | | ⏳ |
| 技術リード | | | ⏳ |
| QAリード | | | ⏳ |

---

## 変更履歴

| バージョン | 日付 | 変更者 | 変更内容 |
|-----------|------|--------|---------|
| 1.0 | 2025-12-25 | GitHub Copilot | 初版作成 |
