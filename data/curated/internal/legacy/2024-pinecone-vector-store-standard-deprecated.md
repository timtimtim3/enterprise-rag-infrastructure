---
doc_id: "northstar-legacy-pinecone-vector-store-standard"
title: "2024 Pinecone Vector Store Standard"
source_type: internal
doc_type: "legacy_policy"
status: "deprecated"
authority: "historical"
category: "legacy"
folder: "internal/legacy/"
filename: "2024-pinecone-vector-store-standard-deprecated.md"
source_path: "internal/legacy/2024-pinecone-vector-store-standard-deprecated.md"
organization: "Northstar Solutions"
version: "1.4"
owner: "AI Platform"
classification: "internal"
visibility: "employees"
audience:
  - "engineering"
  - "ai-platform"
effective_from: "2024-03-01"
deprecated_at: "2025-11-08"
superseded_by: "adr-017-migrate-pinecone-to-qdrant.md"
applies_to: "legacy Pinecone workloads only"
reason_deprecated: "Qdrant selected as enterprise retrieval standard"
---

# Pinecone Vector Store Standard (Deprecated)

> WARNING: This document is deprecated and retained for historical migration support only.

# Purpose

Defines the original vector database standards for Northstar retrieval systems.

---

# Approved Vector Store

Primary approved vector platform:

- Pinecone

pgvector is permitted only for experimentation.

---

# Namespace Strategy

Each customer must receive:

- dedicated Pinecone namespace
- isolated retrieval indexes
- environment-specific index prefixes

---

# Retrieval Standards

Production retrieval must support:

- dense vector retrieval
- metadata filtering
- namespace isolation

Hybrid retrieval is considered experimental.

---

# Operational Concerns

Known issues:

- rising query cost
- regional deployment limitations
- limited VPC deployment flexibility

---

# Migration Notice

Future deployments should migrate to Qdrant according to ADR-017.
