# Stop-Hook-Interrogation

A lightweight agent debugging technique in which the agent is queried at the end of each run — via a stop hook — about what would have helped it succeed, surfacing configuration errors, contradictory directives, and missing tools that would otherwise go undetected.

## Mechanism

At the stop hook (end of session), inject a single inference call:

> "What could we have done better to set you up for success in this run?"

The agent reviews its own execution and reports friction points it encountered. This is "user research where the user is the robot."

The technique is cheap (one additional inference call per run) and catches errors that no amount of reading the output would reveal — because the agent often produces plausible-looking output even when running with broken configuration.

## What it catches

PostHog Wizard examples from production:

- **Missing MCP tool**: Agent instructions referenced a tool by name; the MCP server didn't expose it. Hundreds of runs failed silently until interrogation surfaced: "The MCP does not have a tool by this name."
- **Contradictory directives**: Two tool instruction files gave conflicting guidance. The agent flagged: "You're putting me in an impossible spot."
- **Wrong language context**: Agent was receiving JavaScript documentation for a Python project. Output was wrong but looked syntactically plausible.

None of these were visible in the output. Only the agent's own account of its run revealed them.

## Practical application

1. Add a stop hook to your agent configuration
2. At hook fire, send: "What could we have done better to set you up for success in this run?"
3. Log the response alongside each run's output
4. Review when error rates spike or periodically as QA
5. Fix the highest-frequency complaints first

Combine with [Eval-Flywheel](Eval-Flywheel.md) for systematic improvement: interrogation output feeds the failure discovery step.

## Relationship to adjacent patterns

**[Decision-Log](Decision-Log.md)**: Decision-Log captures agent decisions for human review; Stop-Hook-Interrogation captures agent complaints about the environment. Complementary: one audits what the agent did, the other audits what the agent was given to work with.

## Sources

- Danilo Campos, "LLM Codegen Fails and How to Stop 'Em", AI Engineer 2026 — [https://www.youtube.com/watch?v=juoNbJiZUi0](https://www.youtube.com/watch?v=juoNbJiZUi0)

## Notes
