from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# from app.db import Base, engine
# from app.models import models
from app.api.routes.rag import router as rag_router
from app.api.routes.rag import router as health_router

from app.llm.client import LLM
from app.models.models import EmbeddingService, Reranker
from app.rag.retriever import Retriever
from app.rag.answer_service import AnswerService
from app.core.config import (
    COLLECTION_NAME,
    EMBEDDING_MODEL,
    RERANKER_MODEL,
    USING_LLM,
)
from app.vectorstores.qdrant_store import init_qdrant


@asynccontextmanager
async def lifespan(app: FastAPI):
    # DB conn for future:
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)

    embedding_svc = EmbeddingService(EMBEDDING_MODEL)
    qdrant_client = init_qdrant()
    reranker = Reranker(RERANKER_MODEL)
    retriever = Retriever(embedding_svc, reranker, qdrant_client, COLLECTION_NAME)
    llm = LLM(USING_LLM)
    answer_svc = AnswerService(retriever, llm)
    app.state.answer_svc = answer_svc

    yield

    # shutdown logic here...


app = FastAPI(lifespan=lifespan)

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

app.include_router(rag_router)
app.include_router(health_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
