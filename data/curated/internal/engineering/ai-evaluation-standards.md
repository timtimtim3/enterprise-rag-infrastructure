---
doc_id: "northstar-engineering-ai-evaluation-standards"
title: "AI Evaluation Standards"
source_type: internal
doc_type: "standard"
status: "current"
authority: "authoritative"
category: "engineering"
folder: "internal/engineering/"
filename: "ai-evaluation-standards.md"
source_path: "internal/engineering/ai-evaluation-standards.md"
organization: "Northstar Solutions"
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
content_hash: "647931f4e1a4"
metadata_added_on: "2026-05-25"
---
# AI Evaluation Standards

# Purpose

This document defines evaluation requirements for production AI systems.

---

# Core Metrics

Required metrics:

- hallucination rate
- answer relevancy
- retrieval precision
- citation accuracy
- latency
- cost per request

---

# Hallucination Thresholds

Customer-facing systems:

< 3%

Internal copilots:

< 8%

---

# Evaluation Dataset Rules

Datasets must include:

- factual questions
- ambiguous questions
- adversarial prompts
- multi-document retrieval

---

# Human Review

Mandatory for:

- legal workflows
- financial outputs
- healthcare-adjacent systems

---

# RAG Evaluation Standards

All retrieval systems must evaluate:

- chunk quality
- reranker quality
- citation correctness
- retrieval recall

---

# Benchmark Frequency

Production evaluations:

- weekly

Major model changes:

- mandatory regression evaluation

---

# Approved Models

Current preferred models:

- GPT-4.1
- Claude Sonnet
- Gemini 2.5 Pro

Experimental models require governance approval.
