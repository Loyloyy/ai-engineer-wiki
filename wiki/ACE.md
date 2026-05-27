# ACE

Agent Collaboration Environment — a research prototype from GitHub Next that combines multiplayer team chat, coding agents, cloud-hosted micro-VMs, and shared development sessions under one interface, designed to address [Coordination-Debt](Coordination-Debt.md) in AI-assisted software teams.

## Overview

Built by Maggie Appleton's team at GitHub Next (the "Department of F--- Around and Find Out"). In technical preview as of AI Engineer 2026. Not a production product. The team planned to test it with a few thousand users and iterate.

## Architecture

Each ACE **session** is:
- A multiplayer chat channel (Slack-like) shared by teammates and coding agents
- Backed by a **micro-VM** — a sandboxed cloud computer on its own git branch
- Isolated per-session: changes in one session do not affect another

Because all participants (human and agent) share the same cloud computer, there is no "works on my machine" problem. Any teammate can run terminal commands, see the same live preview in the browser, and view real-time shared outputs.

The agent reads the full conversation history as context. Teammates can discuss plans naturally and then prompt the agent with "@ACE do it" — the agent has already seen the full context of the conversation.

When a session closes, the micro-VM persists. The developer can close their laptop and teammates (or the agent) continue working. A mobile interface is in development.

## Key capabilities

- **Multiplayer prompting**: any participant can prompt the coding agent, not just the session creator
- **Session summary block**: real-time summary of the latest changes in a session, enabling fast context recovery when switching between many parallel sessions
- **Shared terminal**: all participants can run commands and see outputs in the same environment
- **Live preview**: browser-rendered output visible to all participants simultaneously
- **PR creation inline**: branches and PRs are created from within the session; the PR description links back to the ACE session for context
- **VS Code integration**: the session's micro-VM can be opened directly in VS Code for participants who need to edit code directly

## Contrast with adjacent ideas

**[AgentCraft](AgentCraft.md)** also provides multi-agent visibility and collaboration but focuses on individual developer throughput at scale (RTS-style management). ACE focuses on team-level alignment — bringing in non-developers (PMs, designers, domain experts) alongside the coding work.

**GitHub/Slack/Jira** provide coordination for human-paced development. ACE is explicitly designed for the pace of agentic development, where alignment must happen continuously alongside implementation, not asynchronously after it.

## Sources

- Maggie Appleton, "Collaborative AI Engineering", AI Engineer 2026 — [https://www.youtube.com/watch?v=ClWD8OEYgp8](https://www.youtube.com/watch?v=ClWD8OEYgp8)

## Notes
