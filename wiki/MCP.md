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

See [MCP-Gateway](MCP-Gateway.md) for the enterprise architectural response.

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

## Sources

- Matt Carey, "MCP = Mega Context Problem", AI Engineer 2026 — [https://www.youtube.com/watch?v=YBYUvGOuotE](https://www.youtube.com/watch?v=YBYUvGOuotE)
- Sam Morrow, "Scaling GitHub for Your Agents", AI Engineer 2026 — [https://www.youtube.com/watch?v=0n3MKk7r60w](https://www.youtube.com/watch?v=0n3MKk7r60w)
- Karan Sampath, "Gateways are All You Need", AI Engineer 2026 — [https://www.youtube.com/watch?v=CD6R4Wf3jnY](https://www.youtube.com/watch?v=CD6R4Wf3jnY)
- Garrett Galow, "Cross-App Access for MCP", AI Engineer 2026 — [https://www.youtube.com/watch?v=EmhRyw6xeT0](https://www.youtube.com/watch?v=EmhRyw6xeT0)

## Notes
