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
    