"""
拡張された教育理論データをNeo4jに投入するスクリプト

MECE（Mutually Exclusive, Collectively Exhaustive）に基づいて
構成された包括的な教育理論GraphRAGデータを投入します。

使用方法:
    uv run python -m tengin_mcp.scripts.seed_extended_data

ノードタイプ:
    - Theory: 教育理論（35件）
    - Theorist: 理論家（28件）
    - Concept: 教育概念（25件）
    - Methodology: 教授法（15件）
    - Evidence: 研究エビデンス（15件）
    - Context: 適用文脈（10件）

エッジタイプ:
    - PROPOSED: 理論家が理論を提唱
    - DEVELOPED: 理論家が理論を発展
    - INFLUENCED: 影響関係
    - EXTENDS: 理論の拡張
    - CONTRADICTS: 理論間の対立
    - COMPLEMENTS: 相補的関係
    - INCLUDES_CONCEPT: 概念を含む
    - OPERATIONALIZES: 操作化
    - SUPPORTS: エビデンスが支持
    - CHALLENGES: エビデンスが挑戦
    - EFFECTIVE_FOR: 文脈での有効性
"""

import asyncio
import json
from pathlib import Path
from typing import Any

from neo4j import AsyncGraphDatabase

from tengin_mcp.infrastructure.config import Settings


