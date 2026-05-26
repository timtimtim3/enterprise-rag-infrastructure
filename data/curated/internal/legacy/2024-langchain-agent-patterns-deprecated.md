---
doc_id: "northstar-legacy-langchain-agent-patterns"
title: "LangChain Agent Workflow Patterns"
doc_type: "legacy_standard"
status: "deprecated"
authority: "historical"
category: "legacy"
folder: "internal/legacy/"
filename: "2024-langchain-agent-patterns-deprecated.md"
source_path: "internal/legacy/2024-langchain-agent-patterns-deprecated.md"
organization: "Northstar Solutions"
version: "2.0"
owner: "AI Research"
classification: "internal"
visibility: "employees"
audience:
  - "engineering"
  - "ai-platform"
effective_from: "2024-05-01"
deprecated_at: "2026-01-19"
superseded_by: "adr-021-langchain-vs-langgraph-evaluation.md"
applies_to: "older orchestration services"
reason_deprecated: "LangGraph selected for production orchestration"
---

# LangChain Agent Workflow Patterns (Deprecated)

> WARNING: Deprecated in favor of LangGraph orchestration standards.

# Approved Patterns

Recommended orchestration model:

- LangChain sequential chains
- agent executors
- tool routing chains

---

# Memory Strategy

Preferred memory:

- ConversationBufferMemory

Persistent agent memory is allowed for internal copilots.

---

# Known Issues

Operational problems observed:

- debugging complexity
- implicit execution flow
- retry instability
- difficult state inspection

---

# Migration Guidance

New multi-step workflows should migrate to LangGraph orchestration patterns.
