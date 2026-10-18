import pytest

from guiderail.evalkit import (
    Query, answer_correct, is_answer_bearing, load_queries, load_stress, norm, review_list,
    status_at, summarize, sweep, validate_labels,
)
from guiderail.models import Chunk
from tests.conftest import ROOT

EVAL = ROOT / "evaluation"


def q(**over):
    base = dict(id="Q1", question="?", kind="in_corpus", split="dev", relevant_docs=("d1",),
                facts=(("5 days",),), forbidden=(), note="")
    return Query(**{**base, **over})


def chunk(text, doc="d1"):
    return Chunk(f"{doc}#a-0", doc, "WHO", "T", 2024, 1, "t", "A", 0, text, True)


# ---------- label files ----------

def test_synthetic_labels_are_consistent_with_the_corpus(loaded):
    queries = load_queries(EVAL / "queries_synthetic.jsonl")
    assert validate_labels(queries, loaded.chunks) == []
    assert {x.kind for x in queries} == {"in_corpus", "out_of_corpus"}
    assert {x.split for x in queries} == {"dev", "test"}


def test_real_labels_are_consistent_with_the_pdfs():
    sources = ROOT / "data" / "real" / "sources.json"
    if not sources.exists() or not list((ROOT / "data" / "real").glob("*.pdf")):
        pytest.skip("real PDFs not present")
    from guiderail.chunker import chunk_corpus
    from guiderail.loaders import PdfLoader

    chunks, _ = chunk_corpus(PdfLoader(ROOT / "data" / "real").load())
    assert validate_labels(load_queries(EVAL / "queries_real.jsonl"), chunks) == []


def test_splits_are_balanced_and_disjoint():
    for name in ("queries_synthetic.jsonl", "queries_real.jsonl"):
        queries = load_queries(EVAL / name)
        for kind in ("in_corpus", "out_of_corpus"):
            dev = [x for x in queries if x.kind == kind and x.split == "dev"]
            test = [x for x in queries if x.kind == kind and x.split == "test"]
            assert abs(len(dev) - len(test)) <= 1 and dev and test
        assert len({x.question for x in queries}) == len(queries)


def test_validate_labels_catches_problems():
    chunks = [chunk("Staff may return after 5 days.")]
    bad = [q(id="A", relevant_docs=("nope",)), q(id="B", facts=(("99 years",),)), q(id="A"),
           q(id="C", kind="out_of_corpus"), q(id="D", split="holdout"), q(id="E", facts=())]
    text = "\n".join(validate_labels(bad, chunks))
    for needle in ("not in the corpus", "no relevant document contains", "duplicate id",
                   "must not have labels", "bad split", "needs relevant_docs and facts"):
        assert needle in text


def test_stress_set_does_not_reuse_test_split_questions():
    test_questions = {x.question for name in ("queries_synthetic.jsonl", "queries_real.jsonl")
                      for x in load_queries(EVAL / name) if x.split == "test"}
    cases = load_stress(EVAL / "validator_stress.jsonl")
    assert cases and not [c["id"] for c in cases if c["question"] in test_questions]
    assert {c["label"] for c in cases} == {"good", "bad"}
    assert len({c["id"] for c in cases}) == len(cases)


# ---------- text matching ----------

def test_norm_unifies_case_space_dashes_and_quotes():
    assert norm("  Minus −50°C and  “X” ") == 'minus -50°c and "x"'
    assert norm("-50°C") == norm("−50°C") == norm("–50°C")


def test_answer_correct_needs_all_groups_and_no_forbidden():
    query = q(facts=(("5 days", "five days"), ("24 hours",)), forbidden=("10 days",))
    assert answer_correct("Return after 5 days and 24 hours fever-free.", query)
    assert answer_correct("RETURN AFTER FIVE DAYS; fever free for 24  hours", query)
    assert not answer_correct("Return after 5 days.", query)                      # missing group
    assert not answer_correct("5 days, 24 hours, not 10 days.", query)            # forbidden present


def test_answer_bearing_chunk_must_be_from_a_relevant_doc():
    query = q()
    assert is_answer_bearing(chunk("Return after 5 days."), query)
    assert not is_answer_bearing(chunk("Return after 5 days.", doc="other"), query)
    assert not is_answer_bearing(chunk("Nothing relevant."), query)


