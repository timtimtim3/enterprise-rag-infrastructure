from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.llm.client import LLM


class QueryRouter:
    def __init__(self, llm: LLM):
        self.llm = llm

    def route_query(self, query: str):
        """
        Decides:
        intent = desired final outcome
        retrieval_scope = knowledge needed
        tool = action needed
        response_mode = how final response should be produced
        """
        pass
