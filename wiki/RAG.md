# RAG

Retrieval-Augmented Generation: supplying an LLM with documents fetched from an external store at inference time so its output is grounded in that data rather than parametric memory alone.

The canonical mechanism: embed the query, run a similarity search over a vector store, inject the top-k chunks into context, then generate. This hub collects how the concept recurs across the wiki — mostly as a **foil**. The repeated practitioner finding is that *naive* RAG (flat chunking + vector similarity) underperforms for agent work:

- It causes **satisfaction of search** — agents stop at the first plausible hit and miss the real signal (see [Context-Engine](Context-Engine.md)).
- Bolting RAG onto an unreliable knowledge base yields 10–30% accuracy; the knowledge base, not the retrieval layer, is the bottleneck (see [Demand-Driven-Context](Demand-Driven-Context.md)).
- For documentation-heavy workflows, loading skills as on-demand tool calls beats flat-chunk retrieval (see [Skills](Skills.md)).
- It is ill-suited to stable framing context that should *always* be present (see [Nested-Context-Injection](Nested-Context-Injection.md)).

Where RAG *does* earn its place: as grounding / "factual anchors" that pull generation toward reality (see [Coherence-Trap](Coherence-Trap.md)), and in richer retrieval architectures that go beyond semantic distance (see [GraphRAG](GraphRAG.md)). Access control must be enforced at the retrieval layer, never inside the model (see [Agent-Identity](Agent-Identity.md)).

## Related pages in this wiki
- [GraphRAG](GraphRAG.md) — knowledge-graph + vector retrieval; multi-hop traversal beyond similarity
- [Context-Engine](Context-Engine.md) — pre-computed expert context as an alternative to naive retrieval
- [Demand-Driven-Context](Demand-Driven-Context.md) — fixing the knowledge base before the retrieval layer
- [Coherence-Trap](Coherence-Trap.md) — RAG as grounding against hallucination
- [Nested-Context-Injection](Nested-Context-Injection.md) — when stable framing beats per-query retrieval
- [Search-Tool-Design](Search-Tool-Design.md) — designing agent retrieval tools
- [Smart-Truncation](Smart-Truncation.md) — retrievable memory store for offloaded context
- [Skills](Skills.md) — skills-as-tool-calls vs. RAG for docs
- [Agent-Identity](Agent-Identity.md) — retrieval-layer authorization (FGA)

## Sources
Synthesis / navigation hub. Per-claim attribution lives on the linked topic pages above (RAG appears as a supporting concept across them rather than as the subject of a single talk).

## Notes
