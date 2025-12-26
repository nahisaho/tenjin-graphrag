# Product Context

**Project**: TENGIN-GraphRAG
**Last Updated**: 2025-12-26
**Version**: 1.0
**Status**: 実装完了

---

## Product Vision

**Vision Statement**: 教育理論に基づいたエビデンスベースの教育コンテンツ生成を実現する

> 生成AIが教育コンテンツを生成する際、単なる経験則や一般的な知識ではなく、体系化された教育理論に基づいたコンテンツを生成できるようにすることで、より効果的で信頼性の高い教育体験を提供する。TENGIN-GraphRAGは、教育理論のナレッジグラフとGraphRAG技術を組み合わせ、LLMが理論的根拠を持った回答を生成できるようにするシステムである。

**Mission**: 教育理論のナレッジグラフを構築し、GraphRAGを通じてLLMに理論的文脈を提供する

> 行動主義、認知主義、構成主義などの主要な学習理論から、ガニェの9教授事象、ARCSモデルなどの教授設計理論まで、体系的にナレッジグラフ化し、クエリに応じて関連する理論・概念・エビデンスを検索・提供することで、生成AIの回答品質を向上させる。

---

## Product Overview

### What is TENGIN-GraphRAG?

教育理論に特化したGraphRAG（Graph-based Retrieval Augmented Generation）システム

> TENGIN-GraphRAGは、教育理論・学習理論のナレッジグラフデータベースとGraphRAG検索エンジンを提供するシステムです。生成AIが教育関連のコンテンツを生成する際、このシステムを通じて関連する教育理論、概念、エビデンスを取得し、理論に基づいた回答を生成できるようになります。
>
> 従来のRAGシステムでは、テキストの類似性に基づいた検索のみが行われていましたが、GraphRAGでは理論間の関係（「発展」「対立」「基盤」など）を活用した深い文脈理解が可能です。例えば、「効果的な授業設計」というクエリに対して、単にキーワードが一致するドキュメントを返すのではなく、ガニェの教授事象→認知主義→情報処理理論といった理論的系譜を辿り、包括的な理論的背景を提供できます。
>
> 主な特徴：
> - 38の教育理論（8つのMECEパラダイムに分類）
> - 27名の理論家、25の核心概念
> - 15の教授法、15のメタ分析エビデンス、10の教育文脈
> - 303のリレーションシップでナレッジグラフを構成
> - 理論間の関係（基盤、発展、対立、相補）をグラフで表現
> - エビデンスレベルの追跡と引用管理
> - MCP（Model Context Protocol）によるLLM統合

### Problem Statement

**Problem**: 生成AIによる教育コンテンツは理論的根拠が欠如している

> 現在の生成AIは膨大なテキストデータで学習されていますが、教育理論を体系的に理解しているわけではありません。そのため、教育コンテンツを生成する際に以下の問題が発生します：
> - 教育理論の誤った解釈や混同
> - エビデンスに基づかない経験則的なアドバイス
> - 理論的背景の説明なしに「効果的」と主張
> - 相反する理論を無批判に混在させた回答
> - 出典・引用の不在

### Solution

**Solution**: 教育理論のナレッジグラフを活用したGraphRAGシステム

> TENGIN-GraphRAGは以下のアプローチで問題を解決します：
> 1. **構造化された理論データベース**: 主要な教育理論を体系的に分類・格納
> 2. **関係性の明示**: 理論間の「基盤」「発展」「対立」関係をグラフで表現
> 3. **エビデンス追跡**: 各理論・原則に対するエビデンスレベルを管理
> 4. **GraphRAG検索**: 意味検索＋グラフトラバーサルで関連理論を網羅的に取得
> 5. **引用生成**: 使用した理論と出典を明示した回答を生成

---

## Target Users

### Primary Users

#### User Persona 1: AIプロダクト開発者

**Demographics**:

- **Role**: ソフトウェアエンジニア / MLエンジニア
- **Organization Size**: EdTech企業、AI企業
- **Technical Level**: 高い（API統合、システム設計経験あり）

**Goals**:

- 教育系AIプロダクトの回答品質向上
- LLMのハルシネーション抑制
- エビデンスベースのコンテンツ生成

**Pain Points**:

- LLMが教育理論を誤解釈する
- 出典・引用の自動生成が難しい
- 教育ドメイン知識の整備が困難

**Use Cases**:

- AI家庭教師サービスへのRAG統合
- 教育コンテンツ生成パイプラインへの組み込み
- 学習アドバイスボットの品質向上

---

#### User Persona 2: インストラクショナルデザイナー

**Demographics**:

