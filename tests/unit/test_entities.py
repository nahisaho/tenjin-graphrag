"""Tests for domain entities."""

import pytest
from tengin_mcp.domain.entities import (
    Theory,
    TheorySummary,
    Theorist,
    TheoristSummary,
    Concept,
    ConceptSummary,
    Principle,
    PrincipleSummary,
    Evidence,
    EvidenceSummary,
)
from tengin_mcp.domain.value_objects import TheoryCategory, EvidenceLevel


class TestTheory:
    """Theory entity tests."""

    def test_create_theory(self):
        """Test creating a Theory instance."""
        theory = Theory(
            id="theory-001",
            name="構成主義",
            name_en="Constructivism",
            description="知識の能動的構築を重視する学習理論。",
            category=TheoryCategory.LEARNING,
            year=1966,
            evidence_level=EvidenceLevel.STRONG,
            keywords=["active learning", "knowledge construction"],
            summary="学習者が能動的に知識を構築するという考え方。",
        )

        assert theory.id == "theory-001"
        assert theory.name == "構成主義"
        assert theory.name_en == "Constructivism"
        assert theory.category == TheoryCategory.LEARNING
        assert theory.year == 1966
        assert len(theory.keywords) == 2

    def test_theory_optional_fields(self):
        """Test Theory with minimal fields."""
        theory = Theory(
            id="theory-002",
            name="行動主義",
            name_en="Behaviorism",
            description="観察可能な行動に焦点を当てた理論。",
            category=TheoryCategory.LEARNING,
        )

        assert theory.id == "theory-002"
        assert theory.year is None
        assert theory.keywords == []


class TestTheorySummary:
    """TheorySummary tests."""

    def test_create_summary(self):
        """Test creating a TheorySummary instance."""
        summary = TheorySummary(
            id="theory-001",
            name="構成主義",
            name_en="Constructivism",
            category=TheoryCategory.LEARNING,
        )

        assert summary.id == "theory-001"
        assert summary.category == TheoryCategory.LEARNING


class TestTheorist:
    """Theorist entity tests."""

    def test_create_theorist(self):
        """Test creating a Theorist instance."""
        theorist = Theorist(
            id="theorist-001",
            name="ジャン・ピアジェ",
            name_en="Jean Piaget",
            birth_year=1896,
            death_year=1980,
            nationality="スイス",
            biography="発達心理学者。",
        )

        assert theorist.id == "theorist-001"
        assert theorist.name == "ジャン・ピアジェ"
        assert theorist.birth_year == 1896


class TestConcept:
    """Concept entity tests."""

    def test_create_concept(self):
        """Test creating a Concept instance."""
        concept = Concept(
            id="concept-001",
            name="足場かけ",
            name_en="Scaffolding",
            definition="学習者に提供される一時的なサポート。",
            examples=["ヒントの提示", "段階的な課題"],
            related_theory_ids=["theory-001"],
        )

        assert concept.id == "concept-001"
        assert concept.name == "足場かけ"
        assert len(concept.related_theory_ids) == 1


class TestPrinciple:
    """Principle entity tests."""

    def test_create_principle(self):
        """Test creating a Principle instance."""
        principle = Principle(
            id="principle-001",
            name="発達の最近接領域",
            description="学習は現在の能力をわずかに超えた領域で最もよく起こる。",
            application_guide="適切な難易度の課題を提供する",
            examples=["足場かけの活用"],
            source_theory_id="theory-001",
        )

        assert principle.id == "principle-001"
        assert len(principle.examples) == 1


class TestEvidence:
    """Evidence entity tests."""

    def test_create_evidence(self):
        """Test creating an Evidence instance."""
        evidence = Evidence(
            id="evidence-001",
            title="Meta-analysis of Constructivist Learning",
            authors=["Smith, J.", "Jones, M."],
            year=2020,
            evidence_type="meta-analysis",
            sample_size=5000,
            findings="Constructivist approaches show positive effects.",
            doi="10.1234/example",
            supported_theory_ids=["theory-001"],
        )

        assert evidence.id == "evidence-001"
        assert evidence.evidence_type == "meta-analysis"
        assert len(evidence.authors) == 2
