# AFK-Tasks

Software tasks that a developer can hand off to an agent and step away from — work where human presence in the loop is not required during execution. Contrasted with planning and alignment work, which is always human-in-the-loop.

## Mechanism

Pocock divides the AI-assisted development workflow into two phases with different collaboration modes:

**Human-in-the-loop (HIL)**: The planning, requirements, and alignment phase. The developer must be present: making product decisions, resolving ambiguities, evaluating whether the direction is correct. No agent can substitute here because the right answer depends on context that lives in the developer's head, not in the codebase.

**AFK**: The implementation phase, once the specification is clear and decomposed. If a task is well-specified, vertically scoped (touching all system layers to produce something runnable), and the agent has the right context, the developer can leave the keyboard and let the agent execute. The agent runs, makes small incremental changes, and self-verifies through tests.

The workflow is described as a day-shift/night-shift model: the human does the day shift (planning, grilling, structuring PRD into issues), then kicks over to the agent for the night shift (AFK execution via the [Ralph-Loop](Ralph-Loop.md)).

## Conditions for AFK suitability

A task becomes AFK-safe when:
1. The scope is defined as a [Vertical-Slice](Vertical-Slices.md) — testable end-to-end, not a horizontal layer stub
2. Dependencies on prior slices are resolved (the task is not blocked by undefined interfaces)
3. The context window is fresh (task fits in the [Smart-Zone](Smart-Zone.md))
4. The agent has self-verification capability — tests it can run to confirm the change is correct

Tasks that are AFK-unsafe: anything requiring product judgment, prioritization decisions, external feedback, or human approval of architectural choices.

## Practical application

In Pocock's workflow, the issue-generation skill explicitly labels each generated issue as either `HIL` or `AFK`. This lets the developer scan the task list and queue up the AFK tasks for autonomous execution without reading every issue.

## Contrast with adjacent ideas

**Autonomous agents** (running without any human oversight) are the extreme of AFK; Pocock's model still involves human oversight at the planning and review phases. AFK refers specifically to the execution window, not the whole project lifecycle.

**[Decision-Log](Decision-Log.md)** is a complementary pattern: during AFK execution, the agent logs ambiguous decisions rather than blocking, enabling async review without interrupting the AFK run.

## Opinions

- **Planning has to be human-in-the-loop. It has to be.** Implementation can be made AFK, but alignment — deciding what to build and whether it's right — cannot be delegated. The value of AFK execution depends on the quality of the HIL planning that preceded it. — Matt Pocock, independent educator ("Full Walkthrough: Workflow for AI Coding", AI Engineer 2026), [https://www.youtube.com/watch?v=-QFHIoCo-Ko](https://www.youtube.com/watch?v=-QFHIoCo-Ko)

## Sources

- Matt Pocock, "Full Walkthrough: Workflow for AI Coding", AI Engineer 2026 — [https://www.youtube.com/watch?v=-QFHIoCo-Ko](https://www.youtube.com/watch?v=-QFHIoCo-Ko)

## Notes
