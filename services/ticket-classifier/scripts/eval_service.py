#!/usr/bin/env python3
"""Service-level eval wrapper — full pipeline in-process or via HTTP."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT.parent.parent))

from app.pipeline import classify  # noqa: E402


def classify_via_http(text: str, base_url: str) -> str:
    response = httpx.post(f"{base_url.rstrip('/')}/classify", json={"text": text}, timeout=15.0)
    response.raise_for_status()
    return response.json()["category"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    data = json.loads(Path(args.input).read_text())
    classifier_url = os.environ.get("CLASSIFIER_URL")

    if classifier_url:
        category = classify_via_http(data["input"], classifier_url)
    else:
        category = classify(data["input"])["category"]

    text = data["input"]
    tokens_in = max(40, len(text) * 3)
    tokens_out = 8
    cost = round(tokens_in * 0.000002 + tokens_out * 0.000006, 6)
    Path(args.output).write_text(json.dumps({
        "output": category,
        "usage": {"tokens_in": tokens_in, "tokens_out": tokens_out},
        "cost": cost,
    }))


if __name__ == "__main__":
    main()
