# API リファレンス

TENGIN-GraphRAG MCP Server の全ツール・リソース・プロンプトのAPIリファレンスです。

## 目次

- [Tools (23ツール)](#tools)
  - [Theory Tools (7)](#theory-tools)
  - [Graph Tools (4)](#graph-tools)
  - [Citation Tools (2)](#citation-tools)
  - [Methodology Tools (6)](#methodology-tools)
  - [System Tools (4)](#system-tools)
- [Resources (5リソース)](#resources)
- [Prompts (3プロンプト)](#prompts)

---

## Tools

### Theory Tools

教育理論の検索・取得に関するツール群。

#### `search_theories`

教育理論をキーワード、カテゴリ、エビデンスレベルで検索します。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|-----|---|-----|-----|
| `query` | string | ✗ | 検索キーワード |
| `category` | string | ✗ | カテゴリフィルタ（learning, instructional, developmental, motivation, edtech, adult_learning, intelligence） |
| `evidence_level` | string | ✗ | エビデンスレベル（strong, moderate, limited, theoretical, emerging） |
| `limit` | int | ✗ | 結果数上限（デフォルト: 10） |

**レスポンス例:**
```json
{
  "query": "認知負荷",
  "category": null,
  "evidence_level": null,
  "count": 2,
  "theories": [
    {
      "id": "cognitive-load-theory",
      "name": "認知負荷理論",
      "name_en": "Cognitive Load Theory",
      "category": "learning",
      "evidence_level": "strong"
    }
  ]
}
```

---

#### `get_theory`

特定の理論の詳細情報を取得します。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|-----|---|-----|-----|
| `theory_id` | string | ✓ | 理論のID |

**レスポンス例:**
```json
{
  "id": "cognitive-load-theory",
  "name": "認知負荷理論",
  "name_en": "Cognitive Load Theory",
  "description": "ワーキングメモリの限界に基づいた教授設計理論...",
  "category": "learning",
  "year": 1988,
  "evidence_level": "strong",
  "keywords": ["ワーキングメモリ", "認知負荷", "教授設計"],
  "theorist": {
    "id": "sweller",
    "name": "ジョン・スウェラー"
  },
  "concepts": [...],
  "principles": [...],
  "evidence": [...]
}
```

---

#### `get_theories_by_category`

カテゴリ別に理論一覧を取得します。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|-----|---|-----|-----|
| `category` | string | ✓ | カテゴリ名 |

**カテゴリ一覧:**
- `learning` - 学習理論（認知主義、構成主義など）
- `instructional` - 教授理論（ガニェ、ARCS等）
- `developmental` - 発達理論（ピアジェ、ヴィゴツキー等）
- `motivation` - 動機付け理論（自己決定理論等）
- `edtech` - 教育工学（ADDIE、UDL等）
- `adult_learning` - 成人学習理論
- `intelligence` - 知能理論

---

#### `get_theorist`

理論家の詳細情報を取得します。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|-----|---|-----|-----|
| `theorist_id` | string | ✓ | 理論家のID |

**レスポンス例:**
```json
{
  "id": "sweller",
  "name": "ジョン・スウェラー",
  "name_en": "John Sweller",
  "birth_year": 1946,
  "nationality": "オーストラリア",
  "affiliation": "ニューサウスウェールズ大学",
  "biography": "認知負荷理論の提唱者...",
  "major_works": ["Cognitive Load Theory (1988)"],
  "theories": ["cognitive-load-theory"]
}
```

---

#### `get_concept`

概念の詳細情報を取得します。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|-----|---|-----|-----|
| `concept_id` | string | ✓ | 概念のID |

---

#### `get_principle`

原則の詳細情報を取得します。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|-----|---|-----|-----|
| `principle_id` | string | ✓ | 原則のID |

---

### Graph Tools

グラフトラバーサル・関係探索に関するツール群。

#### `traverse_graph`

指定ノードから関連ノードをトラバースします。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|-----|---|-----|-----|
| `start_node_id` | string | ✓ | 開始ノードのID |
| `relationship_types` | list[string] | ✗ | 関係タイプのフィルタ |
| `max_depth` | int | ✗ | 最大深度（デフォルト: 2） |
| `direction` | string | ✗ | 方向（outgoing, incoming, both） |

**関係タイプ一覧:**
- `PROPOSED_BY` - 理論家による提案
- `HAS_CONCEPT` - 概念を含む
- `HAS_PRINCIPLE` - 原則を持つ
- `SUPPORTED_BY` - エビデンスによる支持
- `BUILDS_ON` - 基盤理論
- `CONTRASTS_WITH` - 対照理論
- `COMPLEMENTS` - 相補理論
- `THEORETICALLY_GROUNDED_IN` - 理論的基盤
- `APPLICABLE_IN` - 適用文脈
- `EFFECTIVE_FOR` - 効果的な文脈

---

#### `find_path`

2つのノード間の最短経路を探索します。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|-----|---|-----|-----|
| `start_node_id` | string | ✓ | 開始ノードのID |
| `end_node_id` | string | ✓ | 終了ノードのID |
| `max_depth` | int | ✗ | 最大深度（デフォルト: 5） |

---

#### `get_related_nodes`

指定ノードに関連するノードを取得します。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|-----|---|-----|-----|
| `node_id` | string | ✓ | ノードのID |
| `relationship_type` | string | ✗ | 関係タイプ（オプション） |

---

#### `get_graph_statistics`

グラフ全体の統計情報を取得します。

**パラメータ:** なし

**レスポンス例:**
```json
{
  "total_nodes": 130,
  "total_relationships": 303,
  "nodes_by_label": {
    "Theory": 38,
    "Theorist": 27,
    "Concept": 25,
    "Methodology": 15,
    "Evidence": 15,
    "Context": 10
  },
  "relationships_by_type": {
    "PROPOSED_BY": 38,
    "HAS_CONCEPT": 45,
    "BUILDS_ON": 28
  }
}
```

---

### Citation Tools

引用生成に関するツール群。

#### `cite_theory`

理論の引用文を生成します。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|-----|---|-----|-----|
| `theory_id` | string | ✓ | 理論のID |
| `format` | string | ✗ | 引用形式（APA7, MLA9, Chicago, Harvard, IEEE） |

**レスポンス例:**
```json
{
  "theory_id": "cognitive-load-theory",
  "format": "APA7",
  "citation": "Sweller, J. (1988). Cognitive load theory. In Learning and instruction (Vol. 1, pp. 123-456). Elsevier.",
  "in_text": "(Sweller, 1988)"
}
```

---

#### `compare_theories`

複数の理論を比較分析します。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|-----|---|-----|-----|
| `theory_ids` | list[string] | ✓ | 比較する理論IDのリスト |

**レスポンス例:**
```json
{
  "theories": [
    {"id": "cognitive-load-theory", "name": "認知負荷理論"},
    {"id": "constructivism", "name": "構成主義"}
  ],
  "comparison": {
    "categories": ["learning", "learning"],
    "evidence_levels": ["strong", "strong"],
    "relationships": [
      {"type": "COMPLEMENTS", "description": "相補関係にある"}
    ],
    "common_concepts": ["学習者中心"],
    "differences": ["認知プロセス重視 vs 社会的構成重視"]
  }
}
```

---

### Methodology Tools

教授法・文脈に関するツール群。

#### `search_methodologies`

教授法を検索します。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|-----|---|-----|-----|
| `query` | string | ✗ | 検索キーワード |
| `category` | string | ✗ | カテゴリフィルタ |
| `evidence_level` | string | ✗ | エビデンスレベル |
| `theory_id` | string | ✗ | 理論的基盤でフィルタ |
| `limit` | int | ✗ | 結果数上限 |

---

#### `get_methodology`

教授法の詳細を取得します。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|-----|---|-----|-----|
| `methodology_id` | string | ✓ | 教授法のID |

---

#### `search_contexts`

教育文脈を検索します。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|-----|---|-----|-----|
| `education_level` | string | ✗ | 教育段階（k12, higher-education等） |
| `subject_area` | string | ✗ | 教科領域（STEM, humanities等） |
| `effective_for_theory` | string | ✗ | 理論IDでフィルタ |
| `limit` | int | ✗ | 結果数上限 |

---

#### `get_context`

文脈の詳細を取得します。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|-----|---|-----|-----|
| `context_id` | string | ✓ | 文脈のID |

---

#### `recommend_methodologies`

条件に基づいて教授法を推薦します。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|-----|---|-----|-----|
| `context_id` | string | ✗ | 文脈ID |
| `theory_id` | string | ✗ | 理論ID |
| `min_evidence_level` | string | ✗ | 最低エビデンスレベル |

---

#### `get_evidence_for_theory`

理論に対するエビデンスを取得します。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|-----|---|-----|-----|
| `theory_id` | string | ✓ | 理論のID |
| `include_challenges` | bool | ✗ | 挑戦するエビデンスも含むか |

---

### System Tools

システム管理・監視に関するツール群。

#### `get_cache_stats`

キャッシュの統計情報を取得します。

**パラメータ:** なし

**レスポンス例:**
```json
{
  "theory_cache": {
    "hits": 150,
    "misses": 20,
    "hit_rate": 88.24,
    "size": 45
  },
  "graph_cache": {
    "hits": 80,
    "misses": 10,
    "hit_rate": 88.89,
    "size": 20
  },
  "total": {
    "hits": 230,
    "misses": 30,
    "hit_rate": 88.46
  }
}
```

---

#### `clear_cache`

キャッシュをクリアします。

**パラメータ:**

| 名前 | 型 | 必須 | 説明 |
|-----|---|-----|-----|
| `cache_type` | string | ✗ | "theory", "graph", または null（全て） |

---

#### `health_check`

システムの健康状態をチェックします。

**パラメータ:** なし

**レスポンス例:**
```json
{
  "status": "healthy",
  "components": {
    "theory_repository": {"status": "healthy", "theory_count": 38},
    "graph_repository": {"status": "healthy", "node_count": 130},
    "vector_repository": {"status": "healthy"},
    "cache": {"status": "healthy", "theory_cache_size": 45}
  }
}
```

---

#### `get_system_info`

システム情報を取得します。

**パラメータ:** なし

**レスポンス例:**
```json
{
  "name": "TENGIN Education Theory MCP Server",
  "version": "0.1.0",
  "features": {"tools": 23, "resources": 5, "prompts": 3},
  "capabilities": ["theory_search", "graph_traversal", ...],
  "supported_categories": ["learning", "instructional", ...]
}
```

---

## Resources

MCPリソースはURIスキームでアクセスします。

### `theory://list`

全理論の一覧を取得します。

**URI:** `theory://list`

---

### `theory://{id}`

特定の理論の詳細を取得します。

**URI例:** `theory://cognitive-load-theory`

---

### `concept://{id}`

特定の概念の詳細を取得します。

**URI例:** `concept://cognitive-load`

---

### `theorist://{id}`

特定の理論家の詳細を取得します。

**URI例:** `theorist://sweller`

---

### `graph://schema`

グラフスキーマ情報を取得します。

**URI:** `graph://schema`

---

## Prompts

### `design_lesson`

理論に基づいた授業設計を支援するプロンプト。

**引数:**

| 名前 | 型 | 説明 |
|-----|---|-----|
| `topic` | string | 授業トピック |
| `target_audience` | string | 対象者 |
| `theories` | list[string] | 適用する理論ID |

---

### `create_assessment`

理論に基づいた評価方法を設計するプロンプト。

**引数:**

| 名前 | 型 | 説明 |
|-----|---|-----|
| `learning_objectives` | string | 学習目標 |
| `theories` | list[string] | 適用する理論ID |

---

### `explain_theory`

理論の分かりやすい説明を生成するプロンプト。

**引数:**

| 名前 | 型 | 説明 |
|-----|---|-----|
| `theory_id` | string | 理論ID |
| `audience_level` | string | 対象レベル（beginner, intermediate, expert） |

---

## エラーコード

| コード | 説明 |
|-------|-----|
| `THEORY_NOT_FOUND` | 指定された理論が見つからない |
| `CONCEPT_NOT_FOUND` | 指定された概念が見つからない |
| `THEORIST_NOT_FOUND` | 指定された理論家が見つからない |
| `ENTITY_NOT_FOUND` | 指定されたエンティティが見つからない |
| `INVALID_QUERY` | 無効なクエリパラメータ |
| `GRAPH_TRAVERSAL_ERROR` | グラフトラバーサルエラー |
| `DATABASE_CONNECTION_ERROR` | データベース接続エラー |

---

*Last Updated: 2025-12-26*
