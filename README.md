# Enterprise AI Agent Infrastructure

Enterprise AI assistant built with FastAPI, LangGraph, PostgreSQL, Qdrant, and LiteLLM.

The assistant combines Retrieval-Augmented Generation (RAG) with agentic tool calling, allowing it to reason over both unstructured internal documents and structured enterprise data such as employees, customers, projects, and skills.

## Features

* FastAPI backend
* LangGraph agent orchestration
* Multi-step agent loop with tool calling
* Retrieval-Augmented Generation (RAG)
* Internal knowledge retrieval with source citations
* Structured enterprise data tools
  * Employee directory lookup
  * Employee skills and expertise lookup
  * Customer lookup
  * Customer project lookup
  * Employee project assignments
  * Project lookup and project team lookup
* PostgreSQL + SQLAlchemy
* Alembic database migrations
* Qdrant vector database
* Document retrieval and reranking
* Multi-provider and local LLM support through LiteLLM
* Pluggable embedding providers (currently: local, Voyage AI)
* Pluggable reranking providers (currently: local, Cohere)
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
* AsyncIO
* Pydantic

### AI / Agents

* LangGraph for agent orchestration
* LiteLLM for multi-provider LLM abstraction
* Cloud and local LLM support
* LLM tool/function calling
* Multi-step agent execution loop
* Structured enterprise-data tools
* Retrieval-Augmented Generation (RAG)
* Semantic retrieval using vector embeddings and Qdrant
* Cross-encoder reranking for relevance optimization
* Source-grounded responses with inline citations

### Vector Search

* Qdrant
* Pluggable embedding providers
* Pluggable reranking providers
* Metadata-aware document retrieval
* Retrieved-source tracking across multi-step agent runs

### Frontend

* React
* TypeScript
* Vite

### DevOps

* Docker
* Docker Compose
* GitHub Actions

---

## How It Works

The application uses a LangGraph-based agent.

For every user request, the LLM decides whether it can answer directly or whether it needs one or more tools.

Examples:

```text
"What is dependency injection?"
        │
        ▼
      Agent
        │
        └── Direct answer
```

```text
"Why did Northstar migrate from Pinecone?"
        │
        ▼
      Agent
        │
        ▼
search_company_knowledge
        │
        ▼
 RAG / Qdrant retrieval
        │
        ▼
      Agent
        │
        └── Grounded answer with citations
```

```text
"What projects is John Smith currently working on?"
        │
        ▼
      Agent
        │
        ▼
 lookup_employee
        │
        ▼
get_employee_projects
        │
        ▼
      Agent
        │
        └── Final answer
```

The agent may call multiple tools before producing its final response.

---

## Agent Tooling

The agent can access multiple internal capabilities through typed tools.

Current tools include:

### Internal Knowledge

```text
search_company_knowledge
```

Searches Northstar's internal document knowledge base using semantic retrieval and reranking.

Retrieved documents are exposed to the model using stable `[SOURCE n]` references, which are persisted alongside the generated assistant message.

### Employees

```text
lookup_employee
get_employee_skills
find_expert
get_employee_projects
```

These tools allow the agent to resolve employees, inspect skills and experience, find internal experts, and retrieve project assignments.

### Customers

```text
lookup_customer
get_customer_projects
```

These tools allow the agent to resolve customers and retrieve their associated projects.

### Projects

```text
lookup_project
get_project_team
```

These tools allow the agent to resolve projects and inspect assigned project teams.

Tool implementations access structured enterprise data stored in PostgreSQL.

---

## Agent Architecture

