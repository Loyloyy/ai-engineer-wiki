# Ralph-Loop

An autonomous agent execution pattern in which a coding agent loops over a task list — making one small change per iteration, verifying it, then moving to the next — until all tasks are complete. The human is absent during execution; the loop runs AFK.

## Origin

Named after Ralph Wiggum from *The Simpsons*, the character who cheerfully executes instructions without overthinking them — he just tries the same thing over and over until it works. The earliest articulation: just re-submit the same prompt after the agent finishes, so the agent reviews its own output and catches what it missed. First notable for fixing incomplete code; later evolved into broader continuous-execution loops.

In Pocock's framing, "Ralph" is the pure incremental version: specify the destination, make small changes, repeat until done. Pocock uses the name for the broader loop-based execution pattern in his workflow.

The core insight: a multi-phase plan (Phase 1, Phase 2, Phase 3) is just a loop over phases. Replace the enumerated phases with Phase N — a loop that continues until the plan is complete.

## Mechanism

The loop structure:
1. A PRD or high-level goal is established in the planning phase (human-in-the-loop)
2. The PRD is decomposed into [Vertical-Slices](Vertical-Slices.md) as ordered issue files
3. The agent starts a fresh session per task (or a fresh context per loop iteration) to stay within the [Smart-Zone](Smart-Zone.md)
4. Each iteration: pick the next unblocked issue → implement → run tests → mark done → repeat
5. The human reviews at the end, or monitors asynchronously

The loop is designed to be [AFK](AFK-Tasks.md): once kicked off, it does not require human input until all issues are exhausted or it gets genuinely stuck.

## Key design decisions

**Fresh sessions per task**: Starting a new context for each issue keeps the agent in the smart zone and prevents accumulated context rot from degrading quality on later tasks. The system prompt and the specific issue file are the only persistent inputs.

**Self-verification**: Each task includes enough scope to be testable. The agent runs tests or checks visible output before marking a task done. Without self-verification, the loop cannot be trusted to run AFK.

**Dependency ordering**: Issues are generated with blocking dependencies listed. The loop respects this ordering — it does not start a task blocked by an incomplete prerequisite.

## Practical implementation

**`/loop` command (Claude Code)**: built-in slash command that schedules the loop task as a recurring cron job. Example: `/loop every 1 minute: implement the next most important ticket from doc/tickets`. The loop continues until stopped. Runs within the same Claude Code session; fresh-context loops require an external `while true` shell script invoking `claude -p "..."` instead.

**"Pick the next most important ticket"**: rather than pre-specifying ticket dependencies (which recreates waterfall), instruct the loop to read all open tickets and determine the next most important one itself. The agent can evaluate dependencies on the fly; what it cannot do is coordinate parallel agents without contention. Starting with a single sequential loop is more reliable than premature parallelism.

**Sub-agent validation**: running validation in the same context as implementation produces confirmation bias — the agent that wrote the code is reluctant to fault it. Using a sub-agent for the review step (fresh context, sees only the diff and the criteria) catches significantly more issues. The `simplify` built-in skill runs three sub-agents against recent changes.

**Reversibility heuristic**: before delegating an action to the loop, ask: "Is this reversible without embarrassment to me?" Drafting slides, generating content, making code changes → reversible, auto-approve. Sending emails, posting to LinkedIn, closing tickets → irreversible, require human sign-off. The loop surfaces irreversible decisions for review rather than acting autonomously.

**Context management**: fresh context per loop iteration prevents context rot from accumulating across tasks. With the `/loop` command (same session), prior task context carries over — potentially useful for coherence but risks quality degradation on long runs. With an external shell loop, each invocation starts cold; the agent reconstructs state from the file system.

## Relationship to Grill-Me

The loop is the execution half of the workflow; [Grill-Me](Grill-Me.md) is the planning half. Grill-Me builds the shared understanding and PRD; the PRD feeds into issue generation; the issues feed into the Ralph-Loop. The loop produces code; the human reviews it.

## Contrast with adjacent ideas

**Pure Ralph Wiggum** (Pocock's original framing): just specify the end state and let the agent increment toward it without structured issue decomposition. Works for small tasks; breaks down for anything requiring ordering or dependency management.

**[Decision-Log](Decision-Log.md)**: when the loop hits a genuinely ambiguous decision during AFK execution, the agent logs it rather than blocking. The human reviews the log after the run rather than being interrupted during it.

## Opinions

- **A multi-phase plan is just a loop in disguise.** Once you see it as Phase N, the natural thing to do is automate it. The human shouldn't be clicking "next phase" — the agent should be doing that. — Matt Pocock, independent educator ("Full Walkthrough: Workflow for AI Coding", AI Engineer 2026), [https://www.youtube.com/watch?v=-QFHIoCo-Ko](https://www.youtube.com/watch?v=-QFHIoCo-Ko)
- **Everything is a loop.** Not just code — emails, newsletters, morning briefings, project management. Once you have a loop running for code, the logical extension is to point loops at all other repeating work. The question then shifts from "what can AI do?" to "which bits of work do I actually want to keep doing myself?" — Chris Parsons, Cherrypick ("Ralph Loops: Build Dumb AI Loops That Ship", AI Engineer 2026), [https://www.youtube.com/watch?v=2TLXsxkz0zI](https://www.youtube.com/watch?v=2TLXsxkz0zI)
- **Don't optimize for tokens; optimize for your own time.** Burning a few extra tokens on self-checks that might find nothing is cheap relative to the human time saved. — Chris Parsons, Cherrypick ("Ralph Loops: Build Dumb AI Loops That Ship", AI Engineer 2026), [https://www.youtube.com/watch?v=2TLXsxkz0zI](https://www.youtube.com/watch?v=2TLXsxkz0zI)

## Sources

- Matt Pocock, "Full Walkthrough: Workflow for AI Coding", AI Engineer 2026 — [https://www.youtube.com/watch?v=-QFHIoCo-Ko](https://www.youtube.com/watch?v=-QFHIoCo-Ko)
- Chris Parsons, Cherrypick, "Ralph Loops: Build Dumb AI Loops That Ship", AI Engineer 2026 — [https://www.youtube.com/watch?v=2TLXsxkz0zI](https://www.youtube.com/watch?v=2TLXsxkz0zI)

## Notes
