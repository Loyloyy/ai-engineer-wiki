# Latent-Diffusion

Training and running diffusion models in a compressed latent space learned by an auto-encoder rather than in pixel space — reducing the computational cost of generation by orders of magnitude while preserving perceptual quality.

## The problem with pixel-space diffusion

A raw video frame at 256×256 pixels is a tensor with ~196K values. Running a diffusion model's denoising network directly on this representation at every diffusion timestep (typically hundreds of steps) is computationally prohibitive at scale. For video, where you have sequences of frames, the tensor grows by another 2-3 orders of magnitude.

## How latent diffusion works

An **auto-encoder** (encoder + decoder pair) is trained first to compress images into a compact latent representation and reconstruct them back. The encoder maps a 256×256 image to a much smaller latent tensor — typically 32×32×4 — while the decoder inverts this mapping. The auto-encoder preserves the spatial grid structure so the latent representation is still spatially interpretable; it just has far fewer values.

The diffusion model is then trained to operate in this latent space. The denoising network learns to reverse diffusion in latent coordinates rather than pixel coordinates. At generation time:

1. Sample noise in latent space (small tensor)
2. Run denoising network N times in latent space (cheap)
3. Decode the final latent to pixel space (single decoder pass)

The bottleneck in the auto-encoder is what makes this work: by forcing the encoder to compress information through a narrow channel, the auto-encoder learns to retain perceptually significant features and discard high-frequency noise — leaving the diffusion model to work with a cleaner, lower-dimensional signal.

## Why this matters for video

For video generation, pixel-space computation is essentially infeasible at production scale. A 4-second video at 24fps and 512×512 resolution is ~8GB of raw pixel data before any diffusion steps. The same video in a 16× compressed latent space is ~500MB, and the denoising network sees 2 orders of magnitude fewer values per step. [Classifier-Free-Guidance](Classifier-Free-Guidance.md) and other sampling techniques become practical only when the per-step cost is this low. That low per-step cost is the precondition for real-time generative-video systems, including interactive world models like [Genie-3](Genie-3.md).

## Sources

- Sander Dieleman, Google DeepMind, "Building Generative Image/Video Models at Scale", AI Engineer 2026 — [YouTube](https://www.youtube.com/watch?v=xOP1PM8fwnk)

## Notes

