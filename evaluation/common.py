"""Shared plumbing for the evaluation scripts (paths, fresh index build, report writing)."""

from __future__ import annotations

import json
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from guiderail.index import load_index  # noqa: E402
from pipeline import build  # noqa: E402

REPORTS = ROOT / "evaluation" / "reports"
CORPORA = {
    "synthetic": {"dir": ROOT / "data" / "guidelines", "loader": "markdown", "queries": ROOT / "evaluation" / "queries_synthetic.jsonl"},
    "synthetic2": {"dir": ROOT / "data" / "guidelines_v2", "loader": "markdown", "queries": ROOT / "evaluation" / "queries_synthetic2.jsonl"},
    "real": {"dir": ROOT / "data" / "real", "loader": "pdf", "queries": ROOT / "evaluation" / "queries_real.jsonl"},
}
TEST_LOG = REPORTS / "test_split_runs.log"


def fresh_index(corpus: str, keep: Path | None = None):
    """Build the corpus index from source into a temp dir and load it. Never reuses a stale index."""
    cfg = CORPORA[corpus]
    target = keep or Path(tempfile.mkdtemp(prefix=f"guiderail-{corpus}-"))
    build(cfg["dir"], target, loader=cfg["loader"])
    return load_index(target)


def log_test_split_run(corpus: str, split: str, index_sha: str, what: str) -> None:
    """Every run that touches the held-out test split is recorded, so peeking is visible."""
    if split not in ("test", "all", "sealed", "sealed2", "sealed3", "sealed4", "final"):
        return
    REPORTS.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with TEST_LOG.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(f"{stamp}\tsplit={split}\tcorpus={corpus}\tindex={index_sha[:12]}\t{what}\n")


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def pct(x) -> str:
    return "n/a" if x is None else f"{100 * x:.1f}%"


def render_summary(report: dict) -> str:
    r, v = report["retrieval"], report["validation"]
    ic, oc = v["in_corpus"], v["out_of_corpus"]
    lines = [
        f"# Evaluation summary: {report['corpus']} corpus, {report['split']} split",
        "",
        f"- Index: `{report['index_sha256'][:16]}…`  |  generator: `{report['generator']}`  |  threshold: {report['threshold']}",
        f"- Queries: {ic['n']} in-corpus, {oc['n']} out-of-corpus",
        "",
        "## Retrieval (in-corpus queries)",
        "",
        "| Metric | Value |", "|---|---|",
        *[f"| Precision@{k} (document level) | {pct(r[f'precision@{k}'])} |" for k in (1, 5, 10)],
        *[f"| Capped Precision@{k} (vs. best attainable) | {pct(r[f'capped_precision@{k}'])} |" for k in (1, 5, 10)],
        *[f"| Hit@{k} (a chunk containing the expected fact) | {pct(r[f'hit@{k}'])} |" for k in (1, 5, 10)],
        f"| MRR (first fact-bearing chunk) | {r['mrr']} |",
        "",
        "## Answers and validation",
        "",
        "| Metric | Value |", "|---|---|",
        f"| Pass rate (validated / in-corpus) | {pct(ic['pass_rate'])} |",
        f"| Mean confidence (in-corpus) | {ic['mean_confidence']} |",
        f"| Answer correct (expected facts present) | {pct(ic['answer_correct_rate'])} |",
        f"| **Validated precision** (correct among validated) | {pct(ic['validated_precision'])} |",
        f"| **Validated but wrong** | {pct(ic['validated_but_wrong_rate'])} |",
        f"| Correct but flagged for review | {pct(ic['correct_but_flagged_rate'])} |",
        f"| Out-of-corpus sent to review | {pct(oc['needs_review_rate'])} |",
        f"| Out-of-corpus falsely validated | {pct(oc['false_accept_rate'])} |",
        f"| Decision accuracy (all queries) | {pct(v['decision_accuracy'])} |",
        "",
        "A high pass rate alone is not evidence of quality: an extractive answer is copied from the evidence, so "
        "coverage is near-perfect by construction. Validated precision and the validated-but-wrong rate are the "
        "meaningful numbers.",
        "",
        "## Threshold sweep",
        "",
        "| Threshold | Pass rate | Validated precision | Validated but wrong | Correct but flagged | OOC false accept | Decision accuracy |",
        "|---|---|---|---|---|---|---|",
        *[f"| {s['threshold']} | {pct(s['pass_rate'])} | {pct(s['validated_precision'])} | {pct(s['validated_but_wrong_rate'])} | "
          f"{pct(s['correct_but_flagged_rate'])} | {pct(s['ooc_false_accept_rate'])} | {pct(s['decision_accuracy'])} |"
          for s in report["sweep"]],
        "",
        f"## Items for analyst review ({len(report['review'])})",
        "",
        *[f"- **{x['id']}** ({x['reason']}, confidence {x['confidence']}): {x['question']}" for x in report["review"]],
        "",
    ]
    return "\n".join(lines)
