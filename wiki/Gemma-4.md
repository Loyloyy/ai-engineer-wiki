# Gemma-4

Google DeepMind's fourth-generation family of open-source models, released April 2026 under Apache 2.0. Four sizes spanning on-device to high-capability; first Gemma family with a mixture-of-experts model and per-layer embeddings for on-device efficiency.

## Model sizes

| Model | Type | Active params | Notes |
|---|---|---|---|
| E2B | Dense effective | 2.3B (5.1B total) | On-device; audio+vision+text; 32K context |
| E4B | Dense effective | ~4B | On-device; audio+vision+text; 32K context |
| 26B | MoE | 3.8B active (26B total) | First Gemma MoE; 128 experts, 8 active; 128K context |
| 31B | Dense | 31B | State-of-the-art multimodal; 256K context |

The 31B ranked #3 on the global LM Arena leaderboard at launch. The 26B ranked top 6 among open-source models. Both outperform models 20× their size on various benchmarks.

## E2B and E4B edge capabilities

The on-device models (E2B and E4B) in Gemma 4 ship with agent-oriented features built into the model architecture rather than achieved via prompt engineering:

- **Function calling**: native support for tool calling to local APIs and external services; enables on-device agent loops
- **Structured JSON output**: model-native structured output without prompt workarounds
- **Chain-of-thought (thinking mode)**: on-device reasoning trace; Google AI Gallery app exposes this as a visible thinking panel

RAM requirements after quantization: E2B ≈ 1–2 GB (usable on mid-range phones); E4B higher (suited for laptops and IoT devices).

## Architecture highlights

**Interleaved local/global attention (5:1 ratio)**: Local layers use a sliding window of 1,024 tokens (512 for E2B); global layers attend to all preceding tokens. The last layer is always global. GQA groups 2 queries per KV head in local layers, 8 queries per KV head in global layers (with doubled KV head length to compensate for quality). This reduces memory cost significantly while maintaining quality.

**Mixture-of-Experts (26B)**: One shared router expert (always active, 3× size of other experts) + 128 feedforward experts with 8 activated per forward pass. Replaces the standard feedforward layer in the dense architecture.

**Per-Layer Embeddings (PLE) — E2B and E4B only**: Each layer has its own embedding table stored in flash memory (not VRAM), with embedding dimension 256 (vs. 1,536–2,560 for the main embedding table). At each decoder block's output, the PLE for that layer's tokens is looked up from flash and projected into the full embedding dimension. This keeps the main VRAM footprint small while adding per-layer representational capacity. The effective vs. total parameter gap exists because of this design.

**Variable aspect ratio and resolution for vision**: Images are encoded with spatial positional embeddings so that patch positions are correctly represented regardless of image shape. Developers can select from 5 resolution tiers to trade token budget against image fidelity.

## License

Apache 2.0 — explicit commercial use permitted, enabling seamless integration from development through production deployment.

## Sources

- Cassidy Hardin, "Gemma 4 Deep Dive", AI Engineer 2026 — [https://www.youtube.com/watch?v=_A367W_qvc8](https://www.youtube.com/watch?v=_A367W_qvc8)
- Cormac Brick, "TLMs: Tiny LLMs and Agents on Edge Devices with LiteRT-LM", AI Engineer 2026 — [https://www.youtube.com/watch?v=BKWpYIWvAo4](https://www.youtube.com/watch?v=BKWpYIWvAo4)
- Chintan Parikh & Weiyi Wang, Google, "Accelerating AI on Edge", AI Engineer 2026 — [https://www.youtube.com/watch?v=Lm8BLHkxiAo](https://www.youtube.com/watch?v=Lm8BLHkxiAo)

## Notes
