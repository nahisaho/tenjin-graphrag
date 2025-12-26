# Project Structure

**Project**: TENGIN-GraphRAG
**Last Updated**: 2025-12-26
**Version**: 1.0

---

## Architecture Pattern

**Primary Pattern**: Clean Architecture + MCP Server

> このプロジェクトはClean Architecture（Onion Architecture）パターンを採用しています。
> ドメイン層を中心に、Application層、Infrastructure層、Interface層（MCP Tools/Resources/Prompts）を分離し、
> 依存性逆転の原則に基づいて構築されています。
> 
> インターフェースとしてModel Context Protocol（MCP）サーバーを採用し、
> LLMアプリケーションとの統合を実現しています。

---

## Architecture Layers (Language-Agnostic)

The following layer definitions apply regardless of programming language:

### Layer 1: Domain / Core

**Purpose**: Business logic and domain models
**Rules**:

- MUST NOT depend on any other layer
- Contains: Entities, Value Objects, Domain Services, Domain Events
- No framework dependencies, no I/O

**Language Examples**:
| Language | Location | Pattern |
|----------|----------|---------|
| TypeScript | `lib/{feature}/domain/` | Classes/Types |
| Rust | `{crate}/src/domain/` | Structs + Traits |
| Python | `src/{pkg}/domain/` | Dataclasses |
| Go | `internal/domain/` | Structs + Interfaces |
| Java | `src/main/.../domain/` | Classes + Records |

### Layer 2: Application / Use Cases

**Purpose**: Orchestrate domain logic, implement use cases
**Rules**:

- Depends only on Domain layer
- Contains: Application Services, Commands, Queries, DTOs
- No direct I/O (uses ports/interfaces)

**Language Examples**:
| Language | Location | Pattern |
|----------|----------|---------|
| TypeScript | `lib/{feature}/application/` | Service classes |
| Rust | `{crate}/src/application/` | Impl blocks |
| Python | `src/{pkg}/application/` | Service functions |
| Go | `internal/app/` | Service structs |
| Java | `src/main/.../application/` | @Service classes |

### Layer 3: Infrastructure / Adapters

**Purpose**: External integrations (DB, APIs, messaging)
**Rules**:

- Depends on Application layer (implements ports)
- Contains: Repositories, API Clients, Message Publishers
- All I/O operations here

**Language Examples**:
| Language | Location | Pattern |
|----------|----------|---------|
| TypeScript | `lib/{feature}/infrastructure/` | Repository impls |
| Rust | `{crate}/src/infrastructure/` | Trait impls |
| Python | `src/{pkg}/infrastructure/` | Repository classes |
| Go | `internal/infra/` | Interface impls |
| Java | `src/main/.../infrastructure/` | @Repository classes |

### Layer 4: Interface / Presentation

**Purpose**: Entry points (CLI, API, Web UI)
**Rules**:

- Depends on Application layer
- Contains: Controllers, CLI handlers, API routes
- Input validation and response formatting

**Language Examples**:
| Language | Location | Pattern |
|----------|----------|---------|
| TypeScript | `app/api/` or `cli/` | Route handlers |
| Rust | `{crate}/src/api/` or `cli/` | Axum handlers |
| Python | `src/{pkg}/api/` or `cli/` | FastAPI routes |
| Go | `cmd/` or `internal/api/` | HTTP handlers |
| Java | `src/main/.../api/` | @RestController |

### Layer Dependency Rules

```
┌─────────────────────────────────────────┐
│        Interface / Presentation         │ ← Entry points
├─────────────────────────────────────────┤
│        Application / Use Cases          │ ← Orchestration
├─────────────────────────────────────────┤
│        Infrastructure / Adapters        │ ← I/O & External
├─────────────────────────────────────────┤
│            Domain / Core                │ ← Pure business logic
└─────────────────────────────────────────┘

Dependency Direction: ↓ (outer → inner)
Domain layer has NO dependencies
```

---

## Directory Organization

### Root Structure

```
TENGIN-GraphRAG/
├── src/                  # ソースコード
│   └── tengin_mcp/       # メインパッケージ
│       ├── server.py     # MCPサーバーエントリーポイント
│       ├── domain/       # ドメイン層
│       ├── application/  # アプリケーション層
│       ├── infrastructure/ # インフラ層
│       ├── tools/        # MCPツール
│       ├── resources/    # MCPリソース
│       ├── prompts/      # MCPプロンプト
│       └── scripts/      # ユーティリティスクリプト
├── tests/                # テストスイート
│   ├── unit/             # ユニットテスト
│   ├── integration/      # 統合テスト
│   └── e2e/              # E2Eテスト
├── data/                 # データファイル
│   ├── chromadb/         # ChromaDBストレージ
│   ├── theories/         # 理論データ（JSON）
│   ├── relationships/    # 関係データ
│   └── schema/           # スキーマ定義
├── docs/                 # ドキュメント
├── storage/              # SDD成果物
│   ├── specs/            # 要件、設計、タスク
│   ├── changes/          # 差分仕様（ブラウンフィールド）
│   └── archive/          # アーカイブ済み仕様
├── steering/             # プロジェクトメモリ（このディレクトリ）
│   ├── structure.ja.md   # このファイル
│   ├── tech.ja.md        # 技術スタック
│   ├── product.ja.md     # プロダクトコンテキスト
│   ├── project.yml       # プロジェクト設定
│   └── rules/            # 憲法ガバナンス
├── templates/            # ドキュメントテンプレート
├── pyproject.toml        # Python プロジェクト設定
└── docker-compose.yml    # Docker Compose 設定
```

