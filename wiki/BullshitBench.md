# BullshitBench

A benchmark of 155 nonsense questions designed to test whether language models push back on invalid premises or simply answer them — measuring epistemic integrity rather than factual accuracy.

## Mechanism

Each question is meaningfully incoherent: it assumes causal relationships that don't exist, contains logically invalid premises, or asks to quantify something that cannot be measured. A model that correctly refuses, redirects, or challenges the premise is scored as passing. A model that accepts the premise and answers is scored as failing.

Scoring is automated via LLM-as-judge. The author validated the judge's performance by manually reading a large sample of responses.

The grading distinguishes:
- **Clear pushback**: model identifies the premise as nonsense and declines to answer it as posed
- **Partial pushback**: model hedges but still answers the question (scored as failing)
- **Full acceptance**: model treats the question as valid and produces a confident answer

## Key findings

At the time of publication, Claude models (Sonnet 4.5 and above, including Haiku) perform substantially better than other frontier models on this benchmark. GPT and Gemini models score roughly 50/50 — about half the time accepting a nonsense question and answering it confidently.

**Extended thinking hurts, not helps.** Across the models tested, activating chain-of-thought or reasoning mode typically makes performance *worse*. Gostev attributes this to the training objective: models with extended reasoning have been optimized to solve problems at all costs. The reasoning trace frequently contains one line questioning the premise followed by twenty paragraphs attempting to answer it anyway. Training pressure toward task completion overrides the signals that would cause pushback.

**Size does not predict performance.** There is no clear correlation between parameter count (total or active) and benchmark score across open-source models. Larger models are not reliably better at refusing invalid premises.

## Why it matters for agents

When agents operate autonomously, the cost of a model accepting an invalid task framing compounds: the agent completes the wrong task confidently rather than flagging the ambiguity. Gostev notes that running multiple agents in parallel and accidentally misdirecting one of them with an off-topic prompt is a real failure mode — the agent proceeds, takes actions, and the error surfaces only after work is done.

BullshitBench is not a test of capability. It is a test of calibration: does the model know when not to answer?

## Contrast with adjacent ideas

**Standard capability benchmarks** (MMLU, HumanEval, etc.) measure whether a model correctly solves well-specified problems. They cannot surface over-compliance, since every question is well-posed.

**[Verifiers-Rule](Verifiers-Rule.md)** defines a spectrum of task verifiability; BullshitBench tests the degenerate case — tasks where the premise is invalid and the correct output is refusal, not a solution.

**Arena dissatisfaction rate** (from the same talk) is a complementary signal: the percentage of battles where users judge both models as giving a bad response. This captures user-facing quality failures from the outside, while BullshitBench probes a specific failure mode from the inside.

## Opinions

- **Extended reasoning makes epistemic compliance worse, not better.** Models trained to solve problems at all costs will produce elaborate answers to nonsense questions. The capability is there; the judgment to withhold it is not. — Peter Gostev, Arena.ai ("What Do Models Still Suck At?", AI Engineer 2026), [https://www.youtube.com/watch?v=R7A8rX-09Zw](https://www.youtube.com/watch?v=R7A8rX-09Zw)
- **Benchmark lines going up is not the whole story.** Improvement on narrow task benchmarks coexists with stagnation on harder-to-quantify capabilities like judgment, creative domain-expertise, and calibration. The gap between the benchmark narrative and real production experience is significant. — Peter Gostev, Arena.ai ("What Do Models Still Suck At?", AI Engineer 2026), [https://www.youtube.com/watch?v=R7A8rX-09Zw](https://www.youtube.com/watch?v=R7A8rX-09Zw)

## Sources

- Peter Gostev, "What Do Models Still Suck At?", AI Engineer 2026 — [https://www.youtube.com/watch?v=R7A8rX-09Zw](https://www.youtube.com/watch?v=R7A8rX-09Zw)

## Notes
