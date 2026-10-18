"""Loads markdown guidelines that start with a simple `key: value` front-matter block."""

from __future__ import annotations

import hashlib
from pathlib import Path

from ..models import Document
from .base import BaseLoader, resolve_versions

REQUIRED_FIELDS = ("doc_id", "agency", "title", "year", "version", "topic")


def _parse_front_matter(text: str, path: Path) -> tuple[dict[str, str], str]:
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        raise ValueError(f"{path.name}: missing front matter (file must start with '---')")
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        raise ValueError(f"{path.name}: front matter is not closed with '---'") from None
    meta: dict[str, str] = {}
    for raw in lines[1:end]:
        if not raw.strip():
            continue
        if ":" not in raw:
            raise ValueError(f"{path.name}: bad front-matter line {raw!r}")
        key, _, value = raw.partition(":")
        meta[key.strip()] = value.strip()
    return meta, "\n".join(lines[end + 1 :]).strip()


class MarkdownLoader(BaseLoader):
    def __init__(self, directory: Path | str):
        self.directory = Path(directory)

    def load(self) -> list[Document]:
        paths = sorted(self.directory.glob("*.md"))
        if not paths:
            raise FileNotFoundError(f"no .md guideline files found in {self.directory}")
        docs = [self._load_one(p) for p in paths]
        return resolve_versions(docs)

    def _load_one(self, path: Path) -> Document:
        raw = path.read_bytes().replace(b"\r\n", b"\n")  # same hash on Windows checkouts
        meta, body = _parse_front_matter(raw.decode("utf-8"), path)
        missing = [f for f in REQUIRED_FIELDS if not meta.get(f)]
        if missing:
            raise ValueError(f"{path.name}: missing front-matter fields {missing}")
        if meta["doc_id"] != path.stem:
            raise ValueError(f"{path.name}: doc_id {meta['doc_id']!r} must match the file name")
        if not body:
            raise ValueError(f"{path.name}: empty body")
        return Document(
            doc_id=meta["doc_id"],
            agency=meta["agency"],
            title=meta["title"],
            year=int(meta["year"]),
            version=int(meta["version"]),
            topic=meta["topic"],
            body=body,
            source_path=path.name,
            source_sha256=hashlib.sha256(raw).hexdigest(),
            supersedes=meta.get("supersedes") or None,
            synthetic=meta.get("synthetic", "false").lower() == "true",
        )
