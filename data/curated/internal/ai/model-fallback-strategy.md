---
doc_id: "northstar-ai-model-fallback-strategy"
title: "Model Fallback Strategy"
source_type: internal
doc_type: "knowledge_doc"
status: "current"
authority: "reference"
category: "ai"
folder: "internal/ai/"
filename: "model-fallback-strategy.md"
source_path: "internal/ai/model-fallback-strategy.md"
organization: "Northstar Solutions"
version: "1.7"
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
content_hash: "fbd672638170"
metadata_added_on: "2026-05-25"
---
# Model Fallback Strategy
Version: 1.7

# Purpose

Defines fallback strategies for production AI systems.

---

# Objectives

Fallback systems must ensure:

- high availability
- graceful degradation
- cost control
- customer continuity

---

# Standard Fallback Hierarchy

Primary:

- GPT-4.1

Secondary:

- Claude Sonnet 4

Tertiary:

- Gemini 2.5 Pro

---

# Fallback Triggers

Fallback activation conditions:

- provider outage
- elevated latency
- rate limiting
- token quota exhaustion
- malformed responses

---

# Timeout Standards

Primary model timeout:

- 30 seconds

Fallback activation timeout:

- 10 seconds

---

# Graceful Degradation

When all premium models fail:

Allowed degraded modes:

- retrieval-only responses
- summarization-only mode
- reduced-context responses

---

# Circuit Breakers

Systems must support:

- provider-specific circuit breakers
- retry backoff
- temporary provider suppression

---

# Logging Requirements

Fallback events must log:

- failed provider
- fallback provider
- latency
- request ID
- customer impact level

---

# Evaluation Requirements

Fallback models must pass:

- hallucination benchmarks
- latency thresholds
- retrieval grounding tests

---

# Customer Communication

Customer-facing systems should disclose:

- degraded functionality
- delayed responses
- temporary reduced capabilities

---

# Related Documents

- approved-llm-providers.md
- ai-evaluation-standards.md
- logging-tracing-policy.md
