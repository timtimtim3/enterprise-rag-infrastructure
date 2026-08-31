from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from redis.asyncio import Redis

from app.agents.graph import build_agent_graph
import app.db.models
from app.db.base import Base
from app.db.session import engine
from app.api.routes.chats import router as chat_router
from app.api.routes.health import router as health_router
from app.api.routes.auth import router as auth_router
from app.core.config import (
    COLLECTION_NAME_PREFIX,
    EMBEDDING_PROVIDER,
    REDIS_URL,
    RERANKER_PROVIDER,
    USING_LLM,
)

from app.llm.client import LLM
from app.rag.embeddings.factory import embedding_provider_factory
from app.rag.reranking.factory import reranker_provider_factory
from app.rag.retriever import Retriever
from app.rag.vectorstores.qdrant_store import init_qdrant, name_qdrant_collection
from app.services.answer_service import AnswerService
from app.services.query_router import QueryRouter


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    embedding_provider = embedding_provider_factory(EMBEDDING_PROVIDER)
    reranker_provider = reranker_provider_factory(RERANKER_PROVIDER)
    qdrant_collection_name = name_qdrant_collection(COLLECTION_NAME_PREFIX, EMBEDDING_PROVIDER, embedding_provider.model_name)
    qdrant_client = await init_qdrant(qdrant_collection_name)

    retriever = Retriever(embedding_provider, reranker_provider, qdrant_client, qdrant_collection_name)
    llm = LLM(USING_LLM)

    # Keep these while migrating
    query_router = QueryRouter(llm)
    answer_svc = AnswerService(retriever, llm)

    # New agent flow
    agent_graph = build_agent_graph(
        llm=llm,
        retriever=retriever,
    )
    app.state.agent_graph = agent_graph
    app.state.retriever = retriever

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
