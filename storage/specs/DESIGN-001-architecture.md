# アーキテクチャ設計書: 教育理論GraphRAG MCPサーバー

**ID**: DESIGN-001
**Feature**: Education Theory GraphRAG MCP Server
**Version**: 2.0
**Created**: 2025-12-25
**Updated**: 2025-12-25
**Status**: Draft
**Related Requirements**: REQ-001 v2.0

---

## 1. C4モデル

### 1.1 Level 1: System Context Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         MCP Host Applications                                │
└─────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────┐         ┌──────────────┐         ┌──────────────┐
    │Claude Desktop│         │   VS Code    │         │  Claude Code │
    │              │         │   Copilot    │         │      CLI     │
    └──────┬───────┘         └──────┬───────┘         └──────┬───────┘
           │                        │                        │
           │                        │                        │
    ┌──────────────┐         ┌──────────────┐         ┌──────────────┐
    │  Custom AI   │         │Instructional │         │   Research   │
    │ Application  │         │Designer Tool │         │   Platform   │
    └──────┬───────┘         └──────┬───────┘         └──────┬───────┘
           │                        │                        │
           └────────────────────────┼────────────────────────┘
                                    │
                           MCP Protocol (JSON-RPC 2.0)
                           STDIO / Streamable HTTP
                                    │
                                    ▼
    ┌─────────────────────────────────────────────────────────────────┐
    │                                                                  │
    │              TENGIN Education Theory MCP Server                  │
    │                                                                  │
    │   教育理論のナレッジグラフを提供するMCPサーバー                  │
    │   Tools / Resources / Prompts プリミティブを公開                 │
    │                                                                  │
    └─────────────────────────────────────────────────────────────────┘
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
│                    TENGIN Education Theory MCP Server                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                      MCP Protocol Layer                              │    │
│  │                        (FastMCP SDK)                                 │    │
│  │                                                                      │    │
│  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────────────────┐  │    │
│  │  │   Tools     │    │  Resources  │    │        Prompts          │  │    │
│  │  │  Handler    │    │   Handler   │    │        Handler          │  │    │
│  │  │             │    │             │    │                         │  │    │
│  │  │ @mcp.tool() │    │ @mcp.resource│    │  @mcp.prompt()         │  │    │
│  │  │             │    │             │    │                         │  │    │
│  │  └──────┬──────┘    └──────┬──────┘    └───────────┬─────────────┘  │    │
│  │         │                  │                       │                │    │
│  │         └──────────────────┼───────────────────────┘                │    │
│  │                            │                                        │    │
│  │                      Transport Layer                                │    │
│  │              ┌─────────────┴─────────────┐                          │    │
│  │              │                           │                          │    │
│  │       ┌──────┴──────┐            ┌───────┴───────┐                  │    │
│  │       │    STDIO    │            │Streamable HTTP│                  │    │
│  │       │  Transport  │            │   Transport   │                  │    │
│  │       │ (local use) │            │ (remote/multi)│                  │    │
│  │       └─────────────┘            └───────────────┘                  │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                       │                                      │
│                                       ▼                                      │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                      Application Layer (Python)                        │  │
│  │                                                                        │  │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────┐    │  │
│  │  │ Search Service  │  │  Graph Service  │  │  Citation Service   │    │  │
│  │  │                 │  │                 │  │                     │    │  │
│  │  │ - Semantic      │  │ - Traversal     │  │ - Format Citation   │    │  │
│  │  │   Search        │  │ - Subgraph      │  │ - Track Sources     │    │  │
│  │  │ - Hybrid Search │  │   Extraction    │  │ - Bibliography      │    │  │
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
│  │  │ - Entity        │  │ - Entity        │  │ - PROPOSED_BY       │    │  │
│  │  │ - Repository    │  │ - Repository    │  │ - BASED_ON          │    │  │
│  │  │   Interface     │  │   Interface     │  │ - EXTENDS           │    │  │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────────┘    │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                       │                                      │
│                                       ▼                                      │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                    Infrastructure Layer (Python)                       │  │
│  │                                                                        │  │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────┐    │  │
│  │  │  Neo4j Adapter  │  │ChromaDB Adapter │  │   LLM Client        │    │  │
│  │  │                 │  │                 │  │                     │    │  │
│  │  │ - Graph Ops     │  │ - Embedding     │  │ - OpenAI            │    │  │
│  │  │ - Cypher Query  │  │ - Vector Search │  │ - Embedding API     │    │  │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────────┘    │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
         │                        │                        │
         ▼                        ▼                        ▼
  ┌──────────────┐         ┌──────────────┐         ┌──────────────┐
  │    Neo4j     │         │   ChromaDB   │         │  OpenAI API  │
  │  Graph DB    │         │  Vector DB   │         │  (Embedding) │
  └──────────────┘         └──────────────┘         └──────────────┘
