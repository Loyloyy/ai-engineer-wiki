# Proactive Agents

AI agents that continuously monitor context and act without explicit human prompts — identifying opportunities, catching problems, and completing tasks in the background, triggered by natural workflow events rather than user requests.

## The problem with reactive agents

Current AI developer tools are fundamentally reactive: the agent waits for the user to ask, then responds. This creates a hidden cost: the human still carries the mental load of monitoring, following up, and deciding when to engage the agent. Like delegating dishes to a spouse who only does them when reminded — the delegation is incomplete.

Humans are serial processors executing tasks sequentially. Switching contexts costs up to 40% of productive time. If agents only respond to explicit asks, humans must context-switch into agent-management mode constantly. The promise of proactive agents is to eliminate this: the agent handles tasks before the human realizes they need to be done.

## Four design ingredients

1. **Observation**: continuous monitoring of what's happening — code changes, workflow patterns, calendar, communications — to maintain an up-to-date model of context and intent

2. **Personalization**: learning how the specific user works, what they tend to ignore, what their preferences and constraints are, which parts of the codebase they don't want touched

3. **Timeliness**: acting neither too early (interrupting flow) nor too late (missing the moment when the insight is useful). The agent needs fine-grained conversational awareness to know when to surface something

4. **Workflow integration**: embedding into the spaces where the user already works — terminal, IDE, repository — rather than requiring context switches to a separate application

## Contrast with async agents

[Durable-Agent-Execution](Durable-Agent-Execution.md) and [Continuous-Compute](Continuous-Compute.md) address long-running async agents that the user kicks off and leaves to complete. Proactive agents are different: they are small, continuously observing, and self-initiating on lower-stakes background tasks — fixing auth bugs, updating configs, preparing migrations, flagging potential errors — without waiting to be asked.

## Practical application

1. Choose observable signals from the user's natural workflow (git commits, open tabs, calendar events, running tests, terminal commands)
2. Define the action space narrowly — the agent should only initiate tasks where false positives are low-risk and reversible
3. Surface suggestions with transparency (what the agent noticed, what it did, why) rather than silently taking action
4. Build a feedback mechanism so the agent learns which proactive actions the user accepts vs. dismisses

## Opinions

- **Developers shouldn't babysit agents; agents should babysit the workflow.** The mental load of managing async agents is just as high as doing the tasks yourself. The unlock is agents that watch natural workflow events and act without being asked — doing the dishes without being reminded. — Kath Korevec, Google Labs ("Proactive Agents", AIE Code Summit 2025), [https://www.youtube.com/watch?v=v3u8xc0zLec](https://www.youtube.com/watch?v=v3u8xc0zLec)

## Sources

- Kath Korevec, Google Labs (Project Jewels/Ada), "Proactive Agents", AIE Code Summit 2025 — [https://www.youtube.com/watch?v=v3u8xc0zLec](https://www.youtube.com/watch?v=v3u8xc0zLec)

## Notes
