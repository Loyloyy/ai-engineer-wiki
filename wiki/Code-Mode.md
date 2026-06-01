# Code-Mode

Agent execution pattern where the LLM generates executable code (typically JavaScript) as its "tool call," which is then run directly against a live environment — replacing the sequential JSON tool-call/response cycle with a single code block that expresses the full action.

## The problem it solves

Standard tool-calling scales poorly with large API surfaces. Cloudflare's internal API has 2,600 endpoints. A naive approach requires the agent to choose tools from a context window containing all endpoint definitions: **1.2 million tokens** of tool documentation. Code Mode collapses this to two tools — `search` (finds relevant endpoints) and `execute` (runs generated code) — reducing the effective context to roughly **1,000 tokens**: a 99.9% reduction.

## How it works

Instead of generating a JSON object like `{"tool": "create_worker", "params": {...}}`, the model generates:

```javascript
const worker = await api.workers.create({ name: "my-worker", script: "..." });
console.log(worker.id);
```

This code runs inside a capability-based sandbox and the result is returned to the model. The model "inhabits the state machine" rather than generating a separate application — it is the runtime logic, not a description of it.

## Capability-based sandbox

Security is enforced by granting capabilities explicitly rather than restricting them reactively:

- Agent starts with **zero capabilities** by default
- Capabilities (network access, file system, specific APIs) are granted explicitly per task
- Execution runs in **V8 isolates** — separate JavaScript VMs that share no state
- Outgoing fetches are **blocked by default**; specific domains are allowlisted

This inverts the traditional security model: instead of "allow everything, block the known bad," it's "block everything, grant the known good." Capability grants are auditable; restrictions are not.

## Generative UI

Code Mode extends naturally to UI generation: the model generates React/HTML/CSS code that renders directly in the response. Rather than a fixed tool that returns structured JSON which a template renders, the model produces the rendering logic itself. Sunil Pai frames this as the "generative UI" direction — the UI layer becomes as malleable as the data layer.

## Opinions

- **Sequential tool-call/response cycles are the wrong abstraction for large API surfaces** — the latency, context cost, and complexity of N round-trips to cover N-step operations is fundamentally worse than generating a code block that covers all N steps in one shot; Code Mode is the right default for APIs with more than a few dozen endpoints. — Sunil Pai, Cloudflare (Code Mode: Let the Code Do the Talking, AI Engineer 2026), [link](https://www.youtube.com/watch?v=8txf05vVVl4)

- **Capability-based sandboxing is the correct security model for agent execution** — default-deny with explicit grants produces an auditable, minimal permission surface; default-allow with restrictions produces an ever-growing blocklist that attackers can enumerate around. — Sunil Pai, Cloudflare (Code Mode: Let the Code Do the Talking, AI Engineer 2026), [link](https://www.youtube.com/watch?v=8txf05vVVl4)

- **The only MCP you actually need is eval.** LLMs are trained on vastly more code than on function schemas — they are far better at writing code than calling tools correctly. Every coding agent ultimately resorts to bash when tool calling fails; why not start there? Code generation is dynamic (the tool is created on demand, tailored to the exact query); static MCP tools are not. — Manuel Odendahl ("MCPs Are Boring: Or Why We Are Losing the Sparkle of LLMs", AI Engineer 2025), [https://www.youtube.com/watch?v=J3oJqan2Gv8](https://www.youtube.com/watch?v=J3oJqan2Gv8)

## Sources

- Sunil Pai, "Code Mode: Let the Code Do the Talking", AI Engineer 2026 — [YouTube](https://www.youtube.com/watch?v=8txf05vVVl4)
- Manuel Odendahl, "MCPs Are Boring: Or Why We Are Losing the Sparkle of LLMs", AI Engineer 2025 — [https://www.youtube.com/watch?v=J3oJqan2Gv8](https://www.youtube.com/watch?v=J3oJqan2Gv8)

## Notes

