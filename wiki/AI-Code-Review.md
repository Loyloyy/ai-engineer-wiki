# AI-Code-Review

Applying LLMs to automated pull request review — finding bugs, flagging security issues, and surfacing documentation mismatches — with a two-axis framework for what to prompt the reviewer to do.

## The two-axis taxonomy

From operating millions of AI code reviews (Graphite/Diamond product), Tomas Reimers identified that prompting an LLM to leave "all code review comments" produces two types of bad output:

**Axis 1: What the LLM can and can't catch**
- CAN catch: logical bugs (division by zero, uninstantiated objects), accidentally committed code, performance issues, security concerns, documentation mismatches (code says one thing, comment says another)
- CANNOT catch reliably: tribal knowledge ("we stopped doing X because of incident Y in 2022" — exists in senior dev heads, not training data)

**Axis 2: What developers want and don't want from an LLM reviewer**
- WANT to receive: the bug/security/documentation catches above
- DON'T WANT to receive: code cleanliness and best-practice comments ("add a docstring here", "extract this into a function", "add a test") — technically always correct but context-dependent, and developers find it pedantic from a bot even when they'd accept it from a human

**The target zone (top-right quadrant)**: comments the LLM can correctly generate AND that developers want to receive. Prompt only for this zone. Everything outside it degrades developer trust in the tool.

## Measuring success

Two metrics:
1. **Downvote rate**: explicit negative reactions from developers (< 4% is achievable and healthy)
2. **Action rate**: what percentage of comments lead to code changes in the PR. Human code reviewers average ~50% action rate (not all comments are addressed in the same PR — fix-forwards, disagreements, and FYI comments account for the rest). An AI reviewer should target parity with humans on this metric, not 100%.

Graphite achieved 52% action rate from their AI reviewer (vs. ~50% human baseline) by restricting the prompt to only the target quadrant.

## Practical rules

- Don't ask the LLM "what code review comments would you leave?" — it leaves everything, including outside the target zone
- Prompt specifically for the categories in the target quadrant: bugs, accidentally committed code, performance, security, doc mismatches
- Explicitly exclude code cleanliness and best-practice feedback from the prompt
- Track action rate, not just upvote/downvote, to measure real reviewer value
- Monitor model changes (new Claude versions, new prompts) for quadrant drift — the distribution of comment types can shift as models improve

## Bug detection performance (SM-100)

Ian Butler and Nick Gregory (Bismouth) benchmarked AI agents across 100 real bugs from 84 open-source repositories — a "needle in the haystack" evaluation across Python, TypeScript, JavaScript, and Go:

- Basic agent loop (shell tool + report + loop): 97% false positive rate. The agent finds some bugs but floods developers with noise.
- Best PR-review agent (CodeX): 27% needle-in-haystack detection; Bismouth 17%, Claude Code 16%.
- True positive rate on reported bugs: CodeX 45%, Bismouth 25%, Claude Code 16%. Cursor/Devon/Co-sign: 3–10% true positives out of 900–1,300 reported items.
- Core limitation: agents are narrow thinkers. Even thinking models evaluate files one angle at a time; per-run bugs change but total counts stay consistent — evidence the model is not making a holistic inventory of issues.

Implication: current agents can write software but struggle to manage, maintain, and fix deployed software. SM-100 (software maintenance) represents the back 90% of software engineering work and is largely unsolved.

## Opinions

- **There is stuff LLMs can catch and things humans want to receive — and these are two separate axes.** Naively asking an LLM for code review gets you comments in all four quadrants. Restricting to the top-right (can catch + want to receive) is the entire craft of building an AI code reviewer. — Tomas Reimers, Graphite ("Lessons from Millions of AI Code Reviews", AI Engineer 2025), [https://www.youtube.com/watch?v=TswQeKftnaw](https://www.youtube.com/watch?v=TswQeKftnaw)
- **Measure review quality by action rate, not sentiment.** A code review comment exists to get code changed. If 52% of your AI comments lead to changes — parity with human reviewers — you've succeeded. Upvotes tell you about satisfaction; action rate tells you about utility. — Tomas Reimers, Graphite ("Lessons from Millions of AI Code Reviews", AI Engineer 2025), [https://www.youtube.com/watch?v=TswQeKftnaw](https://www.youtube.com/watch?v=TswQeKftnaw)
- **The most frequently used agents have the worst bug detection rates.** SM-100 benchmark: top agents by market share scored 7% true positive rate on software maintenance bugs. Agents that generate feature code well are systematically failing at the maintenance task that comprises most of a team's actual work. — Ian Butler & Nick Gregory, Bismouth ("Agents Reported Thousands of Bugs. How Many Were Real?", AI Engineer 2025), [https://www.youtube.com/watch?v=wAQK7O3WGEE](https://www.youtube.com/watch?v=wAQK7O3WGEE)
- **Agents are narrow thinkers — they don't holistically evaluate files.** The per-run total of bugs stays consistent, but the specific bugs change run-to-run. This means agents are exploring files from a single angle per run rather than inventorying all issues. Broader thinking chains and deeper pursuit of selected chains are required. — Ian Butler & Nick Gregory, Bismouth ("Agents Reported Thousands of Bugs. How Many Were Real?", AI Engineer 2025), [https://www.youtube.com/watch?v=wAQK7O3WGEE](https://www.youtube.com/watch?v=wAQK7O3WGEE)

## Sources

- Tomas Reimers, Graphite, "Lessons from Millions of AI Code Reviews", AI Engineer 2025 — [https://www.youtube.com/watch?v=TswQeKftnaw](https://www.youtube.com/watch?v=TswQeKftnaw)
- Ian Butler & Nick Gregory, Bismouth, "Agents Reported Thousands of Bugs. How Many Were Real?", AI Engineer 2025 — [https://www.youtube.com/watch?v=wAQK7O3WGEE](https://www.youtube.com/watch?v=wAQK7O3WGEE)

## Notes

