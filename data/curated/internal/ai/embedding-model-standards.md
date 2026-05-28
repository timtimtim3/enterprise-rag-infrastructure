---
doc_id: "northstar-ai-embedding-model-standards"
title: "Embedding Model Standards"
source_type: internal
doc_type: "standard"
status: "current"
authority: "authoritative"
category: "ai"
folder: "internal/ai/"
filename: "embedding-model-standards.md"
source_path: "internal/ai/embedding-model-standards.md"
organization: "Northstar Solutions"
version: "1.8"
classification: "internal"
visibility: "employees"
audience:
  - "ai-platform"
  - "ai-governance"
  - "engineering"
effective_from: null
deprecated_at: null
superseded_by: null
applies_to: "current Northstar internal guidance unless superseded"
content_hash: "8233f1753ddf"
metadata_added_on: "2026-05-25"
---
# Embedding Model Standards
Version: 1.8

# Purpose

Defines embedding model standards for retrieval systems at Northstar Solutions.

---

# Approved Embedding Models

## Primary Standard

Default embedding model:

- text-embedding-3-large

Reasoning:

- high retrieval accuracy
- stable multilingual performance
- strong semantic similarity quality

---

# Secondary Approved Models

| Model | Usage |
|---|---|
| text-embedding-3-small | low-cost workloads |
| Cohere Embed v4 | multilingual customer deployments |

---

# Vector Dimensions

Standard dimensions:

- 3072 for production retrieval
- 1536 for cost-optimized systems

Mixed-dimension indexes are prohibited.

---

# Chunking Standards

Default chunk size:

- 800 tokens

Default overlap:

- 120 tokens

Large legal documents:

- 1200 tokens

---

# Metadata Standards

Every vector must include metadata:

```json
{
  "document_id": "doc_123",
  "source": "internal",
  "team": "platform-engineering",
  "created_at": "2026-01-12",
  "classification": "internal"
}
```

---

# Embedding Refresh Rules

Re-embedding required when:

- chunking strategy changes
- embedding model changes
- metadata schema changes

---

# Retrieval Standards

Production systems must support:

- metadata filtering
- hybrid retrieval
- reranking

---

# Vector Store Standards

Approved vector stores:

- Qdrant
- pgvector

Deprecated:

- Pinecone (legacy workloads only)

---

# Similarity Thresholds

Default similarity threshold:

- 0.78

Low-confidence retrievals must trigger:

- reranking
- clarification prompts
- fallback retrieval strategies

---

# Cost Management

Embedding generation must support:

- batching
- retry limits
- deduplication

---

# Related Documents

- rag-evaluation-checklist.md
- hallucination-mitigation-policy.md
- model-fallback-strategy.md
