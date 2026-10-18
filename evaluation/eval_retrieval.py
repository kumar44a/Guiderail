"""Retrieval-only evaluation: Precision@K, Hit@K, MRR per corpus and split.

    python evaluation/eval_retrieval.py --corpus synthetic --split dev
"""

from __future__ import annotations

import argparse

from common import CORPORA, REPORTS, fresh_index, log_test_split_run, pct, write_json

from guiderail.evalkit import load_queries, retrieval_eval, validate_labels
from guiderail.retriever import Retriever


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("--corpus", choices=sorted(CORPORA), required=True)
    ap.add_argument("--split", choices=["dev", "test", "all"], default="dev")
    args = ap.parse_args()

    loaded = fresh_index(args.corpus)
    sha = loaded.manifest["hashes"]["index_sha256"]
    all_queries = load_queries(CORPORA[args.corpus]["queries"])
    problems = validate_labels(all_queries, loaded.chunks)
    if problems:
        print("LABEL PROBLEMS:\n  " + "\n  ".join(problems))
        return 2
    log_test_split_run(args.corpus, args.split, sha, "eval_retrieval")
    result = retrieval_eval(load_queries(CORPORA[args.corpus]["queries"], args.split), Retriever(loaded))
    write_json(REPORTS / f"retrieval_{args.corpus}_{args.split}.json", {"corpus": args.corpus, "split": args.split,
                                                                         "index_sha256": sha, **result})
    print(f"{args.corpus}/{args.split}: {result['n']} in-corpus queries")
    for k in (1, 5, 10):
        print(f"  Precision@{k:<2} {pct(result[f'precision@{k}']):>7}   Hit@{k:<2} {pct(result[f'hit@{k}']):>7}")
    print(f"  MRR {result['mrr']}")
    misses = [r for r in result["rows"] if not r["hit@10"]]
    if misses:
        print(f"  no fact-bearing chunk in top 10 for: {', '.join(r['id'] for r in misses)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
