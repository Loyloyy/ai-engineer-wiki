# Progressive-Tool-Discovery

A family of approaches for giving agents access to large API surfaces without loading all tool definitions into context at once — discovering and loading only the tools relevant to the current task.

## The problem

Exposing a large API as [MCP](MCP.md) tools naively creates a context overload problem: a 2,000-endpoint API converts to millions of tokens of tool definitions, far exceeding any model's context window. Even at moderate scale (40–100 tools), agent performance degrades: the model gets confused about which tool to call and starts making errors.

## Three approaches

### 1. CLI-based tool access

The agent has shell access and calls the service's CLI binary. It uses `--help` flags to introspect available commands and parameters on demand. Tools are never loaded into context as definitions — the agent reads help text, forms a command, and executes it.

**Pros**: Zero context cost for tool definitions; full API coverage; agents already familiar with CLIs.  
**Cons**: Requires shell access; less structured than typed tool calls; error handling is less predictable.

### 2. Tool search (semantic retrieval)

The agent has access to a search tool that takes a query and returns the K most relevant tool definitions from a larger store. Only the retrieved tools are added to the live context. Unused tools from a prior search may remain in context until cleared.

**Pros**: Works without shell access; structured tool calling once retrieved; applicable to remote MCP clients.  
**Cons**: Retrieval quality determines coverage — the wrong query misses the right tool; unused retrieved tools still consume context; non-deterministic.

This is the approach Claude Code uses for the Cloudflare MCP integration (and Anthropic's "tool search" API).

### 3. Code-mode (programmatic tool calling)

Rather than calling pre-defined tools, the agent writes code against a typed SDK generated from the API's OpenAPI specification. The code is executed in an isolated sandbox. Type definitions serve as a compact API description (~1,000 tokens for thousands of endpoints) and the model generates the necessary function calls.

**Pros**: Minimal context cost; full API coverage from a single TypeScript type file; benefits directly from model capability improvements; execution is reproducible.  
**Cons**: Requires a sandbox with appropriate isolation guarantees; running LLM-generated code was previously a security anti-pattern; requires the API provider to generate and maintain typed SDK.

Cloudflare's implementation uses V8 Workers as the sandbox (Cloudflare Workers isolates). The sandbox has no access to secrets by default; internet access and other capabilities are granted explicitly via boolean flags. Carey reports the generated-code approach as superior for large APIs but notes that most MCP clients have not yet adopted it due to the "running untrusted code" concern.

## Practical application

The three approaches are not mutually exclusive. A single MCP deployment may use tool sets (coarse grouping) + tool search (fine-grained retrieval within a set) + code-mode for full-API access when available.

The emerging direction: agents will select tools programmatically — "server discovery will be automatic and tool use will become compositional, like bash piping" — so that thousands of tools become the norm rather than an exception (Sam Morrow, GitHub).

## Contrast with adjacent ideas

**[MCP-Gateway](MCP-Gateway.md)** solves enterprise access control, auth, and observability across many MCP servers. Progressive discovery solves the context-size problem within a single server's tool surface. They are complementary layers.

**[Smart-Zone](Smart-Zone.md)** motivates why tool overload matters: every tool definition in context consumes smart-zone budget before any user work begins.

## Opinions

- **We shouldn't be dumping loads of tools into context. That's the main thing.** MCP as a protocol is fine; naive exposure of full API surfaces over MCP is the mistake. — Matt Carey, Cloudflare ("MCP = Mega Context Problem", AI Engineer 2026), [https://www.youtube.com/watch?v=YBYUvGOuotE](https://www.youtube.com/watch?v=YBYUvGOuotE)
- **Code is a very compact plan.** Instead of many individual tool calls, one tool called `code` gives the agent much more degrees of freedom at a fraction of the context cost. As models get smarter, programmatic tool calling will be the default. — Matt Carey, Cloudflare ("MCP = Mega Context Problem", AI Engineer 2026), [https://www.youtube.com/watch?v=YBYUvGOuotE](https://www.youtube.com/watch?v=YBYUvGOuotE)

## Sources

- Matt Carey, "MCP = Mega Context Problem", AI Engineer 2026 — [https://www.youtube.com/watch?v=YBYUvGOuotE](https://www.youtube.com/watch?v=YBYUvGOuotE)
- Sam Morrow, "Scaling GitHub for Your Agents", AI Engineer 2026 — [https://www.youtube.com/watch?v=0n3MKk7r60w](https://www.youtube.com/watch?v=0n3MKk7r60w)

## Notes
