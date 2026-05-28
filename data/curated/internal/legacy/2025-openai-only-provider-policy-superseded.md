---
doc_id: "northstar-legacy-openai-only-policy"
title: "OpenAI-Only Provider Policy"
source_type: internal
doc_type: "legacy_policy"
status: "superseded"
authority: "historical"
category: "legacy"
folder: "internal/legacy/"
filename: "2025-openai-only-provider-policy-superseded.md"
source_path: "internal/legacy/2025-openai-only-provider-policy-superseded.md"
organization: "Northstar Solutions"
version: "1.1"
owner: "AI Governance Council"
classification: "internal"
visibility: "employees"
audience:
  - "ai-platform"
  - "engineering"
effective_from: "2025-01-15"
deprecated_at: "2025-10-02"
superseded_by: "approved-llm-providers.md"
applies_to: "historical reference only"
reason_deprecated: "Multi-provider strategy adopted for resilience and cost optimization"
---

# OpenAI-Only Provider Policy (Superseded)

> WARNING: This policy is superseded and no longer represents current provider standards.

# Policy

All production AI systems must use OpenAI-hosted models exclusively.

Approved model family:

- GPT-4
- GPT-4 Turbo

---

# Rationale

The organization standardized on OpenAI because:

- strongest reasoning quality
- ecosystem maturity
- operational simplicity

---

# Limitations

Known concerns:

- vendor lock-in risk
- limited failover flexibility
- escalating inference cost

---

# Historical Context

This policy was replaced after the February 2026 cost spike incident and provider resiliency reviews.
