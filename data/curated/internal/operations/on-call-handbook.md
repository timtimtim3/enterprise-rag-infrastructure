---
doc_id: "northstar-operations-on-call-handbook"
title: "On-Call Handbook"
doc_type: "handbook"
status: "current"
authority: "reference"
category: "operations"
folder: "internal/operations/"
filename: "on-call-handbook.md"
source_path: "internal/operations/on-call-handbook.md"
organization: "Northstar Solutions"
version: "2.1"
owner: "Platform Operations"
classification: "internal"
visibility: "employees"
audience:
  - "platform-operations"
  - "on-call"
  - "engineering"
effective_from: null
deprecated_at: null
superseded_by: null
applies_to: "current Northstar internal guidance unless superseded"
content_hash: "30e019164353"
metadata_added_on: "2026-05-25"
---
# On-Call Handbook
Version: 2.1
Owner: Platform Operations

# Purpose

Defines expectations and procedures for engineers participating in on-call rotations.

---

# Objectives

On-call engineers are responsible for:

- incident response
- production triage
- escalation coordination
- service recovery

---

# Primary Responsibilities

The primary on-call engineer must:

- acknowledge alerts
- investigate incidents
- escalate when necessary
- maintain incident timeline

---

# Escalation Rules

Escalate immediately when:

- customer impact confirmed
- root cause unclear after 30 minutes
- security involvement suspected
- multiple services affected

---

# AI Platform Escalation

Escalate AI Research team for:

- hallucination spikes
- retrieval degradation
- embedding corruption
- reranker instability

---

# Required Tools

On-call engineers must maintain access to:

- AWS console
- monitoring dashboards
- incident management system
- Slack incident channels
- deployment pipeline tools

---

# Alert Fatigue Policy

Low-quality alerts must be reviewed weekly.

Alert owners must:

- tune noisy alerts
- remove non-actionable alerts
- improve signal quality

---

# Handoff Procedures

Shift handoff must include:

- active incidents
- degraded systems
- pending deployments
- unresolved alerts

---

# Incident Notes

All operational actions must be logged in the incident timeline.

Never rely solely on Slack history.

---

# PTO Restrictions

Primary on-call engineers may not take PTO without approved rotation coverage.

---

# Related Documents

- incident-response-process.md
- monitoring-requirements.md
- rollback-procedures.md
