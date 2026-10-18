"""Deterministic 256-D text embeddings. No model, no network, no randomness.

Method ("hash-ngram-md5-v1"): tokenise (stopwords dropped, light stemming), take
unigrams and adjacent-token bigrams, hash each feature with MD5 to a bucket and a
sign, accumulate with sublinear term weighting, L2-normalise. (Corpus idf weighting
was tried and rejected on the dev split; see docs/EVALUATION_LOG.md.)

MD5 is used for stable bucketing only (never Python's salted hash()), so the same
text yields byte-identical vectors on every machine. These vectors are lexical:
they match shared words, not meaning. That limitation is documented in the report.
"""

from __future__ import annotations

import hashlib
import math
from collections import Counter
from functools import lru_cache

import numpy as np

from .text import tokenize

DIM = 256
METHOD = "hash-ngram-md5-v1"
BIGRAM_WEIGHT = 0.5


@lru_cache(maxsize=65536)
def _bucket(feature: str) -> tuple[int, float]:
    digest = hashlib.md5(feature.encode("utf-8")).digest()
    index = int.from_bytes(digest[:4], "big") % DIM
    sign = 1.0 if digest[4] & 1 else -1.0
    return index, sign


def _features(text: str) -> Counter[str]:
    tokens = tokenize(text)
    feats: Counter[str] = Counter(tokens)
    for left, right in zip(tokens, tokens[1:]):
        feats[f"{left} {right}"] += 1
    return feats


def embed(text: str) -> np.ndarray:
    """Return a unit-length float32 vector of shape (DIM,); all zeros for empty text."""
    acc = np.zeros(DIM, dtype=np.float64)
    for feature, count in sorted(_features(text).items()):
        index, sign = _bucket(feature)
        weight = (1.0 + math.log(count)) * (BIGRAM_WEIGHT if " " in feature else 1.0)
        acc[index] += sign * weight
    norm = np.linalg.norm(acc)
    if norm > 0:
        acc /= norm
    return acc.astype(np.float32)


def embed_batch(texts: list[str]) -> np.ndarray:
    if not texts:
        return np.zeros((0, DIM), dtype=np.float32)
    return np.stack([embed(t) for t in texts]).astype(np.float32)