# ---------- metric arithmetic on hand-built records ----------

def rec(kind, conf, correct=None, cited=True, id="x"):
    return {"id": id, "kind": kind, "split": "dev", "question": "q", "answer": "a", "confidence": conf,
            "cited": cited, "correct": correct, "abstained": False,
            "validation": {"reasons": []}}


RECORDS = [
    rec("in_corpus", 0.9, True, id="a"),    # validated, correct
    rec("in_corpus", 0.8, False, id="b"),   # validated, WRONG
    rec("in_corpus", 0.5, True, id="c"),    # flagged, but correct
    rec("in_corpus", 0.2, False, id="d"),   # flagged, wrong (right call)
    rec("out_of_corpus", 0.0, id="e"),      # right call
    rec("out_of_corpus", 0.7, id="f"),      # falsely validated
]


def test_summary_numbers_at_threshold_06():
    s = summarize(RECORDS, 0.6)
    ic, oc = s["in_corpus"], s["out_of_corpus"]
    assert ic["n"] == 4 and ic["pass_rate"] == 0.5
    assert ic["answer_correct_rate"] == 0.5
    assert ic["validated_precision"] == 0.5 and ic["validated_but_wrong_rate"] == 0.5
    assert ic["correct_but_flagged_rate"] == 0.5
    assert ic["mean_confidence"] == 0.6
    assert oc["n"] == 2 and oc["needs_review_rate"] == 0.5 and oc["false_accept_rate"] == 0.5
    # Right calls: a (validated and correct), d (wrong answer sent to review), e (out-of-corpus sent to
    # review) = 3 of 6. b and f were wrongly validated; c is a correct answer needlessly flagged.
    assert s["decision_accuracy"] == 0.5


def test_uncited_answers_are_never_validated():
    assert status_at(rec("in_corpus", 1.0, True, cited=False), 0.6) == "needs_review"
    assert status_at(rec("in_corpus", 1.0, True), 0.6) == "validated"
    assert status_at(rec("in_corpus", 0.6, True), 0.6) == "validated"      # threshold is inclusive


def test_empty_groups_give_none_not_division_errors():
    s = summarize([rec("out_of_corpus", 0.0)], 0.6)
    assert s["in_corpus"]["pass_rate"] is None and s["in_corpus"]["validated_precision"] is None
    assert summarize([], 0.6)["decision_accuracy"] is None


def test_sweep_pass_rate_never_increases_with_threshold():
    rows = sweep(RECORDS)
    rates = [r["pass_rate"] for r in rows]
    assert rates == sorted(rates, reverse=True) and rows[0]["threshold"] == 0.3 and rows[-1]["threshold"] == 0.9


def test_review_list_names_every_kind_of_problem():
    reasons = {r["id"]: r["reason"] for r in review_list(RECORDS, 0.6)}
    assert reasons["b"] == "VALIDATED BUT WRONG"
    assert reasons["c"] == "correct answer withheld"
    assert reasons["d"] == "flagged: low confidence"
    assert reasons["f"] == "VALIDATED BUT OUT OF CORPUS"
    assert "a" not in reasons and "e" not in reasons


def test_stem_aware_matching_accepts_inflections_but_not_negation_loss():
    query = q(facts=(("act in the absence of the primary coordinator",),))
    assert answer_correct("The backup acts in the absence of the primary coordinator.", query)
    neg = q(facts=(("do not wear the same gown",),))
    assert answer_correct("Do not wear the same gown between patients.", neg)
    assert not answer_correct("Wear the same gown between patients.", neg)          # stopwords are kept
    assert not answer_correct("Hands should be washed.", neg)


def test_forbidden_values_are_matched_with_inflections_too():
    query = q(facts=(("5 days",),), forbidden=("10 days",))
    assert not answer_correct("5 days normally, though some units use 10 day periods", query)


def test_wilson_interval_behaves_sensibly():
    from guiderail.evalkit import wilson

    assert wilson(0, 0) is None
    lo, hi = wilson(8, 8)
    assert hi == 1.0 and 0.6 < lo < 0.7                  # 8/8 is far from certain at n=8
    lo, hi = wilson(50, 100)
    assert lo < 0.5 < hi and hi - lo < 0.21
    lo, hi = wilson(0, 20)
    assert lo == 0.0 and 0.1 < hi < 0.2
