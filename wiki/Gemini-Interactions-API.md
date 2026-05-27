# Gemini-Interactions-API

Google DeepMind's unified API surface for building with Gemini models and agents, designed to replace `generate_content` with a more developer-friendly, stateful interface that aligns with industry conventions and supports asynchronous agent execution.

## Overview

Launched in beta December 2025. Designed to work with both models (direct inference) and agents (e.g., Deep Research). The same surface handles both; switching is a configuration change, not an API change.

Philipp Schmid (Google DeepMind DevRel): "We want it to be less Google-branded, less proto-specific, less gRPC — to make it easier for developers to build."

## Key capabilities

**Server-side state management**: The server maintains conversation history. Clients send only the new input plus a `previous_interaction_id` referencing the prior turn, rather than re-sending the full history each request. Clients that need explicit context control (for context engineering, compaction, or removing specific items) can still manage state themselves.

**Asynchronous/background execution**: Requests can be dispatched with `background: true`. The client does not keep the HTTP connection open; it polls or receives a webhook when the interaction completes. Designed for agent tasks that take minutes (e.g., Deep Research) where keeping an HTTP connection open >10s is impractical.

**Typed content blocks**: Inputs and outputs are typed blocks (`text`, `function_call`, `thought_signature`, `audio`, `image`, `video`). Same type system for all modalities; matches the pattern of the OpenAI Chat Completions API for developer familiarity.

**Tool combination**: Supports combining built-in tools (Google Search, Google Maps, URL context) with custom function definitions in a single request. Previously, mixing Google Search grounding with custom functions was not possible.

**Implicit caching improvement**: Because the server maintains state, the context passed to the model is identical across turns (no client-side stripping of whitespace or history that would break cache keys). Schmid reports 2–3× better cache hit rates compared to client-managed context, with cache hits reducing input token cost by ~90%.

**Remote MCP support**: The Interactions API supports remote MCP servers as tools alongside built-in and custom function tools.

## Built-in agents

- **Deep Research**: a built-in agent accessible via the API; initiated by setting the model to the research agent rather than a Gemini model. Visits hundreds of URLs over 10–15 minutes.

Google is working on allowing developers to define and customize their own agents accessible via the same API surface.

## Comparison to generate_content

| Feature | generate_content | Interactions API |
|---|---|---|
| State | Client-managed | Server-side (optional) |
| Background execution | No | Yes (webhooks) |
| Tool combination | No (search OR custom) | Yes (search + custom) |
| Content types | Proto-specific | Typed content blocks |
| Cache hit rate | Lower | 2–3× better |

## Sources

- Thor Schaeff & Philipp Schmid, "Building Conversational Agents", AI Engineer 2026 — [https://www.youtube.com/watch?v=cVzf49yg0D8](https://www.youtube.com/watch?v=cVzf49yg0D8)
- Paige Bailey, "Build and Deploy AI-Powered Apps", AI Engineer 2026 — [https://www.youtube.com/watch?v=G_bHFmEAarM](https://www.youtube.com/watch?v=G_bHFmEAarM)

## Notes
