"""Evaluation logic: labeled queries, retrieval metrics, answer-correctness, validation metrics.

Labels per in-corpus query:
  relevant_docs  documents that legitimately answer it (latest versions only)
  facts          list of groups; a group is satisfied if ANY alternative appears (case/space/dash
                 normalised). An answer is correct when ALL groups are satisfied and no
                 `forbidden` string appears (forbidden = a value from a superseded version).
Out-of-corpus queries have no labels; the right behaviour is to abstain / needs_review.

Two retrieval notions are reported because they answer different questions:
  Precision@K   share of the top-K chunks that come from a relevant document (the brief's metric;
                easy to inflate when a document has many chunks).
  Hit@K / MRR   whether, and how early, a chunk that actually contains an expected fact appears.
"""

from __future__ import annotations

import csv
import json
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path

from .generators import ABSTAIN_TEXT
from .models import Chunk
from .retriever import Retriever
from .text import tokenize
from .service import QAService

KINDS = ("in_corpus", "out_of_corpus")
SPLITS = ("dev", "test", "sealed", "sealed2", "sealed3", "sealed4")
DEFAULT_KS = (1, 5, 10)
DEFAULT_SWEEP = tuple(round(0.3 + 0.05 * i, 2) for i in range(13))   # 0.30 .. 0.90


@dataclass(frozen=True)
class Query:
    id: str
    question: str
    kind: str
    split: str
    relevant_docs: tuple[str, ...]
    facts: tuple[tuple[str, ...], ...]
    forbidden: tuple[str, ...]
    note: str = ""


def load_queries(path: Path | str, split: str | None = None) -> list[Query]:
    queries = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        queries.append(Query(
            id=r["id"], question=r["question"], kind=r["kind"], split=r["split"],
            relevant_docs=tuple(r.get("relevant_docs", [])),
            facts=tuple(tuple(group) for group in r.get("facts", [])),
            forbidden=tuple(r.get("forbidden", [])), note=r.get("note", "")))
    if split == "all":
        queries = [q for q in queries if q.split not in ("sealed", "sealed2", "sealed3", "sealed4")]   # the sealed set is only ever run by asking for it by name
    elif split:
        queries = [q for q in queries if q.split == split]
    return queries


def norm(text: str) -> str:
    text = unicodedata.normalize("NFKC", text).lower()
    text = re.sub(r"[‐‑‒–—−]", "-", text)
    text = text.replace("“", '"').replace("”", '"').replace("’", "'")
    return " ".join(text.split())


def _contains_tokens(haystack: list[str], needle: list[str]) -> bool:
    n = len(needle)
    return n > 0 and any(haystack[i : i + n] == needle for i in range(len(haystack) - n + 1))


def phrase_in(text: str, phrase: str) -> bool:
    """Exact (normalised) substring, or the same stemmed word sequence ("acts" matches "act").
    Stopwords are kept, so "do not wear" is not satisfied by "wear" alone."""
    if norm(phrase) in norm(text):
        return True
    return _contains_tokens(tokenize(text, drop_stopwords=False), tokenize(phrase, drop_stopwords=False))


def group_satisfied(text_norm: str, group: tuple[str, ...]) -> bool:
    return any(phrase_in(text_norm, alt) for alt in group)


def answer_correct(answer: str, q: Query) -> bool:
    return (all(group_satisfied(answer, g) for g in q.facts)
            and not any(phrase_in(answer, f) for f in q.forbidden))


def is_answer_bearing(chunk: Chunk, q: Query) -> bool:
    """Chunk of a relevant document that contains at least one expected-fact group."""
    text = norm(chunk.text)
    return chunk.doc_id in q.relevant_docs and any(group_satisfied(text, g) for g in q.facts)


def validate_labels(queries: list[Query], chunks: list[Chunk]) -> list[str]:
    """Return a list of problems; empty means the label file is consistent with the corpus."""
    problems: list[str] = []
    seen: set[str] = set()
    docs = {c.doc_id for c in chunks}
    for q in queries:
        if q.id in seen:
            problems.append(f"{q.id}: duplicate id")
        seen.add(q.id)
        if q.kind not in KINDS:
            problems.append(f"{q.id}: bad kind {q.kind!r}")
        if q.split not in SPLITS:
            problems.append(f"{q.id}: bad split {q.split!r}")
        if q.kind == "out_of_corpus":
            if q.relevant_docs or q.facts:
                problems.append(f"{q.id}: out-of-corpus query must not have labels")
            continue
        if not q.relevant_docs or not q.facts:
            problems.append(f"{q.id}: in-corpus query needs relevant_docs and facts")
            continue
        for d in q.relevant_docs:
            if d not in docs:
                problems.append(f"{q.id}: relevant doc {d!r} is not in the corpus")
        text = norm(" ".join(c.text for c in chunks if c.doc_id in q.relevant_docs))
        for group in q.facts:
            if not group_satisfied(text, group):
                problems.append(f"{q.id}: no relevant document contains any of {list(group)}")
    return problems


