# Contributing

## Why transcripts aren't in this repo

Raw transcripts are gitignored (`transcripts/`) due to content ownership concerns — the source material belongs to AI Engineer and the individual speakers. The wiki pages in `wiki/` are derivative works: distilled, attributed, and transformative.

## Re-deriving the source material

Full provenance is preserved in two places:

- **`log.md`** — every ingest entry records the talk title, speaker, event, and YouTube URL. `grep "^## \[" log.md` lists all sources chronologically.
- **`scripts/fetch_transcripts.py`** — given the YouTube URLs in `log.md`, this script re-fetches auto-subtitles via `yt-dlp` and writes them to `transcripts/`. Run `python3 scripts/fetch_transcripts.py --help` for usage.

Anyone can reconstruct the full transcript corpus from the URLs in `log.md` using the fetch script.

## Schema

The operational rules governing page structure, entity selection, opinion attribution, and commit conventions are in [CLAUDE.md](CLAUDE.md). All wiki edits — whether by Claude Code or a human contributor — must follow that schema.
