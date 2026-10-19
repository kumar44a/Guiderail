"""Apply the keep rule of retrieval round 3 (evaluation/reports/retrieval_round3_rules.txt) to one step.

    python evaluation/judge_round3.py --step r3A --against r3base [--determinism]

Reads the tagged extractive dev reports for the synthetic and real corpora and the stress report. No API calls.
Keep rule: real-dev Hit@5 rises by >= 1 query or MRR by >= 0.02 with no fall in Hit@5, and guards G1-G5 hold.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys

from common import REPORTS, ROOT

THRESHOLD = 0.6


def load(corpus: str, tag: str) -> dict:
    return json.loads((REPORTS / f"{corpus}_dev_extractive_{tag}.json").read_text(encoding="utf-8"))


def rows(report: dict) -> dict:
    return {r["id"]: r for r in report["retrieval"]["rows"]}


def hit5(report: dict, keep=lambda i: True) -> tuple[int, int]:
    sel = [r for i, r in rows(report).items() if keep(i)]
    return sum(bool(r["hit@5"]) for r in sel), len(sel)


def errors(report: dict) -> dict:
    ok = lambda r: r["confidence"] >= THRESHOLD and r["cited"]
    inc = [r for r in report["records"] if r["kind"] == "in_corpus"]
    ooc = [r for r in report["records"] if r["kind"] != "in_corpus"]
    return {"wrong_validated": sum(ok(r) and not r["correct"] for r in inc), "ooc_accepted": sum(ok(r) for r in ooc),
            "correct_validated": sum(ok(r) and bool(r["correct"]) for r in inc)}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--step", required=True)
    ap.add_argument("--against", required=True)
    ap.add_argument("--determinism", action="store_true")
    ap.add_argument("--min-queries", type=int, default=1, help="gain bar: real-dev Hit@5 must rise by this many queries ...")
    ap.add_argument("--min-mrr", type=float, default=0.02, help="... or MRR by this much (round 5 uses 3 and 0.03)")
    ap.add_argument("--retrieval-only", action="store_true", help="skip the extractive error guards G3 and G4 (round 5 step 1)")
    args = ap.parse_args()

    out, ok = {"step": args.step, "against": args.against}, True
    rb, rs = load("real", args.against), load("real", args.step)
    sb, ss = load("synthetic", args.against), load("synthetic", args.step)
    old = lambda i: not i.startswith("N")          # real dev queries that existed before the natural-wording set
    (hb, n), (hs, _) = hit5(rb), hit5(rs)
    mrr_b, mrr_s = rb["retrieval"]["mrr"], rs["retrieval"]["mrr"]
    out["real_dev"] = {"n": n, "hit5_before": hb, "hit5_after": hs, "mrr_before": round(mrr_b, 4), "mrr_after": round(mrr_s, 4)}
    gain = (hs - hb >= args.min_queries or mrr_s - mrr_b >= args.min_mrr) and hs >= hb
    g1 = hit5(ss)[0] >= hit5(sb)[0] and ss["retrieval"]["mrr"] >= sb["retrieval"]["mrr"] - 0.01
    g2 = hit5(rs, old)[0] >= hit5(rb, old)[0]
    eb = {c: errors(r) for c, r in (("real", rb), ("synthetic", sb))}
    es = {c: errors(r) for c, r in (("real", rs), ("synthetic", ss))}
    g3 = all(es[c]["wrong_validated"] <= eb[c]["wrong_validated"] and es[c]["ooc_accepted"] <= eb[c]["ooc_accepted"] for c in es)
    stb = json.loads((REPORTS / f"validator_stress_{args.against}.json").read_text(encoding="utf-8"))
    sts = json.loads((REPORTS / f"validator_stress_{args.step}.json").read_text(encoding="utf-8"))
    g4 = (sts["bad_answers_flagged_rate"] >= stb["bad_answers_flagged_rate"] and sts["good_answers_accepted_rate"] >= stb["good_answers_accepted_rate"])
    g5 = None
    if args.determinism:
        g5 = True
        for flags in ([], ["--real"]):
            r = subprocess.run([sys.executable, str(ROOT / "scripts" / "pipeline.py"), "--check-determinism", *flags,
                                "--out", str(REPORTS / "_tmp_index")], capture_output=True, text=True)
            g5 &= r.returncode == 0
    out["synthetic_dev"] = {"hit5": [hit5(sb)[0], hit5(ss)[0], hit5(ss)[1]], "mrr": [round(sb["retrieval"]["mrr"], 4), round(ss["retrieval"]["mrr"], 4)]}
    out["real_dev_old_queries_hit5"] = [hit5(rb, old)[0], hit5(rs, old)[0], hit5(rs, old)[1]]
    out["errors_before"], out["errors_after"] = eb, es
    out["stress"] = {"bad_flagged": [stb["bad_answers_flagged_rate"], sts["bad_answers_flagged_rate"]],
                     "good_accepted": [stb["good_answers_accepted_rate"], sts["good_answers_accepted_rate"]]}
    if args.retrieval_only:
        g3 = g4 = True
    out["rules"] = {"gain": gain, "G1": g1, "G2": g2, "G3": g3, "G4": g4, "G5": g5}
    out["keep"] = bool(gain and g1 and g2 and g3 and g4 and g5 is not False)
    (REPORTS / f"retrieval_round3_{args.step}.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))
    print("=> KEEP" if out["keep"] else "=> REVERT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
