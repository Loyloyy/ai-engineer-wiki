# Browser-Agents

AI agents that control a web browser to execute tasks on behalf of a user — navigating pages, interacting with UI elements, filling forms, and taking state-changing actions.

## Architecture

Most browser agents run the same core loop:
1. **Observe** — take a screenshot (VLM approach) or extract DOM/HTML (text approach) to understand current state
2. **Reason** — determine the next step required to progress toward the goal
3. **Act** — click, scroll, type, or navigate; action changes browser state, starting the loop again

Two observation strategies:
- **VLM approach** (screenshot → visual model): handles arbitrary UIs naturally; slower
- **Text/DOM approach** (HTML extraction): faster; brittle on dynamic or canvas-based UIs

## Performance data (WebBench, June 2025)

WebBench: 5,000+ tasks on ~500 websites, combining read and write tasks. As of June 2025:

- **Read tasks** (information retrieval, web scraping): ~80% success — comparable to human-in-the-loop baseline
- **Write tasks** (state changes: form fill, purchase, login, update): ~50% success — significant drop
- **HIL (human in the loop)**: ~80% across both types; last 20-25% failures are often infrastructure/network-related

## Why write tasks fail

- **Longer trajectories** — more steps → higher cumulative error probability
- **Authentication barriers** — login/credential management is a hard problem for agents; triggers anti-bot protections
- **Dynamic UI complexity** — form inputs, multi-step interactions, captchas are significantly harder than scrolling/filtering
- **Anti-bot protections** — websites with write workflows apply stricter protection than read-only pages

## Use cases

- Web scraping at scale (sales prospecting, market research)
- Software QA — automated UI testing
- Form/job application automation
- Generative RPA — replacing brittle traditional RPA workflows that hard-code UI structure

## Opinions

- **Browser agents are already at human-level for read tasks.** The remaining 20% failures are mostly infrastructure issues (network timeouts, CAPTCHAs, connectivity) — not agent capability gaps. The solvable problem is now write tasks. — Jerry Wu & Wyatt Marshall, Illuminate ("The Current State of Browser Agents", AI Engineer 2025), [https://www.youtube.com/watch?v=Djv8Sp11UjI](https://www.youtube.com/watch?v=Djv8Sp11UjI)

- **Infrastructure is a first-class concern in browser agent benchmarks.** The environment the agent runs in — browser version, network reliability, JavaScript rendering speed — affects results as much as the model itself. Most published benchmarks don't control for this. — Jerry Wu & Wyatt Marshall, Illuminate ("The Current State of Browser Agents", AI Engineer 2025), [https://www.youtube.com/watch?v=Djv8Sp11UjI](https://www.youtube.com/watch?v=Djv8Sp11UjI)

## Sources

- Jerry Wu & Wyatt Marshall, Illuminate, "The Current State of Browser Agents", AI Engineer 2025 — [https://www.youtube.com/watch?v=Djv8Sp11UjI](https://www.youtube.com/watch?v=Djv8Sp11UjI)

## Notes

