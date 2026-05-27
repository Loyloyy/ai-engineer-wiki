# LiteRT-LM

Google's open-source cross-platform LLM inference runtime for edge devices (mobile, desktop, IoT), part of the Google AI Edge stack. Formerly built on TensorFlow Lite (LiteRT).

## Overview

LiteRT-LM is the auto-regressive inference layer of the Google AI Edge stack, providing APIs in C++, Java, Swift (forthcoming), and Python. It ships as part of Android system services and has been used in products including Google Photos, YouTube Shorts, and Pixel's live voice translation. The same `.litert_lm` file runs on CPU and GPU across Android, iOS, macOS, Linux, Windows, and IoT.

**LiteRT** (the parent library) is the non-auto-regressive runtime for other model types — voice activity detection, image tracking, denoising — that typically accompany an LLM in a full production app. LiteRT-LM builds on LiteRT specifically for LLMs.

For NPU acceleration, an ahead-of-time (AOT) compilation step is required to produce a device-specific artifact; CPU/GPU use a just-in-time (JIT) workflow with a single portable file. LiteRT has completed NPU integrations with Qualcomm and MediaTek; NPU execution yields 3–10x performance improvements over CPU, and up to 13x in specific accelerator configurations.

**Benchmark performance vs. Llama**: On mobile, LiteRT-LM runs up to 35× faster than Llama.cpp. On desktop, performance is at par. On IoT devices (e.g. Raspberry Pi), roughly 3× faster.

## Skill system (progressive on-demand loading)

LiteRT-LM includes an agent skill architecture designed for token efficiency on small models:

- Each skill has a `skill.md` (metadata: name, one-line description, trigger keywords, detailed instructions) and optional JavaScript or native intent assets.
- The model is given only the one-line descriptions of available skills at startup — not the full instructions.
- When the model decides a skill is relevant, it calls a `load_skill` tool. The full `skill.md` contents are returned as a tool response and enter the context window.
- The model then calls `run_javascript` or `run_intent` as appropriate.

This keeps context small for resource-constrained edge models. The pattern resembles [Progressive-Tool-Discovery](Progressive-Tool-Discovery.md) applied to on-device constraints.

Skills can be written in JavaScript or as Android system intents. API keys for web services can be stored per-skill. Google AI Gallery includes a community skills repository where developers submit skills; popular ones are promoted to featured status in the app.

## Tiny model deployment workflow

For models under ~500M parameters (in-app GenAI use cases):

1. Start from a base Gemma checkpoint (or any compatible transformer).
2. Generate synthetic fine-tuning data using a larger cloud LLM.
3. Fine-tune with `liteRT-torch` (includes PyTorch-native optimizations + quantization).
4. Export to `.litert_lm` file.
5. Deploy with LiteRT-LM APIs or prototype with Google AI Gallery.

For 2–4B models (system GenAI), customization via prompting and skills is preferred over fine-tuning.

**LoRA hot-swapping**: LiteRT-LM supports loading base model weights once and swapping LoRA adapters at runtime without reloading — useful for robotics or IoT platforms with multiple task-specific adapters.

**Fine-tuning impact**: 20–40 point eval improvement for tiny models (sub-500M parameters). Fine-tuning is typically essential below 500M; narrow, task-specific models above that threshold may work without it.

## Sources

- Cormac Brick, "TLMs: Tiny LLMs and Agents on Edge Devices with LiteRT-LM", AI Engineer 2026 — [https://www.youtube.com/watch?v=BKWpYIWvAo4](https://www.youtube.com/watch?v=BKWpYIWvAo4)
- Chintan Parikh & Weiyi Wang, Google, "Accelerating AI on Edge", AI Engineer 2026 — [https://www.youtube.com/watch?v=Lm8BLHkxiAo](https://www.youtube.com/watch?v=Lm8BLHkxiAo)

## Notes
