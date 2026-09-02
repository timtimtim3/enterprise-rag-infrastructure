from langchain_core.tools import tool


def build_knowledge_tools(retriever):

    @tool(response_format="content_and_artifact")
    async def search_company_knowledge(query: str):
        """
        Search the company's internal knowledge base.

        Use this for company-specific policies, procedures, project
        documentation, architecture, runbooks, technical documentation,
        internal processes, and other company knowledge.

        The query should be a concise standalone semantic search query.
        """

        all_docs = await retriever.retrieve_context(query)

        if not all_docs:
            return (
                "No relevant internal sources were found.",
                {
                    "status": "not_found",
                    "query": query,
                    "all_docs": {},
                },
            )

        return (
            "Internal knowledge sources were retrieved.",
            {
                "status": "found",
                "query": query,
                "all_docs": all_docs,
            },
        )

    return [search_company_knowledge]
