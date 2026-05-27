# Search Tool Design

A framework for curating an agent's search tools that balances reliability for common queries with coverage for unexpected ones — the "low floor, high ceiling" approach.

## The design tension

Specialized search tools (e.g., "get customer by ID", "semantic search over documents") have low parameter complexity — the agent rarely makes mistakes, calls are efficient, and latency is low. But they only cover anticipated query patterns. When a user asks something unexpected, the agent hits a wall.

General-purpose tools (shell/bash tool, raw query execution) have a high ceiling — they can handle any query the agent can express as a command or query string. But they impose higher parameter complexity, cause more agent errors, and often require multiple tool iterations to arrive at the right answer.

## Low floor / high ceiling strategy

Curate both types in combination:

- **Low floor (specialized)**: pre-built tools with simple parameters for the most frequent query patterns. Fast, error-free, efficient.
- **High ceiling (general-purpose)**: shell/bash tool or query-execution tool that lets the agent handle anything it can express. Slower and more iterative but available as a fallback.

Do not rely on one silver bullet tool. Good search is hard — the right combination depends on your agents' actual query behavior.

## Starting approach when query behavior is unknown

1. Start with a general-purpose tool (shell/bash tool or query executor).
2. Log the agent's tool calls and observe what it's actually trying to retrieve.
3. If the agent takes 4–5 tool calls per question for a recurring query pattern, that's a signal the tool is too complex — scope out a specialized tool for that pattern.
4. Use the agent's own analysis of its usage logs to recommend specializations (Claude Code identified query pattern clusters and suggested specific database tools after three days of usage logging).

## Shell tool limitations

The shell tool (bash, exec, terminal) is versatile: ls, grep, curl, CLI invocations, custom scripts. But it falls short for semantic search — agents compensate by enumerating synonyms in grep patterns, which is slow, brittle, and misses conceptually related terms with no lexical overlap. Solutions:

- Semantic grep CLIs (e.g., Gina Grep with multi-vector embeddings) can be added as shell-accessible commands, extending the shell tool with semantic capability.
- For database queries, a shell tool combined with a purpose-built database search tool achieves higher accuracy than either alone: the database tool finds candidates; the shell tool verifies/filters results.

## Tool description best practices for search

1. Start with core purpose (one sentence).
2. Add trigger conditions — when should/should not this tool be called.
3. Add relationships — e.g., "call the ESQL skill before calling this tool" or "confirm with the user before calling this tool."
4. Reinforce the description in the agent system prompt if the agent still calls the wrong tool.

If the tool has complex parameter requirements (e.g., writing a query in an unfamiliar query language), attach an agent [Skill](Skills.md) with documentation and load it before the tool is called.

## Error handling

Return tool errors to the agent as tool responses rather than crashing. For search tools that generate query strings, syntax errors are common — returning the error message lets the agent self-correct and rewrite the query. This is especially important for general-purpose query execution tools.

## Opinions

- **Context engineering is ~80% agentic search.** The "curation arrow" from context sources to context window is powered by search tools. Most attention goes to what's in the window; not enough attention goes to the tools that decide what gets there. — Leonie Monigatti, Elastic ("Agentic Search for Context Engineering", AI Engineer 2026), [https://www.youtube.com/watch?v=ynJyIKwjonM](https://www.youtube.com/watch?v=ynJyIKwjonM)
- **There is no silver bullet search tool.** Good search is hard. The right stack for an agent is a curated combination of specialized (low floor) and general-purpose (high ceiling) tools matched to the agent's actual query behavior. — Leonie Monigatti, Elastic ("Agentic Search for Context Engineering", AI Engineer 2026), [https://www.youtube.com/watch?v=ynJyIKwjonM](https://www.youtube.com/watch?v=ynJyIKwjonM)

## Sources

- Leonie Monigatti, Elastic, "Agentic Search for Context Engineering", AI Engineer 2026 — [https://www.youtube.com/watch?v=ynJyIKwjonM](https://www.youtube.com/watch?v=ynJyIKwjonM)

## Notes
