# Validation Contract

A document written during the planning phase, before any implementation begins, that defines what "done" means for a multi-agent task independently of how the implementation will achieve it.

## The problem it solves

Tests written after implementation don't catch bugs — they confirm decisions. An agent that builds a feature and then writes tests will write tests shaped by the code it just produced, not by what the code was supposed to do. The tests pass, coverage looks good, but the system has drifted from the original intent. Over many sequential agent tasks, this drift compounds.

A validation contract prevents this by separating the definition of correctness from the act of implementation. The contract is authored by the orchestrator (or human, during planning) before workers touch the codebase.

## Structure

For a complex project a contract can contain hundreds of assertions. Each feature in the implementation plan is assigned one or more assertions it must satisfy. The sum of all features must cover every assertion in the contract — no assertion can go unvalidated.

The contract answers: *does this behavior work end-to-end?* — not *does the code look right?*

## Two-stage validation

Systems running against validation contracts typically run two types of validators at milestone boundaries:

**Scrutiny validator** (traditional): runs the test suite, type checking, lint, and spawns dedicated code review agents for each completed feature. Fast to execute.

**User testing validator** (behavioral): spawns the application, interacts with it via computer use or similar — fills out forms, clicks buttons, checks that functional flows work holistically. Slower; most of the wall-clock time in long-running missions is spent here waiting for real-world execution rather than generating tokens. Critically, these validators have never seen the code before — they are adversarial by design and have no investment in making the implementation "work."

## Relationship to serial execution

Validation contracts work best in systems that execute features serially (one worker at a time) rather than in parallel. Parallelism causes agents to conflict on shared code, duplicate work, and make inconsistent architectural decisions — the coordination overhead erodes the speed gain. Serial execution with targeted internal parallelization (read-only operations like code search and code review) dramatically lowers error rates, and correctness compounds over multi-day runs.

## Multi-agent communication patterns (reference taxonomy)

Five building blocks appear repeatedly in multi-agent systems:

| Pattern | Description | Notes |
|---|---|---|
| **Delegation** | Parent agent spawns child agent, awaits result | Simplest; sub-agents in coding tools |
| **Creator-Verifier** | One agent builds, a separate agent with fresh context checks | Core of validation contract approach |
| **Direct Communication** | Agents communicate without a central coordinator | State fragments without a coordinator; hard to get right |
| **Negotiation** | Agents communicate over a shared resource | Most valuable when win-win trading is possible |
| **Broadcast** | One agent sends context or status to many | Critical for coherence over long-running tasks |

Long-running systems (multi-day) typically compose delegation, creator-verifier, broadcast, and negotiation together.

## Architecture longevity

Systems relying on hard-coded state machines become obsolete when new models are released. Architectures that encode orchestration logic primarily in prompts and skills (not deterministic code) improve automatically with each model upgrade. The deterministic shell should be thin — restricted to bookkeeping tasks like blocking progress when handoff issues are unresolved, running validators, and managing structured handoffs.

Structured handoffs between workers document: what was completed, what was left undone, commands run and their exit codes, issues discovered, and whether procedures were followed. This is how long-running multi-agent systems self-heal at milestone boundaries rather than drifting silently.

## Opinions

- **Tests written after implementation don't catch bugs — they confirm decisions.** If validation relies on agent-generated tests, the system will eventually drift. The validation contract exists precisely to define correctness before any code is written. — Luke Alvoeiro, Factory ("The Multi-Agent Architecture That Actually Ships", AI Engineer 2026), [https://www.youtube.com/watch?v=ow1we5PzK-o](https://www.youtube.com/watch?v=ow1we5PzK-o)
- **Parallelism sounds faster but isn't — serial-first is better for multi-day tasks.** Agents in parallel conflict on shared code, duplicate work, and make inconsistent architectural decisions. Correctness compounds over time; coordination overhead erodes speed gains. — Luke Alvoeiro, Factory ("The Multi-Agent Architecture That Actually Ships", AI Engineer 2026), [https://www.youtube.com/watch?v=ow1we5PzK-o](https://www.youtube.com/watch?v=ow1we5PzK-o)
- **No single model is best at all three roles.** Planning benefits from slow careful reasoning; implementation from fast code fluency; validation from precise instruction following. Locking into one model provider means being constrained by its weakest capability. Using a different provider for validation avoids training-data bias influencing the assessment. — Luke Alvoeiro, Factory ("The Multi-Agent Architecture That Actually Ships", AI Engineer 2026), [https://www.youtube.com/watch?v=ow1we5PzK-o](https://www.youtube.com/watch?v=ow1we5PzK-o)

## Sources

- Luke Alvoeiro, Factory, "The Multi-Agent Architecture That Actually Ships", AI Engineer 2026 — [https://www.youtube.com/watch?v=ow1we5PzK-o](https://www.youtube.com/watch?v=ow1we5PzK-o)

## Notes
