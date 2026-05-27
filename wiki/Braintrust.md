# Braintrust

An agent quality platform providing evals and observability for LLM-powered products. Used by companies including Notion to run offline experiments and monitor production agent behaviour.

## Overview

Founded ~2023. Originally evals-only; added observability after observing a customer who was running massive evals against production traffic (effectively building their own observability layer). Phil Hetzel leads solutions engineering.

The two pillars: **evals** (pre-production experimentation to gain confidence in agent behaviour) and **observability** (production monitoring to maintain that confidence). Hetzel's framing: "You should be rerunning production in a safe environment" — evals and observability are the same problem from different sides of the deployment boundary.

## Why traces are a hard data problem

LLM agent traces are not like standard application traces:
- **Large**: individual spans can be 10–20 MB (vs. ~kilobytes for standard spans)
- **Semi-structured to unstructured**: heavy text content without fixed schema
- **High velocity**: production agents generate traces rapidly
- **Multiple query patterns**: low-latency retrieval (live observability UI) and aggregate analytics (eval experiments) simultaneously

Braintrust originally used an open-source data warehouse stitched together with a custom DSL (BTQL) and browser-side DuckDB aggregation. This broke for customers like Notion who needed full-text search across millions of traces. The current architecture separates the data storage problem explicitly.

## Headless / agent-native usage

Braintrust increasingly supports headless usage: coding agents (Claude Code, OpenAI Codex) that call the Braintrust API directly to retrieve eval data, run experiments, and update agent configurations without a human in the UI. This requires a data layer queryable via standard SQL, not only a visual interface.

## Sources

- Phil Hetzel, "Why Building Eval Platforms is Hard", AI Engineer 2026 — [https://www.youtube.com/watch?v=_fQ7Z_Wfouk](https://www.youtube.com/watch?v=_fQ7Z_Wfouk)

## Notes
