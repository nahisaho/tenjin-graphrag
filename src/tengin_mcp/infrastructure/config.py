"""Infrastructure: Configuration."""

from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# サポートされる埋め込みプロバイダー
EmbeddingProvider = Literal[
    "openai",
    "openai-compatible",
    "google",
    "ollama",
    "vertex",
    "azure",
    "mistral",
    "voyage",
    "jina",
    "transformers",
]


class Settings(BaseSettings):
    """アプリケーション設定。"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Neo4j Configuration
    neo4j_uri: str = Field(default="bolt://localhost:7687", alias="NEO4J_URI")
    neo4j_user: str = Field(default="neo4j", alias="NEO4J_USER")
    neo4j_password: str = Field(default="password", alias="NEO4J_PASSWORD")

    # ChromaDB Configuration
    chromadb_path: str = Field(default="./data/chromadb", alias="CHROMADB_PATH")

    # Embedding Provider Configuration (using esperanto)
    embedding_provider: EmbeddingProvider = Field(default="openai", alias="EMBEDDING_PROVIDER")
    embedding_model: str = Field(default="text-embedding-3-small", alias="EMBEDDING_MODEL")

    # Provider-specific API Keys (esperanto will use these)
    openai_api_key: str = Field(default="", alias="OPENAI_API_KEY")
    anthropic_api_key: str = Field(default="", alias="ANTHROPIC_API_KEY")
    google_api_key: str = Field(default="", alias="GOOGLE_API_KEY")
    mistral_api_key: str = Field(default="", alias="MISTRAL_API_KEY")
    voyage_api_key: str = Field(default="", alias="VOYAGE_API_KEY")
    jina_api_key: str = Field(default="", alias="JINA_API_KEY")
    azure_openai_api_key: str = Field(default="", alias="AZURE_OPENAI_API_KEY")
    azure_openai_endpoint: str = Field(default="", alias="AZURE_OPENAI_ENDPOINT")

    # OpenAI-Compatible Endpoints (LM Studio, vLLM, etc.)
    openai_compatible_base_url: str = Field(default="", alias="OPENAI_COMPATIBLE_BASE_URL")
    openai_compatible_api_key: str = Field(default="", alias="OPENAI_COMPATIBLE_API_KEY")

    # Ollama Configuration (local models)
    ollama_base_url: str = Field(default="http://localhost:11434", alias="OLLAMA_BASE_URL")

    # Server Configuration
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")


# Singleton instance
_settings: Settings | None = None


def get_settings() -> Settings:
    """設定のシングルトンインスタンスを取得。"""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
