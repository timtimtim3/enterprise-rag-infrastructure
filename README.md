# Enterprise RAG Infrastructure

Retrieval-Augmented Generation (RAG) knowledge assistant built with FastAPI, PostgreSQL, Qdrant, and modern AI tooling.

## Features

* FastAPI backend
* PostgreSQL + SQLAlchemy
* Alembic database migrations
* Qdrant vector database
* Retrieval-Augmented Generation (RAG)
* Query routing
* Document retrieval and reranking
* Multi-provider and local LLM support
* React/Vite frontend
* Automated testing with pytest
* GitHub Actions CI/CD

---

## Tech Stack

### Backend

* FastAPI
* SQLAlchemy
* PostgreSQL
* Alembic
* Qdrant
* AsyncIO
* Pydantic

### AI / RAG

* LiteLLM (multi-provider LLM abstraction)
* Cloud and local LLM support
* Query routing and response generation
* Semantic retrieval using vector embeddings and Qdrant vector search
* Cross-encoder reranking for relevance optimization
* Retrieval-Augmented Generation (RAG)

### Frontend

* React
* TypeScript
* Vite

### DevOps

* Docker
* Docker Compose
* GitHub Actions

---

## Prerequisites

Install:

* Python 3.12+
* Docker & Docker Compose
* Node.js 20+

---

## Backend Setup

### Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Create Environment File

```bash
cp .env.example .env
```

Populate the required environment variables.

### Start Database

```bash
docker compose up -d
```

### Apply Database Migrations

```bash
alembic upgrade head
```

### Run Backend

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Backend available at:

```text
http://localhost:8000
```

FastAPI Docs:

```text
http://localhost:8000/docs
```

---

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend available at:

```text
http://localhost:5173
```

---

## Running Tests

Run all tests:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=app
```

Current test suite includes:

* Unit tests
* API integration tests
* Database-backed tests
* Authentication flow tests

---

## CI/CD

GitHub Actions automatically runs the test suite on:

* Every push
* Every pull request

Workflow location:

```text
.github/workflows/tests.yml
```

The CI pipeline:

1. Starts a PostgreSQL test container
2. Installs project dependencies
3. Runs the full pytest suite
4. Reports test results

---

## Architecture

```text
Frontend (React/Vite)
        │
        ▼
   FastAPI Backend
        │
        ├───────────────────────┐
        │                       │
        ▼                       ▼
   PostgreSQL              RAG Pipeline
        │                       │
        ▼                       ▼
   SQLAlchemy            Query Router
                                │
                                ▼
                             LiteLLM
                                │
                                ▼
                          Answer Service
                                │
                                ▼
                            Retriever
                          ┌─────┴─────┐
                          │           │
                          ▼           ▼
                    Embeddings     Qdrant
                          │
                          ▼
                       Reranker
                          │
                          ▼
                       LiteLLM
```

---

## Project Structure

```text
.
├── app/
│   ├── api/             # FastAPI routes, dependencies, and API schemas
│   ├── core/            # Configuration and security utilities
│   ├── db/              # SQLAlchemy models, sessions, and CRUD functions
│   ├── domain/          # Domain models, enums, and routing concepts
│   ├── ingestion/       # Document ingestion code
│   ├── llm/             # LiteLLM / LLM client abstraction
│   ├── prompts/         # Prompt templates and prompt helpers
│   ├── rag/             # Embeddings, retrieval, reranking, and vector stores
│   ├── services/        # Application service layer
│   └── main.py          # FastAPI application entrypoint
│
├── alembic/             # Database migrations
├── data/                # Local data / cloned source repositories
├── frontend/            # React/Vite frontend
├── scripts/             # Utility scripts
├── tests/
│   ├── api/             # API/integration tests
│   └── unit/            # Unit tests
│
├── docker-compose.yml
├── requirements.txt
├── pytest.ini
└── README.md
```

---

## Environment Variables

See:

```text
.env.example
```

for all required configuration values.
