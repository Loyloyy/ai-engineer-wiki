# High-Bandwidth-Artifacts

Structured, persistent interfaces — documents, tables, kanban boards, annotated outputs — through which humans and agents collaborate on complex work, as opposed to linear chat.

## The problem with chat

Chat is a one-dimensional interface. A complex agent task is better modelled as a directed acyclic graph (DAG) of sub-tasks: research, review, draft, verify, output. Chat collapses this tree into a single linear thread. The human loses spatial context, cannot easily reference earlier decisions, and must scroll to locate relevant output. Feedback is expressed as follow-up messages rather than annotations on the work itself.

At scale, this becomes unusable. Lauritzen gives the example of a 100-node work tree: you do not want 50 questions arriving sequentially in a chat window, each stripped of the agent's intermediate reasoning. You would not know where each question sits in the overall task, and you could not batch-review decisions efficiently.

Chat is also post-hoc and passive — it surfaces output after the fact, rather than giving the human control points *during* the work.

## Mechanism

A high-bandwidth artifact exposes the work's structure directly. Properties that make an artifact high-bandwidth:

- **Spatial organisation**: related items are grouped and visually adjacent, so review cost scales sub-linearly with task size.
- **Granular addressability**: the human can point at a specific clause, cell, or node — not just the whole output.
- **Inline annotation**: comments, flags, and overrides live beside the work rather than in a separate thread.
- **Agent-human co-tenancy**: agents and humans can act on the same artifact without a handoff step.

## Concrete examples

**Document interface (Legora):** A contract is edited in a document view. The human can highlight clause 3 and leave a comment that only affects clause 3. Agents can be tagged inline. The structure of the document — sections, clauses, definitions — provides natural granularity for both human annotation and agent targeting.

**Tabular review (Legora):** For bulk contract review, the agent produces a table: one row per contract, columns for each review criterion, cells flagged where judgment is required. The human scans the table, resolves flagged cells, and releases the remainder for continued agent processing. Review time scales with the number of flags, not the number of contracts.

Both examples give the human high *control* (easy to instil judgment at a specific point) and high *trust* (easy to audit what the agent actually did across the full task).

## Contrast with adjacent ideas

**Chat-as-input** is not being rejected. Natural language input remains valuable for its flexibility. The critique is of chat as the *primary collaboration surface* for complex, long-running work. Input and collaboration surface are separable.

**Agent traces / logs** are a related concept but oriented toward debugging rather than collaboration. A Decision-Log surfaces specific decision points; a trace surfaces everything. High-bandwidth artifacts are designed for human participation, not just inspection.

**[Decision-Log](Decision-Log.md)** is one artefact type that fits this pattern — it surfaces the agent's autonomous decisions in a reviewable, reversible form.

## Opinions

- **Chat is the wrong primary interface for complex agent collaboration.** It is a low-bandwidth, one-dimensional medium trying to represent work that is naturally two-dimensional or graph-structured. Agents aren't humans — we should not constrain them to human language as the primary collaboration medium. — Jacob Lauritzen, Legora ("Agents need more than a chat", AI Engineer 2026), [https://www.youtube.com/watch?v=XNtkiQJ49Ps](https://www.youtube.com/watch?v=XNtkiQJ49Ps)

- **Chat has concurrency of one: every background-agent future runs through document interfaces, not chat.** Chat forces sequential interaction — you can only have one "conversation" at a time. Documents with triggers (cron, Gmail event, Slack message) allow ambient agents to run in the background and surface only issues needing approval. The human's job becomes reviewing and approving results, not driving the conversation. — Filip Kozera, Wordware ("Beyond Conversation: Why Documents Transform Natural Language", AI Engineer 2025), [https://www.youtube.com/watch?v=2Jom-4Brg6Q](https://www.youtube.com/watch?v=2Jom-4Brg6Q)

- **Proactive AI systems outperform chat interfaces by an order of magnitude in engagement.** A system that pushes daily digests and insights ("here's what you need to know today") generated 20 points higher NPS and order-of-magnitude higher engagement than the same AI in chat format. The best interface is the one you never need to use — AI should anticipate next steps, not wait for queries. — Jan Siml ("Stop Ordering AI Takeout: A Cookbook for Winning When You Build In-House", AI Engineer 2025), [https://www.youtube.com/watch?v=DjUIecgpYAo](https://www.youtube.com/watch?v=DjUIecgpYAo)

## Sources

- Jacob Lauritzen, "Agents need more than a chat", AI Engineer 2026 — [https://www.youtube.com/watch?v=XNtkiQJ49Ps](https://www.youtube.com/watch?v=XNtkiQJ49Ps)
- Jan Siml, "Stop Ordering AI Takeout: A Cookbook for Winning When You Build In-House", AI Engineer 2025 — [https://www.youtube.com/watch?v=DjUIecgpYAo](https://www.youtube.com/watch?v=DjUIecgpYAo)
- Filip Kozera, Wordware, "Beyond Conversation: Why Documents Transform Natural Language", AI Engineer 2025 — [https://www.youtube.com/watch?v=2Jom-4Brg6Q](https://www.youtube.com/watch?v=2Jom-4Brg6Q)

## Notes
