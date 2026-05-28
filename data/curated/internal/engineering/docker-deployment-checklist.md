---
doc_id: "northstar-engineering-docker-deployment-checklist"
title: "Docker Deployment Checklist"
source_type: internal
doc_type: "checklist"
status: "current"
authority: "authoritative"
category: "engineering"
folder: "internal/engineering/"
filename: "docker-deployment-checklist.md"
source_path: "internal/engineering/docker-deployment-checklist.md"
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
content_hash: "5a7ae6ba4452"
metadata_added_on: "2026-05-25"
---
# Docker Deployment Checklist

# Pre-Deployment Checklist

## Security

- [ ] No hardcoded secrets
- [ ] Non-root user configured
- [ ] Minimal base image
- [ ] Vulnerability scan passed
- [ ] Dependency versions pinned

---

## Runtime

- [ ] Health endpoints configured
- [ ] Logging outputs to stdout
- [ ] Graceful shutdown enabled
- [ ] Request timeout configured

---

## Build

- [ ] Multi-stage build enabled
- [ ] Image size validated
- [ ] CI build reproducible
- [ ] Dockerignore configured

---

## AI Services

- [ ] Model provider keys loaded from Secrets Manager
- [ ] Token usage logging enabled
- [ ] Retrieval metrics enabled
- [ ] Prompt version tracking enabled

---

## Deployment

- [ ] ECS task definition updated
- [ ] Environment variables validated
- [ ] Rollback revision available
- [ ] Monitoring dashboard updated
