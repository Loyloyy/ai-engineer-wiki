# ModernBERT

Encoder-only transformer architecture (2024) redesigned for long-context understanding; achieves 8192-token context with alternating local/global attention, making it practical for production safety classification at 35ms latency.

## Architecture innovations

**Alternating local/global attention**: the core efficiency decision. Most layers (2 out of every 3) use local attention with a 128-token sliding window — fast and memory-efficient. Every third layer uses full global attention across the entire 8192-token context. The pattern gives the model both fine-grained local pattern recognition and long-range reasoning without paying full quadratic attention cost on every layer.

**Rotary positional encoding (RoPE)**: replaces fixed absolute positional embeddings; handles variable-length inputs and generalises better to unseen sequence lengths.

**Flash attention**: memory-efficient attention kernel that avoids materialising the full attention matrix; enables the global attention layers at 8192 tokens without OOM.

**Unpadding + sequence packing**: strips padding tokens before the forward pass and packs multiple short sequences into a single batch element. Eliminates wasted compute on pad tokens, which is significant when input lengths vary (e.g., short vs. long prompts in a safety classifier).

## Safety classification use case

Fine-tuning ModernBERT on the **InjectGuard dataset** (75K prompt injection examples) achieves:
- **85% accuracy** on prompt injection detection
- **35ms latency** per classification

This fits inline in an agent pipeline — the classifier runs as a pre-execution gate on tool call inputs or LLM outputs before they propagate further.

### Attack vectors ModernBERT classifiers target

- Direct prompt injection (adversarial user input)
- Indirect prompt injection (malicious content in retrieved documents)
- GCG gibberish suffix attacks (Greedy Coordinate Gradient; looks like random tokens but jailbreaks models)
- RAG poisoning (injecting adversarial text into the knowledge base)
- MCP asymmetry exploitation (tool call results not visible in UI; model can be instructed via tool response)

## Opinions

- **Encoder models, not decoder LLMs, are the right tool for safety classification** — 35ms and 85% accuracy from a fine-tuned ModernBERT beats using a general-purpose LLM as a judge at 1–3 seconds with higher cost and similar or worse precision on narrow classification tasks. — Diego Carpentero (The Unreasonable Effectiveness of Finetuned ModernBERTs, AI Engineer 2026), [link](https://www.youtube.com/watch?v=YZHPEkfy2kc)

- **Agentic systems have a fundamentally larger attack surface than chat interfaces** — MCP asymmetry (the user can't see tool call responses) and agentic RCE (agents executing code or filesystem operations) create attack classes that didn't exist in prompt-response chat. Safety classifiers must be designed for the agentic context, not just direct user input. — Diego Carpentero (The Unreasonable Effectiveness of Finetuned ModernBERTs, AI Engineer 2026), [link](https://www.youtube.com/watch?v=YZHPEkfy2kc)

## Sources

- Diego Carpentero, "The Unreasonable Effectiveness of Finetuned ModernBERTs", AI Engineer 2026 — [YouTube](https://www.youtube.com/watch?v=YZHPEkfy2kc)

## Notes

