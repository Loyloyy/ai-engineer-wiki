# Doom-Looping

A failure mode in language models where the model enters an infinite repetition cycle, generating the same sequence of tokens indefinitely without producing a valid completion. Particularly severe in small reasoning models on hard tasks.

## Mechanism

Doom looping occurs when the model's next-token distribution collapses into a self-reinforcing cycle: the model generates token A, which makes token B likely, which makes token A likely again. The condition is worst under the following combination:
- **Small model**: lower capacity reduces robustness in high-entropy generation states
- **Reasoning/thinking mode**: extended generation chains increase the probability of entering a degenerate state
- **Complex task**: tasks that stretch the model's capability produce higher uncertainty, increasing the chance of collapse

Labonne's data for LFM 2.5 1.2B (a small reasoning model): doom loop rate of ~15–16% after pre-training, barely reduced by SFT alone. After DPO: substantial reduction. After RL: near-elimination.

For comparison: Qwen 3.5 0.8B in reasoning mode exceeds 50% doom loop rate — evidence that simply distilling a larger model produces a model that inherits the generation patterns without the stability properties of a purpose-trained edge model.

## Mitigation approaches

### DPO-based (preference alignment)

Generate 5+ rollouts with temperature sampling (diverse outputs, reducing the probability all doom-loop) plus 1 rollout with temperature 0 (expected to doom-loop). Score all rollouts with an LLM jury. The doom-looping rollout receives the lowest score and becomes the **rejected** response in DPO training. The model learns to prefer non-looping completions.

### RL with verifiable rewards + repetition penalty

During reinforcement learning, use verifiable reward tasks (e.g., math: can you extract a final answer?). A doom-looping response never produces a final answer, so it receives zero reward. Add an n-gram repetition penalty as an auxiliary signal. Temperature sampling on rollouts maintains diversity. Together, these eliminate the remaining doom loops that survive DPO.

## Practical significance

Doom looping makes an edge model unreliable in production. A 15% doom loop rate means 1 in 7 responses hangs indefinitely unless the application has a hard token cutoff. For deployment on phones, cars, or other latency-sensitive environments, this is unacceptable.

The mitigation is not achievable via SFT alone — adding doom-loop-free examples to supervised fine-tuning barely moves the metric. The fix requires RL-stage intervention.

## Contrast with adjacent ideas

**[Context-Rot](Context-Rot.md)** degrades output quality as context fills; doom looping is a categorical failure (generation never terminates) rather than a quality degradation.

**[LFM-2](LFM-2.md)**: Liquid's architecture and training choices are explicitly designed to minimize doom looping as part of treating edge models as their own problem class, not scaled-down large models.

## Opinions

- **Qwen 3.5 0.8B doom loops over 50% of the time in reasoning mode — that's a direct consequence of distillation without purpose-training for edge stability.** Small models are not just scaled-down versions of big models, and this is the concrete cost of treating them that way. — Maxime Labonne, Liquid AI ("Everything I Learned Training Frontier Small Models", AI Engineer 2026), [https://www.youtube.com/watch?v=fLUtUkqYHnQ](https://www.youtube.com/watch?v=fLUtUkqYHnQ)

## Sources

- Maxime Labonne, "Everything I Learned Training Frontier Small Models", AI Engineer 2026 — [https://www.youtube.com/watch?v=fLUtUkqYHnQ](https://www.youtube.com/watch?v=fLUtUkqYHnQ)

## Notes
