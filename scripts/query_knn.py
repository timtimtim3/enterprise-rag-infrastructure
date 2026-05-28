from qdrant_client import QdrantClient

from app.models.models import EmbeddingService, Reranker
from app.rag.retriever import Retriever
from app.rag.answer_service import AnswerService
from app.rag.helpers import format_context_dict_for_llm
from app.core.config import (
    COLLECTION_NAME,
    EMBEDDING_MODEL,
    RERANKER_MODEL,
    QDRANT_URL,
    QDRANT_API_KEY
)


QUERY = "How does Northstar deploy LangGraph services to ECS?"


def main() -> None:
    embedding_svc = EmbeddingService(EMBEDDING_MODEL)
    qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    reranker = Reranker(RERANKER_MODEL)
    retriever = Retriever(embedding_svc, reranker, qdrant_client, COLLECTION_NAME)
    answer_svc = AnswerService(retriever)

    # query_embedding = embedding_svc.embed([QUERY])[0]
    # print(query_embedding)

    # resp = qdrant_client.query_points(collection_name=COLLECTION_NAME, query=query_embedding)
    # print(resp.points)
    # for scored_point in resp.points:
    #     print(scored_point.payload['text'])

    # context_dicts = retriever.retrieve_context(QUERY)
    # print(context_dicts)
    # print(retriever.rerank_context_dicts(QUERY, context_dicts))
    # for i, context_dict in enumerate(context_dicts):
    #     print(format_context_dict_for_llm(context_dict, i))

    print(answer_svc.answer_question(QUERY))


if __name__ == "__main__":
    main()
