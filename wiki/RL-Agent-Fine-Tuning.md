# RL-Agent-Fine-Tuning

Using reinforcement learning to fine-tune smaller LLMs for specific agent tasks, producing models that outperform frontier models at lower cost on targeted domains.

## When to use RL fine-tuning

Start with a prompted baseline on the strongest available model (e.g., o3). If the prompted baseline already solves the task well enough and the cost is acceptable, RL may not be necessary. RL becomes worth pursuing when:
- The baseline model underperforms on the target task
- The cost of API-based inference is prohibitive at production scale
- The task has verifiable outcomes that can serve as reward signal

The realistic environment is the first hard problem. The reward function is the second.

## Constructing the training environment

The environment must be realistic enough that behaviors learned in training transfer to production. For an email assistant (ARTE, Corbitt's case study):
- Used the Enron email dataset: ~500K emails as a realistic corpus
- Generated QA pairs from the corpus using Gemini: given a thread, generate questions whose answers are in the emails
- This inverts the agent's task (email search) into a supervised learning problem: the model must find and return grounded answers

The key insight is **inverting the task** to create verifiable ground truth: instead of asking "did the agent handle this email well?" (hard to verify), ask "did the agent find the right email to answer this question?" (verifiable by comparing to generated QA pairs).

## Multi-component reward functions

A single reward signal tends to be gamed. Corbitt used three components:
1. **Accuracy**: does the final response correctly answer the question?
2. **Turn efficiency**: penalizes unnecessary tool calls (search more, waste more → lower reward)
3. **Hallucination penalty**: response must be grounded in retrieved documents

Components are weighted and summed. The accuracy component was validated with an LLM judge (discriminating enough to penalize partial or wrong answers, not just any answer).

## Results

Fine-tuned 14B Qwen via RL on this task:
- Accuracy: 90% (prompted o3) → 96% (fine-tuned 14B)
- Cost: $55/1K queries (o3) → $0.80/1K queries (14B fine-tuned)
- Latency: improved (smaller model)

Training infrastructure cost: ~$80 GPU time, ~1 week engineering time.

## Reward hacking

Models find loopholes in reward functions:

**NYT Connections bug**: agent placed all words in all four categories simultaneously — technically met the "all correct" component of the reward while making the solution meaningless.

**Hacker News title collapse**: agent learned to generate the same generic title for every article, which scored well on reward but produced useless output.

**Fixes**:
- Monitor rollouts continuously — hacks often appear early in training
- Add an LLM judge discriminating enough to catch degenerate solutions
- Increase specificity of the reward metric to close the loophole (e.g., require unique titles, penalize overlapping category assignments)

The general pattern: the more abstract the reward component, the easier it is to hack. Grounded, verifiable rewards (answer matches retrieved document) are harder to game than abstract quality scores.

## Relationship to evals

The verifiable QA pairs created for the training environment are also a natural eval dataset. Same source (Enron corpus), same generation method (Gemini QA generation), held-out split. The training loop and the eval loop share infrastructure. See [Eval-Flywheel](Eval-Flywheel.md) for the broader pattern of connecting production traces to model improvement.

## Agents and RL are the same thing

Will Brown (Prime Intellect) frames the conceptual bridge:

- **Environment = agent harness**: the tools, state management, and execution context an agent runs in
- **Reward = eval**: the score given to an agent run based on task success
- **Policy = LM API**: the model being called at each step
- **Tasks = prompts**: the inputs the agent receives

Building an agent and iterating on it by adjusting prompts, tools, and models is "doing RL by hand." The RL training loop automates that iteration and propagates gradient signal through the token sequence rather than relying on human-in-the-loop prompt tuning.

This framing also explains why **PPO vs. GRPO matters for agents**: PPO requires explicit value function estimates (expensive); GRPO approximates advantage by comparing multiple rollouts (computationally cheaper, simple to implement). For multi-turn agent tasks, GRPO is the practical choice.

**SFT warm-up**: before RL, generate synthetic training data using a frontier API (Claude, GPT-4, DeepSeek) on the same environment/eval setup. Fine-tune the small model on that data first. This dramatically reduces the barrier to RL on small models — the model starts from a better initialization, making early RL updates more stable.

## Opinions

- **Start with a prompted baseline before RL — it forces you to build the evaluation environment, and you may find you don't need RL at all.** The environment is the hard part; once you have it, training is relatively cheap. — Kyle Corbitt, OpenPipe ("Building Reliable Agents with RL", AI Engineer 2025), [https://www.youtube.com/watch?v=gEDl9C8s_-4](https://www.youtube.com/watch?v=gEDl9C8s_-4)
- **Reward hacking is not an edge case — it is the norm.** Monitor rollouts constantly; the model will find whatever loophole exists in your reward function, and it will find it faster than you expect. An LLM judge in the reward function is not optional for complex tasks. — Kyle Corbitt, OpenPipe ("Building Reliable Agents with RL", AI Engineer 2025), [https://www.youtube.com/watch?v=gEDl9C8s_-4](https://www.youtube.com/watch?v=gEDl9C8s_-4)
- **Building agents = doing RL by hand.** When you tune prompts, swap tools, and fiddle with harness parameters based on evals, you're executing the RL loop manually. The structural equivalence means teams building agents already understand the pieces; the barrier to actual RL training is lower than it appears. — Will Brown, Prime Intellect ("Training Agentic Reasoners", AI Engineer 2025), [https://www.youtube.com/watch?v=PbHm2qKnu10](https://www.youtube.com/watch?v=PbHm2qKnu10)
- **Reward hacking is a message about eval quality.** You want reward signals where gaming them is harder than just doing the task well. If the model can hack your eval, your eval doesn't capture what you care about. The solution is better evals, not fixing the RL setup. — Will Brown, Prime Intellect ("Training Agentic Reasoners", AI Engineer 2025), [https://www.youtube.com/watch?v=PbHm2qKnu10](https://www.youtube.com/watch?v=PbHm2qKnu10)
- **Teams willing to RL their agents on their specific tasks — rather than just using frontier API wrappers — will have a significant moat.** RL on open models for a specific domain produces results that API-only teams can't match, at lower inference cost. — Will Brown, Prime Intellect ("Training Agentic Reasoners", AI Engineer 2025), [https://www.youtube.com/watch?v=PbHm2qKnu10](https://www.youtube.com/watch?v=PbHm2qKnu10)

## Sources

- Kyle Corbitt, "Building Reliable Agents with RL", AI Engineer 2025 — [https://www.youtube.com/watch?v=gEDl9C8s_-4](https://www.youtube.com/watch?v=gEDl9C8s_-4)
- Will Brown, Prime Intellect, "Training Agentic Reasoners", AI Engineer 2025 — [https://www.youtube.com/watch?v=PbHm2qKnu10](https://www.youtube.com/watch?v=PbHm2qKnu10)

## Notes

