# Fine-Tuning

Adapting a pre-trained model's weights to a task or domain via further training — as opposed to changing behaviour through prompting, context, or tool design alone.

The recurring pipeline across the wiki's small-model talks is staged: **pre/mid-training → SFT → DPO → RL** (see [LFM-2](LFM-2.md)). Each stage does different work:

- **SFT (supervised fine-tuning)** on curated or distilled traces. Strong models can be built with SFT alone if the *data recipe* is right (see [Reasoning-Data-Recipe](Reasoning-Data-Recipe.md)), but SFT is poor at fixing some failure modes — e.g. it barely moves [Doom-Looping](Doom-Looping.md).
- **DPO / preference alignment** to prefer good completions over bad ones.
- **RL** for failure modes and verifiable-reward tasks that SFT and DPO can't reach; how [Verifiers-Rule](Verifiers-Rule.md) governs what RL can train, and how RL produces small task models that beat frontier models on cost (see [RL-Agent-Fine-Tuning](RL-Agent-Fine-Tuning.md)).

**When it's worth it:** fine-tuning is typically essential below ~500M parameters (20–40 point eval gains) and optional above it, where prompting/skills often suffice (see [LiteRT-LM](LiteRT-LM.md)). For prompt-level gains, [GEPA](GEPA.md) argues fine-tuning is often the wrong lever — costly and obsoleted by the next model release. Encoder fine-tunes ([ModernBERT](ModernBERT.md)) beat general LLMs on narrow classification.

## Related pages in this wiki
- [RL-Agent-Fine-Tuning](RL-Agent-Fine-Tuning.md) — RL to specialise small models for agent tasks
- [Reasoning-Data-Recipe](Reasoning-Data-Recipe.md) — SFT-distillation data recipe for reasoning models
- [Doom-Looping](Doom-Looping.md) — failure mode fixed at the RL stage, not SFT
- [LFM-2](LFM-2.md) — the four-stage small-model training pipeline
- [LiteRT-LM](LiteRT-LM.md) — when tiny edge models need fine-tuning
- [Gemma-4](Gemma-4.md) — open weights with a large fine-tune ecosystem
- [ModernBERT](ModernBERT.md) — fine-tuned encoders for safety classification
- [GEPA](GEPA.md) — prompt optimization as an alternative to fine-tuning
- [Verifiers-Rule](Verifiers-Rule.md) — verifiability as the constraint on RL training

## Sources
Synthesis / navigation hub. Per-claim attribution lives on the linked topic pages above.

## Notes
