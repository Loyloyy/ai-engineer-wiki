# Verifiers-Rule

The principle that AI will eventually solve any task that is both solvable and easy to verify — and that the ease of training AI to solve a task is proportional to how verifiable that task is.

## Origin

Coined by Jason Wei (then at OpenAI, now independent researcher) in the context of reinforcement learning: if a task has objective, fast, scalable, low-noise verification, RL can optimise against it. Wei's formulation is primarily about model training — the verification signal enables post-training. His blog post ("Asymmetry of verification and verifier's law", 2025) establishes the theoretical grounding: [jasonwei.net/blog/asymmetry-of-verification-and-verifiers-law](https://www.jasonwei.net/blog/asymmetry-of-verification-and-verifiers-law).

## Extension to agents

Jacob Lauritzen extends the rule from training to agent deployment. If a task is easy to verify, you can run an agent in a loop, feed back the verification signal ("you did this wrong, fix it"), and it will converge. The verification criterion is thus a design input: tasks that can be made verifiable can be handed to agents with high confidence; tasks that cannot be made verifiable require human judgment in the loop.

## The verifiability spectrum

Not all tasks in a vertical sit at the same point:

**Legal:**
- *Easy to verify*: checking whether all defined terms in a contract are used and defined consistently. Objective, fast, automatable.
- *Hard to verify*: whether a contract will hold up in court. The only true verification is a judge's ruling — a signal that arrives years late and only once.
- *Impossible to verify*: litigation strategy. Five lawyers give five different answers; there is no objective truth to optimise against.

**Software:**
- *Easy to verify*: unit tests, type checks, lint rules.
- *Hard to verify*: whether a consumer app will succeed commercially. Verification requires market feedback over months or years.

## Strategies for moving tasks down the spectrum

The practical value of Verifiers-Rule is as a design prompt: if a task currently sits in the "hard to verify" zone, ask whether it can be restructured.

**Test-driven development** moves feature implementation from "does this look right?" to "do these tests pass?" — an objective, near-instant signal. The agent can loop on the test suite without human review.

**Proxy verification** is used when ground-truth is inaccessible. Legora uses golden contracts — a corpus of known-good precedents — as a proxy for contract quality. The agent compares its output against the corpus. It is not perfect verification, but it is fast and scalable, which moves the task meaningfully down the spectrum.

**Task decomposition** splits a hard-to-verify task into sub-tasks, some of which may be individually easy to verify. A full contract review is hard to verify; checking whether all defined terms are consistent is trivial to verify. Decomposing isolates the verifiable sub-tasks and lets agents run unsupervised on those while humans focus attention on the irreducibly hard sub-tasks.

## Contrast with adjacent ideas

**RLHF / reward modelling** is an attempt to construct a learned verifier when no objective signal exists. This is expensive and fragile — Verifiers-Rule implies that tasks requiring learned verifiers will always be harder to automate than tasks with objective verifiers.

**[High-Bandwidth-Artifacts](High-Bandwidth-Artifacts.md)** is a complementary pattern: for tasks that remain hard to verify, the design goal shifts from eliminating human review to making human review faster and higher-bandwidth.

## Opinions

- **The verifiability of a task is the primary design variable for vertical AI.** Before choosing an agent architecture, ask where the task sits on the spectrum and whether you can move it. — Jacob Lauritzen, Legora ("Agents need more than a chat", AI Engineer 2026), [https://www.youtube.com/watch?v=XNtkiQJ49Ps](https://www.youtube.com/watch?v=XNtkiQJ49Ps)
- **Verifier's Rule originated as a claim about RL training, not agents** — the verification signal enables post-training optimisation. Extension to deployed agents is Lauritzen's contribution, not Wei's. — Jason Wei ("Asymmetry of verification and verifier's law", 2025), [jasonwei.net/blog/asymmetry-of-verification-and-verifiers-law](https://www.jasonwei.net/blog/asymmetry-of-verification-and-verifiers-law)

## Sources

- Jacob Lauritzen, "Agents need more than a chat", AI Engineer 2026 — [https://www.youtube.com/watch?v=XNtkiQJ49Ps](https://www.youtube.com/watch?v=XNtkiQJ49Ps)
- Jason Wei, "Asymmetry of verification and verifier's law", 2025 — [https://www.jasonwei.net/blog/asymmetry-of-verification-and-verifiers-law](https://www.jasonwei.net/blog/asymmetry-of-verification-and-verifiers-law)

## Notes
