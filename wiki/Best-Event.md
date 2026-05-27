# Best-Event

A parallelization pattern in which the same task is dispatched to multiple models or agents simultaneously in isolated work trees, with results compared and optionally combined by a parent agent — enabling competitive selection over model outputs rather than serial trial and error.

## Mechanism

1. User submits a single task
2. Parent agent spawns one sub-agent per model, each operating in its own isolated git work tree
3. Sub-agents work independently without context of each other's output
4. Parent agent collects all outputs and produces a comparative summary: which models did the same thing, which diverged, what each approach's tradeoffs are
5. User selects the preferred implementation, or asks the parent to stitch together pieces from different sub-agent outputs

For frontend work, visual previews of each implementation can be shown side-by-side before selection.

## Why it matters

Traditional iterative trial-and-error with one model at a time is expensive in wall-clock time and lacks comparison signal. Best-Event transforms a sequential guessing problem into a parallel selection problem: you get N candidate implementations in roughly the time it takes to run one, and you have concrete differences to reason about rather than abstract model uncertainty.

The parent agent's comparative summary provides more insight than unaided comparison would — it can identify which sub-agent made non-obvious architectural choices, flag where implementations diverge, and suggest hybrid approaches the user might not have thought to request.

## Implementations

**Cursor** (`/best-event` command): Spawns sub-agents per model into separate git work trees. The entire implementation fits ~40 lines of markdown (a skill file). Judges output by running a parent model as a synthetic reviewer. David Gomes: this replaced a ~4,000-line hardcoded implementation with comparable capability plus improved judging and the ability to combine outputs across sub-agents.

**OpenAI Codex** (cloud mode): Run the same task N times in parallel in the cloud, select best output. Available from the app, IDE extension, and web interface.

## Limitations

- **Work tree drift**: In skill-based implementations, models are instructed to stay within their assigned work tree but can deviate — particularly smaller models and over long sessions. Haiku deviates significantly more than larger models in Cursor's evals.
- **Git dependency**: git work trees require a git repo. Non-git codebases have no native isolation primitive. Cursor is exploring non-git parallelization alternatives.
- **Disk usage**: Each work tree creates a full checkout; users with many parallel runs accumulate significant disk space.

## Relationship to adjacent patterns

**[Vertical-Slices](Vertical-Slices.md)**: Vertical slices decompose a task into independent cross-layer sub-tasks for sequential or parallel execution. Best-Event runs the *same* task in parallel across models for selection — these patterns are orthogonal and composable.

**[AFK-Tasks](AFK-Tasks.md)**: Best-Event is most valuable for AFK tasks where the selection step can be deferred until all sub-agents have completed.

## Opinions

- **The judging experience in the skill-based implementation is far superior to what we had before. The parent now has a lot more context over what each sub-agent did — and the user can ask it to stitch together pieces from different implementations, which was not possible before.** The previous hardcoded version forced you to pick one model and stick with it. — David Gomes, Cursor ("Replacing 12K LOC with a 200-LOC Skill", AI Engineer 2026), [https://www.youtube.com/watch?v=WE_Gnowy3uw](https://www.youtube.com/watch?v=WE_Gnowy3uw)

## Sources

- David Gomes, "Replacing 12K LOC with a 200-LOC Skill", AI Engineer 2026 — [https://www.youtube.com/watch?v=WE_Gnowy3uw](https://www.youtube.com/watch?v=WE_Gnowy3uw)

## Notes
