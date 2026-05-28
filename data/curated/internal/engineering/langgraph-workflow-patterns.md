---
doc_id: "northstar-engineering-langgraph-workflow-patterns"
title: "LangGraph Workflow Patterns"
source_type: internal
doc_type: "knowledge_doc"
status: "current"
authority: "reference"
category: "engineering"
folder: "internal/engineering/"
filename: "langgraph-workflow-patterns.md"
source_path: "internal/engineering/langgraph-workflow-patterns.md"
organization: "Northstar Solutions"
version: "1.3"
classification: "internal"
visibility: "employees"
audience:
  - "engineering"
  - "platform"
  - "ai-platform"
effective_from: null
deprecated_at: null
superseded_by: null
applies_to: "current Northstar internal guidance unless superseded"
content_hash: "b4c1606dfa4c"
metadata_added_on: "2026-05-25"
---
# LangGraph Workflow Patterns
Version: 1.3

# Purpose

This document defines approved orchestration patterns for LangGraph-based AI systems at Northstar Solutions.

---

# Approved Use Cases

LangGraph is approved for:

- multi-step agent workflows
- retrieval orchestration
- tool routing
- escalation flows
- human-in-the-loop review
- retryable AI pipelines

Not approved for:

- simple single-prompt APIs
- synchronous CRUD services

---

# Standard Graph Architecture

Recommended node categories:

- retrieval
- reasoning
- tool execution
- validation
- escalation
- response formatting

---

# State Management Rules

State objects must remain:

- serializable
- deterministic
- minimal

Disallowed:

- storing raw embeddings in graph state
- large document blobs
- secrets

---

# Retry Strategy

Allowed retries:

- transient LLM failures
- vector retrieval timeouts
- rate limits

Maximum retries:

- 3

---

# Human Escalation Nodes

Mandatory for:

- financial recommendations
- legal reasoning
- PHI workflows
- destructive actions

---

# Retrieval Pattern Standards

Approved retrieval strategies:

- hybrid retrieval
- metadata filtering
- reranker-enhanced retrieval

Default chunk size:

- 800 tokens

Default overlap:

- 120 tokens

---

# Memory Policy

Long-term conversational memory is disabled by default.

Allowed memory systems:

- Redis session state
- customer-approved memory stores

---

# Tool Invocation Standards

Tools must be:

- idempotent
- observable
- timeout-controlled

Every tool call must emit:

- execution duration
- status
- correlation ID

---

# Hallucination Mitigation

Required safeguards:

- retrieval grounding
- confidence thresholds
- citation enforcement
- response validation nodes

---

# Observability

All graph executions must support:

- trace IDs
- node-level metrics
- execution replay
- failure inspection

---

# Production Restrictions

Disallowed in production:

- autonomous internet browsing
- unrestricted code execution
- self-modifying prompts

---

# References

- ai-governance-policy.md
- rag-evaluation-checklist.md
- model-fallback-strategy.md
