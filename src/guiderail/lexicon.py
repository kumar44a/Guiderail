"""Corpus statistics used to weight terms: rare words matter more than common ones."""

from __future__ import annotations

import math
from collections import Counter

from .models import Chunk
from .text import tokenize


class Lexicon:
    def __init__(self, chunks: list[Chunk]):
        self.n_docs = len(chunks)
        self._df: Counter[str] = Counter()
        for chunk in chunks:
            self._df.update(set(tokenize(chunk.embed_text)))

    def idf(self, token: str) -> float:
        """Smoothed inverse document frequency; unseen tokens get the maximum weight."""
        return math.log((self.n_docs + 1) / (self._df.get(token, 0) + 1)) + 1.0

    def weight(self, tokens) -> float:
        return sum(self.idf(t) for t in tokens)
