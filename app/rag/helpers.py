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
chunk_index: {context_dict.get("chunk_index")}
sections: {" > ".join(section_strings)}

{context_dict.get("text")}
""".strip()
