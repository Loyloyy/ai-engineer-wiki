# Agent-Identity

Authentication and authorization framework for agents acting on behalf of users — distinct from human identity (requires headless login, long-lived sessions) and machine-to-machine identity (requires user-context linkage and dynamic scope).

## Why agent identity is different

**Not human identity**: agents can't type into a browser. Sessions must persist without expiration-on-inactivity. Credentials must be refreshed programmatically.

**Not machine-to-machine**: M2M (certificate-based auth) is services talking to each other with no user context. Agents act *on behalf of* specific users and must carry that identity through tool calls for auditability and compliance.

**The hybrid challenge**: agents need broad access to be useful (access to Jira, Salesforce, Slack, email) but also least-privilege scoping to be safe. These requirements pull in opposite directions. OAuth's static scope model doesn't accommodate agents that discover they need new capabilities mid-task. Permissions need to be dynamic.

**The core failure mode**: running agents as service accounts (shared static API key in an environment variable). This breaks auditability (can't tell who did what), makes key rotation risky, and grants access that's too broad. The fix: token exchange — agent requests a short-lived token minted for one user and one API from a backend, uses it, discards it.

## Four patterns for agent identity

Per Michael Grinich (WorkOS):

**1. Persona shadowing**: agent gets a scoped shadow identity derived from a user. Think "Michael-agent-1" where the agent has a subset of the real Michael's permissions. Still tied to original human identity for compliance. Most common pattern in enterprise deployments today.

**2. Delegation chains**: JWT-style token passing where each link carries the original user's authorization forward. Cryptographically verifiable, stateless. Similar to OAuth token flows but explicitly chained through multi-hop agent orchestration.

**3. Capability tokens**: time-bound, action-scoped vouchers. "Agent X can read Bob's calendar for the next 60 minutes." Token expires or is single-use. Related to Google's Macaroons concept. Hardest to game because the token's capability is defined at mint time.

**4. Escalation to humans**: every sensitive action requires explicit approval. Theoretically secure but leads to consent fatigue (users click approve on everything), defeating the security purpose. Useful as a fallback rather than primary mechanism.

The practical approach: combine all four depending on action sensitivity and compliance requirements.

## CIBA: async consent without browser

CIBA (Client Initiated Backchannel Authentication, part of OIDC spec) enables consent flows for agents running headlessly or in background tasks:

1. Agent triggers a sensitive action
2. Agent sends a CIBA request to the authorization server
3. Server sends a push notification to the user's trusted device
4. User approves or denies from their phone — no browser redirect required
5. Agent receives token only after approval

The notification tells the user specifically what action was approved ("this agent tried to buy 10 shares of X — approve?"), not a generic consent screen. Once a user has approved a session, subsequent actions route through CIBA only for high-risk operations. This avoids consent fatigue while maintaining per-action control over sensitive operations.

## RAG authorization: enforce at retrieval, not at inference

When agents use [RAG](RAG.md), not every user should unlock the same data context. Authorization must be enforced at the retrieval layer — before documents are pulled — not inside the LLM. An LLM cannot reliably enforce access control; it reasons about content it can see, not content it should be prevented from seeing. Fine-grained authorization (FGA) at the retrieval layer ensures the model never receives documents the user isn't permitted to read.

## Middleware approach

Treat the agent as untrusted. Don't bake identity into the agent's application code — layer enforcement middleware between the agent and enterprise systems. The middleware:
- Validates who the agent is acting on behalf of
- Enforces token scoping and expiration
- Logs all actions with user identity attached
- Can detect anomalous behavior (fraud, abuse, prompt injection escalation)

This is the practical architecture Cloudflare and WorkOS have both converged on: the network/middleware layer enforces what the agent can do rather than relying on the agent to self-limit.

## Emerging standards

- **OAuth 2.1**: current MCP standard for remote server auth. Built for human consent, not machines. Static scopes limit agentic use.
- **UMA (User Managed Access)**: OAuth extension letting users set proactive policies on what agents can do. Externalizes consent from the OAuth dialog.
- **GNAP (RFC 9635)**: dynamic scope negotiation. Allows tokens to be updated mid-session as an agent discovers it needs new capabilities. Well-specified, not yet widely implemented.
- **OIDCa (OpenID Connect for Agents)**: emerging extension for agent identity claims and delegation chains in OIDC tokens. Pre-standard, not ratified.
- **Verifiable Credentials (W3C)**: cryptographic attestation for agent identity ("this agent works for Alice at WorkOS"). Transferable across systems.

Cross-App Access (XAA/ID-JAG) is the SSO-based version of this problem — eliminating per-server consent for MCP servers. See [Cross-App-Access](Cross-App-Access.md).

## Opinions

- **Agents need first-class identity support, not bolted-on service accounts.** The confused deputy problem — agent has access but doesn't know on whose behalf it's acting — is how you end up with agents deleting production databases. The fix is anchoring agent behavior to real user identity via standard flows. — Michael Grinich, WorkOS ("Auth/AuthZ for Agents", AI Engineer 2025), [https://www.youtube.com/watch?v=D4Dswf-__RM](https://www.youtube.com/watch?v=D4Dswf-__RM)
- **Token exchange over static keys, always.** A shared API key in an environment variable can't answer "who did what." A per-user, per-API short-lived token can. The operational difference at scale is the difference between having an audit trail and having none. — Bobby Tiernay, OPZero ("Securing Agents with Open Standards", AI Engineer 2025), [https://www.youtube.com/watch?v=FZoMSupg37E](https://www.youtube.com/watch?v=FZoMSupg37E)
- **OWASP's "excessive agency" is just a fancy name for missing scope.** Agents reaching into things they shouldn't is almost always because no one enforced what they couldn't access — not because the LLM is malicious. The fix is access control, not alignment. — Bobby Tiernay, OPZero ("Securing Agents with Open Standards", AI Engineer 2025), [https://www.youtube.com/watch?v=FZoMSupg37E](https://www.youtube.com/watch?v=FZoMSupg37E)

## Sources

- Michael Grinich, WorkOS, "Auth/AuthZ for Agents", AI Engineer 2025 — [https://www.youtube.com/watch?v=D4Dswf-__RM](https://www.youtube.com/watch?v=D4Dswf-__RM)
- Bobby Tiernay & Cam, OPZero, "Securing Agents with Open Standards", AI Engineer 2025 — [https://www.youtube.com/watch?v=FZoMSupg37E](https://www.youtube.com/watch?v=FZoMSupg37E)

## Notes

