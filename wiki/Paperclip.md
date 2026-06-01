# Paperclip

Open-source "human control plane for AI labor" — an org-chart-structured multi-agent harness that assigns roles, skills, and approval workflows to heterogeneous agents from any vendor.

## Architecture

Paperclip models an agent workforce as an org chart. A CEO agent at the root delegates to an executive branch (CTO, CMO, etc.), which delegates to IC agents that do the actual work. Each node in the chart has a defined role, an assigned set of skills, and a reporting relationship that determines where work escalates.

**Skills manager**: assigns capabilities (tools, knowledge bases, instructions) to specific agents in the hierarchy. Skills are decoupled from agents, so the same skill can be granted to multiple roles.

**QA reviewer**: an agent (or human) that reviews another agent's output before it proceeds downstream. Composable: a review step can itself be delegated to a sub-agent.

**Approver workflows**: a human approval gate that blocks execution until explicitly confirmed. Separate from QA — QA evaluates quality, approval enforces policy and accountability.

**Routines**: scheduled tasks defined with template variables; analogous to cron jobs. "Every Monday, generate a weekly report using {{project}} data and send to {{stakeholder}}."

## Vendor neutrality

Paperclip treats the underlying model as a swappable backend. Supported agents include Claude, [OpenAI Codex](OpenAI-Codex.md), Gemini, [Pi](Pi.md), Hermes, and [OpenClaw](OpenClaw.md). The harness owns the org structure, skill routing, and approval logic; the individual agents own task execution.

## Practical application

```bash
npx paperclip-ai onboard
```

Walks through defining the initial org chart and connecting agent backends. Documentation and templates at paperclip.ing.

## Opinions

- **The org-chart model for agent teams is the right abstraction for enterprises** — it maps to existing accountability structures, so humans know who (which agent role) is responsible for a given output. — Dotta & Bippa (Open Source Human Control Plane for AI Labor, AI Engineer 2026), [link](https://www.youtube.com/watch?v=h403btjldDQ)

- **Human approval gates and QA review steps should be first-class primitives in any agent harness** — bolting them on after the fact produces fragile pipelines that bypass safety checks under load. — Dotta & Bippa (Open Source Human Control Plane for AI Labor, AI Engineer 2026), [link](https://www.youtube.com/watch?v=h403btjldDQ)

## Sources

- Dotta & Bippa, "Open Source Human Control Plane for AI Labor", AI Engineer 2026 — [YouTube](https://www.youtube.com/watch?v=h403btjldDQ)

## Notes

