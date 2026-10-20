from pathlib import Path

from guiderail.chunker import chunk_document
from guiderail.loaders import MarkdownLoader, resolve_versions

ROOT = Path(__file__).resolve().parents[1]


def test_v2_keeps_v1_text_verbatim_and_every_document_but_linen_has_enough_chunks():
    v1, v2 = ROOT / "data" / "guidelines", ROOT / "data" / "guidelines_v2"
    for old in v1.glob("*.md"):
        assert (v2 / old.name).read_text(encoding="utf-8").startswith(old.read_text(encoding="utf-8").rstrip("\n")), old.name
    docs = resolve_versions(MarkdownLoader(v2).load())
    for doc in docs:
        n = len(chunk_document(doc))
        if doc.doc_id == "who-linen-laundry-2022":
            assert n == 1
        else:
            assert n >= 6, (doc.doc_id, n)
