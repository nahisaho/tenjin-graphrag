"""
ツールの単体テスト

citation_tools, theory_tools のヘルパー関数をテスト
"""

import pytest

# Citation tools helper functions
from tengin_mcp.tools.citation_tools import (
    _generate_apa7_citation,
    _generate_mla9_citation,
    _generate_chicago_citation,
    _generate_harvard_citation,
    _generate_ieee_citation,
)


class TestCitationHelpers:
    """引用生成ヘルパー関数のテスト"""

    def setup_method(self):
        """テスト用データのセットアップ"""
        self.theory_with_year = {
            "name": "認知負荷理論",
            "year_introduced": 1988,
        }
        self.theory_without_year = {
            "name": "構成主義",
        }
        self.theorist = {
            "name": "ジョン・スウェラー",
        }

    def test_apa7_citation_with_theorist(self):
        """APA7形式 - 理論家あり"""
        result = _generate_apa7_citation(self.theory_with_year, self.theorist)
        assert "ジョン・スウェラー" in result
        assert "1988" in result
        assert "認知負荷理論" in result
        assert result == "ジョン・スウェラー (1988). 認知負荷理論."

    def test_apa7_citation_without_theorist(self):
        """APA7形式 - 理論家なし"""
        result = _generate_apa7_citation(self.theory_with_year, None)
        assert "Unknown" in result
        assert "1988" in result

    def test_apa7_citation_without_year(self):
        """APA7形式 - 年なし"""
        result = _generate_apa7_citation(self.theory_without_year, self.theorist)
        assert "n.d." in result

    def test_mla9_citation_with_theorist(self):
        """MLA9形式 - 理論家あり"""
        result = _generate_mla9_citation(self.theory_with_year, self.theorist)
        assert "ジョン・スウェラー" in result
        assert '"認知負荷理論."' in result
        assert "1988" in result

    def test_mla9_citation_without_theorist(self):
        """MLA9形式 - 理論家なし"""
        result = _generate_mla9_citation(self.theory_with_year, None)
        assert "Unknown" in result

    def test_chicago_citation_with_theorist(self):
        """Chicago形式 - 理論家あり"""
        result = _generate_chicago_citation(self.theory_with_year, self.theorist)
        assert "ジョン・スウェラー" in result
        assert '"認知負荷理論,"' in result
        assert "1988" in result

    def test_chicago_citation_without_theorist(self):
        """Chicago形式 - 理論家なし"""
        result = _generate_chicago_citation(self.theory_with_year, None)
        assert "Unknown" in result

    def test_harvard_citation_with_theorist(self):
        """Harvard形式 - 理論家あり"""
        result = _generate_harvard_citation(self.theory_with_year, self.theorist)
        assert "ジョン・スウェラー" in result
        assert "(1988)" in result
        assert "認知負荷理論" in result

    def test_harvard_citation_without_theorist(self):
        """Harvard形式 - 理論家なし"""
        result = _generate_harvard_citation(self.theory_with_year, None)
        assert "Unknown" in result

    def test_ieee_citation_with_theorist(self):
        """IEEE形式 - 理論家あり"""
        result = _generate_ieee_citation(self.theory_with_year, self.theorist)
        assert "ジョン・スウェラー" in result
        assert '"認知負荷理論,"' in result
        assert "1988" in result

    def test_ieee_citation_without_theorist(self):
        """IEEE形式 - 理論家なし"""
        result = _generate_ieee_citation(self.theory_with_year, None)
        assert "Unknown" in result

    def test_all_formats_produce_string(self):
        """全形式が文字列を生成することを確認"""
        generators = [
            _generate_apa7_citation,
            _generate_mla9_citation,
            _generate_chicago_citation,
            _generate_harvard_citation,
            _generate_ieee_citation,
        ]
        
        for generator in generators:
            result = generator(self.theory_with_year, self.theorist)
            assert isinstance(result, str)
            assert len(result) > 0


class TestCitationFormatValidation:
    """引用形式の検証テスト"""

    def test_all_citation_formats_available(self):
        """すべての引用形式が利用可能"""
        from tengin_mcp.domain.value_objects import CitationFormat
        
        expected_formats = ["APA7", "MLA9", "Chicago", "Harvard", "IEEE"]
        for fmt in expected_formats:
            assert CitationFormat(fmt) is not None

    def test_invalid_citation_format_raises_error(self):
        """無効な引用形式はエラー"""
        from tengin_mcp.domain.value_objects import CitationFormat
        
        with pytest.raises(ValueError):
            CitationFormat("INVALID_FORMAT")
