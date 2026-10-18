"""Loader contract. This interface is the one swap point for a real guideline
repository: implement `load()` and the rest of the pipeline is unchanged."""

from __future__ import annotations

from abc import ABC, abstractmethod

from ..models import Document


class BaseLoader(ABC):
    @abstractmethod
    def load(self) -> list[Document]:
        """Return documents sorted by doc_id, with versions resolved."""


def resolve_versions(docs: list[Document]) -> list[Document]:
    """Fill `superseded_by` from each document's `supersedes` pointer.

    Raises ValueError on duplicate ids, unknown targets, or a document that is
    superseded twice, so a bad corpus fails at load time and not at query time.
    """
    by_id: dict[str, Document] = {}
    for doc in docs:
        if doc.doc_id in by_id:
            raise ValueError(f"duplicate doc_id: {doc.doc_id}")
        by_id[doc.doc_id] = doc

    for doc in docs:
        doc.superseded_by = None
    for doc in docs:
        if not doc.supersedes:
            continue
        target = by_id.get(doc.supersedes)
        if target is None:
            raise ValueError(f"{doc.doc_id} supersedes unknown document {doc.supersedes!r}")
        if target.superseded_by is not None:
            raise ValueError(
                f"{target.doc_id} is superseded by both {target.superseded_by} and {doc.doc_id}"
            )
        target.superseded_by = doc.doc_id
    return sorted(docs, key=lambda d: d.doc_id)