```text
                         ┌─────────────────────┐
                         │   React / Vite UI   │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │       FastAPI       │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   LangGraph Agent   │
                         │  LLM + Tool Schemas │
                         └──────────┬──────────┘
                                    │
                              tool calls?
                         ┌──────────┴──────────┐
                         │                     │
                        no                    yes
                         │                     │
                         ▼                     ▼
               ┌─────────────────┐    ┌─────────────────┐
               │  Direct Answer  │    │    ToolNode     │
               └────────┬────────┘    └────────┬────────┘
                        │                      │
                        ▼                      │
                      END                      │
                                               │
                    ┌──────────────────────────┼──────────────────────────┐
                    │                          │                          │
                    ▼                          ▼                          ▼
          ┌───────────────────┐      ┌───────────────────┐      ┌─────────────────┐
          │ Internal Knowledge│      │ PostgreSQL Tools  │      │   Other Tools   │
          │      Search       │      │                   │      │    extensible   │
          └─────────┬─────────┘      │ • Employees       │      └─────────────────┘
                    │                │ • Customers       │
                    ▼                │ • Projects        │
          ┌───────────────────┐      │ • Skills          │
          │   RAG Pipeline    │      └─────────┬─────────┘
          └─────────┬─────────┘                │
                    │                          │
             ┌──────┴──────┐                   │
             │             │                   │
             ▼             ▼                   │
       ┌───────────┐  ┌───────────┐            │
       │Embeddings │  │  Qdrant   │            │
       └─────┬─────┘  └───────────┘            │
             │                                 │
             ▼                                 │
       ┌───────────┐                           │
       │ Reranker  │                           │
       └─────┬─────┘                           │
             │                                 │
             └────────────────┬────────────────┘
                              │
                              ▼
                   ┌─────────────────────┐
                   │   LangGraph Agent   │
                   └──────────┬──────────┘
                              │
                        tool calls?
                   ┌──────────┴──────────┐
                   │                     │
                  yes                    no
                   │                     │
                   └──────► ToolNode     ▼
                                      ┌──────────────┐
                                      │ Final Answer │
                                      └──────┬───────┘
                                             │
                                             ▼
                                            END
```

The graph follows a simple agent loop:

```text
START
  │
  ▼
Agent
  │
  ├── no tool calls ──────────────► END
  │
  ▼
Tools
  │
  └───────────────────────────────► Agent
```

The LLM decides which tools to call. LangGraph manages the execution loop and passes tool results back to the model.

---

## Enterprise Data Model

The demo environment contains fictional Northstar Solutions business data.

Structured data includes relationships such as:

```text
Employee ─── EmployeeSkill ─── Skill

Employee ─── EmployeeProject ─── Project ─── Customer
```

This enables queries that require reasoning across multiple internal data sources, for example:

```text
Who is our most experienced Python expert?

What projects is John Smith currently working on?

What projects do we have with ACME Bank?

Who is working on the ACME Cloud Migration?

Which customer owns a particular project?
```

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

### Start Services

```bash
docker compose up -d
```

### Apply Database Migrations

```bash
alembic upgrade head
```

### Seed Database with Northstar Demo Data

```bash
python -m scripts.seed_northstar
```

This populates PostgreSQL with fictional Northstar enterprise data such as:

* Employees
* Skills
* Employee skill relationships
* Customers
* Projects
* Employee project assignments

### Ingest Northstar Documents and Store Embeddings in Vector Store

```bash
python -m scripts.ingest_documents
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

The test suite includes:

* Unit tests
* API integration tests
* Database-backed tests
* Authentication flow tests
* Agent and tool behavior tests

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

## Project Structure

```text
.
├── app/
│   ├── agents/          # LangGraph agent, state, graph, and tool definitions
│   ├── api/             # FastAPI routes, dependencies, and API schemas
│   ├── core/            # Configuration and security utilities
│   ├── db/              # SQLAlchemy models, sessions, and CRUD functions
│   ├── domain/          # Domain models and enums
│   ├── ingestion/       # Document ingestion code
│   ├── llm/             # LiteLLM / LLM client abstraction
│   ├── prompts/         # Agent and RAG prompt templates/helpers
│   ├── rag/             # Embeddings, retrieval, reranking, and vector stores
│   ├── services/        # Application service layer
│   └── main.py          # FastAPI application entrypoint
│
├── alembic/             # Database migrations
├── data/                # Northstar documents / local source data
├── frontend/            # React/Vite frontend
├── scripts/             # Seeding, ingestion, and utility scripts
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