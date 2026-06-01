# AI Engineer Wiki

A living knowledge base distilled from AI Engineer conference talks, built and maintained with an AI coding agent as the writer (tool-agnostic via [`AGENTS.md`](AGENTS.md) — Claude Code, Codex, Cursor, or Gemini).

## Why I built this

Conference talks are dense with practitioner opinion — things people won't write in blog posts because they're too specific, too controversial, or too tied to their current production situation. But talks are ephemeral: you watch once, maybe take a few notes, and the insight evaporates.

Andrej Karpathy sketched the "LLM Wiki" pattern: feed raw transcripts into an agent, have it extract and accumulate entities into a flat markdown wiki. The key insight is that the wiki *compounds* — each new transcript either creates a new page or enriches an existing one with a new opinion, a new cross-link, a new contradiction. After 60 talks, you have a reference that no single talk could produce.

I wanted this specifically for AI Engineering material. The field moves fast enough that "what practitioners think today" is often more useful than any textbook treatment. The wiki captures exactly that: what real teams are actually doing, what they've burned on, and where they disagree.

The operational contract ([AGENTS.md](AGENTS.md)) enforces that every opinion is attributed to a specific speaker and timestamp, pages are never invented, and the user-authored `## Notes` sections are never touched. The agent writes; I curate.

## Architecture

```
transcripts/          ← raw yt-dlp output (gitignored, local only)
    2026-05-13-hugo-santos-cicd-is-dead.md
    ...

wiki/                 ← the compounding artifact (flat, no subfolders)
    Continuous-Compute.md
    Durable-Agent-Execution.md
    Eval-Flywheel.md
    ...               ← one file per entity

index.md              ← catalog of all pages, grouped by type
log.md                ← append-only event log (ingest, lint, system entries)
DEV_NOTES.md          ← setup gotchas and implementation notes
scripts/
    fetch_transcripts.py   ← yt-dlp wrapper, writes to transcripts/
AGENTS.md             ← operational schema (source of truth, cross-tool)
CLAUDE.md             ← Claude Code bridge; imports AGENTS.md + automation notes
```

**Ingest flow**: fetch transcript → the agent reads it → extracts entities → creates or updates wiki pages → updates index.md and log.md → lint → single commit at end of batch.

## Features

- **Entity-centric pages**: one page per concrete concept, pattern, tool, model, or benchmark — not per talk
- **Attributed opinions**: every practitioner claim includes speaker, affiliation, talk title, event, year, and YouTube timestamp link
- **Cross-linked**: pages reference each other inline; the wiki is a graph, not a list
- **Lint pass**: detects orphans, hub candidates (terms appearing in 2+ pages without their own page), debate threads (same claim across 3+ pages), and contradictions
- **Append-only log**: full audit trail of every ingest session, what was added/updated, and all lint findings

## Setup

### Prerequisites

- Python 3 (`python3` — not `python`)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp): `pip install yt-dlp` (on Ubuntu/WSL with PEP 668, use `pip install yt-dlp --break-system-packages` or `pipx install yt-dlp`)
- An `AGENTS.md`-compatible coding agent (Claude Code, Codex, Cursor, or Gemini). Claude Code additionally runs the `/ingest` and `/lint` automation under `.claude/`.

### Fetch transcripts

```bash
# Fetch the 20 most recent talks from the AI Engineer channel
python3 scripts/fetch_transcripts.py

# Fetch talks uploaded after a specific date
python3 scripts/fetch_transcripts.py --after 20260501 --limit 30
```

Transcripts land in `transcripts/` (gitignored). The script maintains `transcripts/_manifest.json` to skip already-fetched videos on subsequent runs.

### Ingest a batch

Point your agent at the transcript range and ask it to ingest the batch; `AGENTS.md` drives the full workflow. With Claude Code, use `/goal` (it runs the `/ingest` and `/lint` skills end to end).

## Project structure

```
ai-engineer-wiki/
├── AGENTS.md                  # operational schema (source of truth, cross-tool)
├── CLAUDE.md                  # Claude Code bridge (imports AGENTS.md + automation notes)
├── GEMINI.md                  # Gemini bridge (imports AGENTS.md)
├── .cursor/rules/             # Cursor rules (project + wiki-page-conventions glob rule)
├── .claude/                   # Claude Code automation layer (skills, subagent, hook, rule)
├── README.md
├── DEV_NOTES.md               # setup gotchas and implementation notes
├── index.md                   # wiki catalog
├── log.md                     # event log
├── scripts/
│   └── fetch_transcripts.py
├── transcripts/               # gitignored
└── wiki/                      # flat markdown pages
```

## AI agent compatibility

The operational contract follows the [`AGENTS.md`](https://agents.md/) open standard, so the
wiki can be maintained from any AI coding tool:

- **OpenAI Codex, Cursor, Copilot, Windsurf** — read `AGENTS.md` natively.
- **Claude Code** — reads `CLAUDE.md`, which imports `AGENTS.md` and adds the Claude-only automation layer below.
- **Gemini** — reads `GEMINI.md`, which imports `AGENTS.md`.
- **Cursor** — also gets `.cursor/rules/`, including a glob-scoped rule that auto-attaches the page conventions when editing `wiki/*.md`.

`AGENTS.md` is the single source of truth. On top of it, Claude Code runs an automation layer
under `.claude/`: `/ingest` and `/lint` skills, a read-only `lint-scanner` subagent, and a
`PreToolUse` guard hook enforcing the hard rules. Other tools follow the same rules manually —
the rules live in `AGENTS.md`, the automation is a Claude-Code convenience on top.

## Tech stack

- **yt-dlp** — transcript fetching
- **Any AGENTS.md-compatible agent** (Claude Code, Codex, Cursor, Gemini) — ingestion and maintenance
- **Markdown + git** — storage and version history