class ExtendedDataSeeder:
    """拡張教育理論データをNeo4jに投入するクラス"""

    def __init__(self, settings: Settings):
        self.settings = settings
        self.driver = None
        project_root = Path(__file__).resolve().parent.parent.parent.parent
        self.data_dir = project_root / "data" / "theories"

    async def connect(self) -> None:
        """Neo4jに接続"""
        self.driver = AsyncGraphDatabase.driver(
            self.settings.neo4j_uri,
            auth=(self.settings.neo4j_user, self.settings.neo4j_password),
        )
        async with self.driver.session() as session:
            await session.run("RETURN 1")
        print(f"✓ Neo4jに接続しました: {self.settings.neo4j_uri}")

    async def close(self) -> None:
        """接続を閉じる"""
        if self.driver:
            await self.driver.close()
            print("✓ Neo4j接続を閉じました")

    def load_json(self, filename: str) -> dict[str, Any]:
        """JSONファイルを読み込む"""
        filepath = self.data_dir / filename
        if not filepath.exists():
            print(f"⚠ ファイルが見つかりません: {filename}")
            return {}
        with open(filepath, encoding="utf-8") as f:
            return json.load(f)

    async def clear_database(self) -> None:
        """データベースをクリア"""
        async with self.driver.session() as session:
            await session.run("MATCH (n) DETACH DELETE n")
        print("✓ 既存データをクリアしました")

    async def create_constraints(self) -> None:
        """ユニーク制約とインデックスを作成"""
        constraints = [
            "CREATE CONSTRAINT theory_id IF NOT EXISTS FOR (t:Theory) REQUIRE t.id IS UNIQUE",
            "CREATE CONSTRAINT theorist_id IF NOT EXISTS FOR (t:Theorist) REQUIRE t.id IS UNIQUE",
            "CREATE CONSTRAINT concept_id IF NOT EXISTS FOR (c:Concept) REQUIRE c.id IS UNIQUE",
            "CREATE CONSTRAINT methodology_id IF NOT EXISTS FOR (m:Methodology) REQUIRE m.id IS UNIQUE",
            "CREATE CONSTRAINT evidence_id IF NOT EXISTS FOR (e:Evidence) REQUIRE e.id IS UNIQUE",
            "CREATE CONSTRAINT context_id IF NOT EXISTS FOR (c:Context) REQUIRE c.id IS UNIQUE",
        ]

        # 全文検索インデックス
        fulltext_indexes = [
            """CREATE FULLTEXT INDEX theory_search IF NOT EXISTS
               FOR (t:Theory) ON EACH [t.name, t.name_en, t.description, t.core_principle]""",
            """CREATE FULLTEXT INDEX concept_search IF NOT EXISTS
               FOR (c:Concept) ON EACH [c.name, c.name_en, c.definition]""",
            """CREATE FULLTEXT INDEX theorist_search IF NOT EXISTS
               FOR (t:Theorist) ON EACH [t.name, t.name_en, t.field]""",
        ]

        async with self.driver.session() as session:
            for constraint in constraints:
                try:
                    await session.run(constraint)
                except Exception:
                    pass

            for index in fulltext_indexes:
                try:
                    await session.run(index)
                except Exception:
                    pass

        print("✓ 制約とインデックスを作成しました")

    async def seed_theories(self) -> int:
        """理論データを投入"""
        data = self.load_json("theories_extended.json")
        theories = data.get("theories", [])

        async with self.driver.session() as session:
            for t in theories:
                await session.run(
                    """
                    CREATE (n:Theory {
                        id: $id,
                        name: $name,
                        name_en: $name_en,
                        paradigm: $paradigm,
                        category: $category,
                        subcategory: $subcategory,
                        description: $description,
                        core_principle: $core_principle,
                        year: $year,
                        evidence_level: $evidence_level,
                        meta_analyses_count: $meta_analyses_count,
                        keywords: $keywords,
                        applications: $applications,
                        limitations: $limitations,
                        related_theories: $related_theories
                    })
                    """,
                    id=t["id"],
                    name=t["name"],
                    name_en=t["name_en"],
                    paradigm=t["paradigm"],
                    category=t["category"],
                    subcategory=t.get("subcategory", ""),
                    description=t["description"],
                    core_principle=t["core_principle"],
                    year=t["year"],
                    evidence_level=t["evidence_level"],
                    meta_analyses_count=t.get("meta_analyses_count", 0),
                    keywords=t["keywords"],
                    applications=t.get("applications", []),
                    limitations=t.get("limitations", []),
                    related_theories=t.get("related_theories", []),
                )

        print(f"✓ 理論を投入しました: {len(theories)}件")
        return len(theories)

    async def seed_theorists(self) -> int:
        """理論家データを投入"""
        data = self.load_json("theorists_extended.json")
        theorists = data.get("theorists", [])

        async with self.driver.session() as session:
            for t in theorists:
                await session.run(
                    """
                    CREATE (n:Theorist {
                        id: $id,
                        name: $name,
                        name_en: $name_en,
                        birth_year: $birth_year,
                        death_year: $death_year,
                        nationality: $nationality,
                        affiliation: $affiliation,
                        field: $field,
                        contributions: $contributions,
                        key_theories: $key_theories,
                        key_publications: $key_publications,
                        influenced_by: $influenced_by,
                        influenced: $influenced
                    })
                    """,
                    id=t["id"],
                    name=t["name"],
                    name_en=t["name_en"],
                    birth_year=t["birth_year"],
                    death_year=t.get("death_year"),
                    nationality=t["nationality"],
                    affiliation=t["affiliation"],
                    field=t["field"],
                    contributions=t["contributions"],
                    key_theories=t["key_theories"],
                    key_publications=json.dumps(t["key_publications"], ensure_ascii=False),
                    influenced_by=t.get("influenced_by", []),
                    influenced=t.get("influenced", []),
                )

        print(f"✓ 理論家を投入しました: {len(theorists)}件")
        return len(theorists)

    async def seed_concepts(self) -> int:
        """概念データを投入"""
        data = self.load_json("concepts_extended.json")
        concepts = data.get("concepts", [])

        async with self.driver.session() as session:
            for c in concepts:
                await session.run(
                    """
                    CREATE (n:Concept {
                        id: $id,
                        name: $name,
                        name_en: $name_en,
                        category: $category,
                        definition: $definition,
                        examples: $examples,
                        related_theories: $related_theories,
                        related_concepts: $related_concepts,
                        measurable: $measurable,
                        measurement_methods: $measurement_methods
                    })
                    """,
                    id=c["id"],
                    name=c["name"],
                    name_en=c["name_en"],
                    category=c["category"],
                    definition=c["definition"],
                    examples=c["examples"],
                    related_theories=c["related_theories"],
                    related_concepts=c.get("related_concepts", []),
                    measurable=c.get("measurable", False),
                    measurement_methods=c.get("measurement_methods", []),
                )

        print(f"✓ 概念を投入しました: {len(concepts)}件")
        return len(concepts)

    async def seed_methodologies(self) -> int:
        """教授法データを投入"""
        data = self.load_json("methodologies_extended.json")
        methodologies = data.get("methodologies", [])

        async with self.driver.session() as session:
            for m in methodologies:
                await session.run(
                    """
                    CREATE (n:Methodology {
                        id: $id,
                        name: $name,
                        name_en: $name_en,
                        category: $category,
                        description: $description,
                        procedures: $procedures,
                        theoretical_grounding: $theoretical_grounding,
                        evidence_level: $evidence_level,
                        effect_size: $effect_size,
                        best_for: $best_for,
                        limitations: $limitations
                    })
                    """,
                    id=m["id"],
                    name=m["name"],
                    name_en=m["name_en"],
                    category=m["category"],
                    description=m["description"],
                    procedures=m["procedures"],
                    theoretical_grounding=m["theoretical_grounding"],
                    evidence_level=m["evidence_level"],
                    effect_size=m.get("effect_size"),
                    best_for=m.get("best_for", []),
                    limitations=m.get("limitations", []),
                )

        print(f"✓ 教授法を投入しました: {len(methodologies)}件")
        return len(methodologies)

    async def seed_evidence(self) -> int:
        """エビデンスデータを投入"""
        data = self.load_json("evidence_extended.json")
        evidence_list = data.get("evidence", [])

        async with self.driver.session() as session:
            for e in evidence_list:
                await session.run(
                    """
                    CREATE (n:Evidence {
                        id: $id,
                        name: $name,
                        type: $type,
                        year: $year,
                        authors: $authors,
                        title: $title,
                        source: $source,
                        findings: $findings,
                        effect_size: $effect_size,
                        sample_size: $sample_size,
                        supports: $supports,
                        challenges: $challenges,
                        evidence_quality: $evidence_quality,
                        implications: $implications
                    })
                    """,
                    id=e["id"],
                    name=e["name"],
                    type=e["type"],
                    year=e["year"],
                    authors=e["authors"],
                    title=e["title"],
                    source=e["source"],
                    findings=e["findings"],
                    effect_size=e.get("effect_size"),
                    sample_size=e.get("sample_size"),
                    supports=e.get("supports", []),
                    challenges=e.get("challenges", []),
                    evidence_quality=e["evidence_quality"],
                    implications=e.get("implications", ""),
                )

        print(f"✓ エビデンスを投入しました: {len(evidence_list)}件")
        return len(evidence_list)

    async def seed_contexts(self) -> int:
        """文脈データを投入"""
        data = self.load_json("contexts_extended.json")
        contexts = data.get("contexts", [])

        async with self.driver.session() as session:
            for c in contexts:
                await session.run(
                    """
                    CREATE (n:Context {
                        id: $id,
                        name: $name,
                        name_en: $name_en,
                        education_level: $education_level,
                        subject_area: $subject_area,
                        description: $description,
                        characteristics: $characteristics,
                        effective_theories: $effective_theories,
                        effective_methodologies: $effective_methodologies,
                        challenges: $challenges
                    })
                    """,
                    id=c["id"],
                    name=c["name"],
                    name_en=c["name_en"],
                    education_level=c["education_level"],
                    subject_area=c.get("subject_area", "general"),
                    description=c["description"],
                    characteristics=c["characteristics"],
                    effective_theories=c["effective_theories"],
                    effective_methodologies=c["effective_methodologies"],
                    challenges=c.get("challenges", []),
                )

        print(f"✓ 文脈を投入しました: {len(contexts)}件")
        return len(contexts)

    async def seed_relationships(self) -> int:
        """関係性データを投入"""
        data = self.load_json("relationships_extended.json")
        relationships = data.get("relationships", [])
        count = 0

        async with self.driver.session() as session:
            for rel in relationships:
                source = rel["source"]
                target = rel["target"]
                rel_type = rel["type"]
                strength = rel.get("strength", "moderate")
                description = rel.get("description", "")

                # ソースノードのラベルを特定
                source_label = await self._find_node_label(session, source)
                target_label = await self._find_node_label(session, target)

                if source_label and target_label:
                    query = f"""
                    MATCH (a:{source_label} {{id: $source}})
                    MATCH (b:{target_label} {{id: $target}})
                    CREATE (a)-[r:{rel_type} {{strength: $strength, description: $description}}]->(b)
                    """
                    await session.run(
                        query,
                        source=source,
                        target=target,
                        strength=strength,
                        description=description,
                    )
                    count += 1

        print(f"✓ 関係性を投入しました: {count}件")
        return count

    async def _find_node_label(self, session, node_id: str) -> str | None:
        """ノードIDからラベルを検索"""
        labels = ["Theory", "Theorist", "Concept", "Methodology", "Evidence", "Context"]
        for label in labels:
            result = await session.run(
                f"MATCH (n:{label} {{id: $id}}) RETURN n LIMIT 1", id=node_id
            )
            record = await result.single()
            if record:
                return label
        return None

    async def create_implicit_relationships(self) -> int:
        """データから暗黙的な関係性を生成"""
        count = 0

        async with self.driver.session() as session:
            # Theory -> Concept (INCLUDES_CONCEPT) from related_theories
            result = await session.run("""
                MATCH (c:Concept)
                WHERE c.related_theories IS NOT NULL
                UNWIND c.related_theories as theory_id
                MATCH (t:Theory {id: theory_id})
                MERGE (t)-[:INCLUDES_CONCEPT]->(c)
                RETURN count(*) as count
            """)
            record = await result.single()
            count += record["count"]

            # Methodology -> Theory (THEORETICALLY_GROUNDED_IN)
            result = await session.run("""
                MATCH (m:Methodology)
                WHERE m.theoretical_grounding IS NOT NULL
                UNWIND m.theoretical_grounding as theory_id
                MATCH (t:Theory {id: theory_id})
                MERGE (m)-[:THEORETICALLY_GROUNDED_IN]->(t)
                RETURN count(*) as count
            """)
            record = await result.single()
            count += record["count"]

            # Evidence -> Theory (SUPPORTS)
            result = await session.run("""
                MATCH (e:Evidence)
                WHERE e.supports IS NOT NULL
                UNWIND e.supports as theory_id
                MATCH (t:Theory {id: theory_id})
                MERGE (e)-[:SUPPORTS]->(t)
                RETURN count(*) as count
            """)
            record = await result.single()
            count += record["count"]

            # Evidence -> Theory (CHALLENGES)
            result = await session.run("""
                MATCH (e:Evidence)
                WHERE e.challenges IS NOT NULL
                UNWIND e.challenges as theory_id
                MATCH (t:Theory {id: theory_id})
                MERGE (e)-[:CHALLENGES]->(t)
                RETURN count(*) as count
            """)
            record = await result.single()
            count += record["count"]

            # Context -> Theory (EFFECTIVE_FOR)
            result = await session.run("""
                MATCH (c:Context)
                WHERE c.effective_theories IS NOT NULL
                UNWIND c.effective_theories as theory_id
                MATCH (t:Theory {id: theory_id})
                MERGE (t)-[:EFFECTIVE_FOR]->(c)
                RETURN count(*) as count
            """)
            record = await result.single()
            count += record["count"]

            # Context -> Methodology (APPLICABLE_IN)
            result = await session.run("""
                MATCH (c:Context)
                WHERE c.effective_methodologies IS NOT NULL
                UNWIND c.effective_methodologies as method_id
                MATCH (m:Methodology {id: method_id})
                MERGE (m)-[:APPLICABLE_IN]->(c)
                RETURN count(*) as count
            """)
            record = await result.single()
            count += record["count"]

            # Theory -> Theory (related_theories)
            result = await session.run("""
                MATCH (t1:Theory)
                WHERE t1.related_theories IS NOT NULL
                UNWIND t1.related_theories as related_id
                MATCH (t2:Theory {id: related_id})
                WHERE t1.id <> t2.id
                MERGE (t1)-[:RELATED_TO]->(t2)
                RETURN count(*) as count
            """)
            record = await result.single()
            count += record["count"]

        print(f"✓ 暗黙的関係性を生成しました: {count}件")
        return count

    async def verify_data(self) -> dict[str, int]:
        """投入データを検証"""
        counts = {}
        labels = ["Theory", "Theorist", "Concept", "Methodology", "Evidence", "Context"]

        async with self.driver.session() as session:
            for label in labels:
                result = await session.run(f"MATCH (n:{label}) RETURN count(n) as count")
                record = await result.single()
                counts[label] = record["count"]

            # 関係性の数
            result = await session.run("MATCH ()-[r]->() RETURN count(r) as count")
            record = await result.single()
            counts["Relationships"] = record["count"]

            # パラダイム別の理論数
            result = await session.run("""
                MATCH (t:Theory)
                RETURN t.paradigm as paradigm, count(*) as count
                ORDER BY count DESC
            """)
            paradigm_counts = {}
            async for record in result:
                paradigm_counts[record["paradigm"]] = record["count"]
            counts["Paradigms"] = paradigm_counts

        return counts

    async def run(self, clear: bool = True) -> None:
        """データ投入を実行"""
        print("=" * 60)
        print("TENGIN GraphRAG - 拡張教育理論データ投入スクリプト")
        print("=" * 60)

        try:
            await self.connect()

            if clear:
                await self.clear_database()

            await self.create_constraints()

            # ノードを投入
            print("\n--- ノード投入 ---")
            await self.seed_theories()
            await self.seed_theorists()
            await self.seed_concepts()
            await self.seed_methodologies()
            await self.seed_evidence()
            await self.seed_contexts()

            # 明示的な関係性を投入
            print("\n--- 関係性投入 ---")
            await self.seed_relationships()

            # 暗黙的な関係性を生成
            await self.create_implicit_relationships()

            # 検証
            print("\n--- データ検証 ---")
            counts = await self.verify_data()
            for label, count in counts.items():
                if isinstance(count, dict):
                    print(f"  {label}:")
                    for k, v in count.items():
                        print(f"    - {k}: {v}")
                else:
                    print(f"  {label}: {count}件")

            print("\n" + "=" * 60)
            print("✓ 拡張データ投入が完了しました！")
            print("=" * 60)

        finally:
            await self.close()


async def main():
    """メイン関数"""
    settings = Settings()
    seeder = ExtendedDataSeeder(settings)
    await seeder.run()


if __name__ == "__main__":
    asyncio.run(main())
