---
doc_id: "northstar-incidents-2026-03-ecs-deployment-outage"
title: "Incident Report — March ECS Deployment Outage"
source_type: internal
doc_type: "incident_report"
status: "current"
authority: "historical_record"
category: "incidents"
folder: "internal/incidents/"
filename: "2026-03-ecs-deployment-outage.md"
source_path: "internal/incidents/2026-03-ecs-deployment-outage.md"
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
content_hash: "3240ffe6138c"
metadata_added_on: "2026-05-25"
---
# Incident Report — March ECS Deployment Outage
Incident ID: INC-2026-0314
Severity: SEV-1
Date: 2026-03-14

# Summary

A failed ECS deployment caused widespread API instability across multiple customer-facing retrieval systems.

The outage impacted:

- RAG API platform
- ingestion workers
- customer support copilots
- internal engineering assistant

Total impact duration:

- 2 hours 18 minutes

---

# Customer Impact

Affected customers experienced:

- elevated 5xx errors
- failed retrieval requests
- intermittent authentication failures
- degraded AI response quality

Approximately 41% of production traffic was impacted.

---

# Timeline

## 09:12 UTC

Platform Engineering initiated deployment of:

rag-api:v2.18.4

---

## 09:18 UTC

CloudWatch alerts triggered:

- elevated task restart count
- readiness check failures

---

## 09:21 UTC

Customer reports began appearing in support escalation channels.

---

## 09:27 UTC

Incident declared SEV-1.

Incident bridge created.

---

## 09:34 UTC

Rollback initiated.

Rollback partially failed due to incompatible task definition changes.

---

## 10:02 UTC

Root cause identified:

new OpenTelemetry middleware caused container startup deadlock during readiness checks.

---

## 10:41 UTC

Hotfix deployment completed.

---

## 11:30 UTC

Metrics stabilized.

Incident resolved.

---

# Root Cause

The deployment introduced a new tracing middleware dependency which attempted synchronous exporter initialization during FastAPI startup.

Under high-load conditions:

- ECS readiness checks timed out
- tasks cycled continuously
- ALB target registration failed

---

# Contributing Factors

## Missing Staging Load Test

The deployment passed integration testing but did not undergo high-concurrency startup testing.

---

## Aggressive Health Check Thresholds

ECS readiness timeout was too strict for startup recovery behavior.

---

## Rollback Incompatibility

Task definition changes modified environment variable requirements, causing rollback instability.

---

# Resolution

Mitigation actions:

- reverted tracing middleware
- increased readiness grace period
- disabled startup exporter blocking

---

# Follow-Up Actions

## Immediate

- add startup load testing
- validate rollback compatibility
- improve readiness diagnostics

---

## Long-Term

- standardize async telemetry initialization
- add deployment canary stage
- improve ECS rollback automation

---

# Related Documents

- ecs-deployment-procedure.md
- rollback-procedures.md
- logging-tracing-policy.md
