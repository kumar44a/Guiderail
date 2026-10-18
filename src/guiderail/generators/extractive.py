"""Default generator: copies the best-matching sentences out of the evidence.

No model call, fully deterministic. Because the answer is copied from the evidence,
the validator's coverage score is high by construction for this generator; the
meaningful signals are question support and retrieval relevance (see validator.py).

Selection works on single lines (bullets or sentences) and then repairs two cases where a
line is incomplete without its neighbours:
  * a lead-in ending in ":" brings the list items it introduces;
  * a line starting with "This/These/It/They..." continues the previous line.
"""

from __future__ import annotations

from ..lexicon import Lexicon
from ..retriever import Hit
from ..text import tokenize
from .base import Generated, Generator

MIN_SENTENCE_SCORE = 0.15     # fraction of question weight a sentence must cover
RELATIVE_CUTOFF = 0.6         # keep sentences scoring >= this fraction of the best one
RETRIEVAL_TIEBREAK = 0.1      # small bonus for sentences from better-retrieved chunks
CONTEXT_WEIGHT = 0.5          # credit for question terms found in the chunk's title and section
MAX_LIST_ITEMS = 4            # lines pulled in after a lead-in ending with ":"
ANAPHORA = frozenset({"this", "these", "that", "those", "it", "they", "such", "he", "she"})


def _is_continuation(line: str) -> bool:
    first = line.split(" ", 1)[0].lower().strip(",;:")
    return first in ANAPHORA


class ExtractiveGenerator(Generator):
    name = "extractive"

    def __init__(self, lexicon: Lexicon, max_sentences: int = 3):
        self.lexicon = lexicon
        self.max_sentences = max_sentences

    def generate(self, question: str, hits: list[Hit]) -> Generated:
        q_tokens = set(tokenize(question))
        q_weight = self.lexicon.weight(q_tokens)
        if not q_tokens or q_weight == 0 or not hits:
            return Generated.abstain()

        units_by_hit = [[u.strip() for u in h.chunk.text.split("\n") if u.strip()] for h in hits]
        scored: list[tuple[float, int, int]] = []          # (score, hit rank, unit index)
        seen: set[str] = set()
        for h_rank, hit in enumerate(hits):
            # A sentence inherits its context: "Wash at 70 degrees" says nothing about linen on its
            # own, but it sits in the guideline titled "Handling of Soiled Linen".
            context = set(tokenize(f"{hit.chunk.title} {hit.chunk.section}"))
            ctx_score = CONTEXT_WEIGHT * self.lexicon.weight(q_tokens & context) / q_weight
            for u_idx, unit in enumerate(units_by_hit[h_rank]):
                key = " ".join(unit.lower().split())
                if key in seen:
                    continue
                seen.add(key)
                own = self.lexicon.weight(q_tokens & set(tokenize(unit))) / q_weight
                if own == 0 or own + ctx_score < MIN_SENTENCE_SCORE:   # must speak to the question itself
                    continue
                scored.append((own + ctx_score + RETRIEVAL_TIEBREAK * hit.score, h_rank, u_idx))

        if not scored:
            return Generated.abstain()
        scored.sort(key=lambda t: (-t[0], t[1], t[2]))
        best = scored[0][0]
        chosen = [t for t in scored if t[0] >= RELATIVE_CUTOFF * best][: self.max_sentences]

        lines: list[str] = []
        chunk_ids: list[str] = []
        taken: set[tuple[int, int]] = set()

        def take(h_rank: int, u_idx: int) -> None:
            if (h_rank, u_idx) in taken:
                return
            taken.add((h_rank, u_idx))
            lines.append(units_by_hit[h_rank][u_idx])
            cid = hits[h_rank].chunk.chunk_id
            if cid not in chunk_ids:
                chunk_ids.append(cid)

        for _, h_rank, u_idx in chosen:
            take(h_rank, u_idx)
            units = units_by_hit[h_rank]
            if units[u_idx].endswith(":"):
                for follow in range(u_idx + 1, min(len(units), u_idx + 1 + MAX_LIST_ITEMS)):
                    take(h_rank, follow)
            elif u_idx + 1 < len(units) and _is_continuation(units[u_idx + 1]):
                take(h_rank, u_idx + 1)
        return Generated(answer=" ".join(lines), chunk_ids=chunk_ids)
