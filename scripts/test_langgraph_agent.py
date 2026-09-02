import asyncio
from pprint import pprint

from langchain_core.messages import AIMessage, HumanMessage, ToolMessage

from app.agents.graph import build_agent_graph
from app.agents.state import AgentContext
from app.db.session import SessionLocal
from app.llm.client import LLM
from app.rag.embeddings.factory import embedding_provider_factory
from app.rag.reranking.factory import reranker_provider_factory
from app.rag.retriever import Retriever
from app.core.config import (
    COLLECTION_NAME_PREFIX,
    EMBEDDING_PROVIDER,
    RERANKER_PROVIDER,
    USING_LLM,
)
from app.rag.vectorstores.qdrant_store import init_qdrant, name_qdrant_collection


def print_trajectory(messages):
    print("\n--- AGENT TRAJECTORY ---")

    for i, message in enumerate(messages, start=1):
        print(f"\n[{i}] {type(message).__name__}")

        if isinstance(message, HumanMessage):
            print(f"User: {message.content}")

        elif isinstance(message, AIMessage):
            if message.tool_calls:
                print("Tool calls:")
                for call in message.tool_calls:
                    print(f"  → {call['name']}")
                    pprint(call["args"])
            else:
                print(f"Assistant: {message.content}")

        elif isinstance(message, ToolMessage):
            print(f"Tool: {message.name}")
            print(f"Result: {message.content}")

        else:
            print(message)


async def run_case(graph, query: str):
    print("\n" + "=" * 80)
    print(f"QUERY: {query}")
    print("=" * 80)

    result = await graph.ainvoke(
        {
            "messages": [
                HumanMessage(content=query)
            ],
            "tool_iterations": 0,
            "tool_history": [],
            "user_id": "test_user",
            "source_registry": {},
        },
        context=AgentContext(
            user_id="test-user",
            db_session_factory=SessionLocal,
        ),
    )

    print_trajectory(result["messages"])

    print("\n--- FINAL ANSWER ---")
    print(result["messages"][-1].content)

    print("\n--- TOOL HISTORY ---")
    pprint(result.get("tool_history", []))

    print("\nTool iterations:", result.get("tool_iterations", 0))

    sources = sorted(
        result["source_registry"].values(),
        key=lambda source: source["source_index"],
    )


async def main():
    llm = LLM(model_name=USING_LLM)

    embedding_provider = embedding_provider_factory(EMBEDDING_PROVIDER)
    reranker_provider = reranker_provider_factory(RERANKER_PROVIDER)
    qdrant_collection_name = name_qdrant_collection(COLLECTION_NAME_PREFIX, EMBEDDING_PROVIDER, embedding_provider.model_name)
    qdrant_client = await init_qdrant(qdrant_collection_name)
    retriever = Retriever(embedding_provider, reranker_provider, qdrant_client, qdrant_collection_name)

    graph = build_agent_graph(
        llm=llm,
        retriever=retriever,
    )

    # test_queries = [
    #     # Direct answer — should use no tools
    #     "Explain what dependency injection is in Python.",

    #     # Single tool
    #     "Which Northstar employee knows LangGraph?",

    #     # Sequential tools
    #     "What projects do we have with ACME?",

    #     # Ambiguity
    #     "What project is John currently working on?",

    #     # RAG
    #     "What is Northstar's remote working policy?",
    # ]

    test_queries = [
        # RAG
        # "Why did we migrate from Pinecone if pgvector was also evaluated?",

        # Employee lookup
        "Does John still work for us?",
        "Who is John Smith?",
        "What skills does Alice Jansen have?",
        "Who is our most experienced Python expert?",
    ]

    for query in test_queries:
        await run_case(graph, query)


if __name__ == "__main__":
    asyncio.run(main())
