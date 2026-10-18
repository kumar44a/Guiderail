"""Like-for-like effect of validator F1 on the answers already saved in the test-split reports (no new answers, no API calls).

    python evaluation/round2_test_effect.py        # writes evaluation/reports/validator_round2_test_effect.json

Held-out answers are only re-scored here, not regenerated. This is descriptive: the queries are exposed and carry no weight in the
accept decision, which was made on dev material before the new test queries were run.
"""

from __future__ import annotations

import json

from common import REPORTS
from revalidate import decision, load, revalidate_report

STEMS = ["synthetic_test_extractive_final", "synthetic_test_llm_final", "real_test_extractive_final", "real_test_llm_final"]


def main() -> int:
    out = {}
    for stem in STEMS:
        report = load(stem)
        t = report["threshold"]
        new = revalidate_report(report)
        old = {r["id"]: r for r in report["records"]}
        flips = [{"id": r["id"], "kind": r["kind"], "correct": r["correct"], "before": decision(old[r["id"]], t), "after": decision(r, t)}
                 for r in new if decision(old[r["id"]], t) != decision(r, t)]
        out[stem] = {"flips": flips,
                     "validated_before": sum(decision(r, t) for r in old.values() if r["kind"] == "in_corpus"),
                     "validated_after": sum(decision(r, t) for r in new if r["kind"] == "in_corpus"),
                     "wrong_validated_after": sum(decision(r, t) and not r["correct"] for r in new if r["kind"] == "in_corpus"),
                     "ooc_accepted_before": sum(decision(r, t) for r in old.values() if r["kind"] != "in_corpus"),
                     "ooc_accepted_after": sum(decision(r, t) for r in new if r["kind"] != "in_corpus")}
        print(stem, out[stem]["validated_before"], "->", out[stem]["validated_after"], "flips:", [(f["id"], f["correct"]) for f in flips])
    (REPORTS / "validator_round2_test_effect.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
