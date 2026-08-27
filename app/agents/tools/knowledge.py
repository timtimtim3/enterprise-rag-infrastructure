from langchain_core.tools import tool


def build_knowledge_tools(retriever):

    @tool
    async def search_company_knowledge(query: str) -> dict:
        """
        Search Northstar's internal knowledge base.

        Use this for Northstar-specific policies, procedures, project
        documentation, architecture, runbooks, technical documentation,
        internal processes, and other company knowledge.

        The query should be a concise standalone semantic search query.
        """

        context_dicts = await retriever.retrieve_context(query)

        if not context_dicts:
            return {
                "status": "not_found",
                "query": query,
                "sources": [],
            }

        # Starting point. We can improve formatting next.
        sources = [
            {
                "source_index": i,
                "title": item["title"],
                "text": item.get("text"),
                "source_path": item["source_path"],
                "doc_id": item["doc_id"],
                "chunk_index": item["chunk_index"],
            }
            for i, item in enumerate(context_dicts)
        ]

        return {
            "status": "found",
            "query": query,
            "sources": sources,
        }

    return [search_company_knowledge]