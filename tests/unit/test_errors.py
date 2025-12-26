"""Tests for domain errors."""

import pytest
from tengin_mcp.domain.errors import (
    TenginError,
    GraphRAGError,
    TheoryNotFoundError,
    ConceptNotFoundError,
    TheoristNotFoundError,
    InvalidQueryError,
    EntityNotFoundError,
    GraphTraversalError,
    DatabaseConnectionError,
)


class TestTenginError:
    """TenginError tests."""

    def test_base_error_with_defaults(self):
        """Test base error with default code."""
        error = TenginError("Test error")
        assert str(error) == "Test error"
        assert error.message == "Test error"
        assert error.code == "TENGIN_ERROR"
        assert isinstance(error, Exception)

    def test_base_error_with_custom_code(self):
        """Test base error with custom code."""
        error = TenginError("Custom error", code="CUSTOM_CODE")
        assert error.message == "Custom error"
        assert error.code == "CUSTOM_CODE"


class TestGraphRAGError:
    """GraphRAGError tests (alias for backward compatibility)."""

    def test_alias(self):
        """Test GraphRAGError is alias for TenginError."""
        assert GraphRAGError is TenginError

    def test_base_error(self):
        """Test base error creation."""
        error = GraphRAGError("Test error")
        assert str(error) == "Test error"
        assert isinstance(error, Exception)


class TestTheoryNotFoundError:
    """TheoryNotFoundError tests."""

    def test_not_found_error(self):
        """Test theory not found error."""
        error = TheoryNotFoundError("theory-001")
        assert "theory-001" in str(error)
        assert error.theory_id == "theory-001"
        assert error.code == "THEORY_NOT_FOUND"
        assert isinstance(error, TenginError)


class TestConceptNotFoundError:
    """ConceptNotFoundError tests."""

    def test_not_found_error(self):
        """Test concept not found error."""
        error = ConceptNotFoundError("concept-001")
        assert "concept-001" in str(error)
        assert error.concept_id == "concept-001"
        assert error.code == "CONCEPT_NOT_FOUND"
        assert isinstance(error, TenginError)


class TestTheoristNotFoundError:
    """TheoristNotFoundError tests."""

    def test_not_found_error(self):
        """Test theorist not found error."""
        error = TheoristNotFoundError("theorist-001")
        assert "theorist-001" in str(error)
        assert error.theorist_id == "theorist-001"
        assert error.code == "THEORIST_NOT_FOUND"
        assert isinstance(error, TenginError)


class TestInvalidQueryError:
    """InvalidQueryError tests."""

    def test_invalid_query_error(self):
        """Test invalid query error."""
        error = InvalidQueryError("Query too short")
        assert "Query too short" in str(error)
        assert error.code == "INVALID_QUERY"
        assert isinstance(error, TenginError)


class TestEntityNotFoundError:
    """EntityNotFoundError tests."""

    def test_entity_not_found(self):
        """Test generic entity not found error."""
        error = EntityNotFoundError("Evidence", "evidence-001")
        assert "Evidence not found: evidence-001" in str(error)
        assert error.entity_type == "Evidence"
        assert error.entity_id == "evidence-001"
        assert error.code == "EVIDENCE_NOT_FOUND"
        assert isinstance(error, TenginError)


class TestGraphTraversalError:
    """GraphTraversalError tests."""

    def test_traversal_error(self):
        """Test graph traversal error."""
        error = GraphTraversalError("Max depth exceeded")
        assert "Max depth exceeded" in str(error)
        assert error.code == "GRAPH_TRAVERSAL_ERROR"
        assert isinstance(error, TenginError)


class TestDatabaseConnectionError:
    """DatabaseConnectionError tests."""

    def test_connection_error(self):
        """Test database connection error."""
        error = DatabaseConnectionError("Failed to connect")
        assert "Failed to connect" in str(error)
        assert error.code == "DATABASE_CONNECTION_ERROR"
        assert isinstance(error, TenginError)
