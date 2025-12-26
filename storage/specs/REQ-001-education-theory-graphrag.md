# 要件仕様書: 教育理論GraphRAG MCPサーバー

**ID**: REQ-001
**Feature**: Education Theory GraphRAG MCP Server
**Version**: 2.0
**Created**: 2025-12-25
**Updated**: 2025-12-25
**Status**: Draft
**Author**: GitHub Copilot

---

## 1. 概要

### 1.1 背景

生成AIが教育コンテンツを生成する際、教育理論に基づいたエビデンスベースのコンテンツを生成することが求められている。Model Context Protocol（MCP）を採用することで、Claude Desktop、VS Code、その他のMCP対応AIアプリケーションから標準的なインターフェースで教育理論ナレッジグラフにアクセス可能になる。

### 1.2 目的

教育理論のナレッジグラフを構築し、**MCPサーバー**として公開することで、あらゆるMCP対応AIアプリケーションが理論に基づいた教育コンテンツを生成できるようにする。

### 1.3 MCPとは

Model Context Protocol (MCP) は、AIアプリケーションと外部システムを接続するためのオープンスタンダード。MCPサーバーは以下の3つのプリミティブを提供できる：

| プリミティブ | 説明 | 制御主体 |
|-------------|------|---------|
| **Tools** | LLMが呼び出せる実行可能な関数 | Model |
| **Resources** | コンテキストとして提供する読み取り専用データ | Application |
| **Prompts** | 特定タスクのための再利用可能なテンプレート | User |

### 1.4 スコープ

| 項目 | スコープ内 | スコープ外 |
|------|-----------|-----------|
| MCPサーバー実装 | ✅ | |
| 教育理論データベース | ✅ | |
| ナレッジグラフ構築 | ✅ | |
| Tools（検索・クエリ） | ✅ | |
| Resources（理論データ） | ✅ | |
| Prompts（教育テンプレート） | ✅ | |
| MCPクライアント実装 | | ❌ |
| 独自UI | | ❌ |

---

## 2. システムアーキテクチャ

### 2.1 MCPアーキテクチャ概要

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        MCP Hosts (AI Applications)                       │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐ │
│  │Claude Desktop│  │   VS Code    │  │  Claude Code │  │ Custom App  │ │
│  │              │  │   Copilot    │  │              │  │             │ │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └──────┬──────┘ │
│         │                 │                 │                 │        │
│         └─────────────────┼─────────────────┼─────────────────┘        │
│                           │                 │                          │
│                     MCP Clients                                        │
└───────────────────────────┼─────────────────┼──────────────────────────┘
                            │                 │
                    ┌───────┴─────────────────┴───────┐
                    │     JSON-RPC 2.0 (stdio/HTTP)   │
                    └───────┬─────────────────────────┘
                            │
┌───────────────────────────┴─────────────────────────────────────────────┐
│                    TENGIN Education Theory MCP Server                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                         MCP Primitives                           │    │
│  │                                                                  │    │
│  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────────────┐  │    │
│  │  │   Tools     │    │  Resources  │    │      Prompts        │  │    │
│  │  │             │    │             │    │                     │  │    │
│  │  │ - search    │    │ - theories  │    │ - lesson_design     │  │    │
│  │  │ - query     │    │ - concepts  │    │ - assessment_create │  │    │
│  │  │ - traverse  │    │ - theorists │    │ - theory_explain    │  │    │
│  │  │ - cite      │    │ - evidence  │    │ - curriculum_plan   │  │    │
│  │  └─────────────┘    └─────────────┘    └─────────────────────┘  │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                    │                                     │
│  ┌─────────────────────────────────┴───────────────────────────────┐    │
│  │                       Core Services                              │    │
│  │                                                                  │    │
│  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────────────┐  │    │
│  │  │   Search    │    │   Graph     │    │    Citation         │  │    │
│  │  │   Service   │    │   Service   │    │    Service          │  │    │
│  │  └─────────────┘    └─────────────┘    └─────────────────────┘  │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                    │                                     │
└────────────────────────────────────┼─────────────────────────────────────┘
                                     │
        ┌────────────────────────────┼────────────────────────────┐
        │                            │                            │
        ▼                            ▼                            ▼
