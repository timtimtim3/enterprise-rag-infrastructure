---
doc_id: "northstar-customer-sla-guidelines"
title: "SLA Guidelines"
source_type: internal
doc_type: "standard"
status: "current"
authority: "authoritative"
category: "customer"
folder: "internal/customer/"
filename: "sla-guidelines.md"
source_path: "internal/customer/sla-guidelines.md"
organization: "Northstar Solutions"
version: "1.8"
owner: "Customer Operations"
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
content_hash: "529acd3df8c9"
metadata_added_on: "2026-05-25"
---
# SLA Guidelines
Version: 1.8
Owner: Customer Operations

# Purpose

Defines standard service level agreement (SLA) targets for Northstar Solutions customer deployments.

---

# Availability Targets

## Standard Tier

Availability target:

- 99.5%

---

## Enterprise Tier

Availability target:

- 99.9%

Includes:

- enhanced support
- dedicated escalation path
- priority incident handling

---

# Response Time Targets

## SEV-1

Response target:

- 15 minutes

Update frequency:

- every 30 minutes

---

## SEV-2

Response target:

- 1 hour

---

## SEV-3

Response target:

- next business day

---

# AI Platform Limitations

The following are excluded from SLA guarantees:

- third-party LLM provider outages
- customer-managed infrastructure failures
- unsupported integrations
- customer prompt misconfiguration

---

# Performance Targets

Typical production targets:

- retrieval latency < 500ms
- API response latency < 8 seconds
- ingestion processing < 30 minutes for standard workloads

---

# Maintenance Windows

Standard maintenance windows:

- Saturdays 02:00–05:00 UTC

Emergency maintenance may occur outside scheduled windows during critical incidents.

---

# Support Coverage

Enterprise customers receive:

- 24/7 incident response
- dedicated escalation channel
- quarterly architecture reviews

---

# Related Documents

- support-escalation-flow.md
- production-outage-sop.md
- enterprise-deployment-standards.md
