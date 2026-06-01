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

## Enterprise voice deployment patterns (Intercom Finn Voice)

From shipping a voice agent to enterprise customers in 100 days:

**Use-case wedge**: start with out-of-hours calls (replaces voicemail, low risk, no disruption to in-hours workflows). Once customers trust it, expand to in-hours.

**Answer chunking**: for multi-step responses, break into chunks, deliver one at a time, confirm before continuing ("Should I go on to the next step?"). Works especially well for troubleshooting flows.

**User mindset shift**: early in a call, users often interact like an IVR (single words: "support", "yes", "no"). As they hear the agent use full sentences, they shift to full sentences themselves. Design the opening turns to model the expected conversation format.

**Workflow integration is the deployment blocker**: majority of enterprise feedback was about escalation paths and context handoff (transcript summary to human agent on pickup), not about model quality or latency. Non-flashy integrations are the difference between pilot and production.

**Resolution rate definition (northstar)**: user explicitly confirms resolution OR user disconnects after hearing ≥1 answer AND does not call back within 24 hours.

**Pricing trend**: market converging from usage-based (per minute) to outcome-based (per resolution). Outcome-based better aligns incentives but requires the provider to absorb cost on unresolved calls.

## Voice overlay paradigm

A **voice overlay** sits alongside human-to-human calls and adds real-time AI assistance without becoming a third speaker. The AI listens passively, surfaces relevant help at the right moment (language suggestions, definitions, context), and otherwise stays out of the way.

Distinct from both standard voice agents (human-to-AI) and meeting bots (post-call summaries). The constraint is that assistance must be glancible and non-disruptive — the overlay cannot break the conversational rhythm of the two humans speaking.

Engineering challenges Gregory Bruss calls the **four horsemen of overlay engineering**:
1. **Jitterbug input**: speaker pauses (breath, thought) cause STT to drop; smart debouncing required.
2. **Context repair**: must keep a current model of the conversation in under-second budget — the full pipeline must be optimized.
3. **Premature interrupt / no show**: help too early interrupts; too late is useless. Needs fine-grained conversational awareness to pick the right moment.
4. **Glancible ghost**: every hint arriving on screen taxes attention. Must be dismissible and minimal; attention is a currency.

Design principles: transparency and control over overlay involvement; minimum cognitive load; progressive autonomy (help more at start, less as user gains proficiency).

## Opinions

- **Tool call latency is the real bottleneck now.** Voice systems are fighting for 10ms of TTS improvement while a single tool call adds 500ms–4s. We need agents resilient to unpredictable and high-latency tool calls more than we need faster TTS. — Neil Zeghidour, Gradium AI ("When Is the Her Moment?", AI Engineer 2026), [https://www.youtube.com/watch?v=P_RI1kCkRbo](https://www.youtube.com/watch?v=P_RI1kCkRbo)
- **Full-duplex is a solved architecture problem; intelligence and reliability are not.** The conversational naturalness of full-duplex models (like Moshi) is established — adding it to any system is technically feasible. The gap is giving those models the same intelligence, tool use, and observability as cascaded systems. — Neil Zeghidour, Gradium AI ("When Is the Her Moment?", AI Engineer 2026), [https://www.youtube.com/watch?v=P_RI1kCkRbo](https://www.youtube.com/watch?v=P_RI1kCkRbo)
- **Voice is not a commodity.** Current systems are still "a glorified text model with a voice around it." Anything not expressible in text — tone, timing, backchannel, emotional cues — cannot be leveraged until the stack handles it natively. — Neil Zeghidour, Gradium AI ("When Is the Her Moment?", AI Engineer 2026), [https://www.youtube.com/watch?v=P_RI1kCkRbo](https://www.youtube.com/watch?v=P_RI1kCkRbo)
- **Voice is not just chat with sound.** Answer length, latency tolerance, and user mindset differ fundamentally. A voice agent requires separate conversation design from a chat agent — chunked answers, filler words for latency, shorter responses. Ship a version of the product before tackling the model improvements. — Peter Bar, Intercom ("Shipping an Enterprise Voice AI Agent in 100 Days", AI Engineer 2025), [https://www.youtube.com/watch?v=HOYLZ7IVgJo](https://www.youtube.com/watch?v=HOYLZ7IVgJo)
- **In enterprise voice deployments, workflow integration matters more than model quality.** The majority of customer feedback was about escalation paths and context handoff — not about latency or resolution rates. The demo works, but the deployment fails if the support team can't integrate it into their existing workflow. — Peter Bar, Intercom ("Shipping an Enterprise Voice AI Agent in 100 Days", AI Engineer 2025), [https://www.youtube.com/watch?v=HOYLZ7IVgJo](https://www.youtube.com/watch?v=HOYLZ7IVgJo)

## Sources

- Neil Zeghidour, Gradium AI, "When Is the 'Her' Moment?", AI Engineer 2026 — [https://www.youtube.com/watch?v=P_RI1kCkRbo](https://www.youtube.com/watch?v=P_RI1kCkRbo)
- Peter Bar, Intercom, "Shipping an Enterprise Voice AI Agent in 100 Days", AI Engineer 2025 — [https://www.youtube.com/watch?v=HOYLZ7IVgJo](https://www.youtube.com/watch?v=HOYLZ7IVgJo)
- Gregory Bruss, "The Voice-First AI Overlay: Designing Conversational Co-Pilots", AI Engineer 2025 — [https://www.youtube.com/watch?v=y9YQc9a3gNw](https://www.youtube.com/watch?v=y9YQc9a3gNw)

## Notes
