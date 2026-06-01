---
paths:
  - "wiki/*.md"
  - "wiki/**/*.md"
---

# Wiki page conventions

These apply whenever you create or edit a page under `wiki/`. The operational
contract and the hard rules (including "never edit `## Notes`") are in CLAUDE.md.

## Filename

`Title-Case-Kebab.md`. Examples: `Generator-Evaluator-Pattern.md`, `Context-Rot.md`, `Heterogeneous-Intelligence.md`.

## Page structure

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

## Section rules

- `## Practical application` is optional. Include only when the source gives concrete steps to apply the concept. Never invent steps not in the source.
- `## Opinions` is omitted entirely if the page has no opinion claims (e.g., a tool definition page).
- `## Sources` is mandatory; list every source that contributed to the page, not just the most recent.
- `## Notes` is mandatory and always present, even when empty. Never edit content under this heading. User entries use `### YYYY-MM-DD (source)` subheadings.

## Opinion placement and attribution

- Opinions live on the **most specific topic page** they apply to (topic-first).
- Attribution format: `- **<Claim summary>** <Brief context.> — Speaker Name, Affiliation (Talk Title, Event Year), [link with timestamp](https://...)`. Unattributed claims are rejected.
- Speaker views are achieved via grep (`grep "— Ash, Anthropic" wiki/`), not via dedicated speaker pages.
- Lint proposes a `Debates/<Theme>.md` aggregator page only when the same opinion-thread (judged semantically, not lexically) appears across 3+ topic pages.

## Lazy hub creation

Create a new page only when:
- (a) the source spends substantial time on the concept (a primary topic, not a passing mention), OR
- (b) the concept is already mentioned in 2+ existing pages without a page of its own.

Otherwise, link inline as plain text without creating the page yet. Lint will catch it later.
