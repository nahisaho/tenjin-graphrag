"""MCP Prompts: Educational content generation prompts."""

from tengin_mcp.server import mcp


@mcp.prompt()
async def design_lesson(
    topic: str,
    target_level: str = "high_school",
    duration_minutes: int = 50,
) -> str:
    """
    教育理論に基づいた授業設計を支援するプロンプトを生成します。

    Args:
        topic: 授業のトピック
        target_level: 対象レベル（elementary, middle_school, high_school, university, adult）
        duration_minutes: 授業時間（分）

    Returns:
        授業設計のためのプロンプト
    """
    level_descriptions = {
        "elementary": "小学生",
        "middle_school": "中学生",
        "high_school": "高校生",
        "university": "大学生",
        "adult": "成人学習者",
    }

    level_desc = level_descriptions.get(target_level, target_level)

    return f"""あなたは教育理論の専門家です。以下の条件で授業を設計してください。

## 授業設計の条件
- **トピック:** {topic}
- **対象:** {level_desc}
- **時間:** {duration_minutes}分

## 設計に活用すべき教育理論
以下のツールを使用して、関連する教育理論を検索・参照してください：
- `search_theories`: トピックに関連する理論を検索
- `get_theory`: 理論の詳細情報を取得
- `get_principles`: 理論の実践原則を取得

## 出力形式
1. **学習目標** - 具体的で測定可能な目標（ブルームの分類法に基づく）
2. **理論的基盤** - 使用する教育理論とその適用理由
3. **授業展開**
   - 導入（フック、前提知識の活性化）
   - 展開（主要な学習活動）
   - まとめ（振り返り、評価）
4. **評価方法** - 学習目標の達成度を測る方法
5. **差別化戦略** - 多様な学習者への対応

理論に基づいた根拠を必ず含めてください。"""


@mcp.prompt()
async def create_assessment(
    learning_objectives: str,
    assessment_type: str = "formative",
) -> str:
    """
    教育理論に基づいた評価設計を支援するプロンプトを生成します。

    Args:
        learning_objectives: 評価対象の学習目標
        assessment_type: 評価タイプ（formative, summative, diagnostic）

    Returns:
        評価設計のためのプロンプト
    """
    type_descriptions = {
        "formative": "形成的評価（学習過程での評価）",
        "summative": "総括的評価（学習終了時の評価）",
        "diagnostic": "診断的評価（学習前の前提知識確認）",
    }

    type_desc = type_descriptions.get(assessment_type, assessment_type)

    return f"""あなたは教育評価の専門家です。以下の条件で評価を設計してください。

## 評価設計の条件
- **学習目標:** {learning_objectives}
- **評価タイプ:** {type_desc}

## 設計に活用すべき教育理論
以下のツールを使用して、評価に関連する教育理論を参照してください：
- `search_theories`: "assessment" または "evaluation" で検索
- `get_theory`: 理論の詳細情報を取得
- `get_evidence`: エビデンスに基づく評価手法を確認

## 考慮すべき理論
- ブルームの分類法（認知領域のレベル）
- 構成主義的評価
- 真正な評価（Authentic Assessment）
- ルーブリック設計

## 出力形式
1. **評価の目的と範囲**
2. **評価基準（ルーブリック）**
3. **具体的な評価課題・問題**
4. **採点ガイドライン**
5. **フィードバック方針**

理論に基づいた根拠を必ず含めてください。"""


@mcp.prompt()
async def explain_theory(
    theory_name: str,
    target_audience: str = "educator",
) -> str:
    """
    教育理論の説明を生成するためのプロンプトを提供します。

    Args:
        theory_name: 説明する理論の名前
        target_audience: 対象読者（educator, student, parent, researcher）

    Returns:
        理論説明のためのプロンプト
    """
    audience_descriptions = {
        "educator": "教育者（教師、講師）",
        "student": "学生（教育学専攻）",
        "parent": "保護者",
        "researcher": "研究者",
    }

    audience_desc = audience_descriptions.get(target_audience, target_audience)

    return f"""あなたは教育理論の解説者です。以下の理論を分かりやすく説明してください。

## 説明する理論
**{theory_name}**

## 対象読者
{audience_desc}

## 情報収集
以下のツールを使用して、理論の詳細情報を取得してください：
- `search_theories`: "{theory_name}" で検索して理論IDを特定
- `get_theory`: 理論の詳細情報を取得
- `get_concept`: 関連概念を取得
- `get_theorist`: 提唱者の情報を取得
- `get_evidence`: 裏付けるエビデンスを取得
- `traverse_graph`: 関連する理論や概念を探索

## 出力形式
1. **概要** - 理論の核心を1-2文で
2. **背景** - 理論が生まれた歴史的・学術的背景
3. **主要概念** - 理論を構成する重要な概念
4. **原則** - 実践につながる原則
5. **具体例** - 教育現場での適用例
6. **限界と批判** - 理論の限界点
7. **関連理論** - 類似・対立する理論
8. **参考文献** - 引用（cite_theoryツールを使用）

対象読者に合わせた語彙と深さで説明してください。"""


