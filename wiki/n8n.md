# n8n

A visual, low-code workflow automation platform with a built-in AI agent node and a human-in-the-loop interceptor for vetting tool calls before execution.

## Overview

Founded 2019. Nodes represent individual API operations; connections between nodes define execution flow. JavaScript escape hatches are available on any node for custom logic beyond the low-code interface. The platform is self-hostable and open-core.

The AI agent node accepts a model, a memory provider, and a set of tools. Each tool is a standard n8n node. Node name becomes the tool name; node description becomes the tool description — both are injected directly into the LLM's context. Per-field access control is configurable: the agent can only set fields that are explicitly marked as agent-controllable.

## Human-in-the-loop interceptor

n8n's distinguishing agentic feature is a review step that physically intercepts tool calls before execution. When the agent attempts to invoke a tool that has the interceptor attached:

1. Execution pauses.
2. The human reviewer sees the full proposed action — what the agent wants to call and with what arguments.
3. The reviewer can: **approve** (execution proceeds), **deny** (agent receives rejection), or **redirect** (provide corrective instruction and let the agent retry).

The agent cannot bypass the interceptor; it is at the node level, not a prompt instruction. Multiple tools can share a single review step, so one reviewer handles all sensitive operations in a workflow.

The tool description should explicitly tell the model "there is a human in the loop who reviews this action" — this prevents the agent from treating the pause as an error and encourages it to articulate its intent clearly in the call.

## Sub-agent architecture

n8n recommends using sub-workflow agents (specialized agents per domain) orchestrated from a main agent, rather than loading all tools into one agent. Benefits:
- Avoids context bloat from unrelated tools
- Enables per-agent model selection (e.g., a cheaper model for simple sub-tasks)
- Isolates failures to a single sub-workflow

Each sub-workflow is itself a callable node, making the orchestrator's tool list a set of domain-scoped capabilities rather than raw API endpoints.

## Practical application

- Place the human-in-the-loop interceptor on any tool where mistakes are costly or irreversible.
- Write explicit "a human reviews this action" language into tool descriptions so the model doesn't interpret pauses as failure.
- Use node description fields for full prompting: per-field guidance, constraints, and examples fit here.
- Build domain-scoped sub-workflow agents and call them from an orchestrator to limit per-agent tool surface area.

## Sources

- Liam McGarrigle, "Human-in-the-Loop Automation with n8n", AI Engineer 2026 — [https://www.youtube.com/watch?v=tDArkCqjA-c](https://www.youtube.com/watch?v=tDArkCqjA-c)

## Notes