┌──────────────┐            ┌──────────────┐            ┌──────────────┐
│    Neo4j     │            │   ChromaDB   │            │  JSON Files  │
│  Graph DB    │            │  Vector DB   │            │  (初期データ) │
└──────────────┘            └──────────────┘            └──────────────┘
```

### 2.2 トランスポート

| トランスポート | 用途 | 特徴 |
|---------------|------|------|
| **STDIO** | ローカル実行 | Claude Desktop、VS Code連携 |
| **Streamable HTTP** | リモート実行 | 複数クライアント対応、認証対応 |

---

## 3. MCP Tools（機能要件）

### 3.1 Tools一覧

MCPサーバーが提供するTools（LLMが呼び出し可能な関数）：

| Tool名 | 説明 | 入力 | 出力 |
|--------|------|------|------|
| `search_theories` | 教育理論をセマンティック検索 | query, limit | 理論リスト |
| `get_theory` | 特定の理論の詳細を取得 | theory_id | 理論詳細 |
| `traverse_graph` | 理論間の関係をトラバース | theory_id, depth, relation_type | 関連理論グラフ |
| `find_applicable_theories` | コンテキストに適用可能な理論を検索 | context, learner_type, goal | 推奨理論リスト |
| `get_evidence` | 理論のエビデンスを取得 | theory_id | エビデンスリスト |
| `cite_theory` | 理論の引用情報を生成 | theory_id, format | 引用テキスト |
| `compare_theories` | 複数理論を比較 | theory_ids | 比較表 |
| `get_principles` | 理論の原則・原理を取得 | theory_id | 原則リスト |

---

### 3.2 Tool詳細仕様

#### TOOL-001: search_theories
**Type**: Event-driven
```
WHEN a user queries for educational theories,
the system SHALL search the knowledge graph using semantic similarity
and return relevant theories with relevance scores.
```

**JSON Schema**:
```json
{
  "name": "search_theories",
  "description": "Search for educational theories using natural language query. Returns theories relevant to the query with relevance scores.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string",
        "description": "Natural language search query (e.g., 'effective methods for teaching mathematics')"
      },
      "limit": {
        "type": "integer",
        "description": "Maximum number of results to return",
        "default": 5
      },
      "category": {
        "type": "string",
        "enum": ["learning", "instructional", "developmental", "motivation", "edtech"],
        "description": "Optional: Filter by theory category"
      }
    },
    "required": ["query"]
  }
}
```

**出力例**:
```json
{
  "content": [
    {
      "type": "text",
      "text": "Found 3 relevant theories:\n\n1. **Cognitive Load Theory** (Sweller, 1988)\n   Relevance: 0.95\n   Category: Learning Theory\n   Summary: Explains how working memory limitations affect learning...\n\n2. **Scaffolding** (Wood, Bruner, Ross, 1976)\n   Relevance: 0.87\n   ..."
    }
  ]
}
```

---

#### TOOL-002: get_theory
**Type**: Ubiquitous
```
The system SHALL provide detailed information about a specific theory
including name, description, proposer, key concepts, and evidence level.
```

**JSON Schema**:
```json
{
  "name": "get_theory",
  "description": "Get detailed information about a specific educational theory by ID or name.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "theory_id": {
        "type": "string",
        "description": "Theory ID or exact name"
      },
      "include_concepts": {
        "type": "boolean",
        "default": true,
        "description": "Include related concepts"
      },
      "include_evidence": {
        "type": "boolean",
        "default": false,
        "description": "Include supporting evidence"
      }
    },
    "required": ["theory_id"]
  }
}
```

---

#### TOOL-003: traverse_graph
**Type**: Event-driven
```
WHEN a user wants to explore relationships between theories,
the system SHALL traverse the knowledge graph from a starting theory
and return related theories based on relationship types.
```

**JSON Schema**:
```json
{
  "name": "traverse_graph",
  "description": "Traverse the theory knowledge graph to find related theories. Useful for understanding theoretical foundations, developments, and contradictions.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "theory_id": {
        "type": "string",
        "description": "Starting theory ID"
      },
      "depth": {
        "type": "integer",
        "default": 2,
        "minimum": 1,
        "maximum": 4,
        "description": "How many hops to traverse"
      },
      "relation_types": {
        "type": "array",
        "items": {
          "type": "string",
          "enum": ["BASED_ON", "EXTENDS", "CONTRADICTS", "COMPLEMENTS", "INFLUENCED_BY"]
        },
        "description": "Filter by relationship types"
      }
    },
    "required": ["theory_id"]
  }
}
```

---

#### TOOL-004: find_applicable_theories
**Type**: Event-driven
```
WHEN a user describes an educational context or goal,
the system SHALL recommend applicable theories
based on learner characteristics, subject domain, and objectives.
```

**JSON Schema**:
```json
{
  "name": "find_applicable_theories",
  "description": "Find educational theories applicable to a specific learning context. Provides recommendations based on learner type, subject, and goals.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "context": {
        "type": "string",
        "description": "Description of the educational context (e.g., 'teaching programming to beginners')"
      },
      "learner_type": {
        "type": "string",
        "enum": ["children", "adolescents", "adults", "elderly"],
        "description": "Target learner age group"
      },
      "goal": {
        "type": "string",
        "description": "Learning objective or goal"
      },
      "constraints": {
        "type": "string",
        "description": "Any constraints (e.g., 'limited time', 'online only')"
      }
    },
    "required": ["context"]
  }
}
```

---

#### TOOL-005: cite_theory
**Type**: Ubiquitous
```
The system SHALL generate properly formatted citations
for educational theories in various academic formats.
```

**JSON Schema**:
```json
{
  "name": "cite_theory",
  "description": "Generate a properly formatted citation for an educational theory.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "theory_id": {
        "type": "string",
        "description": "Theory ID to cite"
      },
      "format": {
        "type": "string",
        "enum": ["APA7", "MLA9", "Chicago", "Harvard", "IEEE"],
        "default": "APA7",
        "description": "Citation format"
      }
    },
    "required": ["theory_id"]
  }
}
```

---

#### TOOL-006: compare_theories
**Type**: Event-driven
```
WHEN a user wants to understand differences between theories,
the system SHALL provide a structured comparison
including key differences, similarities, and use cases.
```

**JSON Schema**:
```json
{
  "name": "compare_theories",
  "description": "Compare multiple educational theories side by side. Highlights differences, similarities, and appropriate use cases.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "theory_ids": {
        "type": "array",
        "items": { "type": "string" },
        "minItems": 2,
        "maxItems": 5,
        "description": "List of theory IDs to compare"
      },
      "aspects": {
        "type": "array",
        "items": {
          "type": "string",
          "enum": ["principles", "applications", "evidence", "limitations", "history"]
        },
        "description": "Aspects to compare"
      }
    },
    "required": ["theory_ids"]
  }
}
```

---

#### TOOL-007: get_evidence
**Type**: Ubiquitous
```
The system SHALL retrieve research evidence supporting a specific theory
including study details, methodology, and findings.
```

**JSON Schema**:
```json
{
  "name": "get_evidence",
  "description": "Get research evidence supporting an educational theory. Returns studies, meta-analyses, and their findings.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "theory_id": {
        "type": "string",
        "description": "Theory ID to get evidence for"
      },
      "evidence_type": {
        "type": "string",
        "enum": ["all", "meta-analysis", "rct", "quasi-experimental", "qualitative"],
        "default": "all",
        "description": "Filter by evidence type"
      },
      "limit": {
        "type": "integer",
        "default": 5,
        "description": "Maximum number of evidence items"
      }
    },
    "required": ["theory_id"]
  }
}
```

---

#### TOOL-008: get_principles
**Type**: Ubiquitous
```
The system SHALL retrieve the key principles and guidelines
derived from a specific theory with application guidance.
```

**JSON Schema**:
```json
{
  "name": "get_principles",
  "description": "Get key principles and practical guidelines derived from an educational theory.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "theory_id": {
        "type": "string",
        "description": "Theory ID to get principles for"
      },
      "include_examples": {
        "type": "boolean",
        "default": true,
        "description": "Include practical examples"
      }
    },
    "required": ["theory_id"]
  }
}
```

---

## 4. MCP Resources（データリソース）

### 4.1 Resources一覧

MCPサーバーが提供するResources（読み取り専用データ）：

| Resource URI | 説明 | MIME Type |
|--------------|------|-----------|
| `theory://list` | 全理論のリスト | application/json |
| `theory://{category}/list` | カテゴリ別理論リスト | application/json |
| `theory://{id}` | 特定理論の詳細 | application/json |
| `concept://{id}` | 概念の詳細 | application/json |
| `theorist://{id}` | 理論家の情報 | application/json |
| `evidence://{theory_id}` | 理論のエビデンス | application/json |
| `graph://schema` | グラフスキーマ情報 | application/json |
| `graph://stats` | グラフ統計情報 | application/json |

