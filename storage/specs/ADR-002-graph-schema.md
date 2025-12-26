# ADR-002: グラフスキーマ設計

**Status**: Accepted
**Date**: 2025-12-25
**Deciders**: Development Team
**Related**: REQ-001, DESIGN-001, ADR-001

---

## Context

教育理論のナレッジグラフを構築するにあたり、Neo4jのノードラベル、プロパティ、リレーションシップタイプを定義する必要がある。

## Decision

### ノードラベル（エンティティ）

```cypher
// 理論 (Theory)
(:Theory {
  id: STRING,           // UUID
  name: STRING,         // 理論名（日本語）
  name_en: STRING,      // 理論名（英語）
  description: STRING,  // 説明
  category: STRING,     // カテゴリ（learning, instructional, developmental, motivation, edtech）
  year_proposed: INTEGER, // 提唱年
  keywords: LIST<STRING>, // キーワード
  evidence_level: STRING, // エビデンスレベル（strong, moderate, limited, theoretical）
  created_at: DATETIME,
  updated_at: DATETIME
})

// 概念 (Concept)
(:Concept {
  id: STRING,
  name: STRING,
  name_en: STRING,
  definition: STRING,   // 定義
  examples: LIST<STRING>, // 例
  created_at: DATETIME,
  updated_at: DATETIME
})

// 理論家 (Theorist)
(:Theorist {
  id: STRING,
  name: STRING,         // 名前
  name_ja: STRING,      // 日本語名
  birth_year: INTEGER,
  death_year: INTEGER,  // NULL if alive
  nationality: STRING,
  affiliation: STRING,  // 所属
  biography: STRING,    // 略歴
  created_at: DATETIME,
  updated_at: DATETIME
})

// 原理・原則 (Principle)
(:Principle {
  id: STRING,
  name: STRING,
  name_en: STRING,
  description: STRING,
  application_guide: STRING, // 適用ガイド
  evidence_level: STRING,
  created_at: DATETIME,
  updated_at: DATETIME
})

// エビデンス (Evidence)
(:Evidence {
  id: STRING,
  title: STRING,        // 研究タイトル
  authors: LIST<STRING>,
  year: INTEGER,
  source_type: STRING,  // journal, book, meta-analysis, review
  journal: STRING,
  doi: STRING,
  methodology: STRING,  // RCT, quasi-experimental, qualitative, etc.
  sample_size: INTEGER,
  findings: STRING,     // 主要な発見
  effect_size: FLOAT,   // 効果量（あれば）
  created_at: DATETIME,
  updated_at: DATETIME
})

// 適用コンテキスト (ApplicationContext)
(:ApplicationContext {
  id: STRING,
  name: STRING,         // e.g., "K-12 Mathematics", "Corporate Training"
  description: STRING,
  age_range: STRING,    // e.g., "6-12", "adult"
  domain: STRING,       // education, training, etc.
  created_at: DATETIME,
  updated_at: DATETIME
})
```

### リレーションシップタイプ

```cypher
// 理論 - 理論家
(:Theory)-[:PROPOSED_BY {year: INTEGER}]->(:Theorist)
(:Theory)-[:DEVELOPED_BY {year: INTEGER, contribution: STRING}]->(:Theorist)

// 理論 - 理論（関係性）
(:Theory)-[:BASED_ON {description: STRING}]->(:Theory)
(:Theory)-[:EXTENDS {description: STRING}]->(:Theory)
(:Theory)-[:CONTRADICTS {description: STRING}]->(:Theory)
(:Theory)-[:COMPLEMENTS {description: STRING}]->(:Theory)
(:Theory)-[:INFLUENCED_BY {description: STRING}]->(:Theory)

// 理論 - 概念
(:Theory)-[:CONTAINS {importance: STRING}]->(:Concept)
(:Theory)-[:DEFINES]->(:Concept)

// 理論 - 原理
(:Theory)-[:HAS_PRINCIPLE {order: INTEGER}]->(:Principle)

// 理論 - エビデンス
(:Theory)-[:SUPPORTED_BY {relevance: FLOAT}]->(:Evidence)
(:Theory)-[:CHALLENGED_BY {relevance: FLOAT}]->(:Evidence)

// 理論 - 適用コンテキスト
(:Theory)-[:EFFECTIVE_FOR {effectiveness: STRING, conditions: STRING}]->(:ApplicationContext)
(:Theory)-[:NOT_RECOMMENDED_FOR {reason: STRING}]->(:ApplicationContext)

// 概念 - 概念
(:Concept)-[:RELATED_TO {description: STRING}]->(:Concept)
(:Concept)-[:PREREQUISITE_OF]->(:Concept)

// 理論家 - 理論家
(:Theorist)-[:INFLUENCED]->(:Theorist)
(:Theorist)-[:COLLABORATED_WITH]->(:Theorist)
```

