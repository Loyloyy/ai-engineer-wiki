# Reasoning-Data-Recipe

The data pipeline design for training reasoning models via SFT distillation — the "missing link" from DeepSeek R1's training recipe that specifies which data choices actually move performance.

## The distillation approach

DeepSeek R1's final released weights are an SFT model (fine-tuned on 800K examples, 600K of which are reasoning traces). RL was used to generate those traces, but the delivered model is SFT. This means: if you have the right data recipe, you can create strong reasoning models with SFT alone — without running expensive RL infrastructure.

The data pipeline:
1. **Source questions**: from existing datasets, scraped sources, or synthetically generated
2. **Mix sources**: combine and deduplicate
3. **Filter questions**: select the hardest/most informative questions
4. **Generate answers (distillation)**: use a teacher model to produce reasoning traces + answers
5. **Filter answers**: remove low-quality answers (for some domains)

## Key findings (Open Thoughts 3, Bespoke Labs)

**Multiple reasoning traces per question is highly effective**: sampling 16 traces for each of 30K questions performs similarly to having 480K unique questions with 1 trace each. A 16x scale from diversity of examples — each trace shows different reasoning paths, all teaching the same question. Data diversity at the reasoning level, not the question level.

**Better model ≠ better teacher**: Qwen 32B was a stronger teacher than DeepSeek R1 (much larger), and Claude was a terrible teacher despite being a strong model. A brilliant researcher who is a terrible lecturer: strong performance on benchmarks doesn't predict good teaching of reasoning format. Hypothesis: teacher quality is about trace format and length distribution, not benchmark score.

**Synthetic questions work**: top-performing sources included entirely synthetic questions, outperforming scraped forums and human-written problems. Synthetic generation is also scalable — more questions from the same pipeline.

**Question filtering matters**: use an LLM to rate difficulty, or use LLM response length as a proxy for difficulty (longer response = harder problem). Keep the hardest questions. But: what works varies by domain — difficulty labels work for code, response length works for math/science.

**Fewer high-quality sources > many diverse sources**: maximizing number of sources for diversity was counterintuitive — it didn't help. A smaller set of high-quality curated sources outperformed a larger diverse pool.

**For SFT, answer verification doesn't help much**: filtering out incorrect answers didn't improve performance in most experiments. For hard problems, even an incorrect answer from the teacher model provides useful reasoning trace signal. (Contrast with RL, where verification is critical — see [Verifiers-Rule](Verifiers-Rule.md).)

## Surpassing the teacher with distillation

On specialized domains, a small distilled model can surpass the teacher at that specific task. Example: 7B model fine-tuned on 2K legal reasoning questions (5 traces each, incorrect answers filtered) surpasses DeepSeek R1 on Supreme Court decision classification. Specialization at the data level can produce a student that outperforms a teacher on the narrow task, despite the teacher being 50× larger.

## Evaluation guidance

- Small evaluation sets (e.g., AMC math: 30 questions/year) require multiple runs and averaging to get reliable signal. Run the model on the evaluation set 10× and average to reduce variance.
- Without a reliable evaluation signal, data experiments produce noise rather than insight.
- Libraries: Evalchemy (evaluation with sharding/parallelism), curator (data generation/synthetic question creation).

## Opinions

- **The missing link is the data recipe, not the training recipe.** Everyone knows RL+SFT works; nobody published the data choices that make it work. Choosing the right questions, the right teacher model, the right filtering criteria — this is where performance is won or lost, not in the RL algorithm. — Ryan Marten, Bespoke Labs ("Data Recipes for Reasoning Models", AI Engineer 2025), [https://www.youtube.com/watch?v=liG97YXaTSA](https://www.youtube.com/watch?v=liG97YXaTSA)
- **A better model does not make a better teacher.** Benchmark performance and teaching ability are orthogonal. If you're building a distillation pipeline, experiment with multiple teacher models — your strongest available model may not produce the best traces for a student to learn from. — Ryan Marten, Bespoke Labs ("Data Recipes for Reasoning Models", AI Engineer 2025), [https://www.youtube.com/watch?v=liG97YXaTSA](https://www.youtube.com/watch?v=liG97YXaTSA)
- **Distillation can surpass the teacher on specialized domains.** For a narrow task, a fine-tuned 7B model can outperform a 70B+ reasoning model. RL is not the only path to pushing performance past existing frontiers. — Ryan Marten, Bespoke Labs ("Data Recipes for Reasoning Models", AI Engineer 2025), [https://www.youtube.com/watch?v=liG97YXaTSA](https://www.youtube.com/watch?v=liG97YXaTSA)

## Sources

- Ryan Marten, Bespoke Labs, "Data Recipes for Reasoning Models", AI Engineer 2025 — [https://www.youtube.com/watch?v=liG97YXaTSA](https://www.youtube.com/watch?v=liG97YXaTSA)

## Notes

