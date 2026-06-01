---
name: lint
description: Scan the whole wiki for orphans, hub candidates, opinion threads, and contradictions, then record findings to log.md. Triggered by /lint, at the end of an ingest batch, or on user request.
---

# Lint

Lint is a **stateless full-state scan** of `wiki/` — it reads the current state
of every page, not a per-batch diff. Running it after several un-linted ingests
catches everything currently present. It is safe to run any time, decoupled from
`/ingest` completion.

## Workflow

1. **Delegate the scan to the `lint-scanner` subagent** (read-only). Spawn it via
   the Agent tool with `subagent_type: lint-scanner`. It reads the whole corpus
   in its own context and returns a compact findings block, so ~85→400 pages of
   page text never floods this session.
2. Take the returned findings and **write them to `log.md`** as a `lint:` entry
   (format below).
3. Surface the findings to the user.
4. **Do NOT auto-apply.** Wait for user approval before creating any
   `wiki/Debates/<Theme>.md` page or doing any restructuring. Hard rule 4 (never
   create folders/taxonomies without approval) applies.

If the subagent under-detects semantic opinion threads (verify against your own
read of a few pages), do the semantic-thread judgment yourself in this context
and keep only the mechanical sweeps (orphans, hub frequency, grep-able
contradictions) delegated.

## What the scan checks

- **Orphans**: pages with no inbound links from other pages or `index.md`.
- **Hub candidates**: terms appearing in 2+ pages without their own page.
- **Opinion threads**: the same opinion claim recurring across 3+ topic pages →
  candidate for `wiki/Debates/<Theme>.md`. Detection is **semantic, not
  lexical**: two opinions arguing the same position from different framings count
  as one thread (e.g. "self-eval is unreliable" and "evaluators need adversarial
  pressure" are the same thread despite no shared words). Ask: would a
  practitioner treat these as the same debate? If yes, count them together.
- **Contradictions**: opposing claims across pages.

Deep lint (cleanup, large restructuring proposals): defer until the wiki has
~100 pages.

## log.md lint entry format

```markdown
## [2026-05-27] lint | post-bootstrap scan
Orphans: none.
Hub candidates: "MCP" mentioned in 4 pages, no page exists. Proposed: create MCP.md.
Opinion threads: none reaching 3 pages.
Contradictions: none.
Awaiting user approval.
```
