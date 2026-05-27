# Model-Rot

The progressive erosion of an LLM's usefulness for a specific software domain as its training data ages relative to the pace of change in that domain — particularly acute for fast-moving frameworks, APIs, and developer tools.

## Mechanism

Models are trained on a snapshot of the web. For general knowledge this is usually fine. For software libraries that evolve rapidly, the model's knowledge is a snapshot of how things worked 6–18 months before training completion. Fast-moving projects see model output that:
- Invents API keys and methods that no longer exist or never existed
- Uses deprecated patterns
- Applies documentation conventions from older versions
- Gets framework idioms subtly wrong

The problem is invisible from the model's perspective — it generates confidently incorrect code.

Danilo Campos (PostHog): "It was not our fault... but it was our problem." A year before the PostHog Wizard shipped, agents using Cursor would fabricate PostHog keys and API patterns entirely.

## Mitigation

Large context windows make the mitigation tractable: inject fresh, up-to-date documentation directly into context at runtime rather than relying on training knowledge.

**Practical approach (PostHog Wizard)**:
1. Detect the user's framework and language from their codebase
2. Fetch current documentation from the live docs site (fresh markdown)
3. Let the agent select the relevant documentation subset via tool call
4. Inject the selected markdown into the context before implementation begins

This bypasses the stale training knowledge entirely. The agent's integration knowledge is only as old as the documentation fetch.

## Relationship to adjacent concepts

**[Context-Rot](Context-Rot.md)** is a different problem: quality degradation within a single context window as it fills. Model-Rot is a deployment-time problem — stale training data — not a runtime problem. Both are forms of knowledge decay, but at different points in the pipeline.

## Opinions

- **If you have a fast-moving software project, the model doesn't know what the hell is going on anymore.** Training requires serious capital expense; you're not screwing around training a model on a weekend. The trade-off is the model sits there no longer representing reality. — Danilo Campos, PostHog ("LLM Codegen Fails and How to Stop 'Em", AI Engineer 2026), [https://www.youtube.com/watch?v=juoNbJiZUi0](https://www.youtube.com/watch?v=juoNbJiZUi0)

## Sources

- Danilo Campos, "LLM Codegen Fails and How to Stop 'Em", AI Engineer 2026 — [https://www.youtube.com/watch?v=juoNbJiZUi0](https://www.youtube.com/watch?v=juoNbJiZUi0)

## Notes