---

## Clean Architecture Pattern

このプロジェクトはClean Architecture（Onion Architecture）パターンを採用しています。

### パッケージ構造

```
src/tengin_mcp/
├── domain/               # ドメイン層（最内層）
│   ├── entities/         # エンティティ
│   │   ├── theory.py     # 理論エンティティ
│   │   ├── concept.py    # 概念エンティティ
│   │   ├── principle.py  # 原則エンティティ
│   │   ├── theorist.py   # 理論家エンティティ
│   │   └── evidence.py   # エビデンスエンティティ
│   ├── value_objects/    # 値オブジェクト
│   │   ├── theory_category.py
│   │   ├── citation_format.py
│   │   └── evidence_level.py
│   ├── repositories/     # リポジトリインターフェース
│   │   └── interfaces.py
│   └── errors.py         # ドメインエラー
├── application/          # アプリケーション層
│   └── services/         # アプリケーションサービス
├── infrastructure/       # インフラストラクチャ層
│   ├── config.py         # 設定管理
│   ├── adapters/         # 外部サービスアダプター
│   │   ├── neo4j_adapter.py
│   │   ├── chromadb_adapter.py
│   │   └── embedding_adapter.py
│   └── repositories/     # リポジトリ実装
│       ├── neo4j_theory_repository.py
│       └── neo4j_graph_repository.py
├── tools/                # MCPツール（インターフェース層）
│   ├── theory_tools.py   # 理論検索・取得ツール (7ツール)
│   ├── graph_tools.py    # グラフトラバーサルツール (4ツール)
│   ├── citation_tools.py # 引用生成ツール (2ツール)
│   ├── methodology_tools.py # 教授法・文脈ツール (6ツール)
│   └── system_tools.py   # システム管理ツール (4ツール)
├── resources/            # MCPリソース（インターフェース層）
│   └── theory_resources.py
├── prompts/              # MCPプロンプト（インターフェース層）
│   └── education_prompts.py
└── server.py             # エントリーポイント
```

### 層の依存関係ルール

- **Domain層**: 他の層に依存しない（純粋なビジネスロジック）
- **Application層**: Domain層のみに依存
- **Infrastructure層**: Domain層、Application層に依存
- **Interface層（Tools/Resources/Prompts）**: 全ての層を利用可能

### Application Guidelines

- **Library Usage**: Applications import from `lib/` modules
- **Thin Controllers**: API routes delegate to library services
- **No Business Logic**: Business logic belongs in libraries

---

## Component Organization

### UI Components

```
components/
├── ui/                   # Base UI components (shadcn/ui)
│   ├── button.tsx
│   ├── input.tsx
│   └── card.tsx
├── auth/                 # Feature-specific components
│   ├── LoginForm.tsx
│   └── RegisterForm.tsx
├── dashboard/
│   └── StatsCard.tsx
└── shared/               # Shared components
    ├── Header.tsx
    └── Footer.tsx
```

### Component Guidelines

- **Composition**: Prefer composition over props drilling
- **Types**: All props typed with TypeScript
- **Tests**: Component tests with React Testing Library

---

## Database Organization

### Schema Organization

```
prisma/
├── schema.prisma         # Prisma schema
├── migrations/           # Database migrations
│   ├── 001_create_users_table/
│   │   └── migration.sql
│   └── 002_create_sessions_table/
│       └── migration.sql
└── seed.ts               # Database seed data
```

### Database Guidelines

- **Migrations**: All schema changes via migrations
- **Naming**: snake_case for tables and columns
- **Indexes**: Index foreign keys and frequently queried columns

---

## Test Organization

### Test Structure

```
tests/
├── unit/                 # ユニットテスト（107テスト）
│   ├── test_entities.py      # エンティティテスト
│   ├── test_errors.py        # エラーテスト
│   ├── test_value_objects.py # 値オブジェクトテスト
│   ├── test_embedding_adapter.py  # 埋め込みアダプターテスト
│   └── test_chromadb_adapter.py   # ChromaDBテスト
├── integration/          # 統合テスト（253テスト）
│   ├── test_mcp_server.py    # MCPサーバーテスト
│   ├── test_mcp_tools.py     # MCPツールテスト
│   ├── test_theory_repository.py  # リポジトリテスト
│   ├── test_methodology_tools.py  # 教授法ツールテスト
│   └── test_citation_tools.py     # 引用ツールテスト
├── e2e/                  # E2Eテスト
└── conftest.py           # pytest fixtures
```

