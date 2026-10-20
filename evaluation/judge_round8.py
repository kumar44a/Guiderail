"""Apply the keep rule of retrieval round 8 (evaluation/reports/retrieval_round8_rules.txt) to one candidate.

    python evaluation/judge_round8.py --step r8L05 --against r8base

Reads tagged extractive dev reports for synthetic2, synthetic and real. No API calls. Index hash identity (R7) is checked from the reports.
"""

from __future__ import annotations

import argparse
import json

from common import CORPORA, REPORTS
from guiderail.evalkit import load_queries

THRESHOLD = 0.6


def load(corpus: str, tag: str) -> dict:
    return json.loads((REPORTS / f"{corpus}_dev_extractive_{tag}.json").read_text(encoding="utf-8"))


def rows(rep): return {r["id"]: r for r in rep["retrieval"]["rows"]}


def hits(rep, keep=lambda i: True):
    sel = [r for i, r in rows(rep).items() if keep(i)]
    return sum(bool(r["hit@5"]) for r in sel), len(sel)


def errors(rep):
    ok = lambda r: r["confidence"] >= THRESHOLD and r["cited"]
    inc = [r for r in rep["records"] if r["kind"] == "in_corpus"]
    ooc = [r for r in rep["records"] if r["kind"] != "in_corpus"]
    return {"wrong_validated": sum(ok(r) and not r["correct"] for r in inc), "ooc_accepted": sum(ok(r) for r in ooc)}


def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("--step", required=True); ap.add_argument("--against", required=True)
    a = ap.parse_args()
    out, rules = {"step": a.step, "against": a.against}, {}
    b2, s2 = load("synthetic2", a.against), load("synthetic2", a.step)
    p_b, p_s = b2["retrieval"]["precision@5"], s2["retrieval"]["precision@5"]
    out["p5_synthetic2_dev"] = [round(p_b, 4), round(p_s, 4)]
    rules["R1"] = p_s - p_b >= 0.05 - 1e-9
    (hb, n), (hs, _) = hits(b2), hits(s2)
    out["synthetic2_dev"] = {"n": n, "hit5": [hb, hs], "mrr": [round(b2["retrieval"]["mrr"], 4), round(s2["retrieval"]["mrr"], 4)]}
    rules["R2"] = hs >= hb and s2["retrieval"]["mrr"] >= b2["retrieval"]["mrr"] - 0.01
    b1, s1 = load("synthetic", a.against), load("synthetic", a.step)
    (h1b, _), (h1s, n1) = hits(b1), hits(s1)
    out["synthetic_dev"] = {"n": n1, "hit5": [h1b, h1s], "mrr": [round(b1["retrieval"]["mrr"], 4), round(s1["retrieval"]["mrr"], 4)]}
    rules["R3"] = h1s >= h1b and s1["retrieval"]["mrr"] >= b1["retrieval"]["mrr"] - 0.01
    br, sr = load("real", a.against), load("real", a.step)
    (hrb, nr), (hrs, _) = hits(br), hits(sr)
    out["real_dev"] = {"n": nr, "hit5": [hrb, hrs], "mrr": [round(br["retrieval"]["mrr"], 4), round(sr["retrieval"]["mrr"], 4)]}
    rules["R4"] = hrs >= hrb - 1 and sr["retrieval"]["mrr"] >= br["retrieval"]["mrr"] - 0.01
    e = {k: (errors(x), errors(y)) for k, (x, y) in {"synthetic2": (b2, s2), "real": (br, sr)}.items()}
    out["errors"] = {k: [v[0], v[1]] for k, v in e.items()}
    rules["R5"] = all(v[1]["wrong_validated"] <= v[0]["wrong_validated"] and v[1]["ooc_accepted"] <= v[0]["ooc_accepted"] for v in e.values())
    qs = {q.id: q for q in load_queries(CORPORA["synthetic2"]["queries"], "dev")}
    multi = lambda i: i in qs and len(qs[i].relevant_docs) >= 2
    (mb, nm), (ms, _) = hits(b2, multi), hits(s2, multi)
    out["multi_doc"] = {"n": nm, "hit5": [mb, ms]}
    rules["R6"] = ms >= mb
    rules["R7_index_unchanged"] = all(x["index_sha256"] == y["index_sha256"] for x, y in ((b2, s2), (b1, s1), (br, sr)))
    out["rules"] = rules
    out["kept"] = all(rules.values())
    path = REPORTS / f"retrieval_round8_{a.step}.json"
    path.write_text(json.dumps(out, indent=1, sort_keys=True), encoding="utf-8")
    print(json.dumps(out, indent=1, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
