---
doc_id: "northstar-engineering-redis-caching-guidelines"
title: "Redis Caching Guidelines"
source_type: internal
doc_type: "standard"
status: "current"
authority: "authoritative"
category: "engineering"
folder: "internal/engineering/"
filename: "redis-caching-guidelines.md"
source_path: "internal/engineering/redis-caching-guidelines.md"
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
content_hash: "8c282359fc92"
metadata_added_on: "2026-05-25"
---
# Redis Caching Guidelines

# Approved Redis Use Cases

- session caching
- retrieval caching
- rate limiting
- distributed locking
- conversation state

---

# Disallowed Usage

- permanent persistence
- long-term analytics storage
- embedding storage

---

# TTL Standards

Default TTL:

- 1 hour

Conversation memory TTL:

- 24 hours

Retrieval cache TTL:

- 15 minutes

---

# Key Naming Standards

Format:

service:environment:resource:id

Example:

rag-prod-session:user_123

---

# Memory Protection

Maximum memory policy:

allkeys-lru

---

# Operational Rules

Redis outages must never fully break customer-facing APIs.

All services must support:

- degraded mode
- retry logic
- timeout fallback

---

# Monitoring Requirements

Required metrics:

- memory usage
- eviction rate
- latency
- connection count