### 4.2 Resource Templates

```json
{
  "resourceTemplates": [
    {
      "uriTemplate": "theory://{category}/list",
      "name": "theories-by-category",
      "title": "Theories by Category",
      "description": "List all theories in a specific category (learning, instructional, developmental, motivation, edtech)",
      "mimeType": "application/json"
    },
    {
      "uriTemplate": "theory://{id}",
      "name": "theory-detail",
      "title": "Theory Details",
      "description": "Get detailed information about a specific theory",
      "mimeType": "application/json"
    },
    {
      "uriTemplate": "concept://{id}",
      "name": "concept-detail",
      "title": "Concept Details",
      "description": "Get detailed information about a specific concept",
      "mimeType": "application/json"
    },
    {
      "uriTemplate": "theorist://{id}",
      "name": "theorist-detail",
      "title": "Theorist Information",
      "description": "Get biographical information about an educational theorist",
      "mimeType": "application/json"
    },
    {
      "uriTemplate": "evidence://{theory_id}",
      "name": "theory-evidence",
      "title": "Theory Evidence",
      "description": "Get research evidence supporting a theory",
      "mimeType": "application/json"
    }
  ]
}
```

### 4.3 Direct Resources

```json
{
  "resources": [
    {
      "uri": "theory://list",
      "name": "all-theories",
      "title": "All Educational Theories",
      "description": "Complete list of all educational theories in the knowledge graph",
      "mimeType": "application/json"
    },
    {
      "uri": "graph://schema",
      "name": "graph-schema",
      "title": "Knowledge Graph Schema",
      "description": "Schema definition for the education theory knowledge graph",
      "mimeType": "application/json"
    },
    {
      "uri": "graph://stats",
      "name": "graph-statistics",
      "title": "Graph Statistics",
      "description": "Statistics about the knowledge graph (node counts, relationship counts, etc.)",
      "mimeType": "application/json"
    }
  ]
}
```

