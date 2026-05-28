---
doc_id: "northstar-hr-access-request-process"
title: "Access Request Process"
source_type: internal
doc_type: "procedure"
status: "current"
authority: "authoritative"
category: "hr"
folder: "internal/hr/"
filename: "access-request-process.md"
source_path: "internal/hr/access-request-process.md"
organization: "Northstar Solutions"
version: "2.3"
owner: "IT Operations"
classification: "internal"
visibility: "employees"
audience:
  - "all-employees"
  - "people-operations"
effective_from: null
deprecated_at: null
superseded_by: null
applies_to: "current Northstar internal guidance unless superseded"
content_hash: "b97b93d89d8d"
metadata_added_on: "2026-05-25"
---
# Access Request Process
Version: 2.3
Owner: IT Operations

# Purpose

This document defines how employees request, approve, modify, and revoke access to Northstar systems.

---

# Supported Access Types

Employees may request access to:

- Google Workspace
- Slack
- GitHub
- AWS
- Qdrant
- customer environments
- monitoring dashboards
- internal documentation systems

---

# Access Principles

Northstar follows least-privilege access.

Employees should only receive access required for their role and active project assignments.

---

# Request Workflow

All access requests must be submitted through the internal access request form.

Required fields:

- requester
- manager
- system requested
- business justification
- access duration
- customer/project name if applicable

---

# Approval Requirements

## Standard Internal Tools

Approved by:

- direct manager

## Engineering Systems

Approved by:

- direct manager
- system owner

## Production Infrastructure

Approved by:

- manager
- platform engineering lead
- security reviewer

## Customer Environments

Approved by:

- delivery lead
- customer owner
- security reviewer

---

# AWS Access

AWS access must use:

- SSO
- role-based permissions
- MFA

Long-lived IAM users are prohibited.

Production AWS access expires after 30 days unless renewed.

---

# GitHub Access

GitHub access is granted by team membership.

Repository admin access requires Platform Engineering approval.

---

# Emergency Access

Emergency production access may be granted during incidents.

Requirements:

- incident ticket
- incident commander approval
- automatic expiration
- post-incident review

---

# Access Review

Access reviews occur:

- quarterly for production systems
- monthly for customer environments
- after employee role changes

---

# Offboarding

People Operations must trigger access removal on the employee’s final working day.

Critical systems must be revoked immediately.

---

# Related Documents

- employee-onboarding-guide.md
- remote-work-policy.md
- incident-response-handbook.md
