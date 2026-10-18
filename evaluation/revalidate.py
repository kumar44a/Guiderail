"""Re-run the CURRENT validator on the answers stored in saved reports (no generator, no API calls).

    python evaluation/revalidate.py --verify real_dev_extractive_final synthetic_dev_llm_final ...
    python evaluation/revalidate.py --compare real_dev_llm_final ...
    python evaluation/revalidate.py --write cur real_dev_llm_r2base ...    # saves real_dev_llm_cur.json (+ summary, review CSV)

Retrieval is deterministic, so the evidence for each stored answer can be rebuilt exactly. `--verify` checks that the
stored confidences are reproduced unchanged (use it before any validator change, to prove the tool is faithful).
`--compare` prints what changed after a validator change: per report, answers whose decision flipped.
Reports must have been produced on the current corpus build (the 3-document `final_3doc` reports cannot be revalidated).
"""

from __future__ import annotations

import argparse
import json

from common import CORPORA, REPORTS, fresh_index, render_summary, write_json

from guiderail.evalkit import answer_correct, load_queries, review_list, summarize, sweep, write_review_csv
from guiderail.retriever import top_retrieval_score
from guiderail.service import QAService
from guiderail.validator import validate

_SERVICES: dict[str, QAService] = {}


def service_for(corpus: str, threshold: float, rerank_weight: float) -> QAService:
    if corpus not in _SERVICES:
        _SERVICES[corpus] = QAService(fresh_index(corpus), threshold=threshold, rerank_weight=rerank_weight)
    return _SERVICES[corpus]


def revalidate_report(report: dict, top_k: int = 5) -> list[dict]:
    service = service_for(report["corpus"], report["threshold"], report["rerank_weight"])
    queries = {q.id: q for q in load_queries(CORPORA[report["corpus"]]["queries"])}
    out = []
    for r in report["records"]:
        hits = service.retriever.expand_sparse(service.retriever.search(r["question"], top_k))
        by_id = {h.chunk.chunk_id: h for h in hits}
        cited_hits = [by_id[i] for i in r["citations"] if i in by_id]
        v = validate(question=r["question"], answer=r["answer"], evidence=[h.chunk for h in hits],
                     top_score=top_retrieval_score(hits), lexicon=service.lexicon, threshold=report["threshold"],
                     abstained=r["abstained"], cited=r["cited"], cited_chunks=[h.chunk for h in cited_hits])
        q = queries[r["id"]]
        out.append({**r, "confidence": v.confidence, "validation": v.to_dict(),
                    "correct": answer_correct(r["answer"], q) if q.kind == "in_corpus" else None})
    return out


def load(stem: str) -> dict:
    return json.loads((REPORTS / f"{stem}.json").read_text(encoding="utf-8"))


def decision(r: dict, threshold: float) -> bool:
    return r["confidence"] >= threshold and r["cited"]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("stems", nargs="+")
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--verify", action="store_true")
    mode.add_argument("--compare", action="store_true")
    mode.add_argument("--write", metavar="TAG", help="save a re-scored copy of each report under this tag")
    args = ap.parse_args()

    bad = 0
    for stem in args.stems:
        report = load(stem)
        new = revalidate_report(report)
        old_by_id = {r["id"]: r for r in report["records"]}
        t = report["threshold"]
        if args.write:
            out_stem = stem.rsplit("_", 1)[0] + f"_{args.write}"
            copy = {**report, "records": new, "validation": summarize(new, t), "sweep": sweep(new), "review": review_list(new, t),
                    "revalidated_from": stem, "note": "answers are the stored ones; confidences recomputed with the current validator"}
            write_json(REPORTS / f"{out_stem}.json", copy)
            (REPORTS / f"{out_stem}_summary.md").write_text(render_summary(copy), encoding="utf-8")
            write_review_csv(REPORTS / f"{out_stem}_low_confidence.csv", copy["review"])
            print(f"wrote {out_stem}.json")
        elif args.verify:
            diffs = [r["id"] for r in new if abs(r["confidence"] - old_by_id[r["id"]]["confidence"]) > 1e-9]
            print(f"{stem}: {len(new)} records, {'REPRODUCED' if not diffs else 'MISMATCH ' + str(diffs)}")
            bad += bool(diffs)
        else:
            flips = [(r["id"], old_by_id[r["id"]]["confidence"], r["confidence"], decision(old_by_id[r["id"]], t), decision(r, t), r["correct"])
                     for r in new if decision(old_by_id[r["id"]], t) != decision(r, t) or abs(r["confidence"] - old_by_id[r["id"]]["confidence"]) > 1e-9]
            print(f"{stem}: {len(flips)} confidence changes")
            for i, a, b, da, db, ok in flips:
                print(f"    {i}: {a:.3f} -> {b:.3f}  {'validated' if da else 'review'} -> {'validated' if db else 'review'}  correct={ok}")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
