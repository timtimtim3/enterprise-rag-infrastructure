import yaml
import hashlib
from sentence_transformers import SentenceTransformer
from typing import List


class EmbeddingService:
    def __init__(self, model_name: str):
        self.model = SentenceTransformer(model_name)

    def embed(self, chunk_texts: List[str]) -> List[List[float]]:
        return self.model.encode(chunk_texts, normalize_embeddings=True, batch_size=32)


def strip_existing_frontmatter(text: str) -> str:
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            return parts[2].lstrip()
    return text


def content_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


def frontmatter_from_metadata(metadata: dict) -> str:
    yaml_text = yaml.safe_dump(
        metadata,
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
    )
    return f"---\n{yaml_text}---\n\n"