### グラフスキーマ図

```
                                    ┌─────────────┐
                                    │  Theorist   │
                                    │             │
                                    │  - name     │
                                    │  - bio      │
                                    └──────┬──────┘
                                           │
                          PROPOSED_BY      │      INFLUENCED
                        ┌──────────────────┼──────────────────┐
                        │                  │                  │
                        ▼                  ▼                  ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Evidence   │    │   Theory    │    │   Theory    │    │  Theorist   │
│             │◀───│             │───▶│             │    │             │
│  - title    │    │  - name     │    │  - name     │    └─────────────┘
│  - findings │    │  - category │    │  - category │
└─────────────┘    │  - evidence │    └─────────────┘
  SUPPORTED_BY     │    _level   │         ▲
                   └──────┬──────┘         │
                          │                │ BASED_ON / EXTENDS
          ┌───────────────┼───────────────┘
          │               │
          ▼               ▼
    ┌─────────────┐  ┌─────────────┐
    │   Concept   │  │  Principle  │
    │             │  │             │
    │  - name     │  │  - name     │
    │  - definition│ │  - guide    │
    └──────┬──────┘  └─────────────┘
           │
           │ RELATED_TO
           ▼
    ┌─────────────┐
    │   Concept   │
    └─────────────┘
           │
           │ EFFECTIVE_FOR
           ▼
    ┌─────────────┐
    │ Application │
    │   Context   │
    └─────────────┘
```

---

## インデックス定義

```cypher
// ユニーク制約
CREATE CONSTRAINT theory_id IF NOT EXISTS FOR (t:Theory) REQUIRE t.id IS UNIQUE;
CREATE CONSTRAINT concept_id IF NOT EXISTS FOR (c:Concept) REQUIRE c.id IS UNIQUE;
CREATE CONSTRAINT theorist_id IF NOT EXISTS FOR (th:Theorist) REQUIRE th.id IS UNIQUE;
CREATE CONSTRAINT principle_id IF NOT EXISTS FOR (p:Principle) REQUIRE p.id IS UNIQUE;
CREATE CONSTRAINT evidence_id IF NOT EXISTS FOR (e:Evidence) REQUIRE e.id IS UNIQUE;

// 検索用インデックス
CREATE INDEX theory_name IF NOT EXISTS FOR (t:Theory) ON (t.name);
CREATE INDEX theory_category IF NOT EXISTS FOR (t:Theory) ON (t.category);
CREATE INDEX concept_name IF NOT EXISTS FOR (c:Concept) ON (c.name);
CREATE INDEX theorist_name IF NOT EXISTS FOR (th:Theorist) ON (th.name);

// 全文検索インデックス
CREATE FULLTEXT INDEX theory_fulltext IF NOT EXISTS 
  FOR (t:Theory) ON EACH [t.name, t.name_en, t.description, t.keywords];
CREATE FULLTEXT INDEX concept_fulltext IF NOT EXISTS 
  FOR (c:Concept) ON EACH [c.name, c.name_en, c.definition];
```

---

## Consequences

### Good

- 教育理論の複雑な関係性を表現可能
- Cypherによる直感的なトラバーサルクエリ
- 全文検索インデックスによる高速検索
- エビデンスレベルの追跡が可能

### Bad

- スキーマ変更時のマイグレーションが必要
- 大量のリレーションシップでクエリ最適化が必要な場合あり

---

## 変更履歴

| バージョン | 日付 | 変更内容 |
|-----------|------|---------|
| 1.0 | 2025-12-25 | 初版作成 |
