# Eval-Flywheel

A continuous improvement loop connecting production observability to offline evals: real agent traces surface failure modes, which inform new scoring functions, which drive agent improvements, which then go to production and generate new traces.

## Mechanism

The flywheel has four stages that repeat throughout the lifetime of a production agent:

1. **Production observability**: the deployed agent runs against real users. Traces are collected, stored, and monitored. Online eval scoring functions can be applied to live traffic to generate alerts.

2. **Failure mode discovery**: production trace data reveals how users actually interact with the agent — including edge cases and failure modes not present in the original test set. Topic modeling and clustering can surface "unknown unknowns": patterns in how the agent fails that the team didn't anticipate.

3. **Offline experiments**: real production examples are pulled into an offline eval environment. The team modifies the agent (prompt changes, model upgrades, tool changes), runs the modified agent against the same examples, and compares scores.

4. **Deployment**: a higher-confidence version of the agent is deployed to production. The cycle restarts.

The flywheel accelerates because each iteration refines both the agent and the scoring functions. Finding the best failure modes requires production data; improving the agent requires evals against those failures; getting production data requires a deployed agent.

## Why it's a systems problem

The flywheel sounds simple but becomes a hard engineering problem at scale. Key technical challenges:
- **Dual query patterns**: the trace data must support low-latency retrieval (for live observability dashboards) and aggregate analytics (for offline experiment comparison) simultaneously. These patterns require different storage architectures.
- **Semi-structured large traces**: LLM spans are 10–100× larger and less structured than standard application spans. Standard observability stacks (e.g., open-source data warehouses + DuckDB) break at the volume and query complexity customers actually need.
- **Multi-persona problem**: building a good eval platform requires engineers (for infrastructure), AI engineers (for scoring functions), domain SMEs (for failure mode labeling), and product engineers (for experiment design). The tooling must work for all of them.

Hetzel's conclusion: evals are a systems problem, not a UI/UX problem. Building a frontend that shows eval results is easy. Building the data layer that supports the full flywheel at production scale is hard.

## Practical application

Entry points at different maturity levels:
- **Spreadsheet + for-loop**: the minimum viable eval. Documents outputs; doesn't support real experimentation. Valuable as a starting point.
- **Custom eval UI**: more approachable for non-technical stakeholders; still lacks production observability connection.
- **Connected flywheel**: production traces feed offline evals; scoring functions operate on live traffic; the loop closes.

Hetzel recommends not building the connected flywheel from scratch. The data layer complexity is underestimated; teams that vibe-code their own eval platform inherit ongoing maintenance of a hard infrastructure problem.

## Contrast with adjacent ideas

**[Verifiers-Rule](Verifiers-Rule.md)** establishes that agent quality is bounded by verifiability. The eval flywheel is the operational mechanism for maximizing that verifiability over time: evals are the verifier; the flywheel is how you build and improve them.

**[High-Bandwidth-Artifacts](High-Bandwidth-Artifacts.md)**: production traces are a form of high-bandwidth artifact — structured records of agent work that enable human review and improvement. The flywheel converts these artifacts into agent improvement.

## Opinions

- **Evals are a systems problem, not a UI/UX problem.** The frontend is easy to vibe-code. The data layer — handling large, semi-structured, high-velocity traces with multiple query patterns — is the hard part that teams consistently underestimate. — Phil Hetzel, Braintrust ("Why Building Eval Platforms is Hard", AI Engineer 2026), [https://www.youtube.com/watch?v=_fQ7Z_Wfouk](https://www.youtube.com/watch?v=_fQ7Z_Wfouk)
- **The best way to find failure modes is production data.** You can't pre-imagine how users will interact with your agent. The flywheel exists to surface what you didn't know to test for. — Phil Hetzel, Braintrust ("Why Building Eval Platforms is Hard", AI Engineer 2026), [https://www.youtube.com/watch?v=_fQ7Z_Wfouk](https://www.youtube.com/watch?v=_fQ7Z_Wfouk)

## Sources

- Phil Hetzel, "Why Building Eval Platforms is Hard", AI Engineer 2026 — [https://www.youtube.com/watch?v=_fQ7Z_Wfouk](https://www.youtube.com/watch?v=_fQ7Z_Wfouk)

## Notes
