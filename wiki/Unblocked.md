# Unblocked

A [Context-Engine](Context-Engine.md) product for engineering teams, exposing organizational knowledge (codebase history, expert graphs, best practices, Slack/Teams context) to coding agents via MCP server, CLI, and API.

## Overview

Integrates with SCM (GitHub, GitLab), planning tools, messaging (Slack, Microsoft Teams), docs, and CI/CD. Processes data continuously (real-time webhooks where available; cron jobs otherwise) and builds an incrementally updated knowledge graph.

The core output surface is an MCP server that coding agents (Claude Code, Cursor, Codex) can query to retrieve pre-distilled context relevant to the current task and developer.

Primary agent customers (observed by Unblocked across its user base): Claude Code most-used, followed by Cursor; Claude Desktop shows unexpectedly high usage; VS Code and Codex account for a smaller share.

## Expert graph

Identifies domain experts per codebase area using a multi-layer approach:
- Procedural layer: PR contribution counts and review frequency
- ML layer: vector clustering of code contributions — who worked on what, with what proximity
- LLM distillation layer: summarizes each expert's past decisions, Slack conversations, and PR comment patterns

Expertise-weighted feedback loop: when a known expert flags a context response as incorrect, that signal carries more weight in updating confidence scores than a correction from a new contributor.

## Conflict resolution

Best-practice memories are distilled from repeated PR review patterns; conflicts are resolved by ranking recency, code (main branch), and expert opinion — in that order. Unresolvable conflicts are surfaced to the human through the UI rather than silently resolved.

## Sources

- Peter Werry, "Mergeable by Default: Building the Context Engine", AI Engineer 2026 — [https://www.youtube.com/watch?v=5ID22ACI7IM](https://www.youtube.com/watch?v=5ID22ACI7IM)

## Notes
