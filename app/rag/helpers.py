from app.prompts.helpers import format_retrieved_context_message


def format_context_dict_for_llm(context_dict: dict, source_index: int) -> str:
    section_strings = []
    for section_lvl in ["h1", "h2", "h3"]:
        section = context_dict.get(section_lvl)
        if section is not None:
            section_strings.append(f"{section_lvl}: {section}")

    return f"""
[SOURCE {source_index + 1}]
title: {context_dict.get("title")}
source_path: {context_dict.get("source_path")}
source_type: {context_dict.get("source_type")}
doc_type: {context_dict.get("doc_type")}
vendor: {context_dict.get("vendor")}
status: {context_dict.get("status")}
authority: {context_dict.get("authority")}
category: {context_dict.get("category")}
sections: {" > ".join(section_strings)}
chunk_index: {context_dict.get("chunk_index")}
{context_dict.get("text")}
""".strip()


def format_context_dict_for_llm_doc_chunks(context_dict: dict):
    return f"""
chunk_index: {context_dict.get("chunk_index")}
{context_dict.get("text")}
""".strip()


def format_sources(context_dicts: list[dict]):
    formatted_sources = []
    last_doc_id = None
    source_index = 0
    sources = []
    for context_dict in context_dicts:
        doc_id = context_dict["doc_id"]

        # If not the same, it's the first chunk of doc, we display full context / meta
        if doc_id != last_doc_id:
            formatted_sources.append(format_context_dict_for_llm(context_dict, source_index))
            sources.append(
                {
                    "source_index": source_index,
                    "title": context_dict["title"],
                    "source_path": context_dict["source_path"],
                    "doc_id": doc_id,
                    "chunk_indices": [context_dict["chunk_index"]],
                    "source_type": context_dict["source_type"],
                    "doc_type": context_dict["doc_type"],
                }
            )

            last_doc_id = doc_id
            source_index += 1
        else:
            # Otherwise we only display the text and chunk_i
            formatted_sources.append(format_context_dict_for_llm_doc_chunks(context_dict))
            sources[source_index - 1]["chunk_indices"].append(context_dict["chunk_index"])

    formatted_context = "\n\n".join(formatted_sources)
    return format_retrieved_context_message(formatted_context), sources
