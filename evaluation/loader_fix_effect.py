"""Measure what the two PDF-loader fixes (glyph cleaning, wrapped-sentence headings) changed, per document.

    python evaluation/loader_fix_effect.py     # writes evaluation/reports/loader_fix_effect.json

Runs the loader twice on data/real: with the fixes, and with both switched off.
"""

from __future__ import annotations

import collections
import hashlib
import json

from common import CORPORA, REPORTS

from guiderail.chunker import chunk_corpus
from guiderail.loaders import PdfLoader
from guiderail.loaders import pdf_loader as m


def digest() -> dict:
    chunks, _ = chunk_corpus(PdfLoader(CORPORA["real"]["dir"]).load())
    hashes: dict = {}
    counts: collections.Counter = collections.Counter()
    for c in chunks:
        hashes.setdefault(c.doc_id, hashlib.sha256()).update((c.chunk_id + "\x00" + c.text).encode())
        counts[c.doc_id] += 1
    return {d: {"chunks": counts[d], "sha": hashes[d].hexdigest()[:12]} for d in counts}


def main() -> int:
    after = digest()
    glyphs, wraps = m.clean_glyphs, m._wraps_onto_lowercase
    m.clean_glyphs, m._wraps_onto_lowercase = (lambda t: t), (lambda t: False)
    try:
        before = digest()
    finally:
        m.clean_glyphs, m._wraps_onto_lowercase = glyphs, wraps
    rows = [{"doc_id": d, "chunks_before": before[d]["chunks"], "chunks_after": after[d]["chunks"],
             "unchanged": before[d]["sha"] == after[d]["sha"]} for d in after]
    out = {"description": "PDF loader fixes off vs on", "rows": rows,
           "total_before": sum(r["chunks_before"] for r in rows), "total_after": sum(r["chunks_after"] for r in rows)}
    (REPORTS / "loader_fix_effect.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    for r in rows:
        print(r)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