@mcp.prompt()
async def apply_theory(
    theory_name: str,
    context: str,
) -> str:
    """
    教育理論を特定の文脈に適用するためのプロンプトを生成します。

    Args:
        theory_name: 適用する理論の名前
        context: 適用する文脈・状況の説明

    Returns:
        理論適用のためのプロンプト
    """
    return f"""あなたは教育理論の実践専門家です。以下の理論を特定の文脈に適用してください。

## 適用する理論
**{theory_name}**

## 適用文脈
{context}

## 情報収集
以下のツールを使用して情報を収集してください：
- `search_theories`: "{theory_name}" で検索
- `get_theory`: 理論の詳細を取得
- `get_principles`: 実践原則を取得
- `get_evidence`: 類似文脈でのエビデンスを確認

## 出力形式
1. **理論の要約** - 適用に関連する理論の側面
2. **文脈の分析** - 適用文脈の特性と課題
3. **適用戦略** - 具体的な実践方法
4. **予想される効果** - 理論適用による期待される成果
5. **注意点** - 適用時の留意事項
6. **評価指標** - 成功を測る指標

理論とエビデンスに基づいた実践的な提案を行ってください。"""


@mcp.prompt()
async def curriculum_plan(
    subject: str,
    grade_level: str,
    duration_weeks: int = 12,
) -> str:
    """
    教育理論に基づいたカリキュラム設計を支援するプロンプトを生成します。

    Args:
        subject: 教科・科目
        grade_level: 学年レベル
        duration_weeks: カリキュラム期間（週）

    Returns:
        カリキュラム設計のためのプロンプト
    """
    return f"""あなたはカリキュラム設計の専門家です。以下の条件でカリキュラムを設計してください。

## カリキュラム設計の条件
- **教科:** {subject}
- **学年:** {grade_level}
- **期間:** {duration_weeks}週間

## 設計に活用すべき教育理論
以下のツールを使用して、関連する教育理論を検索・参照してください：
- `search_theories`: "curriculum" "instructional design" で検索
- `get_theories_by_category`: "instructional" カテゴリの理論を取得
- `get_principles`: カリキュラム設計の原則を取得

## 考慮すべき理論的枠組み
- タイラーのカリキュラムモデル
- 逆向き設計（UbD）
- スパイラルカリキュラム（ブルーナー）
- 構成主義的カリキュラム設計

## 出力形式
1. **カリキュラム目標** - 全体の到達目標
2. **理論的基盤** - 採用するカリキュラム理論
3. **スコープとシーケンス** - 内容の範囲と順序
4. **週別計画** - 各週の学習内容と活動
5. **評価計画** - 形成的・総括的評価の配置
6. **リソースと教材** - 必要な教材・資源
7. **差別化と支援** - 多様な学習者への対応

理論に基づいた根拠を各セクションに含めてください。"""


@mcp.prompt()
async def troubleshoot_learning(
    problem_description: str,
    learner_context: str = "",
) -> str:
    """
    学習上の問題を教育理論に基づいて分析・解決するプロンプトを生成します。

    Args:
        problem_description: 学習上の問題の説明
        learner_context: 学習者の背景情報（オプション）

    Returns:
        問題解決のためのプロンプト
    """
    context_section = f"\n## 学習者の背景\n{learner_context}" if learner_context else ""

    return f"""あなたは学習支援の専門家です。以下の学習上の問題を分析し、解決策を提案してください。

## 問題の説明
{problem_description}
{context_section}

## 分析に活用すべき教育理論
以下のツールを使用して、関連する教育理論を検索・参照してください：
- `search_theories`: 問題に関連するキーワードで検索
- `get_theory`: 理論の詳細情報を取得
- `get_evidence`: 介入の効果に関するエビデンスを確認

## 考慮すべき理論的視点
- 動機づけ理論（内発的動機づけ、自己効力感）
- 認知負荷理論
- 足場かけ（スキャフォールディング）
- 多重知能理論
- 学習スタイル理論

## 出力形式
1. **問題の分析** - 理論的観点からの問題の特定
2. **考えられる原因** - 複数の可能性を理論に基づいて列挙
3. **推奨される介入** - 理論に基づいた具体的な対策
4. **実施手順** - 介入の実施方法
5. **効果測定** - 改善を確認する方法
6. **フォローアップ** - 継続的な支援計画

エビデンスに基づいた実践的な提案を行ってください。"""
