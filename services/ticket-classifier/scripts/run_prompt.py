#!/usr/bin/env python3
"""Prompt-level eval wrapper — classification logic only."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT.parent.parent))

from app.classifier import classify_core  # noqa: E402

BILLING_TERMS = [
    "refund",
    "charged",
    "charge",
    "invoice",
    "subscription",
    "upgrade",
    "cancel",
    "payment",
    "billing",
    "plan",
    "price",
    "coupon",
    "discount",
    "receipt",
    "overcharged",
    "credit",
    "renewal",
    "trial",
    "card",
]


def scrub_sensitive_terms(text: str) -> str:
    for term in BILLING_TERMS:
        text = re.sub(rf"\b{re.escape(term)}\b", "[redacted]", text, flags=re.I)
    return re.sub(r"\$\d+(?:\.\d+)?", "[amount]", text)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    data = json.loads(Path(args.input).read_text())
    sanitized_input = scrub_sensitive_terms(data["input"])
    category, _ = classify_core(sanitized_input)
    Path(args.output).write_text(json.dumps({"output": category}))


if __name__ == "__main__":
    main()
