"""Heading-aware chunking: Document -> list[Chunk].

Each `## Heading` section is split into units (bullets, or sentences for prose),
and units are packed into chunks of at most `max_words` words. A unit longer than
`max_words` (common in extracted tables) is hard-split on word boundaries. A chunk
never crosses a section boundary, so every citation can name its section.
"""

from __future__ import annotations

import re

from .models import Chunk, Document

DEFAULT_MAX_WORDS = 80
_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")


def _slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "section"


def _split_sections(body: str) -> list[tuple[str, str]]:
    """Return (heading, text) pairs. Text before the first heading is 'Preamble'."""
    sections: list[tuple[str, list[str]]] = [("Preamble", [])]
    for line in body.split("\n"):
        if line.startswith("## "):
            sections.append((line[3:].strip(), []))
        else:
            sections[-1][1].append(line)
    return [(h, "\n".join(ls).strip()) for h, ls in sections if "\n".join(ls).strip()]


def _units(section_text: str) -> list[str]:
    """Bullets stay whole; prose is split into sentences."""
    units: list[str] = []
    prose: list[str] = []

    def flush_prose() -> None:
        if prose:
            joined = " ".join(prose).strip()
            units.extend(s.strip() for s in _SENTENCE_SPLIT.split(joined) if s.strip())
            prose.clear()

    for line in section_text.split("\n"):
        stripped = line.strip()
        if not stripped:
            flush_prose()
        elif stripped.startswith("- "):
            flush_prose()
            units.append(stripped[2:].strip())
        else:
            prose.append(stripped)
    flush_prose()
    return units


def _split_oversized(unit: str, max_words: int) -> list[str]:
    """Hard-split a unit with no sentence boundary (table rows, long lists) into word windows."""
    words = unit.split()
    if len(words) <= max_words:
        return [unit]
    return [" ".join(words[i : i + max_words]) for i in range(0, len(words), max_words)]


def _pack(units: list[str], max_words: int) -> list[str]:
    units = [piece for unit in units for piece in _split_oversized(unit, max_words)]
    chunks: list[list[str]] = []
    current: list[str] = []
    count = 0
    for unit in units:
        words = len(unit.split())
        if current and count + words > max_words:
            chunks.append(current)
            current, count = [], 0
        current.append(unit)
        count += words
    if current:
        chunks.append(current)
    return ["\n".join(c) for c in chunks]


def chunk_document(doc: Document, max_words: int = DEFAULT_MAX_WORDS) -> list[Chunk]:
    chunks: list[Chunk] = []
    for heading, text in _split_sections(doc.body):
        for n, chunk_text in enumerate(_pack(_units(text), max_words)):
            chunks.append(
                Chunk(
                    chunk_id=f"{doc.doc_id}#{_slug(heading)}-{n}",
                    doc_id=doc.doc_id,
                    agency=doc.agency,
                    title=doc.title,
                    year=doc.year,
                    version=doc.version,
                    topic=doc.topic,
                    section=heading,
                    position=len(chunks),
                    text=chunk_text,
                    is_latest=doc.is_latest,
                )
            )
    return chunks


def dedupe_within_document(chunks: list[Chunk]) -> tuple[list[Chunk], int]:
    """Drop chunks whose normalised text repeats inside the same document.

    Cross-document similarity is deliberately kept: superseded versions and
    other agencies' wording are handled by the version policy and citations,
    not by deleting evidence.
    """
    seen: set[tuple[str, str]] = set()
    kept: list[Chunk] = []
    for chunk in chunks:
        key = (chunk.doc_id, " ".join(chunk.text.lower().split()))
        if key in seen:
            continue
        seen.add(key)
        kept.append(chunk)
    return kept, len(chunks) - len(kept)


def chunk_corpus(docs: list[Document], max_words: int = DEFAULT_MAX_WORDS) -> tuple[list[Chunk], int]:
    all_chunks: list[Chunk] = []
    removed = 0
    for doc in docs:
        kept, dropped = dedupe_within_document(chunk_document(doc, max_words))
        all_chunks.extend(kept)
        removed += dropped
    return all_chunks, removed
