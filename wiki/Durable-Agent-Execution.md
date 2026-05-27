# Durable Agent Execution

An architectural framework for making production agents resilient across turns, code versions, and failures — combining an append-only context log with VM-level execution snapshots.

## The problem with stateless compute

Backend infrastructure for 30 years has operated on shared-nothing architecture: compute is stateless, all meaningful state lives in the database. This works for request/response workflows. Agents break this model because they are sessions, not transactions — they can run for hours, accumulate significant execution state (cloned repos, installed packages, running dev servers, subprocess state), and must survive the user going to lunch.

The replay model used by durable execution engines (Temporal, Inngest, Trigger.dev) wraps every side effect in a cached step. On resume, the function re-executes and skips already-completed steps. This works for multi-step workflows — but agent context logs grow unboundedly as the agent interacts, and replay journals hit fundamental size limits. An agent isn't a transaction; it's a session that lasts as long as the user wants.

## Two kinds of durable state

Agents have two distinct types of state requiring different durability strategies:

**Context log** — system messages, user messages, tool calls, tool results, assistant responses. This is append-only and maps naturally to databases, object storage, or distributed file systems. Persisting the context log gives:
- Durability across code versions (upgrade the harness, reuse the same context)
- Recovery from machine crashes
- Append-only logs scale well

**Execution state** — everything in the compute layer: cloned repositories, installed packages, in-memory data, running dev servers, subprocess state. This cannot be reconstructed from a log — it must be preserved as-is.

## Snapshot and restore

For execution state durability, the solution is VM-level snapshot and restore:

1. When the agent is waiting (user goes to lunch, LLM retry delay), snapshot the VM to disk and shut it down.
2. When the user message arrives, restore the VM from snapshot — it picks up exactly where it left off.
3. No expensive idle compute during wait periods.

Implementation path: CRIU (process-level checkpoint via user-space injection, 2011) was the earlier approach — works but limited to process-level state, incompatible with open files not captured at snapshot time, and slow with container registries. Firecracker microVMs (whole-machine snapshot) solves these limitations.

Firecracker optimization: naive VM snapshot of a 512MB machine produces a 512MB snapshot. Seekable compression with lazy page decompression (decompress only the pages needed at restore time) reduces this to ~14MB compressed. Snapshot: ~1s. Restore: ~200ms.

## Combined architecture

A durable agent = context log + execution snapshot:

| Failure mode | Recovery mechanism |
|---|---|
| LLM unavailable (retry in 15 minutes) | Snapshot → restore when retry is ready |
| Machine crash | Context log → replay context, rebuild execution state |
| Code version upgrade | Context log → load new harness, reuse same context |
| User goes offline for hours | Snapshot → restore on next user message |

## Practical application

1. Persist every message in and out of the LLM to an append-only store (database or object storage) as it happens — not as a post-hoc dump.
2. Design the agent harness so it can resume from a context log without requiring the execution state (fallback path when snapshot is unavailable).
3. Use Firecracker microVMs (or a wrapper like FCRun) for execution state durability — snapshot on wait, restore on resume.
4. Separate the two durability concerns: context is cheap to persist, execution state is expensive but needed only for long-running stateful agents.

## Opinions

- **Agents are forcing a shift from stateless to stateful compute.** The 30-year shared-nothing paradigm works for transactions but fails for sessions. Agents are sessions that last as long as the user wants them to. — Eric Allam, Trigger.dev ("Replay vs. Snapshot: Two Roads to Durable Agents", AI Engineer 2026), [https://www.youtube.com/watch?v=svCnShDvgQg](https://www.youtube.com/watch?v=svCnShDvgQg)
- **Replay is the wrong model for agent durability.** Replay journals were designed for multi-step workflows with defined start and end points — not unbounded sessions. As agents do meaningful work for hours, replay hits fundamental size limits. — Eric Allam, Trigger.dev ("Replay vs. Snapshot: Two Roads to Durable Agents", AI Engineer 2026), [https://www.youtube.com/watch?v=svCnShDvgQg](https://www.youtube.com/watch?v=svCnShDvgQg)
- **The duration of meaningful agentic work is doubling every 4–7 months.** Currently a few hours; soon multiple days. Infrastructure must plan for sessions that outlast human working days. — Eric Allam, Trigger.dev ("Replay vs. Snapshot: Two Roads to Durable Agents", AI Engineer 2026), [https://www.youtube.com/watch?v=svCnShDvgQg](https://www.youtube.com/watch?v=svCnShDvgQg)

## Sources

- Eric Allam, Trigger.dev, "Replay vs. Snapshot: Two Roads to Durable Agents", AI Engineer 2026 — [https://www.youtube.com/watch?v=svCnShDvgQg](https://www.youtube.com/watch?v=svCnShDvgQg)

## Notes
