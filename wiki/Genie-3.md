# Genie-3

Google DeepMind's third-generation world model; generates interactive, persistent environments from a text description or a short video fragment, with real-time in-world prompting to modify the environment while a user is inside it.

## Progression from Genie 1 and 2

**Genie 1** (2024): established the core idea of a world model that generates interactive environments from video. Trained on internet video; could simulate simple 2D game-like worlds.

**Genie 2** (2024): extended to 3D environments and longer coherent video generation; improved physics simulation and object interaction fidelity.

**Genie 3**: adds two capabilities that define it as a qualitatively different system:

1. **Persistent memory**: the world state is preserved between sessions. If you enter an environment, interact with objects, change the state of the world, and then leave, the world is as you left it when you return. Earlier world models generated each session from scratch.

2. **Real-time in-world prompting**: while inside a generated environment, a user can describe a change in natural language ("make it rain," "add a locked door here," "replace the floor with water") and the environment updates in real time without leaving and re-entering. The model updates the world state continuously rather than regenerating from a new prompt.

## Generation from text or video

Genie 3 can bootstrap a world from:
- A **text description**: "a forest with a river running through it, medieval ruins in the distance" generates a navigable environment from that description.
- A **short video fragment**: a few seconds of real-world or synthetic video provides the visual style and scene structure; Genie 3 extrapolates an interactive world consistent with what it saw.

## Context from same talk

The Raya Hadsel talk also covered **Gemini Embeddings 2** (omnimodal embeddings supporting 8K text tokens, 128 seconds of video, 80 seconds of audio, full PDF; Matryoshka Representation Learning for variable-dimension outputs) and the **GraphCast → GenCast → FGN** progression in weather foundation models. These are distinct product/research threads from the same speaker.

## Opinions

- **Persistent world state is the threshold that separates a generative toy from a usable creative tool** — a world model that forgets between sessions requires the user to reconstruct their world each time, which collapses the value of anything built collaboratively or incrementally; Genie 3's memory is what makes long-form world-building viable. — Raya Hadsel, Google DeepMind (How Google DeepMind Is Researching the Next Frontier of AI, AI Engineer 2026), [link](https://www.youtube.com/watch?v=zZsTVBXcbow)

## Sources

- Raya Hadsel, "How Google DeepMind Is Researching the Next Frontier of AI", AI Engineer 2026 — [YouTube](https://www.youtube.com/watch?v=zZsTVBXcbow)

## Notes

