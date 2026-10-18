"""Re-score a saved report's stored answers against the CURRENT labels and matching rules.

    python evaluation/rescore.py synthetic_dev_llm_llm_v1 real_dev_llm_llm_v1

Lets older runs be compared fairly after a scoring fix, without repeating paid API calls.
Prints the headline numbers; does not overwrite the report.
"""

from __future__ import annotations

import json
import sys

from common import CORPORA, REPORTS

from guiderail.evalkit import answer_correct, load_queries, summarize


def rescore(stem: str) -> dict:
    report = json.loads((REPORTS / f"{stem}.json").read_text(encoding="utf-8"))
    queries = {q.id: q for q in load_queries(CORPORA[report["corpus"]]["queries"])}
    for r in report["records"]:
        q = queries[r["id"]]
        r["correct"] = answer_correct(r["answer"], q) if q.kind == "in_corpus" else None
    return summarize(report["records"], report["threshold"])


def main() -> int:
    for stem in sys.argv[1:]:
        s = rescore(stem)
        ic, oc = s["in_corpus"], s["out_of_corpus"]
        print(f"{stem}: correct={ic['answer_correct_rate']} pass={ic['pass_rate']} valid_precision={ic['validated_precision']} "
              f"wrong_validated={ic['validated_but_wrong_rate']} correct_flagged={ic['correct_but_flagged_rate']} "
              f"ooc_false_accept={oc['false_accept_rate']} decision_acc={s['decision_accuracy']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
