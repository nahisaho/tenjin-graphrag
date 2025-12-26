"""
プロンプトの単体テスト

education_prompts モジュールのテスト
"""

import pytest

from tengin_mcp.prompts.education_prompts import (
    design_lesson,
    create_assessment,
    explain_theory,
    apply_theory,
    curriculum_plan,
    troubleshoot_learning,
)


class TestDesignLessonPrompt:
    """授業設計プロンプトのテスト"""

    @pytest.mark.asyncio
    async def test_basic_prompt_generation(self):
        """基本的なプロンプト生成"""
        result = await design_lesson(topic="光合成")
        
        assert isinstance(result, str)
        assert "光合成" in result
        assert "高校生" in result  # default level
        assert "50分" in result  # default duration

    @pytest.mark.asyncio
    async def test_custom_level(self):
        """カスタムレベルでのプロンプト生成"""
        result = await design_lesson(
            topic="分数の足し算",
            target_level="elementary",
        )
        
        assert "小学生" in result
        assert "分数の足し算" in result

    @pytest.mark.asyncio
    async def test_custom_duration(self):
        """カスタム時間でのプロンプト生成"""
        result = await design_lesson(
            topic="英文法",
            duration_minutes=90,
        )
        
        assert "90分" in result

    @pytest.mark.asyncio
    async def test_all_levels(self):
        """すべての対象レベルをテスト"""
        levels = ["elementary", "middle_school", "high_school", "university", "adult"]
        expected = ["小学生", "中学生", "高校生", "大学生", "成人学習者"]
        
        for level, expected_text in zip(levels, expected):
            result = await design_lesson(topic="テスト", target_level=level)
            assert expected_text in result

    @pytest.mark.asyncio
    async def test_includes_tool_references(self):
        """ツール参照が含まれていることを確認"""
        result = await design_lesson(topic="数学")
        
        assert "search_theories" in result
        assert "get_theory" in result


class TestCreateAssessmentPrompt:
    """評価設計プロンプトのテスト"""

    @pytest.mark.asyncio
    async def test_basic_assessment(self):
        """基本的な評価プロンプト生成"""
        result = await create_assessment(
            learning_objectives="二次方程式を解くことができる"
        )
        
        assert isinstance(result, str)
        assert "二次方程式" in result
        assert "形成的評価" in result  # default type

    @pytest.mark.asyncio
    async def test_summative_assessment(self):
        """総括的評価のプロンプト生成"""
        result = await create_assessment(
            learning_objectives="歴史的事象を分析できる",
            assessment_type="summative",
        )
        
        assert "総括的評価" in result

    @pytest.mark.asyncio
    async def test_diagnostic_assessment(self):
        """診断的評価のプロンプト生成"""
        result = await create_assessment(
            learning_objectives="基礎的な計算ができる",
            assessment_type="diagnostic",
        )
        
        assert "診断的評価" in result

    @pytest.mark.asyncio
    async def test_includes_rubric_reference(self):
        """ルーブリックへの言及を確認"""
        result = await create_assessment(
            learning_objectives="レポートを書ける"
        )
        
        assert "ルーブリック" in result


class TestExplainTheoryPrompt:
    """理論説明プロンプトのテスト"""

    @pytest.mark.asyncio
    async def test_basic_explanation(self):
        """基本的な理論説明プロンプト生成"""
        result = await explain_theory(theory_name="認知負荷理論")
        
        assert isinstance(result, str)
        assert "認知負荷理論" in result
        assert "教育者" in result  # default audience

    @pytest.mark.asyncio
    async def test_student_audience(self):
        """学生向けプロンプト生成"""
        result = await explain_theory(
            theory_name="構成主義",
            target_audience="student",
        )
        
        assert "学生" in result
        assert "構成主義" in result

    @pytest.mark.asyncio
    async def test_researcher_audience(self):
        """研究者向けプロンプト生成"""
        result = await explain_theory(
            theory_name="発達の最近接領域",
            target_audience="researcher",
        )
        
        assert "研究者" in result

    @pytest.mark.asyncio
    async def test_includes_tool_references(self):
        """ツール参照が含まれていることを確認"""
        result = await explain_theory(theory_name="テスト理論")
        
        assert "get_theory" in result
        assert "get_concept" in result
        assert "cite_theory" in result


