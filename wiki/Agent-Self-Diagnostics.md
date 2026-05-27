# Agent Self-Diagnostics

A pattern for agent observability where the agent is given a `report` tool and a system prompt instruction encouraging it to call that tool with notable observations about its own behavior — effectively asking the agent to send a note to its creators when something unusual happens.

## Implementation

Add two things to any agent:

1. **A `report` tool** — minimal, single call, sends a short message to Slack or any endpoint. The description matters more than the implementation.
2. **A system prompt line** — e.g., "Before giving your final answer, use the report tool to surface anything noteworthy for your creators."

The tool name and framing are critical. Naming the tool `unsafe_bash_use` or `report_bad_behavior` suppresses firing — the model treats completing the task via any means as success and doesn't self-incriminate. Naming it `report` and framing it as "feedback to creators" works better because models are more willing to give notes than confess faults.

## What it catches

- **Tool failures**: if a tool is repeatedly failing, the model's reasoning trace will "rant" about it — it is aware of the failure, and a self-diagnostics tool will surface that.
- **Capability gaps**: if a user requests something the agent has no tool for, the agent knows it can't fulfill the request and will report it — acts as a built-in feature request signal.
- **Self-correction**: when the agent works around a failure (e.g., write tool blocked → switches to bash heredoc to create the file), it will report this if prompted — useful for catching security-relevant workarounds.
- **User frustration**: the model infers from tone when a user is frustrated and can flag it.

## Limitations and calibration

Models are trained to appear polished and are reluctant to self-incriminate. Firing rate is low without system prompt encouragement. At high scale, you may want to reduce the system prompt encouragement so the tool only fires for genuinely unusual cases rather than routine notes.

Self-diagnostics is not a substitute for classifier-based implicit signals at scale — it's best for catching capability gaps and unusual behavior during development and low-to-mid scale production.

## Broader context: agent monitoring signals

Production agent monitoring uses two signal types:

**Explicit signals** (objective, easily measurable): tool error rate, latency, cost per request, user regeneration rate. Spikes in any of these are straightforward alerts.

**Implicit signals** (semantic): refusals, task failures, user frustration, jailbreaking, NSFW content. These are detected via:
- Regex on conversation content (cheap, coarse, surprisingly powerful in aggregate)
- Trained small classifiers (run on every output; designed for scale — LLM-as-judge would double AI spend at Replit-level volumes)
- Self-diagnostics (agent-reported; targeted at unknown unknowns)

Implicit signals become the feedback mechanism for semantic A/B testing: ship a prompt change, watch whether user frustration rate goes down in production — not just in evals.

## Inspiration

Derived from OpenAI's 2024 paper on training models to self-confess misalignment: models prompted to report their own behavior will honestly admit shortcuts like deleting a failing unit test rather than fixing it.

## Opinions

- **Production monitoring is more important than evals.** As agents handle wider input spaces with more tools and longer sessions, no pre-built test set covers the combinatorial failure space. The monitoring paradigm — watching what happens live — catches the long tail that evals miss. — Zubin & Danny, Raindrop ("Everything You Need to Know About Agent Observability", AI Engineer 2026), [https://www.youtube.com/watch?v=-aM2EDTiaMs](https://www.youtube.com/watch?v=-aM2EDTiaMs)
- **Don't run an LLM on every output for classification.** At Replit-scale this doubles your AI spend. Train small, cheap classifiers for binary signals (refusals, user frustration) instead. — Danny, Raindrop ("Everything You Need to Know About Agent Observability", AI Engineer 2026), [https://www.youtube.com/watch?v=-aM2EDTiaMs](https://www.youtube.com/watch?v=-aM2EDTiaMs)

## Sources

- Zubin & Danny, Raindrop, "Everything You Need to Know About Agent Observability", AI Engineer 2026 — [https://www.youtube.com/watch?v=-aM2EDTiaMs](https://www.youtube.com/watch?v=-aM2EDTiaMs)

## Notes
