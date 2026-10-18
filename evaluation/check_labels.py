"""Check that every labeled query is consistent with its corpus (documents exist, expected facts are
actually present in the relevant documents). Run after editing a query file or changing the loader.

    python evaluation/check_labels.py
"""

from __future__ import annotations

from common import CORPORA, fresh_index

from guiderail.evalkit import load_queries, validate_labels


def main() -> int:
    bad = 0
    for corpus, cfg in CORPORA.items():
        if corpus == "real" and not (cfg["dir"] / "sources.json").exists():
            print(f"{corpus}: skipped (no sources.json)")
            continue
        queries = load_queries(cfg["queries"])
        problems = validate_labels(queries, fresh_index(corpus).chunks)
        print(f"{corpus}: {len(queries)} queries, {len(problems)} problems")
        for p in problems:
            print("   ", p)
        bad += len(problems)
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
