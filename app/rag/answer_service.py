from __future__ import annotations

from typing import TYPE_CHECKING

from app.rag.helpers import format_context_dict_for_llm, format_context_dict_for_llm_doc_chunks

if TYPE_CHECKING:
    from app.rag.retriever import Retriever


class AnswerService:
    def __init__(self, retriever: Retriever):
        self.retriever = retriever

    def answer_question(self, query: str):
        context_dicts = self.retriever.retrieve_context(query)
        formatted_sources = []
        last_doc_id = None
        source_index = 0
        for context_dict in context_dicts:
            doc_id = context_dict["doc_id"]

            # If not the same, it's the first chunk of doc, we display full context / meta
            if doc_id != last_doc_id:
                formatted_sources.append(format_context_dict_for_llm(context_dict, source_index))
                last_doc_id = doc_id
                source_index += 1
            else:
                # Otherwise we only display the text and chunk_i
                formatted_sources.append(format_context_dict_for_llm_doc_chunks(context_dict))
        formatted_context = "\n\n".join(formatted_sources)
        return formatted_context
