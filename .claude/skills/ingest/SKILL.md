---
name: ingest
description: Run a full batch ingest of unprocessed transcripts. Triggered explicitly by /ingest or when the user asks to process the latest transcript batch.
---

# Ingest

Process every unprocessed transcript in `transcripts/`, following the contract in
CLAUDE.md (hard rules apply throughout). Page-format rules live in
`.claude/rules/wiki-page-conventions.md` and load automatically when you touch a
`wiki/` page. Do NOT commit or push between transcripts — keep all changes in the
working tree. Run the lint pass after the batch (see the `lint` skill). At the
very end, make a single commit covering the entire batch + lint, then push once.

## Per-transcript workflow

1. Read the transcript fully.
2. Read `index.md` to know what pages exist.
3. Identify entities worth a page (per **Entity selection** in CLAUDE.md).
4. For each entity:
   - If the page exists: update it. Append to `## Opinions` if there are new opinions, add to `## Sources`, integrate factual additions. Preserve prior content. Apply the contradiction rule (hard rule 3) if needed.
   - If the page doesn't exist: create it per the wiki-page-conventions rule, respecting lazy hub creation.
5. Extract opinion claims and attribute every one. Unattributed claims are rejected.
6. Update `index.md` with new/modified pages.
7. Append an entry to `log.md`.
8. Do NOT commit after each transcript. Continue to the next transcript without committing.

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

## log.md ingest entry format

Append-only. Most recent entries at the bottom. Every entry prefixed with `## [YYYY-MM-DD] <type> | <description>`. Types: `ingest`, `lint`, `update`, `system`, `unprocessable`.

```markdown
## [2026-05-27] ingest | Long-Running Agents — Ash & Andrew (Anthropic, AI Engineer 2026)
Source: https://youtube.com/watch?v=...
Pages added: Generator-Evaluator-Pattern, Context-Rot, Context-Anxiety, Sprint-Decomposition
Pages updated: Claude-Code, Ralph-Loop
17 entities extracted.

## [2026-05-28] unprocessable | <Talk Title>
Auto-subs were unreadable. Skipped.
```

If a transcript yields no extractable entities, log it (`unprocessable`, or an `ingest` entry noting zero entities) rather than forcing a thin page.

## End of batch

1. Run the lint pass over the whole wiki (invoke the `lint` skill).
2. Make ONE commit covering the entire batch:
   ```
   ingest: batch of N transcripts (M pages added, K updated) + lint
   ```
3. ONE push to origin. No commits or pushes at any earlier point in the session.

Done when every transcript has an `ingest` or `unprocessable` entry in `log.md`,
lint findings are recorded, one batch commit exists, and it has been pushed.
