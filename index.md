# Wiki Index

## Benchmarks
- [Benchmark-Design](wiki/Benchmark-Design.md) — Craft of designing AI benchmarks: lifecycle from idea → spread → training target → saturation; properties of good benchmarks; meme lifecycle
- [BullshitBench](wiki/BullshitBench.md) — 155-question benchmark testing model pushback on nonsense premises; measures epistemic calibration, not capability

## Concepts
- [12-Factor-Agents](wiki/12-Factor-Agents.md) — Framework of twelve engineering principles for building reliable agents; agents are software, LLMs are stateless functions, own your control flow
- [AI-Code-Review](wiki/AI-Code-Review.md) — Two-axis framework for AI code reviewers: LLM capability × developer desire; action rate as the success metric; 50% human baseline achievable
- [AI-Dev-Productivity](wiki/AI-Dev-Productivity.md) — Empirical Stanford study: 15–20% net AI productivity gain; matrix by task complexity × project maturity; greenfield vs brownfield; language popularity effects
- [Agent-Eval-Map](wiki/Agent-Eval-Map.md) — Taxonomy dividing agent evaluation into semantic quality (representations) and behavioral quality (actions); eval ops as a distinct discipline
- [Agent-Identity](wiki/Agent-Identity.md) — Auth/authz for agents: persona shadowing, delegation chains, capability tokens, CIBA; treat agent as untrusted; token exchange over static keys
- [AFK-Tasks](wiki/AFK-Tasks.md) — Implementation work delegable to agents without human presence; contrasted with always-HIL planning
- [Agent-Legible-Codebase](wiki/Agent-Legible-Codebase.md) — Codebase designed for agent navigation: explicit flow, unique names, no hidden magic, single primitive libraries
- [Classifier-Free-Guidance](wiki/Classifier-Free-Guidance.md) — Sampling technique amplifying the conditional vs unconditional prediction delta; universally applied in diffusion models
- [Coherence-Trap](wiki/Coherence-Trap.md) — Engineering mistake of treating LLM output coherence as evidence of intelligence; LLMs are coherent pattern-matching systems, not reasoning machines
- [Context-Engine](wiki/Context-Engine.md) — Pre-computation layer supplying agents with expert graphs, organisational history, and resolved best practices
- [Context-Lifecycle](wiki/Context-Lifecycle.md) — Engineering discipline for context: generate, test, distribute, observe, and adapt prompts/skills like software
- [Context-Rot](wiki/Context-Rot.md) — Degradation in LLM output quality as context fills, even below stated limits
- [Continuous-Compute](wiki/Continuous-Compute.md) — Infrastructure paradigm replacing CI/CD at agent scale; embeds validation in the loop, pre-merge queue, stateful compute, semantic human approval
- [Coordination-Debt](wiki/Coordination-Debt.md) — Wasted work and misalignment from skipping team alignment before agents build; aggravated by fast implementation
- [Deep-Modules](wiki/Deep-Modules.md) — Large functionality behind simple interfaces; improves AI navigability and testability
- [Doom-Looping](wiki/Doom-Looping.md) — Infinite token repetition in small reasoning models on hard tasks; mitigated by DPO and RL with verifiable rewards
- [Durable-Agent-Execution](wiki/Durable-Agent-Execution.md) — Framework for production agent durability: append-only context log + VM-level execution snapshots; replaces replay model for long-running sessions
- [Fine-Tuning](wiki/Fine-Tuning.md) — Hub: adapting model weights via SFT/DPO/RL; staged pipeline, data recipes, when it's worth it vs. prompting; ties together the small-model and reasoning-model pages
- [Harness-Engineering](wiki/Harness-Engineering.md) — Discipline of structuring codebases, tooling, and processes so agents can execute the full engineering job with minimal human intervention per loop
- [Intentional-Compaction](wiki/Intentional-Compaction.md) — Context management pattern for coding agents: proactively compress session into a handoff document so the next context starts with targeted knowledge instead of re-doing discovery
- [High-Bandwidth-Artifacts](wiki/High-Bandwidth-Artifacts.md) — Structured persistent interfaces (docs, tables) for human-agent collaboration, contrasted with linear chat
- [Latent-Diffusion](wiki/Latent-Diffusion.md) — Training diffusion models in compressed latent space rather than pixel space; reduces per-step compute by orders of magnitude
- [Mechanistic-Interpretability](wiki/Mechanistic-Interpretability.md) — Reverse-engineering neural network internals to find and steer individual feature directions; enables attribution, feature steering, dynamic prompting, and model diffs
- [Model-Rot](wiki/Model-Rot.md) — Progressive staleness of LLM domain knowledge as training data ages; acute for fast-moving frameworks and APIs
- [RAG](wiki/RAG.md) — Hub: retrieval-augmented generation; mechanism and the recurring critique that naive RAG underperforms for agents; ties together the retrieval/context-grounding pages
- [Smart-Truncation](wiki/Smart-Truncation.md) — Context management technique: preserve head + tail of conversation window, offload middle to retrievable memory store
- [Smart-Zone](wiki/Smart-Zone.md) — First ~100K tokens of context window where LLM output quality is highest; tasks should be sized to fit
- [Spec-Driven-Code-Generation](wiki/Spec-Driven-Code-Generation.md) — Workflow of generating code from a spec iteratively without engaging with the codebase directly
- [Token-Maxing-Culture](wiki/Token-Maxing-Culture.md) — Perverse incentive pattern where measuring AI token consumption drives junk agent usage over productive work
- [Ubiquitous-Language](wiki/Ubiquitous-Language.md) — Shared domain glossary maintained consistently across developer, codebase, and AI interactions
- [Verifiers-Rule](wiki/Verifiers-Rule.md) — AI solves tasks in proportion to how easy they are to verify; defines a verifiability spectrum

