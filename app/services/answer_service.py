from __future__ import annotations

from textwrap import dedent
from typing import TYPE_CHECKING, Optional

from app.api.schemas.chats import SourceInfo
from app.domain.enums.llm_route import LLMRoute, ResponseMode, RetrievalScope
from app.rag.helpers import format_sources
from app.prompts.assistant.rag import RAG_SYSTEM_MESSAGE, format_rag_user_query_message
from app.prompts import ANSWER_SYSTEM_PROMPTS_BY_MODE, RAG_SYSTEM_PROMPTS_BY_SCOPE
from app.services.helpers import build_messages

if TYPE_CHECKING:
    from app.rag.retriever import Retriever
    from app.llm.client import LLM


class AnswerService:
    def __init__(self, retriever: Retriever, llm: LLM):
        self.retriever = retriever
        self.llm = llm
    
    def build_resp_obj(self, llm_resp, sources: Optional[list[SourceInfo]] = None):
        return {
            "answer": llm_resp.choices[0].message.content,
            "model": llm_resp.model,
            "finish_reason": llm_resp.choices[0].finish_reason,
            "usage": {
                "completion_tokens": llm_resp.usage.completion_tokens,
                "prompt_tokens": llm_resp.usage.prompt_tokens,
                "total_tokens": llm_resp.usage.total_tokens
            },
            "sources": sources or [],
        }
    
    async def retrieve_and_format(self, query: str):
        context_dicts = await self.retriever.retrieve_context(query)
        llm_formatted_sources_message, original_sources = format_sources(context_dicts)
        return llm_formatted_sources_message, original_sources

    async def answer_question(self, query: str):
        formatted_context, sources = await self.retrieve_and_format(query)

        # Create messages
        messages = [RAG_SYSTEM_MESSAGE, format_rag_user_query_message(query, formatted_context)]
        resp_obj = await self.llm.get_response(messages)
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
    
    async def answer(
        self,
        query: str,
        retrieval_scope: RetrievalScope,
        response_mode: ResponseMode,
        reason: str,
        retrieval_query: Optional[str] = None,
        history_messages: Optional[list[dict]] = None,
    ):
        # Get system prompt
        if response_mode == ResponseMode.RAG_ANSWER:
            system_prompt = RAG_SYSTEM_PROMPTS_BY_SCOPE[retrieval_scope]
        else:
            system_prompt = ANSWER_SYSTEM_PROMPTS_BY_MODE[response_mode]
        
        # Do retrieval
        app_context_messages, sources = [], []
        if retrieval_scope != RetrievalScope.NONE:
            retrieval_query = retrieval_query or query
            formatted_context, sources = await self.retrieve_and_format(retrieval_query)
            app_context_messages.append(formatted_context)

        if response_mode == ResponseMode.ASK_CLARIFYING_QUESTION:
            # Append reason for query_router choosing to ask for clarification first
            app_context_messages.append(
                dedent(
                    f"""
                    Reason for asking for clarification first:

                    {reason}
                    """
                ).strip()
            )

        # Build messages for llm
        messages = build_messages(
            system_prompt=system_prompt,
            user_query=query,
            app_context_messages=app_context_messages,
            history_messages=history_messages,
        )
        llm_resp = await self.llm.get_response(messages) # Get response
        return self.build_resp_obj(llm_resp=llm_resp, sources=sources)
