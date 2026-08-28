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

        context_dicts = await retriever.retrieve_context(query)

        if not context_dicts:
            return (
                "No relevant internal sources were found.",
                {
                    "status": "not_found",
                    "query": query,
                    "sources": [],
                },
            )

        formatted_context, sources = format_sources(
            context_dicts
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