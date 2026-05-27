# Smart Truncation

A context management technique for long-running agents that preserves conversation head and tail in the active window while offloading the middle to a retrievable memory store — keeping context small without losing access to prior turns.

## Why naive approaches fail

**Naive truncation** (discard everything past N tokens): the agent loses continuity. Follow-up questions get answered as if they're new conversations — asking "tell me more about option B" after a previous response yields no recognition of option B. Over-truncation breaks reasoning.

**Summarization** (compress context via LLM before injecting): too inconsistent. Leaving summarization to the LLM provides no control over what's preserved as important. What the agent considers worth summarizing doesn't reliably match what downstream reasoning needs.

## Smart truncation + memory

The technique:
1. Keep the **head** (first N tokens) — system prompt, task framing, initial context. Never reset the system prompt.
2. Keep the **tail** (last M tokens) — the most recent turns and tool results. Always keep the latest result for any repeated tool call (deduplicate).
3. Remove the **middle** — store it externally with IDs and positional metadata (how many messages back, which turn).
4. Give the agent a **retrieval tool** — it can look up any middle-segment entry by ID when it determines prior context is needed. The tool returns a preview of available context so the agent can select.

This gives the agent agency over what it retrieves rather than relying on pre-computed summaries. The model decides which middle-segment entries are relevant to the current reasoning step.

## Long session evals

Context degradation failures appear late: early in a conversation, truncation seems fine; failures emerge at turn 20+ when important context has been pushed out of the window. By then it's usually a user report, not a caught regression.

Mitigation: construct evals that simulate long sessions. Load 10 turns of representative conversation history, then test the 11th — checking whether references to earlier turns resolve correctly. This makes context degradation bugs testable and catchable before users report them.

## Sub-agent delegation for heavy data

When a task involves large intermediate data (hundreds of search result spans, complex multi-query reasoning, large datasets), running it in the main conversation context accumulates tokens that crowd out user-facing chat history.

Pattern: delegate data-heavy operations to a sub-agent with its own isolated context. The main conversation stays small (light chat history + system prompt only). The sub-agent handles the heavy computation, returns a result summary, and the main agent incorporates that into its response. Both agents can access the shared memory store independently.

This is iterative — as the variety of heavy operations grows, the number of specialized sub-agents grows correspondingly.

## Context vs. memory

A useful framing: **context** is what the model currently sees; **memory** is what it can retrieve on demand. These are separate concerns. Trying to make context serve both roles (large enough to hold everything, precise enough to enable reasoning) leads to both failing. Separate them:
- Context: managed tightly, always current, fits in Smart Zone
- Memory: append-only, external, accessed via tool

## Opinions

- **Agents don't fail because of prompts — they fail because of context.** Early AI engineering focused entirely on prompt quality. The real failure mode at scale is context management: wrong data in the window, insufficient access to prior reasoning, or context that has grown beyond what the model can reliably use. — Sally-Ann Delucia, Arize ("How We Solved Context Management in Agents", AI Engineer 2026), [https://www.youtube.com/watch?v=esY99nYXxR4](https://www.youtube.com/watch?v=esY99nYXxR4)
- **Context management is a product and UX problem, not just an engineering one.** If the agent doesn't have the right data, it gives bad answers. The choice of what the model sees is ultimately about what makes the product work for users — not what fits in the token budget. — Sally-Ann Delucia, Arize ("How We Solved Context Management in Agents", AI Engineer 2026), [https://www.youtube.com/watch?v=esY99nYXxR4](https://www.youtube.com/watch?v=esY99nYXxR4)
- **Summarization sounds obvious but is unreliable.** Leaving context compression to an LLM provides no control over what's preserved. Explicit head-tail truncation with a retrievable memory store gave more consistent results than LLM-driven summarization. — Sally-Ann Delucia, Arize ("How We Solved Context Management in Agents", AI Engineer 2026), [https://www.youtube.com/watch?v=esY99nYXxR4](https://www.youtube.com/watch?v=esY99nYXxR4)

## Sources

- Sally-Ann Delucia, Arize, "How We Solved Context Management in Agents", AI Engineer 2026 — [https://www.youtube.com/watch?v=esY99nYXxR4](https://www.youtube.com/watch?v=esY99nYXxR4)

## Notes
