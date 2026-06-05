from app.prompts.helpers import format_message_dict


def build_messages(
    *,
    system_prompt: str, # current task-specific prompt, decided by query router, depends on query
    user_query: str,
    app_context_messages: list[str] | None = None, # e.g. RAG results, query_router reason for asking clarification, etc.
    history_messages: list[dict] | None = None, # user, assistant messages in recent conversation
) -> list[dict]:
    messages = [format_message_dict(system_prompt, "system")]
    for ctx in app_context_messages or []:
        messages.append(format_message_dict(ctx, "system"))

    messages.extend(history_messages or [])

    messages.append(format_message_dict(user_query, "user"))

    return messages