### Test Guidelines

- **Test-First**: Tests written BEFORE implementation (Article III)
- **Real Services**: Integration tests use real DB/cache (Article IX)
- **Coverage**: 96% カバレッジ達成（目標: 80%以上）
- **Test Count**: 391 テスト（unit: 138, integration: 253）
- **Naming**: `test_*.py` for Python tests

---

## Documentation Organization

### Documentation Structure

```
docs/
├── architecture/         # Architecture documentation
│   ├── c4-diagrams/
│   └── adr/              # Architecture Decision Records
├── api/                  # API documentation
│   ├── openapi.yaml
│   └── graphql.schema
├── guides/               # Developer guides
│   ├── getting-started.md
│   └── contributing.md
└── runbooks/             # Operational runbooks
    ├── deployment.md
    └── troubleshooting.md
```

---

## SDD Artifacts Organization

### Storage Directory

```
storage/
├── specs/                # Specifications
│   ├── auth-requirements.md
│   ├── auth-design.md
│   ├── auth-tasks.md
│   └── payment-requirements.md
├── changes/              # Delta specifications (brownfield)
│   ├── add-2fa.md
│   └── upgrade-jwt.md
├── features/             # Feature tracking
│   ├── auth.json
│   └── payment.json
└── validation/           # Validation reports
    ├── auth-validation-report.md
    └── payment-validation-report.md
```

---

## Naming Conventions

### File Naming

- **TypeScript**: `PascalCase.tsx` for components, `camelCase.ts` for utilities
- **React Components**: `PascalCase.tsx` (e.g., `LoginForm.tsx`)
- **Utilities**: `camelCase.ts` (e.g., `formatDate.ts`)
- **Tests**: `*.test.ts` or `*.spec.ts`
- **Constants**: `SCREAMING_SNAKE_CASE.ts` (e.g., `API_ENDPOINTS.ts`)

### Directory Naming

- **Features**: `kebab-case` (e.g., `user-management/`)
- **Components**: `kebab-case` or `PascalCase` (consistent within project)

### Variable Naming

- **Variables**: `camelCase`
- **Constants**: `SCREAMING_SNAKE_CASE`
- **Types/Interfaces**: `PascalCase`
- **Enums**: `PascalCase`

---

## Integration Patterns

### Library → Application Integration

```typescript
// ✅ CORRECT: Application imports from library
import { AuthService } from '@/lib/auth';

const authService = new AuthService(repository);
const result = await authService.login(credentials);
```

```typescript
// ❌ WRONG: Library imports from application
// Libraries must NOT depend on application code
import { AuthContext } from '@/app/contexts/auth'; // Violation!
```

### Service → Repository Pattern

```typescript
// Service layer (business logic)
export class AuthService {
  constructor(private repository: UserRepository) {}

  async login(credentials: LoginRequest): Promise<LoginResponse> {
    // Business logic here
    const user = await this.repository.findByEmail(credentials.email);
    // ...
  }
}

// Repository layer (data access)
export class UserRepository {
  constructor(private prisma: PrismaClient) {}

  async findByEmail(email: string): Promise<User | null> {
    return this.prisma.user.findUnique({ where: { email } });
  }
}
```

---

## Deployment Structure

### Deployment Units

**Projects** (independently deployable):

1. TENGIN-GraphRAG - Main application

> ⚠️ **Simplicity Gate (Article VII)**: Maximum 3 projects initially.
> If adding more projects, document justification in Phase -1 Gate approval.

### Environment Structure

```
environments/
├── development/
│   └── .env.development
├── staging/
│   └── .env.staging
└── production/
    └── .env.production
```

---

## Multi-Language Support

### Language Policy

- **Primary Language**: English
- **Documentation**: English first (`.md`), then Japanese (`.ja.md`)
- **Code Comments**: English
- **UI Strings**: i18n framework

### i18n Organization

```
locales/
├── en/
│   ├── common.json
│   └── auth.json
└── ja/
    ├── common.json
    └── auth.json
```

---

## Version Control

### Branch Organization

- `main` - Production branch
- `develop` - Development branch
- `feature/*` - Feature branches
- `hotfix/*` - Hotfix branches
- `release/*` - Release branches

### Commit Message Convention

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

**Example**:

```
feat(auth): implement user login (REQ-AUTH-001)

Add login functionality with email and password authentication.
Session created with 24-hour expiry.

Closes REQ-AUTH-001
```

---

## Constitutional Compliance

This structure enforces:

- **Article I**: Library-first pattern in `lib/`
- **Article II**: CLI interfaces per library
- **Article III**: Test structure supports Test-First
- **Article VI**: Steering files maintain project memory

---

## Changelog

### Version 1.1 (Planned)

- [Future changes]

---

**Last Updated**: 2025-12-26
**Maintained By**: {{MAINTAINER}}
