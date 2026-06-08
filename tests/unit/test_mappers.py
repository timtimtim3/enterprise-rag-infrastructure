from app.api.schemas.chats import SourceInfo
from app.api.schemas.mappers import sources_from_answer, construct_ask_response


def test_sources_from_answer_maps_dicts_to_source_info():
    source_dicts = [
        {
            "doc_id": "doc-1",
            "source_index": 0,
            "chunk_indices": [1, 2],
            "title": "Test document",
            "source_path": "/docs/test.pdf",
            "source_type": "file",
            "doc_type": "pdf",
        }
    ]

    sources = sources_from_answer(source_dicts)

    assert len(sources) == 1
    assert isinstance(sources[0], SourceInfo)
    assert sources[0].doc_id == "doc-1"
    assert sources[0].chunk_indices == [1, 2]
    assert sources[0].title == "Test document"


def test_construct_ask_response_maps_answer_to_response_schema():
    sources = [
        SourceInfo(
            doc_id="doc-1",
            source_index=0,
            chunk_indices=[1],
            title="Test document",
            source_path="/docs/test.pdf",
            source_type="file",
            doc_type="pdf",
        )
    ]

    answer = {
        "answer": "This is the answer.",
        "model": "gpt-4.1-mini",
        "finish_reason": "stop",
        "usage": {
            "completion_tokens": 10,
            "prompt_tokens": 20,
            "total_tokens": 30,
        },
    }

    response = construct_ask_response(
        chat_id="chat-1",
        query_message_id="msg-q",
        answer_message_id="msg-a",
        answer=answer,
        sources=sources,
    )

    assert response.chat_id == "chat-1"
    assert response.query_message_id == "msg-q"
    assert response.answer_message_id == "msg-a"
    assert response.answer == "This is the answer."
    assert response.model == "gpt-4.1-mini"
    assert response.usage.total_tokens == 30
    assert response.sources == sources
    