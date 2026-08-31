import asyncio

from langchain_core.messages import HumanMessage

from app.agents.graph import build_agent_graph
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
    
    agent_graph = build_agent_graph(
        llm=llm,
        retriever=retriever,
    )

    # query_embedding = embedding_provider.embed_query(QUERY)
    # print(query_embedding)

    # resp = qdrant_client.query_points(collection_name=qdrant_collection_name, query=query_embedding)
    # print(resp.points)
    # for scored_point in resp.points:
    #     print(scored_point.payload['text'])

    # all_docs = await retriever.retrieve_context(QUERY, expand=False)

    # for doc_id, chunks in all_docs.items():
    #     print(doc_id)
    #     for chunk in chunks:
    #         print(chunk["id"], chunk["chunk_index"])
    #     print()

    # answer = await answer_svc.answer_question(QUERY)
    # print(answer)

    result = await agent_graph.ainvoke(
        {
            "messages": [
                HumanMessage(content=QUERY),
            ],
            "tool_iterations": 0,
            "tool_history": [],
            "source_registry": {},
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
        }
    )
    final_message = result["messages"][-1]
    answer_text = final_message.content
    print(answer_text)


if __name__ == "__main__":
    asyncio.run(main())
