---
doc_id: "northstar-engineering-service-ownership-registry"
title: "Service Ownership Registry"
source_type: internal
doc_type: "knowledge_doc"
status: "current"
authority: "reference"
category: "engineering"
folder: "internal/engineering/"
filename: "service-ownership-registry.md"
source_path: "internal/engineering/service-ownership-registry.md"
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
content_hash: "7d0e1194db3a"
metadata_added_on: "2026-05-25"
---
# Service Ownership Registry

# Critical Services

| Service | Owner | Criticality |
|---|---|---|
| rag-api | AI Platform | High |
| ingestion-worker | Data Platform | High |
| evaluation-service | AI Research | Medium |
| auth-gateway | Platform Security | Critical |
| agent-runtime | AI Platform | Critical |

---

# Escalation Channels

| Team | Slack Channel |
|---|---|
| Platform Engineering | #platform-alerts |
| AI Platform | #ai-platform |
| Security | #security-incidents |

---

# Ownership Rules

Every production service must define:

- primary owner
- secondary owner
- escalation channel
- deployment approver
- on-call rotation
