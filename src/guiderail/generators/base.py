from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from ..retriever import Hit

ABSTAIN_TEXT = "No supported answer was found in the indexed guidelines."


class GenerationError(RuntimeError):
    """The generator could not produce an answer (e.g. the LLM API failed)."""


@dataclass
class Generated:
    answer: str
    chunk_ids: list[str] = field(default_factory=list)   # chunks the answer relies on, best first
    abstained: bool = False

    @classmethod
    def abstain(cls) -> Generated:
        return cls(answer=ABSTAIN_TEXT, chunk_ids=[], abstained=True)


class Generator(ABC):
    name: str

    @abstractmethod
    def generate(self, question: str, hits: list[Hit]) -> Generated:
        """Answer from the supplied evidence only."""
