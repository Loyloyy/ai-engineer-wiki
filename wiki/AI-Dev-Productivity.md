# AI-Dev-Productivity

Empirical findings from a 3-year Stanford longitudinal study on the impact of AI coding tools on developer productivity across 100K+ engineers at 600+ companies.

## Methodology

Existing studies have three weaknesses: counting commits and PRs (task size varies), greenfield controlled experiments (real codebases aren't greenfield), and surveys (correlation near zero with actual productivity). The Stanford group's approach:

- Access to private git repositories from 600+ companies (enterprise, mid-sized, startups)
- LLM-analyzed commit content: quantifies functionality delivered per commit by type (added, removed, refactored, reworked)
- **Rework vs. refactoring**: both modify existing code, but rework alters recent code — a signal of waste. Refactoring may be intentional; rework usually isn't.
- Validated against expert panel evaluation (panel of 10-15 engineers agree well; model approximates panel efficiently)
- Time-series: access to git history predating AI adoption, capturing pre/post transitions

## Key findings

**Net productivity gain from AI: 15–20% on average** across all industries. Gross gain is 30–40%, but AI introduces rework (fixing AI-introduced bugs) that consumes 10–15% of that gain.

**Task complexity × project maturity matrix** (136 teams, 27 companies):

| | Greenfield | Brownfield |
|---|---|---|
| **Low complexity** | 30–40% gain | 15–20% gain |
| **High complexity** | 10–15% gain | 0–10% gain |

For enterprise settings (not personal projects or vibe coding). Greenfield AI gains would be substantially higher in unconstrained settings.

**Language popularity matters**: Low-popularity languages (COBOL, Haskell, Elixir) produce minimal AI gains on low-complexity tasks and can *decrease* productivity on complex tasks — the model generates subtly wrong code that makes developers slower. Most real-world development is in high-popularity languages (Python, Java, TypeScript), where gains are 10–20%.

**Codebase size**: gains decrease logarithmically as codebase size increases. Context window limitations, signal-to-noise degradation, and domain-specific logic density all contribute. NOLA benchmark data shows model coding performance drops from ~90% to ~50% as context grows from 1K to 32K tokens — and degrades further beyond that.

## Ghost engineers

A separate finding from the same research group: approximately 10% of software engineers in their dataset (sampled at ~50K engineers) were "ghost engineers" — collecting a paycheck but contributing effectively nothing. Data-driven developer productivity measurement surfaces this without manager visibility or surveys. The inverse failure — ranking engineers by a gameable proxy like token consumption rather than delivered functionality — is its own anti-pattern (see [Token-Maxing-Culture](Token-Maxing-Culture.md)).

## Opinions

- **AI increases developer productivity, but not equally and not always.** Gains depend on task complexity, project maturity, language popularity, and codebase size. Teams that assume uniform gains will misallocate effort. — Yegor Denisov-Blanch, Stanford ("Does AI Actually Boost Developer Productivity? 100K Devs Study", AI Engineer 2025), [https://www.youtube.com/watch?v=tbDDYKRFjhk](https://www.youtube.com/watch?v=tbDDYKRFjhk)
- **Surveys are near-useless for measuring developer productivity.** Developers misjudge their own productivity by ~30 percentile points on average; only 1 in 3 correctly place themselves within their own quartile. Git history is authoritative; self-report is not. — Yegor Denisov-Blanch, Stanford ("Does AI Actually Boost Developer Productivity? 100K Devs Study", AI Engineer 2025), [https://www.youtube.com/watch?v=tbDDYKRFjhk](https://www.youtube.com/watch?v=tbDDYKRFjhk)
- **AI is most dangerous in high-complexity brownfield tasks** — it generates confident-looking code that introduces subtle bugs, consuming the developer's time on rework rather than forward progress. 0–10% net gain in this quadrant. — Yegor Denisov-Blanch, Stanford ("Does AI Actually Boost Developer Productivity? 100K Devs Study", AI Engineer 2025), [https://www.youtube.com/watch?v=tbDDYKRFjhk](https://www.youtube.com/watch?v=tbDDYKRFjhk)

- **30% faster delivery for daily AI coding assistant users, with lighter PRs.** Booking.com measured developers using Cody daily versus non-users: daily users shipped 30%+ more MRs in a given month and those MRs contained less code — a pattern not yet fully understood but likely reflecting sharper task scoping. — Bruno Passos, Booking.com ("Building AI Agents With Real ROI in the Enterprise SDLC", AI Engineer 2025), [https://www.youtube.com/watch?v=UXOLprPvr-0](https://www.youtube.com/watch?v=UXOLprPvr-0)

- **Training developers is the unlock, not just tool access.** At Booking.com, developers who had access but hadn't been trained on AI tools were low adopters. Once trained, usage and satisfaction jumped — the tool wasn't the barrier; knowing how to work with LLMs was. — Bruno Passos, Booking.com ("Building AI Agents With Real ROI in the Enterprise SDLC", AI Engineer 2025), [https://www.youtube.com/watch?v=UXOLprPvr-0](https://www.youtube.com/watch?v=UXOLprPvr-0)

## Sources

- Yegor Denisov-Blanch, Stanford, "Does AI Actually Boost Developer Productivity? 100K Devs Study", AI Engineer 2025 — [https://www.youtube.com/watch?v=tbDDYKRFjhk](https://www.youtube.com/watch?v=tbDDYKRFjhk)
- Bruno Passos (Booking.com) & Beyang Liu (Sourcegraph), "Building AI Agents With Real ROI in the Enterprise SDLC", AI Engineer 2025 — [https://www.youtube.com/watch?v=UXOLprPvr-0](https://www.youtube.com/watch?v=UXOLprPvr-0)

## Notes

