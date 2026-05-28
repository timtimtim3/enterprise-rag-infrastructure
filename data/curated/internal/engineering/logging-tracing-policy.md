---
doc_id: "northstar-engineering-logging-tracing-policy"
title: "Logging & Tracing Policy"
source_type: internal
doc_type: "policy"
status: "current"
authority: "authoritative"
category: "engineering"
folder: "internal/engineering/"
filename: "logging-tracing-policy.md"
source_path: "internal/engineering/logging-tracing-policy.md"
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
content_hash: "39a7d885465e"
metadata_added_on: "2026-05-25"
---
# Logging & Tracing Policy

# Purpose

Defines observability standards for all production services.

---

# Logging Format

All logs must be JSON structured logs.

Required fields:

- timestamp
- level
- service_name
- request_id
- trace_id
- customer_id
- environment

---

# Sensitive Data Rules

Disallowed in logs:

- API keys
- passwords
- customer secrets
- raw PHI
- full prompts containing sensitive customer data

---

# Trace Requirements

All distributed systems must propagate:

- traceparent
- x-request-id

---

# OpenTelemetry

Required for:

- APIs
- retrieval systems
- agent orchestration
- background workers

---

# Retention Policy

Production logs:

- 30 days hot storage
- 180 days archive

---

# Incident Requirements

During incidents:

- DEBUG logging may be temporarily enabled
- retention exceptions require approval

---

# AI-Specific Metrics

Required AI metrics:

- token usage
- model latency
- retrieval latency
- hallucination flags
- fallback events

---

# Alerting Standards

Critical alerts:

- p95 latency spikes
- elevated 5xx rate
- vector DB failures
- LLM provider failures
