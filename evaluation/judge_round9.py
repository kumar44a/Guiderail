"""Apply the keep rule of retrieval round 9 (evaluation/reports/retrieval_round9_rules.txt) to one Claude candidate.

    python evaluation/judge_round9.py --step r9K1 --against cur --against r9base2

Reads tagged Claude dev reports for real and synthetic. No API calls. Rejects (exit 2) any report that contains generator errors.
"""

from __future__ import annotations

import argparse
import json
import sys

from common import REPORTS

T = 0.6


def load(corpus: str, tag: str) -> dict:
    rep = json.loads((REPORTS / f"{corpus}_dev_llm_{tag}.json").read_text(encoding="utf-8"))
    bad = sum(bool(r.get("generator_error")) for r in rep["records"])
    if bad:
        print(f"DISCARD: {corpus} {tag} has {bad} generator errors", file=sys.stderr)
        raise SystemExit(2)
    return rep


def stats(rep: dict) -> dict:
    ok = lambda r: r["confidence"] >= T and r["cited"]
    inc = [r for r in rep["records"] if r["kind"] == "in_corpus"]
    ooc = [r for r in rep["records"] if r["kind"] != "in_corpus"]
    val = [r for r in inc if ok(r)]
    wrong = sum(not r["correct"] for r in val)
    return {"n": len(inc), "pass": len(val), "wrong_validated": wrong, "ooc_accepted": sum(ok(r) for r in ooc),
            "val_precision": round((len(val) - wrong) / len(val), 4) if val else None}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--step", required=True)
    ap.add_argument("--against", action="append", required=True)
    a = ap.parse_args()
    out = {"step": a.step, "against": a.against, "rules": {}}
    new_r, new_s = stats(load("real", a.step)), stats(load("synthetic", a.step))
    out["candidate"] = {"real": new_r, "synthetic": new_s}
    q1 = q2 = q3 = q4 = True
    out["baselines"] = {}
    for b in a.against:
        br, bs = stats(load("real", b)), stats(load("synthetic", b))
        out["baselines"][b] = {"real": br, "synthetic": bs}
        q1 &= new_r["pass"] - br["pass"] >= 2
        q2 &= new_r["wrong_validated"] - br["wrong_validated"] <= 1 and new_r["val_precision"] >= br["val_precision"] - 0.02
        q3 &= new_r["ooc_accepted"] <= br["ooc_accepted"] and new_s["ooc_accepted"] <= bs["ooc_accepted"]
        q4 &= new_s["pass"] >= bs["pass"] - 1
    out["rules"] = {"Q1": q1, "Q2": q2, "Q3": q3, "Q4": q4, "Q5": True}
    out["kept"] = all(out["rules"].values())
    (REPORTS / f"retrieval_round9_{a.step}.json").write_text(json.dumps(out, indent=1, sort_keys=True), encoding="utf-8")
    print(json.dumps(out, indent=1, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
