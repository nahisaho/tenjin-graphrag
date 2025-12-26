# アーキテクチャ設計書: 教育理論GraphRAGシステム

**ID**: DESIGN-001
**Feature**: Education Theory GraphRAG System
**Version**: 1.0
**Created**: 2025-12-25
**Status**: Draft
**Related Requirements**: REQ-001

---

## 1. C4モデル

### 1.1 Level 1: System Context Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              External Systems                                │
└─────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────┐         ┌──────────────┐         ┌──────────────┐
    │  AI Product  │         │Instructional │         │   Education  │
    │  Developer   │         │   Designer   │         │  Researcher  │
    └──────┬───────┘         └──────┬───────┘         └──────┬───────┘
           │                        │                        │
           │  REST API / CLI        │  REST API              │  REST API
           │                        │                        │
           ▼                        ▼                        ▼
    ┌─────────────────────────────────────────────────────────────────┐
    │                                                                  │
    │                    TENGIN-GraphRAG System                        │
    │                                                                  │
    │   教育理論のナレッジグラフを提供し、GraphRAGによる                │
    │   理論に基づいたコンテキスト検索を実現                            │
    │                                                                  │
    └─────────────────────────────────────────────────────────────────┘
           │                        │                        │
           │                        │                        │
           ▼                        ▼                        ▼
    ┌──────────────┐         ┌──────────────┐         ┌──────────────┐
    │   LLM API    │         │  Graph DB    │         │  Vector DB   │
    │  (OpenAI等)  │         │   (Neo4j)    │         │  (ChromaDB)  │
    └──────────────┘         └──────────────┘         └──────────────┘
```

### 1.2 Level 2: Container Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         TENGIN-GraphRAG System                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────────┐    ┌─────────────────────┐    ┌─────────────────┐  │
│  │      CLI Tool       │    │     REST API        │    │   Admin Web UI  │  │
│  │     (Python)        │    │  (FastAPI/Python)   │    │   (Optional)    │  │
│  │                     │    │                     │    │                 │  │
│  │  - graph import     │    │  - /api/v1/query    │    │  - Graph Editor │  │
│  │  - graph export     │    │  - /api/v1/theories │    │  - Visualization│  │
│  │  - query test       │    │  - /api/v1/rag      │    │                 │  │
│  └─────────┬───────────┘    └─────────┬───────────┘    └────────┬────────┘  │
│            │                          │                         │           │
│            └──────────────────────────┼─────────────────────────┘           │
│                                       │                                      │
│                                       ▼                                      │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                      Application Layer (Python)                        │  │
│  │                                                                        │  │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────┐    │  │
│  │  │  Query Service  │  │  Graph Service  │  │  RAG Orchestrator   │    │  │
│  │  │                 │  │                 │  │                     │    │  │
│  │  │  - Semantic     │  │  - CRUD         │  │  - Context Builder  │    │  │
│  │  │    Search       │  │  - Traversal    │  │  - Prompt Template  │    │  │
│  │  │  - Reranking    │  │  - Import/Export│  │  - Citation Tracker │    │  │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────────┘    │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                       │                                      │
│                                       ▼                                      │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                      Domain Layer (Python)                             │  │
│  │                                                                        │  │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────┐    │  │
│  │  │     Theory      │  │     Concept     │  │     Relationship    │    │  │
│  │  │                 │  │                 │  │                     │    │  │
│  │  │  - Entity       │  │  - Entity       │  │  - PROPOSED_BY      │    │  │
│  │  │  - Repository   │  │  - Repository   │  │  - BASED_ON         │    │  │
│  │  │    Interface    │  │    Interface    │  │  - EXTENDS          │    │  │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────────┘    │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                       │                                      │
│                                       ▼                                      │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                    Infrastructure Layer (Python)                       │  │
│  │                                                                        │  │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────┐    │  │
│  │  │  Neo4j Adapter  │  │ ChromaDB Adapter│  │   LLM Client        │    │  │
│  │  │                 │  │                 │  │                     │    │  │
│  │  │  - Graph Ops    │  │  - Embedding    │  │  - OpenAI           │    │  │
│  │  │  - Cypher Query │  │  - Vector Search│  │  - Azure OpenAI     │    │  │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────────┘    │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
         │                        │                        │
         ▼                        ▼                        ▼
  ┌──────────────┐         ┌──────────────┐         ┌──────────────┐
  │    Neo4j     │         │   ChromaDB   │         │  OpenAI API  │
  │  Graph DB    │         │  Vector DB   │         │   / LLM      │
  └──────────────┘         └──────────────┘         └──────────────┘
```

