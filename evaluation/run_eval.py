"""Full evaluation: retrieval, answers, validation, threshold sweep, review list, summary.

    python evaluation/run_eval.py --corpus synthetic --split dev
    python evaluation/run_eval.py --corpus real --split dev
    python evaluation/run_eval.py --corpus synthetic --split test      # held-out; run after freezing changes

The index is rebuilt from source on every run. Runs that touch the test split are logged to
evaluation/reports/test_split_runs.log.
"""

from __future__ import annotations

import argparse

from common import CORPORA, REPORTS, fresh_index, log_test_split_run, render_summary, write_json

from guiderail import config
from guiderail.evalkit import (
    load_queries, retrieval_eval, review_list, run_qa, summarize, sweep, validate_labels, write_review_csv,
)
from guiderail.service import QAService


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("--corpus", choices=sorted(CORPORA), required=True)
    ap.add_argument("--split", choices=["dev", "test", "all", "sealed", "sealed2", "sealed3"], default="dev")
    ap.add_argument("--generator", choices=["extractive", "llm"], default="extractive")
    ap.add_argument("--threshold", type=float, default=config.DEFAULT_THRESHOLD)
    ap.add_argument("--rerank-weight", type=float, default=None,
                    help="lexical re-ranking weight (default: config, 0 = off)")
    ap.add_argument("--tag", default="", help="suffix for report file names, e.g. a change label")
    ap.add_argument("--rewrite-cache", default=None,
                    help="turn on query rewriting (API calls on cache misses) and read/write rewrites in this JSON file")
    args = ap.parse_args()

    loaded = fresh_index(args.corpus)
    sha = loaded.manifest["hashes"]["index_sha256"]
    queries = load_queries(CORPORA[args.corpus]["queries"], args.split)
    problems = validate_labels(load_queries(CORPORA[args.corpus]["queries"]), loaded.chunks)
    if problems:
        print("LABEL PROBLEMS:\n  " + "\n  ".join(problems))
        return 2
    log_test_split_run(args.corpus, args.split, sha, f"run_eval generator={args.generator}")

    generator = None
    if args.generator == "llm":
        config.load_env_file()
        from guiderail.generators.llm import LlmGenerator
        generator = LlmGenerator()
    rewriter = None
    if args.rewrite_cache:
        config.load_env_file()
        from guiderail.rewrite import QueryRewriter
        rewriter = QueryRewriter(cache_path=args.rewrite_cache)
    service = QAService(loaded, generator=generator, threshold=args.threshold, rerank_weight=args.rerank_weight, rewriter=rewriter)

    records = run_qa(queries, service)
    report = {
        "corpus": args.corpus, "split": args.split, "generator": service.generator.name,
        "threshold": args.threshold, "index_sha256": sha, "manifest_counts": loaded.manifest["counts"],
        "rerank_weight": service.retriever.rerank_weight,
        "retrieval": retrieval_eval(queries, service.retriever, rewriter=rewriter),
        "rewrite": bool(rewriter),
        "validation": summarize(records, args.threshold),
        "sweep": sweep(records),
        "review": review_list(records, args.threshold),
        "records": records,
    }
    stem = f"{args.corpus}_{args.split}_{service.generator.name}{('_' + args.tag) if args.tag else ''}"
    write_json(REPORTS / f"{stem}.json", report)
    (REPORTS / f"{stem}_summary.md").write_text(render_summary(report), encoding="utf-8")
    write_review_csv(REPORTS / f"{stem}_low_confidence.csv", report["review"])
    print(render_summary(report))
    print(f"\nWrote evaluation/reports/{stem}.json (+ _summary.md, _low_confidence.csv)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