---

## 5. MCP Prompts（プロンプトテンプレート）

### 5.1 Prompts一覧

MCPサーバーが提供するPrompts（再利用可能なテンプレート）：

| Prompt名 | 説明 | パラメータ |
|----------|------|-----------|
| `design_lesson` | 理論に基づいた授業設計 | topic, duration, learner_level |
| `create_assessment` | 評価方法の設計 | learning_objectives, theory_basis |
| `explain_theory` | 理論の分かりやすい説明生成 | theory_id, audience |
| `apply_theory` | 理論の実践適用ガイド | theory_id, context |
| `curriculum_plan` | カリキュラム計画 | subject, duration, objectives |
| `troubleshoot_learning` | 学習課題の診断と対策 | problem_description |

### 5.2 Prompt詳細仕様

#### PROMPT-001: design_lesson

```json
{
  "name": "design_lesson",
  "title": "Design a Theory-Based Lesson",
  "description": "Create a lesson plan grounded in educational theory with evidence-based practices.",
  "arguments": [
    {
      "name": "topic",
      "description": "Lesson topic or subject",
      "required": true
    },
    {
      "name": "duration",
      "description": "Lesson duration (e.g., '45 minutes', '2 hours')",
      "required": true
    },
    {
      "name": "learner_level",
      "description": "Target learner level (e.g., 'elementary', 'undergraduate')",
      "required": true
    },
    {
      "name": "preferred_theories",
      "description": "Optional: Specific theories to incorporate",
      "required": false
    }
  ]
}
```

**生成されるプロンプト**:
```
You are an instructional designer creating a lesson plan.

Topic: {topic}
Duration: {duration}
Learner Level: {learner_level}

Use the education theory knowledge graph to find applicable theories.
Then create a detailed lesson plan that includes:

1. Learning objectives (aligned with Bloom's Taxonomy)
2. Theoretical rationale - cite specific theories from the knowledge graph
3. Instructional sequence (consider Gagné's Nine Events or similar framework)
4. Activities and materials with theoretical justification
5. Assessment strategies aligned with theory
6. Accommodations for diverse learners (reference UDL principles)

For each recommendation, use the cite_theory tool to provide proper citations.
```

