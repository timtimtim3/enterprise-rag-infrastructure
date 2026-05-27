from typing import List

from app.embeddings.service import EmbeddingService
from app.core.config import EMBEDDING_MODEL


# def retrieve_context(queries: List[str]):
#     embedding_svc = EmbeddingService(EMBEDDING_MODEL)
#     queries_embeddings = embedding_svc.embed(queries)
#     qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
#     resp = qdrant_client.query_points(collection_name=COLLECTION_NAME, query=query_embedding)
