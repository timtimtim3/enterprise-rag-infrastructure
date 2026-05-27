from qdrant_client import QdrantClient

from app.embeddings.service import EmbeddingService
from app.core.config import (
    COLLECTION_NAME,
    EMBEDDING_MODEL,
    QDRANT_URL,
    QDRANT_API_KEY
)


QUERY = "How does Northstar deploy LangGraph services to ECS?"


def main() -> None:
    embedding_svc = EmbeddingService(EMBEDDING_MODEL)
    query_embedding = embedding_svc.embed([QUERY])[0]
    print(query_embedding)

    qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    resp = qdrant_client.query_points(collection_name=COLLECTION_NAME, query=query_embedding)
    print(resp)


if __name__ == "__main__":
    main()
