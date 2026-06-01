# Compressed-Research

Agent pattern that automates the research phase of a three-step business process (business event → research → human decision) without changing the process itself or increasing its risk profile.

## The pattern

Many recurring business processes have this abstract shape:
1. **Business event** (a lead arrives, an abuse report comes in, a contract needs review)
2. **Research phase** (look up the company, check the source, read the relevant policy)
3. **Human decision** (route to sales, take down the content, approve/reject)

The research phase is the target. Replace it with an agent that does the same lookups, checks, and summaries automatically. The business event still triggers the process; a human still makes the final decision. Nothing else changes.

## Why this is low-risk

The process stays unchanged, so there is no new accountability structure to build, no workflow to redesign, and no decision authority to delegate to AI. The risk profile doesn't increase — the human decision point is still there. The only change is that the human arrives at that decision point with a pre-researched brief instead of a blank slate.

If the research was taking 30 minutes per event and it now takes 5 minutes, and the process runs 100,000 times a year, the company saves ~42,000 person-hours per year without touching the decision layer.

## Vercel examples

**Contact-sales routing**: incoming messages to vercel.com/contact hit an agent first. About 75% are classified as support requests and routed to the support team. The remaining 25% trigger enrichment: the agent checks LinkedIn, searches the company, estimates size, and routes to the right sales rep with a brief. What previously took a salesperson 15 minutes per lead now happens before the first human touches it.

**Abuse report triage**: incoming abuse reports go to an agent that checks whether the reported site violates policy, gathers evidence, and summarises the case. A human professional still makes the call; they just no longer have to do the baseline investigation themselves.

## Practical application

1. Identify a recurring business process with a clear research phase between trigger and decision.
2. Define the research steps as a reproducible checklist (what does the researcher look up, in what order, with what output format).
3. Build an agent that executes those steps and returns a structured brief.
4. Insert the agent between the trigger and the existing human decision queue — no other process change.
5. Measure time saved per event; multiply by annual frequency for the business case.

## Opinions

- **The most valuable agents are boring ones that don't change anything except compress time** — enterprises can't change processes quickly; a Compressed-Research agent slots into an existing process without approval chains, budget cycles, or risk reviews, and still delivers millions in annual savings. — Malte Ubl, Vercel (The New Application Layer, AI Engineer 2026), [link](https://www.youtube.com/watch?v=XKup1pj-34M)

- **Every business has at least one process of this shape** — ask people what they hate about their job and you will find a research-before-deciding step that someone does manually a hundred times a week; that is where agent investment should start. — Malte Ubl, Vercel (The New Application Layer, AI Engineer 2026), [link](https://www.youtube.com/watch?v=XKup1pj-34M)

## Sources

- Malte Ubl, "The New Application Layer", AI Engineer 2026 — [YouTube](https://www.youtube.com/watch?v=XKup1pj-34M)

## Notes

