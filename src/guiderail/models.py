"""Plain data containers shared by every pipeline stage."""

from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass
class Document:
    doc_id: str
    agency: str
    title: str
    year: int
    version: int
    topic: str
    body: str
    source_path: str
    source_sha256: str
    supersedes: str | None = None
    superseded_by: str | None = None
    synthetic: bool = True

    @property
    def is_latest(self) -> bool:
        return self.superseded_by is None


@dataclass
class Chunk:
    chunk_id: str
    doc_id: str
    agency: str
    title: str
    year: int
    version: int
    topic: str
    section: str
    position: int
    text: str
    is_latest: bool

    @property
    def embed_text(self) -> str:
        """Text that gets embedded: metadata context plus the chunk body."""
        return f"{self.agency} {self.title}. {self.section}. {self.text}"

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> Chunk:
        return cls(**data)
