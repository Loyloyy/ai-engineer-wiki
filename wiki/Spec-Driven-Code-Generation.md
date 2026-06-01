# Spec-Driven-Code-Generation

A workflow in which a developer writes a natural-language or structured specification describing how software should behave, then uses an LLM to generate the implementation from that spec — and iterates by modifying the spec rather than the code directly.

## Mechanism

The workflow operates as a compiler loop: write spec → generate code → observe failure → update spec → regenerate. The developer is positioned upstream of the code, treating the implementation as a disposable artifact that gets re-derived from the spec on each iteration. In principle, this means the developer never needs to read or maintain the generated code — it is always a fresh output.

Advocates argue this raises the abstraction level: humans think in behaviour and intent; the spec captures that; the code is an implementation detail. The phrase "code is cheap" is the rallying claim — if code can be regenerated at will, the cost of a wrong implementation approaches zero.

## The software entropy problem

Matt Pocock's empirical critique: in practice, each regeneration compounds entropy. The Pragmatic Programmer defines software entropy as the tendency of a codebase to degrade with each change when the developer is thinking locally (about the immediate change) rather than globally (about the design of the whole system). Spec-driven generation amplifies this dynamic because the model has no durable memory of prior design decisions — each regeneration is, in effect, a local change made without global design awareness.

Pocock ran the loop repeatedly and observed the pattern: first generation was tolerable, second was worse, third was worse still. The spec-to-code compiler, run iteratively, produced monotonically degrading code.

## Why "code is cheap" is the wrong frame

The cost of code is not in its initial production — LLMs have genuinely reduced that. The cost is in the *changeability* of the resulting codebase over time. A codebase with high entropy (shallow modules, unclear interfaces, inconsistent terminology) cannot absorb future AI-generated changes reliably. The AI itself performs worse in a poorly-structured codebase because it cannot navigate the dependency graph efficiently.

Pocock's counter-claim: **bad code is now more expensive than it has ever been**, precisely because it taxes the AI's ability to reason about and extend it. The multiplier has flipped — good code quality now unlocks AI leverage; bad code quality destroys it.

## Contrast with adjacent ideas

**[Grill-Me](Grill-Me.md)** is a direct counter-pattern: instead of skipping to generation, it forces exhaustive alignment on intent before any code is written. This does not eliminate AI code generation — it changes when generation happens (after shared understanding is reached) and on what basis (a durable design concept, not a one-shot spec).

**Vibe coding** is the informal version of the same failure mode: generate, observe result, regenerate, without structured feedback or design intent. Pocock explicitly frames spec-driven generation as "vibe coding by another name" — the spec is an attempt to formalise input, but the core problem (no design-level reasoning between iterations) is identical.

**Test-driven development** ([Grill-Me](Grill-Me.md) → TDD chain) is the structural alternative: the feedback loop is built from automated tests rather than human observation of outputs, forcing small deliberate steps and giving the model a verifiable signal on each change.

**[Validation-Contract](Validation-Contract.md)** is the multi-agent form of the same instinct: define correctness as a contract written during planning, before implementation, so adversarial validators check behaviour the agent never got to shape.

## The case for specification-first development

Sean Grove (OpenAI, 2025) argues the opposite valence: specifications are *more* powerful than code, not a naive shortcut to it.

His argument: code is a **lossy projection from the specification**. A compiled binary cannot be decompiled back to well-commented, intention-revealing source — you have to infer what the programmer was trying to do. In the same way, even well-written code typically doesn't embody the full intentions and values behind it. The source specification has that. A sufficiently robust specification given to an LLM can produce TypeScript, Rust, documentation, tutorials, and blog posts — targeting any architecture from a single source.

The vibe coding critique from this view: "When we vibe code, we communicate intent via prompts, get code as output, and throw the prompt away. We kept the generated binary and deleted the source." The fix is to treat the specification as the valuable, version-controlled artifact and the code as the generated output.

This reframes the entropy criticism: the spec-driven loop compounds entropy not because specs are the wrong idea, but because developers fail to evolve the spec as the primary artifact — they end up maintaining the generated code, which is the mistake.

Grove extends the model to AI alignment: a written specification (like OpenAI's model spec) serves as a trust anchor for humans and as both training and eval material for models (via "deliberative alignment": spec + challenging prompt → model response → grader scores alignment → reinforce weights). Specifications are composable, executable, testable, and have interfaces — they are code for intent rather than syntax.

## Opinions

- **Spec-to-code is vibe coding with extra steps.** The spec is just a structured way of ignoring the codebase. The underlying problem — no ongoing investment in the design of the system — is the same. — Matt Pocock, independent educator ("Software Fundamentals Matter More Than Ever", AI Engineer 2026), [https://www.youtube.com/watch?v=v4F1gFy-hqg](https://www.youtube.com/watch?v=v4F1gFy-hqg)
- **Code is not cheap. Bad code is the most expensive it has ever been.** AI performs well in a good codebase and poorly in a bad one, so code quality is now a multiplier on AI leverage. — Matt Pocock, independent educator ("Software Fundamentals Matter More Than Ever", AI Engineer 2026), [https://www.youtube.com/watch?v=v4F1gFy-hqg](https://www.youtube.com/watch?v=v4F1gFy-hqg)

- **Code is only 10–20% of the value a programmer produces; 80–90% is structured communication.** The person who communicates most effectively is the most valuable programmer. "In the near future, if you can communicate effectively, you can program." — Sean Grove, OpenAI ("The New Code", AI Engineer 2025), [https://www.youtube.com/watch?v=8rABwKRsec4](https://www.youtube.com/watch?v=8rABwKRsec4)
- **You shred the source and version-control the binary.** Keeping generated code while throwing away prompts is the vibe coding failure mode — the prompt is the source specification, and that's what deserves to be preserved and evolved. — Sean Grove, OpenAI ("The New Code", AI Engineer 2025), [https://www.youtube.com/watch?v=8rABwKRsec4](https://www.youtube.com/watch?v=8rABwKRsec4)

## Sources

- Matt Pocock, "Software Fundamentals Matter More Than Ever", AI Engineer 2026 — [https://www.youtube.com/watch?v=v4F1gFy-hqg](https://www.youtube.com/watch?v=v4F1gFy-hqg)
- Sean Grove, "The New Code", AI Engineer 2025 — [https://www.youtube.com/watch?v=8rABwKRsec4](https://www.youtube.com/watch?v=8rABwKRsec4)

## Notes
