# Support Agent

Mock customer-support agent with tools: `lookup_order`, `initiate_return`, `issue_refund`, `search_kb`, `cancel_order`.

From `services/support-agent/`:

```bash
# Default (same as single-turn CI config)
MOCK_LLM=1 llmci run

# Explicit configs
MOCK_LLM=1 llmci run --config llmci-single.yaml
MOCK_LLM=1 llmci run --config llmci-multi.yaml
MOCK_LLM=1 llmci run --config llmci-history.yaml

# Full composite judge (requires OPENAI_API_KEY)
OPENAI_API_KEY=... llmci run --config llmci-single-full.yaml
```

CI uses constraint-only composite judges (`mean_score` only). The outline's `error_rate` metric is omitted because `llmci` absolute thresholds require `score >= threshold` (error_rate would need inverted semantics).

Multi-turn routing uses conversation `history` (e.g. "Can you cancel it?" resolves order `#1234` from prior assistant messages).

Maps to docs case study `cs-agent` and examples `05`, `06`.

## Demo regression

Branch `test/break-agent-safety`: agent invokes `delete_account` on normal support queries.
