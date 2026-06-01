# Harness-Engineering

Discipline of structuring codebases, tooling, documentation, and processes so that agents can execute the full software engineering job — not just individual tasks — with minimal human intervention per loop.

## Core reframe

"Code is free." The scarce resources in an AI-augmented engineering org are **human time**, **human attention**, and **context window**. Harness engineering is the work of making those scarce resources go further by front-loading structure so agents don't need to ask for clarification mid-task.

Every engineer operating with agents becomes a de facto staff engineer — writing the specs, personas, and structural constraints that shape what dozens of agent runs will produce.

## Structural assets to build

**CLAUDE.md / agent instructions**: the agent's operating manual for the repo. Not just setup instructions — include team norms, architectural decisions, what not to do, persona descriptions. See [Skills](Skills.md) for the portable context-packaging format.

**Persona docs**: per-role agent descriptions used in automated review. A "security reviewer" persona doc defines what the security-focused review agent should check. A "product manager" persona doc defines acceptance criteria framing. These live in the repo and are passed to review agents in CI.

**ADRs (Architecture Decision Records)**: document why the codebase is the way it is. Agents that read ADRs don't propose changes that violate settled architectural decisions.

**Custom lint rules**: encode structural constraints that agents tend to violate. Example: a rule asserting that no source file exceeds 350 lines. The rule runs in CI; agents that produce long files get failed builds rather than human review comments. Lint rules also serve as back-pressure against library-specific anti-patterns — see [Library-Source-Context](Library-Source-Context.md).

**Tests asserting code structure**: unit tests that check the shape of the codebase itself (module dependency graph, file size, naming conventions). Makes agent-violating structural decisions fail fast rather than accumulate as tech debt.

## Process patterns

**Reviewer agents per persona in CI**: each PR is reviewed by multiple agents with different personas (security, product, code quality) before human review. Catches issues that would otherwise require a human reviewer to context-switch to a different mental mode.

**Garbage Collection Fridays**: a dedicated weekly slot where the team reviews agent-generated code for accumulated drift — code that passes tests and review but introduces subtle structural problems. Named because it runs the "garbage collector" on agent output quality.

**1/3/1/3/1/3 time split**: spending equal thirds on planning, implementation, and [CI/validation](Continuous-Compute.md) per feature. The planning and CI thirds are where harness investment compounds — better specs and better automated checks reduce the implementation third over time.

**"Every time I have to type continue is a failure of the harness"**: if an agent run requires human prompting to restart, the harness hasn't provided enough context. The goal is full AFK execution on well-defined tasks. See [AFK-Tasks](AFK-Tasks.md).

## Scale signal

Ryan Lopopolo's team at OpenAI runs **1 billion+ output tokens per day** across a PNPM monorepo of 750 packages. At that scale, harness investments (lint rules, persona docs, structural tests) pay back many times over compared to per-run human corrections.

## Opinions

- **You are the developer experience engineer for your agent.** As you stop being in the weeds doing the work, you start thinking: "How can I make the feedback loop faster?" The power user pattern is not steering the agent manually — it's improving the rails so the agent can loop back faster on its own. — Beyang Liu, Sourcegraph ("The Emerging Skillset of Wielding Coding Agents", AI Engineer 2025), [https://www.youtube.com/watch?v=F_RyElT_gJk](https://www.youtube.com/watch?v=F_RyElT_gJk)

- **Long, detailed prompts consistently outperform short ones.** The model is programmable — give it as much context as you'd give a colleague. A five-word prompt works for toy tasks well-represented in training data; a nuanced production codebase change needs the full context. Agents that underprompt are using the tool like a chatbot. — Beyang Liu, Sourcegraph ("The Emerging Skillset of Wielding Coding Agents", AI Engineer 2025), [https://www.youtube.com/watch?v=F_RyElT_gJk](https://www.youtube.com/watch?v=F_RyElT_gJk)

