# Intentional Compaction

A context management pattern for coding agents: proactively compress an agent's context window into a structured handoff document before starting a new session, so the next session begins with targeted knowledge rather than running codebase discovery from scratch.

## The problem it solves

LLMs are stateless — performance is determined by what tokens enter the context window. In complex, long-running coding tasks on brownfield codebases, the context window fills with codebase exploration, test runs, failed approaches, and error output. This creates two failure modes:

1. **Context bloat**: tokens used for discovery and dead ends crowd out the actual work; quality degrades as the window fills
2. **Session loss**: when you start a new context (because the agent went off-track or the session hit its limit), the next agent must re-discover everything the previous one already learned

Intentional compaction addresses both by creating an explicit handoff.

## How it works

**When to compact**: either reactively (when the agent has gone significantly off-track) or proactively (before starting a new session, regardless of whether the current one worked).

**What to compact**: the exact files and line numbers that matter to the problem being solved, the approach being taken, and any relevant context about why certain paths were explored or abandoned. Not a full conversation replay — a curated map.

**How**: instruct the current agent to compress its context into a markdown file containing:
- The specific goal and current state
- The exact files (with line numbers) relevant to the task
- Decisions made and the reasoning behind them
- What hasn't worked and why

The new agent session starts from this document and can begin working immediately instead of spending its first N tokens on discovery.

## Relationship to other context patterns

[Smart-Truncation](Smart-Truncation.md) preserves the head and tail of a conversation window — it manages within a single session. Intentional compaction manages *across* sessions, creating continuity between them. Both address the same underlying problem (LLMs degrade as context fills) but at different scopes.

## Practical application

1. **Recognize when to compact**: the agent has started apologizing, is looping, or has drifted significantly from the goal
2. **Prompt for compaction**: "Summarize our session into a handoff document. Include: goal, current state, exact files and line numbers we've touched (specify them precisely), decisions made, and what approaches failed"
3. **Review the compaction**: scan it to ensure it accurately captures the state; edit if needed
4. **Start the new session**: open a fresh context, paste the compaction document, continue

## Opinions

- **Context is the only lever for brownfield AI coding.** LLMs are stateless; putting better tokens in is the only way to get better tokens out. In complex legacy codebases, intentional compaction is the difference between 2–3x throughput and constant rework. — Dex Horthy, HumanLayer ("No Vibes Allowed: Solving Hard Problems in Complex Codebases", AI Engineer Code Summit 2025), [https://www.youtube.com/watch?v=rmvDxxNubIg](https://www.youtube.com/watch?v=rmvDxxNubIg)
- **The naive approach — steering and re-steering until context runs out — is the worst use of a coding agent.** Deliberately compacting and restarting outperforms running a single session to exhaustion. — Dex Horthy, HumanLayer ("No Vibes Allowed: Solving Hard Problems in Complex Codebases", AI Engineer Code Summit 2025), [https://www.youtube.com/watch?v=rmvDxxNubIg](https://www.youtube.com/watch?v=rmvDxxNubIg)

## Sources

- Dex Horthy, HumanLayer, "No Vibes Allowed: Solving Hard Problems in Complex Codebases", AI Engineer Code Summit 2025 — [https://www.youtube.com/watch?v=rmvDxxNubIg](https://www.youtube.com/watch?v=rmvDxxNubIg)

## Notes
