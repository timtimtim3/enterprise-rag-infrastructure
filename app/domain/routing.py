from pydantic import BaseModel
from domain.enums.llm_route import IntentRoute, RetrievalScope, ToolAction, ResponseMode


class SearchHints(BaseModel):
    internal: bool
    public: bool
    vendors: list[str]
    keywords: list[str]


class RoutePlan(BaseModel):
    intent: IntentRoute
    retrieval_scope: RetrievalScope
    tool_action: ToolAction
    response_mode: ResponseMode
    confidence: float
    reason: str
    search_hints: SearchHints
