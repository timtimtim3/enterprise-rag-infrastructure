from langchain_core.tools import tool

from app.rag.helpers import format_sources


def build_knowledge_tools(retriever):

    @tool(response_format="content_and_artifact")
    async def search_company_knowledge(query: str):
        """
        Search Northstar's internal knowledge base.

        Use this for company-specific policies, procedures, project
        documentation, architecture, runbooks, and internal knowledge.
        """

        all_docs = await retriever.retrieve_context(query)

        if not all_docs:
            return (
                "No relevant internal sources were found.",
                {
                    "status": "not_found",
                    "query": query,
                    "sources": [],
                },
            )

        formatted_context, sources = format_sources(
            all_docs
        )

        return (
            formatted_context,
            {
                "status": "found",
                "query": query,
                "sources": sources,
            },
        )

    return [search_company_knowledge]