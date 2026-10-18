"""Tokenisation shared by the embedder and (later) the validator.

Keeping one definition here means retrieval and validation agree on what a
"token" is. Negations (not, no, never, without) are deliberately kept.
"""

from __future__ import annotations

import re

_TOKEN_RE = re.compile(r"[a-z0-9]+")

STOPWORDS = frozenset(
    """a an and are as at be been being by can do does for from had has have if in into
    is it its may of on or our should so such than that the their then there these they
    this those to was were what when where which while who whom why will with would you
    your how any all each both more most other some than too very""".split()
)


def stem(token: str) -> str:
    """Light, deterministic suffix stripper (not a full Porter stemmer)."""
    if len(token) <= 3 or token.isdigit():
        return token
    if token.endswith("ies") and len(token) > 4:
        token = token[:-3] + "y"
    elif token.endswith("sses"):
        token = token[:-2]
    elif token.endswith("ing") and len(token) > 5:
        token = token[:-3]
    elif token.endswith("ed") and len(token) > 4:
        token = token[:-2]
    elif token.endswith("es") and len(token) > 4:
        token = token[:-2]
    elif token.endswith("s") and not token.endswith("ss"):
        token = token[:-1]
    if token.endswith("e") and len(token) > 3:
        token = token[:-1]
    return token


def tokenize(text: str, *, drop_stopwords: bool = True, apply_stem: bool = True) -> list[str]:
    tokens = _TOKEN_RE.findall(text.lower())
    if drop_stopwords:
        tokens = [t for t in tokens if t not in STOPWORDS]
    if apply_stem:
        tokens = [stem(t) for t in tokens]
    return tokens
