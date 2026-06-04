from app.domain.enums.llm_route import ResponseMode, RetrievalScope
from app.prompts.assistant.clarifying_question import CLARIFYING_QUESTION_SYSTEM_PROMPT
from app.prompts.assistant.comparison import COMPARISON_SYSTEM_PROMPT
from app.prompts.assistant.direct import DIRECT_ANSWER_SYSTEM_PROMPT
from app.prompts.assistant.rag import RAG_INTERNAL_SYSTEM_PROMPT, RAG_MIXED_SYSTEM_PROMPT, RAG_PUBLIC_SYSTEM_PROMPT
from app.prompts.assistant.search_results import SEARCH_RESULTS_SYSTEM_PROMPT


ANSWER_SYSTEM_PROMPTS_BY_MODE = {
    ResponseMode.DIRECT_ANSWER: DIRECT_ANSWER_SYSTEM_PROMPT,
    ResponseMode.RAG_ANSWER: None,  # choose by retrieval_scope
    ResponseMode.COMPARISON: COMPARISON_SYSTEM_PROMPT,
    ResponseMode.SEARCH_RESULTS: SEARCH_RESULTS_SYSTEM_PROMPT,
    ResponseMode.ASK_CLARIFYING_QUESTION: CLARIFYING_QUESTION_SYSTEM_PROMPT,
    ResponseMode.TOOL_WITH_CONTEXT: None, # Not yet implemented
    ResponseMode.TOOL_ONLY: None, # Not yet implemented
}
RAG_SYSTEM_PROMPTS_BY_SCOPE = {
    RetrievalScope.INTERNAL: RAG_INTERNAL_SYSTEM_PROMPT,
    RetrievalScope.PUBLIC: RAG_PUBLIC_SYSTEM_PROMPT,
    RetrievalScope.MIXED: RAG_MIXED_SYSTEM_PROMPT,
}
