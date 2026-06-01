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
6. **Never include customer-identifying information** in any committed file.
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

Page structure, filename rules, the section conventions (`## Practical application` / `## Opinions` / `## Sources` / `## Notes`), opinion attribution format, and lazy hub creation live in `.claude/rules/wiki-page-conventions.md`, which loads automatically whenever you create or edit a page under `wiki/`.

## Entity selection

An entity worth a page is concrete: a concept, pattern, technique, tool, framework, model, benchmark, paper, or company. NOT a vague theme.

Examples of valid entities: `Context-Rot`, `Generator-Evaluator-Pattern`, `vLLM`, `LangGraph`, `BGE-M3`, `MTEB`, `Anthropic`, `Recursive-Language-Models`.

Examples of invalid entities: `Agents`, `Better-RAG`, `AI-Engineering-In-2026`, `Future-Of-LLMs`.

When in doubt, prefer fewer, more concrete entities.

## Workflows

The ingest and lint procedures live in skills that load on demand:

- **Ingest** (`/ingest`, `.claude/skills/ingest/SKILL.md`): per-transcript workflow, `index.md` and `log.md` ingest-entry formats, and end-of-batch commit/push (one commit per batch, never mid-session).
- **Lint** (`/lint`, `.claude/skills/lint/SKILL.md`): stateless full-state scan for orphans, hub candidates, semantic opinion threads, and contradictions, backed by the read-only `lint-scanner` subagent. Records findings to `log.md`; never auto-applies; waits for approval before any Debate page or restructuring. Run after every batch ingest, or on user request.

## Opinions

Bias toward capturing more opinions, not fewer — the user specifically values accumulated practitioner advice. Every opinion needs full attribution. Placement, attribution format, and Debate-thread aggregation are specified in `.claude/rules/wiki-page-conventions.md`.

## Catalog and log

`index.md` is the page catalog; `log.md` is the append-only event log (entries prefixed `## [YYYY-MM-DD] <type> | <description>`; types: `ingest`, `lint`, `update`, `system`, `unprocessable`). The exact formats are documented in the ingest and lint skills, where those files are written. `log.md` stays grep-friendly: `grep "^## \[" log.md | tail -10` gives recent events.

## Commit conventions

Format: `<type>: <description>`

Types:
- `ingest:` — end-of-session batch commit covering all transcripts processed + lint in that session
- `update:` — non-ingest edits to existing pages (single commit, push immediately)
- `system:` — changes to CLAUDE.md, scripts, structure (single commit, push immediately)
- `init:` — initial scaffolding only

**Batching rule**: during an ingest session, do all work in the working tree without committing. One commit at the end (`ingest: batch of N transcripts (M pages added, K updated) + lint`), then one push. Never commit mid-session.

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