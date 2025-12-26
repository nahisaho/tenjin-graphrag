"""Unit tests for SimpleCache."""

import asyncio
import time

import pytest

from tengin_mcp.infrastructure.cache import (
    CacheEntry,
    CacheStats,
    SimpleCache,
    cached,
    clear_all_caches,
    get_graph_cache,
    get_theory_cache,
)


class TestCacheEntry:
    """CacheEntry のテスト。"""

    def test_create_entry(self) -> None:
        """エントリ作成のテスト。"""
        entry = CacheEntry(value="test", expires_at=time.time() + 60)
        assert entry.value == "test"
        assert entry.hits == 0

    def test_entry_hits_counter(self) -> None:
        """ヒットカウンターのテスト。"""
        entry = CacheEntry(value="test", expires_at=time.time() + 60, hits=5)
        assert entry.hits == 5


class TestCacheStats:
    """CacheStats のテスト。"""

    def test_default_stats(self) -> None:
        """デフォルト統計のテスト。"""
        stats = CacheStats()
        assert stats.hits == 0
        assert stats.misses == 0
        assert stats.size == 0

    def test_hit_rate_zero_total(self) -> None:
        """総数ゼロ時のヒット率。"""
        stats = CacheStats()
        assert stats.hit_rate == 0.0

    def test_hit_rate_calculation(self) -> None:
        """ヒット率計算のテスト。"""
        stats = CacheStats(hits=3, misses=1)
        assert stats.hit_rate == 0.75

    def test_hit_rate_100_percent(self) -> None:
        """100%ヒット率のテスト。"""
        stats = CacheStats(hits=10, misses=0)
        assert stats.hit_rate == 1.0


class TestSimpleCache:
    """SimpleCache のテスト。"""

    @pytest.fixture
    def cache(self) -> SimpleCache:
        """キャッシュインスタンスを作成。"""
        return SimpleCache(default_ttl=60.0, max_size=10)

    @pytest.mark.asyncio
    async def test_get_nonexistent_key(self, cache: SimpleCache) -> None:
        """存在しないキーの取得。"""
        result = await cache.get("nonexistent")
        assert result is None

    @pytest.mark.asyncio
    async def test_set_and_get(self, cache: SimpleCache) -> None:
        """保存と取得。"""
        await cache.set("key1", "value1")
        result = await cache.get("key1")
        assert result == "value1"

    @pytest.mark.asyncio
    async def test_set_with_custom_ttl(self, cache: SimpleCache) -> None:
        """カスタムTTLでの保存。"""
        await cache.set("key1", "value1", ttl=0.1)
        result = await cache.get("key1")
        assert result == "value1"

        # TTL後は取得できない
        await asyncio.sleep(0.15)
        result = await cache.get("key1")
        assert result is None

    @pytest.mark.asyncio
    async def test_delete_existing_key(self, cache: SimpleCache) -> None:
        """存在するキーの削除。"""
        await cache.set("key1", "value1")
        result = await cache.delete("key1")
        assert result is True
        assert await cache.get("key1") is None

    @pytest.mark.asyncio
    async def test_delete_nonexistent_key(self, cache: SimpleCache) -> None:
        """存在しないキーの削除。"""
        result = await cache.delete("nonexistent")
        assert result is False

    @pytest.mark.asyncio
    async def test_clear(self, cache: SimpleCache) -> None:
        """クリア。"""
        await cache.set("key1", "value1")
        await cache.set("key2", "value2")
        await cache.clear()
        assert await cache.get("key1") is None
        assert await cache.get("key2") is None

    @pytest.mark.asyncio
    async def test_invalidate_pattern(self, cache: SimpleCache) -> None:
        """パターン削除。"""
        await cache.set("theory:1", "t1")
        await cache.set("theory:2", "t2")
        await cache.set("graph:1", "g1")

        deleted = await cache.invalidate_pattern("theory:")
        assert deleted == 2
        assert await cache.get("theory:1") is None
        assert await cache.get("graph:1") == "g1"

    @pytest.mark.asyncio
    async def test_stats_tracking(self, cache: SimpleCache) -> None:
        """統計トラッキング。"""
        await cache.set("key1", "value1")
        await cache.get("key1")  # hit
        await cache.get("key1")  # hit
        await cache.get("nonexistent")  # miss

        stats = cache.get_stats()
        assert stats.hits == 2
        assert stats.misses == 1
        assert stats.size == 1

    @pytest.mark.asyncio
    async def test_max_size_eviction(self) -> None:
        """最大サイズ時の削除。"""
        cache = SimpleCache(default_ttl=60.0, max_size=3)

        await cache.set("key1", "value1")
        await cache.set("key2", "value2")
        await cache.set("key3", "value3")
        await cache.set("key4", "value4")  # これで削除が発生

        # 少なくとも最新のものは残っている
        assert await cache.get("key4") == "value4"

    @pytest.mark.asyncio
    async def test_expired_entry_removal(self, cache: SimpleCache) -> None:
        """期限切れエントリの削除。"""
        await cache.set("key1", "value1", ttl=0.1)
        await asyncio.sleep(0.15)

        # 期限切れのエントリは取得できない
        result = await cache.get("key1")
        assert result is None

        # 統計にmissとして記録
        stats = cache.get_stats()
        assert stats.misses == 1

    @pytest.mark.asyncio
    async def test_overwrite_existing_key(self, cache: SimpleCache) -> None:
        """既存キーの上書き。"""
        await cache.set("key1", "value1")
        await cache.set("key1", "value2")
        result = await cache.get("key1")
        assert result == "value2"


