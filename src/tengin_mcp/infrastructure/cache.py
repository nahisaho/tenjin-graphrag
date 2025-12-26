"""Infrastructure: Simple in-memory cache with TTL support."""

import asyncio
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from functools import wraps
from typing import Any, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


@dataclass
class CacheEntry:
    """キャッシュエントリ。"""

    value: Any
    expires_at: float
    hits: int = 0


@dataclass
class CacheStats:
    """キャッシュ統計情報。"""

    hits: int = 0
    misses: int = 0
    size: int = 0
    max_size: int = 0

    @property
    def hit_rate(self) -> float:
        """ヒット率を計算。"""
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0


@dataclass
class SimpleCache:
    """
    シンプルな TTL ベースのインメモリキャッシュ。

    Features:
    - TTL (Time-To-Live) サポート
    - 最大サイズ制限
    - LRU (Least Recently Used) 風の削除
    - 非同期関数のキャッシュデコレータ
    """

    default_ttl: float = 300.0  # 5分
    max_size: int = 1000
    _cache: dict[str, CacheEntry] = field(default_factory=dict)
    _stats: CacheStats = field(default_factory=CacheStats)
    _lock: asyncio.Lock = field(default_factory=asyncio.Lock)

    async def get(self, key: str) -> Any | None:
        """
        キャッシュから値を取得。

        Args:
            key: キャッシュキー

        Returns:
            キャッシュされた値、または None
        """
        async with self._lock:
            entry = self._cache.get(key)
            if entry is None:
                self._stats.misses += 1
                return None

            if time.time() > entry.expires_at:
                del self._cache[key]
                self._stats.misses += 1
                return None

            entry.hits += 1
            self._stats.hits += 1
            return entry.value

    async def set(self, key: str, value: Any, ttl: float | None = None) -> None:
        """
        値をキャッシュに保存。

        Args:
            key: キャッシュキー
            value: 保存する値
            ttl: TTL（秒）、None の場合はデフォルト TTL
        """
        async with self._lock:
            # 最大サイズ超過時は古いエントリを削除
            if len(self._cache) >= self.max_size:
                await self._evict_oldest()

            expires_at = time.time() + (ttl if ttl is not None else self.default_ttl)
            self._cache[key] = CacheEntry(value=value, expires_at=expires_at)
            self._stats.size = len(self._cache)
            self._stats.max_size = max(self._stats.max_size, self._stats.size)

    async def delete(self, key: str) -> bool:
        """
        キャッシュから削除。

        Args:
            key: キャッシュキー

        Returns:
            削除された場合は True
        """
        async with self._lock:
            if key in self._cache:
                del self._cache[key]
                self._stats.size = len(self._cache)
                return True
            return False

    async def clear(self) -> None:
        """キャッシュをクリア。"""
        async with self._lock:
            self._cache.clear()
            self._stats.size = 0

    async def invalidate_pattern(self, pattern: str) -> int:
        """
        パターンに一致するキーを削除。

        Args:
            pattern: プレフィックスパターン

        Returns:
            削除されたエントリ数
        """
        async with self._lock:
            keys_to_delete = [k for k in self._cache if k.startswith(pattern)]
            for key in keys_to_delete:
                del self._cache[key]
            self._stats.size = len(self._cache)
            return len(keys_to_delete)

    def get_stats(self) -> CacheStats:
        """統計情報を取得。"""
        return self._stats

    async def _evict_oldest(self) -> None:
        """最も古い/アクセスの少ないエントリを削除。"""
        if not self._cache:
            return

        # 有効期限切れのエントリを優先削除
        now = time.time()
        expired_keys = [k for k, v in self._cache.items() if v.expires_at < now]
        for key in expired_keys[:10]:  # 最大10件
            del self._cache[key]

        # まだ削除が必要な場合、hits が少ないものを削除
        if len(self._cache) >= self.max_size:
            sorted_entries = sorted(self._cache.items(), key=lambda x: (x[1].hits, x[1].expires_at))
            for key, _ in sorted_entries[: len(self._cache) // 10]:
                del self._cache[key]


def cached(
    cache: SimpleCache,
    ttl: float | None = None,
    key_prefix: str = "",
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    非同期関数をキャッシュするデコレータ。

    Args:
        cache: キャッシュインスタンス
        ttl: TTL（秒）
        key_prefix: キャッシュキーのプレフィックス

    Example:
        ```python
        cache = SimpleCache()

        @cached(cache, ttl=60, key_prefix="theory")
        async def get_theory(theory_id: str) -> Theory:
            ...
        ```
    """

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            # キャッシュキーを生成
            key_parts = [key_prefix or func.__name__]
            key_parts.extend(str(arg) for arg in args)
            key_parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))
            cache_key = ":".join(key_parts)

            # キャッシュチェック
            cached_value = await cache.get(cache_key)
            if cached_value is not None:
                return cached_value

            # 関数を実行してキャッシュ
            result = await func(*args, **kwargs)
            await cache.set(cache_key, result, ttl)
            return result

        return wrapper

    return decorator


# グローバルキャッシュインスタンス
_theory_cache: SimpleCache | None = None
_graph_cache: SimpleCache | None = None


def get_theory_cache() -> SimpleCache:
    """Theory キャッシュを取得。"""
    global _theory_cache
    if _theory_cache is None:
        _theory_cache = SimpleCache(default_ttl=300.0, max_size=500)
    return _theory_cache


def get_graph_cache() -> SimpleCache:
    """Graph キャッシュを取得。"""
    global _graph_cache
    if _graph_cache is None:
        _graph_cache = SimpleCache(default_ttl=60.0, max_size=200)
    return _graph_cache


async def clear_all_caches() -> None:
    """全キャッシュをクリア。"""
    if _theory_cache:
        await _theory_cache.clear()
    if _graph_cache:
        await _graph_cache.clear()
