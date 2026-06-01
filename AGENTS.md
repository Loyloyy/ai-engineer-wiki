# AGENTS.md

Operational contract for any AI coding agent working in this repository (Codex, Cursor,
Gemini, Claude Code, etc.). Read fully before any action. This is the source of truth;
tool-specific files (`CLAUDE.md`, `GEMINI.md`, `.cursor/rules/`) import or point here.

## What this project is

A personal knowledge wiki built from AI Engineer conference talks (and other GenAI source material), maintained by the user (Aloysius) with an AI agent as the writer. Based on Andrej Karpathy's LLM Wiki pattern (April 2026).

Three-layer architecture:
- **Raw sources** (`transcripts/`, gitignored): talk transcripts fetched via yt-dlp. Immutable. Read-only.
- **Wiki** (`wiki/`): markdown entity pages written and maintained by the agent. The compounding artifact.
- **Schema** (this file): operational rules. Co-evolved with the user over time.

## Hard rules (never violate)

1. **Never invent sources or facts.** Every claim comes from a real source. Every opinion gets attributed: speaker + talk + timestamp link.
2. **Never edit content under `## Notes` sections.** Those belong to the user. The agent writes everywhere else; the user writes there.
3. **Never silently overwrite existing pages.** If new content contradicts existing content, append to `## Opinions` and flag with `[CONTRADICTION: <brief>]` for user review.
4. **Never create folders, taxonomies, schemas, or topic-level instruction files beyond what's specified here.** If you find yourself wanting to add structure, STOP, log the observation in `log.md`, wait for user instruction.
5. **Never create speaker pages.** Speakers are metadata on sources, not entities.
6. **Never include customer-identifying information** in any committed file.
7. **Never fabricate transcript content** if auto-subs are unintelligible. Log as `unprocessable` in `log.md` and skip.

## Folder structure

```
ai-engineer-wiki/
├── AGENTS.md           # this file — source-of-truth operational contract
├── CLAUDE.md           # imports AGENTS.md + Claude-Code-only automation notes
├── GEMINI.md           # imports AGENTS.md
├── .cursor/rules/      # Cursor pointers (project rule + wiki-page-conventions glob rule)
├── README.md
├── CONTRIBUTING.md
├── .gitignore
├── index.md            # catalog of all wiki pages
├── log.md              # chronological event log
├── scripts/
│   └── fetch_transcripts.py
├── transcripts/        # gitignored, local only
│   └── *.md
└── wiki/               # flat, no subfolders
    └── *.md
```

`wiki/` stays flat unless the user explicitly approves subfolder creation. `wiki/Debates/` may be created later by lint after thread detection.

## Entity selection

An entity worth a page is concrete: a concept, pattern, technique, tool, framework, model, benchmark, paper, or company. NOT a vague theme.

Examples of valid entities: `Context-Rot`, `Generator-Evaluator-Pattern`, `vLLM`, `LangGraph`, `BGE-M3`, `MTEB`, `Anthropic`, `Recursive-Language-Models`.

Examples of invalid entities: `Agents`, `Better-RAG`, `AI-Engineering-In-2026`, `Future-Of-LLMs`.

When in doubt, prefer fewer, more concrete entities.

## Wiki page conventions

These apply whenever you create or edit a page under `wiki/`.

### Filename

`Title-Case-Kebab.md`. Examples: `Generator-Evaluator-Pattern.md`, `Context-Rot.md`, `Heterogeneous-Intelligence.md`.

### Page structure

```markdown
# <Entity Name>

<One-sentence definition. Lead with what it IS.>

<Body: as long as the source material warrants. No fixed length. Subheadings allowed. Cross-link other wiki pages inline using [Page-Name](Page-Name.md).>

## Practical application
<Optional. Include only when the source describes concrete steps to apply the concept — a workflow, a checklist, a skill prompt, a decision procedure. Omit if the source is purely descriptive or theoretical. Placed between body and ## Opinions.>

## Opinions
- **<Claim summary>** <Brief context.> — Speaker Name, Affiliation (Talk Title, Event Year), [link with timestamp](https://...)

## Sources
- Speaker Name, "Talk Title", Event Year — [YouTube URL](https://...)

## Notes

### YYYY-MM-DD (source)
<User note. Source is optional, e.g. "desk", "commute". Each entry gets its own H3.>
```

### Section rules

- `## Practical application` is optional. Include only when the source gives concrete steps to apply the concept. Never invent steps not in the source.
- `## Opinions` is omitted entirely if the page has no opinion claims (e.g., a tool definition page).
- `## Sources` is mandatory; list every source that contributed to the page, not just the most recent.
- `## Notes` is mandatory and always present, even when empty. Never edit content under this heading. User entries use `### YYYY-MM-DD (source)` subheadings.

### Opinion placement and attribution

- Opinions live on the **most specific topic page** they apply to (topic-first).
- Attribution format: `- **<Claim summary>** <Brief context.> — Speaker Name, Affiliation (Talk Title, Event Year), [link with timestamp](https://...)`. Unattributed claims are rejected.
- Speaker views are achieved via grep (`grep "— Ash, Anthropic" wiki/`), not via dedicated speaker pages.
- Lint proposes a `Debates/<Theme>.md` aggregator page only when the same opinion-thread (judged semantically, not lexically) appears across 3+ topic pages.

