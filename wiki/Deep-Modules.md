# Deep-Modules

A codebase architecture principle in which modules encapsulate large amounts of functionality behind simple, narrow interfaces — as opposed to shallow modules that expose complex interfaces relative to the functionality they contain.

## Origin

Concept from John Ousterhout's *A Philosophy of Software Design*. Ousterhout argues that the primary driver of software complexity is unnecessary exposure of internal complexity through interfaces — too many small modules with too many entry points force every reader and every caller to understand the internals. Deep modules hide complexity; shallow modules spread it.

## Mechanism

A deep module has two properties in tension: large internal functionality, and a small external surface. The interface is the contract — it is what callers depend on. The implementation is the detail — it can be changed without affecting callers as long as the interface holds.

In a deep-module architecture, the codebase looks like a small number of large, well-bounded units with clean interfaces on top. In a shallow-module architecture, it looks like many small blobs with dense interconnections — the developer must navigate the graph to understand what any given piece does.

Ousterhout's design heuristic: if you could draw your module boundaries differently and expose fewer functions while retaining the same capability, you should.

## Application to AI-assisted development

Pocock identifies two AI-specific benefits of deep modules:

**Navigation**: AI models explore codebases by reading files and tracing imports. In a shallow-module codebase, the dependency graph is wide — the model must visit many files to understand a single operation, and may not reach the right module within its context window. In a deep-module codebase, the relevant logic is concentrated. The model spends fewer tokens navigating and more tokens on the actual problem.

**Delegation boundary**: the interface of a deep module is small and well-defined. The developer can design the interface (the contract) and delegate the implementation to the AI. Because the interface is tested as a boundary, the developer does not need to audit the implementation line-by-line — only verify that the interface contract holds. Pocock calls this "design the interface, delegate the implementation" — a cognitive offload that becomes practical when the interface is narrow enough to reason about fully.

## Concrete example

Two versions of the same codebase: (1) 40 small modules with overlapping responsibilities and 150 exported functions; (2) 8 modules with clear boundaries and 20 exported functions. Same total functionality. In version (1), the AI attempting to add a feature explores 12 files, misses a dependency, and introduces a regression. In version (2), it identifies the 2 relevant modules, reads their interfaces, and generates a correct implementation. Testability follows the same pattern: version (1) requires mocking 8 dependencies per test; version (2) tests at the module interface with 1–2 dependencies.

## Contrast with adjacent ideas

**[Spec-Driven-Code-Generation](Spec-Driven-Code-Generation.md)** tends to produce shallow-module codebases because LLMs generating code locally optimise for the immediate task without global design awareness. The irony: spec-driven generation is more likely to produce code that future AI generations cannot work in effectively.

**Microservices** decompose at the service level, not the module level. A microservice architecture can have deep or shallow modules within each service — the two concepts operate at different granularities.

**[Ubiquitous-Language](Ubiquitous-Language.md)** is complementary: once module boundaries are defined, consistent naming in the ubiquitous language ensures the model understands which module handles which concept.

## Opinions

- **Design the interface, delegate the implementation.** Once a module has a clean, testable interface, the developer can treat the implementation as a gray box — review the contract, not the internals. This is the cognitive model that makes high-velocity AI development sustainable. — Matt Pocock, independent educator ("Software Fundamentals Matter More Than Ever", AI Engineer 2026), [https://www.youtube.com/watch?v=v4F1gFy-hqg](https://www.youtube.com/watch?v=v4F1gFy-hqg)
- **AI is very good at creating shallow-module codebases.** Left unchecked, it will produce code that neither it nor the developer can effectively work in six months later. Actively restructuring toward deep modules is necessary maintenance. — Matt Pocock, independent educator ("Software Fundamentals Matter More Than Ever", AI Engineer 2026), [https://www.youtube.com/watch?v=v4F1gFy-hqg](https://www.youtube.com/watch?v=v4F1gFy-hqg)

## Sources

- Matt Pocock, "Software Fundamentals Matter More Than Ever", AI Engineer 2026 — [https://www.youtube.com/watch?v=v4F1gFy-hqg](https://www.youtube.com/watch?v=v4F1gFy-hqg)

## Notes
