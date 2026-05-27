# Model-Airplane

A simplified reference implementation used to show an autonomous coding agent the correct shape of an integration, without the complexity and token cost of a full production application.

## Concept

Coined by the PostHog Wizard team. A model airplane is a thin simulacrum of a real production app: it has realistic structural shape (login flow, Stripe interface, identity management) but is deliberately hollowed out in ways that don't matter for the integration task. Authentication, for example, accepts any password — the auth is "auth-shaped," not real auth.

The purpose is to show the agent a correct, opinionated implementation pattern without burdening it with the full complexity of an actual production codebase. Advantages:

- **Correct shape**: The agent sees exactly where to place integration code within a realistic code structure
- **Token-efficient**: Much thinner than a production app; can be included in context as a skill file reference
- **Opinionated**: Encodes the team's preferred integration pattern, suppressing the agent's tendency to improvise

## Use at PostHog

PostHog maintains a fleet of model airplanes covering multiple frameworks and languages, each with PostHog already integrated correctly. These are flattened into a single markdown file by a context service and included as a reference in the skill file provided to the agent.

When the agent encounters an auth flow in the user's project, it can compare against the model airplane and determine: "This is a great place to add identity tracking." The pattern recognition is reliable because the agent has seen the canonical version.

## Relationship to adjacent patterns

**[Breadcrumb-Prompting](Breadcrumb-Prompting.md)**: Model airplanes address the "what shape" problem (correct integration structure); Breadcrumb-Prompting addresses the "what order" problem (how to sequence task disclosure). Both are used together in the PostHog Wizard.

**[Model-Rot](Model-Rot.md)**: Model airplanes complement fresh documentation injection. Documentation tells the agent how the API works; the model airplane shows the agent where in the host project to apply it.

## Sources

- Danilo Campos, "LLM Codegen Fails and How to Stop 'Em", AI Engineer 2026 — [https://www.youtube.com/watch?v=juoNbJiZUi0](https://www.youtube.com/watch?v=juoNbJiZUi0)

## Notes
