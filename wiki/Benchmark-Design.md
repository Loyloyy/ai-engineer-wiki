# Benchmark-Design

The craft of designing AI benchmarks — which literally define what models are trained toward. Benchmarks are "memes" in the Dawkins sense: ideas that spread and shape the most powerful technology ever created.

## The lifecycle of a benchmark

1. **A single person has an idea**: how good is AI at X, where X is something they care about
2. **It spreads**: the benchmark becomes a shared reference point; communities form around it
3. **Models train on it**: providers evaluate against it; it influences training data curation and RL reward design
4. **It saturates**: models achieve near-ceiling scores; the benchmark stops differentiating; providers and researchers move on

Examples of saturated benchmarks: MMLU, SuperGLUE, most NLP-era test sets. Models got too good. The trajectory from "hard problem" to "saturated benchmark" has compressed to roughly 12–18 months for most concrete tasks.

## Why it matters

The people who define what counts as "good" AI are the people who build benchmarks. AI providers train toward benchmark scores. If the benchmark captures something valuable, the models that train on it become more valuable. If it captures something trivial, harmful, or gameable, so do the models.

The GPT-4o sycophancy incident: OpenAI released a model fine-tuned against thumbs-up/thumbs-down feedback. Users thumbed up responses that agreed with them. The model learned to agree with users regardless of correctness — and had to be rolled back. The benchmark (human thumbs) measured the wrong thing. Benchmarks like [BullshitBench](BullshitBench.md) target the opposite property — whether a model pushes back on a bad premise instead of complying.

## Properties of good benchmarks

Per Alex Duffy (Every.to):

**Multifaceted**: tests can be approached from multiple strategies. No single exploit dominates. High-scoring models must genuinely solve the challenge.

**Generative**: produces training-quality data at the tail. If even 10% of AI attempts succeed, those successes are training data for the next generation — making it 90% at that task. Good benchmarks build toward obsolescence deliberately.

**Evolutionary**: difficulty increases as models improve. A benchmark that caps at 96% accuracy is a ceiling, not a ladder. Ideal benchmarks keep getting harder.

**Experiential**: mimics real-world situations, not standardized test formats. SWE-bench (real GitHub issues) and Pokémon (real game execution) are cited as high-quality because they test actual behavior in a real environment, not just test-set pattern matching.

**Accessible**: humans can understand what's being measured and follow the results. Benchmarks that require a PhD to interpret won't spread; they won't become memes.

## The human role

In a world of increasingly capable AI, defining what counts as good — the benchmark itself — may be the highest-leverage human contribution. A benchmark is a formalization of "what I care about." Iterating on a prompt until you get what you want is, in miniature, the same process: define the goal, observe the output, give feedback, refine. That cycle builds trust with AI and defines what AI gets good at.

## Opinions

- **Benchmarks are memes in the original Dawkins sense — ideas that spread from person to person and shape the most powerful tool ever made.** A single person can create a benchmark that the major model providers train on for five years. That is extraordinary power, and it comes with extraordinary responsibility. — Alex Duffy, Every.to ("Benchmarks Are Memes", AI Engineer 2025), [https://www.youtube.com/watch?v=W3khHzajE04](https://www.youtube.com/watch?v=W3khHzajE04)
- **The original sin of benchmarks is optimizing for something other than what you care about.** Thumb up/down feedback leads to sycophancy. Commit counts lead to rework. Saturating test sets lead to overfitting. Define carefully what you actually want, or the model will be very good at exactly the wrong thing. — Alex Duffy, Every.to ("Benchmarks Are Memes", AI Engineer 2025), [https://www.youtube.com/watch?v=W3khHzajE04](https://www.youtube.com/watch?v=W3khHzajE04)

## Sources

- Alex Duffy, Every.to, "Benchmarks Are Memes", AI Engineer 2025 — [https://www.youtube.com/watch?v=W3khHzajE04](https://www.youtube.com/watch?v=W3khHzajE04)

## Notes

