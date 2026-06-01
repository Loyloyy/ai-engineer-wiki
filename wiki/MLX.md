# MLX

Apple Silicon ML framework — a PyTorch/TensorFlow equivalent optimised for unified memory architecture, enabling on-device inference for frontier models on Mac, iPhone, and iPad.

## What it is

MLX is an open-source array framework for Apple Silicon from Apple. Unlike PyTorch (optimised for cloud GPU) and LiteRT-LM (Google's cross-platform edge runtime), MLX targets Apple's unified memory architecture specifically — CPU, GPU, and Neural Engine share the same memory pool, eliminating copy overhead between compute units.

Over 4,000 models have been ported to MLX format. Day-zero support for frontier open-source model releases (e.g., Gemma 4 on release day) is a community goal.

## Capabilities

**MLX VLM** — vision-language models on device. Enables real-time image analysis, object detection, grounded visual reasoning, and multimodal Q&A. Runs entirely offline; powers LM Studio's inference engine.

**MLX Audio** — modular audio pipeline for on-device voice agents:
- Automatic speech recognition (Whisper-based models)
- Text-to-speech (Marvis: custom model, <100ms latency)
- Speech-to-speech (end-to-end voice conversation)

Supports Python and Swift; modular design lets you swap ASR, LLM, and TTS components independently, so the pipeline can be tuned to available hardware.

**MLX Video** — on-device video generation from text prompts, including chained generation for narrative sequences.

## TurboQuant

KV cache compression technique that reduces memory requirements ~4x without matching loss on standard benchmarks. Enables 1M-token context on-device (dependent on model size and hardware). Implementation: quantise the KV cache entries rather than the weights, preserving output distribution. Result: at 300K context, throughput nearly doubles.

## Hardware utilisation

MLX uses the GPU, not the Neural Engine. Neural Engine access requires Core ML (Apple private API), which as of 2026 has poor developer ergonomics. A hybrid GPU + Neural Engine inference path is in development. Monitoring GPU utilisation: `mactop` CLI tool shows real-time GPU/CPU/memory usage.

## Use cases

- **Offline/low-connectivity environments**: on-device inference works without internet or cloud subscriptions.
- **Privacy-sensitive workloads**: no data leaves the device.
- **Voice agent pipelines**: assemble STT + LLM + TTS with per-device hardware budget selection.
- **Vision-language**: real-time camera analysis (accessibility, security, dash cam).
- **Robotics**: MLX Audio + MLX VLM as perception layer for embedded robots.

## iOS / iPhone support

MLX runs on iPhone via **MLX Swift LM** — an iOS/macOS Swift package that downloads models from HuggingFace and provides inference via the same unified-memory architecture as Mac. Quantised model variants are typically available in the MLX Community on HuggingFace within 30 minutes of a new model release.

Performance benchmark: [Gemma 4](Gemma-4.md) at 8-bit, 4-bit quantised on the latest iPhone: **~40 tok/s**. Older iPhones achieve ~20 tok/s — still usable for most interactive applications.

**Locally AI** is a native iPhone/iPad/macOS chatbot built on MLX Swift LM; acquired by **LM Studio** (the cross-platform AI studio for local models) in April 2026. LM Studio runs models via llama.cpp or MLX, opens a local API server with OpenAI-compatible endpoints, and enables desktop users to serve models to their own apps. The acquisition brings MLX Swift LM's iOS ecosystem into LM Studio's multi-platform distribution.

Structured generation (constrained output) is not yet built into MLX Swift LM as of April 2026; third-party packages are available. Tool calling is supported natively.

## Sources

- Prince Canuma, Neywa Labs, "Why MLX", AI Engineer 2026 — [https://www.youtube.com/watch?v=zTLJNHj0DeQ](https://www.youtube.com/watch?v=zTLJNHj0DeQ)
- Adrien Grondin, Locally AI, "40 tok/s Gemma 4 with MLX: Running LLMs on Your iPhone", AI Engineer 2026 — [https://www.youtube.com/watch?v=a2muGkT4WD4](https://www.youtube.com/watch?v=a2muGkT4WD4)

## Notes
