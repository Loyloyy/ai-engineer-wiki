# Coordination-Debt

The accumulated cost of skipped team alignment in AI-assisted development — wasted work, duplicate effort, and features nobody asked for, produced when agents enable fast code generation but teams fail to agree on what to build before agents start working.

## Mechanism

Coordination debt accumulates when the pace of implementation outstrips the pace of alignment. In traditional software development, the slow speed of implementation created natural alignment checkpoints: draft PRs, design discussions, Slack threads, code reviews with context. The implementation window was long enough for everyone to get on the same page before code merged.

AI agents collapse the implementation window to minutes. A developer can log an issue and open a PR in the time it used to take to write a spec. This removes most alignment checkpoints and compresses any remaining ones to the back of the process — the PR review — where they are too late to course-correct cheaply.

Concrete manifestations:
- **Duplicate work**: two developers each prompt an agent to implement the same feature independently, both ship PRs
- **Hairy merge conflicts**: agents touch the same files because no one coordinated on file ownership
- **Features nobody asked for**: unshared plan mode produces code that satisfies the literal prompt but misses business intent
- **Stacked PR queues**: reviewers face PRs with no context about the decisions that led to the code

Appleton's framing: "When production is cheap, opportunity cost becomes the real cost." Every AFK-built feature carries the cost of everything else that was not built instead.

## Why existing tools don't help

GitHub, Slack, Jira, Linear — current coordination tooling was designed for a world where implementation is slow and sequential. They assume alignment conversations happen before and during development. They provide no shared space for teams to align on a plan, gather context, and direct agents as a collective before implementation begins.

PRs were designed for code review, not for team alignment. Using them as the primary alignment mechanism in an agentic world means all the correction happens after the work is done.

## The structural fix

Appleton's argument: tools must bring planning, context-gathering, and implementation under one roof, with a multiplayer interface that includes all stakeholders (developers, PMs, designers, domain experts) before agents start. The alignment has to happen alongside and ahead of implementation, not only after it.

See [ACE](ACE.md) for GitHub Next's prototype implementation of this model.

## Contrast with adjacent ideas

**Technical debt** accumulates from rushed implementation decisions. Coordination debt accumulates from skipped communication and alignment. The two interact: coordination debt produces features that need rework, which generates technical debt in the rework.

**[High-Bandwidth-Artifacts](High-Bandwidth-Artifacts.md)** provide a structural mechanism for surfacing agent work for human review. Coordination debt is the problem that motivates both high-bandwidth artifacts and multiplayer agent environments.

## Opinions

- **More individual output doesn't solve problems that require communication and coordination — it makes them worse.** The "one dev with two dozen agents" model assumes software is made by one person. It's not. Scaling individual throughput without scaling team alignment amplifies the cost of misalignment. — Maggie Appleton, GitHub Next ("Collaborative AI Engineering", AI Engineer 2026), [https://www.youtube.com/watch?v=ClWD8OEYgp8](https://www.youtube.com/watch?v=ClWD8OEYgp8)
- **All our coordination tools are from another era.** GitHub, Slack, Jira were built for sequential, human-paced development. They are not designed for agentic development. Funneling agentic outputs into them amplifies coordination debt rather than reducing it. — Maggie Appleton, GitHub Next ("Collaborative AI Engineering", AI Engineer 2026), [https://www.youtube.com/watch?v=ClWD8OEYgp8](https://www.youtube.com/watch?v=ClWD8OEYgp8)

## Sources

- Maggie Appleton, "Collaborative AI Engineering", AI Engineer 2026 — [https://www.youtube.com/watch?v=ClWD8OEYgp8](https://www.youtube.com/watch?v=ClWD8OEYgp8)

## Notes
