# Context-Rot

Degradation in LLM output quality as the context window fills, even when total token count remains within stated model limits. Manifests as lost coherence, forgotten earlier reasoning, post-compaction regressions, and reduced instruction-following fidelity.

## Mechanism

LLMs do not treat all tokens in their context window equally. Empirically, attention to earlier tokens weakens as the window fills. Before the context limit is hit, models begin to lose track of decisions, constraints, and reasoning established early in the conversation. When a tool like Claude Code triggers compaction — summarising prior turns to free context space — the compressed representation discards nuance, and the model effectively starts reasoning from a degraded state.

The rot is not a binary cliff. It is progressive: coherence and instruction-following erode gradually as the window fills, then drop sharply at compaction. A long-running agent that appears to be working correctly may already be in a partially-rotted state before compaction fires.

## Concrete example

Jacob Lauritzen (CTO, Legora) describes a representative failure: a legal agent is tasked with drafting a contract, runs for 30 minutes across multiple sub-agents, and produces a result. The human reviewer spots a problem in clause 3 and asks for a targeted correction. The agent agrees. Compaction fires. The agent continues and delivers a revised contract — but the correction to clause 3 came at the cost of regressions elsewhere. Clauses that were correct before are now wrong. The context rot consumed the reasoning that was holding them in place.

## Contrast with adjacent ideas

**Context window exhaustion** is a hard limit — the model cannot accept more tokens. Context-rot is a softer, gradual phenomenon that begins well before exhaustion. A model can be deeply context-rotted at 40% window utilisation.

**Compaction** is a mitigation mechanism (summarising prior context to free space), not a cure. Compaction can itself trigger a sharp regression because the summary loses precision. Lauritzen notes that seeing the compaction indicator in a long agent run is a signal to expect quality degradation in what follows.

**Context-Anxiety** is a related but distinct downstream effect: the human-side tendency to avoid giving agents long tasks because of anticipated context-rot, leading to overly conservative task scoping.

## Strategies for mitigation

Lauritzen frames the primary countermeasures as structural rather than prompting tricks:

- **Task decomposition**: break work into sub-tasks with clear handoff contracts, so each agent operates over a bounded, fresh context rather than an accumulating one.
- **Proxy verification**: for domains where ground-truth verification is hard (e.g. contract quality), compare against a golden corpus. This lets the agent detect its own regressions before the human does.
- **Guardrails**: limiting the agent's action space reduces the surface area over which context-rot can cause harm.

## Opinions

- **Compaction is a reliable signal of context-rot onset in long-running agents.** Once you see it fire, expect the agent to have forgotten context-critical constraints from earlier in the run. — Jacob Lauritzen, Legora ("Agents need more than a chat", AI Engineer 2026), [https://www.youtube.com/watch?v=XNtkiQJ49Ps](https://www.youtube.com/watch?v=XNtkiQJ49Ps)

## Sources

- Jacob Lauritzen, "Agents need more than a chat", AI Engineer 2026 — [https://www.youtube.com/watch?v=XNtkiQJ49Ps](https://www.youtube.com/watch?v=XNtkiQJ49Ps)

## Notes
