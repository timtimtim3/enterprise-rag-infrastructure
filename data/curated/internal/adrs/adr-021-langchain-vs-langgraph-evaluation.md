---
doc_id: "northstar-adrs-adr-021-langchain-vs-langgraph-evaluation"
title: "ADR-021 — LangChain vs LangGraph Evaluation"
source_type: internal
doc_type: "adr"
status: "current"
authority: "decision_record"
category: "adrs"
folder: "internal/adrs/"
filename: "adr-021-langchain-vs-langgraph-evaluation.md"
source_path: "internal/adrs/adr-021-langchain-vs-langgraph-evaluation.md"
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
content_hash: "e0aba6631414"
metadata_added_on: "2026-05-25"
---
# ADR-021 — LangChain vs LangGraph Evaluation
Status: Accepted
Date: 2026-01-19

# Context

Northstar Solutions evaluated orchestration frameworks for complex AI workflows.

Primary candidates:

- LangChain
- LangGraph

Evaluation focused on:

- state management
- workflow observability
- retry orchestration
- agent control
- production debugging

---

# Decision

LangGraph is the preferred orchestration framework for multi-step AI systems.

LangChain remains approved for lightweight chains and utility abstractions.

---

# Evaluation Findings

## LangChain Strengths

- rapid prototyping
- broad ecosystem support
- simpler learning curve

---

## LangChain Weaknesses

- difficult debugging for complex workflows
- implicit execution flow
- limited durable state handling

---

## LangGraph Strengths

- explicit graph architecture
- deterministic workflow execution
- better recovery semantics
- stronger observability support

---

## LangGraph Weaknesses

- increased implementation complexity
- steeper onboarding curve

---

# Production Considerations

Platform Engineering strongly preferred explicit graph execution due to improved incident debugging capabilities.

AI Research reported:

- lower orchestration instability
- easier retry handling
- improved human-in-the-loop integration

---

# Consequences

## Positive

- improved workflow observability
- better failure recovery
- cleaner escalation patterns

---

## Negative

- increased implementation complexity
- additional developer onboarding time

---

# Related Documents

- langgraph-workflow-patterns.md
- ai-governance-policy.md
- agent-safety-tool-usage-standards.md
