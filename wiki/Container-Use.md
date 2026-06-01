# Container-Use

A pattern for giving coding agents fully isolated, containerized development environments — so each agent (or parallel experiment) has its own filesystem, tools, and execution context rather than sharing the developer's workspace.

Introduced by Solomon Hykes (Dagger) as a missing primitive between "computer use" (OS-level agent access) and pure sandbox execution.

## The problem

Running a single coding agent in your local workspace is manageable with human oversight. Running multiple agents in parallel falls apart fast: they share the environment, overwrite each other's files, run conflicting processes, and make it impossible to watch them closely. The two options in use today are unsatisfactory:

1. **YOLO mode**: run N agents in a shared env, accept chaos
2. **All-in-one hosted**: delegate everything to a cloud product, wait for a PR, lose access to your machine/model/infra choices

What engineers actually need: background work, rails (constraints), the ability to seamlessly step in, and optionality (freedom to choose models, compute, and tools).

## Container-use as the solution

The environment needs four properties:
- **Isolated**: each agent has its own filesystem and execution context; no cross-agent interference
- **Customizable**: inject secrets, set base images, define build/test commands so the agent doesn't waste tokens on environmental trial and error
- **Multiplayer**: human can step in at any point to inspect state, redirect, or take over — without disrupting other agents
- **Open**: no lock-in to a specific model or compute provider; any agent that supports MCP can attach

**Key distinction from sandboxing**: sandboxing secures the *execution of agent output*. Container-use means the agent *develops inside containers entirely* — editing files, building, running tests, all within ephemeral containerized steps. The agent's entire development loop happens inside the container.

## How it works

Each tool call (file edit, build command, test run) spawns an ephemeral container and produces a snapshot. Snapshots are stored as git objects alongside the repo — not polluting the working tree, but accessible and versioned. The result is a git-log-style history of every state the agent traversed.

The human can:
- List all active environments with their random names
- Open a terminal into any environment to inspect what the agent sees
- View a snapshot diff of the agent's history
- Merge a chosen environment state into their working tree

Environments can run on remote compute (a basement server, a cloud cluster, CI) and tunnel their services transparently to the developer's machine.

## Parallel experiments

When you want multiple versions of a solution simultaneously, you fork from a stable state and run multiple agents concurrently. Each produces its own diverging branch. You diff, compare, and discard or merge as you see fit — the discarded branch cleans up automatically because it was always isolated.

## Integration

The open-source implementation (Dagger's `container-use`) integrates via MCP. Claude Code, Goose, and other MCP-compatible agents can call it as a standard MCP tool, getting container-backed environments without changes to the agent itself. Internally it uses Dagger as a toolbox for container primitives.

Open source: github.com/dagger/container-use

## Contrast with adjacent ideas

**[Durable-Agent-Execution](Durable-Agent-Execution.md)** focuses on preserving agent *state* across failures via an append-only context log and VM snapshots. Container-use focuses on *environment isolation* — preventing agents from interfering with each other and with the developer's workspace.

**[AFK-Tasks](AFK-Tasks.md)** describes the goal (agents running unattended). Container-use provides the environment infrastructure that makes multi-agent AFK execution safe.

## Opinions

- **Every coding agent user has just been welcomed to platform engineering.** Your job is now enabling robots to ship software productively. The tools we use for humans (containers, git) are underutilized — we haven't built the native integration for agents yet. — Solomon Hykes, Dagger ("Containing Agent Chaos", AI Engineer 2025), [https://www.youtube.com/watch?v=bUBF5V6oDKw](https://www.youtube.com/watch?v=bUBF5V6oDKw)
- **This is not sandboxing.** Sandboxing secures agent *outputs*; container-use means the agent *develops inside containers*. The distinction matters: you need the full development loop — editing, building, testing — in the isolated environment, not just the execution of what the agent already built. — Solomon Hykes, Dagger ("Containing Agent Chaos", AI Engineer 2025), [https://www.youtube.com/watch?v=bUBF5V6oDKw](https://www.youtube.com/watch?v=bUBF5V6oDKw)

## Sources

- Solomon Hykes, "Containing Agent Chaos", AI Engineer 2025 — [https://www.youtube.com/watch?v=bUBF5V6oDKw](https://www.youtube.com/watch?v=bUBF5V6oDKw)

## Notes