---

#### PROMPT-002: create_assessment

```json
{
  "name": "create_assessment",
  "title": "Create Theory-Based Assessment",
  "description": "Design assessments aligned with educational theory and learning objectives.",
  "arguments": [
    {
      "name": "learning_objectives",
      "description": "Learning objectives to assess",
      "required": true
    },
    {
      "name": "assessment_type",
      "description": "Type of assessment (formative, summative, diagnostic)",
      "required": true
    },
    {
      "name": "theory_basis",
      "description": "Optional: Specific theories to base assessment on",
      "required": false
    }
  ]
}
```

---

#### PROMPT-003: explain_theory

```json
{
  "name": "explain_theory",
  "title": "Explain Educational Theory",
  "description": "Generate a clear, accessible explanation of an educational theory for a specific audience.",
  "arguments": [
    {
      "name": "theory_id",
      "description": "ID of the theory to explain",
      "required": true
    },
    {
      "name": "audience",
      "description": "Target audience (e.g., 'teachers', 'parents', 'students', 'administrators')",
      "required": true
    },
    {
      "name": "depth",
      "description": "Explanation depth: 'brief', 'moderate', 'comprehensive'",
      "required": false
    }
  ]
}
```

**生成されるプロンプト**:
```
First, use the get_theory tool to retrieve detailed information about the theory: {theory_id}
Also use get_principles and get_evidence to gather supporting information.

Then explain this theory to {audience} at a {depth} level.

Your explanation should:
1. Start with a relatable analogy or example
2. Explain the core principles in accessible language
3. Provide practical implications for the audience
4. Address common misconceptions
5. Suggest how to apply this theory in practice

Include proper citations using the cite_theory tool.
```

---

#### PROMPT-004: apply_theory

```json
{
  "name": "apply_theory",
  "title": "Apply Theory to Practice",
  "description": "Generate practical guidance for applying an educational theory in a specific context.",
  "arguments": [
    {
      "name": "theory_id",
      "description": "ID of the theory to apply",
      "required": true
    },
    {
      "name": "context",
      "description": "Specific educational context (e.g., 'teaching math to 5th graders')",
      "required": true
    },
    {
      "name": "constraints",
      "description": "Any constraints or limitations",
      "required": false
    }
  ]
}
```

---

#### PROMPT-005: curriculum_plan

```json
{
  "name": "curriculum_plan",
  "title": "Create Curriculum Plan",
  "description": "Develop a comprehensive curriculum plan grounded in educational theory.",
  "arguments": [
    {
      "name": "subject",
      "description": "Subject or topic area",
      "required": true
    },
    {
      "name": "duration",
      "description": "Curriculum duration (e.g., 'semester', 'year')",
      "required": true
    },
    {
      "name": "learner_level",
      "description": "Target learner level",
      "required": true
    },
    {
      "name": "objectives",
      "description": "High-level learning objectives",
      "required": true
    }
  ]
}
```

---

#### PROMPT-006: troubleshoot_learning

```json
{
  "name": "troubleshoot_learning",
  "title": "Troubleshoot Learning Issues",
  "description": "Diagnose learning challenges and suggest theory-based interventions.",
  "arguments": [
    {
      "name": "problem_description",
      "description": "Description of the learning challenge or problem",
      "required": true
    },
    {
      "name": "learner_context",
      "description": "Information about the learner (age, subject, etc.)",
      "required": false
    },
    {
      "name": "interventions_tried",
      "description": "Previous interventions that have been attempted",
      "required": false
    }
  ]
}
```

**生成されるプロンプト**:
```
Analyze this learning challenge:

Problem: {problem_description}
Learner Context: {learner_context}
Previous Interventions: {interventions_tried}

Use the search_theories tool to find theories that address this type of challenge.
Use the traverse_graph tool to explore related theories and concepts.

Provide:
1. Theoretical diagnosis - what theories explain this challenge?
2. Root cause analysis based on educational theory
3. Theory-based interventions with citations
4. Implementation steps for each intervention
5. How to measure improvement

Support each recommendation with evidence from the knowledge graph.
```

---

## 6. ドメインモデル

### 6.1 教育理論の分類体系

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

### 6.2 ナレッジグラフのエンティティ

