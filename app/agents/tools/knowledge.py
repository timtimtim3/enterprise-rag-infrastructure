from langchain_core.tools import tool


def build_knowledge_tools(retriever):

    @tool(response_format="content_and_artifact")
    async def search_company_knowledge(query: str):
        """
        Search the company's internal knowledge base.

        Use this for information contained in documents such as policies,
        procedures, architecture decision records, standards, runbooks,
        technical documentation, historical decisions, and project documentation.

        Do not use this as the first choice for structured operational facts about
        employees, customers, projects, project teams, assignments, or skills when
        a dedicated structured-data tool is available.
        
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
