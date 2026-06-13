from app.rag.reranking.providers import RerankerProviders


def reranker_provider_factory(provider: RerankerProviders):
    if provider == RerankerProviders.LOCAL:
        from app.rag.reranking.local import LocalRerankerProvider
        from app.core.config import LOCAL_RERANKER_MODEL
        return LocalRerankerProvider(model_name=LOCAL_RERANKER_MODEL)
    elif provider == RerankerProviders.COHERE:
        from app.rag.reranking.cohere import CohereRerankerProvider
        from app.core.config import COHERE_API_KEY, COHERE_RERANKER_MODEL
        if COHERE_API_KEY is None:
            raise ValueError("COHERE_API_KEY should be set in .env when using CohereRerankerProvider")
        if COHERE_RERANKER_MODEL is None:
            raise ValueError("COHERE_RERANKER_MODEL should be set in .env when using CohereRerankerProvider")
        return CohereRerankerProvider(model_name=COHERE_RERANKER_MODEL, api_key=COHERE_API_KEY)
