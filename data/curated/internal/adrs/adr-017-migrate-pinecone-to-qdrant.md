---
doc_id: "northstar-adrs-adr-017-migrate-pinecone-to-qdrant"
title: "ADR-017 — Migration from Pinecone to Qdrant"
doc_type: "adr"
status: "current"
authority: "decision_record"
category: "adrs"
folder: "internal/adrs/"
filename: "adr-017-migrate-pinecone-to-qdrant.md"
source_path: "internal/adrs/adr-017-migrate-pinecone-to-qdrant.md"
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
content_hash: "1a50608b344b"
metadata_added_on: "2026-05-25"
---
# ADR-017 — Migration from Pinecone to Qdrant
Status: Accepted
Date: 2025-11-08

# Context

Northstar Solutions originally standardized on Pinecone for vector retrieval workloads.

As customer deployments scaled, multiple limitations emerged:

- rising query cost
- limited filtering flexibility
- regional deployment restrictions
- operational latency concerns

Large enterprise customers additionally requested:

- VPC-isolated deployments
- infrastructure portability
- self-hosting options

---

# Decision

Northstar Solutions will standardize future deployments on Qdrant.

Existing Pinecone workloads will migrate incrementally.

---

# Reasons for Decision

## Improved Filtering

Qdrant supports more flexible metadata filtering for enterprise retrieval use cases.

This improves:

- tenant isolation
- document classification filtering
- retrieval precision

---

## Self-Hosting Flexibility

Qdrant supports:

- private VPC deployments
- customer-managed infrastructure
- regional deployment control

This aligns with enterprise compliance requirements.

---

## Cost Efficiency

Projected annual retrieval infrastructure savings:

- approximately 34%

---

## Operational Visibility

Platform Engineering reported improved observability and operational debugging compared to prior Pinecone deployments.

---

# Alternatives Considered

## Remain on Pinecone

Rejected due to:

- cost trajectory
- limited deployment flexibility
- vendor dependency concerns

---

## pgvector Only

Rejected because:

- operational scaling concerns
- retrieval performance variability
- insufficient ANN optimization

---

# Consequences

## Positive

- improved filtering
- lower operational cost
- deployment portability
- stronger enterprise compliance posture

---

## Negative

- migration complexity
- embedding reindexing requirements
- temporary dual-vector infrastructure

---

# Migration Plan

Migration phases:

1. new workloads default to Qdrant
2. dual-write ingestion pipeline
3. customer-by-customer migration
4. Pinecone retirement

---

# Related Documents

- embedding-model-standards.md
- rag-evaluation-checklist.md
- enterprise-deployment-standards.md
