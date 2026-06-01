# CLAUDE.md

@AGENTS.md

<!-- AGENTS.md (imported above) is the source-of-truth operational contract. Read it fully.
     The Claude-Code-only mechanics below take priority on any conflict, but they only enforce
     and accelerate the AGENTS.md rules — they do not change them. -->

## Claude Code automation layer

This repo's `.claude/` directory wires the AGENTS.md contract into Claude Code features:

- **Skills** — `/ingest` (`.claude/skills/ingest/SKILL.md`) runs the per-transcript ingest +
  end-of-batch commit/push; `/lint` (`.claude/skills/lint/SKILL.md`) runs the full-state scan.
  These load on demand as slash commands.
- **Subagent** — `/lint` delegates the read-only full-state scan to the `lint-scanner` subagent
  (`.claude/agents/lint-scanner.md`).
- **Hook** — `.claude/hooks/guard.py` is a `PreToolUse` guard enforcing the hard rules (e.g.
  blocking edits under `## Notes`). Its prompts are expected, not glitches.
- **Rule** — `.claude/rules/wiki-page-conventions.md` auto-loads the page conventions whenever you
  create or edit a page under `wiki/`. (Mirrored for Cursor at `.cursor/rules/wiki-page-conventions.mdc`.)
- **Settings** — `.claude/settings.json` / `settings.local.json` hold permissions and config.

## /goal usage for bootstrap

The user invokes `/goal` for the initial 20-transcript batch. This is Claude Code's expression of
the "long-running goals" section in AGENTS.md: do not stop early, do not request input mid-run unless
a hard rule is about to be violated, process every transcript, commit/push per the batching rule, lint at the end.
