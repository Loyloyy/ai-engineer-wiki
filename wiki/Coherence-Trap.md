# Coherence-Trap

The engineering mistake of treating LLM output coherence as evidence of reasoning or intelligence — and the implications of correctly framing LLMs as coherent pattern-matching systems, not thinking machines.

## What coherence is

Coherence in LLMs is a system property, not a cognitive one. It has four observable properties:

- **Relevance**: output feels topical, connected, and purposeful to the conversation
- **Consistency**: the model maintains a singular tone, terminology, and structure across turns
- **Stability**: the model withstands pressure — questioning its outputs causes it to firm up or course-correct, not collapse
- **Emergence**: capabilities appear that were not explicitly trained — a model can diagnose swine disease or identify cancer markers without having been trained on those tasks, because coherent pattern alignment across related domains generates novel competence

These properties produce output that feels like comprehension. This is the trap: coherence mimics intelligence well enough that engineers over-rely on it and under-architect around its limits.

## The mechanics

LLMs represent concepts via superposition — a single neuron can encode multiple related ideas, and overlapping neuron sets represent concept neighborhoods. When a prompt is issued, it acts as a force vector in high-dimensional latent space, activating the concept clusters most relevant to the input. The model does not retrieve information; it reconstructs the essence of ideas on demand.

This is why hallucinations feel correct: they are coherent pattern completions, not errors in retrieval. The model fills gaps with plausible continuations — the same mechanism that generates useful outputs also generates confident fictions.

RAG functions as "factual anchors" — fragments of grounding context that provide enough "contextual gravity" to pull the force vector toward reality rather than toward plausible fiction. Dense, relevant context works; sparse or irrelevant context does not.

## Engineering implications

Correctly framing LLMs as coherent systems (not intelligent ones) changes how you build:

1. **Hallucinations are features of coherence, not bugs of intelligence.** They are predictable and follow internal logic. Manage them via grounding (RAG, constraints), not by hoping the model "gets smarter."

2. **Prompts are interfaces, not conversations.** They have directional force in latent space. Well-formed prompts shape the output space consistently; poorly formed prompts produce inconsistent outputs because the force vector is underspecified.

3. **Design for emergence, not control.** The system is not deterministic. Build the frame-generate-judge-iterate loop around its non-determinism, rather than fighting it.

4. **Avoid long reasoning chains.** Long chains break coherency over many steps — the model loses grip on the original context. Keep chains modular and reinforce context at each step.

5. **Watch for coherence breakdowns.** Shifts in tone, structure, or terminology signal the model is losing context grip. Treat them as debugging signals.

## Practical application

Frame-generate-judge-iterate:
1. **Frame**: provide the problem, context, and constraints (prompt engineering)
2. **Generate**: produce one or multiple outputs
3. **Judge**: evaluate quality and reasoning (not just the answer)
4. **Validate**: check against external requirements if needed
5. **Iterate**: nudge the model toward the target, then repeat

## Opinions

- **Coherence is a system property, not a cognitive one. LLMs are not intelligent — they are coherent.** The trap is mistaking coherent output for understanding. Once you stop expecting intelligence and start designing for coherence, you build more reliable systems. — Travis Frisinger, AI ETHLite ("The Coherence Trap: Why LLMs Feel Smart But Aren't Thinking", AI Engineer 2025), [https://www.youtube.com/watch?v=u825uxb7LnA](https://www.youtube.com/watch?v=u825uxb7LnA)

- **Hallucinations are an indicator of coherence, not a failure of intelligence.** The model is completing a coherent pattern under insufficient grounding — it is working as designed. The fix is providing enough contextual gravity (dense, relevant RAG) to anchor the output, not improving the model's "intelligence." — Travis Frisinger, AI ETHLite ("The Coherence Trap: Why LLMs Feel Smart But Aren't Thinking", AI Engineer 2025), [https://www.youtube.com/watch?v=u825uxb7LnA](https://www.youtube.com/watch?v=u825uxb7LnA)

## Sources

- Travis Frisinger, AI ETHLite, "The Coherence Trap: Why LLMs Feel Smart But Aren't Thinking", AI Engineer 2025 — [https://www.youtube.com/watch?v=u825uxb7LnA](https://www.youtube.com/watch?v=u825uxb7LnA)

## Notes
