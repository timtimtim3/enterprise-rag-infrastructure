---
doc_id: "northstar-ai-hallucination-mitigation-policy"
title: "Hallucination Mitigation Policy"
doc_type: "policy"
status: "current"
authority: "authoritative"
category: "ai"
folder: "internal/ai/"
filename: "hallucination-mitigation-policy.md"
source_path: "internal/ai/hallucination-mitigation-policy.md"
organization: "Northstar Solutions"
version: "2.1"
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
content_hash: "45e67625fd19"
metadata_added_on: "2026-05-25"
---
# Hallucination Mitigation Policy
Version: 2.1

# Purpose

Defines hallucination mitigation standards for all AI systems deployed by Northstar Solutions.

---

# Core Principle

LLMs must never be treated as authoritative sources without verification.

All production systems must implement grounding mechanisms.

---

# Required Mitigation Layers

Production systems must include at least three of:

- retrieval grounding
- citation enforcement
- response validation
- confidence scoring
- reranking
- structured outputs
- human review

---

# Citation Requirements

Customer-facing RAG systems must:

- provide source citations
- expose document references
- support retrieval traceability

---

# Confidence Thresholds

Low-confidence responses must:

- abstain
- request clarification
- escalate to human review

---

# High-Risk Domains

Mandatory human review required for:

- legal guidance
- financial recommendations
- healthcare-adjacent workflows
- compliance interpretation

---

# Retrieval Validation

Required validation steps:

1. retrieval completeness
2. metadata verification
3. duplicate chunk suppression
4. reranker evaluation

---

# Prompt Rules

Prompts must:

- explicitly discourage fabrication
- encourage uncertainty acknowledgment
- require citations where applicable

---

# Prohibited Patterns

Disallowed:

- fabricated citations
- unsupported claims
- invisible system prompts containing false authority framing

---

# Monitoring

Required metrics:

- hallucination rate
- unsupported answer rate
- citation mismatch rate
- abstention rate

---

# Incident Escalation

Hallucination incidents impacting customers require:

- incident ticket creation
- root cause analysis
- evaluation dataset update

---

# Related Documents

- rag-evaluation-checklist.md
- ai-governance-policy.md
- prompt-engineering-guide.md