- **Use sub-agents to preserve context window quality.** The main agent's context degrades at scale (visible degradation around 120K–130K tokens, serious problems by 170K). Sub-agents encapsulate the context of a subtask — implementing a small feature, running a search — without polluting the main agent's context. — Beyang Liu, Sourcegraph ("The Emerging Skillset of Wielding Coding Agents", AI Engineer 2025), [https://www.youtube.com/watch?v=F_RyElT_gJk](https://www.youtube.com/watch?v=F_RyElT_gJk)

- **Give the agent a target to iterate against.** If there's any way to verify output — a unit test, integration test, a screenshot from a simulator — Claude can iterate to a much better result than it can on a single shot. TDD works well with coding agents because the model is doing it, not the human; write tests first, commit, then write code. — Boris Cherny, Anthropic ("Claude Code: The Evolution of Agentic Coding", AI Engineer 2025), [https://www.youtube.com/watch?v=Lue8K2jqfKk](https://www.youtube.com/watch?v=Lue8K2jqfKk)

- **Extended thinking works best when context is already loaded.** Asking the model to think before it has retrieved anything wastes tokens and produces shallow results. Have it use tools to pull context first, then think. — Boris Cherny, Anthropic ("Claude Code: The Evolution of Agentic Coding", AI Engineer 2025), [https://www.youtube.com/watch?v=Lue8K2jqfKk](https://www.youtube.com/watch?v=Lue8K2jqfKk)

- **The more general model always wins** — and the more general product around it too. Stay unopinionated about the UX; the model is on an exponential and will outgrow any opinionated wrapper. The right investment is giving the model low-level access and getting out of its way. — Boris Cherny, Anthropic ("Claude Code: The Evolution of Agentic Coding", AI Engineer 2025), [https://www.youtube.com/watch?v=Lue8K2jqfKk](https://www.youtube.com/watch?v=Lue8K2jqfKk)

- **The scarce resource has flipped from writing code to reviewing it** — agents produce code faster than humans can review it, so the bottleneck is now human attention for review, not implementation. Harness investments that reduce review burden (automated persona reviewers, structural tests) have the highest ROI. — Ryan Lopopolo, OpenAI (How to Build Software When Humans Steer, Agents Execute, AI Engineer 2026), [link](https://www.youtube.com/watch?v=am_oeAoUhew)

- **Persona documents in CI are a better investment than detailed per-PR review comments** — comments are ephemeral; persona docs persist and shape every future agent run on every PR. — Ryan Lopopolo, OpenAI (How to Build Software When Humans Steer, Agents Execute, AI Engineer 2026), [link](https://www.youtube.com/watch?v=am_oeAoUhew)

- **"Every time I have to type continue is a failure of the harness"** — a need for human mid-run prompting indicates the task spec, context, or tooling is incomplete; the fix is always in the harness, not in the agent. — Ryan Lopopolo, OpenAI (How to Build Software When Humans Steer, Agents Execute, AI Engineer 2026), [link](https://www.youtube.com/watch?v=am_oeAoUhew)

- **Surface only high-reliability capabilities to users, not everything the agent can theoretically do.** Capability discovery means itemizing what the agent does well and making those paths obvious — not advertising the full action space. Proactive suggestions based on parsed current context (e.g., what's in the scene) are more useful than open-ended prompting. — Victor Diaz, Microsoft Research / AutoGen ("UX Design Principles for Semi-Autonomous Multi-Agent Systems", AI Engineer 2025), [https://www.youtube.com/watch?v=fmZWvE7yDZo](https://www.youtube.com/watch?v=fmZWvE7yDZo)

- **Stream all activity logs and expose debugging metadata (tokens, latency per step) as a first-class UX concern.** From the LLM's perspective, the agent's actions are a black box to the user. Observability and provenance — streamed in real time — are what transform an autonomous system from a magic box into a trustworthy collaborator. — Victor Diaz, Microsoft Research / AutoGen ("UX Design Principles for Semi-Autonomous Multi-Agent Systems", AI Engineer 2025), [https://www.youtube.com/watch?v=fmZWvE7yDZo](https://www.youtube.com/watch?v=fmZWvE7yDZo)

- **Design every agent to be interruptible: checkpoint, rollback, pause/resume.** An agent that can't be paused mid-run is an agent that can't be trusted with consequential actions. Interruptibility is the prerequisite for user trust, not an afterthought. — Victor Diaz, Microsoft Research / AutoGen ("UX Design Principles for Semi-Autonomous Multi-Agent Systems", AI Engineer 2025), [https://www.youtube.com/watch?v=fmZWvE7yDZo](https://www.youtube.com/watch?v=fmZWvE7yDZo)

- **Agents treat all actions as equal unless you add a cost-estimation layer.** From the LLM's perspective, "add a sphere" and "delete the OS" are equivalent tool calls. Cost-aware delegation means estimating the risk/cost of each action and routing high-cost actions to a human approval step. — Victor Diaz, Microsoft Research / AutoGen ("UX Design Principles for Semi-Autonomous Multi-Agent Systems", AI Engineer 2025), [https://www.youtube.com/watch?v=fmZWvE7yDZo](https://www.youtube.com/watch?v=fmZWvE7yDZo)

- **Build in this order: goal → baseline (no AI) → tools → eval test bed → agent.** Starting with the agent is the most common mistake. A working non-AI baseline and a verified tool set are prerequisites. Spend 50% of your time on tools — the agent is only as good as what it can call. — Victor Diaz, Microsoft Research / AutoGen ("UX Design Principles for Semi-Autonomous Multi-Agent Systems", AI Engineer 2025), [https://www.youtube.com/watch?v=fmZWvE7yDZo](https://www.youtube.com/watch?v=fmZWvE7yDZo)

## Sources

- Ryan Lopopolo, "How to Build Software When Humans Steer, Agents Execute", AI Engineer 2026 — [YouTube](https://www.youtube.com/watch?v=am_oeAoUhew)
- Boris Cherny, "Claude Code: The Evolution of Agentic Coding", AI Engineer 2025 — [https://www.youtube.com/watch?v=Lue8K2jqfKk](https://www.youtube.com/watch?v=Lue8K2jqfKk)
- Beyang Liu, "The Emerging Skillset of Wielding Coding Agents", AI Engineer 2025 — [https://www.youtube.com/watch?v=F_RyElT_gJk](https://www.youtube.com/watch?v=F_RyElT_gJk)
- Victor Diaz, Microsoft Research, "UX Design Principles for Semi-Autonomous Multi-Agent Systems", AI Engineer 2025 — [https://www.youtube.com/watch?v=fmZWvE7yDZo](https://www.youtube.com/watch?v=fmZWvE7yDZo)

## Notes

