# CLAUDE.md

Operational contract for Claude Code in this repository. Read fully before any action.

## What this project is

A personal knowledge wiki built from AI Engineer conference talks (and other GenAI source material), maintained by the user (Aloysius) with Claude Code as the writer. Based on Andrej Karpathy's LLM Wiki pattern (April 2026).

Three-layer architecture:
- **Raw sources** (`transcripts/`, gitignored): talk transcripts fetched via yt-dlp. Immutable. Read-only.
- **Wiki** (`wiki/`): markdown entity pages written and maintained by you. The compounding artifact.
- **Schema** (this file): operational rules. Co-evolved with the user over time.

## Hard rules (never violate)

1. **Never invent sources or facts.** Every claim comes from a real source. Every opinion gets attributed: speaker + talk + timestamp link.
2. **Never edit content under `## Notes` sections.** Those belong to the user. You write everywhere else; the user writes there.
3. **Never silently overwrite existing pages.** If new content contradicts existing content, append to `## Opinions` and flag with `[CONTRADICTION: <brief>]` for user review.
4. **Never create folders, taxonomies, schemas, or topic-level CLAUDE.md files beyond what's specified here.** If you find yourself wanting to add structure, STOP, log the observation in `log.md`, wait for user instruction.
5. **Never create speaker pages.** Speakers are metadata on sources, not entities.
6. **Never include customer-identifying information** (Daiwa, Dell client names, etc.) in any committed file.
7. **Never fabricate transcript content** if auto-subs are unintelligible. Log as `unprocessable` in `log.md` and skip.

## Folder structure

```
ai-engineer-wiki/
├── CLAUDE.md
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

## Page conventions

**Filename**: `Title-Case-Kebab.md`. Examples: `Generator-Evaluator-Pattern.md`, `Context-Rot.md`, `Heterogeneous-Intelligence.md`.

**Page structure**:

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

**Rules**:
- `## Practical application` is optional. Include only when the source gives concrete steps to apply the concept. Never invent steps not in the source.
- `## Opinions` is omitted entirely if the page has no opinion claims (e.g., a tool definition page).
- `## Sources` is mandatory; list every source that contributed to the page, not just the most recent.
- `## Notes` is mandatory and always present, even when empty. Never edit content under this heading. User entries use `### YYYY-MM-DD (source)` subheadings.

## Entity selection

An entity worth a page is concrete: a concept, pattern, technique, tool, framework, model, benchmark, paper, or company. NOT a vague theme.

Examples of valid entities: `Context-Rot`, `Generator-Evaluator-Pattern`, `vLLM`, `LangGraph`, `BGE-M3`, `MTEB`, `Anthropic`, `Recursive-Language-Models`.

Examples of invalid entities: `Agents`, `Better-RAG`, `AI-Engineering-In-2026`, `Future-Of-LLMs`.

When in doubt, prefer fewer, more concrete entities.

## Lazy hub creation

