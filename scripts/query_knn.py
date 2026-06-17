import asyncio

from app.llm.client import LLM
from app.rag.embeddings.factory import embedding_provider_factory
from app.rag.reranking.factory import reranker_provider_factory
from app.rag.retriever import Retriever
from app.services.answer_service import AnswerService
from app.core.config import (
    COLLECTION_NAME_PREFIX,
    EMBEDDING_PROVIDER,
    RERANKER_PROVIDER,
    USING_LLM,
)
from app.rag.vectorstores.qdrant_store import init_qdrant, name_qdrant_collection


QUERY = "How does Northstar deploy LangGraph services to ECS?"


async def main() -> None:
    embedding_provider = embedding_provider_factory(EMBEDDING_PROVIDER)
    reranker_provider = reranker_provider_factory(RERANKER_PROVIDER)
    qdrant_collection_name = name_qdrant_collection(COLLECTION_NAME_PREFIX, EMBEDDING_PROVIDER, embedding_provider.model_name)
    qdrant_client = await init_qdrant(qdrant_collection_name)

    retriever = Retriever(embedding_provider, reranker_provider, qdrant_client, qdrant_collection_name)
    llm = LLM(USING_LLM)
    answer_svc = AnswerService(retriever, llm)

    # query_embedding = embedding_provider.embed_query(QUERY)
    # print(query_embedding)

    # resp = qdrant_client.query_points(collection_name=qdrant_collection_name, query=query_embedding)
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