### 1.3 Level 3: Component Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            Application Layer                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                         RAG Orchestrator                             │    │
│  │                                                                      │    │
│  │   ┌───────────────┐   ┌───────────────┐   ┌───────────────────┐    │    │
│  │   │ Query Parser  │──▶│Context Builder│──▶│ Response Generator│    │    │
│  │   │               │   │               │   │                   │    │    │
│  │   │ - Intent      │   │ - Theory      │   │ - Prompt Render   │    │    │
│  │   │   Detection   │   │   Aggregation │   │ - LLM Call        │    │    │
│  │   │ - Entity      │   │ - Relation    │   │ - Citation        │    │    │
│  │   │   Extraction  │   │   Mapping     │   │   Injection       │    │    │
│  │   └───────────────┘   └───────────────┘   └───────────────────┘    │    │
│  │           │                   │                     │               │    │
│  │           ▼                   ▼                     ▼               │    │
│  │   ┌───────────────────────────────────────────────────────────┐    │    │
│  │   │                  Citation Tracker                          │    │    │
│  │   │                                                            │    │    │
│  │   │  - Track used theories    - Generate bibliography          │    │    │
│  │   │  - Evidence level mapping - Source attribution             │    │    │
│  │   └───────────────────────────────────────────────────────────┘    │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  ┌──────────────────────────────┐    ┌──────────────────────────────┐       │
│  │       Query Service          │    │        Graph Service          │       │
│  │                              │    │                               │       │
│  │  ┌────────────────────────┐  │    │  ┌─────────────────────────┐ │       │
│  │  │   Semantic Searcher    │  │    │  │   Graph Traverser       │ │       │
│  │  │                        │  │    │  │                         │ │       │
│  │  │  - Text Embedding      │  │    │  │  - BFS/DFS Search       │ │       │
│  │  │  - Similarity Search   │  │    │  │  - Path Finding         │ │       │
│  │  │  - Hybrid Search       │  │    │  │  - Subgraph Extraction  │ │       │
│  │  └────────────────────────┘  │    │  └─────────────────────────┘ │       │
│  │                              │    │                               │       │
│  │  ┌────────────────────────┐  │    │  ┌─────────────────────────┐ │       │
│  │  │     Re-ranker          │  │    │  │   Graph CRUD            │ │       │
│  │  │                        │  │    │  │                         │ │       │
│  │  │  - Cross-encoder       │  │    │  │  - Create/Update Node   │ │       │
│  │  │  - MMR Diversity       │  │    │  │  - Create/Update Edge   │ │       │
│  │  └────────────────────────┘  │    │  │  - Import/Export        │ │       │
│  └──────────────────────────────┘    │  └─────────────────────────┘ │       │
│                                       └──────────────────────────────┘       │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. ディレクトリ構造

