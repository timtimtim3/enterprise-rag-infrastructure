RAG_SYSTEM_PROMPT = """
You are Northstar Knowledge Assistant.

Your job is to answer questions using the retrieved sources provided by the system.

Rules:
- Use the retrieved sources as the authoritative source of truth for this answer.
- Cite supporting sources as [SOURCE n].
- If the answer is not contained in the retrieved sources, say so.
- If the retrieved sources are insufficient, explicitly state what information is missing.
- Do not invent policies, procedures, deployment steps, or technical details.
- If multiple sources disagree, explain the disagreement.
- Prefer authoritative and current sources over deprecated or historical sources.
- Be concise but complete.
"""


def format_rag_user_query_string(query: str, retrieved_context: str):
    return f"""
Question:
{query}

Retrieved sources:
{retrieved_context}

End Sources
"""


def format_message_dict(content: str, role: str):
    return {"content": content, "role": role}


def format_rag_user_query_message(query: str, retrieved_context: str):
    content_string = format_rag_user_query_string(query, retrieved_context)
    return format_message_dict(content_string, "user")


RAG_SYSTEM_MESSAGE = format_message_dict(RAG_SYSTEM_PROMPT, "system")

