# Agent Computer

The pattern of giving an agent a persistent file system or sandbox as a computing substrate — enabling scratchpad planning, persistent memory, reusable scripts, and self-extending behavior.

## The behavioral shift

Without a file system, an agent's state lives entirely in context. Everything it reasons about must fit in the window; once context is full, prior work is lost. With a persistent file system, the agent gains an external store it can write to and read from at will — planning artifacts, research outputs, and reusable tools all persist between turns.

The observed improvement from adding a file system to agents at Vercel: agents that previously used 5–10 tools and returned somewhat hallucinated answers dramatically improved task completion rates across customer support, data analysis, and engineering workflows.

## Scratchpad planning

When given a file system with instructions to write a plan file at the start of each session, agents exhibit more disciplined long-task execution:
1. Agent writes an initial plan to `plan.md` with the objective at the top.
2. Agent is instructed to reference `plan.md` before every step and check off completed items.
3. The objective survives arbitrary context length — even if context compacts, the agent re-reads the plan and recovers its goal.

This prevents the drift toward forgetting the original instruction that occurs in long contexts. The plan file also becomes an artifact that shows humans exactly what the agent did and why.

## Memory as files

Rather than vector stores or external memory APIs, a simple pattern:
- `memories.md`: persistent facts about the user and preferences, injected into the system prompt at session start. The agent writes to it when it learns important facts; the harness reads it and injects on every invocation.
- `conversations.jsonl` or similar: retrievable history the agent can search with grep/find.

The file system becomes a structured workspace: different files serve different memory roles (core/contextual), and the agent can query it using tools it already knows (bash, grep, glob). Agents are highly proficient at writing bash to navigate file systems.

## Agent self-extension via scripts

Agents can build reusable tools for themselves:
1. When the agent performs a repeatable task (e.g., fetch weather), it writes a reusable script to the file system.
2. Future sessions: the agent checks for relevant existing scripts before writing new code.
3. Over time, the agent accumulates a personal toolkit of scripts it references for common operations.

This is a lightweight form of agent-extended capability — the agent learns from its own prior work without any fine-tuning or retraining.

## Persistent named sandboxes

For production deployments, the practical mechanism for persistence between turns:
- Each agent session is tied to a named sandbox (keyed to user ID or session ID).
- On user inactivity: snapshot the file system, shut down the instance.
- On next request: restore from snapshot into a fresh instance — transparent to the agent.
- The agent experiences it as the same machine, even across multi-hour or multi-day gaps.

This complements [Durable-Agent-Execution](Durable-Agent-Execution.md) (context log + VM snapshot) — the file system state is part of the execution snapshot.

## Three tool types (AI SDK taxonomy)

For reference when designing agent tool surfaces:
- **Custom tools**: developer provides description + input schema + execute function. Full control; model calls based on description match.
- **Provider-defined tools**: provider post-trained the model to use effectively (e.g., Anthropic's bash tool, computer use tool). Developer writes the execute handler only.
- **Provider-executed tools**: run on the LLM provider's infrastructure; developer opts in (e.g., OpenAI web search). No execute function needed; provider returns the result.

Provider-executed tools are the fastest to integrate but introduce provider lock-in and no visibility into execution.

## Opinions

- **Adding a file system to an agent is the single biggest behavioral improvement.** An agent with a scratchpad plan file stays on task for 100+ minute runs across 300+ tool calls using only 32% of a 1M token window. The file system offloads memory management from context to disk. — Nico Albanese, Vercel ("Give Your Agent a Computer", AI Engineer 2026), [https://www.youtube.com/watch?v=wflNENRSUb4](https://www.youtube.com/watch?v=wflNENRSUb4)
- **Memory is a file, not a database.** The ideal memory system is `memories.md` injected into the system prompt, backed by files the agent can read and write with bash. The file system is the playground; bash is the interface. — Nico Albanese, Vercel ("Give Your Agent a Computer", AI Engineer 2026), [https://www.youtube.com/watch?v=wflNENRSUb4](https://www.youtube.com/watch?v=wflNENRSUb4)
- **LLM summarization (auto-compaction) is lossy and dangerous.** The case of an agent deleting an entire email inbox because auto-compaction dropped the "stop" instruction illustrates the risk. Prefer sub-agents that return a short summary over compacting the main thread. — Nico Albanese, Vercel ("Give Your Agent a Computer", AI Engineer 2026), [https://www.youtube.com/watch?v=wflNENRSUb4](https://www.youtube.com/watch?v=wflNENRSUb4)

## Sources

- Nico Albanese, Vercel, "Give Your Agent a Computer", AI Engineer 2026 — [https://www.youtube.com/watch?v=wflNENRSUb4](https://www.youtube.com/watch?v=wflNENRSUb4)

## Notes
