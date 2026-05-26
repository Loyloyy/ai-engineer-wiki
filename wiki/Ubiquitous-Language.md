# Ubiquitous-Language

A shared, explicitly maintained glossary of domain terms that is used consistently across developer communication, codebase naming, and AI model interactions — so that all parties are reasoning from the same vocabulary.

## Origin

Concept from Eric Evans' *Domain-Driven Design* (DDD). In DDD, the ubiquitous language bridges the gap between domain experts (who speak business language) and developers (who speak technical language): both parties agree on a precise set of terms, and those terms appear verbatim in code identifiers, documentation, and all conversations.

Matt Pocock adapts the concept for the developer-AI pair: the "domain expert" role is played by the developer; the "developer" role is played by the AI; the ubiquitous language prevents the drift between what the developer intends and what the AI understands.

## Mechanism

In practice: a markdown file of tables, each row a term with a definition. The file is generated via a Claude Code skill that scans the codebase for recurring terminology and surfaces it for human review. Once established, the developer:

- Reads the file during planning sessions to stay aligned on terminology
- References it when prompting the AI ("the *claim processor* should invoke the *eligibility checker*")
- Ensures the AI's generated code uses these identifiers, not synonyms or paraphrases

Pocock reports two observable effects from reading the model's thinking traces: (a) the AI thinks in a less verbose way when a ubiquitous language is present — it does not need to resolve ambiguity mid-thought; (b) the resulting implementation is more aligned with what was planned, because the planning conversation and the code share a common vocabulary.

## Concrete example

Without a ubiquitous language: developer says "check if the user is allowed to do this." AI generates code with variables named `is_permitted`, `can_access`, `has_rights` used inconsistently across files. The developer's mental model calls this operation "eligibility check." The gap creates friction: each prompt requires re-establishing what "eligibility check" means.

With a ubiquitous language: the glossary defines `eligibility_check` with a precise description. The AI uses this term consistently. The developer can say "run the eligibility check before the claim is submitted" and the AI maps directly to the right concept and the right code path without disambiguation.

## Contrast with adjacent ideas

**[Grill-Me](Grill-Me.md)** builds a shared *design concept* — an understanding of what is being built. Ubiquitous language maintains shared *terminology* — the words used to refer to the pieces. They are complementary: Grill-Me front-loads alignment on intent; ubiquitous language sustains alignment on vocabulary throughout the project.

**CLAUDE.md / system prompts** are a related mechanism for priming the model with project context. A ubiquitous language file can be included in or referenced from a system prompt, but the discipline of explicitly naming and defining terms is distinct from general project instructions.

**Code style guides** govern syntax and structure. A ubiquitous language governs *meaning* — what the names refer to. The two are orthogonal.

## Opinions

- **A ubiquitous language is a powerhouse for AI-assisted development.** It reduces AI verbosity, improves planning accuracy, and aligns implementation with intent — effects visible in the model's own thinking traces. — Matt Pocock, independent educator ("Software Fundamentals Matter More Than Ever", AI Engineer 2026), [https://www.youtube.com/watch?v=v4F1gFy-hqg](https://www.youtube.com/watch?v=v4F1gFy-hqg)

## Sources

- Matt Pocock, "Software Fundamentals Matter More Than Ever", AI Engineer 2026 — [https://www.youtube.com/watch?v=v4F1gFy-hqg](https://www.youtube.com/watch?v=v4F1gFy-hqg)

## Notes
