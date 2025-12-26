"""MCP Tools: システム管理ツール"""

from tengin_mcp.infrastructure.cache import (
    clear_all_caches,
    get_graph_cache,
    get_theory_cache,
)
from tengin_mcp.server import app_state, mcp


@mcp.tool()
async def get_cache_stats() -> dict:
    """
    キャッシュの統計情報を取得します。

    Returns:
        キャッシュの統計情報（ヒット率、サイズなど）
    """
    theory_cache = get_theory_cache()
    graph_cache = get_graph_cache()

    theory_stats = theory_cache.get_stats()
    graph_stats = graph_cache.get_stats()

    return {
        "theory_cache": {
            "hits": theory_stats.hits,
            "misses": theory_stats.misses,
            "hit_rate": round(theory_stats.hit_rate * 100, 2),
            "size": theory_stats.size,
            "max_size_reached": theory_stats.max_size,
        },
        "graph_cache": {
            "hits": graph_stats.hits,
            "misses": graph_stats.misses,
            "hit_rate": round(graph_stats.hit_rate * 100, 2),
            "size": graph_stats.size,
            "max_size_reached": graph_stats.max_size,
        },
        "total": {
            "hits": theory_stats.hits + graph_stats.hits,
            "misses": theory_stats.misses + graph_stats.misses,
            "hit_rate": round(
                (
                    (theory_stats.hits + graph_stats.hits)
                    / max(
                        1,
                        theory_stats.hits
                        + graph_stats.hits
                        + theory_stats.misses
                        + graph_stats.misses,
                    )
                )
                * 100,
                2,
            ),
        },
    }


@mcp.tool()
async def clear_cache(cache_type: str | None = None) -> dict:
    """
    キャッシュをクリアします。

    Args:
        cache_type: クリアするキャッシュの種類
                   - "theory": Theory キャッシュのみ
                   - "graph": Graph キャッシュのみ
                   - None または "all": 全キャッシュ

    Returns:
        クリア結果
    """
    if cache_type == "theory":
        theory_cache = get_theory_cache()
        await theory_cache.clear()
        return {"cleared": "theory", "message": "Theory cache cleared"}
    elif cache_type == "graph":
        graph_cache = get_graph_cache()
        await graph_cache.clear()
        return {"cleared": "graph", "message": "Graph cache cleared"}
    else:
        await clear_all_caches()
        return {"cleared": "all", "message": "All caches cleared"}


@mcp.tool()
async def health_check() -> dict:
    """
    システムの健康状態をチェックします。

    Returns:
        各コンポーネントの状態
    """
    status = {
        "status": "healthy",
        "components": {},
    }

    # Theory Repository チェック
    if app_state.theory_repository:
        try:
            theories = await app_state.theory_repository.get_all()
            status["components"]["theory_repository"] = {
                "status": "healthy",
                "theory_count": len(theories),
            }
        except Exception as e:
            status["components"]["theory_repository"] = {
                "status": "unhealthy",
                "error": str(e),
            }
            status["status"] = "degraded"
    else:
        status["components"]["theory_repository"] = {
            "status": "not_initialized",
        }

    # Graph Repository チェック
    if app_state.graph_repository:
        try:
            stats = await app_state.graph_repository.get_statistics()
            status["components"]["graph_repository"] = {
                "status": "healthy",
                "node_count": stats.get("total_nodes", 0),
                "relationship_count": stats.get("total_relationships", 0),
            }
        except Exception as e:
            status["components"]["graph_repository"] = {
                "status": "unhealthy",
                "error": str(e),
            }
            status["status"] = "degraded"
    else:
        status["components"]["graph_repository"] = {
            "status": "not_initialized",
        }

    # Vector Repository チェック
    if app_state.vector_repository:
        status["components"]["vector_repository"] = {
            "status": "healthy",
        }
    else:
        status["components"]["vector_repository"] = {
            "status": "not_initialized",
        }

    # Cache チェック
    theory_cache = get_theory_cache()
    graph_cache = get_graph_cache()
    status["components"]["cache"] = {
        "status": "healthy",
        "theory_cache_size": theory_cache.get_stats().size,
        "graph_cache_size": graph_cache.get_stats().size,
    }

    return status


@mcp.tool()
async def get_system_info() -> dict:
    """
    システム情報を取得します。

    Returns:
        バージョン、設定などのシステム情報
    """
    from tengin_mcp import __version__

    return {
        "name": "TENGIN Education Theory MCP Server",
        "version": __version__,
        "mcp_version": "1.0",
        "features": {
            "tools": 23,
            "resources": 5,
            "prompts": 3,
        },
        "capabilities": [
            "theory_search",
            "graph_traversal",
            "citation_generation",
            "methodology_recommendation",
            "context_search",
            "evidence_analysis",
            "caching",
        ],
        "supported_categories": [
            "learning",
            "instructional",
            "developmental",
            "motivation",
            "edtech",
            "adult_learning",
            "intelligence",
        ],
        "supported_evidence_levels": [
            "strong",
            "moderate",
            "limited",
            "theoretical",
            "emerging",
        ],
        "supported_citation_formats": [
            "APA7",
            "MLA9",
            "Chicago",
            "Harvard",
            "IEEE",
        ],
    }