# ---------------------------------------------------------------- retrieval

def retrieval_eval(queries: list[Query], retriever: Retriever, ks=DEFAULT_KS, rewriter=None) -> dict:
    rows = []
    for q in (q for q in queries if q.kind == "in_corpus"):
        hits = retriever.search(q.question, top_k=max(ks), rewrite=rewriter.rewrite(q.question) if rewriter else None)
        relevant = [h.chunk.doc_id in q.relevant_docs for h in hits]
        bearing = [is_answer_bearing(h.chunk, q) for h in hits]
        first = next((i + 1 for i, b in enumerate(bearing) if b), None)
        available = sum(1 for c in retriever.chunks if c.doc_id in q.relevant_docs and c.is_latest)
        row = {"id": q.id, "question": q.question, "first_answer_bearing_rank": first,
               "top_docs": [h.chunk.doc_id for h in hits[:3]]}
        for k in ks:
            row[f"precision@{k}"] = sum(relevant[:k]) / k
            # Precision@K cannot exceed 1 only if the relevant documents have >= K chunks. The capped
            # version divides by the most that was attainable, min(K, chunks in relevant documents).
            row[f"capped_precision@{k}"] = sum(relevant[:k]) / max(1, min(k, available))
            row[f"hit@{k}"] = any(bearing[:k])
        row["rr"] = 1 / first if first else 0.0
        rows.append(row)
    n = len(rows)
    mean = lambda key: round(sum(float(r[key]) for r in rows) / n, 4) if n else None
    return {
        "n": n,
        **{f"precision@{k}": mean(f"precision@{k}") for k in ks},
        **{f"capped_precision@{k}": mean(f"capped_precision@{k}") for k in ks},
        **{f"hit@{k}": mean(f"hit@{k}") for k in ks},
        "mrr": mean("rr"),
        "rows": rows,
    }


# ------------------------------------------------------------- QA / validation

def run_qa(queries: list[Query], service: QAService, top_k: int = 5) -> list[dict]:
    records = []
    for q in queries:
        result = service.ask(q.question, top_k=top_k)
        records.append({
            "id": q.id, "kind": q.kind, "split": q.split, "question": q.question,
            "answer": result.answer, "confidence": result.confidence,
            "abstained": result.answer == ABSTAIN_TEXT, "cited": bool(result.citations),
            "citations": [c["chunk_id"] for c in result.citations],
            "correct": answer_correct(result.answer, q) if q.kind == "in_corpus" else None,
            "validation": result.debug["validation"],
            "generator_error": result.debug.get("generator_error"),
        })
    return records


def status_at(record: dict, threshold: float) -> str:
    return "validated" if record["confidence"] >= threshold and record["cited"] else "needs_review"


def _rate(num: int, den: int) -> float | None:
    return round(num / den, 4) if den else None


def wilson(successes: int, n: int, z: float = 1.96) -> tuple[float, float] | None:
    """95% Wilson score interval for a proportion; the honest error bar for small samples."""
    if n == 0:
        return None
    p = successes / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5) / denom
    return round(max(0.0, centre - half), 4), round(min(1.0, centre + half), 4)


def summarize(records: list[dict], threshold: float) -> dict:
    inc = [r for r in records if r["kind"] == "in_corpus"]
    ooc = [r for r in records if r["kind"] == "out_of_corpus"]
    val_in = [r for r in inc if status_at(r, threshold) == "validated"]
    correct = [r for r in inc if r["correct"]]
    val_correct = [r for r in val_in if r["correct"]]
    accepted_ooc = [r for r in ooc if status_at(r, threshold) == "validated"]
    right_calls = len(val_correct) + sum(1 for r in inc if not r["correct"] and status_at(r, threshold) != "validated") \
        + (len(ooc) - len(accepted_ooc))
    return {
        "threshold": threshold,
        "in_corpus": {
            "n": len(inc),
            "pass_rate": _rate(len(val_in), len(inc)),
            "mean_confidence": round(sum(r["confidence"] for r in inc) / len(inc), 4) if inc else None,
            "answer_correct_rate": _rate(len(correct), len(inc)),
            "validated_precision": _rate(len(val_correct), len(val_in)),
            "validated_but_wrong_rate": _rate(len(val_in) - len(val_correct), len(val_in)),
            "correct_but_flagged_rate": _rate(len(correct) - len(val_correct), len(correct)),
        },
        "out_of_corpus": {
            "n": len(ooc),
            "needs_review_rate": _rate(len(ooc) - len(accepted_ooc), len(ooc)),
            "false_accept_rate": _rate(len(accepted_ooc), len(ooc)),
            "mean_confidence": round(sum(r["confidence"] for r in ooc) / len(ooc), 4) if ooc else None,
        },
        "decision_accuracy": _rate(right_calls, len(records)),
    }


