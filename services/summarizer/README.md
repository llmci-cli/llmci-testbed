# Summarizer

Article → summary pipeline with LLM-as-judge (real) or heuristic judge (CI mock).

From `services/summarizer/`:

```bash
# CI (deterministic) — use this by default
MOCK_LLM=1 llmci run --config llmci-mock.yaml

# Real LLM judge (requires OPENAI_API_KEY)
OPENAI_API_KEY=... llmci run --config llmci.yaml
```

**Note:** `llmci.yaml` in this directory is the **real LLM judge** config. Running bare `llmci run` here requires `OPENAI_API_KEY` and will fail without it. Always use `llmci-mock.yaml` for local mock runs and CI.

The mock config uses `mean_score` + `pass_rate` only (not `min_score` / `cosine_similarity` from the outline's LLM judge config).

Maps to docs case study `cs-summarization` and `examples/09-summarization-qa`.
