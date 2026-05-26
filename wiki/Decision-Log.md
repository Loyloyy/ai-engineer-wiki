# Decision-Log

A pattern in which an agent, upon encountering uncertainty during a long-running task, makes an autonomous decision to unblock itself and immediately records that decision in a structured log for later human review — rather than either interrupting the human or proceeding silently.

## Mechanism

When an agent hits an ambiguous branch point it cannot resolve from available context, it has three broad options: pause and ask the human (elicitation), proceed with a silent assumption, or proceed while logging the assumption. The Decision-Log is the third option. The agent writes an entry describing what it encountered, what decision it made, and what alternative it ruled out. It continues working. The human reviews the log asynchronously and can reverse any logged decision before accepting the final output.

The log entry format is not standardised by the pattern — the key property is that the entry is *discoverable and reversible*: the human can find it without re-reading the full agent trace, and acting on it does not require re-running the entire task.

## Concrete example

Lauritzen describes the contract review case: an agent reviewing dozens of employment contracts encounters a special EU clause it was not briefed on. With elicitation, it would interrupt the human mid-run. With a silent assumption, the human discovers the problem only in the final output. With a Decision-Log, the agent flags: "Encountered non-standard EU termination clause in contract 7. Applied generic template. Human should verify." The agent continues. The human, reviewing the completed tabular output, sees the flag, investigates contract 7, and overrides the decision if needed — without re-running the 30-minute task.

## Contrast with adjacent ideas

**Elicitation** (asking the user) maximises human control but blocks the agent and interrupts the human's context. It is appropriate for high-stakes branches early in a task where proceeding with a wrong assumption would invalidate most downstream work. The Decision-Log is more appropriate mid-task, where the agent has enough momentum that stopping is costly.

**Silent assumption** is the default behaviour of most agents today. The problem is not the assumption itself — agents must make assumptions — it is that silent assumptions are invisible and therefore unauditable. The Decision-Log makes the assumption explicit without the cost of an interruption.

**[High-Bandwidth-Artifacts](High-Bandwidth-Artifacts.md)** provide the interface through which the Decision-Log is typically surfaced. A tabular review or document with inline comments is the right surface for flagged decisions; a chat thread is not.

## Opinions

- **Blocking the agent is often the wrong tradeoff.** If the agent is unsure about something mid-task, the right design is: make a decision, unblock yourself, write it to a Decision-Log. — Jacob Lauritzen, Legora ("Agents need more than a chat", AI Engineer 2026), [https://www.youtube.com/watch?v=XNtkiQJ49Ps](https://www.youtube.com/watch?v=XNtkiQJ49Ps)

## Sources

- Jacob Lauritzen, "Agents need more than a chat", AI Engineer 2026 — [https://www.youtube.com/watch?v=XNtkiQJ49Ps](https://www.youtube.com/watch?v=XNtkiQJ49Ps)

## Notes
