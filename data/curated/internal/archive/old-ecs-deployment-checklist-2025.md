---
doc_id: "northstar-archive-old-ecs-deployment-checklist"
title: "Old ECS Deployment Checklist (2025)"
source_type: internal
doc_type: "archived_checklist"
status: "archived"
authority: "historical"
category: "archive"
folder: "internal/archive/"
filename: "old-ecs-deployment-checklist-2025.md"
source_path: "internal/archive/old-ecs-deployment-checklist-2025.md"
organization: "Northstar Solutions"
version: "0.9"
owner: "Platform Engineering"
classification: "internal"
visibility: "employees"
audience:
  - "platform-engineering"
effective_from: "2025-02-01"
deprecated_at: "2026-03-14"
superseded_by: "fastapi-deployment-sop.md"
applies_to: "historical deployments only"
reason_deprecated: "Deployment standards consolidated after March ECS outage"
---

# ECS Deployment Checklist (Archived)

> ARCHIVED: Retained for historical incident analysis.

# Legacy Deployment Steps

- manually update ECS task definition
- manually restart unhealthy tasks
- validate ALB registration
- manually inspect CloudWatch logs

---

# Missing Safeguards

This older checklist did not require:

- canary deployments
- startup load testing
- rollback compatibility validation
- OpenTelemetry startup testing

These gaps contributed to the March 2026 deployment incident.
