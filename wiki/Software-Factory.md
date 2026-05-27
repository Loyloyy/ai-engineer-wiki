# Software-Factory

A fully autonomous agent pipeline for continuous software production — where human involvement is limited to providing intent and reviewing outputs, while agents handle decomposition, implementation, testing, and deployment 24/7.

## Origin

From Dan Shapiro's blog post (January/February 2026) defining six levels of software development autonomy. Eric Zakariasson (Cursor) extended the model with practical observations from building toward this state at Cursor.

Shapiro's six levels:
1. Spicy autocomplete (tab completion)
2. Pair programmer (back-and-forth with agent)
3. Developer (AI generates majority of code, human reviews)
4. Manager (human delegates most work, reviews outputs)
5. Software factory (autonomous pipeline; human provides intent)
6. Dark factory (fully autonomous; no human insight required)

Zakariasson positions himself at level 4 for most projects.

## Required components

Zakariasson frames factory prerequisites as three categories:

### Primitives and patterns
- **Modular, co-located codebase**: if an agent can `ls` a folder and find all relevant files, it works within that module without needing to grep the whole codebase. Same principle helps human onboarding.
- **Usage patterns**: established methods for auth, startup scripts, test writing. Agents given a reference example can reproduce patterns consistently rather than inventing from scratch.

### Guardrails
- **Rules** (e.g., Cursor Rules): emerge dynamically when agents go off-rails; SOPs encoding what agents can and cannot do. Zakariasson's observation: rules should arise from actual failures, not be installed preemptively from templates.
- **Hooks**: shell commands on specific events (e.g., agent about to touch encryption/auth code). Prevents costly errors in sensitive areas.
- **Tests**: self-verification mechanism; without runnable tests, the agent cannot know if it broke something.

### Enablers
- **Skills and MCPs**: give agents additional capabilities (e.g., a skill to add a feature flag means an autonomously-launched agent can flag its own changes for gradual rollout)
- **Feature flags**: let agents merge PRs behind a flag; humans review and enable when ready, or revert cleanly
- **Runnable dev environment**: agent can start the project without human involvement; prerequisite for autonomous VM execution

## Human role in a factory

The shift is from implementation to management: "Am I making the right things? Are we spending energy in the right place?" The factory produces more code per unit of human time; the bottleneck moves to judgment and taste.

Zakariasson describes the pre-factory role as "verifiable systems": before launching an AFK factory run, the human ensures the agent can verify its own work — through unit tests, integration tests, or UI tests (clicking through the DOM to confirm buttons work, loading spinners render, etc.). Backend systems are easier to verify; UI systems require more setup to make AFK-safe.

## Contrast with adjacent ideas

**[Software-Factory](Software-Factory.md)** is the end-state; [AFK-Tasks](AFK-Tasks.md) are the building block. Individual AFK tasks compose into a factory when orchestrated and equipped with the right guardrails and enablers.

**[Deep-Modules](Deep-Modules.md)** is a prerequisite: a shallow-module codebase makes factory-scale agents ineffective because they must traverse too many files to understand any one operation.

**[AgentCraft](AgentCraft.md)** provides visibility and management tooling suited to operating at factory scale; a software factory needs some form of orchestration layer once more than a few agents run simultaneously.

## Opinions

- **Rules should emerge from failures, not be installed preventively.** A directory of "best practice" Cursor Rules for your stack misses the point — rules are SOPs that codify what went wrong in your specific codebase, written after an agent actually goes off-rails. — Eric Zakariasson, Cursor ("Building Your Own Software Factory", AI Engineer 2026), [https://www.youtube.com/watch?v=rnDm57Py54A](https://www.youtube.com/watch?v=rnDm57Py54A)
- **Verifiable systems are the hardest prerequisite.** The factory only works when agents can confirm their own output. Most teams underinvest in this. For UI especially, you need agents that can actually click around in the DOM — unit tests alone are not enough. — Eric Zakariasson, Cursor ("Building Your Own Software Factory", AI Engineer 2026), [https://www.youtube.com/watch?v=rnDm57Py54A](https://www.youtube.com/watch?v=rnDm57Py54A)

## Sources

- Eric Zakariasson, "Building Your Own Software Factory", AI Engineer 2026 — [https://www.youtube.com/watch?v=rnDm57Py54A](https://www.youtube.com/watch?v=rnDm57Py54A)

## Notes
