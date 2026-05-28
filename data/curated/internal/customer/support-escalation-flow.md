---
doc_id: "northstar-customer-support-escalation-flow"
title: "Support Escalation Flow"
source_type: internal
doc_type: "knowledge_doc"
status: "current"
authority: "reference"
category: "customer"
folder: "internal/customer/"
filename: "support-escalation-flow.md"
source_path: "internal/customer/support-escalation-flow.md"
organization: "Northstar Solutions"
version: "1.9"
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
content_hash: "4f5c3bb0d215"
metadata_added_on: "2026-05-25"
---
# Support Escalation Flow
Version: 1.9
Owner: Customer Operations

# Purpose

Defines the escalation process for customer support issues.

---

# Escalation Levels

## Level 1 — Support Desk

Handles:

- onboarding questions
- user access issues
- basic troubleshooting
- ingestion requests

---

## Level 2 — Platform Engineering

Handles:

- deployment issues
- infrastructure incidents
- retrieval failures
- authentication problems

---

## Level 3 — AI Platform Team

Handles:

- hallucination incidents
- prompt failures
- reranker issues
- model provider instability

---

# Escalation Triggers

Immediate escalation required for:

- production outages
- security concerns
- customer data exposure
- failed deployments

---

# Communication Standards

All escalations must include:

- customer name
- impact summary
- severity level
- affected systems
- timeline

---

# SEV-1 Workflow

1. Create incident bridge
2. Assign incident commander
3. Notify executive stakeholders
4. Provide customer updates every 30 minutes

---

# Customer Escalation Contacts

Enterprise customers receive:

- dedicated Slack channel
- escalation email alias
- named delivery lead

---

# Related Documents

- incident-response-process.md
- sla-guidelines.md
- production-outage-sop.md
