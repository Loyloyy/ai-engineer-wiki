# Classifier-Free-Guidance

Sampling technique for diffusion models that amplifies the conditional signal by computing the delta between a conditional prediction (with a text prompt) and an unconditional prediction (no prompt), then pushing the sample further in the conditional direction; universally used in production image and video generation.

## Mechanics

During training, the model is trained on two types of inputs alternately:
- **Conditional**: the model sees both the noisy image and the text prompt → learns `p(image | prompt)`
- **Unconditional**: the prompt is replaced with a null token → learns `p(image)` with no conditioning

At sampling time, both predictions are computed at each denoising step:

```
guided_score = unconditional_score + guidance_scale × (conditional_score - unconditional_score)
```

The `guidance_scale` (often called "CFG scale" or "w") controls how hard the model chases the conditional signal. At `guidance_scale = 1`, the model ignores the guidance. At typical values of 7–15, the model produces images that are strongly prompt-consistent. At very high values, the model produces oversaturated, "burned" images that are maximally prompt-consistent but unrealistic.

## Trade-off: prompt fidelity vs. diversity

Higher guidance scale → images that match the prompt closely, but with reduced variety across samples and potential quality artifacts.  
Lower guidance scale → more natural, diverse outputs that may stray from the prompt.

This is the primary quality control knob in image generation: raising guidance scale is often the first thing to try when a model ignores parts of the prompt.

## Why it's called "classifier-free"

The original guidance technique for diffusion models used a separately trained image classifier to compute gradients that steered the denoising process toward a target class. "Classifier-free" guidance eliminates the separate classifier by training the conditional and unconditional predictions inside the same model — cheaper, simpler, and more general (works with any conditioning signal, not just discrete classes).

## Relationship to latent diffusion

CFG is applied in latent space when used with [Latent-Diffusion](Latent-Diffusion.md) models. The guided score is computed over latent representations rather than pixels, so the additional unconditional forward pass costs the same as the conditional one — roughly doubling per-step compute, which is acceptable given how much latent diffusion reduced the base cost.

## Sources

- Sander Dieleman, Google DeepMind, "Building Generative Image/Video Models at Scale", AI Engineer 2026 — [YouTube](https://www.youtube.com/watch?v=xOP1PM8fwnk)

## Notes

