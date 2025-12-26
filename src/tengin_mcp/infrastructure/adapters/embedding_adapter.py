"""Infrastructure: Embedding Adapter using esperanto for multi-provider support."""

import logging
from typing import Any

from esperanto.factory import AIFactory
from esperanto.providers.embedding.ollama import OllamaEmbeddingModel

from tengin_mcp.infrastructure.config import Settings

logger = logging.getLogger(__name__)


class EmbeddingAdapter:
    """
    マルチプロバイダー対応 Embedding アダプター。

    esperantoライブラリを使用して、以下のプロバイダーをサポート:
    - OpenAI (text-embedding-3-small, text-embedding-3-large, text-embedding-ada-002)
    - OpenAI-Compatible (LM Studio, vLLM, Ollama via OpenAI API)
    - Google (text-embedding-004, embedding-001)
    - Ollama (nomic-embed-text, mxbai-embed-large, all-minilm)
    - Azure OpenAI
    - Mistral (mistral-embed)
    - Voyage (voyage-3, voyage-2, voyage-code-2)
    - Jina (jina-embeddings-v3, jina-embeddings-v2-base-en)
    - Transformers (local models: BAAI/bge-*, sentence-transformers/*)
    """

    # プロバイダーごとのデフォルトモデル
    DEFAULT_MODELS = {
        "openai": "text-embedding-3-small",
        "openai-compatible": "text-embedding-3-small",
        "google": "text-embedding-004",
        "ollama": "nomic-embed-text",
        "vertex": "text-embedding-004",
        "azure": "text-embedding-3-small",
        "mistral": "mistral-embed",
        "voyage": "voyage-3",
        "jina": "jina-embeddings-v3",
        "transformers": "BAAI/bge-small-en-v1.5",
    }

    def __init__(self, settings: Settings) -> None:
        """
        Embeddingアダプターを初期化。

        Args:
            settings: アプリケーション設定
        """
        self._settings = settings
        self._embedder: Any = None
        self._provider = settings.embedding_provider
        self._model = settings.embedding_model or self.DEFAULT_MODELS.get(
            self._provider, "text-embedding-3-small"
        )
        self._is_ollama = self._provider == "ollama"

    def _get_provider_config(self) -> dict[str, Any]:
        """プロバイダー固有の設定を取得。"""
        config: dict[str, Any] = {}

        match self._provider:
            case "openai":
                if self._settings.openai_api_key:
                    config["api_key"] = self._settings.openai_api_key

            case "openai-compatible":
                if self._settings.openai_compatible_base_url:
                    config["base_url"] = self._settings.openai_compatible_base_url
                if self._settings.openai_compatible_api_key:
                    config["api_key"] = self._settings.openai_compatible_api_key

            case "google":
                if self._settings.google_api_key:
                    config["api_key"] = self._settings.google_api_key

            case "ollama":
                if self._settings.ollama_base_url:
                    config["base_url"] = self._settings.ollama_base_url

            case "azure":
                if self._settings.azure_openai_api_key:
                    config["api_key"] = self._settings.azure_openai_api_key
                if self._settings.azure_openai_endpoint:
                    config["azure_endpoint"] = self._settings.azure_openai_endpoint

            case "mistral":
                if self._settings.mistral_api_key:
                    config["api_key"] = self._settings.mistral_api_key

            case "voyage":
                if self._settings.voyage_api_key:
                    config["api_key"] = self._settings.voyage_api_key

            case "jina":
                if self._settings.jina_api_key:
                    config["api_key"] = self._settings.jina_api_key

            case "transformers":
                # transformersはローカルモデルを使用（APIキー不要）
                pass

        return config

    async def connect(self) -> None:
        """Embeddingクライアントを初期化。"""
        try:
            config = self._get_provider_config()

            # Ollamaは直接プロバイダークラスを使用（AIFactoryではbase_urlが正しく渡されない）
            if self._is_ollama:
                base_url = config.get("base_url", "http://localhost:11434")
                self._embedder = OllamaEmbeddingModel(
                    model_name=self._model,
                    base_url=base_url,
                )
                logger.info(
                    f"Ollama Embedding client initialized: model={self._model}, base_url={base_url}"
                )
            else:
                # 他のプロバイダーはAIFactoryを使用
                self._embedder = AIFactory.create_embedding(
                    provider=self._provider,
                    model_name=self._model,
                    config=config if config else None,
                )
                logger.info(
                    f"Embedding client initialized: provider={self._provider}, model={self._model}"
                )

        except Exception as e:
            logger.error(f"Failed to initialize embedding client: {e}")
            raise RuntimeError(f"Embedding initialization failed: {e}") from e

    async def close(self) -> None:
        """クライアントをクローズ。"""
        # esperantoのembedderは明示的なクローズ不要
        self._embedder = None
        logger.info("Embedding client closed")

    @property
    def provider(self) -> str:
        """現在のプロバイダー名を取得。"""
        return self._provider

    @property
    def model(self) -> str:
        """現在のモデル名を取得。"""
        return self._model

    async def embed_text(self, text: str) -> list[float]:
        """
        テキストを埋め込みベクトルに変換。

        Args:
            text: 埋め込むテキスト

        Returns:
            埋め込みベクトル
        """
        if not self._embedder:
            raise RuntimeError("Embedding client not initialized. Call connect() first.")

        if self._is_ollama:
            # Ollamaは同期APIで、list[list[float]]を返す
            result = self._embedder.embed([text])
            return result[0]
        else:
            # 他のプロバイダーは非同期APIでEmbeddingResponseを返す
            response = await self._embedder.aembed([text])
            return response.data[0].embedding

    async def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """
        複数テキストを埋め込みベクトルに変換。

        Args:
            texts: 埋め込むテキストのリスト

        Returns:
            埋め込みベクトルのリスト
        """
        if not self._embedder:
            raise RuntimeError("Embedding client not initialized. Call connect() first.")

        if self._is_ollama:
            # Ollamaは同期APIで、list[list[float]]を返す
            return self._embedder.embed(texts)
        else:
            # 他のプロバイダーは非同期APIでEmbeddingResponseを返す
            response = await self._embedder.aembed(texts)
            return [item.embedding for item in response.data]

    @classmethod
    def get_available_providers(cls) -> list[str]:
        """利用可能なプロバイダー一覧を取得。"""
        providers = AIFactory.get_available_providers()
        return providers.get("embedding", [])

    @classmethod
    def get_provider_models(
        cls,
        provider: str,
        api_key: str | None = None,
        base_url: str | None = None,
    ) -> list[dict[str, Any]]:
        """
        指定プロバイダーで利用可能なモデル一覧を取得。

        Args:
            provider: プロバイダー名
            api_key: APIキー（オプション）
            base_url: ベースURL（openai-compatible用）

        Returns:
            モデル情報のリスト
        """
        try:
            kwargs: dict[str, Any] = {}
            if api_key:
                kwargs["api_key"] = api_key
            if base_url:
                kwargs["base_url"] = base_url

            models = AIFactory.get_provider_models(provider, **kwargs)
            return [{"id": m.id, "owned_by": m.owned_by} for m in models]
        except Exception as e:
            logger.warning(f"Failed to get models for {provider}: {e}")
            return []
