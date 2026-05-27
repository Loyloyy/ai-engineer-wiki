# Breadcrumb-Prompting

A prompting pattern for autonomous agents in which task information is disclosed incrementally across multiple steps rather than front-loaded as a single complete instruction — designed to prevent early-task sprint followed by late-task quality collapse.

## The problem it solves

When an agent receives a complete multi-step task upfront, it tends to execute early steps mechanically (low inference effort, "good enough") and spend its attention budget on the final steps. This produces what Danilo Campos calls a "Claude-code-shaped hole through the first four tasks" — early work is correct but shallow — followed by "rock-polish" on the last step where the agent finally engages fully. For an 8-step integration workflow, this means 7 steps done carelessly.

## How it works

Reveal only the current step's goal; frame each step as complete work before disclosing the next.

**PostHog Wizard sequence**:
1. "Find files in this project that contain interesting business value — logins, payment flows, churn signals."
2. "What events would be valuable to track in those files? Don't write any code yet. Just list event names and descriptions."
3. *(Save event list to file)*
4. "Now let's implement PostHog. We have a list of events and fresh documentation. Start integration."

The agent is never told upfront that this is a PostHog integration. Business logic casts a large shadow in code — step 1 reliably surfaces the right files. Step 2 produces thoughtful event naming because it's all the agent is doing. By step 4, all the thinking is already done and the implementation follows a prepared plan.

## Practical application

- Start with reconnaissance, not implementation
- Never mention the destination until the agent has navigated to it naturally
- Intermediate artifacts (event lists, file maps) become structured context for later steps
- Combine with [Model-Airplane](Model-Airplane.md) references and fresh documentation for the implementation step
- Pair with [Stop-Hook-Interrogation](Stop-Hook-Interrogation.md) to catch cases where breadcrumb sequencing is still wrong

## Opinions

- **If you tell the agent exactly where you want to go, it might make a code-shaped hole through the first four tasks and then just get really rock-polishy with the fifth. That is not what we want.** The solution is not to scaffold the behavior heavily but to ask: how do I sequence the information I give it so that it does the right thing? — Danilo Campos, PostHog ("LLM Codegen Fails and How to Stop 'Em", AI Engineer 2026), [https://www.youtube.com/watch?v=juoNbJiZUi0](https://www.youtube.com/watch?v=juoNbJiZUi0)

## Sources

- Danilo Campos, "LLM Codegen Fails and How to Stop 'Em", AI Engineer 2026 — [https://www.youtube.com/watch?v=juoNbJiZUi0](https://www.youtube.com/watch?v=juoNbJiZUi0)

## Notes