```

### 1.3 Level 3: MCP Primitives Component

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            MCP Primitives Layer                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                              Tools                                   │    │
│  │                    (Model-controlled, LLM calls)                     │    │
│  │                                                                      │    │
│  │   ┌────────────────┐   ┌────────────────┐   ┌────────────────┐      │    │
│  │   │search_theories │   │  get_theory    │   │traverse_graph  │      │    │
│  │   │ Semantic search│   │ Get details    │   │ BFS/DFS graph  │      │    │
│  │   └────────────────┘   └────────────────┘   └────────────────┘      │    │
│  │                                                                      │    │
│  │   ┌────────────────┐   ┌────────────────┐   ┌────────────────┐      │    │
│  │   │find_applicable │   │  cite_theory   │   │compare_theories│      │    │
│  │   │ Context-based  │   │ APA/MLA/etc    │   │ Side-by-side   │      │    │
│  │   └────────────────┘   └────────────────┘   └────────────────┘      │    │
│  │                                                                      │    │
│  │   ┌────────────────┐   ┌────────────────┐                           │    │
│  │   │  get_evidence  │   │ get_principles │                           │    │
│  │   │ Research data  │   │ Key principles │                           │    │
│  │   └────────────────┘   └────────────────┘                           │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                            Resources                                 │    │
│  │                  (Application-controlled, read-only)                 │    │
│  │                                                                      │    │
│  │   theory://{category}/list  │  concept://{id}  │  graph://schema    │    │
│  │   theory://{id}             │  theorist://{id} │  graph://stats     │    │
│  │   theory://list             │  evidence://{id} │                    │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                             Prompts                                  │    │
│  │                      (User-controlled templates)                     │    │
│  │                                                                      │    │
│  │   design_lesson    │  create_assessment  │  explain_theory          │    │
│  │   apply_theory     │  curriculum_plan    │  troubleshoot_learning   │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. ディレクトリ構造

```
TENGIN-GraphRAG/
├── src/                              # MCP Server Source
│   └── tengin_mcp/                   # Main package
│       ├── __init__.py
│       ├── server.py                 # MCP Server entry point
│       │
│       ├── tools/                    # MCP Tools
│       │   ├── __init__.py
│       │   ├── search.py             # search_theories, find_applicable
│       │   ├── theory.py             # get_theory, get_principles, get_evidence
│       │   ├── graph.py              # traverse_graph
│       │   ├── citation.py           # cite_theory
│       │   └── compare.py            # compare_theories
│       │
│       ├── resources/                # MCP Resources
│       │   ├── __init__.py
│       │   ├── theory_resources.py
│       │   ├── concept_resources.py
│       │   └── graph_resources.py
│       │
│       ├── prompts/                  # MCP Prompts
│       │   ├── __init__.py
│       │   ├── lesson_prompts.py
│       │   ├── assessment_prompts.py
│       │   └── theory_prompts.py
│       │
│       ├── domain/                   # Domain Layer
│       │   ├── __init__.py
│       │   ├── entities/
│       │   │   ├── theory.py
│       │   │   ├── concept.py
│       │   │   ├── theorist.py
│       │   │   ├── evidence.py
│       │   │   └── principle.py
│       │   ├── repositories/
│       │   │   ├── theory_repository.py
│       │   │   └── graph_repository.py
│       │   └── value_objects/
│       │       ├── theory_category.py
│       │       ├── evidence_level.py
│       │       └── citation_format.py
│       │
│       ├── application/              # Application Layer
│       │   ├── __init__.py
│       │   └── services/
│       │       ├── search_service.py
│       │       ├── graph_service.py
│       │       └── citation_service.py
│       │
│       └── infrastructure/           # Infrastructure Layer
│           ├── __init__.py
│           ├── adapters/
│           │   ├── neo4j_adapter.py
│           │   ├── chromadb_adapter.py
│           │   └── embedding_adapter.py
│           ├── repositories/
│           │   ├── neo4j_theory_repository.py
│           │   └── neo4j_graph_repository.py
│           └── config.py
│
├── data/                             # Education Theory Data
│   ├── theories/
│   │   ├── learning_theories.json
│   │   ├── instructional_theories.json
│   │   ├── developmental_theories.json
│   │   └── motivation_theories.json
│   ├── relationships/
│   │   └── theory_relationships.json
│   └── schema/
│       └── theory_schema.json
│
├── tests/                            # Tests
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
├── docs/                             # Documentation
├── storage/                          # SDD Artifacts
├── steering/                         # Project Memory
├── templates/                        # Templates
│
├── docker-compose.yml
├── pyproject.toml
└── README.md
```

---

## 3. データフロー

### 3.1 MCP Tool Call Flow

```
MCP Host ──▶ JSON-RPC tools/call ──▶ Tool Handler ──▶ Service ──▶ DB
    ▲                                                              │
    └──────────────── Tool Result (content[]) ◀────────────────────┘
```

### 3.2 Resource Read Flow

```
MCP Host ──▶ resources/read {uri} ──▶ Resource Handler ──▶ Neo4j Query
    ▲                                                         │
    └──────────────── Resource Content ◀──────────────────────┘
```

---

## 4. 技術スタック

| 領域 | 技術 | 理由 |
|------|------|------|
| 言語 | Python 3.11+ | FastMCP公式サポート |
| MCP SDK | FastMCP (`mcp[cli]`) | デコレータベースAPI |
| Graph DB | Neo4j 5.x | 成熟したグラフDB |
| Vector DB | ChromaDB | ローカル開発容易 |
| Embedding | OpenAI text-embedding-3-small | 高品質 |
| Package Mgr | uv | 高速、MCP推奨 |

---

## 5. トレーサビリティ

| 要件ID | 設計コンポーネント |
|--------|-------------------|
| TOOL-001~008 | tools/*.py |
| RESOURCE-* | resources/*.py |
| PROMPT-001~006 | prompts/*.py |
| NFR-001 (MCP準拠) | server.py |

---

## 変更履歴

| バージョン | 日付 | 変更者 | 変更内容 |
|-----------|------|--------|---------|
| 1.0 | 2025-12-25 | GitHub Copilot | 初版（REST API版） |
| 2.0 | 2025-12-25 | GitHub Copilot | MCP準拠に再設計 |
