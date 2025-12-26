"""Unit Tests: embedding_adapter - 埋め込みアダプターのユニットテスト"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch


def create_mock_settings(**kwargs):
    """テスト用のモックSettings作成"""
    settings = MagicMock()
    settings.embedding_provider = kwargs.get("embedding_provider", "openai")
    settings.embedding_model = kwargs.get("embedding_model", None)
    settings.openai_api_key = kwargs.get("openai_api_key", "")
    settings.google_api_key = kwargs.get("google_api_key", "")
    settings.mistral_api_key = kwargs.get("mistral_api_key", "")
    settings.voyage_api_key = kwargs.get("voyage_api_key", "")
    settings.jina_api_key = kwargs.get("jina_api_key", "")
    settings.azure_openai_api_key = kwargs.get("azure_openai_api_key", "")
    settings.azure_openai_endpoint = kwargs.get("azure_openai_endpoint", "")
    settings.ollama_base_url = kwargs.get("ollama_base_url", "http://localhost:11434")
    settings.openai_compatible_base_url = kwargs.get("openai_compatible_base_url", "")
    settings.openai_compatible_api_key = kwargs.get("openai_compatible_api_key", "")
    return settings


class TestEmbeddingAdapterInit:
    """EmbeddingAdapterの初期化テスト"""

    def test_default_model_selection(self):
        """デフォルトモデルの選択"""
        from tengin_mcp.infrastructure.adapters.embedding_adapter import EmbeddingAdapter

        # 各プロバイダーのデフォルトモデル
        expected_defaults = {
            "openai": "text-embedding-3-small",
            "google": "text-embedding-004",
            "ollama": "nomic-embed-text",
            "mistral": "mistral-embed",
            "voyage": "voyage-3",
            "jina": "jina-embeddings-v3",
        }

        for provider, expected_model in expected_defaults.items():
            settings = create_mock_settings(embedding_provider=provider, embedding_model=None)
            adapter = EmbeddingAdapter(settings)
            assert adapter._model == expected_model

    def test_custom_model_selection(self):
        """カスタムモデルの選択"""
        from tengin_mcp.infrastructure.adapters.embedding_adapter import EmbeddingAdapter

        settings = create_mock_settings(
            embedding_provider="openai",
            embedding_model="text-embedding-3-large"
        )
        adapter = EmbeddingAdapter(settings)
        assert adapter._model == "text-embedding-3-large"

    def test_ollama_provider_flag(self):
        """Ollamaプロバイダーのフラグ設定"""
        from tengin_mcp.infrastructure.adapters.embedding_adapter import EmbeddingAdapter

        settings = create_mock_settings(embedding_provider="ollama")
        adapter = EmbeddingAdapter(settings)
        assert adapter._is_ollama is True

        settings2 = create_mock_settings(embedding_provider="openai")
        adapter2 = EmbeddingAdapter(settings2)
        assert adapter2._is_ollama is False


class TestEmbeddingAdapterProviderConfig:
    """プロバイダー設定のテスト"""

    def test_openai_config(self):
        """OpenAI設定の取得"""
        from tengin_mcp.infrastructure.adapters.embedding_adapter import EmbeddingAdapter

        settings = create_mock_settings(
            embedding_provider="openai",
            openai_api_key="test-api-key"
        )
        adapter = EmbeddingAdapter(settings)
        config = adapter._get_provider_config()

        assert config["api_key"] == "test-api-key"

    def test_openai_compatible_config(self):
        """OpenAI互換設定の取得"""
        from tengin_mcp.infrastructure.adapters.embedding_adapter import EmbeddingAdapter

        settings = create_mock_settings(
            embedding_provider="openai-compatible",
            openai_compatible_base_url="http://localhost:8080",
            openai_compatible_api_key="test-key"
        )
        adapter = EmbeddingAdapter(settings)
        config = adapter._get_provider_config()

        assert config["base_url"] == "http://localhost:8080"
        assert config["api_key"] == "test-key"

    def test_google_config(self):
        """Google設定の取得"""
        from tengin_mcp.infrastructure.adapters.embedding_adapter import EmbeddingAdapter

        settings = create_mock_settings(
            embedding_provider="google",
            google_api_key="google-api-key"
        )
        adapter = EmbeddingAdapter(settings)
        config = adapter._get_provider_config()

        assert config["api_key"] == "google-api-key"

    def test_ollama_config(self):
        """Ollama設定の取得"""
        from tengin_mcp.infrastructure.adapters.embedding_adapter import EmbeddingAdapter

        settings = create_mock_settings(
            embedding_provider="ollama",
            ollama_base_url="http://localhost:11434"
        )
        adapter = EmbeddingAdapter(settings)
        config = adapter._get_provider_config()

        assert config["base_url"] == "http://localhost:11434"

    def test_azure_config(self):
        """Azure設定の取得"""
        from tengin_mcp.infrastructure.adapters.embedding_adapter import EmbeddingAdapter

        settings = create_mock_settings(
            embedding_provider="azure",
            azure_openai_api_key="azure-key",
            azure_openai_endpoint="https://example.openai.azure.com"
        )
        adapter = EmbeddingAdapter(settings)
        config = adapter._get_provider_config()

        assert config["api_key"] == "azure-key"
        assert config["azure_endpoint"] == "https://example.openai.azure.com"

    def test_mistral_config(self):
        """Mistral設定の取得"""
        from tengin_mcp.infrastructure.adapters.embedding_adapter import EmbeddingAdapter

        settings = create_mock_settings(
            embedding_provider="mistral",
            mistral_api_key="mistral-key"
        )
        adapter = EmbeddingAdapter(settings)
        config = adapter._get_provider_config()

        assert config["api_key"] == "mistral-key"

    def test_voyage_config(self):
        """Voyage設定の取得"""
        from tengin_mcp.infrastructure.adapters.embedding_adapter import EmbeddingAdapter

        settings = create_mock_settings(
            embedding_provider="voyage",
            voyage_api_key="voyage-key"
        )
        adapter = EmbeddingAdapter(settings)
        config = adapter._get_provider_config()

        assert config["api_key"] == "voyage-key"

    def test_jina_config(self):
        """Jina設定の取得"""
        from tengin_mcp.infrastructure.adapters.embedding_adapter import EmbeddingAdapter

        settings = create_mock_settings(
            embedding_provider="jina",
            jina_api_key="jina-key"
        )
        adapter = EmbeddingAdapter(settings)
        config = adapter._get_provider_config()

        assert config["api_key"] == "jina-key"

    def test_transformers_config(self):
        """Transformers設定の取得（APIキー不要）"""
        from tengin_mcp.infrastructure.adapters.embedding_adapter import EmbeddingAdapter

        settings = create_mock_settings(embedding_provider="transformers")
        adapter = EmbeddingAdapter(settings)
        config = adapter._get_provider_config()

        assert config == {}


class TestEmbeddingAdapterProperties:
    """プロパティのテスト"""

    def test_provider_property(self):
        """プロバイダープロパティ"""
        from tengin_mcp.infrastructure.adapters.embedding_adapter import EmbeddingAdapter

        settings = create_mock_settings(embedding_provider="openai")
        adapter = EmbeddingAdapter(settings)
        assert adapter.provider == "openai"

    def test_model_property(self):
        """モデルプロパティ"""
        from tengin_mcp.infrastructure.adapters.embedding_adapter import EmbeddingAdapter

        settings = create_mock_settings(
            embedding_provider="openai",
            embedding_model="text-embedding-3-large"
        )
        adapter = EmbeddingAdapter(settings)
        assert adapter.model == "text-embedding-3-large"


class TestEmbeddingAdapterConnection:
    """接続/切断のテスト"""

    @pytest.mark.asyncio
    async def test_connect_ollama(self):
        """Ollama接続のテスト"""
        from tengin_mcp.infrastructure.adapters.embedding_adapter import EmbeddingAdapter

        settings = create_mock_settings(
            embedding_provider="ollama",
            ollama_base_url="http://localhost:11434"
        )
        adapter = EmbeddingAdapter(settings)

        with patch('tengin_mcp.infrastructure.adapters.embedding_adapter.OllamaEmbeddingModel') as mock_ollama:
            mock_instance = MagicMock()
            mock_ollama.return_value = mock_instance

            await adapter.connect()

            mock_ollama.assert_called_once_with(
                model_name="nomic-embed-text",
                base_url="http://localhost:11434",
            )
            assert adapter._embedder == mock_instance

    @pytest.mark.asyncio
    async def test_connect_other_provider(self):
        """他プロバイダー接続のテスト"""
        from tengin_mcp.infrastructure.adapters.embedding_adapter import EmbeddingAdapter

        settings = create_mock_settings(
            embedding_provider="openai",
            openai_api_key="test-key"
        )
        adapter = EmbeddingAdapter(settings)

        with patch('tengin_mcp.infrastructure.adapters.embedding_adapter.AIFactory') as mock_factory:
            mock_embedder = MagicMock()
            mock_factory.create_embedding.return_value = mock_embedder

            await adapter.connect()

            mock_factory.create_embedding.assert_called_once()
            assert adapter._embedder == mock_embedder

    @pytest.mark.asyncio
    async def test_connect_failure(self):
        """接続失敗のテスト"""
        from tengin_mcp.infrastructure.adapters.embedding_adapter import EmbeddingAdapter

        settings = create_mock_settings(
            embedding_provider="openai",
            openai_api_key="test-key"
        )
        adapter = EmbeddingAdapter(settings)

        with patch('tengin_mcp.infrastructure.adapters.embedding_adapter.AIFactory') as mock_factory:
            mock_factory.create_embedding.side_effect = Exception("Connection failed")

            with pytest.raises(RuntimeError, match="Embedding initialization failed"):
                await adapter.connect()

    @pytest.mark.asyncio
    async def test_close(self):
        """クローズのテスト"""
        from tengin_mcp.infrastructure.adapters.embedding_adapter import EmbeddingAdapter

        settings = create_mock_settings(embedding_provider="openai")
        adapter = EmbeddingAdapter(settings)
        adapter._embedder = MagicMock()

        await adapter.close()

        assert adapter._embedder is None


class TestEmbeddingAdapterEmbed:
    """埋め込み処理のテスト"""

    @pytest.mark.asyncio
    async def test_embed_text_not_initialized(self):
        """初期化前の埋め込みでエラー"""
        from tengin_mcp.infrastructure.adapters.embedding_adapter import EmbeddingAdapter

        settings = create_mock_settings(embedding_provider="openai")
        adapter = EmbeddingAdapter(settings)

        with pytest.raises(RuntimeError, match="Embedding client not initialized"):
            await adapter.embed_text("test")

    @pytest.mark.asyncio
    async def test_embed_texts_not_initialized(self):
        """初期化前の複数埋め込みでエラー"""
        from tengin_mcp.infrastructure.adapters.embedding_adapter import EmbeddingAdapter

        settings = create_mock_settings(embedding_provider="openai")
        adapter = EmbeddingAdapter(settings)

        with pytest.raises(RuntimeError, match="Embedding client not initialized"):
            await adapter.embed_texts(["test1", "test2"])

    @pytest.mark.asyncio
    async def test_embed_text_ollama(self):
        """Ollamaでの単一埋め込み"""
        from tengin_mcp.infrastructure.adapters.embedding_adapter import EmbeddingAdapter

        settings = create_mock_settings(embedding_provider="ollama")
        adapter = EmbeddingAdapter(settings)
        adapter._embedder = MagicMock()
        adapter._embedder.embed.return_value = [[0.1, 0.2, 0.3]]

        result = await adapter.embed_text("test text")

        adapter._embedder.embed.assert_called_once_with(["test text"])
        assert result == [0.1, 0.2, 0.3]

    @pytest.mark.asyncio
    async def test_embed_texts_ollama(self):
        """Ollamaでの複数埋め込み"""
        from tengin_mcp.infrastructure.adapters.embedding_adapter import EmbeddingAdapter

        settings = create_mock_settings(embedding_provider="ollama")
        adapter = EmbeddingAdapter(settings)
        adapter._embedder = MagicMock()
        adapter._embedder.embed.return_value = [[0.1, 0.2], [0.3, 0.4]]

        result = await adapter.embed_texts(["text1", "text2"])

        adapter._embedder.embed.assert_called_once_with(["text1", "text2"])
        assert result == [[0.1, 0.2], [0.3, 0.4]]

    @pytest.mark.asyncio
    async def test_embed_text_other_provider(self):
        """他プロバイダーでの単一埋め込み"""
        from tengin_mcp.infrastructure.adapters.embedding_adapter import EmbeddingAdapter

        settings = create_mock_settings(embedding_provider="openai")
        adapter = EmbeddingAdapter(settings)

        # モックレスポンス
        mock_data = MagicMock()
        mock_data.embedding = [0.1, 0.2, 0.3]
        mock_response = MagicMock()
        mock_response.data = [mock_data]

        adapter._embedder = AsyncMock()
        adapter._embedder.aembed.return_value = mock_response

        result = await adapter.embed_text("test text")

        adapter._embedder.aembed.assert_called_once_with(["test text"])
        assert result == [0.1, 0.2, 0.3]

    @pytest.mark.asyncio
    async def test_embed_texts_other_provider(self):
        """他プロバイダーでの複数埋め込み"""
        from tengin_mcp.infrastructure.adapters.embedding_adapter import EmbeddingAdapter

        settings = create_mock_settings(embedding_provider="openai")
        adapter = EmbeddingAdapter(settings)

        # モックレスポンス
        mock_data1 = MagicMock()
        mock_data1.embedding = [0.1, 0.2]
        mock_data2 = MagicMock()
        mock_data2.embedding = [0.3, 0.4]
        mock_response = MagicMock()
        mock_response.data = [mock_data1, mock_data2]

        adapter._embedder = AsyncMock()
        adapter._embedder.aembed.return_value = mock_response

        result = await adapter.embed_texts(["text1", "text2"])

        adapter._embedder.aembed.assert_called_once_with(["text1", "text2"])
        assert result == [[0.1, 0.2], [0.3, 0.4]]


class TestEmbeddingAdapterClassMethods:
    """クラスメソッドのテスト"""

    def test_get_available_providers(self):
        """利用可能なプロバイダー一覧"""
        from tengin_mcp.infrastructure.adapters.embedding_adapter import EmbeddingAdapter

        with patch('tengin_mcp.infrastructure.adapters.embedding_adapter.AIFactory') as mock_factory:
            mock_factory.get_available_providers.return_value = {
                "embedding": ["openai", "google", "ollama"]
            }

            providers = EmbeddingAdapter.get_available_providers()

            assert providers == ["openai", "google", "ollama"]

    def test_get_provider_models(self):
        """プロバイダーモデル一覧"""
        from tengin_mcp.infrastructure.adapters.embedding_adapter import EmbeddingAdapter

        with patch('tengin_mcp.infrastructure.adapters.embedding_adapter.AIFactory') as mock_factory:
            mock_model1 = MagicMock()
            mock_model1.id = "model1"
            mock_model1.owned_by = "openai"
            mock_model2 = MagicMock()
            mock_model2.id = "model2"
            mock_model2.owned_by = "openai"

            mock_factory.get_provider_models.return_value = [mock_model1, mock_model2]

            models = EmbeddingAdapter.get_provider_models("openai", api_key="test-key")

            mock_factory.get_provider_models.assert_called_once_with(
                "openai", api_key="test-key"
            )
            assert models == [
                {"id": "model1", "owned_by": "openai"},
                {"id": "model2", "owned_by": "openai"},
            ]

    def test_get_provider_models_with_base_url(self):
        """ベースURL付きでプロバイダーモデル一覧"""
        from tengin_mcp.infrastructure.adapters.embedding_adapter import EmbeddingAdapter

        with patch('tengin_mcp.infrastructure.adapters.embedding_adapter.AIFactory') as mock_factory:
            mock_factory.get_provider_models.return_value = []

            models = EmbeddingAdapter.get_provider_models(
                "openai-compatible",
                api_key="test-key",
                base_url="http://localhost:8080",
            )

            mock_factory.get_provider_models.assert_called_once_with(
                "openai-compatible",
                api_key="test-key",
                base_url="http://localhost:8080",
            )

    def test_get_provider_models_failure(self):
        """プロバイダーモデル取得失敗"""
        from tengin_mcp.infrastructure.adapters.embedding_adapter import EmbeddingAdapter

        with patch('tengin_mcp.infrastructure.adapters.embedding_adapter.AIFactory') as mock_factory:
            mock_factory.get_provider_models.side_effect = Exception("API Error")

            models = EmbeddingAdapter.get_provider_models("unknown")

            assert models == []
