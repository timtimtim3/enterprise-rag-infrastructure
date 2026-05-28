---
doc_id: "northstar-engineering-fastapi-deployment-sop"
title: "FastAPI Deployment SOP"
source_type: internal
doc_type: "procedure"
status: "current"
authority: "authoritative"
category: "engineering"
folder: "internal/engineering/"
filename: "fastapi-deployment-sop.md"
source_path: "internal/engineering/fastapi-deployment-sop.md"
organization: "Northstar Solutions"
version: "1.9"
owner: "Platform Engineering"
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
content_hash: "24ccd24c98dc"
metadata_added_on: "2026-05-25"
---
# FastAPI Deployment SOP
Version: 1.9
Owner: Platform Engineering

# Overview

This document describes the standard deployment process for FastAPI services at Northstar Solutions.

---

# Deployment Platform

Production workloads are deployed to:

- AWS ECS Fargate

Non-production environments:

- shared ECS staging cluster
- ephemeral preview environments

---

# Required Components

Every service deployment must include:

- Docker image
- ECS task definition
- CloudWatch log group
- ALB target group
- health checks
- OpenTelemetry instrumentation

---

# Build Pipeline

CI stages:

1. lint
2. unit tests
3. security scan
4. container build
5. integration tests
6. image signing
7. deployment approval

Main branch deployments require:

- 2 approving reviews
- passing integration tests

---

# Docker Standards

Base image:

python:3.11-slim

Container rules:

- run as non-root
- no embedded secrets
- image size < 1.5GB
- deterministic dependency versions

---

# ECS Configuration Standards

Minimum task requirements:

- 1 vCPU
- 2GB RAM

LLM orchestration services:

- minimum 4GB RAM

---

# Rolling Deployment Strategy

Deployment type:

- ECS rolling deployment

Defaults:

- minimum healthy percent: 100
- maximum percent: 200

This ensures zero-downtime deployments.

---

# Health Checks

Readiness endpoint:

/health/ready

Liveness endpoint:

/health/live

Deployment fails automatically if readiness checks fail for 5 minutes.

---

# Secrets Management

Secrets must come from:

- AWS Secrets Manager

Never allowed:

- .env production secrets
- hardcoded credentials
- plaintext API keys

---

# Environment Variables

Required environment variables:

- ENVIRONMENT
- SERVICE_NAME
- AWS_REGION
- OTEL_EXPORTER_OTLP_ENDPOINT

Optional:

- FEATURE_FLAGS
- MODEL_PROVIDER_OVERRIDE

---

# Rollback Procedure

Rollback triggers:

- elevated 5xx errors
- latency increase > 40%
- retrieval failure spikes
- customer-impacting incidents

Rollback steps:

1. halt deployment
2. restore prior ECS task revision
3. invalidate unhealthy tasks
4. verify health checks
5. notify incident channel

---

# Production Approval Rules

Production deployment approval required from:

- platform engineering
- owning application team

Critical AI services additionally require:

- AI governance approval

---

# Deployment Windows

Preferred deployment windows:

- Tue–Thu
- 09:00–15:00 UTC

Restricted:

- Fridays
- customer blackout periods
- active incident windows

---

# Observability Requirements

All services must expose:

- request latency
- error rate
- token usage
- retrieval metrics
- downstream dependency latency

---

# References

- ecs-deployment-procedure.md
- logging-tracing-policy.md
- production-outage-sop.md
