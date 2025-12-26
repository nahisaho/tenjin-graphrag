"""
Neo4jへのサンプルデータ投入スクリプト

使用方法:
    uv run python -m tengin_mcp.scripts.seed_data

事前準備:
    1. docker compose up -d でNeo4jを起動
    2. .env ファイルに接続情報を設定
"""

import asyncio
import json
from pathlib import Path
from typing import Any

from neo4j import AsyncGraphDatabase

from tengin_mcp.infrastructure.config import Settings


class DataSeeder:
    """Neo4jへのデータ投入を行うクラス"""

    def __init__(self, settings: Settings):
        self.settings = settings
        self.driver = None
        # scripts -> tengin_mcp -> src -> TENGIN-GraphRAG
        project_root = Path(__file__).resolve().parent.parent.parent.parent
        self.data_dir = project_root / "data" / "theories"

    async def connect(self) -> None:
        """Neo4jに接続"""
        self.driver = AsyncGraphDatabase.driver(
            self.settings.neo4j_uri,
            auth=(self.settings.neo4j_user, self.settings.neo4j_password),
        )
        # 接続確認
        async with self.driver.session() as session:
            await session.run("RETURN 1")
        print(f"✓ Neo4jに接続しました: {self.settings.neo4j_uri}")

    async def close(self) -> None:
        """接続を閉じる"""
        if self.driver:
            await self.driver.close()
            print("✓ Neo4j接続を閉じました")

    def load_json(self, filename: str, key: str) -> list[dict[str, Any]]:
        """JSONファイルを読み込む"""
        filepath = self.data_dir / filename
        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)
        return data.get(key, [])

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
            "CREATE CONSTRAINT principle_id IF NOT EXISTS FOR (p:Principle) REQUIRE p.id IS UNIQUE",
            "CREATE CONSTRAINT evidence_id IF NOT EXISTS FOR (e:Evidence) REQUIRE e.id IS UNIQUE",
        ]

        async with self.driver.session() as session:
            for constraint in constraints:
                try:
                    await session.run(constraint)
                except Exception:
                    pass  # 既に存在する場合は無視

        print("✓ 制約を作成しました")

    async def seed_theories(self) -> int:
        """理論データを投入"""
        theories = self.load_json("theories.json", "theories")

        async with self.driver.session() as session:
            for t in theories:
                await session.run(
                    """
                    CREATE (n:Theory {
                        id: $id,
                        name: $name,
                        name_en: $name_en,
                        description: $description,
                        category: $category,
                        year: $year,
                        evidence_level: $evidence_level,
                        keywords: $keywords,
                        summary: $summary
                    })
                    """,
                    id=t["id"],
                    name=t["name"],
                    name_en=t["name_en"],
                    description=t["description"],
                    category=t["category"],
                    year=t["year"],
                    evidence_level=t["evidence_level"],
                    keywords=t["keywords"],
                    summary=t["summary"],
                )

        print(f"✓ 理論を投入しました: {len(theories)}件")
        return len(theories)

    async def seed_theorists(self) -> int:
        """理論家データを投入"""
        theorists = self.load_json("theorists.json", "theorists")

        async with self.driver.session() as session:
            for t in theorists:
                await session.run(
                    """
                    CREATE (n:Theorist {
                        id: $id,
                        name: $name,
                        name_en: $name_en,
                        birth_year: $birth_year,
                        nationality: $nationality,
                        affiliation: $affiliation,
                        biography: $biography,
                        major_works: $major_works
                    })
                    """,
                    id=t["id"],
                    name=t["name"],
                    name_en=t["name_en"],
                    birth_year=t["birth_year"],
                    nationality=t["nationality"],
                    affiliation=t["affiliation"],
                    biography=t["biography"],
                    major_works=t["major_works"],
                )

        print(f"✓ 理論家を投入しました: {len(theorists)}件")
        return len(theorists)

    async def seed_concepts(self) -> int:
        """概念データを投入"""
        concepts = self.load_json("concepts.json", "concepts")

        async with self.driver.session() as session:
            for c in concepts:
                await session.run(
                    """
                    CREATE (n:Concept {
                        id: $id,
                        name: $name,
                        name_en: $name_en,
                        definition: $definition,
                        examples: $examples,
                        related_theory_ids: $related_theory_ids
                    })
                    """,
                    id=c["id"],
                    name=c["name"],
                    name_en=c["name_en"],
                    definition=c["definition"],
                    examples=c["examples"],
                    related_theory_ids=c["related_theory_ids"],
                )

        print(f"✓ 概念を投入しました: {len(concepts)}件")
        return len(concepts)

    async def seed_principles(self) -> int:
        """原則データを投入"""
        principles = self.load_json("principles.json", "principles")

        async with self.driver.session() as session:
            for p in principles:
                await session.run(
                    """
                    CREATE (n:Principle {
                        id: $id,
                        name: $name,
                        description: $description,
                        application_guide: $application_guide,
                        examples: $examples,
                        source_theory_id: $source_theory_id
                    })
                    """,
                    id=p["id"],
                    name=p["name"],
                    description=p["description"],
                    application_guide=p["application_guide"],
                    examples=p["examples"],
                    source_theory_id=p["source_theory_id"],
                )

        print(f"✓ 原則を投入しました: {len(principles)}件")
        return len(principles)

    async def seed_evidence(self) -> int:
        """エビデンスデータを投入"""
        evidence_list = self.load_json("evidence.json", "evidence")

        async with self.driver.session() as session:
            for e in evidence_list:
                await session.run(
                    """
                    CREATE (n:Evidence {
                        id: $id,
                        title: $title,
                        authors: $authors,
                        year: $year,
                        source: $source,
                        doi: $doi,
                        evidence_type: $evidence_type,
                        methodology: $methodology,
                        findings: $findings,
                        sample_size: $sample_size,
                        effect_size: $effect_size,
                        supported_theory_ids: $supported_theory_ids
                    })
                    """,
                    id=e["id"],
                    title=e["title"],
                    authors=e["authors"],
                    year=e["year"],
                    source=e["source"],
                    doi=e.get("doi"),
                    evidence_type=e["evidence_type"],
                    methodology=e["methodology"],
                    findings=e["findings"],
                    sample_size=e.get("sample_size"),
                    effect_size=e.get("effect_size"),
                    supported_theory_ids=e["supported_theory_ids"],
                )

        print(f"✓ エビデンスを投入しました: {len(evidence_list)}件")
        return len(evidence_list)

    async def seed_relationships(self) -> int:
        """関係性データを投入"""
        relationships = self.load_json("relationships.json", "relationships")

        async with self.driver.session() as session:
            for rel in relationships:
                rel_type = rel["type"]
                from_id = rel["from_id"]
                to_id = rel["to_id"]

                # ノードのラベルを推定
                from_label = self._get_label_from_id(from_id)
                to_label = self._get_label_from_id(to_id)

                props = rel.get("properties", {})

                if props:
                    prop_str = ", ".join([f"{k}: ${k}" for k in props.keys()])
                    query = f"""
                    MATCH (a:{from_label} {{id: $from_id}})
                    MATCH (b:{to_label} {{id: $to_id}})
                    CREATE (a)-[r:{rel_type} {{{prop_str}}}]->(b)
                    """
                    await session.run(query, from_id=from_id, to_id=to_id, **props)
                else:
                    query = f"""
                    MATCH (a:{from_label} {{id: $from_id}})
                    MATCH (b:{to_label} {{id: $to_id}})
                    CREATE (a)-[r:{rel_type}]->(b)
                    """
                    await session.run(query, from_id=from_id, to_id=to_id)

        print(f"✓ 関係性を投入しました: {len(relationships)}件")
        return len(relationships)

    def _get_label_from_id(self, node_id: str) -> str:
        """IDからノードラベルを推定"""
        # IDの先頭部分（最初のハイフンまで）でラベルを判定
        parts = node_id.split("-")
        if len(parts) < 2:
            return "Node"

        # john-sweller のような形式
        label_hints = {
            "cognitive": "Theory",
            "constructivism": "Theory",
            "zone": "Theory",
            "multimedia": "Theory",
            "self": "Theory",
            "blooms": "Theory",
            "gagnes": "Theory",
            "elaboration": "Theory",
            "john": "Theorist",
            "jean": "Theorist",
            "lev": "Theorist",
            "richard": "Theorist",
            "edward": "Theorist",
            "benjamin": "Theorist",
            "robert": "Theorist",
            "charles": "Theorist",
            "intrinsic": "Concept",
            "extraneous": "Concept",
            "germane": "Concept",
            "scaffolding": "Concept",
            "schema": "Concept",
            "dual": "Concept",
            "autonomy": "Concept",
            "split": "Principle",
            "redundancy": "Principle",
            "modality": "Principle",
            "contiguity": "Principle",
            "worked": "Principle",
            "expertise": "Principle",
            "sweller": "Evidence",
            "mayer": "Evidence",
            "chi": "Evidence",
        }

        first_part = parts[0].lower()
        return label_hints.get(first_part, "Node")

    async def verify_data(self) -> dict[str, int]:
        """投入データを検証"""
        counts = {}
        labels = ["Theory", "Theorist", "Concept", "Principle", "Evidence"]

        async with self.driver.session() as session:
            for label in labels:
                result = await session.run(f"MATCH (n:{label}) RETURN count(n) as count")
                record = await result.single()
                counts[label] = record["count"]

            # 関係性の数
            result = await session.run("MATCH ()-[r]->() RETURN count(r) as count")
            record = await result.single()
            counts["Relationships"] = record["count"]

        return counts

    async def run(self, clear: bool = True) -> None:
        """データ投入を実行"""
        print("=" * 50)
        print("TENGIN GraphRAG - データ投入スクリプト")
        print("=" * 50)

        try:
            await self.connect()

            if clear:
                await self.clear_database()

            await self.create_constraints()

            # ノードを投入
            await self.seed_theories()
            await self.seed_theorists()
            await self.seed_concepts()
            await self.seed_principles()
            await self.seed_evidence()

            # 関係性を投入
            await self.seed_relationships()

            # 検証
            print("\n--- データ検証 ---")
            counts = await self.verify_data()
            for label, count in counts.items():
                print(f"  {label}: {count}件")

            print("\n✓ データ投入が完了しました！")

        finally:
            await self.close()


async def main():
    """メイン関数"""
    settings = Settings()
    seeder = DataSeeder(settings)
    await seeder.run()


if __name__ == "__main__":
    asyncio.run(main())
