# Agent-Legible-Codebase

A codebase structured so that AI agents can navigate, understand, and extend it reliably — prioritising explicit code flow, unique identifiers, and simple primitives over developer ergonomics that depend on implicit conventions or magic.

Distinct from [Deep-Modules](Deep-Modules.md), which focuses on hiding complexity behind clean interfaces. Agent-legibility focuses on removing hidden complexity altogether so agents don't need to infer what they can't read.

## Design principles

**Modularise code flow explicitly**: structure the codebase around RL-style patterns where agent tasks map cleanly to discrete, bounded modules. Avoid designs where "understanding what this code does" requires tracing through multiple layers of abstraction.

**No hidden magic**: framework magic (auto-wiring, convention-based routing, implicit defaults) is particularly dangerous in agent-modified codebases. The config-file-with-defaults anti-pattern — where a config file silently applies defaults that change behaviour — is a common example: an agent modifies the config, the behaviour changes in ways not visible in the diff, and the bug is hard to trace. Agents optimise for visible progress, not invisible correctness.

**Unique function names**: avoid overloaded function names or names that appear in multiple modules. Agents navigating by symbol search will confuse similarly-named functions across contexts.

**Single primitive/component libraries**: pick one button, one modal, one date picker. Agents exposed to multiple competing implementations of the same UI primitive will mix them. The decision cost is low; the consistency payoff is high.

**Erasable TypeScript mode**: write TypeScript in a style where types can be stripped to valid JavaScript without semantic change. Avoids type-level magic that agents may not correctly maintain when modifying code.

**Libraries over products for agents**: when building tools that agents will use, prefer clean library interfaces over opinionated product abstractions. Libraries expose the primitives; products hide them behind opinions. Agents navigate primitives better.

## Human callout extensions

A practical pattern from [Pi](Pi.md): define a set of "dangerous action" categories (database migrations, permission changes, destructive file operations) and wire them to a human confirmation step via an extension. The agent can propose the change but cannot execute it without explicit human approval. Workflow tools like [n8n](n8n.md) implement the same gate at the node level — the agent proposes a tool call, a human approves, denies, or redirects before it executes.

The principle: **"don't let the agent decide" on irreversible or high-consequence operations**. The agent's judgment on a schema migration may be correct 95% of the time; the 5% failure on a production database is unacceptable. Route those decisions to humans at the harness level, not at the agent's discretion.

## The psychological trap

Armin Ronacher's framing: AI coding tools are addictive because they produce a false efficiency signal — visible output (code written, files created) feels like progress even when that output is fragile or incorrect. This breaks the code review ratio: producers (agents) can generate far more code than reviewers (humans) can evaluate. Non-engineers shipping agent-generated code without accountability accelerates this asymmetry.

**"Friction is your judgment"**: the moments where you slow down, review carefully, or push back are precisely the moments of highest engineering value. Removing friction from agent interactions removes those judgment opportunities.

## Opinions

- **Agents optimise for progress, not correctness** — an agent told to "fix the bug" will find the path of least resistance to passing tests, not the architecturally sound fix; codebases designed with no hidden magic remove the shortcuts that lead agents to fragile solutions. — Armin Ronacher (The Friction Is Your Judgment, AI Engineer 2026), [link](https://www.youtube.com/watch?v=_Zcw_sVF6hU)

- **The code review ratio is broken** — with agents as producers, the number of lines written per day vastly exceeds what human reviewers can evaluate with care; the answer is not to review faster but to constrain what agents can produce through harness design and legibility conventions. — Armin Ronacher (The Friction Is Your Judgment, AI Engineer 2026), [link](https://www.youtube.com/watch?v=_Zcw_sVF6hU)

- **"Friction is your judgment"** — the friction you feel before approving an agent action is not inefficiency to be optimised away; it is the signal that your engineering expertise is actually engaged; removing it removes the thing that makes you valuable. — Armin Ronacher (The Friction Is Your Judgment, AI Engineer 2026), [link](https://www.youtube.com/watch?v=_Zcw_sVF6hU)

- **Super clean modular code is a multiplier on AI leverage.** A rearchitected repo with clear module boundaries and good documentation lets AI contribute meaningfully to every module. A sprawling codebase with unclear interfaces locks out AI assistance in all but the most obvious spots. At DataLab (team of 3–4), this is what enables a 2-person team to handle model training, inference, and integration in parallel. — Vik Paruchuri, DataLab ("Small AI Teams with Huge Impact", AI Engineer 2025), [https://www.youtube.com/watch?v=K-iYKDMFKhE](https://www.youtube.com/watch?v=K-iYKDMFKhE)

## Sources

- Armin Ronacher (The Friction Is Your Judgment, AI Engineer 2026) — [YouTube](https://www.youtube.com/watch?v=_Zcw_sVF6hU)
- Vik Paruchuri, DataLab, "Small AI Teams with Huge Impact", AI Engineer 2025 — [https://www.youtube.com/watch?v=K-iYKDMFKhE](https://www.youtube.com/watch?v=K-iYKDMFKhE)

## Notes

