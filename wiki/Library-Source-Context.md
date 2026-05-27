# Library Source Context

A technique for giving coding agents reliable access to third-party library patterns by adding the library's source repository as a git subtree — making it appear as first-party code rather than a dependency.

## The problem

Coding agents are trained to focus on the codebase they're working in, not on dependencies. This means:

- **node_modules**: agents are trained to not prioritize code in dependency directories; it's treated as read-only infrastructure, not a source of patterns to learn from.
- **gitignored files**: IDEs like Cursor don't index gitignored files. Agents also tend to deprioritize them.
- **MCP documentation servers**: agents haven't been trained on reading documentation via MCP; they've been trained primarily to consume and produce code. A model given an MCP server pointing to docs behaves less reliably than one that can read source files.

The result: when using a library the model wasn't trained on (a new version, a niche library, an internal framework), none of the standard options give the model the pattern familiarity needed to produce idiomatic code.

## The solution: git subtree

Add the library's source repository as a git subtree (squashed, without history) into a non-gitignored directory such as `.repos/<library-name>/`. The agent now treats the library code as part of the same codebase — it reads it, extracts patterns from it, and replicates those patterns when generating new code.

```bash
git subtree add --prefix=.repos/some-lib \
  https://github.com/org/some-lib main --squash
```

The agent is told in `CLAUDE.md` or `agents.md` that the reference library lives at `.repos/some-lib/` and should be consulted for patterns and best practices.

## Pattern extraction workflow

Once the library source is accessible, the workflow is:
1. Ask the agent to explore the library repo and extract patterns for the feature you want to build.
2. Have the agent save those patterns as markdown files (e.g., `patterns/http-api.md`, `patterns/sql.md`, `patterns/testing.md`).
3. Reference those files in `CLAUDE.md` or `agents.md` so future sessions inherit the library knowledge.
4. Implement features by asking the agent to follow the patterns files — not by asking it to re-explore the library each time.

This approach lets you selectively pick patterns (e.g., use the HTTP module but not the workflow module) without forcing the agent to use the entire library.

## ESLint back pressure

When agents repeatedly produce anti-patterns — unsafe type casts, plain strings where branded types are needed, raw SQL instead of validated schemas — the solution is custom ESLint rules that reject those patterns at lint time:

- Ban `as X` type assertions; require schema-based validation constructors instead.
- Ban `unknown` and explicit type parameters on SQL templates; require SQL schema.
- Require branded types for all identifiers to prevent cross-type assignment.

Each rule in the lint file originated from a bad pattern the model produced. The lint failure becomes the back-pressure signal: the agent can't ship code that violates the rules, so it eventually learns (within a session) to avoid those patterns. This is more reliable than instructions alone because it's verifiable — the model can't claim to have followed instructions when the linter disagrees.

## Opinions

- **Clone the repo is the only reliably working approach.** Documentation MCP servers, node_modules inspection, and gitignored directories all fail for different reasons. Adding library source as a git subtree makes it discoverable to the agent on the same terms as first-party code. — Michael Arnaldi, Effectful ("Vibe Engineering: Effect Apps", AI Engineer 2026), [https://www.youtube.com/watch?v=Wmp2Tku2PrI](https://www.youtube.com/watch?v=Wmp2Tku2PrI)
- **Lint rules codify every mistake the model makes.** Whenever the model takes a shortcut (deleting tests, using type casts, bypassing validation), write a lint rule that prohibits that pattern. The rules file becomes a persistent institutional memory of what not to do. — Michael Arnaldi, Effectful ("Vibe Engineering: Effect Apps", AI Engineer 2026), [https://www.youtube.com/watch?v=Wmp2Tku2PrI](https://www.youtube.com/watch?v=Wmp2Tku2PrI)
- **With AI, less is more. Fewer tools and dumber loops outperform sophisticated architectures.** A simple bash script looping with "pick the next small task, implement it, exit" beats complex context management pipelines. — Michael Arnaldi, Effectful ("Vibe Engineering: Effect Apps", AI Engineer 2026), [https://www.youtube.com/watch?v=Wmp2Tku2PrI](https://www.youtube.com/watch?v=Wmp2Tku2PrI)

## Sources

- Michael Arnaldi, Effectful, "Vibe Engineering: Effect Apps", AI Engineer 2026 — [https://www.youtube.com/watch?v=Wmp2Tku2PrI](https://www.youtube.com/watch?v=Wmp2Tku2PrI)

## Notes
