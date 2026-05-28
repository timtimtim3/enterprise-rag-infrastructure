---
doc_id: "northstar-ai-approved-llm-providers"
title: "Approved LLM Providers"
source_type: internal
doc_type: "knowledge_doc"
status: "current"
authority: "reference"
category: "ai"
folder: "internal/ai/"
filename: "approved-llm-providers.md"
source_path: "internal/ai/approved-llm-providers.md"
organization: "Northstar Solutions"
version: "2.2"
owner: "AI Governance Council"
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
content_hash: "42df2f8aae32"
metadata_added_on: "2026-05-25"
---
# Approved LLM Providers
Version: 2.2
Owner: AI Governance Council

# Purpose

This document defines the approved large language model (LLM) providers for production and internal systems at Northstar Solutions.

---

# Approved Providers

## Tier 1 — Fully Approved

These providers are approved for production customer workloads.

| Provider | Approved Models | Status |
|---|---|---|
| OpenAI | GPT-4.1, GPT-4o | Approved |
| Anthropic | Claude Sonnet 4 | Approved |
| Google | Gemini 2.5 Pro | Approved |

---

# Tier 2 — Restricted Approval

Restricted approval requires architecture review.

| Provider | Restriction |
|---|---|
| Cohere | Retrieval-only workloads |
| Mistral | Internal experimentation only |
| AWS Bedrock models | Customer-specific approval required |

---

# Disallowed Providers

The following are prohibited for production usage:

- self-hosted open internet models without governance review
- anonymous hosted inference providers
- providers lacking SOC2 compliance
- providers without data retention guarantees

---

# Model Selection Guidance

## Preferred General Reasoning Model

Default:

- GPT-4.1

Use Cases:

- enterprise copilots
- retrieval QA
- workflow orchestration
- structured generation

---

## Preferred Long Context Model

Default:

- Gemini 2.5 Pro

Use Cases:

- large document synthesis
- architecture review
- ADR summarization

---

## Preferred Cost-Efficient Model

Default:

- Claude Sonnet 4

Use Cases:

- internal automation
- evaluation pipelines
- medium-complexity workflows

---

# Customer Data Rules

Customer data may only be sent to providers that support:

- enterprise agreements
- data retention controls
- regional processing requirements

---

# Prompt Retention Rules

Disallowed:

- storing sensitive prompts in third-party telemetry
- training on customer prompts
- uncontrolled provider logging

---

# Required Metadata

All LLM requests must log:

- provider
- model
- token usage
- latency
- prompt version
- retrieval strategy

---

# Failover Requirements

Production AI systems must support:

- provider failover
- timeout recovery
- degraded response handling

---

# Review Process

New providers require:

1. Security review
2. AI governance approval
3. Cost analysis
4. Reliability testing
5. Evaluation benchmark validation

---

# Related Documents

- model-fallback-strategy.md
- ai-governance-policy.md
- rag-evaluation-checklist.md
