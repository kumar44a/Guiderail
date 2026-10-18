"""Build, save and load the FAISS index plus its manifest.

Everything written here is deterministic: no timestamps, sorted JSON keys, LF newlines.
The manifest records content hashes so two builds can be proven identical and so the
README can quote counts from an artifact instead of typing them.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

import faiss
import numpy as np

from .embeddings import DIM, METHOD, embed_batch
from .models import Chunk, Document

INDEX_FILE = "guiderail.faiss"
CHUNKS_FILE = "chunks.jsonl"
MANIFEST_FILE = "manifest.json"
SCHEMA_VERSION = 1


@dataclass
class LoadedIndex:
    index: faiss.Index
    chunks: list[Chunk]
    manifest: dict


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _write_text(path: Path, text: str) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def build_index(chunks: list[Chunk]) -> tuple[faiss.IndexFlatIP, np.ndarray]:
    """Exact inner-product search over unit vectors, i.e. cosine similarity."""
    vectors = embed_batch([c.embed_text for c in chunks])
    index = faiss.IndexFlatIP(DIM)
    index.add(vectors)
    return index, vectors


def build_manifest(
    docs: list[Document],
    chunks: list[Chunk],
    vectors: np.ndarray,
    index: faiss.Index,
    chunks_jsonl: str,
    duplicates_removed: int,
    max_words: int,
) -> dict:
    corpus_digest = _sha256("\n".join(f"{d.doc_id}:{d.source_sha256}" for d in docs).encode("utf-8"))
    return {
        "schema_version": SCHEMA_VERSION,
        "embedding": {"method": METHOD, "dim": DIM},
        "chunking": {"max_words": max_words, "duplicates_removed": duplicates_removed},
        "counts": {
            "documents": len(docs),
            "superseded_documents": sum(1 for d in docs if not d.is_latest),
            "chunks": len(chunks),
            "agencies": dict(sorted(Counter(d.agency for d in docs).items())),
        },
        "hashes": {
            "corpus_sha256": corpus_digest,
            "chunks_sha256": _sha256(chunks_jsonl.encode("utf-8")),
            "vectors_sha256": _sha256(np.ascontiguousarray(vectors).tobytes()),
            "index_sha256": _sha256(faiss.serialize_index(index).tobytes()),
        },
    }


def save_index(
    out_dir: Path | str,
    docs: list[Document],
    chunks: list[Chunk],
    duplicates_removed: int = 0,
    max_words: int = 80,
) -> dict:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    index, vectors = build_index(chunks)
    chunks_jsonl = "".join(
        json.dumps(c.to_dict(), sort_keys=True, ensure_ascii=False) + "\n" for c in chunks
    )
    manifest = build_manifest(docs, chunks, vectors, index, chunks_jsonl, duplicates_removed, max_words)
    faiss.write_index(index, str(out / INDEX_FILE))
    _write_text(out / CHUNKS_FILE, chunks_jsonl)
    _write_text(out / MANIFEST_FILE, json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    return manifest


def load_index(directory: Path | str) -> LoadedIndex:
    d = Path(directory)
    for name in (INDEX_FILE, CHUNKS_FILE, MANIFEST_FILE):
        if not (d / name).exists():
            raise FileNotFoundError(f"{d / name} not found; run scripts/pipeline.py first")
    index = faiss.read_index(str(d / INDEX_FILE))
    chunks = [
        Chunk.from_dict(json.loads(line))
        for line in (d / CHUNKS_FILE).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    manifest = json.loads((d / MANIFEST_FILE).read_text(encoding="utf-8"))
    if index.ntotal != len(chunks):
        raise ValueError(f"index has {index.ntotal} vectors but chunks.jsonl has {len(chunks)}")
    return LoadedIndex(index=index, chunks=chunks, manifest=manifest)
