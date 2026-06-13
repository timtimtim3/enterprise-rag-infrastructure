import asyncio

from app.llm.client import LLM
from app.rag.embeddings.local import LocalEmbeddingProvider
from app.rag.reranking.local import LocalRerankerProvider
from app.rag.retriever import Retriever
from app.services.answer_service import AnswerService
from app.rag.helpers import format_context_dict_for_llm
from app.core.config import (
    COLLECTION_NAME_PREFIX,
    LOCAL_EMBEDDING_MODEL,
    LOCAL_RERANKER_MODEL,
    USING_LLM,
)
from app.rag.vectorstores.qdrant_store import init_qdrant


QUERY = "How does Northstar deploy LangGraph services to ECS?"


async def main() -> None:
    embedding_svc = LocalEmbeddingProvider(LOCAL_EMBEDDING_MODEL)
    qdrant_client = await init_qdrant()
    reranker = LocalRerankerProvider(LOCAL_RERANKER_MODEL)
    retriever = Retriever(embedding_svc, reranker, qdrant_client, COLLECTION_NAME_PREFIX)
    llm = LLM(USING_LLM)
    answer_svc = AnswerService(retriever, llm)

    # query_embedding = embedding_svc.embed_query(QUERY)
    # print(query_embedding)

    # resp = qdrant_client.query_points(collection_name=COLLECTION_NAME_PREFIX, query=query_embedding)
    # print(resp.points)
    # for scored_point in resp.points:
    #     print(scored_point.payload['text'])

    # context_dicts = retriever.retrieve_context(QUERY)
    # print(context_dicts)
    # print(retriever.rerank_context_dicts(QUERY, context_dicts))
    # for i, context_dict in enumerate(context_dicts):
    #     print(format_context_dict_for_llm(context_dict, i))

    answer = await answer_svc.answer_question(QUERY)
    print(answer)


if __name__ == "__main__":
    asyncio.run(main())
