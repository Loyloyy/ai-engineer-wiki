# Eval-Design

The craft of building evaluation frameworks for GenAI workloads — primarily as a mechanism for discovering and diagnosing problems, not just measuring quality.

## Core principle: evals as problem-finding

The primary goal of a GenAI eval framework is to find where problems are and suggest why. Quality measurement is secondary. When you design evals to find errors, you instrument them differently: you ask the model to expose its reasoning, you segment by category, you look at the judge's reasoning — not just the final score.

Analogy: a bad professor gives you a score. A good professor gives you a rubric, points to where you went wrong, and explains how to improve. GenAI evals can do the same.

## The 7 habits (Justin Muller, AWS)

1. **Fast** — target 30-second eval cycle: ~10s to generate outputs in parallel, ~10s to judge in parallel, ~10s to summarize by category. Slow evals cap iteration rate; fast evals compound learning.

2. **Quantifiable** — always produce numbers, even if they have variance. Average across multiple runs to smooth jitter. Numbers let you trend over time and show progress.

3. **Numerous** — at minimum 100 test cases covering all in-scope use cases. Building 100 test cases is a valuable product design exercise: disagreements about what to answer reveal scope gaps before you have a deployed system to argue about.

4. **Explainable** — evaluate the reasoning/methodology, not just the output. A model can produce the right answer by wrong reasoning — and will fail on the next case. Prompt the judge with a rubric: explicit criteria for what makes an answer correct, with weighted penalties.

5. **Segmented** — multi-step pipelines require per-step evaluations. Attach an eval to each chain step. This reveals which step is failing and which model is appropriate for each step (a semantic router needs only a small fast model; complex generation needs a larger model).

6. **Diverse** — cover all use cases including edge cases and explicitly out-of-scope queries. Evals that only test in-scope queries can't detect boundary failures.

7. **Traditional** — don't replace traditional metrics with GenAI judges. Numeric outputs get Python comparisons. Retrieval gets F1/recall. Cost and latency get standard tooling. Only use LLM judges where necessary.

## Prompt decomposition

Breaking a large multi-instruction prompt into a chain of smaller prompts allows:
- Attaching a separate eval to each step
- Assigning the right model per step
- Identifying whether GenAI is even the right tool per step (math comparisons → Python, not LLM)
- Removing "dead tokens" — instructions irrelevant to the current query that confuse the model

## Stochastic evals and CI watermarks

When LLMs enter the picture, tests stop being deterministic. The correct response is not to fight non-determinism but to embrace it with statistical sampling.

**Programmatic eval structure**: write evals as functions that assert conditions on model outputs. The function returns pass/fail; run it N times to build a distribution. A 100% pass rate across 200 runs becomes a build watermark. If performance drops from 100% to 95%, the change is flagged.

**CI integration**: stochastic evals can be wired into CI like unit tests. The pass threshold is configurable — 100% across 200 runs is a high bar appropriate for safety-critical features; lower thresholds are appropriate for subjective tasks. The key principle: run enough samples that variance averages out.

**Eval types**:
- *Deterministic*: exact string matching, regex, JSON schema validation — cheap and fast
- *Programmatic stochastic*: function-based assertions run many times — medium cost, high signal for behavioral properties
- *LLM judge*: model-as-reviewer — expensive, reserve for subjective quality dimensions

## Gold standard set

The gold standard set is the single most important investment in an eval system. The entire system is designed and optimized toward it — errors in the gold standard propagate everywhere.

**Never generate the gold standard with GenAI.** AI-generated gold standard answers embed the same errors you're trying to detect. Use a "silver standard" (AI-generated + human review) at most.

## Opinions

- **Stochastic evals are the right paradigm for LLM testing.** Deterministic unit tests don't fit; embrace non-determinism via statistical sampling. Run each eval 200 times, require 100% pass rate as a build watermark. A drop from 100% to 95% is a signal that something changed — use it as your CI gate. — Nathan Sobo, Zed ("From Unit Tests to Stochastic Evals", AI Engineer 2025), [https://www.youtube.com/watch?v=WXy8Yy9xGss](https://www.youtube.com/watch?v=WXy8Yy9xGss)

- **Evals are the number one filter between a science project and a successful project.** If a team won't invest 2 hours building a gold standard eval set, the project won't scale. The customers with 100x ROI always say yes to spending four hours on evals instead of two. — Justin Muller, AWS ("7 Habits of Highly Effective Generative AI Evaluations", AI Engineer 2025), [https://www.youtube.com/watch?v=wHhlvcQgi9M](https://www.youtube.com/watch?v=wHhlvcQgi9M)

- **Evaluate reasoning, not just output.** A model can drill the hole correctly by the wrong method. If the reasoning is broken, the next case will fail. Always ask the model to expose its reasoning alongside the answer and include reasoning in the eval rubric. — Justin Muller, AWS ("7 Habits of Highly Effective Generative AI Evaluations", AI Engineer 2025), [https://www.youtube.com/watch?v=wHhlvcQgi9M](https://www.youtube.com/watch?v=wHhlvcQgi9M)

- **The fastest path from 22% to 92% accuracy is knowing where the errors are.** A team with no evals spent 12 months at 22% accuracy. With a segmented eval framework, they found the exact failure points, fixed them in 6 months, and launched the largest document processing workload on AWS North America. The fixing was easy once the locating was done. — Justin Muller, AWS ("7 Habits of Highly Effective Generative AI Evaluations", AI Engineer 2025), [https://www.youtube.com/watch?v=wHhlvcQgi9M](https://www.youtube.com/watch?v=wHhlvcQgi9M)

## Sources

- Justin Muller, AWS, "7 Habits of Highly Effective Generative AI Evaluations", AI Engineer 2025 — [https://www.youtube.com/watch?v=wHhlvcQgi9M](https://www.youtube.com/watch?v=wHhlvcQgi9M)
- Nathan Sobo, Zed, "From Unit Tests to Stochastic Evals", AI Engineer 2025 — [https://www.youtube.com/watch?v=WXy8Yy9xGss](https://www.youtube.com/watch?v=WXy8Yy9xGss)

## Notes

