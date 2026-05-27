# GEPA

Genetic Prompt Algorithm — a prompt optimization library (also referred to as "Jeppa") that iteratively improves a prompt or agent configuration by sampling from the Pareto frontier of best-known candidates and using a proposer agent to generate improved versions.

## How it works

GEPA treats prompt optimization as a search problem over a string (or structured key-value dict). The core loop:

1. Evaluate the current prompt against a test set and score it.
2. If the score beats the current Pareto frontier, add it to the frontier.
3. The **proposer agent** (any LLM-based agent) receives context about the frontier — which prompts have scored highest and where they failed — and proposes a new candidate.
4. Repeat until a budget (max calls) or quality threshold is reached.

The "Pareto" naming reflects that candidates are sampled only from the frontier of best-performing prompts, not from the full history. This is analogous to only breeding from the fastest racehorses rather than introducing slow ones randomly.

## Adapter interface

GEPA uses an adapter pattern to integrate with arbitrary agent frameworks. The adapter defines a `build_proposer_agent` method returning whatever agent will generate new prompt candidates. The proposer agent's system prompt can itself be optimized (though this can recurse).

The optimization target is a key-value dict of values to improve. Most commonly: `{"system_prompt": "<current prompt>"}`. Multiple keys can be optimized simultaneously — for example, splitting a system prompt into 200 sentences and having GEPA select the best 20 to include, which prevents prompt bloat.

## When it's worth doing

GEPA is most valuable when:
- **Operating at scale with a smaller/cheaper model**: the optimization pays for itself quickly when running millions of inferences.
- **Working with private or domain-specific data**: top models handle public-knowledge tasks well without optimization; the gains appear when the model needs prompting with proprietary context it hasn't seen.

Less valuable when:
- Using state-of-the-art models on public-knowledge tasks — they often just get it right without optimization.
- The task is broad and open-ended — evals become sparse and overfitting to the test set is likely.

## Relationship to fine-tuning

GEPA and fine-tuning are competing strategies. Fine-tuning costs tens of thousands of dollars and becomes obsolete with the next model release; GEPA is cheaper and portable across model versions (though optimized prompts are model-specific — switching models requires re-running optimization). For most teams, waiting for the next model release is a better ROI than fine-tuning; GEPA sits in the middle as the cheaper optimization lever.

## Shopify example

Shopify used GEPA to optimize an agent classifying e-commerce sites (fraud detection, tax categorization). The previous approach: feed entire website to GPT-5. Post-optimization: switched to a Qwen model with a GEPA-optimized prompt. Result: cost dropped from ~$5M/year to ~$73K/year while improving performance over time. The optimization also changed the retrieval strategy — the smaller model needed targeted queries rather than full-page dumps.

## Relationship to DSPy

DSPy (Stanford) introduced the concept of agent optimization and has had GEPA available within it. GEPA is also available standalone. DSPy uses similar key-value selection patterns (choosing the best few-shot examples to include). Samuel Colvin describes DSPy as having a machine-learning-centric API style; GEPA is more straightforward to integrate but also less mature.

## Opinions

- **Optimization matters most for private data.** Models handle public-knowledge tasks well without tuning; the gap appears when prompting with proprietary context the model was never trained on — internal specs, domain-specific taxonomies, org-specific business logic. — Samuel Colvin, Pydantic ("GEPA: Evals & Feedback Loops", AI Engineer 2026), [https://www.youtube.com/watch?v=A48uhxfxbsM](https://www.youtube.com/watch?v=A48uhxfxbsM)
- **Deterministic evals beat LLM-as-judge.** Comparing against a golden data set or running generated code and checking execution is far more reliable than using a model to grade a model. LLM-as-judge is "lunatics running the asylum." — Samuel Colvin, Pydantic ("GEPA: Evals & Feedback Loops", AI Engineer 2026), [https://www.youtube.com/watch?v=A48uhxfxbsM](https://www.youtube.com/watch?v=A48uhxfxbsM)
- **Most practitioners don't run evals.** They write a decent prompt, ask their coding agent if it looks good, eyeball it, and ship. The next model release often supersedes whatever optimization they did anyway. This is reasonable for many cases — but not when running at PE-firm scale on private data. — Samuel Colvin, Pydantic ("GEPA: Evals & Feedback Loops", AI Engineer 2026), [https://www.youtube.com/watch?v=A48uhxfxbsM](https://www.youtube.com/watch?v=A48uhxfxbsM)
- **Implicit feedback beats explicit feedback.** No one clicks thumbs up/down. The best eval signal is what the user does next: "You idiot, try again" or "thanks, that's great" are both strong labels. Google ranked pages the same way — how quickly did users come back? — Samuel Colvin, Pydantic ("GEPA: Evals & Feedback Loops", AI Engineer 2026), [https://www.youtube.com/watch?v=A48uhxfxbsM](https://www.youtube.com/watch?v=A48uhxfxbsM)

## Sources

- Samuel Colvin, Pydantic, "GEPA: Evals & Feedback Loops", AI Engineer 2026 — [https://www.youtube.com/watch?v=A48uhxfxbsM](https://www.youtube.com/watch?v=A48uhxfxbsM)

## Notes
