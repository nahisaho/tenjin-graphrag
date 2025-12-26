"""Infrastructure: Neo4j Theory Repository."""

from typing import Any

from tengin_mcp.domain.entities import (
    Concept,
    Evidence,
    Principle,
    Theorist,
    Theory,
    TheorySummary,
)
from tengin_mcp.domain.errors import TheoryNotFoundError
from tengin_mcp.domain.value_objects import EvidenceLevel, TheoryCategory
from tengin_mcp.infrastructure.adapters.neo4j_adapter import Neo4jAdapter


class Neo4jTheoryRepository:
    """Neo4j を使用した TheoryRepository 実装。"""

    def __init__(self, adapter: Neo4jAdapter) -> None:
        """
        リポジトリを初期化。

        Args:
            adapter: Neo4j アダプター
        """
        self._adapter = adapter

    # --- Interface methods (TheoryRepository Protocol) ---

    async def get_by_id(self, theory_id: str) -> Theory | None:
        """IDで理論を取得（インターフェース実装）。"""
        try:
            return await self.get_theory_by_id(theory_id)
        except TheoryNotFoundError:
            return None

    async def get_all(self) -> list[TheorySummary]:
        """全理論の要約リストを取得。"""
        query = "MATCH (t:Theory) RETURN t ORDER BY t.name"
        results = await self._adapter.execute_query(query)
        return [
            TheorySummary(
                id=r["t"]["id"],
                name=r["t"]["name"],
                name_en=r["t"].get("name_en"),
                category=TheoryCategory(r["t"]["category"]),
            )
            for r in results
        ]

    async def get_by_category(self, category: TheoryCategory) -> list[TheorySummary]:
        """カテゴリで理論をフィルタリング（インターフェース実装）。"""
        return await self.get_theories_by_category(category)

    async def search(self, query: str, limit: int = 10) -> list[TheorySummary]:
        """キーワード検索（インターフェース実装）。"""
        return await self.search_theories(query, limit=limit)

    async def get_theorist(self, theory_id: str) -> Theorist | None:
        """理論の提唱者を取得。"""
        cypher = """
        MATCH (t:Theory {id: $theory_id})-[:PROPOSED_BY]->(th:Theorist)
        RETURN th
        LIMIT 1
        """
        results = await self._adapter.execute_query(cypher, {"theory_id": theory_id})
        if not results or results[0]["th"] is None:
            return None
        data = results[0]["th"]
        return Theorist(
            id=data["id"],
            name=data["name"],
            name_en=data.get("name_en", ""),
            birth_year=data.get("birth_year"),
            death_year=data.get("death_year"),
            nationality=data.get("nationality", ""),
            affiliation=data.get("affiliation", ""),
            biography=data.get("biography", ""),
            major_works=data.get("major_works", []),
        )

    async def get_concepts(self, theory_id: str) -> list[Concept]:
        """理論に含まれる概念を取得。"""
        cypher = """
        MATCH (t:Theory {id: $theory_id})-[:HAS_CONCEPT]->(c:Concept)
        RETURN c
        """
        results = await self._adapter.execute_query(cypher, {"theory_id": theory_id})
        return [
            Concept(
                id=r["c"]["id"],
                name=r["c"]["name"],
                name_en=r["c"].get("name_en", ""),
                definition=r["c"].get("definition", ""),
                examples=r["c"].get("examples", []),
                related_theory_ids=[theory_id],
            )
            for r in results
        ]

    async def get_principles(self, theory_id: str) -> list[Principle]:
        """理論から導出される原則を取得。"""
        cypher = """
        MATCH (t:Theory {id: $theory_id})-[:HAS_PRINCIPLE]->(p:Principle)
        RETURN p
        """
        results = await self._adapter.execute_query(cypher, {"theory_id": theory_id})
        return [
            Principle(
                id=r["p"]["id"],
                name=r["p"]["name"],
                description=r["p"].get("description", ""),
                application_guide=r["p"].get("application_guide", ""),
                examples=r["p"].get("examples", []),
                source_theory_id=theory_id,
            )
            for r in results
        ]

    async def get_evidence(self, theory_id: str) -> list[Evidence]:
        """理論を支持するエビデンスを取得。"""
        cypher = """
        MATCH (t:Theory {id: $theory_id})-[:SUPPORTED_BY]->(e:Evidence)
        RETURN e
        """
        results = await self._adapter.execute_query(cypher, {"theory_id": theory_id})
        return [
            Evidence(
                id=r["e"]["id"],
                title=r["e"]["title"],
                authors=r["e"].get("authors", []),
                year=r["e"].get("year"),
                study_type=r["e"].get("study_type"),
                sample_size=r["e"].get("sample_size"),
                findings=r["e"]["findings"],
                findings_ja=r["e"].get("findings_ja"),
                level=EvidenceLevel(r["e"]["level"]),
                doi=r["e"].get("doi"),
                theory_ids=[theory_id],
            )
            for r in results
        ]

    # --- Extended methods ---

    async def get_theory_by_id(self, theory_id: str) -> Theory:
        """IDで理論を取得。"""
        query = """
        MATCH (t:Theory {id: $theory_id})
        OPTIONAL MATCH (t)-[:PROPOSED_BY]->(th:Theorist)
        OPTIONAL MATCH (t)-[:HAS_CONCEPT]->(c:Concept)
        OPTIONAL MATCH (t)-[:HAS_PRINCIPLE]->(p:Principle)
        OPTIONAL MATCH (t)-[:SUPPORTED_BY]->(e:Evidence)
        RETURN t,
               collect(DISTINCT th) as theorists,
               collect(DISTINCT c) as concepts,
               collect(DISTINCT p) as principles,
               collect(DISTINCT e) as evidences
        """
        results = await self._adapter.execute_query(query, {"theory_id": theory_id})

        if not results or results[0]["t"] is None:
            raise TheoryNotFoundError(f"Theory not found: {theory_id}")

        record = results[0]
        theory_data = record["t"]

        return Theory(
            id=theory_data["id"],
            name=theory_data["name"],
            name_en=theory_data.get("name_en", ""),
            description=theory_data.get("description", ""),
            category=TheoryCategory(theory_data["category"]),
            year=theory_data.get("year"),
            evidence_level=EvidenceLevel(theory_data.get("evidence_level", "theoretical")),
            keywords=theory_data.get("keywords", []),
            summary=theory_data.get("core_principle", ""),
        )

    async def get_theory_summary(self, theory_id: str) -> TheorySummary:
        """IDで理論サマリを取得。"""
        query = """
        MATCH (t:Theory {id: $theory_id})
        RETURN t
        """
        results = await self._adapter.execute_query(query, {"theory_id": theory_id})

        if not results or results[0]["t"] is None:
            raise TheoryNotFoundError(f"Theory not found: {theory_id}")

        theory_data = results[0]["t"]

        return TheorySummary(
            id=theory_data["id"],
            name=theory_data["name"],
            name_en=theory_data.get("name_en"),
            category=TheoryCategory(theory_data["category"]),
        )

    async def search_theories(
        self,
        query: str,
        category: TheoryCategory | None = None,
        limit: int = 10,
    ) -> list[TheorySummary]:
        """理論を検索。"""
        cypher = """
        MATCH (t:Theory)
        WHERE t.name CONTAINS $query
           OR t.description CONTAINS $query
           OR coalesce(t.name_en, '') CONTAINS $query
           OR ANY(kw IN t.keywords WHERE kw CONTAINS $query)
        """
        params: dict[str, Any] = {"query": query, "limit": limit}

        if category:
            cypher += " AND t.category = $category"
            params["category"] = category.value

        cypher += " RETURN t LIMIT $limit"

        results = await self._adapter.execute_query(cypher, params)

        return [
            TheorySummary(
                id=r["t"]["id"],
                name=r["t"]["name"],
                name_en=r["t"].get("name_en"),
                category=TheoryCategory(r["t"]["category"]),
            )
            for r in results
        ]

    async def get_theories_by_category(
        self,
        category: TheoryCategory,
        limit: int = 10,
    ) -> list[TheorySummary]:
        """カテゴリで理論を取得。"""
        query = """
        MATCH (t:Theory {category: $category})
        RETURN t
        LIMIT $limit
        """
        results = await self._adapter.execute_query(
            query, {"category": category.value, "limit": limit}
        )

        return [
            TheorySummary(
                id=r["t"]["id"],
                name=r["t"]["name"],
                name_en=r["t"].get("name_en"),
                category=TheoryCategory(r["t"]["category"]),
            )
            for r in results
        ]

    async def get_theorist_by_id(self, theorist_id: str) -> Theorist:
        """IDで理論家を取得。"""
        query = """
        MATCH (th:Theorist {id: $theorist_id})
        OPTIONAL MATCH (th)<-[:PROPOSED_BY]-(t:Theory)
        RETURN th, collect(t.id) as theory_ids
        """
        results = await self._adapter.execute_query(query, {"theorist_id": theorist_id})

        if not results or results[0]["th"] is None:
            raise TheoryNotFoundError(f"Theorist not found: {theorist_id}")

        record = results[0]
        data = record["th"]

        return Theorist(
            id=data["id"],
            name=data["name"],
            name_en=data.get("name_en", ""),
            birth_year=data.get("birth_year"),
            death_year=data.get("death_year"),
            nationality=data.get("nationality", ""),
            affiliation=data.get("affiliation", ""),
            biography=data.get("biography", ""),
            major_works=data.get("major_works", []),
        )

    async def get_concept_by_id(self, concept_id: str) -> Concept:
        """IDで概念を取得。"""
        query = """
        MATCH (c:Concept {id: $concept_id})
        OPTIONAL MATCH (c)<-[:HAS_CONCEPT]-(t:Theory)
        OPTIONAL MATCH (c)-[:RELATED_TO]->(rc:Concept)
        RETURN c, collect(DISTINCT t.id) as theory_ids, collect(DISTINCT rc.id) as related_ids
        """
        results = await self._adapter.execute_query(query, {"concept_id": concept_id})

        if not results or results[0]["c"] is None:
            raise TheoryNotFoundError(f"Concept not found: {concept_id}")

        record = results[0]
        data = record["c"]

        return Concept(
            id=data["id"],
            name=data["name"],
            name_en=data.get("name_en", ""),
            definition=data.get("definition", ""),
            examples=data.get("examples", []),
            related_theory_ids=record["theory_ids"] or [],
        )

    async def get_principle_by_id(self, principle_id: str) -> Principle:
        """IDで原則を取得。"""
        query = """
        MATCH (p:Principle {id: $principle_id})
        OPTIONAL MATCH (p)<-[:HAS_PRINCIPLE]-(t:Theory)
        RETURN p, collect(t.id) as theory_ids
        """
        results = await self._adapter.execute_query(query, {"principle_id": principle_id})

        if not results or results[0]["p"] is None:
            raise TheoryNotFoundError(f"Principle not found: {principle_id}")

        record = results[0]
        data = record["p"]

        return Principle(
            id=data["id"],
            name=data["name"],
            description=data.get("description", ""),
            application_guide=data.get("application_guide", ""),
            examples=data.get("examples", []),
            source_theory_id=record["theory_ids"][0] if record["theory_ids"] else "",
        )

    async def get_evidence_by_id(self, evidence_id: str) -> Evidence:
        """IDでエビデンスを取得。"""
        query = """
        MATCH (e:Evidence {id: $evidence_id})
        OPTIONAL MATCH (e)<-[:SUPPORTED_BY]-(t:Theory)
        RETURN e, collect(t.id) as theory_ids
        """
        results = await self._adapter.execute_query(query, {"evidence_id": evidence_id})

        if not results or results[0]["e"] is None:
            raise TheoryNotFoundError(f"Evidence not found: {evidence_id}")

        record = results[0]
        data = record["e"]

        return Evidence(
            id=data["id"],
            title=data["title"],
            authors=data.get("authors", []),
            year=data.get("year", 0),
            source=data.get("source", ""),
            doi=data.get("doi"),
            evidence_type=data.get("evidence_type", data.get("study_type", "review")),
            methodology=data.get("methodology", ""),
            findings=data.get("findings", ""),
            sample_size=data.get("sample_size"),
            effect_size=str(data["effect_size"]) if data.get("effect_size") is not None else None,
            supported_theory_ids=record["theory_ids"] or [],
        )
