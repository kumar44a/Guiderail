"""Stress-test the validator with hand-written good and bad answers it did not generate.

    python evaluation/eval_validator_stress.py

Bad answers (fabricated numbers, wrong claims, unrelated text, off-corpus fabrications) should be
sent to review; good answers should be validated. Known-hard cases are labelled in the file's
`note` field and are reported, not hidden.
"""

from __future__ import annotations

import argparse

from common import REPORTS, ROOT, fresh_index, pct, write_json

from guiderail import config
from guiderail.evalkit import load_stress, stress_eval
from guiderail.service import QAService


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("--threshold", type=float, default=config.DEFAULT_THRESHOLD)
    ap.add_argument("--tag", default="")
    args = ap.parse_args()

    cases = load_stress(ROOT / "evaluation" / "validator_stress.jsonl")
    needed = sorted({c["corpus"] for c in cases})
    services = {corpus: QAService(fresh_index(corpus), threshold=args.threshold) for corpus in needed}
    result = stress_eval(cases, services, args.threshold)
    write_json(REPORTS / f"validator_stress{('_' + args.tag) if args.tag else ''}.json", result)

    print(f"Validator stress test, threshold {args.threshold}, {result['n']} cases")
    print(f"  bad answers sent to review : {pct(result['bad_answers_flagged_rate'])}")
    print(f"  good answers validated     : {pct(result['good_answers_accepted_rate'])}")
    for kind, v in result["by_kind"].items():
        print(f"    {kind:<24} {v['correct_decisions']}/{v['n']}")
    print("  wrong decisions:")
    for r in result["rows"]:
        if not r["caught"]:
            print(f"    {r['id']} [{r['label']}/{r['kind']}] conf={r['confidence']} {r['note']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
