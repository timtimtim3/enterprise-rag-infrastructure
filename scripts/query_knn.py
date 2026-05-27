import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from helpers import EmbeddingService


load_dotenv()


EMBEDDING_MODEL = 'BAAI/bge-small-en-v1.5'
COLLECTION_NAME = "northstar_knowledge_chunks"
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
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
