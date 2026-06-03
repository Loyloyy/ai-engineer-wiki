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

**Descriptions are routing rules.** The description field is not for humans — it is what the LLM reads at runtime to decide whether this skill applies to the current task. Write it from the LLM's perspective: "when the user wants to X" or "when working with Y." You can test your description by asking the agent directly: "When would you load this skill? If I only want it to run in condition Z, is this description correct?"

**Location**: skills live in `.claude/skills/<skill-name>/skill.md` within a repo (project-scoped) or in `~/.claude/skills/` (global). The `npx skills` and `npx workos` tools are wrappers that symlink skills into these directories from a remote registry or repository.

When the agent decides a skill is relevant, it calls a load-skill tool (or equivalent mechanism). The full `skill.md` body enters context, along with links to reference files. Reference files can themselves link to other files, forming a skill graph rather than a flat document.

Scripts (bash, python, etc.) can be included and executed by the agent in the local environment. These differ from MCP tools: scripts run on the client machine and are environment-dependent; MCP tools run server-side with no environment dependency.

**Script interpolation** (Claude Code): use `!``<shell command>``` syntax in skill.md to inject deterministic command output directly into context. Example: instead of asking the agent to "get the last 10 git commits," write `!``git log --oneline -10``` and the output is substituted inline before the LLM sees it. This prevents non-determinism (the agent may run the git command differently across sessions) and saves tokens — the agent works from the actual data rather than executing and potentially failing to parse the result.

**Constraints vs. prescriptions**: specifying what the skill must *not* do (constraints) produces better performance than over-prescribing exact steps. Three tight constraints — "never be vague," "always cite line numbers and git references" — outperform a prose-heavy workflow description. A common failure mode is writing the skill like a novel.

**Confidence scoring pattern**: instruct the skill to score its own confidence (e.g., 0–100) on understanding the task before executing, and loop with clarifying questions until a threshold is reached. Forces the agent to surface gaps rather than assuming. Works especially well in planning/ideation skills where the human has not fully specified intent.

**Progressive disclosure within skills**: reference additional markdown files that are only loaded when relevant. Example: a routing rubric for scoring commits loaded only during the scoring phase, not during analysis. This keeps individual runs lean while supporting complex multi-phase workflows.

## The emerging agent architecture stack

Anthropic's Barry Zhang & Mahesh Murali describe skills as the "application layer" above the agent runtime:

- **Model** (processor): Claude, GPT, etc. — massive investment, immense potential, but not useful alone
- **Agent runtime** (operating system): the agent loop + file system — manages context, orchestrates tools
- **Skills** (applications): domain-specific procedural knowledge that make the agent effective in a vertical

The insight: instead of building separate domain-specific agents for each use case, build a universal agent (Claude Code or similar) and equip it with a library of skills. Just as millions of developers have written software encoding domain expertise on top of processors and operating systems, skills open that layer to anyone with a computer.

**MCP + skills architecture**: MCP provides connectivity to the outside world (external data, APIs); skills provide domain expertise and procedural knowledge. An agent equipped with both can enter any vertical without being rebuilt.

**Skills as continuous learning**: Because skills are just folders in the file system, Claude can:
1. Write new skills as it learns patterns about how you work
2. Update existing skills when better approaches are found
3. Drop obsolete skills

"Claude on day 30 of working with you is going to be a lot better than Claude on day one." The standardized format ensures "anything that Claude writes down can be used efficiently by a future version of itself."

## Types of skills

- **Foundational skills**: give the agent new general or domain capabilities it didn't have before (e.g., creating professional office documents, bioinformatics analysis, scientific research workflows)
- **Partner/ecosystem skills**: built by third parties to help Claude work better with specific products (e.g., Browserbase built a skill for browser automation with Stagehand, Notion built workspace research skills)
- **Enterprise skills**: company-specific — org best practices, internal tool workflows, code style guides, the "weird and unique ways" a company uses bespoke software

## MCP vs. skills

