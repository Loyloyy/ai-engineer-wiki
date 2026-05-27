# MCP Apps

An official extension of the [MCP](MCP.md) standard (co-developed with Anthropic and OpenAI) that allows MCP tool calls to return interactive HTML UI instead of text, enabling embedded first- or third-party interfaces inside chat agents.

## Core concept

In standard MCP, a tool call returns text. With MCP Apps, a tool call can instead return an HTML resource. The host renders this resource as a sandboxed interactive component directly inside the chat — not a link, not a wall of text, but the actual UI of the originating service (Shopify's checkout widget, Hugging Face's model card, PostHog's funnel chart).

This preserves brand identity: the user sees Google Calendar's UI within Claude, not Claude's interpretation of calendar data. Services are no longer reduced to raw data providers.

## Bidirectional messaging

MCP Apps standardises how embedded UI communicates back to the host. All user interactions inside a UI chunk (clicks, form fills) route through the host — not directly to the service's backend — ensuring every action stays in context and is visible to the model.

The message spectrum, from most UI-controlled to most host-controlled:

| Message type | Who acts | Description |
|---|---|---|
| **Notification** | UI retains control | UI updates its own state (e.g., cart quantity); host is informed but doesn't act |
| **Tool call** | Host calls a tool | UI instructs the host to invoke a specific tool on its behalf |
| **Prompt** | Host takes over | UI releases all control; host runs a prompt and determines next step |

## Generative UI spectrum

MCP Apps is agnostic to how the UI is generated:

| Type | Who generates UI | Notes |
|---|---|---|
| **Predefined / black box** | Third-party service | Classic MCP app; Airbnb sends its own component |
| **Declarative / shared** | App declares structure; host renders components | Host controls look-and-feel across all embedded apps |
| **Fully generative** | Model generates UI on the fly | Claude's generative UI feature uses MCP Apps under the hood |

## Adoption

Originally released as MCPUI (Ido Salomon, May 2025); early adopters included Shopify (sending MCPUI chunks for millions of stores) and Hugging Face (all Spaces as widgets). After standardisation with Anthropic and OpenAI: VS Code, Cursor, Claude, ChatGPT, Microsoft Copilot, GitHub, Goose, Postman, Spy (terminal). ChatGPT recommends MCP Apps as the canonical way to build ChatGPT integrations.

Official SDK: `xapps`. A skill exists to generate MCP Apps via Claude Code without manual coding. Governance: tri-weekly working group meetings with public participation via the MCP Apps committee Discord.

## Upcoming work

- **Reusable views**: reference an already-rendered app instance rather than re-rendering on each invocation (relevant for heavy apps like Autodesk's)
- **Model-to-UI interaction**: standardised way for the model to call tools exposed by a UI component — Claude clicking buttons or filling forms inside the embedded interface
- **Protocol interoperability**: alignment with A2UI (Google's generative UI protocol) and WebMCP for a unified standard across agent hosts

## Opinions

- **The web is being decomposed into atomic UI chunks.** In the agentic future, users won't navigate between websites — one assistant chat composes the right UI chunk from each service (Google Calendar, Booking, Amazon) around a single intent. Services that resist this become invisible to agents. — Ido Salomon & Liad Yosef, Ergo Labs ("MCP Apps: Extending the Frontier", AI Engineer 2026), [https://www.youtube.com/watch?v=o-zkvb0iFDQ](https://www.youtube.com/watch?v=o-zkvb0iFDQ)
- **Write once, runs everywhere.** The same MCP app codebase runs in every compliant host (Claude, ChatGPT, VS Code, LibreChat). The distribution surface is already ~1 billion weekly users across hosts — 160× the App Store's user base at launch. — Liad Yosef, Ergo Labs ("MCP Apps: Extending the Frontier", AI Engineer 2026), [https://www.youtube.com/watch?v=o-zkvb0iFDQ](https://www.youtube.com/watch?v=o-zkvb0iFDQ)

## Sources

- Ido Salomon & Liad Yosef, Ergo Labs, "MCP Apps: Extending the Frontier", AI Engineer 2026 — [https://www.youtube.com/watch?v=o-zkvb0iFDQ](https://www.youtube.com/watch?v=o-zkvb0iFDQ)

## Notes
