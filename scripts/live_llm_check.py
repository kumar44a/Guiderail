"""Run the LLM generator against the real API on a few questions and log the evidence.

    python scripts/live_llm_check.py                 # uses ./index and the key in .env
    python scripts/live_llm_check.py --out evaluation/logs/live_llm_run.json

This makes a handful of paid API calls. The log records the model, request ids, token
usage, answers and validator decisions. It never records the API key.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from guiderail import config  # noqa: E402
from guiderail.generators.llm import LlmGenerator  # noqa: E402
from guiderail.index import load_index  # noqa: E402
from guiderail.service import QAService  # noqa: E402

QUESTIONS = [
    ("in_corpus", "What temperature should refrigerated vaccines be stored at?"),
    ("in_corpus", "In what order should PPE be taken off?"),
    ("in_corpus", "When can healthcare staff return to work after a respiratory illness?"),
    ("in_corpus", "How long should alcohol-based hand rub be applied?"),
    ("out_of_corpus", "How do I bake a chocolate cake?"),
    ("out_of_corpus", "What is the recommended dose of amoxicillin for otitis media?"),
]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--index", type=Path, default=config.index_dir())
    parser.add_argument("--out", type=Path, default=ROOT / "evaluation" / "logs" / "live_llm_run.json")
    args = parser.parse_args()

    config.load_env_file()
    generator = LlmGenerator()
    service = QAService(load_index(args.index), generator=generator)

    runs = []
    for kind, question in QUESTIONS:
        started = time.time()
        result = service.ask(question, top_k=5)
        runs.append({
            "kind": kind,
            "question": question,
            "answer": result.answer,
            "status": result.status,
            "confidence": result.confidence,
            "citations": [c["chunk_id"] for c in result.citations],
            "validation": result.debug["validation"],
            "generator_error": result.debug.get("generator_error"),
            "request_id": generator.last_request_id,
            "response_model": generator.last_model,
            "usage": generator.last_usage,
            "seconds": round(time.time() - started, 2),
        })
        print(f"[{result.status:12} {result.confidence:.3f}] {question}\n    {result.answer[:200]}")

    log = {
        "run_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "requested_model": generator.model,
        "index_sha256": service.loaded.manifest["hashes"]["index_sha256"],
        "fallbacks_enabled": generator.use_fallbacks,
        "runs": runs,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(log, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    errors = [r for r in runs if r["generator_error"]]
    print(f"\nWrote {args.out} ({len(runs)} questions, {len(errors)} generator errors)")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
