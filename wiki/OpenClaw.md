# OpenClaw

Open-source coding agent that became the fastest-growing project in its category; ~30K commits and ~2K contributors as of April 2026, now governed by the OpenClaw Foundation and maintained alongside Peter Steinberger's role at OpenAI.

## History and governance

OpenClaw grew from a side project into one of the most active open-source AI engineering repositories. The OpenClaw Foundation was established using the Switzerland model of non-profit open-source governance — independent of any single company, with Peter Steinberger maintaining the project while joining OpenAI.

## Security posture

At the scale OpenClaw operates — 1,142 security advisories filed as of April 2026, 99 rated critical, averaging 16.6 advisories per day — security is the dominant operational concern. The "legal trifecta" refers to the combination of liability exposure, open-source maintainer responsibility, and the security challenges introduced by giving AI agents broad system access. Steinberger describes this as "almost a security nightmare" and considers it one of the hardest unsolved problems in agentic systems.

## Design philosophy

**Taste**: Steinberger defines taste for an AI agent as (a) output that "doesn't stink like AI" — prose and code that doesn't feel machine-generated — and (b) delightful details: small polish decisions that make the product feel intentional. Taste is a judgment applied at the boundaries where the model's defaults would produce adequate-but-forgettable output.

**Saying no**: the most valuable capability in a coding agent is refusing inappropriate requests. An agent that says yes to everything is an agent that can't be trusted with consequential actions. Steinberger considers the quality of refusals — when the agent declines, what it says, how it explains the refusal — a first-class product decision.

**System design still critical**: agent quality is bounded by the system design of the harness, not just the model. OpenClaw invests heavily in the orchestration layer rather than treating the model as the only lever.

## Dreaming feature

A planned OpenClaw capability: periodically reconcile memory fragments from across multiple session logs into coherent, persistent user context. Rather than accumulating disconnected facts per session, the agent "dreams" — runs a consolidation pass over past sessions — to build a more accurate long-term model of the user's codebase and preferences.

## Opinions

- **The hardest part of running an open-source AI agent at scale isn't the AI — it's the security surface** — 99 critical advisories in a codebase designed to execute arbitrary code on user machines creates liability and governance challenges that no open-source project had to navigate before agentic systems. — Peter Steinberger (State of the Claw, AI Engineer 2026), [link](https://www.youtube.com/watch?v=zgNvts_2TUE)

- **Saying no is the most valuable capability you can give an agent** — the ability to refuse confidently and clearly is what separates a trustworthy assistant from a dangerous one; it's a deliberate product investment, not a default. — Peter Steinberger (State of the Claw, AI Engineer 2026), [link](https://www.youtube.com/watch?v=zgNvts_2TUE)

- **Taste in AI output is definable and measurable** — "doesn't stink like AI" is a real quality bar; output that reads as clearly machine-generated, even if technically correct, fails the taste test; delightful details are the positive signal. — Peter Steinberger (State of the Claw, AI Engineer 2026), [link](https://www.youtube.com/watch?v=zgNvts_2TUE)

## Sources

- Peter Steinberger, "State of the Claw", AI Engineer 2026 — [YouTube](https://www.youtube.com/watch?v=zgNvts_2TUE)

## Notes