class TestCachedDecorator:
    """cached デコレータのテスト。"""

    @pytest.mark.asyncio
    async def test_cached_function(self) -> None:
        """キャッシュされた関数。"""
        cache = SimpleCache(default_ttl=60.0)
        call_count = 0

        @cached(cache, ttl=60.0, key_prefix="test")
        async def expensive_function(x: int) -> int:
            nonlocal call_count
            call_count += 1
            return x * 2

        # 最初の呼び出し
        result1 = await expensive_function(5)
        assert result1 == 10
        assert call_count == 1

        # 2回目はキャッシュから
        result2 = await expensive_function(5)
        assert result2 == 10
        assert call_count == 1  # 増えていない

        # 異なる引数では新しく計算
        result3 = await expensive_function(10)
        assert result3 == 20
        assert call_count == 2

    @pytest.mark.asyncio
    async def test_cached_with_kwargs(self) -> None:
        """キーワード引数でのキャッシュ。"""
        cache = SimpleCache(default_ttl=60.0)
        call_count = 0

        @cached(cache, key_prefix="kwargs_test")
        async def func_with_kwargs(a: int, b: str = "default") -> str:
            nonlocal call_count
            call_count += 1
            return f"{a}-{b}"

        result1 = await func_with_kwargs(1, b="test")
        result2 = await func_with_kwargs(1, b="test")
        assert result1 == result2 == "1-test"
        assert call_count == 1

        # 異なる kwargs では新しく計算
        result3 = await func_with_kwargs(1, b="other")
        assert result3 == "1-other"
        assert call_count == 2


class TestGlobalCaches:
    """グローバルキャッシュのテスト。"""

    def test_get_theory_cache(self) -> None:
        """Theory キャッシュの取得。"""
        cache = get_theory_cache()
        assert cache is not None
        assert isinstance(cache, SimpleCache)

        # 同じインスタンスが返される
        cache2 = get_theory_cache()
        assert cache is cache2

    def test_get_graph_cache(self) -> None:
        """Graph キャッシュの取得。"""
        cache = get_graph_cache()
        assert cache is not None
        assert isinstance(cache, SimpleCache)

    @pytest.mark.asyncio
    async def test_clear_all_caches(self) -> None:
        """全キャッシュのクリア。"""
        theory_cache = get_theory_cache()
        graph_cache = get_graph_cache()

        await theory_cache.set("test_key", "test_value")
        await graph_cache.set("test_key", "test_value")

        await clear_all_caches()

        # クリア後は取得できない
        assert await theory_cache.get("test_key") is None
        assert await graph_cache.get("test_key") is None
