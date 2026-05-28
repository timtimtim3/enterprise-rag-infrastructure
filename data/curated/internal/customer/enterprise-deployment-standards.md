---
doc_id: "northstar-customer-enterprise-deployment-standards"
title: "Enterprise Deployment Standards"
source_type: internal
doc_type: "standard"
status: "current"
authority: "authoritative"
category: "customer"
folder: "internal/customer/"
filename: "enterprise-deployment-standards.md"
source_path: "internal/customer/enterprise-deployment-standards.md"
organization: "Northstar Solutions"
version: "2.0"
owner: "Platform Engineering"
classification: "internal"
visibility: "employees"
audience:
  - "customer-delivery"
  - "customer-success"
  - "platform"
effective_from: null
deprecated_at: null
superseded_by: null
applies_to: "current Northstar internal guidance unless superseded"
content_hash: "87275a3e7610"
metadata_added_on: "2026-05-25"
---
# Enterprise Deployment Standards
Version: 2.0
Owner: Platform Engineering

# Purpose

Defines deployment standards for enterprise customer AI platforms.

---

# Approved Deployment Models

Supported deployment options:

- Northstar-managed AWS
- customer-owned AWS
- hybrid deployment
- private VPC deployment

---

# Standard Architecture Components

Typical deployments include:

- ECS services
- Qdrant cluster
- PostgreSQL
- Redis
- OpenTelemetry stack
- API gateway

---

# Security Standards

Enterprise deployments must support:

- SSO
- MFA
- encryption at rest
- encryption in transit
- audit logging

---

# Network Standards

Recommended architecture:

- private subnets
- restricted ingress
- VPC peering where required
- outbound egress controls

---

# AI Governance Requirements

Production deployments require:

- hallucination monitoring
- prompt version tracking
- model auditability
- retrieval traceability

---

# Regional Restrictions

Customer workloads may require region-specific deployment for:

- GDPR
- financial compliance
- healthcare restrictions

---

# Monitoring Requirements

Enterprise deployments must expose:

- service health
- retrieval metrics
- token usage
- provider latency
- deployment status

---

# Related Documents

- customer-onboarding-process.md
- ai-governance-policy.md
- monitoring-requirements.md
