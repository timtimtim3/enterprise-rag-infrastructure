# app/core/config.py
import os
from pathlib import Path
from dotenv import load_dotenv


load_dotenv()


# Data
DOC_EXTENSIONS = {".md", ".mdx"}
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR_PATH = BASE_DIR / "data/curated"
INGESTION_STATE_PATH = BASE_DIR / "data/processed/ingestion_state.json"

# RAG (Embedding and reranking models)
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
RERANKER_MODEL = "BAAI/bge-reranker-v2-m3"

# Qdrant
COLLECTION_NAME = "northstar_knowledge_chunks"
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
USE_LOCAL_LLM = os.getenv("USE_LOCAL_LLM")
LOCAL_LLM = "ollama/qwen3:0.6b"
CLOUD_LLM = "openai/gpt-4.1-mini"
USING_LLM = LOCAL_LLM if USE_LOCAL_LLM else CLOUD_LLM

# DB
DATABASE_URL = os.getenv("DATABASE_URL", "default")
ALEMBIC_DATABASE_URL = os.getenv("ALEMBIC_DATABASE_URL", "default")

# Security
DUMMY_PASSWORD = os.getenv("DUMMY_PASSWORD")
SESSION_EXPIRE_SECONDS = int(os.getenv("SESSION_EXPIRE_SECONDS", 60 * 60))