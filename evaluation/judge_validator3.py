"""Apply the keep rules of validator round 3 (evaluation/reports/validator_round3_rules.txt), fix by fix, to saved dev answers.

    python evaluation/judge_validator3.py

Fixes V1, V2, V3 are judged cumulatively in that order; a fix that fails is left out of the later comparisons. No API calls.
Rules per fix: A no report gains wrong-but-validated answers or out-of-scope accepts; B the stress set is not worse; C at least one withheld correct
answer is validated.
"""

from __future__ import annotations

import json

from common import REPORTS, ROOT, fresh_index
from revalidate import decision, load, revalidate_report

from guiderail import validator
from guiderail.evalkit import load_stress, stress_eval
from guiderail.service import QAService

STEMS = ["real_dev_extractive_r3B", "synthetic_dev_extractive_r3B", "real_dev_llm_r5Lbase", "synthetic_dev_llm_r5Lbase"]
FIXES = [("V1", "GATE_QUANTITY_UNITS"), ("V2", "FOOTNOTE_DECIMALS"), ("V3", "CITED_TEXT_SUPPORT")]


def measure() -> dict:
    out = {}
    for stem in STEMS:
        report = load(stem)
        t = report["threshold"]
        recs = revalidate_report(report)
        inc = [r for r in recs if r["kind"] == "in_corpus"]
        ooc = [r for r in recs if r["kind"] != "in_corpus"]
        out[stem] = {"wrong_validated": sorted(r["id"] for r in inc if decision(r, t) and not r["correct"]),
                     "ooc_accepted": sorted(r["id"] for r in ooc if decision(r, t)),
                     "validated_correct": sorted(r["id"] for r in inc if decision(r, t) and r["correct"]),
                     "withheld_correct": sorted(r["id"] for r in inc if not decision(r, t) and r["correct"])}
    cases = load_stress(ROOT / "evaluation" / "validator_stress.jsonl")
    services = {c: QAService(fresh_index(c), threshold=0.6) for c in sorted({x["corpus"] for x in cases})}
    s = stress_eval(cases, services, 0.6)
    out["stress"] = {"bad_flagged": s["bad_answers_flagged_rate"], "good_accepted": s["good_answers_accepted_rate"],
                     "caught": {r["id"]: r["caught"] for r in s["rows"]}}
    return out


def set_flags(active: set[str]) -> None:
    for _, flag in FIXES:
        setattr(validator, flag, flag in active)


def main() -> int:
    kept: set[str] = set()
    set_flags(kept)
    state = measure()
    result = {"baseline": state, "fixes": {}}
    print("baseline withheld correct:", {s: len(state[s]["withheld_correct"]) for s in STEMS},
          "wrong validated:", {s: len(state[s]["wrong_validated"]) for s in STEMS})
    for name, flag in FIXES:
        set_flags(kept | {flag})
        after = measure()
        a = all(len(after[s]["wrong_validated"]) <= len(state[s]["wrong_validated"]) and
                len(after[s]["ooc_accepted"]) <= len(state[s]["ooc_accepted"]) for s in STEMS)
        broke = sorted(i for i, c in state["stress"]["caught"].items() if c and not after["stress"]["caught"][i])
        b = not broke and after["stress"]["bad_flagged"] >= state["stress"]["bad_flagged"]
        released = {s: sorted(set(state[s]["withheld_correct"]) & set(after[s]["validated_correct"])) for s in STEMS}
        c = any(released.values())
        new_wrong = {s: sorted(set(after[s]["wrong_validated"]) - set(state[s]["wrong_validated"])) for s in STEMS}
        keep = a and b and c
        result["fixes"][name] = {"rules": {"A": a, "B": b, "C": c}, "kept": keep, "released_correct": released,
                                 "new_wrong_validated": new_wrong, "stress_broke": broke,
                                 "stress": {"bad_flagged": [state["stress"]["bad_flagged"], after["stress"]["bad_flagged"]],
                                            "good_accepted": [state["stress"]["good_accepted"], after["stress"]["good_accepted"]]}}
        print(f"\n{name}: A={a} B={b} C={c} -> {'KEEP' if keep else 'REVERT'}")
        print("   released correct:", {s: v for s, v in released.items() if v})
        print("   new wrong-validated:", {s: v for s, v in new_wrong.items() if v}, " stress broke:", broke,
              " stress bad/good:", result["fixes"][name]["stress"])
        if keep:
            kept.add(flag)
            state = after
    result["kept"] = sorted(f for n, f in FIXES if f in kept)
    set_flags(set())
    (REPORTS / "validator_round3.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print("\nkept:", result["kept"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
