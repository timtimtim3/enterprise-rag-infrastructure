import tiktoken


ENCODING = tiktoken.get_encoding("cl100k_base")


def estimate_tokens(text: str) -> int:
    return len(ENCODING.encode(text))


def format_message_dict(content: str, role: str):
    return {"content": content, "role": role}


def format_retrieved_context_message(retrieved_context: str):
    return f"""
Retrieved sources:

{retrieved_context}

End retrieved sources.

Use these sources according to the system instructions.
"""
