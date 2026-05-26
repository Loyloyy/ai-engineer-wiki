# Nested-Context-Injection

A pattern for providing agents with relevant background context by injecting the descriptions of all ancestor topics in a hierarchy directly into the conversation prompt — rather than retrieving context from a memory system at inference time.

## Mechanism

The agent interface is organised as a tree of topics (e.g. Work → Projects → Benji → Customer Support). When a conversation is opened in any node, the system automatically prepends the descriptions of all parent nodes to the first prompt in that conversation. The agent receives, in a single deterministic pass, a complete view of the nested context without ever querying a memory store.

The injection is hierarchical and compositional: each description is a human-authored, stable piece of context that can be maintained and reviewed directly. The agent's understanding of "what Benji is" comes from the Benji topic description, which is written once and remains consistent across all conversations under that node.

## Concrete example

Kitze describes his Wolfer setup: he has a topic tree like Work → Projects → Benji → Customer Support. When he opens a conversation in the Customer Support topic, the first prompt is automatically augmented with:

1. The Work description: what his work context is
2. The Projects description: what kinds of projects exist
3. The Benji description: what the Benji app is, its target users, its current state
4. The Customer Support description: what the goals and constraints of customer support are for Benji

The agent enters the conversation already holding this full context stack. No retrieval query is issued. No memory record is searched. The context is structural.

## Why structure beats retrieval

Kitze's explicit critique of memory systems: probabilistic retrieval introduces the possibility of missing the right context or pulling irrelevant context. Hierarchical injection is deterministic — if the right context is in the parent descriptions, the agent will always have it. The failure mode of a retrieval-based memory system ("it forgot what Benji is") does not exist here because the context is composed structurally from the topic tree, not recalled from a vector store.

The tradeoff is that context is static relative to how often topic descriptions are updated. Retrieval-based memory is better for highly dynamic, individual-fact recall ("what did I say about the payment bug three weeks ago?"). Nested injection is better for stable framing context ("what is this project? what is my role? what are the operating constraints?").

## Contrast with adjacent ideas

**Vector memory / RAG** retrieves relevant past context based on semantic similarity to the current query. This is appropriate when the relevant context is one of many possible facts in a large store, and when the right fact to retrieve changes significantly per query. It is ill-suited for stable framing context that should *always* be present.

**System prompts** serve a similar role — priming the model with fixed context before the conversation begins. Nested-context injection is a dynamic, composable system-prompt: the injected content is assembled at conversation-open time from the live topic hierarchy, rather than being a single static document.

**CLAUDE.md / project instructions** in Claude Code operate on the same principle: a hierarchical, structured set of always-present instructions rather than retrieved context. Nested-context injection applies this idea to multi-agent personal assistants.

## Opinions

- **Memory systems don't solve the problem people think they solve.** For stable framing context, structural injection is more reliable than retrieval. The right context isn't something you search for — it's something you should always have. — Kitze, Sizzy.co ("The End of Apps", AI Engineer 2026), [https://www.youtube.com/watch?v=4fntwuOoedA](https://www.youtube.com/watch?v=4fntwuOoedA)
- **The productive future of personal AI is inversion: AI works continuously in the background and prompts humans for decisions, rather than humans prompting AI.** The people who will get the most out of agents are those who delegate 99% of execution and reserve themselves for judgment calls. Structural context management (not remembered facts) is the foundation that makes this viable. — Kitze, Sizzy.co ("The End of Apps", AI Engineer 2026), [https://www.youtube.com/watch?v=4fntwuOoedA](https://www.youtube.com/watch?v=4fntwuOoedA)

## Sources

- Kitze, "The End of Apps", AI Engineer 2026 — [https://www.youtube.com/watch?v=4fntwuOoedA](https://www.youtube.com/watch?v=4fntwuOoedA)

## Notes
