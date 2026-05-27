# OpenAI-Codex

OpenAI's software engineering agent — not just a code-completion tool but a full autonomous agent that runs commands, executes tests, explores codebases, and integrates with external services across multiple surfaces.

## Architecture

Built on a **unified agent harness** layered on top of GPT models. The harness manages tool execution, environment setup, and safety guardrails independent of the underlying model. Model family as of April 2026: GPT-5.2 Codex → GPT-5.3 Codex → GPT-5.3 Codex Spark (Cerebras-backed, fast) → GPT-5.4; plus GPT-5.4-mini and GPT-5.4-nano for lightweight sub-agent tasks. The harness and models are evolved in tandem — each model upgrade improves the full agent capability, not just raw inference.

Surfaces: Codex app (Mac, Windows), IDE extensions, CLI, Slack integration, GitHub integration.

## Core features

**Plugins**: Bundles that package skills (reusable instruction sets for specific processes), app connections (Notion, Linear, Figma, Google Drive, Slack), and MCP servers into a single installable unit. Eliminates per-component setup. First-party plugins ship for web dev, game dev, and more; user-defined plugins also supported.

**Automations**: Scheduled background tasks (cron-style) that run without interactive session. Examples: daily Slack digest, email triage, calendar briefings. Configured via the app UI or by asking Codex to create the automation from a description.

**Sub-agents**: Decompose a task into parallel independent sub-tasks and delegate each to a spawned Codex agent. Each sub-agent is configurable: model choice (e.g., GPT-5.3 Spark for read-only exploration, full GPT-5.4 for write tasks), sandbox mode (read-only vs. write), custom skills and MCP access. Three default personas ship: general-purpose fallback, worker (execution), explorer (read-only exploration). Sub-agents report back to the orchestrating agent for collation. Used at OpenAI for parallel code review, feature brainstorming, and vulnerability analysis.

**Code review**: Available on GitHub (auto-reviews all PRs), Codex CLI (`/review`), Codex app, and as a Claude Code plugin. Reviews the full repo context, not just the diff — catches second-order effects on untouched modules. Outputs p0/p1/p2 severity callouts. 100% of OpenAI pull requests (all employees) pass through Codex code review as a first pass.

**Native git worktree support**: Work on multiple features in parallel across separate worktrees within a single project in the Codex app.

## Experimental features

**Guardian approvals**: For each privileged operation (file deletion, server start, network exposure), Codex spawns a sub-agent that evaluates whether human approval is needed. Most operations pass automatically; only genuinely risky ones interrupt the user. Addresses "YOLO mode fatigue" — users approving every tool call in an autonomous session. Enable with `/experimental`.

**Hooks**: Programmatic callbacks at three lifecycle events: session start, per-tool-use, session stop. Use case examples: pull latest from GitHub on session start; document each tool use per researcher preference; run a "keep going" script on stop to sustain long-running tasks without human re-prompting.

## Other capabilities

**Codex Security**: Commit-by-commit vulnerability scanning and patching on GitHub repos.

**Best-of-N execution**: Run the same task N times in parallel in cloud mode; select best output. Available from the app, IDE extension, and web interface.

## Sources

- Vaibhav Srivastav & Katia Gil Guzman, "OpenAI Codex Masterclass", AI Engineer 2026 — [https://www.youtube.com/watch?v=MhHEGMFCEB0](https://www.youtube.com/watch?v=MhHEGMFCEB0)

## Notes
