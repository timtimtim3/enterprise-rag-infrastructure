import operator
from typing import Annotated

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from typing_extensions import NotRequired, TypedDict


class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

    # Increment this by returning {"tool_iterations": 1}
    tool_iterations: Annotated[int, operator.add]

    # Append new tool-call records
    tool_history: Annotated[list[dict], operator.add]

    user_id: NotRequired[str | None]

    # doc_id -> persisted citation metadata for this answer
    source_registry: dict[str, dict]

    # Aggregated across ALL agent LLM calls
    prompt_tokens: Annotated[int, operator.add]
    completion_tokens: Annotated[int, operator.add]
    total_tokens: Annotated[int, operator.add]

    # Last agent call wins, which will normally be the final answer call
    model: NotRequired[str | None]
    finish_reason: NotRequired[str | None]
    