### Lazy hub creation

Create a new page only when:
- (a) the source spends substantial time on the concept (a primary topic, not a passing mention), OR
- (b) the concept is already mentioned in 2+ existing pages without a page of its own.

Otherwise, link inline as plain text without creating the page yet. Lint will catch it later.

## Opinions policy

Bias toward capturing more opinions, not fewer — the user specifically values accumulated practitioner advice. Every opinion needs full attribution (format above).

Debate pages require contested positions, not consensus. Consensus patterns across the corpus (different speakers independently reaching the same conclusion) may become Synthesis pages — a separate page type, TBD at the 100-page mark. Do not create either page type without user approval.

## Workflows

Two procedures drive the project. The detailed, step-by-step versions live in
`.claude/skills/ingest/SKILL.md` and `.claude/skills/lint/SKILL.md` — these are plain
markdown. Claude Code loads them automatically as the `/ingest` and `/lint` slash commands;
**any other agent should read those SKILL.md files directly** when asked to ingest or lint.

- **Ingest**: per-transcript workflow — read transcript → extract entities → create/update wiki pages → update `index.md` and `log.md` → run lint at end of batch → one commit per batch (never mid-session).
- **Lint**: stateless full-state scan for orphans, hub candidates, semantic opinion threads, and contradictions. Records findings to `log.md`. Never auto-applies. Waits for user approval before any Debate page or restructuring. Run after every batch ingest, or on user request.

## Catalog and log

`index.md` is the page catalog; `log.md` is the append-only event log (entries prefixed `## [YYYY-MM-DD] <type> | <description>`; types: `ingest`, `lint`, `update`, `system`, `unprocessable`). The exact formats are documented in the ingest and lint workflow files, where those files are written. `log.md` stays grep-friendly: `grep "^## \[" log.md | tail -10` gives recent events.

## Commit conventions

Format: `<type>: <description>`

Types:
- `ingest:` — end-of-session batch commit covering all transcripts processed + lint in that session
- `update:` — non-ingest edits to existing pages (single commit, push immediately)
- `system:` — changes to instruction files, scripts, structure (single commit, push immediately)
- `init:` — initial scaffolding only

**Batching rule**: during an ingest session, do all work in the working tree without committing. One commit at the end (`ingest: batch of N transcripts (M pages added, K updated) + lint`), then one push. Never commit mid-session.

## Bootstrap / long-running goals

For the initial 20-transcript batch the user will hand the agent a single long-running goal. When given such a goal, do not stop early, do not request user input mid-run unless a hard rule is about to be violated, do not deviate. Process every transcript, ingest per workflow, commit and push as you go (per the batching rule), run lint at the end.

(Claude Code expresses this via `/goal`; other agents should treat a multi-transcript instruction the same way.)

## fetch_transcripts.py requirements

When writing this script, it must:
- Use `yt-dlp` to fetch auto-subtitles from the AI Engineer YouTube channel (https://www.youtube.com/@aiDotEngineer)
- Accept arguments: `--after <YYYYMMDD>` (default 20250101), `--limit <N>` (default 20)
- Filter out: shorts (`duration < 120`), live streams (`is_live`), member-only content
- Sort by upload date ascending, take first N
- Output one markdown file per talk in `transcripts/<YYYY-MM-DD>-<speaker-slug>-<title-slug>.md`
- Each output file has frontmatter: speaker (if detectable from title), event, date, YouTube URL — then raw transcript text below
- Maintain `transcripts/_manifest.json` tracking processed video IDs for incremental runs
- Skip videos already in the manifest

## User working style

The user is a production GenAI data scientist. Direct, surgical, low tolerance for verbose or hedged responses. When proposing actions:
- State the action concisely; no preamble.
- Push back if you disagree with a request, but briefly.
- No excessive caveats or apologies.
- If unsure, ask one clear question rather than guessing or producing low-confidence output.

## Out of scope (Phase 2+)

Mentioned here so they're not forgotten, but explicitly NOT part of the current system:
- Telegram bot for commute note capture (Phase 2)
- Personalized model fine-tuning on wiki content (rejected by user)
- `wiki/` subfolder restructuring (only when search-failure / overwhelm triggers fire)

## When in doubt

Stop. Append an entry to `log.md` describing what you encountered. Wait for user instruction. Cost of pausing is small; cost of wrong autonomous action propagated across pages is high.

## Claude Code automation layer (informational)

This repo ships extra automation under `.claude/` that only Claude Code runs. It does not
change the rules above — it enforces and accelerates them. Other agents follow the same rules
manually.

- `.claude/skills/{ingest,lint}/SKILL.md` — the `/ingest` and `/lint` workflows (readable by any agent).
- `.claude/agents/lint-scanner.md` — a read-only subagent the lint workflow delegates the full-state scan to.
- `.claude/hooks/guard.py` — a pre-edit hook enforcing the hard rules (e.g. blocking edits to `## Notes`).
- `.claude/rules/wiki-page-conventions.md` — auto-loads the page conventions when editing `wiki/*.md`.
- `.claude/settings*.json` — Claude Code permissions/config.
