# Demand-Driven Context

A methodology for building coherent enterprise knowledge bases for agents by inverting the typical push strategy: instead of pre-loading all institutional knowledge, agents are given real tasks, allowed to fail, and their failures are used to surface and document what is actually missing.

## The problem it addresses

Enterprise institutional knowledge is typically: ~20% outdated, ~20% unreliable, ~10% duplicated, and ~40% tribal (never documented at all). Plugging MCP servers or RAG pipelines onto this monolith produces unreliable, untested context — agents get 10–30% accuracy and the human ends up doing the data entry work to fill gaps. The underlying knowledge base is the bottleneck, not the retrieval layer.

Analogy: institutional knowledge is a monolith that needs to be decomposed into focused "context blocks" (like a monolith-to-microservices migration) before retrieval can work reliably.

## The methodology

**Pull strategy vs. push strategy**: Rather than pre-loading all documentation into the agent's context (push), give the agent a task item, let it fail, and let it surface what it needs (pull). Modelled on how a new employee is onboarded: give them a task, let them ask questions, encourage them to document what they learn.

**One demand-driven cycle**:
1. Assign a real problem to the agent (a Jira ticket, incident, support request).
2. Agent attempts the task and fails — lists what it couldn't find (undocumented terminology, missing business logic, unknown system relationships).
3. Domain expert fills in the gaps from tribal knowledge.
4. Agent documents the new knowledge into structured context blocks.
5. Repeat with the next problem.

TDD analogy: write failing "tests" (task failures) first; implement the "code" (documentation) to make them pass. After 14+ cycles, confidence scores in the demo climbed from ~1.5/5 to ~4.4/5.

**Agent shifts roles**: from knowledge consumer to knowledge manager. The agent surfaces gaps, receives answers, and maintains its own knowledge base — rather than the human managing it.

## Context gap scanner

An automated version that eliminates the need for a human to sit through each cycle manually:

1. Take archived work items (Jira, incidents, support tickets) — they already represent the real demand on the knowledge base.
2. Agent generates "probes" — minimal tests of the knowledge base against each work item.
3. Agent runs probes and classifies each knowledge gap as: **clean** (documented and current), **stale** (outdated), **incomplete**, or **missing/tribal**.
4. Consolidates into a prioritized Kanban of documentation work items (critical / high / medium) based on frequency across incidents.

**Scale**: ~96K tokens per domain when aggregating Confluence, GitHub, and Slack context; fits within modern context windows without RAG for a single team's domain.

**Storage**: knowledge output stored in GitHub, using the PR/review workflow for multi-agent/multi-team contribution conflict resolution. Curated documents tagged with creation date and freshness state (active / stale / clean).

## Meta-model (optional add-on)

A structured map of relationships between business processes, systems, APIs, and terminology. Helps agents navigate the knowledge base spatially (like a filesystem encoding relationships) rather than treating it as a flat document dump. Not required for the methodology but increases value: the agent can infer which systems are affected when a business process changes.

## Sources

- Raj (staff software engineer, IKEA), "Demand-Driven Context: A Methodology for Coherent Knowledge Bases Through Agent Failure", AI Engineer 2026 — [https://www.youtube.com/watch?v=_QAVExf_1uw](https://www.youtube.com/watch?v=_QAVExf_1uw)

## Notes
