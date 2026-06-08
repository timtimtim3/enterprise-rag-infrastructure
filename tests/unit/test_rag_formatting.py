from app.rag.helpers import format_context_dict_for_llm, format_context_dict_for_llm_doc_chunks


def test_format_context_dict_for_llm_contains_metadata():
    context = {
        "title": "Azure Guide",
        "source_path": "/docs/azure.pdf",
        "source_type": "pdf",
        "doc_type": "manual",
        "vendor": "Microsoft",
        "status": "active",
        "authority": "official",
        "category": "cloud",
        "h1": "Azure",
        "h2": "Storage",
        "chunk_index": 5,
        "text": "Blob storage explanation",
    }

    result = format_context_dict_for_llm(context, 0)

    assert "[SOURCE 1]" in result
    assert "title: Azure Guide" in result
    assert "vendor: Microsoft" in result
    assert "h1: Azure" in result
    assert "h2: Storage" in result
    assert "Blob storage explanation" in result


def test_format_context_dict_for_llm_doc_chunks():
    context = {
        "chunk_index": 12,
        "text": "Hello world"
    }

    result = format_context_dict_for_llm_doc_chunks(context)

    assert "chunk_index: 12" in result
    assert "Hello world" in result
    