# app/core/config.py
from enum import Enum
import os
from pathlib import Path
from dotenv import load_dotenv

from app.rag.embeddings.providers import EmbeddingProviders
from app.rag.reranking.providers import RerankerProviders


def get_required_env(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise ValueError(f"{key} environment variable is required")
    return value


def get_enum_env(name: str, enum_cls: type[Enum]):
    value = os.getenv(name)

    if not value:
        raise ValueError(f"{name} environment variable is required")

    try:
        return enum_cls(value)
    except ValueError:
        valid_values = ", ".join(member.value for member in enum_cls)
        raise ValueError(
            f"Invalid value for {name}: {value!r}. "
            f"Valid values are: {valid_values}"
        ) from None


load_dotenv()


# Data
DOC_EXTENSIONS = {".md", ".mdx"}
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR_PATH = BASE_DIR / "data/curated"
INGESTION_STATE_PATH = BASE_DIR / "data/processed"

# RAG (Embedding and reranking models)
EMBEDDING_PROVIDER: EmbeddingProviders = get_enum_env(
    "EMBEDDING_PROVIDER",
    EmbeddingProviders,
)
LOCAL_EMBEDDING_MODEL: str = os.getenv("LOCAL_EMBEDDING_MODEL", "BAAI/bge-small-en-v1.5")
VOYAGE_EMBEDDING_MODEL: str = os.getenv("VOYAGE_EMBEDDING_MODEL", None)
VOYAGE_EMBEDDING_BATCH_SIZE: int = int(os.getenv("VOYAGE_EMBEDDING_BATCH_SIZE", 8))
VOYAGE_EMBEDDING_SLEEP_SECONDS: int = int(os.getenv("VOYAGE_EMBEDDING_SLEEP_SECONDS", 25))
VOYAGE_API_KEY: str = os.getenv("VOYAGE_API_KEY", None)

RERANKER_PROVIDER: RerankerProviders = get_enum_env(
    "RERANKER_PROVIDER",
    RerankerProviders,
)
LOCAL_RERANKER_MODEL: str = os.getenv("LOCAL_RERANKER_MODEL", "BAAI/bge-reranker-v2-m3")
COHERE_RERANKER_MODEL: str = os.getenv("COHERE_RERANKER_MODEL", None)
COHERE_API_KEY: str = os.getenv("COHERE_API_KEY", None)

# Qdrant
COLLECTION_NAME_PREFIX = "northstar-knowledge-chunks"
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

# Retrieval settings
INITIAL_TOP_K = 20
FINAL_TOP_K = 5
MIN_REQUIRED = 3
REL_SCORE_THRESH = 0.1
MIN_CHUNK_CHARS = 80
EXPAND_WINDOW_BEFORE = 1
EXPAND_WINDOW_AFTER = 3
KEEP_ENTIRE_DOC_CHUNK_THRESH = 6

# LLM settings
USE_LOCAL_LLM = os.getenv("USE_LOCAL_LLM", "true").lower() == "true"
LOCAL_LLM = "ollama/qwen3:0.6b"
CLOUD_LLM = "openai/gpt-4.1-mini"
USING_LLM = LOCAL_LLM if USE_LOCAL_LLM else CLOUD_LLM
ROUTER_HISTORY_TOKEN_BUDGET = 2_000
ANSWER_HISTORY_TOKEN_BUDGET = 3_000

# DB
DATABASE_URL = os.getenv("DATABASE_URL", "default")
ALEMBIC_DATABASE_URL = os.getenv("ALEMBIC_DATABASE_URL", "default")
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL", "default")

# Redis
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Security
DUMMY_PASSWORD_HASH = os.getenv("DUMMY_PASSWORD_HASH")
SESSION_EXPIRE_SECONDS = int(os.getenv("SESSION_EXPIRE_SECONDS", 60 * 60 * 24))  # 24 hours

# JWT
REFRESH_TOKEN_EXPIRE_SECONDS = int(os.getenv("REFRESH_TOKEN_EXPIRE_SECONDS", 60 * 60 * 24 * 7))  # 7 days
ACCESS_TOKEN_EXPIRE_SECONDS = int(os.getenv("ACCESS_TOKEN_EXPIRE_SECONDS", 60 * 15))  # 15 minutes
JWT_SECRET_KEY = get_required_env("JWT_SECRET_KEY")
JWT_ALGORITHM = "HS256"

# Cookie settings
COOKIE_SECURE = os.getenv("COOKIE_SECURE", "false").lower() == "true"