## Patterns
- [Agent-Computer](wiki/Agent-Computer.md) — Giving agents a persistent file system/sandbox for scratchpad planning, memory files, and self-extending script libraries
- [Browser-Agents](wiki/Browser-Agents.md) — AI agents controlling web browsers; ~80% on read tasks, ~50% on write tasks; auth and anti-bot as key failure modes
- [Container-Use](wiki/Container-Use.md) — Pattern for isolated containerized agent workspaces; each agent gets its own filesystem/execution context; supports parallel experiments and multiplayer step-in
- [Agent-Registry](wiki/Agent-Registry.md) — Enterprise catalog combining MCP server registry, A2A agent registry, and use case registry for AI capability governance
- [Agent-Self-Diagnostics](wiki/Agent-Self-Diagnostics.md) — Pattern for agent self-reporting via a report tool; catches capability gaps, tool failures, and workarounds; framing as "feedback to creators" is key
- [Best-Event](wiki/Best-Event.md) — Dispatching the same task to multiple models in parallel work trees; parent agent compares and combines outputs
- [Breadcrumb-Prompting](wiki/Breadcrumb-Prompting.md) — Incremental task disclosure to agents to prevent early-step sprint and late-step quality collapse
- [Code-Mode](wiki/Code-Mode.md) — LLM generates executable code as its tool call; compresses large API surfaces from millions of tokens to ~1K
- [Compressed-Research](wiki/Compressed-Research.md) — Agent pattern automating the research phase of a business event → research → human decision workflow
- [Cross-App-Access](wiki/Cross-App-Access.md) — OAuth extension (XAA/ID-JAG) enabling automatic MCP auth via enterprise SSO; eliminates per-server consent screens
- [Decision-Log](wiki/Decision-Log.md) — Agent self-unblocks on ambiguous decisions and records them for async human review
- [Demand-Driven-Context](wiki/Demand-Driven-Context.md) — Pull-based methodology for curating enterprise knowledge bases: let agents fail on real tasks, surface gaps, document what's missing
- [Eval-Design](wiki/Eval-Design.md) — 7 habits of effective GenAI evals: fast, quantifiable, numerous, explainable, segmented, diverse, traditional; gold standard set; prompt decomposition
- [Eval-Flywheel](wiki/Eval-Flywheel.md) — Continuous loop: production traces → offline evals → agent improvement → deployment; requires purpose-built data layer
- [GEPA](wiki/GEPA.md) — Genetic Prompt Algorithm; iterative prompt optimization via Pareto-frontier sampling and a proposer agent; most valuable for private-data tasks at scale
- [GraphRAG](wiki/GraphRAG.md) — Retrieval architecture combining knowledge graphs with vector search; enables multi-hop traversal and controllable similarity beyond semantic distance
- [Grill-Me](wiki/Grill-Me.md) — Claude Code skill that exhaustively interviews the developer before planning to build a shared design concept
- [Library-Source-Context](wiki/Library-Source-Context.md) — Add library source as git subtree so agents treat it as first-party code; paired with ESLint back-pressure rules to prevent anti-patterns
- [MCP-Gateway](wiki/MCP-Gateway.md) — Enterprise layer centralising auth, access control, and observability across all MCP servers
- [Model-Airplane](wiki/Model-Airplane.md) — Simplified reference implementation showing correct integration shape; thin production simulacrum for agent context
- [Nested-Context-Injection](wiki/Nested-Context-Injection.md) — Inject parent topic descriptions hierarchically into agent conversations instead of relying on memory retrieval
- [Progressive-Tool-Discovery](wiki/Progressive-Tool-Discovery.md) — Loading only relevant tools into agent context rather than dumping full API surfaces; CLI, search, and code-mode approaches
- [Ralph-Loop](wiki/Ralph-Loop.md) — AFK agent execution loop over vertical slice issues until a plan is complete
- [Reasoning-Data-Recipe](wiki/Reasoning-Data-Recipe.md) — SFT distillation pipeline for training reasoning models: multiple traces per question, teacher model selection, synthetic questions, filtering strategies
- [RL-Agent-Fine-Tuning](wiki/RL-Agent-Fine-Tuning.md) — Using RL to fine-tune smaller LLMs for specific agent tasks; realistic environment + multi-component reward + reward hacking mitigation
- [Search-Tool-Design](wiki/Search-Tool-Design.md) — Low-floor/high-ceiling strategy for agent search tools; start general, log behavior, add specialized tools for frequent patterns
- [Skills](wiki/Skills.md) — Portable context-packaging format for coding agents: skill.md with progressive disclosure, optional reference files and scripts
- [Software-Factory](wiki/Software-Factory.md) — Autonomous agent pipeline for 24/7 software production; human provides intent, agents decompose and implement
- [Stop-Hook-Interrogation](wiki/Stop-Hook-Interrogation.md) — Querying the agent at run end about what would have helped; surfaces contradictory directives, missing tools, config errors
- [Validation-Contract](wiki/Validation-Contract.md) — Pre-implementation correctness spec written during planning; defines done independently of implementation to prevent agent drift
- [Vertical-Slices](wiki/Vertical-Slices.md) — Cross-layer task decomposition (DB + service + UI) enabling per-task self-verification by agents
- [Voice-Agent-Design](wiki/Voice-Agent-Design.md) — Design considerations and failure modes for voice-first AI agents, covering latency architecture, conversational naturalness, and cost structure

