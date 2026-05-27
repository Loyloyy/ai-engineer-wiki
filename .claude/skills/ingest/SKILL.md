---
name: ingest
description: Run a full batch ingest of unprocessed transcripts. Triggered explicitly by /ingest or when the user asks to process the latest transcript batch.
---

Process all unprocessed transcripts in transcripts/. Full ingest workflow per CLAUDE.md. Do NOT commit or push between transcripts — keep all changes in the working tree. Run lint after the batch. At the very end, make a single commit covering the entire batch + lint, then push once. Done when every transcript has either an ingest or unprocessable log.md entry, lint findings are written to log.md, one commit exists for the batch, and it has been pushed to origin.
