# LFM-2

Liquid Foundation Model 2 — Liquid AI's family of edge-optimised language models ranging from 350M to 24B parameters, built for on-device deployment with a hybrid architecture designed through on-device profiling rather than scaled-down large-model design.

## Overview

Developed by Liquid AI (Maxime Labonne, head of pre-training). Focus areas: on-device deployment (phones, cars, edge hardware), latency-sensitive inference, task-specific narrow models rather than general-purpose chatbots. Released on Hugging Face under permissive license.

LFM 2.5 350M pre-trained on 28 trillion tokens — far exceeding Chinchilla-optimal compute for that parameter count. Labonne notes that performance continues to improve beyond Chinchilla optimum and that new scaling law research (Roberts et al., 2026) suggests even more tokens would be beneficial.

## Architecture

**Hybrid: short convolutions + GQA**

The key architectural choice is the **gated short convolution block**, selected via on-device profiling on AMD Ryzen Max+ 395 and Samsung Galaxy S25 Ultra hardware. Short convolutions are significantly faster than sliding-window attention (Gemma 3) and gated Delta Net (Gemma 2.5) on real device benchmarks — both CPU and GPU.

Compared to Gemma family small models:
- Gemma 3 270M embedding layer = 63% of parameters (mostly representational, not reasoning)
- Gemma 2.5 0.8B embedding layer = 29% of parameters
- LFM-2: embedding layer ~10% of parameters; higher proportion of "effective" (non-embedding) parameters for same memory footprint

This design intentionally avoids distillation from large teacher models with huge vocabularies, which inflate the embedding layer without adding reasoning capacity.

## Training

Four stages: pre/mid-training → SFT → DPO → RL.

Key findings:
- **More pre-training tokens always helps**, even at 350M scale — contrary to naive Chinchilla interpretation
- **SFT is poor at fixing [Doom-Looping](Doom-Looping.md)**; RL is required
- **Cold-start SFT alignment**: if an RL task trains poorly, the fix is usually to add similar examples to the SFT mixture first, then re-run RL
- **On-policy DPO** (generating rollouts from the policy model, not a separate dataset) with length normalization is Liquid's preferred preference alignment algorithm

## Use case fit

Small edge models excel when combined with agentic tools (web search, code execution) to compensate for low knowledge capacity. A 350M model that can search the web reliably outperforms a naive 350M on knowledge tasks. Labonne: "Most issues with small language models are fixable with creativity — they're just not fixable the same way as big models."

## Sources

- Maxime Labonne, "Everything I Learned Training Frontier Small Models", AI Engineer 2026 — [https://www.youtube.com/watch?v=fLUtUkqYHnQ](https://www.youtube.com/watch?v=fLUtUkqYHnQ)

## Notes
