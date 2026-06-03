# Mechanistic Interpretability

Reverse-engineering the internal representations of neural networks to understand what concepts individual neurons or feature directions encode, then using that knowledge to inspect and steer model behavior at the neuron level.

## The core idea

Large language models and diffusion models learn internal features — directions in activation space that represent concepts (a "Golden Gate Bridge" feature in Claude, a "lion face" feature in Flux). Mechanistic interpretability (also called "mech interp") finds and maps these features, enabling two capabilities:

- **Attribution**: for any output token, inspect which features were active — see what the model was "thinking about" when it made that choice
- **Feature steering**: amplify or suppress individual features to directly alter model behavior, without changing the prompt

These capabilities treat the model's internals as an engineering substrate rather than a black box.

## Sparse autoencoders

The dominant current technique for finding features is training a **sparse autoencoder** (SAE) on the model's residual stream activations. The SAE learns a dictionary of features; any activation can be decomposed into a sparse linear combination of these features. Each feature then has a human-interpretable label (determined by what text maximally activates it).

Limitations: SAEs must be trained per model; the vocabulary of features is approximate; not all features have obvious semantic meaning.

## Practical use cases for AI engineers

**Whack-a-mole prompting problem**: When an LLM ignores an instruction, fixing the prompt often causes a different instruction to break. With feature steering, instead of re-prompting, you find the feature governing the behavior and directly amplify it. Example: to make a model treat email addresses as confidential PII, find the "sensitive/protected information" feature and steer it up — no prompt change, surgical fix.

**Dynamic prompting**: Set a listener on a feature. When the model's internal state fires a "beverages" feature during generation, intercept and inject a context-specific system prompt. The user sees a single seamless response; the feature activation triggered a prompt injection invisible to them.

**Model diffs**: After post-training (RLHF, SFT), compare the weight changes at the feature level to catch behavioral regressions before deployment. If the model has become sycophantic, this shows up as changes to specific sycophancy-related features.

**Regulated industries**: Provides the explainability layer that healthcare, finance, and law require. An AI decision citing "it activated feature X (risk of non-compliance) at this point in the document" is auditable in a way that a raw probability score is not.

**Red teaming**: Inject adversarial feature values and observe how the model's behavior changes, without needing to craft natural-language jailbreaks.

## Practical application

1. Identify the behavior you want to reliably control (PII handling, tone, domain adherence)
2. Run attribution on a set of examples where the behavior occurs and where it fails
3. Find the features that activate on success but not on failure (or vice versa)
4. Use feature steering to amplify those features at inference time
5. Monitor for off-target effects by running your existing eval suite with the steering active

## Opinions

- **Interpretability is moving from labs to production.** The field produced interesting demos (Golden Gate Claude) for years; in 2025 it started providing differential practical value — PII detection, red teaming, regulated-industry explainability — that wasn't achievable with prompt engineering or fine-tuning alone. — Mark Bissell, Goodfire AI ("Why You Should Care About AI Interpretability", AI Engineer World's Fair 2025), [https://www.youtube.com/watch?v=6AVMHZPjpTQ](https://www.youtube.com/watch?v=6AVMHZPjpTQ)
- **Feature steering outperforms prompt patching for precise behavioral control.** Prompts produce whack-a-mole effects — fixing one instruction breaks another. Steering a specific feature directly is surgical; it targets only the behavior you want to change. — Mark Bissell, Goodfire AI ("Why You Should Care About AI Interpretability", AI Engineer World's Fair 2025), [https://www.youtube.com/watch?v=6AVMHZPjpTQ](https://www.youtube.com/watch?v=6AVMHZPjpTQ)

## Sources

- Mark Bissell, Goodfire AI, "Why You Should Care About AI Interpretability", AI Engineer World's Fair 2025 — [https://www.youtube.com/watch?v=6AVMHZPjpTQ](https://www.youtube.com/watch?v=6AVMHZPjpTQ)

## Notes
