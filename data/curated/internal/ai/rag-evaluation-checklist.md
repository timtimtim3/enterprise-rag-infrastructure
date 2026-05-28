---
doc_id: "northstar-ai-rag-evaluation-checklist"
title: "RAG Evaluation Checklist"
source_type: internal
doc_type: "checklist"
status: "current"
authority: "authoritative"
category: "ai"
folder: "internal/ai/"
filename: "rag-evaluation-checklist.md"
source_path: "internal/ai/rag-evaluation-checklist.md"
organization: "Northstar Solutions"
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
content_hash: "f2b4a74845cf"
metadata_added_on: "2026-05-25"
---
# RAG Evaluation Checklist

# Purpose

Defines the standard evaluation checklist for retrieval-augmented generation systems.

---

# Retrieval Quality

## Required Checks

- [ ] Correct document retrieved
- [ ] Correct chunk retrieved
- [ ] Metadata filtering works
- [ ] Duplicate suppression works
- [ ] Reranker functioning correctly

---

# Response Quality

- [ ] Response grounded in retrieved docs
- [ ] Citations present
- [ ] No fabricated claims
- [ ] Response concise and relevant

---

# Latency

Target latency:

- retrieval < 500ms
- reranking < 800ms
- total response < 8s

---

# Evaluation Dataset Requirements

Datasets must include:

- single-hop questions
- multi-hop questions
- ambiguous questions
- adversarial prompts
- outdated information tests

---

# Failure Modes

Systems must test for:

- empty retrieval
- irrelevant retrieval
- conflicting documents
- outdated documents

---

# Hybrid Retrieval

Required validation:

- keyword retrieval quality
- vector retrieval quality
- combined ranking quality

---

# Citation Validation

Check:

- source attribution correctness
- citation-document alignment
- chunk relevance

---

# Human Evaluation

Quarterly human reviews required for:

- top customer workflows
- executive copilots
- support automation systems

---

# Production Readiness Gate

Production approval requires:

- hallucination benchmark
- latency benchmark
- cost benchmark
- governance review
