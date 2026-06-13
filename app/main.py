from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from redis.asyncio import Redis

import app.db.models
from app.db.base import Base
from app.db.session import engine
from app.api.routes.chats import router as chat_router
from app.api.routes.health import router as health_router
from app.api.routes.auth import router as auth_router
from app.core.config import (
    COLLECTION_NAME_PREFIX,
    LOCAL_EMBEDDING_MODEL,
    REDIS_URL,
    LOCAL_RERANKER_MODEL,
    USING_LLM,
)

from app.llm.client import LLM
from app.rag.embeddings.local import LocalEmbeddingProvider
from app.rag.reranking.local import LocalRerankerProvider
from app.rag.retriever import Retriever
from app.rag.vectorstores.qdrant_store import init_qdrant
from app.services.answer_service import AnswerService
from app.services.query_router import QueryRouter


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    embedding_svc = LocalEmbeddingProvider(LOCAL_EMBEDDING_MODEL)
    qdrant_client = await init_qdrant()
    reranker = LocalRerankerProvider(LOCAL_RERANKER_MODEL)
    retriever = Retriever(embedding_svc, reranker, qdrant_client, COLLECTION_NAME_PREFIX)
    llm = LLM(USING_LLM)

    query_router = QueryRouter(llm)
    answer_svc = AnswerService(retriever, llm)
    app.state.query_router = query_router
    app.state.answer_svc = answer_svc
    app.state.redis = Redis.from_url(REDIS_URL, decode_responses=True)
    
    yield

    # shutdown logic
    await app.state.redis.aclose()
    await engine.dispose()
    await qdrant_client.close()
    

app = FastAPI(lifespan=lifespan)


@app.middleware("http")
async def security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["X-Frame-Options"] = "DENY"
    return response


origins = [
    "http://localhost:3000",  # React/Next frontend
    "http://localhost:5173",  # Vite
    "http://localhost:8080",
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)
app.include_router(auth_router)
app.include_router(health_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
