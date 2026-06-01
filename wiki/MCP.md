# MCP

Model Context Protocol — an open standard for connecting AI agents to external tools and data sources via a structured client-server protocol. Enables tool-calling agents to use any service that exposes an MCP server without custom per-integration code.

## Overview

MCP separates the agent (client) from the tools it uses (server). A service publishes an MCP server once; any MCP-compatible agent can connect to it. This replaced the previous pattern where each developer bundled their own copies of tools into their agent.

Anthropic created the protocol (open-sourced April 2025). The official registry holds thousands of servers. Transport options: local stdio (subprocess on the same machine) and remote HTTP (OAuth 2.1 for authentication).

## Core enterprise challenges

Enterprises face three recurring pain points when deploying MCP at scale (per Karan Sampath, Anthropic):

1. **Observability** — who is using which MCP, how often, which tools are performing poorly. Currently opaque.
2. **Access control** — scoping which users or agent roles can access which servers and tools. Not natively handled by the protocol.
3. **Security** — preventing data exfiltration via prompt injection; managing token scope; ensuring untrusted remote clients cannot reach sensitive internal data.

See [MCP-Gateway](MCP-Gateway.md) for the enterprise architectural response, and [Agent-Registry](Agent-Registry.md) for cataloguing servers, agents, and use cases under governance.

## Context overload problem

Naively exposing a large API via MCP blows out the agent's context window. Matt Carey (Cloudflare) reports that the Cloudflare OpenAPI spec converts to ~1.1 million tokens of tool definitions — more than the context window of any model. GitHub's MCP server grew to 100+ tools before quality degraded noticeably.

The practical constraint: agents given too many tools perform worse, not better. LangChain research (February 2025) confirmed the same pattern: more tools in context increases confusion and hallucination. See [Progressive-Tool-Discovery](Progressive-Tool-Discovery.md) for the mitigation patterns.

## Authentication

MCP remote servers support OAuth 2.1. GitHub MCP added PKCE support for improved security. Dynamic Client Registration (DCR) is specified but rejected by major authorization servers (including GitHub) due to unbounded app database growth and lack of reliable app identity. Cross-App Access (XAA / ID-JAG) is an emerging pattern enabling SSO-based automatic token exchange across MCP servers via enterprise IDPs. See [Cross-App-Access](Cross-App-Access.md).

## GitHub MCP at scale

Sam Morrow (GitHub) reports lessons from operating GitHub's MCP server at ~7 million tool calls/week:

- Reduced from 100+ tools to ~40 defaults via tool sets and grouping; 49% reduction in context load
- Output token reduction: trimming tool responses (e.g., list pull requests) reduced output by 75%+
- Tool success rate: >95% via encoding agent intent into tool surface, batching multi-step operations server-side
- Evals: testing tool descriptions against each other to ensure correct tool is called in context of similar tools, not in isolation
- Security: scope-filtered tool lists based on PAT token scopes; step-up OAuth for on-demand scope elevation

## Progressive discovery and programmatic tool calling

David Soria Parra (Anthropic, April 2026) frames the primary client-side work for MCP as two techniques:

**Progressive discovery**: instead of loading all tool definitions into context at start, give the agent a "tool search" capability and load tools on demand. Claude Code demonstrates this — before the pattern was added, context was dominated by tool definitions; after, a massive reduction in tool context usage. The protocol itself doesn't handle this; it's the client's responsibility to implement demand-loading rather than full preload. See [Progressive-Tool-Discovery](Progressive-Tool-Discovery.md).

**Programmatic tool calling** (also called [Code-Mode](Code-Mode.md)): give the model a REPL/execution environment and have it write code to compose tool calls rather than making sequential JSON round-trips. MCP's structured output feature (specifying the return type of tool calls) enables type-safe composition — the model can chain tool calls knowing the output type of each. Cloudflare's MCP server is cited as an example: instead of exposing individual tools, it provides an execution environment and lets the model orchestrate directly.

Soria Parra's principle: stop doing 1:1 REST-to-MCP conversions ("every time I see someone building another REST-to-MCP conversion tool, it's a bit cringe"). Design for agents, not endpoints.

## MCP roadmap (announced April 2026)

