---
doc_id: "northstar-engineering-api-development-standards"
title: "Northstar Solutions — API Development Standards"
source_type: internal
doc_type: "standard"
status: "current"
authority: "authoritative"
category: "engineering"
folder: "internal/engineering/"
filename: "api-development-standards.md"
source_path: "internal/engineering/api-development-standards.md"
organization: "Northstar Solutions"
version: "2.4"
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
content_hash: "adcfe4252b65"
metadata_added_on: "2026-05-25"
---
# Northstar Solutions — API Development Standards
Version: 2.4
Owner: Platform Engineering
Last Updated: 2026-02-11

---

# Purpose

This document defines the internal API development standards used across all Northstar Solutions backend services.

These standards apply to:

- FastAPI services
- internal microservices
- customer-facing APIs
- AI orchestration services
- retrieval services
- agent runtime APIs

The goal is to ensure:

- consistency
- observability
- maintainability
- security
- deployment reliability
- interoperability across teams

---

# Core Principles

## 1. APIs Must Be Stateless

All HTTP services must be stateless.

Session state must never be stored in application memory.

Allowed state stores:

- Redis
- PostgreSQL
- Qdrant metadata
- S3 object storage

Disallowed:

- in-memory session caches
- local file persistence
- sticky-session assumptions

---

## 2. All APIs Must Be Versioned

Required path convention:

/api/v1/
/api/v2/

Example:

/api/v1/embeddings/search

Versionless APIs are prohibited in production environments.

---

# Standard FastAPI Layout

Required project structure:

```txt
app/
  api/
  services/
  repositories/
  middleware/
  models/
  schemas/
  core/
  workers/
```

Rules:

- API routers must remain thin
- business logic belongs in services/
- database access belongs in repositories/
- environment configuration belongs in core/

---

# Response Standards

## Standard Success Response

```json
{
  "status": "success",
  "data": {},
  "request_id": "req_123"
}
```

## Standard Error Response

```json
{
  "status": "error",
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Missing required field"
  },
  "request_id": "req_123"
}
```

---

# Authentication Requirements

All production APIs must support one of:

- OAuth2
- JWT bearer auth
- customer API keys via gateway

Internal service-to-service traffic must use:

- signed JWTs
- mTLS for sensitive workloads

Disallowed:

- shared static credentials
- hardcoded API tokens
- plaintext secrets in repositories

---

# Timeout Standards

Default service timeout:

- 30 seconds

LLM inference timeout:

- 120 seconds

Vector retrieval timeout:

- 10 seconds

Redis timeout:

- 2 seconds

Timeouts exceeding these values require architecture review approval.

---

# Pagination Standards

All list endpoints must support:

- limit
- offset
- cursor pagination for large datasets

Maximum page size:

- 500

---

# Logging Requirements

All APIs must emit structured JSON logs.

Required fields:

- timestamp
- service_name
- environment
- request_id
- customer_id
- route
- latency_ms
- status_code

PII must never appear in logs.

---

# OpenTelemetry Requirements

All production APIs must support:

- distributed tracing
- span propagation
- trace correlation

Required headers:

- traceparent
- x-request-id

---

# Deployment Requirements

Every API service must include:

- Dockerfile
- health endpoint
- readiness endpoint
- ECS task definition
- CI validation
- rollback configuration

---

# Health Endpoint Standards

Required endpoints:

/health/live
/health/ready

Liveness checks:

- application process alive

Readiness checks:

- Redis connectivity
- PostgreSQL connectivity
- vector database connectivity
- model provider availability

---

# Rate Limiting

Customer-facing APIs must implement:

- token-based rate limiting
- burst protection
- abuse monitoring

Default limit:

- 100 requests/minute

---

# AI Endpoint Standards

LLM-backed endpoints must:

- return model metadata
- support traceability
- expose prompt version IDs
- support evaluation tagging

Required metadata:

```json
{
  "model": "gpt-4.1",
  "prompt_version": "v12",
  "retrieval_strategy": "hybrid-rag"
}
```

---

# Security Review Requirements

Security review is mandatory when:

- introducing new auth flows
- handling PHI/PII
- enabling external integrations
- deploying customer-specific agents

---

# Approved Languages

Production backend services:

- Python
- TypeScript (limited approval)

Experimental only:

- Go
- Rust

---

# Documentation Requirements

Every production API must include:

- OpenAPI spec
- deployment runbook
- rollback procedure
- ownership metadata
- escalation contacts

---

# Ownership Metadata

Every service must define:

- owning team
- primary on-call rotation
- Slack escalation channel
- business criticality level

Example:

```yaml
owner_team: platform-engineering
criticality: high
slack_channel: #api-platform-alerts
```

---

# References

Related Documents:

- ecs-deployment-procedure.md
- logging-tracing-policy.md
- incident-response-handbook.md
- ai-evaluation-standards.md
