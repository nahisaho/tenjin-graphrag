"""Domain: Repository Interfaces."""

from abc import abstractmethod
from typing import Protocol

from tengin_mcp.domain.entities.concept import Concept
from tengin_mcp.domain.entities.evidence import Evidence
from tengin_mcp.domain.entities.principle import Principle
from tengin_mcp.domain.entities.theorist import Theorist
from tengin_mcp.domain.entities.theory import Theory, TheorySummary
from tengin_mcp.domain.value_objects.theory_category import TheoryCategory


class TheoryRepository(Protocol):
    """理論リポジトリのインターフェース。"""

    @abstractmethod
    async def get_by_id(self, theory_id: str) -> Theory | None:
        """IDで理論を取得。"""
        ...

    @abstractmethod
    async def get_all(self) -> list[TheorySummary]:
        """全理論の要約リストを取得。"""
        ...

    @abstractmethod
    async def get_by_category(self, category: TheoryCategory) -> list[TheorySummary]:
        """カテゴリで理論をフィルタリング。"""
        ...

    @abstractmethod
    async def search(self, query: str, limit: int = 10) -> list[TheorySummary]:
        """キーワード検索。"""
        ...

    @abstractmethod
    async def get_theorist(self, theory_id: str) -> Theorist | None:
        """理論の提唱者を取得。"""
        ...

    @abstractmethod
    async def get_concepts(self, theory_id: str) -> list[Concept]:
        """理論に含まれる概念を取得。"""
        ...

    @abstractmethod
    async def get_principles(self, theory_id: str) -> list[Principle]:
        """理論から導出される原則を取得。"""
        ...

    @abstractmethod
    async def get_evidence(self, theory_id: str) -> list[Evidence]:
        """理論を支持するエビデンスを取得。"""
        ...


class GraphRepository(Protocol):
    """グラフリポジトリのインターフェース。"""

    @abstractmethod
    async def traverse(
        self,
        start_theory_id: str,
        depth: int = 2,
        relation_types: list[str] | None = None,
    ) -> dict:
        """
        理論からグラフをトラバース。

        Returns:
            {
                "nodes": [{"id": ..., "name": ..., "type": ...}, ...],
                "edges": [{"from": ..., "to": ..., "type": ...}, ...]
            }
        """
        ...

    @abstractmethod
    async def get_related_theories(
        self,
        theory_id: str,
        relation_type: str,
    ) -> list[TheorySummary]:
        """特定のリレーションタイプで関連する理論を取得。"""
        ...

    @abstractmethod
    async def get_schema(self) -> dict:
        """グラフスキーマ情報を取得。"""
        ...

    @abstractmethod
    async def get_stats(self) -> dict:
        """グラフの統計情報を取得。"""
        ...
