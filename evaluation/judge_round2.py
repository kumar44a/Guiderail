"""Apply the accept rules of validator round 2 (evaluation/reports/validator_round2_rules.txt) to DEV material.

    python evaluation/judge_round2.py

Rule A: no (report) has more wrong-but-validated answers or out-of-scope false accepts after F1 than before.
Rule B: no stress case decided correctly before is decided wrongly after, and the bad-answer flag rate does not fall.
Rule C: at least one correct, previously withheld answer is validated after F1.
"Before" is the validator with the yes/no marker switched off; "after" is the current validator. No API calls.
"""

from __future__ import annotations

import json
import re

from common import REPORTS, ROOT, fresh_index
from revalidate import decision, load, revalidate_report

from guiderail import validator
from guiderail.evalkit import load_stress, stress_eval
from guiderail.service import QAService

DEV_STEMS = ["synthetic_dev_extractive_final", "synthetic_dev_llm_final", "real_dev_extractive_final", "real_dev_llm_final",
             "real_dev_extractive_r2base", "real_dev_llm_r2base"]
NEVER = re.compile(r"(?!x)x")
MARKER = validator._RESPONSE_MARKER


def tally(records: list[dict], threshold: float) -> dict:
    inc = [r for r in records if r["kind"] == "in_corpus"]
    ooc = [r for r in records if r["kind"] != "in_corpus"]
    return {"validated_wrong": sorted(r["id"] for r in inc if decision(r, threshold) and not r["correct"]),
            "ooc_accepted": sorted(r["id"] for r in ooc if decision(r, threshold)),
            "released": sorted(r["id"] for r in inc if r["correct"]),   # filled below
            "validated": sorted(r["id"] for r in inc if decision(r, threshold))}


def run_all(enabled: bool) -> dict:
    validator._RESPONSE_MARKER = MARKER if enabled else NEVER
    out = {}
    for stem in DEV_STEMS:
        report = load(stem)
        out[stem] = revalidate_report(report), report["threshold"]
    cases = load_stress(ROOT / "evaluation" / "validator_stress.jsonl")
    services = {c: QAService(fresh_index(c), threshold=0.6) for c in sorted({x["corpus"] for x in cases})}
    out["stress"] = stress_eval(cases, services, 0.6)
    return out


def main() -> int:
    before, after = run_all(False), run_all(True)
    validator._RESPONSE_MARKER = MARKER
    verdict = {"A": True, "B": True, "C": False}
    result = {"reports": {}}
    for stem in DEV_STEMS:
        (rb, t), (ra, _) = before[stem], after[stem]
        b, a = tally(rb, t), tally(ra, t)
        newly_released = sorted(x["id"] for x, y in zip(rb, ra)
                                if x["kind"] == "in_corpus" and x["correct"] and not decision(x, t) and decision(y, t))
        newly_withheld = sorted(x["id"] for x, y in zip(rb, ra) if x["kind"] == "in_corpus" and decision(x, t) and not decision(y, t))
        worse = (len(a["validated_wrong"]) > len(b["validated_wrong"])) or (len(a["ooc_accepted"]) > len(b["ooc_accepted"]))
        verdict["A"] &= not worse
        verdict["C"] |= bool(newly_released)
        result["reports"][stem] = {"before": {k: b[k] for k in ("validated_wrong", "ooc_accepted")},
                                   "after": {k: a[k] for k in ("validated_wrong", "ooc_accepted")},
                                   "released_correct": newly_released, "newly_withheld": newly_withheld, "rule_A_violated": worse}
        print(f"{stem}: wrong-validated {len(b['validated_wrong'])}->{len(a['validated_wrong'])}  ooc-accepted {len(b['ooc_accepted'])}->{len(a['ooc_accepted'])}"
              f"  released correct {newly_released}  newly withheld {newly_withheld}")
    sb, sa = before["stress"], after["stress"]
    caught_b = {r["id"]: r["caught"] for r in sb["rows"]}
    caught_a = {r["id"]: r["caught"] for r in sa["rows"]}
    broke = sorted(i for i in caught_b if caught_b[i] and not caught_a[i])
    fixed = sorted(i for i in caught_b if not caught_b[i] and caught_a[i])
    verdict["B"] = not broke and sa["bad_answers_flagged_rate"] >= sb["bad_answers_flagged_rate"]
    result["stress"] = {"bad_flagged_before": sb["bad_answers_flagged_rate"], "bad_flagged_after": sa["bad_answers_flagged_rate"],
                        "good_accepted_before": sb["good_answers_accepted_rate"], "good_accepted_after": sa["good_answers_accepted_rate"],
                        "broke": broke, "fixed": fixed}
    print(f"stress: bad flagged {sb['bad_answers_flagged_rate']} -> {sa['bad_answers_flagged_rate']}; good accepted "
          f"{sb['good_answers_accepted_rate']} -> {sa['good_answers_accepted_rate']}; broke {broke}; fixed {fixed}")
    result["verdict"] = {k: bool(v) for k, v in verdict.items()}
    result["accepted"] = all(verdict.values())
    (REPORTS / "validator_round2_dev.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print("rules:", result["verdict"], "=> F1", "ACCEPTED" if result["accepted"] else "REJECTED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
