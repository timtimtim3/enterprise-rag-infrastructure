from qdrant_client import QdrantClient

from app.embeddings.service import EmbeddingService
from app.rag.retriever import Retriever
from app.rag.helpers import format_context_dict_for_llm
from app.core.config import (
    COLLECTION_NAME,
    EMBEDDING_MODEL,
    QDRANT_URL,
    QDRANT_API_KEY
)


QUERY = "How does Northstar deploy LangGraph services to ECS?"


def main() -> None:
    embedding_svc = EmbeddingService(EMBEDDING_MODEL)
    qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    
    # query_embedding = embedding_svc.embed([QUERY])[0]
    # print(query_embedding)

    # resp = qdrant_client.query_points(collection_name=COLLECTION_NAME, query=query_embedding)
    # print(resp.points)
    # for scored_point in resp.points:
    #     print(scored_point.payload['text'])

    retriever = Retriever(embedding_svc, qdrant_client, COLLECTION_NAME)
    context_dicts = retriever.retrieve_context(QUERY)
    print(context_dicts)

    for i, context_dict in enumerate(context_dicts):
        print(format_context_dict_for_llm(context_dict, i))


if __name__ == "__main__":
    main()
