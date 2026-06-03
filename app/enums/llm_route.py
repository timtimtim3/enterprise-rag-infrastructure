from enum import Enum


class LLMRoute(str, Enum):
    DIRECT = "direct"
    RAG = "rag"
    CLARIFY = "clarify"
    TOOl = "tool"
    