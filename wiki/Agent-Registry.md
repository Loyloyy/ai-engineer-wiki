# Agent-Registry

Enterprise catalog that unifies discovery and governance of all AI capabilities in an organization — combining an MCP server registry, an A2A agent registry, and a use case registry in a single searchable store.

## Three registries

**MCP registry**: tracks both internal MCP servers and curated public servers. Each entry carries ownership metadata (responsible team), environment (dev/staging/prod), auth model, cost attribution, and direct linkage to the use cases that depend on it. Serves the same function as a service registry in microservices architectures.

**A2A registry**: stores agent cards describing each deployed agent's capabilities, interface, and constraints. Cards are auto-published via CI/CD on git tag — tagging a release triggers the pipeline to push the agent card to the registry without manual steps, eliminating the registration overhead that kills adoption.

**Use case registry**: maps business processes to the agents and MCP servers they invoke, giving a lineage view that makes audits tractable. "Which capabilities does this workflow depend on?" becomes answerable from a single place.

## Supporting infrastructure

**AI gateway**: unified access point routing all LLM calls; enforces enterprise SSO auth (e.g. Entra ID) and applies per-team budget limits. Centralises observability without requiring individual teams to instrument their own calls. See [MCP-Gateway](MCP-Gateway.md) for the analogous MCP-layer pattern.

**Blueprints**: template repositories with boilerplate and CI/CD pre-wired; new agent projects inherit the registration workflow automatically. Blueprints are the forcing function that keeps the registry populated without requiring ongoing manual effort.

## Practical application

1. Create a new agent project from a blueprint template.
2. Define the agent's capabilities in an agent card.
3. Tag a release in git; CI/CD auto-publishes the card to the A2A registry.
4. Register MCP server entries with ownership, environment, and cost metadata.
5. Link agent and MCP entries to the relevant use case in the use case registry for audit lineage.

## Opinions

- **Auto-publishing agent cards on git tag is the key to keeping the registry current** — manual registration steps are dropped by engineers under deadline pressure. The CI/CD hook removes the choice. — Sonny Merla, Mauro Luchetti & Mattia Redaelli, Quantyca (One Registry to Rule Them All, AI Engineer 2026), [link](https://www.youtube.com/watch?v=VXfRt_H-V08)

- **Cost attribution metadata at the capability level (not just at the team level) is what makes budget governance possible** — without it, you can see total spend but can't trace which use cases or agents are expensive. — Sonny Merla, Mauro Luchetti & Mattia Redaelli, Quantyca (One Registry to Rule Them All, AI Engineer 2026), [link](https://www.youtube.com/watch?v=VXfRt_H-V08)

## Sources

- Sonny Merla, Mauro Luchetti & Mattia Redaelli, "One Registry to Rule Them All", AI Engineer 2026 — [YouTube](https://www.youtube.com/watch?v=VXfRt_H-V08)

## Notes

