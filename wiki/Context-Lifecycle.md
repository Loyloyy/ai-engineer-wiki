# Context Lifecycle

An engineering discipline for context — treating prompts, skills, and agent instructions like software: generate, test, distribute, observe, and adapt them with the same rigour applied to code.

Coined by Patrick Debois (Tessl) drawing an explicit analogy to the Software Development Lifecycle (SDLC) and DevOps. The premise: LLMs are just an engine; wrong fuel (context) produces wrong output. The lever available to practitioners is context quality, not model internals.

## The loop

**Generate** — Produce context at multiple levels:
- Ad-hoc prompts (interactive, human-authored)
- Reusable instructions files (`agent.md`, `CLAUDE.md`)
- Library documentation injected at runtime to fix hallucinated API versions
- MCP data pulled from GitHub, Slack, GitLab, etc.
- Specs that agents decompose into step-by-step plans

**Test** — Three levels parallel to code testing:
- *Lint*: structural validation — does the skill have a description? Is it within length limits?
- *Unit (LLM-as-judge)*: give the context, run a prompt, have an LLM judge whether the output follows the convention. Example: "Does the generated endpoint start with `/awesome/`?"
- *Integration (agent + tools)*: give the judge a tool so it can execute code in a sandbox and do a real end-to-end check — not just inspect code, but curl the running endpoint.

Non-determinism: run each test N times; track pass rate. Apply **error budgets** — stricter thresholds for critical tests, looser for others. Never gate on a single run.

**Distribute** — Context as a packageable artifact:
- Skills as the package format: a skill contains context, scripts, documents, and MCP references
- Registries for skill discovery (Tessl marketplace, etc.)
- Dependency management: skills can conflict (context dependency hell)
- Security: scan for credential exposure and prompt injection; track an **AI SBOM** — which model built this context and from what data sources

**Observe** — Feedback channels:
- Agent logs: what context did the agent request or find missing? When a team shares context packages, watching aggregate agent log signals shows what's universally missing
- PR review comments: a rejected PR is feedback on the context that generated it
- Production failures: instrument generated code; when it fails, create a new test case so the context is updated and the failure doesn't recur

**Context filter**: an agent.md/skill.md is loaded at startup without filtering. A context filter (like a web application firewall) intercepts that loading to strip prompt-injection patterns before they reach the agent.

**Adapt** — Use eval feedback to auto-optimize context (e.g., "Here's the failing test output; rewrite the prompt to fix it"). Flywheel applies across scales: individual → team → org, where a context fix by one team becomes a distributed package that benefits all teams.

## Opinions

- **99.9% of skills in public registries are not production quality.** Registries are useful for learning patterns but almost none pass serious evals. — Patrick Debois, Tessl ("Context Is the New Code", AI Engineer 2026), [https://www.youtube.com/watch?v=bSG9wUYaHWU](https://www.youtube.com/watch?v=bSG9wUYaHWU)

## Sources

- Patrick Debois, "Context Is the New Code", AI Engineer 2026 — [https://www.youtube.com/watch?v=bSG9wUYaHWU](https://www.youtube.com/watch?v=bSG9wUYaHWU)

## Notes
