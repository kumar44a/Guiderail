"""Query -> scored evidence chunks, with the version policy and sparse-section fallback."""

from __future__ import annotations

from dataclasses import dataclass

from .embeddings import embed
from .index import LoadedIndex
from .lexicon import Lexicon
from .models import Chunk
from .text import tokenize

RERANK_POOL = 30         # FAISS candidates considered when re-ranking
SPARSE_WORDS = 25        # a retrieved chunk shorter than this is "sparse"
SPARSE_TOP_N = 3         # only the best few hits may pull in a neighbour


@dataclass
class Hit:
    chunk: Chunk
    score: float
    via: str = "retrieval"   # "retrieval" or "neighbor"


class Retriever:
    def __init__(self, loaded: LoadedIndex, lexicon: Lexicon | None = None, rerank_weight: float = 0.0):
        self.index = loaded.index
        self.chunks = loaded.chunks
        self.lexicon = lexicon or Lexicon(self.chunks)
        self.rerank_weight = rerank_weight
        self._unit_tokens: dict[str, list[set[str]]] = {}
        self._by_position = {(c.doc_id, c.position): c for c in self.chunks}

    def search(self, question: str, top_k: int = 5, include_superseded: bool = False) -> list[Hit]:
        """Top-k chunks by cosine similarity.

        Version policy: chunks from superseded documents are skipped unless
        `include_superseded` is set, so a withdrawn recommendation is never cited
        as current guidance.
        """
        total = self.index.ntotal
        if total == 0 or top_k < 1:
            return []
        query = embed(question)
        if not query.any():
            return []
        fetch = min(total, max(top_k * 4, 20, RERANK_POOL if self.rerank_weight else 0))
        while True:
            scores, ids = self.index.search(query.reshape(1, -1), fetch)
            hits = [
                Hit(self.chunks[i], float(s))
                for s, i in zip(scores[0], ids[0])
                if i >= 0 and (include_superseded or self.chunks[i].is_latest)
            ]
            if len(hits) >= top_k or fetch >= total:
                if self.rerank_weight:
                    hits = self._rerank(question, hits)
                return hits[:top_k]
            fetch = min(total, fetch * 2)

    def _lexical_score(self, q_tokens: set[str], q_weight: float, chunk: Chunk) -> float:
        """Best single-sentence idf-weighted coverage of the question, plus a title/section bonus."""
        units = self._unit_tokens.get(chunk.chunk_id)
        if units is None:
            units = self._unit_tokens[chunk.chunk_id] = [set(tokenize(u)) for u in chunk.text.split("\n") if u.strip()]
        best = max((self.lexicon.weight(q_tokens & u) for u in units), default=0.0)
        context = self.lexicon.weight(q_tokens & set(tokenize(f"{chunk.title} {chunk.section}")))
        return (best + 0.5 * context) / q_weight

    def _rerank(self, question: str, hits: list[Hit]) -> list[Hit]:
        """Order the candidates by cosine + weight x lexical score. Hit.score stays the cosine,
        which the validator's relevance scale is defined on."""
        q_tokens = set(tokenize(question))
        q_weight = self.lexicon.weight(q_tokens)
        if not q_tokens or q_weight == 0:
            return hits
        return sorted(hits[:RERANK_POOL],
                      key=lambda h: -(h.score + self.rerank_weight * self._lexical_score(q_tokens, q_weight, h.chunk)))

    def expand_sparse(self, hits: list[Hit]) -> list[Hit]:
        """Controlled fallback for very short chunks.

        If one of the top hits is too short to carry an answer, add its next chunk
        (or the previous one at the end of a document) from the same document. Added
        chunks are marked `via="neighbor"`, are never duplicated, and are cited like
        any other evidence, so nothing is padded silently.
        """
        have = {h.chunk.chunk_id for h in hits}
        extra: list[Hit] = []
        for hit in hits[:SPARSE_TOP_N]:
            if hit.via != "retrieval" or len(hit.chunk.text.split()) >= SPARSE_WORDS:
                continue
            for step in (1, -1):
                neighbour = self._by_position.get((hit.chunk.doc_id, hit.chunk.position + step))
                if neighbour and neighbour.chunk_id not in have:
                    have.add(neighbour.chunk_id)
                    extra.append(Hit(neighbour, hit.score, via="neighbor"))
                    break
        return hits + extra


def top_retrieval_score(hits: list[Hit]) -> float:
    scores = [h.score for h in hits if h.via == "retrieval"]
    return max(scores) if scores else 0.0

