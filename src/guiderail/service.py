"""QAService: retrieve -> generate -> validate. The only place the stages are wired."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field

from . import config
from .generators import ABSTAIN_TEXT, GenerationError, Generated, Generator
from .generators.extractive import ExtractiveGenerator
from .index import LoadedIndex
from .lexicon import Lexicon
from .retriever import Hit, Retriever, top_retrieval_score
from .validator import DEFAULT_THRESHOLD, Validation, validate

log = logging.getLogger(__name__)


@dataclass
class QAResult:
    answer: str
    citations: list[dict]
    confidence: float
    status: str
    debug: dict = field(default_factory=dict)


def _citation(hit: Hit) -> dict:
    c = hit.chunk
    return {
        "chunk_id": c.chunk_id, "doc_id": c.doc_id, "title": c.title, "agency": c.agency,
        "year": c.year, "version": c.version, "section": c.section, "score": round(hit.score, 3),
    }


class QAService:
    def __init__(self, loaded: LoadedIndex, generator: Generator | None = None,
                 threshold: float = DEFAULT_THRESHOLD, rerank_weight: float | None = None, rewriter=None):
        self.loaded = loaded
        self.lexicon = Lexicon(loaded.chunks)
        self.retriever = Retriever(loaded, self.lexicon, config.rerank_weight() if rerank_weight is None else rerank_weight,
                                   hybrid=config.hybrid(), doc_cohesion=config.doc_cohesion())
        self.generator = generator or ExtractiveGenerator(self.lexicon)
        self.threshold = threshold
        self.rewriter = rewriter

    def ask(self, question: str, top_k: int = 5) -> QAResult:
        rewrite = self.rewriter.rewrite(question) if self.rewriter is not None else None
        hits = self.retriever.expand_sparse(self.retriever.search(question, top_k, rewrite=rewrite))
        error = None
        try:
            generated = self.generator.generate(question, hits)
        except GenerationError as exc:
            log.warning("generation failed: %s", exc)
            generated, error = Generated.abstain(), str(exc)

        by_id = {h.chunk.chunk_id: h for h in hits}
        cited_hits = [by_id[i] for i in generated.chunk_ids if i in by_id]
        validation: Validation = validate(
            question=question,
            answer=generated.answer,
            evidence=[h.chunk for h in hits],
            top_score=top_retrieval_score(hits),
            lexicon=self.lexicon,
            threshold=self.threshold,
            abstained=generated.abstained,
            cited=bool(cited_hits),
            cited_chunks=[h.chunk for h in cited_hits],
        )
        debug = {
            "generator": self.generator.name,
            "rewrite": rewrite,
            "validation": validation.to_dict(),
            "evidence": [{**_citation(h), "via": h.via} for h in hits],
        }
        if error:
            debug["generator_error"] = error
        return QAResult(
            answer=generated.answer if generated.answer else ABSTAIN_TEXT,
            citations=[_citation(h) for h in cited_hits],
            confidence=validation.confidence,
            status=validation.status,
            debug=debug,
        )
