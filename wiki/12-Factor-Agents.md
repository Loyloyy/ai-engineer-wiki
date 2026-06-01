# 12-Factor-Agents

A framework of twelve engineering principles for building reliable AI agents, analogous to the Twelve-Factor App for cloud-native software. The core thesis: agents are software; apply software engineering discipline, not AI magic.

Created by Dex Horthy (HumanLayer) from interviews with 100+ founders and engineers. The GitHub repo reached 4,000 stars in about two months and was on the front page of Hacker News all day.

## The problem

Agents built on frameworks hit ~70–80% quality quickly — enough to excite stakeholders — but breaking past that ceiling requires understanding the inner workings. When you're seven layers deep in a call stack trying to understand how a prompt gets built, you've lost control. The 12 factors are a checklist for reclaiming that control.

## Selected factors (from the talk)

### Factor 1 — Structured output / JSON is the magic

The most powerful thing an LLM can do is turn a sentence into structured JSON. Not loops, not tools, not agents — just that. Everything else is built on top. If your only use of an LLM is "sentence in, JSON out," that alone is worth integrating.

### Factor 2 — Own your prompts

To get past the 70–80% quality bar, you will eventually write every token by hand. LLMs are pure functions: tokens in, tokens out. Everything in making an agent reliable is context engineering — the prompt, the memory, the RAG, the history. All of it is: what tokens go into the model? You need to be able to try everything, test knobs, and evaluate results. Frameworks that generate prompts for you prevent this.

### Factor 4 — Tool use is just JSON and code

"Tool use" is demystified as: LLM outputs JSON → JSON is passed to a switch statement → deterministic code runs → result optionally fed back. There is nothing ethereal or magical about it. Calling it "tool use" implies an abstraction that often leads engineers to delegate control to frameworks unnecessarily. It is JSON and a function call.

### Factor 8 — Own your control flow

Don't let a framework manage the agent loop. Own:
- The prompt that selects the next step
- The switch statement that handles the model's JSON output
- How context is accumulated
- When and how the loop exits (done, error, human escalation, summarize and continue)
- Pause and resume: serialize the context window to a database when calling a long-running tool; reload it when the tool returns. The agent doesn't know time passed.

Owning the loop means you can do things no framework will support for your use case: custom summarization, conditional branching, LLM-as-judge mid-loop, mid-loop human escalation.

## Micro-agents over monolithic agents

Long single-agent loops with large context windows fail. What works in production: **micro-agents** — agent loops of 3–10 steps embedded in a mostly deterministic DAG. The surrounding pipeline is standard software; the LLM handles only the ambiguous step where natural language input must be resolved to a structured decision.

HumanLayer's deployment bot: CI/CD runs deterministically until the GitHub PR is merged and tests pass → a micro-agent decides deploy order → human approves via Slack → agent confirms order and hands back to deterministic code → end-to-end tests run deterministically. The agent's job is a 3-step loop.

## Stateless reducers

Agents should be stateless. All state lives outside the agent — in your database, your event queue, your context window builder. The agent is a reducer: `f(context) → (action, next_context)`. You own the state; you own what gets accumulated.

## Contacting humans with tools

Most agent frameworks conflate "done" with "no more tool calls." A better pattern: the first token the model generates disambiguates the intent (done / needs clarification / needs human escalation / needs manager). This pushes intent to a natural-language token the model reasons about reliably, and enables out-of-loop agents (long-running agents that contact humans via email, Slack, Discord, SMS) without polling.

## Framework vs. library philosophy

Horthy frames the 12 factors as a wish list for frameworks rather than an anti-framework manifesto: frameworks should take away the *other* hard parts (infra, observability, boilerplate) so that engineers can focus on the *AI* hard parts — prompts, flow, context engineering.

The companion project `create-12-factor-agent` is scaffolded code you own entirely (shadcn-style), not a wrapper framework you're locked into.

## Opinions

- **Agents are software. LLMs are stateless functions. Own your control flow.** Most production agents aren't "agentic" at all — they're software with LLM-powered steps. Stop treating them as a special category. — Dex Horthy, HumanLayer ("12 Factor Agents — Patterns of Reliable LLM Applications", AI Engineer 2025), [https://www.youtube.com/watch?v=8kMaTybvDUw](https://www.youtube.com/watch?v=8kMaTybvDUw)
- **Frameworks take away the wrong hard parts.** The AI hard parts — prompts, flow, context — are what you need control over. Frameworks that abstract those away are working against you. Tools should take away the non-AI hard parts: infrastructure, auth, boilerplate. — Dex Horthy, HumanLayer ("12 Factor Agents — Patterns of Reliable LLM Applications", AI Engineer 2025), [https://www.youtube.com/watch?v=8kMaTybvDUw](https://www.youtube.com/watch?v=8kMaTybvDUw)
- **The "bleeding edge" is engineering reliability into the thing the model can't do reliably yet.** Find the boundary of what the model can do reliably, engineer reliability into your system so it gets it right anyway, and you will have created something magical and better than what everyone else is building. — Dex Horthy, quoting NotebookLM builder, HumanLayer ("12 Factor Agents", AI Engineer 2025), [https://www.youtube.com/watch?v=8kMaTybvDUw](https://www.youtube.com/watch?v=8kMaTybvDUw)

## Sources

- Dex Horthy, "12 Factor Agents — Patterns of Reliable LLM Applications", AI Engineer 2025 — [https://www.youtube.com/watch?v=8kMaTybvDUw](https://www.youtube.com/watch?v=8kMaTybvDUw)

## Notes