Create a new page only when:
- (a) The source spends substantial time on the concept (it's a primary topic, not a passing mention), OR
- (b) The concept is already mentioned in 2+ existing pages without a page of its own.

Otherwise, link inline as plain text without creating the page yet. Lint will catch it later.

## Workflows

### Ingest (per transcript)

1. Read the transcript fully.
2. Read `index.md` to know what pages exist.
3. Identify entities worth a page (per Entity Selection above).
4. For each entity:
   - If page exists: update it. Append to `## Opinions` if new opinions, add to `## Sources`, integrate factual additions. Preserve prior content. Apply contradiction rule if needed.
   - If page doesn't exist: create it per Page Conventions, respecting lazy hub creation.
5. Extract opinion claims and attribute every one. Unattributed claims rejected.
6. Update `index.md` with new/modified pages.
7. Append an entry to `log.md`.
8. Commit: `ingest: <talk-title> (N added, M updated)`
9. Push to origin in batches: push after every 5 ingest commits, and once more after the final lint commit. Do not push after every individual commit.

### Lint (after every batch ingest, or on user request)

1. Scan `wiki/` for:
   - **Orphans**: pages with no inbound links from other pages or index.md
   - **Hub candidates**: terms appearing in 2+ pages without their own page
   - **Opinion threads**: same opinion claim recurring across 3+ topic pages → propose `wiki/Debates/<Theme>.md`
   - **Contradictions**: opposing claims across pages
2. Write findings to `log.md` as a `lint:` entry.
3. Do NOT auto-apply. Wait for user approval before creating Debate pages or restructuring.
4. Deep lint (cleanup, restructuring proposals): defer until wiki has ~100 pages.

## Opinions: scaling and structure

Opinions live on the most specific topic page they apply to (topic-first). Lint will propose a `Debates/<Theme>.md` aggregator page only when the same opinion-thread appears across 3+ topic pages. Speaker views are achieved via grep (`grep "— Ash, Anthropic" wiki/`), not via dedicated pages.

The user cares specifically about accumulating opinionated practitioner advice. Bias toward capturing more opinions, not fewer. Every opinion needs full attribution.

## index.md format

Catalog of all pages. Maintain alphabetical order within sections. Sections are descriptive groupings, not folders. **Only include sections that have at least one entry — omit empty sections entirely. No "(none yet)" placeholders.**

```markdown
# Wiki Index

## Concepts
- [Context-Rot](wiki/Context-Rot.md) — Degradation in LLM output quality as context window fills, even below stated limits

## Patterns
- [Generator-Evaluator-Pattern](wiki/Generator-Evaluator-Pattern.md) — GAN-style harness pairing a builder with an adversarial critic
- [Ralph-Loop](wiki/Ralph-Loop.md) — Looping a single prompt through Claude Code until completion criteria are met

## Tools
- [Claude-Code](wiki/Claude-Code.md) — Anthropic's CLI coding agent

## Companies
- [Colossum](wiki/Colossum.md) — UK startup building heterogeneous compute orchestration
```

Section vocabulary: Concepts, Patterns, Tools, Models, Benchmarks, Papers, Companies, Debates.

## log.md format

Append-only. Most recent entries at the bottom. Every entry prefixed with `## [YYYY-MM-DD] <type> | <description>`.

Types: `ingest`, `lint`, `update`, `system`, `unprocessable`.

```markdown
# Wiki Log

## [2026-05-27] ingest | Long-Running Agents — Ash & Andrew (Anthropic, AI Engineer 2026)
Source: https://youtube.com/watch?v=...
Pages added: Generator-Evaluator-Pattern, Context-Rot, Context-Anxiety, Sprint-Decomposition
Pages updated: Claude-Code, Ralph-Loop
17 entities extracted.

## [2026-05-27] lint | post-bootstrap scan
Orphans: none.
Hub candidates: "MCP" mentioned in 4 pages, no page exists. Proposed: create MCP.md.
Awaiting user approval.

## [2026-05-28] unprocessable | <Talk Title>
Auto-subs were unreadable. Skipped.
```

Grep-friendly: `grep "^## \[" log.md | tail -10` gives recent events.

## Commit conventions

Format: `<type>: <description>`

Types:
- `ingest:` — wiki pages added/updated from a new source
- `lint:` — lint findings written to log.md
- `update:` — non-ingest edits to existing pages
- `system:` — changes to CLAUDE.md, scripts, structure
- `init:` — initial scaffolding only

Push to origin after every commit.

## /goal usage for bootstrap

The user will invoke a goal for the initial 20-transcript batch. When given a `/goal`, do not stop early, do not request user input mid-run unless a hard rule is about to be violated, do not deviate from the goal. Process every transcript, ingest per workflow, commit and push as you go, run lint at the end.

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

The user is a production GenAI data scientist (Dell Singapore). Direct, surgical, low tolerance for verbose or hedged responses. When proposing actions:
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