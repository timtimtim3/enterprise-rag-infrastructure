from __future__ import annotations

from typing import TYPE_CHECKING

from app.domain.enums.llm_route import LLMRoute
from app.rag.helpers import format_context_dict_for_llm, format_context_dict_for_llm_doc_chunks
from app.prompts.rag import RAG_SYSTEM_MESSAGE, format_rag_user_query_message

if TYPE_CHECKING:
    from app.rag.retriever import Retriever
    from app.llm.client import LLM


class AnswerService:
    def __init__(self, retriever: Retriever, llm: LLM):
        self.retriever = retriever
        self.llm = llm

    def answer_question(self, query: str):
        context_dicts = self.retriever.retrieve_context(query)
        formatted_sources = []
        last_doc_id = None
        source_index = 0
        sources = []
        for context_dict in context_dicts:
            doc_id = context_dict["doc_id"]

            # If not the same, it's the first chunk of doc, we display full context / meta
            if doc_id != last_doc_id:
                formatted_sources.append(format_context_dict_for_llm(context_dict, source_index))
                sources.append(
                    {
                        "source_index": source_index,
                        "title": context_dict["title"],
                        "source_path": context_dict["source_path"],
                        "doc_id": doc_id,
                        "chunk_indices": [context_dict["chunk_index"]],
                        "source_type": context_dict["source_type"],
                        "doc_type": context_dict["doc_type"],
                    }
                )

                last_doc_id = doc_id
                source_index += 1
            else:
                # Otherwise we only display the text and chunk_i
                formatted_sources.append(format_context_dict_for_llm_doc_chunks(context_dict))
                sources[source_index - 1]["chunk_indices"].append(context_dict["chunk_index"])

        formatted_context = "\n\n".join(formatted_sources)

        # Create messages
        messages = [RAG_SYSTEM_MESSAGE, format_rag_user_query_message(query, formatted_context)]
        resp_obj = self.llm.get_response(messages)
        answer_text = resp_obj.choices[0].message.content

        resp_dict = {
            "answer": answer_text,
            "model": resp_obj.model,
            "route": LLMRoute.RAG,
            "finish_reason": resp_obj.choices[0].finish_reason,
            "usage": {
                "completion_tokens": resp_obj.usage.completion_tokens,
                "prompt_tokens": resp_obj.usage.prompt_tokens,
                "total_tokens": resp_obj.usage.total_tokens
            },
            "sources": sources,
        }
        return resp_dict
