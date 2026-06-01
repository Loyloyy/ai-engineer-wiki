# GraphRAG

A retrieval architecture that combines a knowledge graph with vector search, enabling both semantic similarity lookup and explicit multi-hop relationship traversal. The graph layer provides structured, controllable retrieval that vector-only RAG cannot.

## The core problem with vector-only RAG

Standard RAG retrieves chunks by semantic similarity (cosine distance in embedding space). Semantic similarity is not business relevance. A dog named "Melody" will be retrieved in response to "favorite tunes" because the embeddings are close — even though the fact is irrelevant to the domain. Unstructured fact accumulation in a vector database produces noisy recall that degrades with scale. (Observed by Daniel Chalef, Zep, AI Engineer 2025.)

## What a knowledge graph adds

A knowledge graph models entities (nodes) and their relationships (edges), both with typed properties. This gives three capabilities beyond vector search:

**Multi-hop traversal**: query paths across multiple relationships in a single operation. Example: "find people who know skills similar to what Lucy knows" traverses person → skill → similar_skill → person, in a single Cypher query.

**Controllable similarity**: similarity can be defined via explicit relationships, not just vector distance. A "SIMILAR_SKILL_SET" edge between two people can encode the count of overlapping skills; this is exact and auditable. You can filter, remove, or reweight these relationships explicitly.

**Community detection**: graph algorithms (Leiden, Louvain) cluster the graph into communities of densely connected nodes. These communities can be summarized by an LLM and used as high-level retrieval targets. Example: a skills graph produces communities corresponding to "frontend developers," "data engineers," "ML practitioners."

## Hybrid retrieval patterns

GraphRAG typically combines vector search and graph traversal:

1. **Vector search first**: embed the user's query, find semantically close nodes (skills, documents), use those as entry points into graph traversal
2. **Graph traversal**: follow explicit relationships from entry-point nodes to find indirectly related entities
3. **Weighted scoring**: balance semantic similarity score against hard graph-overlap count; tune weights for the domain

Variable-length path queries allow specifying how many hops to traverse: `person -[similar_skill*0..2]-> skill` finds skills reachable within 2 hops of a semantic match. This controls the specificity/recall tradeoff.

## Schema design for LLM query generation

When an LLM generates Cypher queries dynamically (text-to-graph), the graph schema doubles as a hint:

- **Natural language relationship names** help the model: `KNOWS` is better than `R1`; `person KNOWS skill` maps directly to the intent
- **Simpler schemas** work better for dynamic query generation — fewer node labels, fewer relationship types, more properties
- **Annotated schemas**: include descriptions of what each node label means and example traversal patterns inline. The model reads this as context when generating queries
- **Expert tools over full text-to-graph**: for frequently-queried complex traversals, encode them as Python functions or MCP tools rather than asking the model to generate them from scratch every time

## Practical application

1. Define a domain schema: identify the entities and relationships your use case needs (people/skills, documents/clauses, products/categories)
2. Ingest structured and unstructured data: structured data maps directly to graph nodes/relationships; documents go through entity extraction (LLM outputs Pydantic objects → graph nodes)
3. Enrich with embeddings: embed node descriptions/properties and store as vector properties; build a vector index for semantic entry-point search
4. Build community structure: run community detection algorithms; summarize each community with an LLM for high-level retrieval
5. Define retrieval tools: implement 3–5 targeted retrieval functions (get skills for person, find similar skills, find similar people, recommend people by skill set); these become LLM tools or MCP endpoints
6. Build the agent: a LangGraph / React agent with access to these expert tools can answer complex queries by composing tool calls

## Opinions

- **Semantic similarity is not business relevance.** Irrelevant facts pollute memory and vector retrieval because embedding distance has no causal or relational semantics. Domain-aware memory — not better semantic search — is the solution. — Daniel Chalef, Zep ("Stop Using RAG as Memory", AI Engineer 2025), [https://www.youtube.com/watch?v=T5IMo5ntyhA](https://www.youtube.com/watch?v=T5IMo5ntyhA)
- **For agents, simpler graph data models work better with dynamic query generation.** When LLMs generate Cypher, the schema is effectively a prompt. Fewer labels and more natural-language relationship names reduce the model's task. Annotate the schema with example traversal patterns for best results. — Zach Blumenfeld, Neo4j ("Intro to GraphRAG", AI Engineer 2025), [https://www.youtube.com/watch?v=J-9EbJBxcbg](https://www.youtube.com/watch?v=J-9EbJBxcbg)

## Sources

- Zach Blumenfeld, "Intro to GraphRAG", AI Engineer 2025 — [https://www.youtube.com/watch?v=J-9EbJBxcbg](https://www.youtube.com/watch?v=J-9EbJBxcbg)
- Daniel Chalef, Zep, "Stop Using RAG as Memory", AI Engineer 2025 — [https://www.youtube.com/watch?v=T5IMo5ntyhA](https://www.youtube.com/watch?v=T5IMo5ntyhA)

## Notes
