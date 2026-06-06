#!/usr/bin/env python3
"""RAG pipeline CLI entry point."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from generate import generate  # noqa: E402
from retrieve import retrieve  # noqa: E402


def run_pipeline(input_data: dict) -> dict:
    query = input_data["input"]
    doc_ids, docs = retrieve(query)
    answer = generate(query, docs)
    return {
        "output": answer,
        "contexts": docs,
        "retrieved_ids": doc_ids,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    data = json.loads(Path(args.input).read_text())
    result = run_pipeline(data)
    Path(args.output).write_text(json.dumps(result))


if __name__ == "__main__":
    main()
