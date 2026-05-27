# Cross-App-Access

An OAuth extension pattern (XAA) that enables MCP clients to authenticate to MCP servers automatically via a shared enterprise identity provider — eliminating per-server OAuth consent screens and tying MCP access to SSO session lifecycle.

## The problem

Standard MCP OAuth requires users to complete a separate consent flow for each MCP server they connect to. A developer with a dozen MCP servers must click through a dozen consent screens. Across a team, this multiplies. More critically: OAuth tokens issued this way outlive SSO sessions — if an employee leaves or a machine is compromised, the MCP access tokens may remain valid for days or weeks after the SSO session is revoked.

## Mechanism

XAA uses the **ID-JAG** (Identity JWT Authorization Grant) token, defined in an IETF spec. The flow:

1. User logs in to their enterprise IDP (e.g., Okta) once via SSO. The MCP client (Claude, Cursor) holds the resulting ID token and refresh token.
2. Client requests an ID-JAG token from the IDP, scoped to a specific MCP server audience (e.g., `mcp.figma.com`).
3. IDP verifies: does the user have access to both the client app and the target server app? If yes, it issues the ID-JAG.
4. Client sends the ID-JAG to the MCP server's authorization server.
5. MCP server validates the ID-JAG with the IDP and issues a short-lived access token (typically 5-minute TTL).
6. Client uses the access token for standard MCP communication.

Steps 2–4 are invisible to the user. No consent screen. As long as the SSO session is active, new access tokens are issued automatically when old ones expire.

## Security properties

- **SSO revocation propagates**: when an IT team revokes an employee's Okta session (e.g., on offboarding or compromise), the ID-JAG flow stops working immediately after the current access token expires. Contrast with standard OAuth refresh tokens, which may continue to issue tokens for weeks.
- **Short-lived access tokens**: 5-minute TTL limits the blast radius of a stolen token.
- **IT visibility and control**: IT configures which client apps may request access to which server apps in a "managed connections" portal. The policy is explicit, auditable, and centralized.

## Setup requirements

**IT admin**: configure in the IDP which client apps are permitted to request access to which server apps. The existing SSO application registrations for client (Cursor, Claude) and server (Figma, Notion) are reused — no new applications to register.

**MCP client** (Claude, Cursor): implement SSO login with an XAA-compatible IDP connection; request ID-JAG tokens; exchange for server access tokens. WorkOS provides this capability for apps using it for SSO (including Anthropic and Cursor).

**MCP server**: announce support for the JWT-bearer grant type; accept and validate ID-JAG tokens from the client; issue access tokens on successful validation.

## Current state

Okta supports XAA for OIDC-based connections (SAML support in progress). Microsoft Entra does not yet support XAA. Dynamic Client Registration (DCR) is not required — XAA works with pre-registered client apps, sidestepping the DCR vs. no-DCR fragmentation issue. WorkOS provides a managed implementation for MCP clients.

## Contrast with adjacent ideas

**Standard MCP OAuth** requires per-server consent screens and issues long-lived refresh tokens. XAA replaces consent screens with IDP-mediated token exchange and bounds token lifetime to the SSO session.

**[MCP-Gateway](MCP-Gateway.md)** solves internal enterprise routing, access control, and observability for MCP servers. XAA solves the external authentication flow between a user's MCP client and an MCP server across organizational boundaries. They are complementary.

## Sources

- Garrett Galow, "Cross-App Access for MCP", AI Engineer 2026 — [https://www.youtube.com/watch?v=EmhRyw6xeT0](https://www.youtube.com/watch?v=EmhRyw6xeT0)

## Notes
