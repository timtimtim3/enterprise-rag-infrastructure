from app.api.schemas.chats import AskResponse, SourceInfo, UsageInfo


def sources_from_answer(source_dicts: list[dict]) -> list[SourceInfo]:
    sources = []
    for source_dict in source_dicts:
        source = SourceInfo(
            doc_id=source_dict["doc_id"],
            source_index=source_dict["source_index"],
            chunk_indices=source_dict["chunk_indices"],
            title=source_dict["title"],
            source_path=source_dict["source_path"],
            source_type=source_dict["source_type"],
            doc_type=source_dict["doc_type"],
        )
        sources.append(source)
    return sources


def construct_ask_response(
    chat_id: str,
    query_message_id: str,
    answer_message_id: str,
    answer: dict,
    sources: list[SourceInfo],
) -> AskResponse:
    return AskResponse(
        chat_id=chat_id,
        query_message_id=query_message_id,
        answer_message_id=answer_message_id,
        answer=answer["answer"],
        model=answer["model"],
        finish_reason=answer["finish_reason"],
        usage=UsageInfo(
            completion_tokens=answer["usage"]["completion_tokens"],
            prompt_tokens=answer["usage"]["prompt_tokens"],
            total_tokens=answer["usage"]["total_tokens"],
        ),
        sources=sources,
    )
