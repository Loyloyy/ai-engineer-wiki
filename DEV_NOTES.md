# Dev Notes

Setup gotchas and implementation notes.

## fetch_transcripts.py — yt-dlp channel metadata quirks

### `--flat-playlist` does not populate `upload_date`

- **Symptom**: Script found 0 eligible videos despite the channel having hundreds.
- **Cause**: `--flat-playlist` returns lightweight playlist entries where `upload_date` and `timestamp` are `null`. The Python-side date filter then dropped everything.
- **Fix**: Removed `--flat-playlist`. Full metadata fetch (`--dump-json` without flat mode) populates `upload_date` correctly.

### Channel URL must include `/videos`

- **Symptom**: Same 0-result issue on the bare `@aiDotEngineer` handle.
- **Fix**: Use `https://www.youtube.com/@aiDotEngineer/videos`. The `/videos` tab is sorted newest-first and is the correct playlist endpoint for scripted access.

### `--break-on-reject` exits with code 1 — that's expected

- The channel is sorted newest-first. Combined with `--dateafter`, yt-dlp rejects videos once it falls below the date threshold and exits with code 1.
- The script treats exit codes 0 and 1 as both acceptable (only fails if stdout is also empty).

## Python invocation

Use `python3`, not `python` — `python` is not in PATH on this WSL environment.

## Entity filtering — what earns a page

After two batches (T1–T60), the pattern for which talks produce pages vs. zero entities:

**Produces pages**: talks where the speaker describes a mechanism with a name — a pattern they use, a framework they built, a concept with engineering consequences. The entity is extractable even if the speaker doesn't name it explicitly.

**Zero entities (log as such, don't force a page)**:
- Product demo or pitch talks without underlying engineering explanation
- Research talks presenting ML results (training curves, benchmarks) without a deployable technique
- Panel discussions where claims are too hedged or too short to attribute
- Talks where the core insight is already covered by an existing page (add an opinion, don't create a thin duplicate)

The discipline here matters: thin pages dilute the wiki. It's better to add 2 opinions to an existing page than to create a 3-sentence stub.

## Batching and commit discipline

**One commit per session, not per transcript.** All ingest work stays in the working tree until lint is done, then a single commit:

```
ingest: T48–T60 batch (6 added, 1 updated)
```

Then one push. This was changed from per-transcript commits after the first batch because mid-session commits created noisy history and didn't reflect the actual unit of work (a curated batch, not a single talk).

**Why this matters**: a partial batch committed mid-session leaves index.md and log.md in an intermediate state. The single-commit model ensures the repo is always internally consistent.

## Edit tool transient ENOENT on index.md

During batch T48–T60, the `Edit` tool returned ENOENT on `index.md` despite the file existing. Workaround: use `Write` to rewrite the full file. This appears to be a transient tool issue, not a file-system problem — subsequent sessions have not reproduced it.

## Context compaction and long ingest sessions

Claude Code compacts context when the conversation grows long. The compaction summary is accurate for entity lists and log entries, but exact wording of opinions and opinions-section formatting may be slightly paraphrased. Always re-read the relevant wiki pages before appending new opinions to existing pages within the same session (after compaction).

The `## Notes` sections are user-owned and must never be touched — this is the most compaction-sensitive rule, since a compacted summary might lose the distinction between user-written and agent-written sections. **If CLAUDE.md hard rules feel uncertain after compaction, re-read CLAUDE.md before continuing. Hard rules being lost is the highest-cost failure mode.**

## Channel exhaustion

At some point `fetch_transcripts.py --limit 30` will return fewer than 30 results. That's not a bug — it's the natural end state of the AI Engineer channel as the primary source. When fetch returns significantly fewer than `--limit`, options are:

- Lower the `--after` date floor to backfill older content
- Add a new channel (e.g. Latent Space podcast, other conference recordings)
- Switch to a different source class (papers, blog posts, podcast transcripts)

The wiki's ingest machinery is source-agnostic — any transcript-style text file in `transcripts/` with the right frontmatter works. The schema doesn't need to change, only the fetch script.

## Transcript quality signals

Auto-subtitles vary significantly in quality. Signals that a transcript will be hard to process:

- Speaker names rendered as "unknown" in the frontmatter (yt-dlp couldn't parse them)
- Heavy use of `[music]` and `[applause]` tags with little text in between
- Frequent `>>` speaker-change markers with very short utterances (panel discussion format)
- Unintelligible technical terms rendered as phonetic approximations

When quality is low enough that extracting accurate claims would require guessing, log as `unprocessable` and skip rather than risk fabricating content.
