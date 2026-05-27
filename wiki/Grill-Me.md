# Grill-Me

A Claude Code skill that forces exhaustive bidirectional questioning before any planning or code generation begins, with the goal of building a shared design concept between the developer and the model.

## Origin

Created by Matt Pocock, published in his GitHub repo `macpocockskills`. As of AI Engineer 2026, the repo had accumulated approximately 13,000 stars — significant organic traction relative to its simplicity. The skill prompt is short: *"Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one by one."*

## Mechanism

When invoked, Grill-Me turns the model adversarial: instead of immediately generating a plan or code, it interrogates the developer about every dimension of what they want to build. It works through the design tree recursively — for each decision, it asks about downstream dependencies before moving on. Pocock reports 40–100 questions before the model is satisfied that a shared understanding has been reached. The resulting conversation is used as input to a PRD. In Pocock's full workflow (documented in his "Workflow for AI Coding" workshop), the PRD is subsequently broken into [Vertical-Slices](Vertical-Slices.md) as ordered issue files, which are then executed autonomously via the [Ralph-Loop](Ralph-Loop.md). Grill-Me is the planning entry point; the loop is the execution half.

The underlying concept Grill-Me operationalises comes from Frederick P. Brooks' *The Design of Design*: the idea of a **design concept** — the invisible, shared theory of what is being built that exists in the minds of collaborators. Pocock's diagnosis is that developer-AI pairs almost never establish a shared design concept before coding begins, and the mismatch manifests as "AI didn't do what I wanted" failures.

## Concrete example

Developer wants to add a new feature. Without Grill-Me: types intent into Claude Code, gets a plan generated in 30 seconds, implementation starts, something is wrong, iterate. With Grill-Me: model asks about the feature's relationship to existing modules, whether the interface should be synchronous or async, what the failure modes are, how it interacts with three other parts of the system the developer had not consciously thought about. After 40 questions, the developer has externalised a complete design concept. The subsequent implementation has far fewer surprises because the model is working from the same mental model as the developer.

## Contrast with adjacent ideas

**Claude Code plan mode** is the built-in alternative. Pocock is explicit in his critique: plan mode is "extremely eager to create an asset" — it wants to produce a plan document and start working as quickly as possible. This optimises for time-to-first-output, not for shared understanding. Grill-Me deliberately slows down to front-load the alignment work.

**[Ubiquitous-Language](Ubiquitous-Language.md)** is complementary: once a shared design concept exists, a ubiquitous language file ensures the terminology of that concept is consistently used in all subsequent code and conversation.

**[Spec-Driven-Code-Generation](Spec-Driven-Code-Generation.md)** is the anti-pattern Grill-Me addresses. Spec-driven generation assumes the spec captures design intent adequately; Grill-Me reveals how much intent is left implicit in any written spec.

## Opinions

- **Reaching a shared design concept before planning is better than plan mode.** Plan mode is eager to produce an asset; Grill-Me forces the slower, harder work of actually aligning on what you're building. This is a non-obvious choice — faster outputs feel like progress but miss the root cause of most AI coding failures. — Matt Pocock, independent educator ("Software Fundamentals Matter More Than Ever", AI Engineer 2026), [https://www.youtube.com/watch?v=v4F1gFy-hqg](https://www.youtube.com/watch?v=v4F1gFy-hqg)

## Sources

- Matt Pocock, "Software Fundamentals Matter More Than Ever", AI Engineer 2026 — [https://www.youtube.com/watch?v=v4F1gFy-hqg](https://www.youtube.com/watch?v=v4F1gFy-hqg)
- Matt Pocock, "Full Walkthrough: Workflow for AI Coding", AI Engineer 2026 — [https://www.youtube.com/watch?v=-QFHIoCo-Ko](https://www.youtube.com/watch?v=-QFHIoCo-Ko)

## Notes
