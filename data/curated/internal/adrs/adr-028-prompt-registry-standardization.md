---
doc_id: "northstar-adrs-adr-028-prompt-registry-standardization"
title: "ADR-028 — Prompt Registry Standardization"
doc_type: "adr"
status: "current"
authority: "decision_record"
category: "adrs"
folder: "internal/adrs/"
filename: "adr-028-prompt-registry-standardization.md"
source_path: "internal/adrs/adr-028-prompt-registry-standardization.md"
organization: "Northstar Solutions"
classification: "internal"
visibility: "employees"
audience:
  - "engineering"
  - "architecture-review"
  - "ai-platform"
effective_from: null
deprecated_at: null
superseded_by: null
applies_to: "current Northstar internal guidance unless superseded"
content_hash: "aa7b40820c40"
metadata_added_on: "2026-05-25"
---
# ADR-028 — Prompt Registry Standardization
Status: Accepted

# Context

Prompt definitions were historically scattered across:

- application repositories
- environment variables
- hardcoded orchestration flows

This caused:

- inconsistent evaluations
- rollback difficulty
- auditability problems

---

# Decision

Northstar Solutions will standardize on centralized prompt registry management.

All production prompts must support:

- version IDs
- rollback history
- evaluation linkage
- ownership metadata

---

# Consequences

## Positive

- improved rollback safety
- stronger governance
- reproducible evaluations

---

## Negative

- increased operational overhead
- prompt migration effort

---

# Related Documents

- prompt-engineering-guide.md
- ai-governance-policy.md
- rollback-procedures.md
