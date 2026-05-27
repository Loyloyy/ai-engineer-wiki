# Continuous Compute

An infrastructure paradigm for agent-scale software delivery that replaces traditional CI/CD — embedding validation inside the agent loop, eliminating the PR as the unit of human coordination, and introducing stateful compute environments that agents work within continuously.

## Why CI/CD breaks at agent scale

Traditional CI/CD was designed around human developer pace: one or two PRs per developer per week, human code review, sequential build/test/deploy steps. The underlying assumptions are sequential coordination, warm local caches, and humans as the serialization layer.

Agents break these assumptions:
- **Volume**: N agents × N PRs × N repos simultaneously. Merge queues become serialization bottlenecks equivalent to database lock contention under high write load.
- **Cold starts**: ephemeral CI compute spinning up for every agent invocation wastes significant time on bootstrapping (dependency installation, cache warming). Human developers have always-warm local environments; agents restart from scratch each time.
- **Review overhead**: code review UIs and processes assume a human reader pacing through diffs at human speed. At 4× the historical PR volume per team, individual code review is impossible.

## The new architecture

The emerging pattern at agent-scale shops (companies like Fall, Zed, Ramp):

**1. Intent and spec as the starting point.** A linear ticket, Slack message, or written spec defines the goal. This replaces the PR title/description as the unit of human intent.

**2. Stateful agent harness.** The agent works in a persistent, warm environment — same commit checkout, same dependencies installed, same working state between loop iterations. Not ephemeral. Internal validation (build, test) runs inside the loop on every iteration, not as a separate CI gate. Every change is continuously validated; validation is no longer a separate phase.

**3. Pre-merge queue.** Validated agent changes accumulate in a staging queue rather than going directly to the main branch. Serialization (making sure concurrent agent changes don't conflict) is handled here — analogous to optimistic concurrency control in databases. Multiple agents can produce changes in parallel; the pre-merge queue reconciles them.

**4. Semantic approval.** The human reviewer no longer reads diffs. They review: (a) the original intent, and (b) the output — a video of the feature working, the output of a security-focused LLM review, functional test results. At 4× historical PR volume, this is the only review model that scales.

## Multiverse / parallel candidates

In the near-future state: when inference is fast enough and the inner loop is tight enough, agents may explore multiple implementations of the same spec simultaneously — working on different candidate commits in parallel ("the multiverse"). The pre-merge queue selects the best candidate, or human judgment chooses among semantic alternatives. Resource consumption scales accordingly (more parallel candidates = more compute).

## Governance and invariants

CI did not only test code — it enforced compliance invariants (well-known checkout, no unvetted code sources, audit trail). These invariants don't disappear with continuous compute; they move into the harness. The harness enforces that every iteration starts from a known-good state, that compliance rules are checked on every generated commit, and that the governance log is maintained. The difference is enforcement is continuous, not gated.

## Connection to durable agents

Continuous compute requires the same stateful infrastructure described in [Durable-Agent-Execution](Durable-Agent-Execution.md). A warm agent environment that persists between loop iterations, survives external waiting (merge conflicts, reviewer unavailability), and can checkpoint/restore is the compute substrate that makes continuous compute economically viable.

## Opinions

- **Traditional CI/CD is designed for human pacing and cannot handle agent-scale PR volume.** The PR is a coordination primitive for delayed human handoffs. At N agents × N PRs, it's impossible for human reviewers to look at every PR. The architecture needs to change. — Hugo Santos, Namespace ("CI/CD Is Dead: Agents Need Continuous Compute", AI Engineer 2026), [https://www.youtube.com/watch?v=VktrqzQgytY](https://www.youtube.com/watch?v=VktrqzQgytY)
- **Code merging is a database problem.** Git repositories are ledgers. At human scale, merge locks are held long enough to be irrelevant; at agent scale, merge serialization becomes the bottleneck. The time-to-merge matters, and it needs a new architecture. — Hugo Santos, Namespace ("CI/CD Is Dead: Agents Need Continuous Compute", AI Engineer 2026), [https://www.youtube.com/watch?v=VktrqzQgytY](https://www.youtube.com/watch?v=VktrqzQgytY)
- **Humans review intent + result, not code.** At agent-scale PR volumes, humans cannot read every diff. The reviewable artifact is: here is what was intended, here is evidence it works (demo video, security report). Code diffs become invisible to humans. — Hugo Santos, Namespace ("CI/CD Is Dead: Agents Need Continuous Compute", AI Engineer 2026), [https://www.youtube.com/watch?v=VktrqzQgytY](https://www.youtube.com/watch?v=VktrqzQgytY)

## Sources

- Madison (NEA) & Hugo Santos, Namespace, "CI/CD Is Dead: Agents Need Continuous Compute", AI Engineer 2026 — [https://www.youtube.com/watch?v=VktrqzQgytY](https://www.youtube.com/watch?v=VktrqzQgytY)

## Notes