def sweep(records: list[dict], thresholds=DEFAULT_SWEEP) -> list[dict]:
    rows = []
    for t in thresholds:
        s = summarize(records, t)
        rows.append({"threshold": t, "pass_rate": s["in_corpus"]["pass_rate"],
                     "validated_precision": s["in_corpus"]["validated_precision"],
                     "validated_but_wrong_rate": s["in_corpus"]["validated_but_wrong_rate"],
                     "correct_but_flagged_rate": s["in_corpus"]["correct_but_flagged_rate"],
                     "ooc_false_accept_rate": s["out_of_corpus"]["false_accept_rate"],
                     "decision_accuracy": s["decision_accuracy"]})
    return rows


def review_list(records: list[dict], threshold: float) -> list[dict]:
    """Queries an analyst should look at: flagged in-corpus, wrongly validated, wrongly accepted OOC."""
    out = []
    for r in records:
        status = status_at(r, threshold)
        if r["kind"] == "in_corpus" and status == "needs_review":
            why = "correct answer withheld" if r["correct"] else "flagged: low confidence"
        elif r["kind"] == "in_corpus" and not r["correct"]:
            why = "VALIDATED BUT WRONG"
        elif r["kind"] == "out_of_corpus" and status == "validated":
            why = "VALIDATED BUT OUT OF CORPUS"
        else:
            continue
        out.append({"id": r["id"], "reason": why, "confidence": r["confidence"], "question": r["question"],
                    "answer": r["answer"][:240], "validator_notes": "; ".join(r["validation"]["reasons"])})
    return out


def write_review_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = ["id", "reason", "confidence", "question", "answer", "validator_notes"]
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


# ------------------------------------------------------------ validator stress

def load_stress(path: Path | str) -> list[dict]:
    return [json.loads(l) for l in Path(path).read_text(encoding="utf-8").splitlines() if l.strip()]


def stress_eval(cases: list[dict], services: dict[str, QAService], threshold: float) -> dict:
    """Score hand-written answers (good/bad) with the validator, using live retrieved evidence."""
    from .retriever import top_retrieval_score
    from .validator import validate

    rows = []
    for case in cases:
        service = services[case["corpus"]]
        question = case["question"]
        hits = service.retriever.expand_sparse(service.retriever.search(question, top_k=5))
        evidence = [h.chunk for h in hits]
        # Make sure the true supporting text is among the evidence, so this test measures the
        # validator and not retrieval failures (retrieval is measured separately).
        have = {c.chunk_id for c in evidence}
        phrases = [norm(p) for p in case.get("gold_phrases", [])]
        for c in service.loaded.chunks:
            if c.doc_id in case.get("gold_docs", []) and c.chunk_id not in have and any(p in norm(c.text) for p in phrases):
                evidence.append(c)
        v = validate(question, case["answer"], evidence, top_retrieval_score(hits),
                     service.lexicon, threshold=threshold, cited=True)
        rows.append({**case, "confidence": v.confidence, "status": v.status, "reasons": v.reasons,
                     "caught": (v.status == "needs_review") if case["label"] == "bad" else (v.status == "validated")})
    bad = [r for r in rows if r["label"] == "bad"]
    good = [r for r in rows if r["label"] == "good"]
    by_kind: dict[str, dict] = {}
    for r in rows:
        k = by_kind.setdefault(r["kind"], {"n": 0, "correct_decisions": 0})
        k["n"] += 1
        k["correct_decisions"] += int(r["caught"])
    return {
        "threshold": threshold, "n": len(rows),
        "bad_answers_flagged_rate": _rate(sum(r["caught"] for r in bad), len(bad)),
        "good_answers_accepted_rate": _rate(sum(r["caught"] for r in good), len(good)),
        "by_kind": {k: {**v, "rate": _rate(v["correct_decisions"], v["n"])} for k, v in sorted(by_kind.items())},
        "rows": rows,
    }
