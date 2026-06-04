from enum import Enum


class LLMRoute(str, Enum):
    DIRECT = "direct"
    RAG = "rag"
    CLARIFY = "clarify"
    TOOL = "tool"


class IntentRoute(str, Enum):
    ANSWER = "answer"
    SEARCH = "search"
    COMPARE = "compare"
    ACTION = "action"
    CLARIFY = "clarify"


class RetrievalScope(str, Enum):
    NONE = "none"
    INTERNAL = "internal"
    PUBLIC = "public"
    MIXED = "mixed"


class ToolAction(str, Enum):
    NONE = "none"
    CREATE_TICKET = "create_ticket"
    SEND_EMAIL = "send_email"
    SCHEDULE_EVENT = "schedule_event"
    UPLOAD_DOCUMENT = "upload_document"
    RUN_JOB = "run_job"
    CALL_API = "call_api"
    MODIFY_DATABASE = "modify_database"
    OTHER = "other"


class ResponseMode(str, Enum):
    DIRECT_ANSWER = "direct_answer"

    RAG_ANSWER = "rag_answer"

    SEARCH_RESULTS = "search_results"

    COMPARISON = "comparison"

    TOOL_WITH_CONTEXT = "tool_with_context"
    TOOL_ONLY = "tool_only"

    ASK_CLARIFYING_QUESTION = "ask_clarifying_question"
