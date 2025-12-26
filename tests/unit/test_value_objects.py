"""Tests for domain value objects."""

import pytest
from tengin_mcp.domain.value_objects import (
    TheoryCategory,
    EvidenceLevel,
    CitationFormat,
)


class TestTheoryCategory:
    """TheoryCategory enum tests."""

    def test_all_categories(self):
        """Test all theory categories exist."""
        categories = [
            TheoryCategory.LEARNING,
            TheoryCategory.INSTRUCTIONAL,
            TheoryCategory.DEVELOPMENTAL,
            TheoryCategory.MOTIVATION,
            TheoryCategory.EDTECH,
            TheoryCategory.ADULT_LEARNING,
            TheoryCategory.INTELLIGENCE,
        ]
        assert len(categories) == 7

    def test_category_values(self):
        """Test category string values."""
        assert TheoryCategory.LEARNING.value == "learning"
        assert TheoryCategory.INSTRUCTIONAL.value == "instructional"
        assert TheoryCategory.DEVELOPMENTAL.value == "developmental"
        assert TheoryCategory.MOTIVATION.value == "motivation"
        assert TheoryCategory.EDTECH.value == "edtech"
        assert TheoryCategory.ADULT_LEARNING.value == "adult_learning"
        assert TheoryCategory.INTELLIGENCE.value == "intelligence"

    def test_category_from_string(self):
        """Test creating category from string."""
        category = TheoryCategory("learning")
        assert category == TheoryCategory.LEARNING

    def test_category_str(self):
        """Test category __str__ method."""
        assert str(TheoryCategory.LEARNING) == "learning"
        assert str(TheoryCategory.EDTECH) == "edtech"

    def test_from_string_valid(self):
        """Test from_string with valid values."""
        assert TheoryCategory.from_string("learning") == TheoryCategory.LEARNING
        assert TheoryCategory.from_string("LEARNING") == TheoryCategory.LEARNING
        assert TheoryCategory.from_string("Learning") == TheoryCategory.LEARNING

    def test_from_string_invalid(self):
        """Test from_string with invalid value raises ValueError."""
        with pytest.raises(ValueError, match="Invalid category"):
            TheoryCategory.from_string("invalid_category")


class TestEvidenceLevel:
    """EvidenceLevel enum tests."""

    def test_all_levels(self):
        """Test all evidence levels exist."""
        levels = [
            EvidenceLevel.STRONG,
            EvidenceLevel.MODERATE,
            EvidenceLevel.LIMITED,
            EvidenceLevel.THEORETICAL,
            EvidenceLevel.EMERGING,
        ]
        assert len(levels) == 5

    def test_level_values(self):
        """Test level string values."""
        assert EvidenceLevel.STRONG.value == "strong"
        assert EvidenceLevel.MODERATE.value == "moderate"
        assert EvidenceLevel.LIMITED.value == "limited"
        assert EvidenceLevel.THEORETICAL.value == "theoretical"
        assert EvidenceLevel.EMERGING.value == "emerging"

    def test_level_str(self):
        """Test level __str__ method."""
        assert str(EvidenceLevel.STRONG) == "strong"
        assert str(EvidenceLevel.EMERGING) == "emerging"

    def test_strength_order(self):
        """Test strength_order property."""
        assert EvidenceLevel.STRONG.strength_order == 5
        assert EvidenceLevel.MODERATE.strength_order == 4
        assert EvidenceLevel.LIMITED.strength_order == 3
        assert EvidenceLevel.THEORETICAL.strength_order == 2
        assert EvidenceLevel.EMERGING.strength_order == 1

    def test_comparison_lt(self):
        """Test less than comparison."""
        assert EvidenceLevel.EMERGING < EvidenceLevel.STRONG
        assert EvidenceLevel.LIMITED < EvidenceLevel.MODERATE
        assert not EvidenceLevel.STRONG < EvidenceLevel.EMERGING

    def test_comparison_le(self):
        """Test less than or equal comparison."""
        assert EvidenceLevel.EMERGING <= EvidenceLevel.STRONG
        assert EvidenceLevel.STRONG <= EvidenceLevel.STRONG
        assert not EvidenceLevel.STRONG <= EvidenceLevel.EMERGING


class TestCitationFormat:
    """CitationFormat enum tests."""

    def test_all_formats(self):
        """Test all citation formats exist."""
        formats = [
            CitationFormat.APA7,
            CitationFormat.MLA9,
            CitationFormat.CHICAGO,
            CitationFormat.HARVARD,
            CitationFormat.IEEE,
        ]
        assert len(formats) == 5

    def test_format_values(self):
        """Test format string values."""
        assert CitationFormat.APA7.value == "APA7"
        assert CitationFormat.MLA9.value == "MLA9"
        assert CitationFormat.CHICAGO.value == "Chicago"
        assert CitationFormat.HARVARD.value == "Harvard"
        assert CitationFormat.IEEE.value == "IEEE"
