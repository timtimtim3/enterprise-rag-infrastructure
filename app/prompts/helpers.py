def format_message_dict(content: str, role: str):
    return {"content": content, "role": role}


def format_retrieved_context_message(retrieved_context: str):
    return f"""
Retrieved sources:

{retrieved_context}

End retrieved sources.

Use these sources according to the system instructions.
"""
