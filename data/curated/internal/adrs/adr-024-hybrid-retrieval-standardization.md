---
doc_id: "northstar-adrs-adr-024-hybrid-retrieval-standardization"
title: "ADR-024 — Hybrid Retrieval Standardization"
source_type: internal
doc_type: "adr"
status: "current"
authority: "decision_record"
category: "adrs"
folder: "internal/adrs/"
filename: "adr-024-hybrid-retrieval-standardization.md"
source_path: "internal/adrs/adr-024-hybrid-retrieval-standardization.md"
organization: "Northstar Solutions"
classification: "internal"
visibility: "employees"
audience:
  - "engineering"
  - "architecture-review"
  - "ai-platform"
effective_from: null
deprecated_at: null
superseded_by: null
applies_to: "current Northstar internal guidance unless superseded"
content_hash: "6cce5aeacebb"
metadata_added_on: "2026-05-25"
---
# ADR-024 — Hybrid Retrieval Standardization
Status: Accepted

# Context

Evaluation benchmarks showed that vector-only retrieval struggled with:

- exact technical terminology
- identifiers
- operational runbooks
- structured infrastructure documents

---

# Decision

Northstar Solutions will standardize on hybrid retrieval:

- dense vector retrieval
- BM25 keyword retrieval
- reranker fusion

---

# Results

Internal benchmark improvements:

| Metric | Improvement |
|---|---|
| Retrieval Recall | +18% |
| Citation Accuracy | +14% |
| Support Resolution Accuracy | +11% |

---

# Key Insight

Operational documents often contain:

- exact error codes
- infrastructure identifiers
- deployment versions
- customer-specific naming

Keyword retrieval substantially improved these scenarios.

---

# Consequences

## Positive

- improved technical retrieval quality
- better operational search
- stronger incident document retrieval

---

## Negative

- increased infrastructure complexity
- higher query latency
- reranker cost increase

---

# Related Documents

- rag-evaluation-checklist.md
- embedding-model-standards.md
- hallucination-mitigation-policy.md
