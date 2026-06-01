# Token-Maxing-Culture

Perverse incentive pattern in large engineering organisations where AI token consumption is measured, ranked, or targeted — leading engineers to generate tokens artificially rather than productively.

## How it emerges

Token usage became a proxy metric for AI adoption after leadership at large companies decided to measure whether engineers were using AI tools. Once the metric exists — whether as a leaderboard, a performance evaluation data point, or a minimum spend target — engineers optimise for it. Goodhart's Law applies: the metric ceases to measure what it was supposed to measure.

Documented examples as of April 2026:

**Meta**: had an internal leaderboard displaying per-engineer token output. Used in performance evaluations as one of many data points (alongside code diffs, impact, and code review contributions). Low token count combined with low performance = "clearly not even trying." High token count combined with high performance = "clearly innovating." Engineers responded by running agents on low-value tasks — asking agents to summarise documentation they would have read directly, generating unnecessary questions to push the count up. The leaderboard was removed after press coverage made it look bad, but the behaviour continued because engineers assumed token count was still tracked.

**Microsoft**: similar leaderboard. Engineers observed running autonomous agents to generate junk output solely to increase their visible token count.

**Salesforce**: a minimum monthly spend target of approximately $175 per employee across AI tools. Engineers token-max at the start of the month to hit the floor.

**Coinbase**: Brian Armstrong sent a company-wide email requiring all engineers to adopt AI tools within a week; fired an engineer shortly after as a signal. No token leaderboard — adoption was enforced through direct managerial action.

## Root cause

The pattern originates from a legitimate leadership concern: engineers at established companies with large legacy codebases were slower to adopt AI tools than engineers at new startups or AI-native companies. Leadership, observing AI revenue growth at Anthropic and OpenAI, concluded that higher AI usage correlated with better outcomes and tried to mandate adoption through measurement.

The problem is that token consumption is a lagging indicator of useful AI use, not a leading one, and is trivially gameable.

## Relationship to lines-of-code metrics

Token maxing is structurally identical to the lines-of-code productivity metrics that velocity tools like Pluralsight Flow introduced in the 2010s. Those metrics were widely criticised for incentivising verbose, low-quality code. Token maxing is the 2025 equivalent — same failure mode, now adopted by the same large companies that should have learned from the earlier experience. Rigorous, outcome-based measurement (see [AI-Dev-Productivity](AI-Dev-Productivity.md)) shows the alternative: quantify delivered functionality from git history, not a gameable proxy.

## Opinions

- **Token maxing is Goodhart's Law applied to AI adoption** — it started as engineers genuinely excited about building things, and has become engineers running junk agents to hit a number; the metric destroyed the behaviour it was meant to encourage. — Gergely Orosz (A Conversation with Gergely Orosz, AI Engineer 2026), [link](https://www.youtube.com/watch?v=CS5Cmz5FssI)

- **The companies enforcing token metrics are the same ones that ran lines-of-code leaderboards 10 years ago** — Meta and Microsoft are repeat offenders at measuring the wrong thing in developer productivity; the specific metric changes but the management failure is the same. — Gergely Orosz (A Conversation with Gergely Orosz, AI Engineer 2026), [link](https://www.youtube.com/watch?v=CS5Cmz5FssI)

- **Individual engineers at high-paying jobs are rational to token max** — when you earn $300-400K base plus equity and the leaderboard is visible to your manager, the cost of being in the bottom quartile on any tracked metric is too high to risk on principle; the problem is the system, not the engineers. — Gergely Orosz (A Conversation with Gergely Orosz, AI Engineer 2026), [link](https://www.youtube.com/watch?v=CS5Cmz5FssI)

## Sources

- Gergely Orosz, "A Conversation with Gergely Orosz, @pragmaticengineer", AI Engineer 2026 — [YouTube](https://www.youtube.com/watch?v=CS5Cmz5FssI)

## Notes