- **Role**: 教育設計者 / e-Learning開発者
- **Organization Size**: 大学、企業研修部門、教育出版社
- **Technical Level**: 中程度（APIは使えるがコーディングは限定的）

**Goals**:

- 理論に基づいた教材設計
- 設計根拠の明示と説明
- 最新の教育研究の活用

**Pain Points**:

- 理論の適用方法がわからない
- 複数の理論の整合性確認が困難
- エビデンスの探索に時間がかかる

**Use Cases**:

- 教材設計時の理論参照
- 設計根拠文書の自動生成
- 理論間の関係理解

---

### Secondary Users

- **{{SECONDARY_USER_1}}**: [Description and role]
- **{{SECONDARY_USER_2}}**: [Description and role]

---

## Market & Business Context

### Market Opportunity

**Market Size**: {{MARKET_SIZE}}

**Target Market**: {{TARGET_MARKET}}

> [Description of the market opportunity, competitive landscape, and positioning]

### Business Model

**Revenue Model**: {{REVENUE_MODEL}}

> Examples: SaaS subscription, One-time purchase, Freemium, Usage-based

**Pricing Tiers** (if applicable):

- **Free Tier**: [Features, limitations]
- **Pro Tier**: ${{PRICE}}/month - [Features]
- **Enterprise Tier**: Custom pricing - [Features]

### Competitive Landscape

