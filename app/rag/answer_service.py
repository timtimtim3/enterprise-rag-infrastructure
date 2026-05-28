from __future__ import annotations

from typing import List, TYPE_CHECKING

from app.rag.helpers import format_context_dict_for_llm

if TYPE_CHECKING:
    from app.rag.retriever import Retriever


class AnswerService:
    def __init__(self, retriever: Retriever):
        self.retriever = retriever

    def answer_question(self, query: str):
        context_dicts = self.retriever.retrieve_context(query)
        formatted_sources = []
        for i, context_dict in enumerate(context_dicts):
            formatted_sources.append(format_context_dict_for_llm(context_dict, i))
        formatted_context = "\n".join(formatted_sources)
        return formatted_context
