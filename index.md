# Wiki Index

## Benchmarks
- [BullshitBench](wiki/BullshitBench.md) — 155-question benchmark testing model pushback on nonsense premises; measures epistemic calibration, not capability

## Concepts
- [AFK-Tasks](wiki/AFK-Tasks.md) — Implementation work delegable to agents without human presence; contrasted with always-HIL planning
- [Context-Rot](wiki/Context-Rot.md) — Degradation in LLM output quality as context fills, even below stated limits
- [Coordination-Debt](wiki/Coordination-Debt.md) — Wasted work and misalignment from skipping team alignment before agents build; aggravated by fast implementation
- [Deep-Modules](wiki/Deep-Modules.md) — Large functionality behind simple interfaces; improves AI navigability and testability
- [Doom-Looping](wiki/Doom-Looping.md) — Infinite token repetition in small reasoning models on hard tasks; mitigated by DPO and RL with verifiable rewards
- [High-Bandwidth-Artifacts](wiki/High-Bandwidth-Artifacts.md) — Structured persistent interfaces (docs, tables) for human-agent collaboration, contrasted with linear chat
- [Model-Rot](wiki/Model-Rot.md) — Progressive staleness of LLM domain knowledge as training data ages; acute for fast-moving frameworks and APIs
- [Smart-Zone](wiki/Smart-Zone.md) — First ~100K tokens of context window where LLM output quality is highest; tasks should be sized to fit
- [Spec-Driven-Code-Generation](wiki/Spec-Driven-Code-Generation.md) — Workflow of generating code from a spec iteratively without engaging with the codebase directly
- [Ubiquitous-Language](wiki/Ubiquitous-Language.md) — Shared domain glossary maintained consistently across developer, codebase, and AI interactions
- [Verifiers-Rule](wiki/Verifiers-Rule.md) — AI solves tasks in proportion to how easy they are to verify; defines a verifiability spectrum

## Patterns
- [Breadcrumb-Prompting](wiki/Breadcrumb-Prompting.md) — Incremental task disclosure to agents to prevent early-step sprint and late-step quality collapse
- [Cross-App-Access](wiki/Cross-App-Access.md) — OAuth extension (XAA/ID-JAG) enabling automatic MCP auth via enterprise SSO; eliminates per-server consent screens
- [Decision-Log](wiki/Decision-Log.md) — Agent self-unblocks on ambiguous decisions and records them for async human review
- [Eval-Flywheel](wiki/Eval-Flywheel.md) — Continuous loop: production traces → offline evals → agent improvement → deployment; requires purpose-built data layer
- [Grill-Me](wiki/Grill-Me.md) — Claude Code skill that exhaustively interviews the developer before planning to build a shared design concept
- [MCP-Gateway](wiki/MCP-Gateway.md) — Enterprise layer centralising auth, access control, and observability across all MCP servers
- [Model-Airplane](wiki/Model-Airplane.md) — Simplified reference implementation showing correct integration shape; thin production simulacrum for agent context
- [Nested-Context-Injection](wiki/Nested-Context-Injection.md) — Inject parent topic descriptions hierarchically into agent conversations instead of relying on memory retrieval
- [Progressive-Tool-Discovery](wiki/Progressive-Tool-Discovery.md) — Loading only relevant tools into agent context rather than dumping full API surfaces; CLI, search, and code-mode approaches
- [Ralph-Loop](wiki/Ralph-Loop.md) — AFK agent execution loop over vertical slice issues until a plan is complete
- [Software-Factory](wiki/Software-Factory.md) — Autonomous agent pipeline for 24/7 software production; human provides intent, agents decompose and implement
- [Stop-Hook-Interrogation](wiki/Stop-Hook-Interrogation.md) — Querying the agent at run end about what would have helped; surfaces contradictory directives, missing tools, config errors
- [Vertical-Slices](wiki/Vertical-Slices.md) — Cross-layer task decomposition (DB + service + UI) enabling per-task self-verification by agents

## Models
- [Gemma-4](wiki/Gemma-4.md) — Google DeepMind open model family; 4 sizes, Apache 2.0, interleaved local/global attention, MoE, PLE for on-device
- [LFM-2](wiki/LFM-2.md) — Liquid AI edge-optimised model family (350M–24B); hybrid short-conv + GQA architecture designed via on-device profiling

## Tools
- [ACE](wiki/ACE.md) — GitHub Next prototype; multiplayer coding sessions backed by micro-VMs for team-aligned agentic development
- [AgentCraft](wiki/AgentCraft.md) — RTS-inspired multi-agent orchestration interface; filesystem-as-map, collision detection, campaign mode
- [Braintrust](wiki/Braintrust.md) — Agent quality platform; evals + production observability; purpose-built trace data layer
- [Gemini-Interactions-API](wiki/Gemini-Interactions-API.md) — Google DeepMind's unified agent+model API; server-side state, async execution, tool combination, typed content blocks
- [MCP](wiki/MCP.md) — Model Context Protocol; open standard connecting agents to external tools via client-server protocol
- [OpenAI-Codex](wiki/OpenAI-Codex.md) — OpenAI's software engineering agent; plugins, sub-agents, automations, code review, guardian approvals
