# MCP-Gateway

An enterprise architectural layer positioned between [MCP](MCP.md) clients and MCP servers that handles authentication, access control, observability, routing, and credential management centrally — allowing individual server teams to focus on business logic rather than security infrastructure.

## The enterprise problem

Enterprises face three interlocking problems when deploying MCP at scale: observability (who uses which tools, how often, what's failing), access control (which users or roles can access which servers), and security (preventing data exfiltration, managing token scope, securing internal data from untrusted remote clients). These are "table stakes" for enterprise deployments but are not solved by the MCP protocol itself.

Without a gateway, every new MCP server must independently solve all three problems. The result: developers produce servers that security teams cannot approve, servers sit undeployed, and the enterprise fails to realize the benefits of MCP.

## What a gateway provides

A gateway is a middleman between any MCP client and the full internal MCP server fleet. All clients connect only to the gateway; the gateway routes to individual servers. Individual servers treat the gateway as their only trusted endpoint.

Components a gateway typically includes:
- **Auth**: OAuth integration with an enterprise IDP; delegated identity for both users and agents
- **Access control**: role-based tool scoping; per-team, per-user, per-agent permission policies
- **Proxy/routing**: single endpoint for all clients; gateway routes to the correct internal server
- **Tunnel**: secure connection between the untrusted external client and internal servers
- **Sub-registry**: catalog of all internal MCP servers, with tool definitions and metadata
- **CLI**: agent-friendly tooling to register a new server; should be usable by a coding agent without human intervention

## Key benefits

**Any new MCP server skips security boilerplate entirely.** A legal team building a contract review server handles only the contract review logic. Auth, access control, and observability are already solved by the gateway.

**Surface invariance**: once the gateway exists, new agent clients (Claude.ai, Claude Code, internal tools) automatically get access to all servers without per-client configuration. The enterprise is not locked into any specific client surface.

**Root of trust**: the security team blesses one platform (the gateway) rather than evaluating every individual MCP server. All servers inherit the gateway's security posture.

**Delegated identity for agents**: as agent identity becomes more important, gateways can define novel agent identity primitives (distinct from user identity) and scope them to specific servers and tools.

## Practical application

Sampath's recommendation: make a one-time investment in the gateway before deploying MCP broadly. Even a minimal gateway (auth + routing + sub-registry) unlocks decentralized MCP development while keeping security teams in control. The investment does not require heavy ongoing maintenance; agents themselves can largely handle server registration via the gateway's CLI.

Anthropic uses this pattern internally for its own MCP deployments.

## Contrast with adjacent ideas

**[MCP](MCP.md)** defines the protocol; a gateway is an architectural deployment pattern on top of it. The protocol does not specify gateway implementations.

**[Cross-App-Access](Cross-App-Access.md)** solves the specific problem of MCP client ↔ server OAuth handshakes via enterprise IDP federation. A gateway and XAA are complementary: the gateway handles internal routing and control; XAA handles the external OAuth flow that clients use to connect.

**[Progressive-Tool-Discovery](Progressive-Tool-Discovery.md)** addresses the context-size problem of too many tools. A gateway addresses the security and governance problem of too many uncontrolled servers. Both are needed at enterprise scale.

## Opinions

- **The protocol allows for enterprise needs; the community just hasn't built for them yet.** MCP was designed to be enterprise-ready. The gap between protocol capability and deployed enterprise reality is a build problem, not a design problem. — Karan Sampath, Anthropic ("Gateways are All You Need", AI Engineer 2026), [https://www.youtube.com/watch?v=CD6R4Wf3jnY](https://www.youtube.com/watch?v=CD6R4Wf3jnY)
- **Bless one platform.** The single most important thing an enterprise can do for MCP adoption is establish one trusted gateway. Everything else flows from that decision. — Karan Sampath, Anthropic ("Gateways are All You Need", AI Engineer 2026), [https://www.youtube.com/watch?v=CD6R4Wf3jnY](https://www.youtube.com/watch?v=CD6R4Wf3jnY)

## Sources

- Karan Sampath, "Gateways are All You Need", AI Engineer 2026 — [https://www.youtube.com/watch?v=CD6R4Wf3jnY](https://www.youtube.com/watch?v=CD6R4Wf3jnY)

## Notes
