---
doc_id: "northstar-ai-prompt-engineering-guide"
title: "Prompt Engineering Guide"
source_type: internal
doc_type: "knowledge_doc"
status: "current"
authority: "reference"
category: "ai"
folder: "internal/ai/"
filename: "prompt-engineering-guide.md"
source_path: "internal/ai/prompt-engineering-guide.md"
organization: "Northstar Solutions"
version: "2.0"
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
content_hash: "c52af075a2b8"
metadata_added_on: "2026-05-25"
---
# Prompt Engineering Guide
Version: 2.0

# Purpose

Defines prompt engineering standards for AI systems developed at Northstar Solutions.

---

# Core Principles

Prompts should be:

- deterministic
- concise
- testable
- version-controlled

---

# Prompt Structure

Recommended structure:

1. system instructions
2. task description
3. constraints
4. retrieval context
5. output format

---

# Required Constraints

All prompts should include:

- truthfulness guidance
- citation requirements
- uncertainty handling
- formatting expectations

---

# Prompt Versioning

All production prompts require:

- version IDs
- change tracking
- evaluation history

Example:

prompt_version=v12

---

# Retrieval Injection Rules

Retrieved context must:

- remain separated from system prompts
- preserve metadata
- avoid hidden instruction contamination

---

# Disallowed Prompt Patterns

Prohibited:

- emotional manipulation prompts
- deceptive authority framing
- hidden policy overrides
- unrestricted autonomous behavior

---

# Structured Outputs

Preferred output formats:

- JSON
- typed schemas
- markdown tables

Freeform generation discouraged for:

- workflow automation
- integrations
- downstream parsing

---

# Few-Shot Guidance

Few-shot examples should:

- reflect production data patterns
- include edge cases
- avoid leaking sensitive data

---

# Prompt Testing

Required evaluations:

- hallucination testing
- adversarial prompt testing
- regression testing
- latency impact analysis

---

# Related Documents

- hallucination-mitigation-policy.md
- ai-governance-policy.md
- model-fallback-strategy.md
