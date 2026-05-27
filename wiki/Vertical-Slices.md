# Vertical-Slices

A task decomposition strategy in which each unit of work cuts through all system layers — database, service, API, UI — to produce a minimal but end-to-end working feature. Contrasted with horizontal decomposition, where tasks are grouped by layer (schema first, then services, then UI).

## Origin

From "Traceable Bullets" in *The Pragmatic Programmer* (Hunt & Thomas). A traceable bullet is a minimal implementation that fires through the full system stack end-to-end, confirming the wiring is correct before the full feature is built.

Matt Pocock adapts this specifically as an AI task structuring discipline.

## Why vertical slices matter for AI-assisted development

Horizontal slices produce code that cannot be run or tested until all layers are complete. An AI implementing "schema first, services second, UI third" receives no feedback until the end, cannot verify its own work, and drifts. A vertical slice produces something runnable after every task — the agent can see the output, run tests, and confirm correctness before moving on.

Pocock's specific criteria for a valid vertical slice:
- Touches at least schema, service/logic, and a visible frontend element
- Is independently testable — can be verified end-to-end without waiting for future slices
- Is not blocked by any slice not yet completed
- Is the smallest thing that produces observable behaviour

The first slice is especially important: it establishes the wiring. Every subsequent slice follows established patterns rather than making architectural choices from scratch.

## Practical application

In Pocock's workflow, the `PRD-to-issues` skill explicitly instructs the model to break requirements into vertical slices. The skill quizzes the model on each proposed issue to confirm it's truly vertical. Pocock demonstrates overriding a model that proposes a horizontal slice ("create the gamification service first") and redirecting to a true vertical: "schema change + service + visible dashboard element."

Issues are generated as local markdown files with:
- Type label (`AFK` or `HIL`)
- Blocking dependencies listed
- Scope description verifying it's a vertical slice

## Contrast with adjacent ideas

**Horizontal decomposition** groups tasks by technical layer. Produces clean separation but requires all layers to be complete before anything is testable. Fine for human developers who can hold more context; problematic for agents who need near-instant feedback loops.

**[Ralph-Loop](Ralph-Loop.md)** is the execution pattern that runs these vertical slice issues; vertical slices are the input the loop consumes.

**[AFK-Tasks](AFK-Tasks.md)** become possible because vertical slices produce self-verifiable units. A horizontally-scoped task (incomplete without sibling tasks) cannot be safely run AFK.

## Opinions

- **The AI is kind of coding blind without vertical slices.** It reaches the later phases without any feedback on whether what it built earlier is correct. Vertical slices give it the near-instant feedback it needs to self-correct. — Matt Pocock, independent educator ("Full Walkthrough: Workflow for AI Coding", AI Engineer 2026), [https://www.youtube.com/watch?v=-QFHIoCo-Ko](https://www.youtube.com/watch?v=-QFHIoCo-Ko)

## Sources

- Matt Pocock, "Full Walkthrough: Workflow for AI Coding", AI Engineer 2026 — [https://www.youtube.com/watch?v=-QFHIoCo-Ko](https://www.youtube.com/watch?v=-QFHIoCo-Ko)

## Notes