class TestApplyTheoryPrompt:
    """理論適用プロンプトのテスト"""

    @pytest.mark.asyncio
    async def test_basic_application(self):
        """基本的な理論適用プロンプト生成"""
        result = await apply_theory(
            theory_name="認知負荷理論",
            context="オンライン授業のデザイン",
        )
        
        assert isinstance(result, str)
        assert "認知負荷理論" in result
        assert "オンライン授業" in result

    @pytest.mark.asyncio
    async def test_detailed_context(self):
        """詳細な文脈でのプロンプト生成"""
        result = await apply_theory(
            theory_name="足場かけ理論",
            context="小学3年生の算数で、掛け算が苦手な生徒を支援する",
        )
        
        assert "足場かけ理論" in result
        assert "小学3年生" in result

    @pytest.mark.asyncio
    async def test_includes_practical_sections(self):
        """実践的なセクションが含まれていることを確認"""
        result = await apply_theory(
            theory_name="テスト理論",
            context="テスト文脈",
        )
        
        assert "適用戦略" in result
        assert "評価指標" in result


class TestCurriculumPlanPrompt:
    """カリキュラム設計プロンプトのテスト"""

    @pytest.mark.asyncio
    async def test_basic_curriculum(self):
        """基本的なカリキュラムプロンプト生成"""
        result = await curriculum_plan(
            subject="数学",
            grade_level="中学1年",
        )
        
        assert isinstance(result, str)
        assert "数学" in result
        assert "中学1年" in result
        assert "12週間" in result  # default duration

    @pytest.mark.asyncio
    async def test_custom_duration(self):
        """カスタム期間でのプロンプト生成"""
        result = await curriculum_plan(
            subject="英語",
            grade_level="高校2年",
            duration_weeks=16,
        )
        
        assert "16週間" in result
        assert "英語" in result

    @pytest.mark.asyncio
    async def test_includes_curriculum_theories(self):
        """カリキュラム理論への言及を確認"""
        result = await curriculum_plan(
            subject="理科",
            grade_level="小学5年",
        )
        
        assert "タイラー" in result or "逆向き設計" in result or "スパイラル" in result


class TestTroubleshootLearningPrompt:
    """学習問題解決プロンプトのテスト"""

    @pytest.mark.asyncio
    async def test_basic_troubleshoot(self):
        """基本的な問題解決プロンプト生成"""
        result = await troubleshoot_learning(
            problem_description="生徒が授業中に集中できない"
        )
        
        assert isinstance(result, str)
        assert "集中できない" in result

    @pytest.mark.asyncio
    async def test_with_learner_context(self):
        """学習者背景ありでのプロンプト生成"""
        result = await troubleshoot_learning(
            problem_description="読解力が低い",
            learner_context="小学4年生、日本語が第二言語",
        )
        
        assert "読解力" in result
        assert "小学4年生" in result
        assert "第二言語" in result

    @pytest.mark.asyncio
    async def test_without_learner_context(self):
        """学習者背景なしでのプロンプト生成"""
        result = await troubleshoot_learning(
            problem_description="暗記が苦手"
        )
        
        assert "暗記が苦手" in result
        # 背景セクションがないことを確認（存在しないか空）
        # "学習者の背景" が出力に含まれないことを確認
        assert "## 学習者の背景" not in result or "## 学習者の背景\n\n##" not in result

    @pytest.mark.asyncio
    async def test_includes_search_tools(self):
        """検索ツールへの言及を確認"""
        result = await troubleshoot_learning(
            problem_description="テスト問題"
        )
        
        assert "search_theories" in result
