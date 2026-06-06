.PHONY: install eval-all eval-classifier eval-classifier-prompt eval-classifier-gate test

install:
	pip install -e ".[dev]"

eval-classifier:
	cd services/ticket-classifier && MOCK_LLM=1 llmci run

eval-classifier-prompt:
	cd services/ticket-classifier && MOCK_LLM=1 llmci run --config llmci-prompt.yaml

eval-classifier-gate:
	cd services/ticket-classifier && MOCK_LLM=1 llmci run --config llmci-gate.yaml

eval-all:
	$(MAKE) eval-classifier
	$(MAKE) eval-classifier-prompt
	$(MAKE) eval-classifier-gate
	cd services/rag-qa && MOCK_LLM=1 llmci run
	cd services/json-api && MOCK_LLM=1 llmci run
	cd services/support-agent && MOCK_LLM=1 llmci run --config llmci-single.yaml
	cd services/support-agent && MOCK_LLM=1 llmci run --config llmci-multi.yaml
	cd services/summarizer && MOCK_LLM=1 llmci run --config llmci-mock.yaml

test:
	pytest shared/ services/ -q
