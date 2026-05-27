# AgentCraft

An agent orchestration interface designed for managing multiple coding agents in parallel, drawing on interaction patterns from real-time strategy (RTS) games to raise the ceiling of human-agent collaboration.

## Overview

Created by Ido Salomon. Available at agentcraft.dev. Salomon is also the creator of MCI and co-maintainer of MC Apps.

The core thesis: the bottleneck in multi-agent development is not spawning agents — it is the human's capacity to manage, direct, and review them. AgentCraft applies RTS game mechanics (unit visibility, heat maps, campaign mode, review bundles) to make that management sustainable.

## Key features

**Filesystem-as-map**: The developer's file system is projected as a navigable map. Each directory is a building, each file is a room. Agents appear on the map as units, showing which file they are currently modifying in real time. The full change log per file is visible.

**Collision detection**: Because file activity is tracked per agent, AgentCraft can generate a heat map of concurrent file access and proactively warn when multiple agents are touching the same files.

**Campaign mode**: A high-level goal ("implement channels") is given to a campaign orchestrator, which decomposes it into sub-tasks and assigns agents to execute them inside an isolated container. The human is removed from task-level babysitting; the orchestrator handles it. The human's role shifts entirely to plan review and output review.

**Review bundles**: After a campaign, the developer reviews a bundle of PRs — each with a change list, task description, and visual evidence (screenshots, video). This makes review parallelizable and asynchronous.

**Multiplayer collaboration**: AgentCraft supports shared workspaces where multiple developers and their agents can see each other's activity. Agents can see the shared chat, observe what other agents are doing, and avoid working in the same areas.

## Contrast with adjacent ideas

**[ACE](ACE.md)** (GitHub Next) also provides multiplayer agent collaboration, but targets team alignment through a shared chat/session model. AgentCraft emphasizes individual developer throughput and visual orchestration at scale.

**[AgentCraft](AgentCraft.md)** is inspired by RTS games; the RTS analogy is explicit — Salomon argues that managing dozens of agents in a game is a familiar skill most developers already have, just not applied to productivity contexts.

## Sources

- Ido Salomon, "Putting the Orc in Orchestration", AI Engineer 2026 — [https://www.youtube.com/watch?v=kR64LOqBBCU](https://www.youtube.com/watch?v=kR64LOqBBCU)

## Notes
