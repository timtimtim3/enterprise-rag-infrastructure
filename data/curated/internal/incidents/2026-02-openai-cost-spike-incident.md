---
doc_id: "northstar-incidents-2026-02-openai-cost-spike-incident"
title: "Incident Report — OpenAI Cost Spike"
source_type: internal
doc_type: "incident_report"
status: "current"
authority: "historical_record"
category: "incidents"
folder: "internal/incidents/"
filename: "2026-02-openai-cost-spike-incident.md"
source_path: "internal/incidents/2026-02-openai-cost-spike-incident.md"
organization: "Northstar Solutions"
classification: "internal"
visibility: "employees"
audience:
  - "platform-operations"
  - "engineering"
  - "ai-platform"
effective_from: null
deprecated_at: null
superseded_by: null
applies_to: "current Northstar internal guidance unless superseded"
content_hash: "bf491c464327"
metadata_added_on: "2026-05-25"
---
# Incident Report — OpenAI Cost Spike
Incident ID: INC-2026-0202
Severity: SEV-2

# Summary

Northstar Solutions experienced an unexpected 312% increase in OpenAI API spend over a 48-hour period.

The issue originated from a prompt routing regression in the evaluation pipeline.

---

# Impact

Impacted systems:

- internal evaluation service
- automated regression benchmarking
- customer pilot sandbox environments

No production customer downtime occurred.

Estimated excess cost:

- $48,000

---

# Root Cause

A deployment unintentionally disabled:

- caching layer
- batching optimization
- evaluation sampling controls

As a result:

- duplicate evaluation prompts executed repeatedly
- GPT-4.1 usage increased dramatically
- fallback routing amplified traffic

---

# Contributing Factors

## Missing Budget Alert Thresholds

Spend anomaly thresholds were too high.

---

## Evaluation Traffic Misclassification

Evaluation traffic incorrectly routed as production priority.

---

## Lack of Token Quotas

Evaluation workers lacked hard token caps.

---

# Resolution

Mitigation actions:

- disabled evaluation workers
- restored Redis caching
- added token usage caps
- rerouted evaluation traffic to lower-cost models

---

# Follow-Up Actions

- implement budget circuit breakers
- add provider cost anomaly dashboards
- enforce evaluation environment quotas
- improve model routing validation

---

# Related Documents

- approved-llm-providers.md
- model-fallback-strategy.md
- monitoring-requirements.md