```
TENGIN-GraphRAG/
├── lib/                              # Library-First (Article I)
│   ├── graphrag-core/               # Core GraphRAG library
│   │   ├── src/
│   │   │   ├── __init__.py
│   │   │   ├── domain/              # Domain Layer
│   │   │   │   ├── __init__.py
│   │   │   │   ├── entities/
│   │   │   │   │   ├── theory.py        # Theory entity
│   │   │   │   │   ├── concept.py       # Concept entity
│   │   │   │   │   ├── theorist.py      # Theorist entity
│   │   │   │   │   ├── evidence.py      # Evidence entity
│   │   │   │   │   └── relationship.py  # Relationship types
│   │   │   │   ├── repositories/
│   │   │   │   │   ├── theory_repository.py    # Interface
│   │   │   │   │   ├── concept_repository.py   # Interface
│   │   │   │   │   └── graph_repository.py     # Interface
│   │   │   │   └── value_objects/
│   │   │   │       ├── evidence_level.py
│   │   │   │       └── theory_category.py
│   │   │   │
│   │   │   ├── application/         # Application Layer
│   │   │   │   ├── __init__.py
│   │   │   │   ├── services/
│   │   │   │   │   ├── query_service.py
│   │   │   │   │   ├── graph_service.py
│   │   │   │   │   └── rag_orchestrator.py
│   │   │   │   ├── dto/
│   │   │   │   │   ├── query_request.py
│   │   │   │   │   ├── query_response.py
│   │   │   │   │   └── theory_dto.py
│   │   │   │   └── ports/
│   │   │   │       ├── llm_port.py
│   │   │   │       ├── vector_db_port.py
│   │   │   │       └── graph_db_port.py
│   │   │   │
│   │   │   └── infrastructure/      # Infrastructure Layer
│   │   │       ├── __init__.py
│   │   │       ├── adapters/
│   │   │       │   ├── neo4j_adapter.py
│   │   │       │   ├── chromadb_adapter.py
│   │   │       │   └── openai_adapter.py
│   │   │       ├── repositories/
│   │   │       │   ├── neo4j_theory_repository.py
│   │   │       │   └── neo4j_graph_repository.py
│   │   │       └── embeddings/
│   │   │           └── embedding_service.py
│   │   │
│   │   ├── tests/
│   │   │   ├── unit/
│   │   │   ├── integration/
│   │   │   └── e2e/
│   │   ├── cli.py                   # CLI Interface (Article II)
│   │   ├── pyproject.toml
│   │   └── README.md
│   │
│   └── education-theories-data/     # Data library
│       ├── data/
│       │   ├── theories/            # Theory JSON files
│       │   │   ├── learning_theories.json
│       │   │   ├── instructional_theories.json
│       │   │   ├── developmental_theories.json
│       │   │   └── motivation_theories.json
│       │   ├── relationships/       # Relationship definitions
│       │   │   └── theory_relationships.json
│       │   └── schema/              # JSON Schema
│       │       └── theory_schema.json
│       ├── scripts/
│       │   └── validate.py
│       └── README.md
│
├── api/                             # API Application
│   ├── src/
│   │   ├── __init__.py
│   │   ├── main.py                  # FastAPI app entry
│   │   ├── routes/
│   │   │   ├── query_routes.py
│   │   │   ├── theory_routes.py
│   │   │   └── health_routes.py
│   │   ├── middleware/
│   │   │   ├── auth.py
│   │   │   └── logging.py
│   │   └── config.py
│   ├── tests/
│   └── Dockerfile
│
├── cli/                             # CLI Application
│   ├── src/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── commands/
│   │       ├── query.py
│   │       ├── graph.py
│   │       └── import_export.py
│   └── pyproject.toml
│
├── docs/                            # Documentation
│   ├── api/
│   ├── architecture/
│   └── user-guide/
│
├── storage/                         # SDD Artifacts
│   ├── specs/
│   ├── changes/
│   └── archive/
│
├── steering/                        # Project Memory
│   ├── product.ja.md
│   ├── tech.ja.md
│   ├── structure.ja.md
│   ├── project.yml
│   └── rules/
│
├── templates/                       # Document Templates
├── docker-compose.yml               # Local development
├── pyproject.toml                   # Root project config
└── README.md
```

---

## 3. データフロー

### 3.1 GraphRAGクエリフロー

```
┌─────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  User   │────▶│   API/CLI   │────▶│Query Service│────▶│  ChromaDB   │
│  Query  │     │             │     │             │     │(Vector DB)  │
└─────────┘     └─────────────┘     └──────┬──────┘     └──────┬──────┘
                                           │                   │
                                           │ 1. Embed query    │
                                           │ 2. Semantic search│
                                           │◀──────────────────┘
                                           │    Initial nodes
                                           ▼
                                    ┌─────────────┐
                                    │Graph Service│
                                    │             │
                                    │ 3. Expand   │
                                    │    via graph│
                                    │    traversal│
                                    └──────┬──────┘
                                           │
                                           │ Related theories,
                                           │ concepts, evidence
                                           ▼
                                    ┌─────────────┐     ┌─────────────┐
                                    │    RAG      │────▶│   LLM API   │
                                    │Orchestrator │     │  (OpenAI)   │
                                    │             │◀────│             │
                                    │ 4. Build    │     └─────────────┘
                                    │    context  │
                                    │ 5. Generate │
                                    │    response │
                                    └──────┬──────┘
                                           │
                                           │ Response with
                                           │ citations
                                           ▼
                                    ┌─────────────┐
                                    │   Client    │
                                    └─────────────┘
```

