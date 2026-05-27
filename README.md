# AI Engineer Wiki

A living knowledge base distilled from AI Engineer conference talks, built and maintained with Claude Code as the writer.

## Why I built this

Conference talks are dense with practitioner opinion — things people won't write in blog posts because they're too specific, too controversial, or too tied to their current production situation. But talks are ephemeral: you watch once, maybe take a few notes, and the insight evaporates.

Andrej Karpathy published a note in April 2026 sketching the "LLM Wiki" pattern: feed raw transcripts into an agent, have it extract and accumulate entities into a flat markdown wiki. The key insight is that the wiki *compounds* — each new transcript either creates a new page or enriches an existing one with a new opinion, a new cross-link, a new contradiction. After 60 talks, you have a reference that no single talk could produce.

I wanted this specifically for AI Engineering material. The field moves fast enough that "what practitioners think today" is often more useful than any textbook treatment. The wiki captures exactly that: what real teams are actually doing, what they've burned on, and where they disagree.

The operational contract ([CLAUDE.md](CLAUDE.md)) enforces that every opinion is attributed to a specific speaker and timestamp, pages are never invented, and the user-authored `## Notes` sections are never touched. Claude Code writes; I curate.

## Architecture

```
transcripts/          ← raw yt-dlp output (gitignored, local only)
    2026-05-13-hugo-santos-cicd-is-dead.md
    ...

wiki/                 ← the compounding artifact
    Continuous-Compute.md
    Durable-Agent-Execution.md
    Eval-Flywheel.md
    ...               ← one file per entity, flat (no subfolders)

index.md              ← catalog of all pages, grouped by type
log.md                ← append-only event log (ingest, lint, system entries)
scripts/
    fetch_transcripts.py   ← yt-dlp wrapper, writes to transcripts/
CLAUDE.md             ← operational schema; Claude Code reads this first
```

**Ingest flow**: fetch transcript → Claude Code reads it → extracts entities → creates or updates wiki pages → updates index.md and log.md → lint → single commit at end of batch.

## Features

- **Entity-centric pages**: one page per concrete concept, pattern, tool, model, or benchmark — not per talk
- **Attributed opinions**: every practitioner claim includes speaker, affiliation, talk title, event, year, and YouTube timestamp link
- **Cross-linked**: pages reference each other inline; the wiki is a graph, not a list
- **Lint pass**: detects orphans, hub candidates (terms appearing in 2+ pages without their own page), debate threads (same claim across 3+ pages), and contradictions
- **Append-only log**: full audit trail of every ingest session, what was added/updated, and all lint findings

## Setup

### Prerequisites

- Python 3 (`python3` — not `python`)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp): `pip install yt-dlp`
- Claude Code CLI

### Fetch transcripts

```bash
# Fetch the 20 most recent talks from the AI Engineer channel
python3 scripts/fetch_transcripts.py

# Fetch talks uploaded after a specific date
python3 scripts/fetch_transcripts.py --after 20260501 --limit 30
```

Transcripts land in `transcripts/` (gitignored). The script maintains `transcripts/_manifest.json` to skip already-fetched videos on subsequent runs.

### Ingest a batch

```
/ingest
```

Or give Claude Code a `/goal` specifying the transcript range. CLAUDE.md drives the full workflow.

## Project structure

```
ai-engineer-wiki/
├── CLAUDE.md                  # operational schema
├── README.md
├── DEV_NOTES.md               # setup gotchas and implementation notes
├── index.md                   # wiki catalog
├── log.md                     # event log
├── scripts/
│   └── fetch_transcripts.py
├── transcripts/               # gitignored
└── wiki/                      # flat markdown pages
```

## Tech stack

- **yt-dlp** — transcript fetching
- **Claude Code** — ingestion and maintenance agent
- **Markdown + git** — storage and version history
