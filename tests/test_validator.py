"""The validator must catch bad answers it did not produce.

Cases are written by hand, independent of the extractive generator: fabricated
figures, flipped meaning, unrelated answers, paraphrase, and uncited answers.
"""

import pytest

from guiderail.lexicon import Lexicon
from guiderail.models import Chunk
from guiderail.retriever import Retriever, top_retrieval_score
from guiderail.validator import validate

QUESTION = "What temperature should vaccines be stored at?"


def _chunk(text: str) -> Chunk:
    return Chunk("t#a-0", "t", "WHO", "T", 2024, 1, "t", "A", 0, text, True)


@pytest.fixture(scope="module")
def evidence(loaded):
    hits = Retriever(loaded).search(QUESTION, top_k=5)
    return [h.chunk for h in hits], top_retrieval_score(hits), Lexicon(loaded.chunks)


def _check(evidence, answer, question=QUESTION, **kw):
    chunks, top, lexicon = evidence
    return validate(question, answer, chunks, top, lexicon, **kw)


def test_faithful_answer_is_validated(evidence):
    v = _check(evidence, "Store refrigerated vaccines between 2 and 8 degrees Celsius.")
    assert v.status == "validated" and v.confidence >= 0.6 and v.coverage == 1.0
    assert v.unsupported_terms == [] and v.unsupported_numbers == []


def test_fabricated_numbers_are_flagged(evidence):
    v = _check(evidence, "Store refrigerated vaccines between 4 and 12 degrees Celsius.")
    assert v.status == "needs_review"
    assert v.unsupported_numbers == ["4", "12"]
    assert any("number" in r for r in v.reasons)


def test_unrelated_answer_is_flagged(evidence):
    v = _check(evidence, "Wash hands with soap and water for 40 to 60 seconds.")
    assert v.status == "needs_review" and v.coverage < 0.5


def test_paraphrase_is_flagged_conservatively(evidence):
    # Documented limitation: token overlap cannot see that this is a faithful paraphrase.
    v = _check(evidence, "Keep vaccines in the fridge at two to eight degrees.")
    assert v.status == "needs_review"
    assert "fridg" in v.unsupported_terms


def test_partially_supported_answer_scores_between_the_extremes(evidence):
    faithful = _check(evidence, "Store refrigerated vaccines between 2 and 8 degrees Celsius.")
    partial = _check(evidence, "Store refrigerated vaccines between 2 and 8 degrees Celsius and photograph each vial.")
    unrelated = _check(evidence, "Wash hands with soap and water for 40 to 60 seconds.")
    assert unrelated.confidence < partial.confidence < faithful.confidence


def test_unsupported_negation_is_penalised():
    chunks = [_chunk("Wash hands before touching a patient.")]
    lexicon = Lexicon(chunks)
    q = "when should hands be washed"
    good = validate(q, "Wash hands before touching a patient.", chunks, 0.5, lexicon)
    flipped = validate(q, "Do not wash hands before touching a patient.", chunks, 0.5, lexicon)
    assert good.status == "validated"
    assert flipped.status == "needs_review" and any("negation" in r for r in flipped.reasons)


@pytest.mark.xfail(strict=True, reason="known limitation: token-level checks miss a negation word "
                                       "that appears elsewhere in the evidence")
def test_negation_flip_hidden_by_word_elsewhere_in_evidence(evidence):
    # 'not' occurs in the cold-chain evidence ("do not use"), so this flip is not caught.
    v = _check(evidence, "Do not store refrigerated vaccines between 2 and 8 degrees Celsius.")
    assert v.status == "needs_review"


def test_off_topic_question_is_flagged_even_if_answer_is_copied_from_evidence(loaded):
    question = "What is the recommended dose of amoxicillin for otitis media?"
    hits = Retriever(loaded).search(question, top_k=5)
    answer = hits[0].chunk.text.split("\n")[0]          # a perfect copy of retrieved text
    v = validate(question, answer, [h.chunk for h in hits], top_retrieval_score(hits), Lexicon(loaded.chunks))
    assert v.coverage == 1.0                            # copying makes coverage trivially perfect...
    assert v.status == "needs_review"                   # ...so relevance has to catch it
    assert v.confidence < 0.6


def test_uncited_answer_needs_review_even_when_supported(evidence):
    v = _check(evidence, "Store refrigerated vaccines between 2 and 8 degrees Celsius.", cited=False)
    assert v.status == "needs_review" and any("citation" in r for r in v.reasons)


def test_abstained_and_empty_answers_have_zero_confidence(evidence):
    for kwargs in ({"answer": "anything", "abstained": True}, {"answer": "   "}, {"answer": "the of and"}):
        v = _check(evidence, **kwargs)
        assert v.confidence == 0.0 and v.status == "needs_review"


def test_threshold_controls_status(evidence):
    answer = "Store refrigerated vaccines between 2 and 8 degrees Celsius."
    strict = _check(evidence, answer, threshold=1.01)
    lenient = _check(evidence, answer, threshold=0.1)
    assert strict.confidence == lenient.confidence
    assert strict.status == "needs_review" and lenient.status == "validated"


def test_confidence_is_bounded(evidence):
    for answer in ("Store refrigerated vaccines between 2 and 8 degrees Celsius.", "zzz qqq 99", "x"):
        assert 0.0 <= _check(evidence, answer).confidence <= 1.0


# ---------- yes/no response marker (validator round 2) ----------

def _plain(text):
    return Chunk("t#a-0", "t", "WHO", "T", 2024, 1, "t", "A", 0, text, True)


def _yn(answer, evidence_text="Brushes are not recommended for surgical hand preparation. Use a nail cleaner."):
    from guiderail.lexicon import Lexicon as L
    chunks = [_plain(evidence_text)]
    return validate("Are brushes recommended for surgical hand preparation?", answer, chunks, 0.4, L(chunks))


def test_leading_no_is_not_scored_as_an_unsupported_negation():
    with_marker = _yn("No, brushes are not recommended for surgical hand preparation.")
    without = _yn("Brushes are not recommended for surgical hand preparation.")
    assert with_marker.confidence == without.confidence
    assert "no" not in with_marker.unsupported_terms and not any("negation" in r for r in with_marker.reasons)


def test_leading_yes_is_not_scored_as_an_unsupported_term():
    v = _yn("Yes. Use a nail cleaner.")
    assert "yes" not in v.unsupported_terms and v.coverage == 1.0


def test_no_as_a_determiner_is_still_scored():
    v = _yn("No further brushes are recommended for surgical hand preparation.")
    assert "no" in v.unsupported_terms and any("negation" in r for r in v.reasons)


def test_a_bare_yes_or_no_is_not_an_answer():
    v = _yn("No.")
    assert v.status == "needs_review" and v.confidence == 0.0


def test_marker_does_not_hide_a_fabricated_number():
    v = _yn("No, scrub for at least 15 minutes.")
    assert v.status == "needs_review" and "15" in v.unsupported_numbers


def test_negation_later_in_the_answer_is_still_checked():
    v = _yn("No, brushes are never allowed.")
    assert "never" in v.unsupported_terms and any("negation" in r for r in v.reasons)
