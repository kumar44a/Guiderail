"""BM25 keyword ranking over the whole vocabulary, plus reciprocal rank fusion.

Why: the 256-D hashed vectors lose information and the re-ranker only reorders a short FAISS list, so a passage outside that list
can never be found. BM25 ranks every chunk by exact (stemmed) term overlap, which gives the pipeline a second, independent way to
surface candidates. Everything here is deterministic: no randomness, ties broken by position.
"""

from __future__ import annotations

import math
from collections import Counter

from .models import Chunk
from .text import tokenize

K1 = 1.5          # textbook defaults, deliberately not tuned
B = 0.75
RRF_K = 60


class Bm25:
    def __init__(self, chunks: list[Chunk]):
        self.n = len(chunks)
        self.postings: dict[str, list[tuple[int, int]]] = {}
        self.lengths: list[int] = []
        for i, chunk in enumerate(chunks):
            counts = Counter(tokenize(chunk.embed_text))
            self.lengths.append(sum(counts.values()))
            for term, tf in sorted(counts.items()):
                self.postings.setdefault(term, []).append((i, tf))
        self.avg_len = (sum(self.lengths) / self.n) if self.n else 0.0
        self.idf = {t: math.log(1.0 + (self.n - len(p) + 0.5) / (len(p) + 0.5)) for t, p in self.postings.items()}

    def rank(self, query_tokens: list[str], limit: int, allowed=None) -> list[tuple[int, float]]:
        """Chunk positions with BM25 scores, best first. `allowed(i)` filters (for the version policy)."""
        scores: dict[int, float] = {}
        for term in sorted(set(query_tokens)):
            for i, tf in self.postings.get(term, ()):
                if allowed is not None and not allowed(i):
                    continue
                norm = tf + K1 * (1.0 - B + B * self.lengths[i] / self.avg_len)
                scores[i] = scores.get(i, 0.0) + self.idf[term] * tf * (K1 + 1.0) / norm
        return sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))[:limit]


def reciprocal_rank_fusion(rankings: list[list[int]], k: int = RRF_K) -> list[int]:
    """Merge ranked lists of ids: score = sum of 1 / (k + rank). Ties go to the lower id, so the result is deterministic."""
    fused: dict[int, float] = {}
    for ranking in rankings:
        for rank, item in enumerate(ranking, start=1):
            fused[item] = fused.get(item, 0.0) + 1.0 / (k + rank)
    return [i for i, _ in sorted(fused.items(), key=lambda kv: (-kv[1], kv[0]))]