Per David Soria Parra (Anthropic):

- **Stateless transport** (June 2026): a Google-proposed protocol change that makes MCP servers stateless, deployable like standard REST servers on Cloud Run/Kubernetes. Fixes the scaling problems with the current streamable HTTP transport.
- **Cross-app access**: SSO-based automatic token exchange — log in once with your enterprise IDP (Google, Okta) and use MCP servers without per-server logins. See [Cross-App-Access](Cross-App-Access.md).
- **Server discovery via well-known URLs**: agents and crawlers can discover MCP servers by visiting `/.well-known/mcp` (or equivalent) on any website; automatic discovery without a central registry.
- **Skills over MCP**: server authors can bundle skill files directly in their MCP server, shipping updated instructions alongside their tools without relying on external registries.
- **Async task primitive**: improved agent-to-agent communication (experimental version exists, few clients support it; expanding client support is the immediate work). Google's [Gemini-Interactions-API](Gemini-Interactions-API.md) takes a different tack — building server-side state and async execution into the model API itself rather than the protocol.
- **TypeScript SDK v2 and Python SDK v2**: rebuilds based on lessons learned; Python SDK v1 acknowledged to be inferior to fast-mcp from the community.

MCP adoption metric: 110 million monthly downloads as of April 2026; comparable adoption velocity to React (which took roughly twice as long to reach the same volume).

## Full MCP spec: underused capabilities

Most MCP implementations only use Tools. The spec defines four core primitives plus sampling, all of which unlock richer interaction patterns:

**Tools**: actions the server performs. Quality degrades in three ways: too many tools (model confused about which to call), too many domains (different property sets for each tool), too many repetitions (more sequential tool calls = more confusion). Quality over quantity; per-session tool selection helps.

**Dynamic tool discovery**: servers can add/remove tools during a session based on state. A tool for "battle monster" should only appear when there is a monster to battle. Clients that support `listChanged` notifications allow the server to expose context-appropriate tools and remove irrelevant ones.

**Resources**: structured references to files, screenshots, or data. Instead of embedding a giant file in a tool response, return a resource URI that both the LLM and the user can follow up on. Enables screenshots (Playwright → resource → LLM + user), filesystem access, and CI/CD pipeline introspection without bloating tool responses.

**Roots**: workspace context the client sends to the server. VS Code sends the current workspace folder and installed packages as roots, allowing the server to adapt to React vs. Svelte setups without asking "what framework are you using?"

**Sampling**: the server requests an LLM completion from the client, proxied back to the server. The "confusingly named" primitive. Enables tool-level agents to piggyback on the parent agent's LLM — no separate LLM configuration, no separate billing, per-tool. Practical pattern: do inference inside an MCP tool to limit the main agent's context overhead (SQL schemas, specialized instructions) rather than loading all that context into the main agent on every call.

**Elicitations** (upcoming spec draft): tools request direct user input during execution rather than routing through the chat transcript. Enables structured forms and confirmations without a round-trip through the LLM. For full interactive HTML UI embedded in the client, see [MCP-Apps](MCP-Apps.md).

The three tool quality failure modes (LangChain research, 2025):
1. Too many tools in context → model confused about which to call
2. Too many tool domains → inconsistent property sets and instructions confuse the model
3. Too many sequential repetitions → each repeat compounds confusion

MCP over OpenAPI: why the protocol matters beyond plain REST (per Samuel Colvin, Pydantic):
- Dynamic tools that change during execution
- In-flight logging/progress updates before the tool returns
- Sampling (tool-level LLM access without separate configuration)
- stdio subprocess support for local tools

## MCP design principles (practitioner view)

David Cramer (Sentry) built Sentry's MCP server and drew these conclusions:

**MCP is a pluggable architecture for agents, not an API proxy.** You cannot expose your OpenAPI spec 1:1 as MCP tools and get good results. The model will fail — it cannot reason about JSON payloads not designed for it.

**Design for agents:** return Markdown, not raw JSON. If a human can reason about the response, the LLM can too — it pattern-matches on language. Raw JSON works sometimes, but under pressure it breaks. Sentry returns bare-essential bug data as Markdown.

