# Voice Agent Design

Design considerations and failure modes for voice-first AI agents, covering latency architecture, conversational naturalness, and cost structure.

## Cascade vs. speech-to-speech

**Cascaded systems** (STT → LLM → TTS) are modular and reliable: each component can be independently optimized, observed, and upgraded. Intelligence, tool use, and observability are mature. Latency is the main drawback — summing three sequential components.

**Speech-to-speech models** eliminate the intermediate text representation. They can theoretically achieve lower latency and preserve paralinguistic cues (tone, emotion, hesitation) that are stripped away when converting to text. But they require full retraining to change the underlying model, lack observability, and are typically limited to factual interaction without tool call support.

The two architectures are not converging quickly: cascaded systems improve as each component improves independently; speech-to-speech models must re-solve intelligence and reliability from scratch.

## Half-duplex vs. full-duplex

Most voice AI systems (including the best commercial speech-to-speech models as of 2026) are **half-duplex**: the model is either listening or speaking. It cannot handle simultaneous speech.

Human conversation is **full-duplex**: overlapping speech, backchanneling ("mhm", "yeah"), and interruption are normal and expected. In some cultures (Japanese), backchannel responses during another person's speech occupy up to 20% of speaking time — breaking when a model doesn't handle this makes the conversation feel robotic and frustrating.

Full-duplex requires training the model to maintain context while receiving audio while generating audio — a different architecture problem from half-duplex generation.

## Tool-call latency as the bottleneck

In production voice agents, tool call latency (500ms–4s, depending on the tool and provider) typically dominates total latency. Fighting for 10–20ms improvements in TTS becomes irrelevant when a single tool call adds 2 seconds.

**Filler generation** is a mitigation: when a tool call is dispatched, the LLM generates a contextually natural filler sentence (e.g., "Tokyo is such an incredible choice — it's a fascinating mix of ultra-modern skyscrapers and beautiful shrines...") while waiting for the result. When the result arrives, it inserts smoothly into the conversation. This moves from a silent wait to a perceived continuation of conversation.

## Cost structure

In cascaded voice agent systems, TTS is the dominant cost component — not LLM inference or STT. Consumer voice apps can burn through funding on TTS API costs before reaching scale. The implication: on-device TTS (running on smartphone CPU rather than cloud API) dramatically changes the unit economics for consumer voice applications.

## Paralinguistic understanding

Speech-to-speech models can in principle capture tone, emotion, and conversational cues that are lost in STT→LLM→TTS pipelines. However, this potential is only realized if the model is trained on data that rewards exploiting those signals. A model fine-tuned purely on factual Q&A (even in speech form) will not learn to respond to emotional tone because there is no training signal encouraging it.

## Opinions

- **Tool call latency is the real bottleneck now.** Voice systems are fighting for 10ms of TTS improvement while a single tool call adds 500ms–4s. We need agents resilient to unpredictable and high-latency tool calls more than we need faster TTS. — Neil Zeghidour, Gradium AI ("When Is the Her Moment?", AI Engineer 2026), [https://www.youtube.com/watch?v=P_RI1kCkRbo](https://www.youtube.com/watch?v=P_RI1kCkRbo)
- **Full-duplex is a solved architecture problem; intelligence and reliability are not.** The conversational naturalness of full-duplex models (like Moshi) is established — adding it to any system is technically feasible. The gap is giving those models the same intelligence, tool use, and observability as cascaded systems. — Neil Zeghidour, Gradium AI ("When Is the Her Moment?", AI Engineer 2026), [https://www.youtube.com/watch?v=P_RI1kCkRbo](https://www.youtube.com/watch?v=P_RI1kCkRbo)
- **Voice is not a commodity.** Current systems are still "a glorified text model with a voice around it." Anything not expressible in text — tone, timing, backchannel, emotional cues — cannot be leveraged until the stack handles it natively. — Neil Zeghidour, Gradium AI ("When Is the Her Moment?", AI Engineer 2026), [https://www.youtube.com/watch?v=P_RI1kCkRbo](https://www.youtube.com/watch?v=P_RI1kCkRbo)

## Sources

- Neil Zeghidour, Gradium AI, "When Is the 'Her' Moment?", AI Engineer 2026 — [https://www.youtube.com/watch?v=P_RI1kCkRbo](https://www.youtube.com/watch?v=P_RI1kCkRbo)

## Notes
