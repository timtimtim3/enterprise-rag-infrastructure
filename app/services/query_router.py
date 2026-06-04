from __future__ import annotations

from typing import TYPE_CHECKING

from app.domain.routing import RoutePlan
from app.prompts.helpers import format_message_dict
from app.prompts.query_router import ROUTER_SYSTEM_MESSAGE

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
                
        # Create messages
        messages = [
            ROUTER_SYSTEM_MESSAGE,
            format_message_dict(
                content=(
                    "Classify the following user message. "
                    "Return only the routing JSON.\n\n"
                    f"USER_MESSAGE:\n{query}"
                ),
                role="user"
            )
        ]

        # Get LLM response
        resp_obj = self.llm.get_response(messages, temperature=0)
        answer_text = resp_obj.choices[0].message.content
        route_plan = RoutePlan.model_validate_json(answer_text)
        return route_plan
