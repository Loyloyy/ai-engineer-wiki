# Context Engine

A pre-computation layer that supplies coding agents with organisational understanding — expert graphs, historical decisions, resolved best practices — rather than letting agents derive that context from scratch on every run.

## The problem it solves

Coding agents start each task at "ground zero": no context about the codebase, team, or organisational history. The typical response — pointing agents at MCP servers, docs, or naive RAG — produces **satisfaction of search**: agents stop searching as soon as they find something plausible (analogous to radiologists stopping after finding the first anomaly on an X-ray) and miss the golden nuggets that live in Slack conversations, incident post-mortems, or deleted code history.

Three myths about solving this problem:
1. *Naive RAG over docs is a context engine.* — Large orgs have conflicting data; RAG without personalization retrieves irrelevant cross-team content. Connecting more MCP servers exacerbates satisfaction of search.
2. *Bigger context windows will solve it.* — Orgs have more than a million tokens of context. Even if infinite context were available, the model would still need to reason about truth, falsehood, and relevance across conflicting sources.
3. *Access equals understanding.* — Wiring up data sources doesn't surface why decisions were made or what was tried and rejected.

## What a context engine does

A context engine provides:
- **Unified system context**: builds relationships between data — PR comments → extracted best practices; expert activities → who-knows-what graph; Slack conversations → historical motivations.
- **Conflict resolution**: biases toward recency (newer data), code (main branch), and expert opinion. Unresolvable conflicts are surfaced to the human rather than silently picked. Naive caching of resolved answers is a trap — context changes constantly; caching regresses toward the mean over time.
- **Access-controlled retrieval**: synthesis is compartmentalized by permission boundary; synthesized cross-boundary data is tagged with group IDs.
- **Targeted retrieval / personal relevance**: identifies which repos the current developer works on most (by PR contribution count) and deep-retrieves those while doing a wider scan of the rest.

## Expert graph / social graph

A key component: a PR-contribution-weighted social graph that identifies domain experts per codebase area. Built from:
1. PR review counts (procedural, fast)
2. Vector clustering of code contributions (who worked where)
3. LLM distillation of Slack conversations, PR comments, and past decisions for each expert

Once built, the expert graph provides a jump-off point for retrieval: loading a domain expert's distilled history into the agent's seed context orients the agent's subsequent search, dramatically reducing context collection time.

## Practical application

Use cases where context engines provide the most value:
- **Planning phase** — biggest bang for buck; correct pre-loaded context eliminates downstream correction loops
- **Code review** — agent understands motivation behind changes, not just syntactic correctness
- **Ticket enrichment** — agent fills in missing context for a new feature ticket
- **Incident triage** — agent instantly correlates current symptoms with past incidents, relevant code areas, and Slack history
- **Engineering support channels** — auto-answers repetitive questions from other teams using accumulated org knowledge

Benchmark (Unblocked internal task — implementing Anthropic's adaptive thinking mode): with context engine: 25 min, 10M tokens; without: 2.5 hours, 21M tokens. Difference is mostly reduced doom-looping, not raw execution speed.

## Sources

- Peter Werry, "Mergeable by Default: Building the Context Engine", AI Engineer 2026 — [https://www.youtube.com/watch?v=5ID22ACI7IM](https://www.youtube.com/watch?v=5ID22ACI7IM)

## Notes
