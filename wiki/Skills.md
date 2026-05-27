# Skills

A portable context-packaging format for coding agents: a folder containing a `skill.md` file plus optional reference documents and executable scripts, loadable on-demand into agent context.

## Structure

```
my-skill/
├── skill.md          # Required. Front matter + instructions.
└── reference/        # Optional. Additional markdown files and scripts.
    ├── guide.md
    └── setup.sh
```

**`skill.md` front matter** (required fields):
- `name`: identifies the skill
- `description`: tells the agent what the skill does and when to use it

Only the front matter is loaded into context initially — not the full file body. This is the **progressive disclosure** mechanism: the agent reads descriptions and decides which skills to load fully, preventing context bloat from loading all skill content upfront.

When the agent decides a skill is relevant, it calls a load-skill tool (or equivalent mechanism). The full `skill.md` body enters context, along with links to reference files. Reference files can themselves link to other files, forming a skill graph rather than a flat document.

Scripts (bash, python, etc.) can be included and executed by the agent in the local environment. These differ from MCP tools: scripts run on the client machine and are environment-dependent; MCP tools run server-side with no environment dependency.

## MCP vs. skills

| | MCP tools | Skills |
|---|---|---|
| Purpose | Integrations and actions | Context and workflows |
| Loading | All tools loaded at startup | Front matter only, full content on demand |
| Execution | Server-side (remote) | Client-side (local) |
| Best for | API integrations, persistent tools | Org-specific instructions, rich context, workflow guides |

The two are complementary: use MCP for tool integrations; use skills for context that agents need to know and workflows too complex to fit in MCP tool descriptions.

## Eval-driven skill development

Pattern for building production-quality skills (from Supabase's approach):
1. **Define metrics first** — what does "good" look like for this skill? Which tools should the agent call? What outputs are required?
2. **Write the skill** — skill.md, reference files, scripts
3. **Test manually** — run the scenario, observe agent behaviour
4. **Automate with evals** — define input/expected-output/expected-tool-calls tuples; run multiple times; grade with LLM-as-judge or deterministic checks; iterate

See [Context-Lifecycle](Context-Lifecycle.md) for the broader context development lifecycle that this eval-driven pattern fits within. See [Progressive-Tool-Discovery](Progressive-Tool-Discovery.md) and [LiteRT-LM](LiteRT-LM.md) for progressive disclosure applied in different contexts.

## Opinions

- **99.9% of skills in public registries are not production quality.** Registries are useful for learning patterns but almost none pass serious evals. — Patrick Debois, Tessl ("Context Is the New Code", AI Engineer 2026), [https://www.youtube.com/watch?v=bSG9wUYaHWU](https://www.youtube.com/watch?v=bSG9wUYaHWU)

## Sources

- Pedro Rodrigues, "Skill Issue: How We Used AI to Make Agents Actually Good at Supabase", AI Engineer 2026 — [https://www.youtube.com/watch?v=GmAQKINjv1E](https://www.youtube.com/watch?v=GmAQKINjv1E)
- Patrick Debois, "Context Is the New Code", AI Engineer 2026 — [https://www.youtube.com/watch?v=bSG9wUYaHWU](https://www.youtube.com/watch?v=bSG9wUYaHWU)
- Nick Nisi & Zack Proser, "Full Walkthrough: Writing & Using Skills", AI Engineer 2026 — (see transcript 2026-05-06)

## Notes