| Competitor       | Strengths   | Weaknesses   | Our Differentiation   |
| ---------------- | ----------- | ------------ | --------------------- |
| {{COMPETITOR_1}} | [Strengths] | [Weaknesses] | [How we're different] |
| {{COMPETITOR_2}} | [Strengths] | [Weaknesses] | [How we're different] |

---

## Core Product Capabilities

### Must-Have Features (MVP)

1. **{{FEATURE_1}}**
   - **Description**: [What it does]
   - **User Value**: [Why users need it]
   - **Priority**: P0 (Critical)

2. **{{FEATURE_2}}**
   - **Description**: [What it does]
   - **User Value**: [Why users need it]
   - **Priority**: P0 (Critical)

3. **{{FEATURE_3}}**
   - **Description**: [What it does]
   - **User Value**: [Why users need it]
   - **Priority**: P0 (Critical)

### High-Priority Features (Post-MVP)

4. **{{FEATURE_4}}**
   - **Description**: [What it does]
   - **User Value**: [Why users need it]
   - **Priority**: P1 (High)

5. **{{FEATURE_5}}**
   - **Description**: [What it does]
   - **User Value**: [Why users need it]
   - **Priority**: P1 (High)

### Future Features (Roadmap)

6. **{{FEATURE_6}}**
   - **Description**: [What it does]
   - **User Value**: [Why users need it]
   - **Priority**: P2 (Medium)

7. **{{FEATURE_7}}**
   - **Description**: [What it does]
   - **User Value**: [Why users need it]
   - **Priority**: P3 (Low)

---

## Product Principles

### Design Principles

1. **{{PRINCIPLE_1}}**
   - [Description of what this means for product decisions]

2. **{{PRINCIPLE_2}}**
   - [Description]

3. **{{PRINCIPLE_3}}**
   - [Description]

**Examples**:

- **Simplicity First**: Favor simple solutions over complex ones
- **User Empowerment**: Give users control and flexibility
- **Speed & Performance**: Fast response times (< 200ms)

### User Experience Principles

1. **{{UX_PRINCIPLE_1}}**
   - [How this guides UX decisions]

2. **{{UX_PRINCIPLE_2}}**
   - [How this guides UX decisions]

**Examples**:

- **Progressive Disclosure**: Show advanced features only when needed
- **Accessibility First**: WCAG 2.1 AA compliance
- **Mobile-First**: Design for mobile, enhance for desktop

---

## Success Metrics

### Key Performance Indicators (KPIs)

#### Business Metrics

| Metric                              | Target            | Measurement    |
| ----------------------------------- | ----------------- | -------------- |
| **Monthly Active Users (MAU)**      | {{MAU_TARGET}}    | [How measured] |
| **Monthly Recurring Revenue (MRR)** | ${{MRR_TARGET}}   | [How measured] |
| **Customer Acquisition Cost (CAC)** | ${{CAC_TARGET}}   | [How measured] |
| **Customer Lifetime Value (LTV)**   | ${{LTV_TARGET}}   | [How measured] |
| **Churn Rate**                      | < {{CHURN_RATE}}% | [How measured] |

#### Product Metrics

| Metric                       | Target                | Measurement    |
| ---------------------------- | --------------------- | -------------- |
| **Daily Active Users (DAU)** | {{DAU_TARGET}}        | [How measured] |
| **Feature Adoption Rate**    | > {{ADOPTION_RATE}}%  | [How measured] |
| **User Retention (Day 7)**   | > {{RETENTION_RATE}}% | [How measured] |
| **Net Promoter Score (NPS)** | > {{NPS_TARGET}}      | [How measured] |

#### Technical Metrics

| Metric                      | Target  | Measurement             |
| --------------------------- | ------- | ----------------------- |
| **API Response Time (p95)** | < 200ms | Monitoring dashboard    |
| **Uptime**                  | 99.9%   | Status page             |
| **Error Rate**              | < 0.1%  | Error tracking (Sentry) |
| **Page Load Time**          | < 2s    | Web vitals              |

---

## Product Roadmap

### Phase 1: MVP (Months 1-3)

**Goal**: Launch minimum viable product

**Features**:

- [Feature 1]
- [Feature 2]
- [Feature 3]

**Success Criteria**:

- [Criterion 1]
- [Criterion 2]

---

### Phase 2: Growth (Months 4-6)

**Goal**: Achieve product-market fit

**Features**:

- [Feature 4]
- [Feature 5]
- [Feature 6]

**Success Criteria**:

- [Criterion 1]
- [Criterion 2]

---

### Phase 3: Scale (Months 7-12)

**Goal**: Scale to {{USER_TARGET}} users

**Features**:

- [Feature 7]
- [Feature 8]
- [Feature 9]

**Success Criteria**:

- [Criterion 1]
- [Criterion 2]

---

## User Workflows

### Primary Workflow 1: {{WORKFLOW_1_NAME}}

**User Goal**: {{USER_GOAL}}

**Steps**:

1. User [action 1]
2. System [response 1]
3. User [action 2]
4. System [response 2]
5. User achieves [goal]

**Success Criteria**:

- User completes workflow in < {{TIME}} minutes
- Success rate > {{SUCCESS_RATE}}%

---

### Primary Workflow 2: {{WORKFLOW_2_NAME}}

**User Goal**: {{USER_GOAL}}

**Steps**:

1. [Step 1]
2. [Step 2]
3. [Step 3]

**Success Criteria**:

- [Criterion 1]
- [Criterion 2]

---

## Business Domain

### Domain Concepts

Key concepts and terminology used in this domain:

1. **{{CONCEPT_1}}**: [Definition and importance]
2. **{{CONCEPT_2}}**: [Definition and importance]
3. **{{CONCEPT_3}}**: [Definition and importance]

**Example for SaaS Authentication**:

- **Identity Provider (IdP)**: Service that authenticates users
- **Single Sign-On (SSO)**: One login for multiple applications
- **Multi-Factor Authentication (MFA)**: Additional verification step

### Business Rules

1. **{{RULE_1}}**
   - [Description of business rule]
   - **Example**: [Concrete example]

2. **{{RULE_2}}**
   - [Description]
   - **Example**: [Example]

**Example for E-commerce**:

- **Inventory Reservation**: Reserved items held for 10 minutes during checkout
- **Refund Window**: Refunds allowed within 30 days of purchase

---

## Constraints & Requirements

### Business Constraints

- **Budget**: ${{BUDGET}}
- **Timeline**: {{TIMELINE}}
- **Team Size**: {{TEAM_SIZE}} engineers
- **Launch Date**: {{LAUNCH_DATE}}

### Compliance Requirements

- **{{COMPLIANCE_1}}**: [Description, e.g., GDPR, SOC 2, HIPAA]
- **{{COMPLIANCE_2}}**: [Description]
- **Data Residency**: [Requirements, e.g., EU data stays in EU]

### Non-Functional Requirements

- **Performance**: API response < 200ms (95th percentile)
- **Availability**: 99.9% uptime SLA
- **Scalability**: Support {{CONCURRENT_USERS}} concurrent users
- **Security**: OWASP Top 10 compliance
- **Accessibility**: WCAG 2.1 AA compliance

---

## Stakeholders

### Internal Stakeholders

| Role                    | Name                 | Responsibilities                  |
| ----------------------- | -------------------- | --------------------------------- |
| **Product Owner**       | {{PO_NAME}}          | Vision, roadmap, priorities       |
| **Tech Lead**           | {{TECH_LEAD_NAME}}   | Architecture, technical decisions |
| **Engineering Manager** | {{EM_NAME}}          | Team management, delivery         |
| **QA Lead**             | {{QA_LEAD_NAME}}     | Quality assurance, testing        |
| **Design Lead**         | {{DESIGN_LEAD_NAME}} | UX/UI design                      |

### External Stakeholders

| Role                        | Name        | Responsibilities            |
| --------------------------- | ----------- | --------------------------- |
| **Customer Advisory Board** | [Members]   | Product feedback            |
| **Investors**               | [Names]     | Funding, strategic guidance |
| **Partners**                | [Companies] | Integration, co-marketing   |

---

## Go-to-Market Strategy

### Launch Strategy

**Target Launch Date**: {{LAUNCH_DATE}}

**Launch Phases**:

1. **Private Beta** ({{START_DATE}} - {{END_DATE}})
   - Invite-only, 50 beta users
   - Focus: Gather feedback, fix critical bugs

2. **Public Beta** ({{START_DATE}} - {{END_DATE}})
   - Open signup
   - Focus: Validate product-market fit

3. **General Availability** ({{LAUNCH_DATE}})
   - Full public launch
   - Focus: Acquisition and growth

### Marketing Channels

- **{{CHANNEL_1}}**: [Strategy, e.g., Content marketing, SEO]
- **{{CHANNEL_2}}**: [Strategy, e.g., Social media, Twitter/LinkedIn]
- **{{CHANNEL_3}}**: [Strategy, e.g., Paid ads, Google/Facebook]
- **{{CHANNEL_4}}**: [Strategy, e.g., Partnerships, integrations]

---

## Risk Assessment

### Product Risks

| Risk       | Probability     | Impact          | Mitigation            |
| ---------- | --------------- | --------------- | --------------------- |
| {{RISK_1}} | High/Medium/Low | High/Medium/Low | [Mitigation strategy] |
| {{RISK_2}} | High/Medium/Low | High/Medium/Low | [Mitigation strategy] |

**Example Risks**:

- **Low adoption**: Users don't understand value → Clear onboarding, demos
- **Performance issues**: System slow at scale → Load testing, optimization
- **Security breach**: Data compromised → Security audit, penetration testing

---

## Customer Support

### Support Channels

- **Email**: support@{{COMPANY}}.com
- **Chat**: In-app live chat (business hours)
- **Documentation**: docs.{{COMPANY}}.com
- **Community**: Forum/Discord/Slack

### Support SLA

| Tier              | Response Time | Resolution Time |
| ----------------- | ------------- | --------------- |
| **Critical (P0)** | < 1 hour      | < 4 hours       |
| **High (P1)**     | < 4 hours     | < 24 hours      |
| **Medium (P2)**   | < 24 hours    | < 3 days        |
| **Low (P3)**      | < 48 hours    | Best effort     |

---

## Product Analytics

### Analytics Tools

- **{{ANALYTICS_TOOL_1}}**: [Purpose, e.g., Google Analytics, Mixpanel]
- **{{ANALYTICS_TOOL_2}}**: [Purpose, e.g., Amplitude, Heap]

### Events to Track

| Event               | Description            | Purpose           |
| ------------------- | ---------------------- | ----------------- |
| `user_signup`       | New user registration  | Track acquisition |
| `feature_used`      | User uses core feature | Track engagement  |
| `payment_completed` | User completes payment | Track conversion  |
| `error_occurred`    | User encounters error  | Track reliability |

---

## Localization & Internationalization

### Supported Languages

- **Primary**: English (en-US)
- **Secondary**: [Languages, e.g., Japanese (ja-JP), Spanish (es-ES)]

### Localization Strategy

- **UI Strings**: i18n framework (next-intl, react-i18next)
- **Date/Time**: Locale-aware formatting
- **Currency**: Multi-currency support
- **Right-to-Left (RTL)**: Support for Arabic, Hebrew (if needed)

---

## Data & Privacy

### Data Collection

**What data we collect**:

- User account information (email, name)
- Usage analytics (anonymized)
- Error logs (for debugging)

**What data we DON'T collect**:

- [Sensitive data we avoid, e.g., passwords (only hashed), payment details (tokenized)]

### Privacy Policy

- **GDPR Compliance**: Right to access, delete, export data
- **Data Retention**: [Retention period, e.g., 90 days for logs]
- **Third-Party Sharing**: [Who we share data with, why]

---

## Integrations

### Existing Integrations

| Integration       | Purpose   | Priority |
| ----------------- | --------- | -------- |
| {{INTEGRATION_1}} | [Purpose] | P0       |
| {{INTEGRATION_2}} | [Purpose] | P1       |

### Planned Integrations

| Integration       | Purpose   | Timeline |
| ----------------- | --------- | -------- |
| {{INTEGRATION_3}} | [Purpose] | Q2 2025  |
| {{INTEGRATION_4}} | [Purpose] | Q3 2025  |

---

## Changelog

### Version 1.1 (Planned)

- [Future product updates]

---

**Last Updated**: 2025-12-25
**Maintained By**: {{MAINTAINER}}
