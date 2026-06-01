# Pi

Minimal open-source coding agent built around four core tools (read, write, edit, bash) with a TypeScript extension API for hot-reloadable user-defined capabilities; ranked 6th on Terminal Bench.

## Design philosophy

Pi's core claim is that agent quality comes from simplicity and explicitness, not from a larger tool surface. The minimal prompt exposes the four tools and nothing else; everything else is user-defined via extensions. This means the user owns the context — no injected system reminders, no opaque capabilities, no hidden tool calls.

**Extensions**: TypeScript modules that add new tools or behaviors to Pi at runtime. Extensions are hot-reloaded, so changes take effect without restarting the agent. Pi can use its own extension API to add tools to itself mid-session (self-modification).

**Human callout extension**: a Pi extension pattern that intercepts dangerous actions — database migrations, permission changes, destructive file operations — and requires explicit human confirmation before proceeding. See [Agent-Legible-Codebase](Agent-Legible-Codebase.md) for the broader codebase design pattern this integrates with.

## Critique of heavy agents

Mario Zechner's design choices in Pi are a direct response to what he sees as failure modes in tools like Claude Code:

- **Token madness**: heavy agents burn tokens on reasoning about things that don't need LLM decision-making.
- **Opaque context**: system prompts and injected reminders are invisible to the user; you can't see what the agent has been told.
- **Zero observability**: no visibility into what the agent is "thinking" between tool calls.
- **Zero model choice**: the agent is locked to a specific model; the user can't swap backends.

The counter-principle: **"slow the fuck down."** Agents should flag uncertainty and ask for confirmation rather than compounding errors. Humans feel pain from mistakes, which creates a corrective feedback signal; agents don't, so errors accumulate silently unless the harness forces explicit checkpoints.

## Benchmarks

- Terminal Bench: 6th overall (as of April 2026)

## Opinions

- **Pain is a bottleneck that is actually a feature** — humans feel the consequences of mistakes, which forces them to slow down on risky actions; agents have no equivalent regulatory mechanism and will compound errors indefinitely without explicit harness-level stops. — Mario Zechner (Building Pi in a World of Slop, AI Engineer 2026), [link](https://www.youtube.com/watch?v=RjfbvDXpFls)

- **Agents that own the context are agents you can't trust** — when the harness injects system reminders and hidden instructions the user can't inspect, there's no way to reason about what the agent is optimising for. Full context transparency is a prerequisite for production use. — Mario Zechner (Building Pi in a World of Slop, AI Engineer 2026), [link](https://www.youtube.com/watch?v=RjfbvDXpFls)

- **The number of built-in tools is not a quality signal** — four well-defined tools with a clean extension API outperforms twenty opaque built-in capabilities; surface area is a liability when you can't audit it. — Mario Zechner (Building Pi in a World of Slop, AI Engineer 2026), [link](https://www.youtube.com/watch?v=RjfbvDXpFls)

## Sources

- Mario Zechner, "Building Pi in a World of Slop", AI Engineer 2026 — [YouTube](https://www.youtube.com/watch?v=RjfbvDXpFls)

## Notes

