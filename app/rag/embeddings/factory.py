from app.rag.embeddings.providers import EmbeddingProviders


def embedding_provider_factory(provider: EmbeddingProviders):
    if provider == EmbeddingProviders.LOCAL:
        from app.rag.embeddings.local import LocalEmbeddingProvider
        from app.core.config import LOCAL_EMBEDDING_MODEL
        return LocalEmbeddingProvider(model_name=LOCAL_EMBEDDING_MODEL)
    elif provider == EmbeddingProviders.VOYAGE:
        from app.rag.embeddings.voyage import VoyageEmbeddingProvider
        from app.core.config import VOYAGE_API_KEY, VOYAGE_EMBEDDING_MODEL
        if VOYAGE_API_KEY is None:
            raise ValueError("VOYAGE_API_KEY should be set in .env when using VoyageEmbeddingProvider")
        if VOYAGE_EMBEDDING_MODEL is None:
            raise ValueError("VOYAGE_EMBEDDING_MODEL should be set in .env when using VoyageEmbeddingProvider")
        return VoyageEmbeddingProvider(model_name=VOYAGE_EMBEDDING_MODEL, api_key=VOYAGE_API_KEY)