| | MCP tools | Skills |
|---|---|---|
| Purpose | Integrations and actions | Context and workflows |
| Loading | All tools loaded at startup | Front matter only, full content on demand |
| Execution | Server-side (remote) | Client-side (local) |
| Best for | API integrations, persistent tools | Org-specific instructions, rich context, workflow guides |

The two are complementary: use MCP for tool integrations; use skills for context that agents need to know and workflows too complex to fit in MCP tool descriptions.

**Skills as agentic tool calls vs. RAG**: loading skills as agent tool calls (on-demand retrieval) outperforms naive RAG (flat chunking + vector search) for documentation-heavy workflows. The agent loads the exact relevant skill rather than retrieving semantically similar but possibly wrong chunks. WorkOS found this on their migration guide skills.

## Eval-driven skill development

Pattern for building production-quality skills (from Supabase's approach):
1. **Define metrics first** — what does "good" look like for this skill? Which tools should the agent call? What outputs are required?
2. **Write the skill** — skill.md, reference files, scripts
3. **Test manually** — run the scenario, observe agent behaviour
4. **Automate with evals** — define input/expected-output/expected-tool-calls tuples; run multiple times; grade with LLM-as-judge or deterministic checks; iterate

See [Context-Lifecycle](Context-Lifecycle.md) for the broader context development lifecycle that this eval-driven pattern fits within. See [Progressive-Tool-Discovery](Progressive-Tool-Discovery.md) and [LiteRT-LM](LiteRT-LM.md) for progressive disclosure applied in different contexts.

## Opinions

- **Code is the universal interface to the digital world; skills package domain expertise for it.** After building Claude Code, Anthropic realized a general-purpose coding agent can handle financial reports, data analysis, document generation — all through code. The bottleneck isn't capability but expertise: "agents are like a brilliant generalist who lacks domain knowledge." Skills solve this by encoding procedural knowledge from domain experts. — Barry Zhang & Mahesh Murali, Anthropic ("Don't Build Agents, Build Skills Instead", AIE Code Summit 2025), [https://www.youtube.com/watch?v=CEvIs9y1uog](https://www.youtube.com/watch?v=CEvIs9y1uog)
- **Stop rebuilding agents, start building skills.** Customization remains important for each domain, but the agent underneath is more universal than expected. Instead of a separate agent per use case, a universal agent + skills library can handle every vertical. — Barry Zhang & Mahesh Murali, Anthropic ("Don't Build Agents, Build Skills Instead", AIE Code Summit 2025), [https://www.youtube.com/watch?v=CEvIs9y1uog](https://www.youtube.com/watch?v=CEvIs9y1uog)
- **99.9% of skills in public registries are not production quality.** Registries are useful for learning patterns but almost none pass serious evals. — Patrick Debois, Tessl ("Context Is the New Code", AI Engineer 2026), [https://www.youtube.com/watch?v=bSG9wUYaHWU](https://www.youtube.com/watch?v=bSG9wUYaHWU)

## Sources

- Pedro Rodrigues, "Skill Issue: How We Used AI to Make Agents Actually Good at Supabase", AI Engineer 2026 — [https://www.youtube.com/watch?v=GmAQKINjv1E](https://www.youtube.com/watch?v=GmAQKINjv1E)
- Patrick Debois, "Context Is the New Code", AI Engineer 2026 — [https://www.youtube.com/watch?v=bSG9wUYaHWU](https://www.youtube.com/watch?v=bSG9wUYaHWU)
- Nick Nisi & Zack Proser, WorkOS, "Full Walkthrough: Writing & Using Skills", AI Engineer 2026 — [https://www.youtube.com/watch?v=pFsfax19yOM](https://www.youtube.com/watch?v=pFsfax19yOM)
- Barry Zhang & Mahesh Murali, Anthropic, "Don't Build Agents, Build Skills Instead", AIE Code Summit 2025 — [https://www.youtube.com/watch?v=CEvIs9y1uog](https://www.youtube.com/watch?v=CEvIs9y1uog)

## Notes
