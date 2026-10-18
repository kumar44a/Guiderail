"""Evidence validator and confidence score (v2).

Independent of the generator: it sees only the question, the answer text and the
retrieved evidence, so it can score extractive answers, LLM answers, or answers an
analyst wrote by hand. confidence = coverage x relevance.

  coverage   share of the answer's content (stemmed, stopwords removed) that appears in the
             retrieved evidence or in its source metadata (agency, title, section). Each
             term is weighted by its idf, so an unsupported rare word (a made-up device, a
             drug name) costs far more than an unsupported common one. Halved if the answer
             contains a number-with-unit or a negation that the evidence does not contain.
  relevance  0.5 x retrieval relevance (top cosine score, rescaled) +
             0.5 x question support: the idf-weighted share of the question's terms that the
             ANSWER addresses (or that sit in the cited sources' titles). Measuring this against
             the answer, not the whole evidence set, is what stops a sentence that merely sits
             in retrieved text from passing as an answer to an unrelated question.

Known limit: a near-domain out-of-scope question ("how should radioactive waste be disposed of?"
against a corpus with a waste guideline) can still be answered with on-topic sentences and
validated. Scaling relevance down by the share of question words absent from the corpus was
tried and rejected (it also flagged correct answers whose questions used ordinary words such
as "often"); see docs/EVALUATION_LOG.md.

v1 measured question support against all retrieved text; on the dev split that let off-topic
answers through (e.g. a waste-container sentence as the answer to a radioactive-waste question).
The rescaling constants are PROVISIONAL and were checked on the development split only.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field

from .lexicon import Lexicon
from .models import Chunk
from .text import tokenize

DEFAULT_THRESHOLD = 0.6
RELEVANCE_FLOOR = 0.10     # cosine at or below this counts as no retrieval relevance
RELEVANCE_CEIL = 0.30      # cosine at or above this counts as full retrieval relevance
PENALTY = 0.5              # multiplier on coverage for unsupported numbers / negations
NEGATIONS = frozenset({"not", "no", "never", "without"})
_NUMBER_RE = re.compile(r"\d+(?:\.\d+)?")
# A number together with the word right after it, e.g. "10 days", "5 years", "0.5 percent".
_QUANTITY_RE = re.compile(r"(\d+(?:\.\d+)?)\s*(?:°\s*)?([a-zA-Z%]+)")


@dataclass
class Validation:
    confidence: float
    status: str                                   # "validated" | "needs_review"
    coverage: float
    question_support: float
    retrieval_relevance: float
    unsupported_terms: list[str] = field(default_factory=list)
    unsupported_numbers: list[str] = field(default_factory=list)
    reasons: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


def _unit_is_stopword(word: str) -> bool:
    """'5 and' / '2 to' are not quantities; skip words the tokenizer would drop."""
    return not tokenize(word)


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, value))


def validate(
    question: str,
    answer: str,
    evidence: list[Chunk],
    top_score: float,
    lexicon: Lexicon,
    threshold: float = DEFAULT_THRESHOLD,
    abstained: bool = False,
    cited: bool = True,
    cited_chunks: list[Chunk] | None = None,
) -> Validation:
    if abstained or not answer.strip():
        return Validation(0.0, "needs_review", 0.0, 0.0, 0.0, reasons=["abstained: no supported answer"])

    evidence_text = "\n".join(c.text for c in evidence)
    metadata_text = " ".join(f"{c.agency} {c.title} {c.section}" for c in evidence)
    evidence_tokens = set(tokenize(evidence_text)) | set(tokenize(metadata_text))
    answer_tokens = list(dict.fromkeys(tokenize(answer)))   # unique, order kept
    if not answer_tokens:
        return Validation(0.0, "needs_review", 0.0, 0.0, 0.0, reasons=["answer has no content terms"])

    unsupported = [t for t in answer_tokens if t not in evidence_tokens]
    coverage = 1.0 - lexicon.weight(unsupported) / lexicon.weight(answer_tokens)
    reasons: list[str] = []

    evidence_numbers = set(_NUMBER_RE.findall(evidence_text))
    unsupported_numbers = [n for n in dict.fromkeys(_NUMBER_RE.findall(answer)) if n not in evidence_numbers]
    evidence_quantities = {(n, tokenize(u, apply_stem=True)[0] if tokenize(u) else u.lower())
                           for n, u in _QUANTITY_RE.findall(evidence_text)}
    for n, u in dict.fromkeys(_QUANTITY_RE.findall(answer)):
        unit = tokenize(u)[0] if tokenize(u) else u.lower()
        if n not in unsupported_numbers and (n, unit) not in evidence_quantities and not _unit_is_stopword(u):
            unsupported_numbers.append(f"{n} {u}")
    if unsupported_numbers:
        coverage *= PENALTY
        reasons.append(f"number(s) not found in evidence: {', '.join(unsupported_numbers)}")
    unsupported_negations = [t for t in unsupported if t in NEGATIONS]
    if unsupported_negations:
        coverage *= PENALTY
        reasons.append(f"negation not found in evidence: {', '.join(unsupported_negations)}")

    q_tokens = set(tokenize(question))
    q_weight = lexicon.weight(q_tokens)
    addressed = set(answer_tokens) | set(tokenize(" ".join(f"{c.title} {c.section}" for c in cited_chunks or evidence[:1])))
    question_support = lexicon.weight(q_tokens & addressed) / q_weight if q_weight else 0.0
    retrieval_relevance = _clamp((top_score - RELEVANCE_FLOOR) / (RELEVANCE_CEIL - RELEVANCE_FLOOR))
    relevance = 0.5 * retrieval_relevance + 0.5 * question_support

    confidence = _clamp(coverage * relevance)
    if coverage < 0.8:
        reasons.append(f"low evidence coverage ({coverage:.2f}); unsupported terms: {', '.join(unsupported[:8])}")
    if relevance < 0.6:
        reasons.append(f"weak relevance to the question ({relevance:.2f})")

    status = "validated" if confidence >= threshold else "needs_review"
    if not cited:
        status = "needs_review"
        reasons.append("answer carries no citation")

    return Validation(
        confidence=round(confidence, 3),
        status=status,
        coverage=round(coverage, 3),
        question_support=round(question_support, 3),
        retrieval_relevance=round(retrieval_relevance, 3),
        unsupported_terms=unsupported,
        unsupported_numbers=unsupported_numbers,
        reasons=reasons,
    )
