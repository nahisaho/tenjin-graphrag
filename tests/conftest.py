"""Pytest configuration."""

import pytest

from tengin_mcp.infrastructure.config import Settings
from tengin_mcp.infrastructure.adapters.neo4j_adapter import Neo4jAdapter
from tengin_mcp.infrastructure.repositories.neo4j_graph_repository import Neo4jGraphRepository
from tengin_mcp.server import app_state


@pytest.fixture
def sample_theory_data():
    """Sample theory data for testing."""
    return {
        "id": "theory-001",
        "name": "Constructivism",
        "name_ja": "構成主義",
        "description": "A learning theory emphasizing active construction of knowledge.",
        "description_ja": "知識の能動的構築を重視する学習理論。",
        "category": "learning",
        "year_introduced": 1966,
        "keywords": ["active learning", "knowledge construction"],
        "related_theory_ids": ["theory-002"],
    }


@pytest.fixture
def sample_theorist_data():
    """Sample theorist data for testing."""
    return {
        "id": "theorist-001",
        "name": "Jean Piaget",
        "name_ja": "ジャン・ピアジェ",
        "birth_year": 1896,
        "death_year": 1980,
        "nationality": "Swiss",
        "biography": "A developmental psychologist known for cognitive development theory.",
        "biography_ja": "認知発達理論で知られる発達心理学者。",
        "theory_ids": ["theory-001"],
    }


@pytest.fixture
def sample_concept_data():
    """Sample concept data for testing."""
    return {
        "id": "concept-001",
        "name": "Scaffolding",
        "name_ja": "足場かけ",
        "definition": "Temporary support provided to learners.",
        "definition_ja": "学習者に提供される一時的なサポート。",
        "theory_ids": ["theory-001"],
        "related_concept_ids": [],
    }


@pytest.fixture
async def initialized_app_state():
    """Initialize app_state with Neo4j connection for integration tests."""
    settings = Settings()
    neo4j_adapter = Neo4jAdapter(settings)
    await neo4j_adapter.connect()
    
    graph_repository = Neo4jGraphRepository(neo4j_adapter)
    app_state.graph_repository = graph_repository
    
    yield app_state
    
    # Cleanup
    await neo4j_adapter.close()
    app_state.graph_repository = None
