"""Domain: Custom Errors."""


class TenginError(Exception):
    """TENGIN MCP Server の基底例外クラス。"""

    def __init__(self, message: str, code: str = "TENGIN_ERROR") -> None:
        self.message = message
        self.code = code
        super().__init__(message)


# Alias for backward compatibility
GraphRAGError = TenginError


class TheoryNotFoundError(TenginError):
    """理論が見つからない場合の例外。"""

    def __init__(self, theory_id: str) -> None:
        super().__init__(
            message=f"Theory not found: {theory_id}",
            code="THEORY_NOT_FOUND",
        )
        self.theory_id = theory_id


class ConceptNotFoundError(TenginError):
    """概念が見つからない場合の例外。"""

    def __init__(self, concept_id: str) -> None:
        super().__init__(
            message=f"Concept not found: {concept_id}",
            code="CONCEPT_NOT_FOUND",
        )
        self.concept_id = concept_id


class TheoristNotFoundError(TenginError):
    """理論家が見つからない場合の例外。"""

    def __init__(self, theorist_id: str) -> None:
        super().__init__(
            message=f"Theorist not found: {theorist_id}",
            code="THEORIST_NOT_FOUND",
        )
        self.theorist_id = theorist_id


class InvalidQueryError(TenginError):
    """無効なクエリの例外。"""

    def __init__(self, message: str) -> None:
        super().__init__(
            message=message,
            code="INVALID_QUERY",
        )


class EntityNotFoundError(TenginError):
    """エンティティが見つからない場合の汎用例外。"""

    def __init__(self, entity_type: str, entity_id: str) -> None:
        super().__init__(
            message=f"{entity_type} not found: {entity_id}",
            code=f"{entity_type.upper()}_NOT_FOUND",
        )
        self.entity_type = entity_type
        self.entity_id = entity_id


class GraphTraversalError(TenginError):
    """グラフトラバーサルエラー。"""

    def __init__(self, message: str) -> None:
        super().__init__(
            message=message,
            code="GRAPH_TRAVERSAL_ERROR",
        )


class DatabaseConnectionError(TenginError):
    """データベース接続エラー。"""

    def __init__(self, message: str) -> None:
        super().__init__(
            message=message,
            code="DATABASE_CONNECTION_ERROR",
        )
