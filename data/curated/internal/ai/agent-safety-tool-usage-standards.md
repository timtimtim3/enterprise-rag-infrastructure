---
doc_id: "northstar-ai-agent-safety-tool-usage-standards"
title: "Agent Safety & Tool Usage Standards"
source_type: internal
doc_type: "standard"
status: "current"
authority: "authoritative"
category: "ai"
folder: "internal/ai/"
filename: "agent-safety-tool-usage-standards.md"
source_path: "internal/ai/agent-safety-tool-usage-standards.md"
organization: "Northstar Solutions"
classification: "internal"
visibility: "employees"
audience:
  - "ai-platform"
  - "ai-governance"
  - "engineering"
effective_from: null
deprecated_at: null
superseded_by: null
applies_to: "current Northstar internal guidance unless superseded"
content_hash: "fd8b6858b3d9"
metadata_added_on: "2026-05-25"
---
# Agent Safety & Tool Usage Standards

# Purpose

Defines operational safety standards for AI agents and tool-enabled workflows.

---

# Approved Agent Capabilities

Approved:

- retrieval
- summarization
- workflow orchestration
- ticket drafting
- documentation analysis

Restricted:

- infrastructure changes
- customer account modification
- production database writes

---

# Tool Invocation Rules

All tools must support:

- authentication
- authorization
- audit logging
- timeout limits

---

# Human Approval Requirements

Human approval mandatory for:

- deleting resources
- modifying production systems
- sending external customer communications
- security-sensitive operations

---

# Sandbox Requirements

Experimental agents must run in:

- isolated environments
- restricted credentials
- non-production datasets

---

# Prompt Injection Defense

Agents must:

- isolate retrieved content
- prevent instruction override
- validate tool invocation permissions

---

# Auditability

All agent actions must log:

- tool called
- arguments
- execution result
- timestamp
- trace ID

---

# Multi-Agent Restrictions

Disallowed without governance review:

- autonomous agent delegation
- recursive self-invocation
- uncontrolled agent spawning

---

# Escalation Requirements

Agents must escalate to humans when:

- confidence below threshold
- conflicting retrievals detected
- authorization unclear
- destructive action requested

---

# Related Documents

- ai-governance-policy.md
- prompt-engineering-guide.md
- hallucination-mitigation-policy.md