## Models
- [Gemma-4](wiki/Gemma-4.md) — Google DeepMind open model family; 4 sizes, Apache 2.0, interleaved local/global attention, MoE, PLE for on-device; 500M+ downloads
- [Genie-3](wiki/Genie-3.md) — Google DeepMind world model generating persistent interactive environments from text or video fragments
- [LFM-2](wiki/LFM-2.md) — Liquid AI edge-optimised model family (350M–24B); hybrid short-conv + GQA architecture designed via on-device profiling
- [ModernBERT](wiki/ModernBERT.md) — Encoder-only transformer with alternating local/global attention; 35ms/85% accuracy for LLM safety classification

## Tools
- [ACE](wiki/ACE.md) — GitHub Next prototype; multiplayer coding sessions backed by micro-VMs for team-aligned agentic development
- [AgentCraft](wiki/AgentCraft.md) — RTS-inspired multi-agent orchestration interface; filesystem-as-map, collision detection, campaign mode
- [Braintrust](wiki/Braintrust.md) — Agent quality platform; evals + production observability; purpose-built trace data layer
- [Gemini-Interactions-API](wiki/Gemini-Interactions-API.md) — Google DeepMind's unified agent+model API; server-side state, async execution, tool combination, typed content blocks
- [LiteRT-LM](wiki/LiteRT-LM.md) — Google cross-platform LLM inference runtime for edge devices; progressive skill loading, LoRA hot-swapping
- [MCP](wiki/MCP.md) — Model Context Protocol; open standard connecting agents to external tools via client-server protocol; 110M monthly downloads
- [MCP-Apps](wiki/MCP-Apps.md) — Official MCP extension for embedding interactive HTML UI inside chat agents; bidirectional messaging, generative UI spectrum
- [MLX](wiki/MLX.md) — Apple Silicon ML framework; on-device inference via unified memory; iOS support via MLX Swift LM; TurboQuant for 1M context
- [n8n](wiki/n8n.md) — Visual low-code workflow automation with AI agent node and human-in-the-loop tool call interceptor
- [OpenAI-Codex](wiki/OpenAI-Codex.md) — OpenAI's software engineering agent; plugins, sub-agents, automations, code review, guardian approvals
- [OpenClaw](wiki/OpenClaw.md) — Fastest-growing open-source coding agent; ~2K contributors; OpenClaw Foundation governance; security-first design
- [Paperclip](wiki/Paperclip.md) — Open-source human control plane for AI labor; org-chart agent hierarchy with skills, QA, and approval workflows
- [Pi](wiki/Pi.md) — Minimal 4-tool coding agent with hot-reloadable TypeScript extension API; Terminal Bench #6; emphasises context transparency
- [Unblocked](wiki/Unblocked.md) — Context engine product for engineering teams; expert graphs, org history, best practices via MCP/CLI/API