### 3.2 グラフインポートフロー

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  JSON/CSV   │────▶│   Parser    │────▶│  Validator  │
│    File     │     │             │     │             │
└─────────────┘     └─────────────┘     └──────┬──────┘
                                               │
                                               │ Valid entities
                                               ▼
                    ┌─────────────┐     ┌─────────────┐
                    │   Neo4j     │◀────│Graph Service│
                    │ (Graph DB)  │     │             │
                    └─────────────┘     └──────┬──────┘
                                               │
                                               │ Entities for
                                               │ embedding
                                               ▼
                    ┌─────────────┐     ┌─────────────┐
                    │  ChromaDB   │◀────│  Embedding  │
                    │ (Vector DB) │     │   Service   │
                    └─────────────┘     └─────────────┘
```

---

## 4. API設計

### 4.1 REST API エンドポイント

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/rag/query` | GraphRAGクエリ実行 |
| GET | `/api/v1/theories` | 理論一覧取得 |
| GET | `/api/v1/theories/{id}` | 理論詳細取得 |
| POST | `/api/v1/theories` | 理論登録 |
| GET | `/api/v1/concepts` | 概念一覧取得 |
| GET | `/api/v1/graph/traverse` | グラフトラバーサル |
| POST | `/api/v1/graph/import` | データインポート |
| GET | `/api/v1/graph/export` | データエクスポート |
| GET | `/health` | ヘルスチェック |

### 4.2 主要リクエスト/レスポンス

#### POST /api/v1/rag/query

**Request:**
```json
{
  "query": "効果的な授業設計の方法を教えてください",
  "options": {
    "max_theories": 5,
    "traversal_depth": 2,
    "include_evidence": true,
    "evidence_level_min": "moderate"
  }
}
```

**Response:**
```json
{
  "answer": "効果的な授業設計には、ガニェの9教授事象に基づいたアプローチが...",
  "citations": [
    {
      "theory": "ガニェの9教授事象",
      "theorist": "Robert Gagné",
      "year": 1965,
      "relevance_score": 0.95,
      "evidence_level": "strong"
    },
    {
      "theory": "認知負荷理論",
      "theorist": "John Sweller",
      "year": 1988,
      "relevance_score": 0.87,
      "evidence_level": "strong"
    }
  ],
  "context": {
    "theories_used": 3,
    "concepts_used": 8,
    "relationships_traversed": 12
  },
  "confidence_score": 0.91
}
```

---

## 5. 技術スタック決定

| 領域 | 選定技術 | 理由 |
|------|---------|------|
| 言語 | Python 3.11+ | ML/AI エコシステム、GraphRAG実装の事例多数 |
| Web Framework | FastAPI | 非同期対応、OpenAPI自動生成、型ヒント |
| Graph DB | Neo4j | 最も成熟したグラフDB、Cypher言語、可視化 |
| Vector DB | ChromaDB | ローカル開発容易、OSS、Python native |
| Embedding | OpenAI Ada / Sentence-Transformers | 高品質な埋め込み |
| LLM | OpenAI GPT-4 / Azure OpenAI | 最高品質の生成能力 |
| CLI | Typer | FastAPIとの親和性、型ヒント活用 |
| Testing | pytest | Python標準、fixture対応 |
| Container | Docker | 再現性、デプロイ容易性 |

---

## 6. トレーサビリティ

| 要件ID | 設計コンポーネント |
|--------|-------------------|
| FR-001 | Graph Service, Theory Entity |
| FR-002 | Graph Service, Concept Entity |
| FR-003 | Graph Service, Relationship |
| FR-004 | Neo4j Adapter |
| FR-005 | Graph Service, Import |
| FR-006 | (Phase 2 - Admin UI) |
| FR-007 | Query Service, ChromaDB Adapter |
| FR-008 | Graph Service, Graph Traverser |
| FR-009 | RAG Orchestrator, Context Builder |
| FR-010 | API Routes, RAG Orchestrator |
| FR-011 | RAG Orchestrator, Prompt Templates |
| FR-012 | Citation Tracker |
| FR-013 | RAG Orchestrator, Error Handling |
| FR-014 | RAG Orchestrator, Confidence Score |

---

## 変更履歴

| バージョン | 日付 | 変更者 | 変更内容 |
|-----------|------|--------|---------|
| 1.0 | 2025-12-25 | GitHub Copilot | 初版作成 |
