---
doc_id: "northstar-incidents-2026-01-qdrant-latency-regression"
title: "Incident Report — Qdrant Latency Regression"
source_type: internal
doc_type: "incident_report"
status: "current"
authority: "historical_record"
category: "incidents"
folder: "internal/incidents/"
filename: "2026-01-qdrant-latency-regression.md"
source_path: "internal/incidents/2026-01-qdrant-latency-regression.md"
organization: "Northstar Solutions"
classification: "internal"
visibility: "employees"
audience:
  - "platform-operations"
  - "engineering"
  - "ai-platform"
effective_from: null
deprecated_at: null
superseded_by: null
applies_to: "current Northstar internal guidance unless superseded"
content_hash: "34dc607e9816"
metadata_added_on: "2026-05-25"
---
# Incident Report — Qdrant Latency Regression
Incident ID: INC-2026-0117
Severity: SEV-2

# Summary

Production retrieval latency increased significantly following deployment of a new multi-tenant metadata filtering strategy.

---

# Symptoms

Observed issues:

- p95 retrieval latency exceeded 4 seconds
- reranker queues backed up
- support copilots degraded

---

# Root Cause

A newly introduced metadata indexing strategy caused inefficient filtering execution paths in large collections.

---

# Contributing Factors

- oversized metadata payloads
- unbounded tenant filters
- missing load-test coverage

---

# Resolution

Mitigations:

- optimized metadata schema
- reduced indexed metadata fields
- introduced filtered collection partitioning

---

# Key Lessons

Enterprise RAG retrieval performance is heavily impacted by metadata design quality.

---

# Related Documents

- embedding-model-standards.md
- monitoring-requirements.md
- hybrid-retrieval-standardization.md
