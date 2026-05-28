---
doc_id: "northstar-engineering-ecs-deployment-procedure"
title: "ECS Deployment Procedure"
source_type: internal
doc_type: "procedure"
status: "current"
authority: "authoritative"
category: "engineering"
folder: "internal/engineering/"
filename: "ecs-deployment-procedure.md"
source_path: "internal/engineering/ecs-deployment-procedure.md"
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
content_hash: "569b5ef0e963"
metadata_added_on: "2026-05-25"
---
# ECS Deployment Procedure

# Standard Architecture

Northstar Solutions deploys workloads using:

- ECS Fargate
- ALB ingress
- CloudWatch logging
- OpenTelemetry tracing

---

# Deployment Flow

1. CI pipeline builds image
2. Image pushed to ECR
3. ECS task definition updated
4. Rolling deployment initiated
5. Health checks validated
6. Metrics monitored
7. Deployment finalized

---

# Scaling Standards

Minimum production replicas:

- 2

Critical AI services:

- 3 minimum

---

# Autoscaling Metrics

Primary metrics:

- CPU
- memory
- request latency
- queue depth

AI inference services additionally scale on:

- token throughput
- active graph executions

---

# Regional Deployment Rules

Default region:

eu-west-1

Customer-regulated workloads may deploy to:

- us-east-1
- eu-central-1

---

# Failure Handling

Deployment auto-aborts when:

- unhealthy tasks exceed threshold
- error rate spikes
- readiness checks fail

---

# Rollback Authority

Rollback approval owners:

- incident commander
- platform engineering lead