**Design your tool descriptions and errors for agents.** Tool descriptions are context for a model that doesn't know what it needs. Error messages must be human-readable — "you passed an invalid value for X" is better than a machine error code — because the model is reasoning about them abstractly.

**No streaming for tool responses is a real problem.** MCP lacks streaming for tool results, which breaks agent-to-agent use cases where a long-running agent needs to surface output progressively. Sentry worked around this with a polling pattern (start the job → poll for completion) but it's fragile.

**Expose agents via MCP, not just tools.** The real unlock for B2B: wrap your internal agents as MCP-accessible resources. Sentry exposed its root-cause analysis agent (which runs a multi-step LLM pipeline internally) as a single MCP endpoint. The calling agent gets a high-quality result without knowing anything about the internals.

**Cost mindfulness:** returning too much data from a tool call passes token cost to the caller and may not even work (tool description length limits exist in some clients). Return only what's necessary.

## Opinions

- **MCP is a pluggable architecture for agents. Full stop.** It is not a thing that sits on top of OpenAPI. You cannot expose all your endpoints as tools and expect good results — you have to design around how agents actually reason about context. — David Cramer, Sentry ("MCP is Not Good Yet", AI Engineer 2025), [https://www.youtube.com/watch?v=FCi4jT86gSw](https://www.youtube.com/watch?v=FCi4jT86gSw)
- **The inherent value of LLMs is agent architecture, and MCP is how you plug into it.** Agents are just services with a new word on them. The fancy new words are just new words for the same thing. — David Cramer, Sentry ("MCP is Not Good Yet", AI Engineer 2025), [https://www.youtube.com/watch?v=FCi4jT86gSw](https://www.youtube.com/watch?v=FCi4jT86gSw)

- **MCP's genesis was model agency, not just context injection.** The co-creators (David and Justin at Anthropic) were tired of manually copying context from Slack and Sentry into the chat window — they wanted the model to "climb out of its box" and reach into the real world. The original question wasn't "how do we pass more context?" but "how do we give the model agency to act?" — Theodora Chu, Anthropic ("MCP Origins and Requests for Startups", AI Engineer 2025), [https://www.youtube.com/watch?v=x-8pBqWiTzk](https://www.youtube.com/watch?v=x-8pBqWiTzk)

- **Standards succeed when builders can get their hands dirty.** MCP launched at Anthropic's hackweek in November 2024 and went viral internally, but the public launch was initially met with "what's MCP?" — the real turning point was Cursor's adoption, which gave developers a concrete environment to build their own MCPs. Standards need builders who can immediately use them, not announcements. — Theodora Chu, Anthropic ("MCP Origins and Requests for Startups", AI Engineer 2025), [https://www.youtube.com/watch?v=x-8pBqWiTzk](https://www.youtube.com/watch?v=x-8pBqWiTzk)

## Sources

- Matt Carey, "MCP = Mega Context Problem", AI Engineer 2026 — [https://www.youtube.com/watch?v=YBYUvGOuotE](https://www.youtube.com/watch?v=YBYUvGOuotE)
- Sam Morrow, "Scaling GitHub for Your Agents", AI Engineer 2026 — [https://www.youtube.com/watch?v=0n3MKk7r60w](https://www.youtube.com/watch?v=0n3MKk7r60w)
- Karan Sampath, "Gateways are All You Need", AI Engineer 2026 — [https://www.youtube.com/watch?v=CD6R4Wf3jnY](https://www.youtube.com/watch?v=CD6R4Wf3jnY)
- Garrett Galow, "Cross-App Access for MCP", AI Engineer 2026 — [https://www.youtube.com/watch?v=EmhRyw6xeT0](https://www.youtube.com/watch?v=EmhRyw6xeT0)
- David Cramer, "MCP is Not Good Yet", AI Engineer 2025 — [https://www.youtube.com/watch?v=FCi4jT86gSw](https://www.youtube.com/watch?v=FCi4jT86gSw)
- Theodora Chu, Anthropic, "MCP Origins and Requests for Startups", AI Engineer 2025 — [https://www.youtube.com/watch?v=x-8pBqWiTzk](https://www.youtube.com/watch?v=x-8pBqWiTzk)

## Notes