| エンティティ | 説明 | 属性 |
|-------------|------|------|
| Theory | 教育理論 | id, name, name_en, description, year, category, evidence_level |
| Theorist | 理論家 | id, name, name_ja, biography, affiliation |
| Concept | 概念 | id, name, definition, examples |
| Principle | 原理・原則 | id, name, description, application_guide |
| Evidence | エビデンス | id, title, authors, year, methodology, findings |

### 6.3 ナレッジグラフのリレーション

| リレーション | From | To | 説明 |
|-------------|------|-----|------|
| PROPOSED_BY | Theory | Theorist | 理論の提唱者 |
| BASED_ON | Theory | Theory | 理論の基盤 |
| CONTRADICTS | Theory | Theory | 対立する理論 |
| EXTENDS | Theory | Theory | 発展・拡張 |
| COMPLEMENTS | Theory | Theory | 補完関係 |
| CONTAINS | Theory | Concept | 含まれる概念 |
| HAS_PRINCIPLE | Theory | Principle | 導出される原則 |
| SUPPORTED_BY | Theory | Evidence | 支持するエビデンス |

---

## 7. 非機能要件

### NFR-001: MCPプロトコル準拠
```
The system SHALL implement MCP specification version 2025-06-18
with full support for tools, resources, and prompts primitives.
```

### NFR-002: トランスポート対応
```
The system SHALL support both STDIO transport (for local execution)
and Streamable HTTP transport (for remote server deployment).
```

### NFR-003: パフォーマンス
```
The system SHALL respond to tool calls within 2 seconds for 95% of requests.
```
- Tool応答: < 2秒 (P95)
- Resource読み取り: < 500ms (P95)

### NFR-004: スケーラビリティ
```
The system SHALL support a knowledge graph with up to 10,000 theories
and 100,000 relationships.
```

### NFR-005: ロギング
```
The system SHALL log all operations to stderr (for STDIO transport)
to avoid corrupting JSON-RPC messages on stdout.
```

### NFR-006: エラーハンドリング
```
IF a tool call fails, THEN the system SHALL return a structured error response
with error code, message, and recovery suggestions.
```

---

## 8. データ要件

### 8.1 初期データセット

| カテゴリ | 理論数 | 概念数 | 主要な理論 |
|---------|--------|--------|-----------|
| 学習理論 | 15+ | 50+ | 行動主義、認知主義、構成主義 |
| 教授理論 | 10+ | 30+ | ガニェ、メリル、ARCS |
| 発達理論 | 8+ | 25+ | ピアジェ、ヴィゴツキー |
| 動機付け理論 | 10+ | 35+ | 自己決定理論、フロー理論 |
| 教育工学 | 8+ | 20+ | ADDIE、UDL |

---

## 9. 接続・デプロイ

### 9.1 Claude Desktop連携設定

```json
{
  "mcpServers": {
    "tengin-education": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/tengin-graphrag",
        "run",
        "tengin-server"
      ]
    }
  }
}
```

### 9.2 VS Code連携設定

```json
{
  "mcp": {
    "servers": {
      "tengin-education": {
        "command": "uv",
        "args": ["--directory", "/path/to/tengin-graphrag", "run", "tengin-server"]
      }
    }
  }
}
```

### 9.3 HTTPサーバーモード

```bash
# HTTPサーバーとして起動
tengin-server --transport http --port 8080
```

---

## 10. トレーサビリティ

| 要件ID | 設計 | 実装 | テスト |
|--------|------|------|--------|
| TOOL-001 (search_theories) | - | - | - |
| TOOL-002 (get_theory) | - | - | - |
| TOOL-003 (traverse_graph) | - | - | - |
| TOOL-004 (find_applicable_theories) | - | - | - |
| TOOL-005 (cite_theory) | - | - | - |
| TOOL-006 (compare_theories) | - | - | - |
| TOOL-007 (get_evidence) | - | - | - |
| TOOL-008 (get_principles) | - | - | - |
| RESOURCE-* | - | - | - |
| PROMPT-001~006 | - | - | - |

*実装後に更新*

---

## 変更履歴

| バージョン | 日付 | 変更者 | 変更内容 |
|-----------|------|--------|---------|
| 1.0 | 2025-12-25 | GitHub Copilot | 初版作成（REST API版） |
| 2.0 | 2025-12-25 | GitHub Copilot | MCP準拠に再定義 |
