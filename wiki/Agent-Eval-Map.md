# Agent-Eval-Map

A structured taxonomy dividing agent evaluation into semantic quality (how well the agent represents reality) and behavioral quality (how well the agent's actions achieve goals in its environment).

## The two dimensions

**Semantic quality** — how well the agent's representations of the world correspond to reality:
- *Single-turn*: coherence, consistency, safety, value alignment, policy adherence
- *Multi-turn/chain*: reasoning trace quality, chain-of-thought consistency
- Grounded via truthfulness (data, [RAG](RAG.md))

**Behavioral quality** — how well the agent's actions achieve its goals:
- *Single-step*: tool selection correctness, tool call format, output quality, error handling
- *Multi-step*: whether actions converge toward the goal, plan quality and consistency
- Grounded via goal achievement and utility

The map highlights a symmetry: representations are a special case of behaviors (representing the world is itself a kind of activity). Single-step evaluations are analogous across both dimensions.

## Practical considerations

Beyond the two main dimensions, evaluations also cover:
- **Cost and latency optimization** — goal is to achieve results in minimum steps and cost
- **Tracing and debugging** — visibility into where the agent went wrong
- **Error management** — handling tool errors vs. reasoning errors (different problems)
- **Offline vs. online testing** — some evals can only be done in production

## Eval Ops

Most teams optimize the "operative LM flow" (the agent) but neglect that their evaluators are themselves LLM-powered and have their own cost, latency, and quality. **Eval Ops** is the practice of treating the evaluator pipeline as a second-class system that also requires optimization and iteration. When the evaluator is expensive and slow, it becomes a separate operational domain that earns its own resourcing.

## Opinions

- **Agent evaluation divides cleanly into semantic quality (representations) and behavioral quality (actions).** Truthfulness grounds the semantic side; goal achievement grounds the behavioral side. These are not independent: accurate representations are the prerequisite for correct behaviors. — Ari Heljakka, Root Signals ("Agent Evaluations: Finally, With The Map", AI Engineer 2025), [https://www.youtube.com/watch?v=y2Drx0SDZLo](https://www.youtube.com/watch?v=y2Drx0SDZLo)

- **Eval Ops is a distinct discipline from LLM Ops.** When your evaluators are themselves slow and expensive LLM calls, optimizing the evaluator pipeline becomes a separate problem from optimizing the agent. Teams that ignore this end up with evaluations that are bottlenecks rather than accelerators. — Ari Heljakka, Root Signals ("Agent Evaluations: Finally, With The Map", AI Engineer 2025), [https://www.youtube.com/watch?v=y2Drx0SDZLo](https://www.youtube.com/watch?v=y2Drx0SDZLo)

## Sources

- Ari Heljakka, Root Signals, "Agent Evaluations: Finally, With The Map", AI Engineer 2025 — [https://www.youtube.com/watch?v=y2Drx0SDZLo](https://www.youtube.com/watch?v=y2Drx0SDZLo)

## Notes

