import json
import subprocess
import sys

import numpy as np
import pytest

from guiderail.chunker import chunk_corpus
from guiderail.embeddings import DIM, embed
from guiderail.index import CHUNKS_FILE, INDEX_FILE, MANIFEST_FILE, load_index, save_index
from guiderail.loaders import MarkdownLoader
from tests.conftest import ROOT


@pytest.fixture(scope="module")
def built(corpus_dir, tmp_path_factory):
    out = tmp_path_factory.mktemp("index")
    docs = MarkdownLoader(corpus_dir).load()
    chunks, removed = chunk_corpus(docs)
    manifest = save_index(out, docs, chunks, duplicates_removed=removed)
    return out, docs, chunks, manifest


def test_manifest_counts_match_the_artifacts(built):
    out, docs, chunks, manifest = built
    assert manifest["counts"]["documents"] == len(docs)
    assert manifest["counts"]["chunks"] == len(chunks)
    assert sum(manifest["counts"]["agencies"].values()) == len(docs)
    on_disk = json.loads((out / MANIFEST_FILE).read_text(encoding="utf-8"))
    assert on_disk == manifest


def test_manifest_has_no_timestamps(built):
    _, _, _, manifest = built
    assert "time" not in json.dumps(manifest).lower()


def test_load_roundtrip(built):
    out, _, chunks, _ = built
    loaded = load_index(out)
    assert loaded.index.ntotal == len(chunks) and loaded.index.d == DIM
    assert [c.chunk_id for c in loaded.chunks] == [c.chunk_id for c in chunks]


def test_in_process_rebuild_is_identical(built, corpus_dir, tmp_path):
    _, docs, chunks, manifest = built
    again = save_index(tmp_path, docs, chunks, duplicates_removed=0)
    assert again["hashes"] == manifest["hashes"]


def test_separate_process_build_is_byte_identical(built, tmp_path):
    """Fresh interpreter, so no shared caches or state can mask nondeterminism."""
    out, *_ = built
    other = tmp_path / "other"
    subprocess.run([sys.executable, str(ROOT / "scripts" / "pipeline.py"), "--out", str(other)],
                   check=True, capture_output=True)
    for name in (CHUNKS_FILE, MANIFEST_FILE, INDEX_FILE):
        assert (out / name).read_bytes() == (other / name).read_bytes(), name


def test_search_returns_on_topic_chunks(built):
    out, *_ = built
    loaded = load_index(out)
    cases = {
        "what temperature should vaccines be stored at": "vaccination-cold-chain",
        "what is shared decision making": "shared-decision-making",
        "how should high-touch surfaces be cleaned": "environmental-cleaning",
    }
    for question, expected in cases.items():
        _, ids = loaded.index.search(embed(question).reshape(1, -1), 3)
        top_docs = {loaded.chunks[i].doc_id for i in ids[0]}
        assert any(expected in d for d in top_docs), (question, top_docs)


def test_out_of_corpus_query_scores_below_in_corpus_query(built):
    out, *_ = built
    loaded = load_index(out)
    best = lambda q: float(loaded.index.search(embed(q).reshape(1, -1), 1)[0][0][0])
    assert best("what temperature should vaccines be stored at") > best("how do I bake a chocolate cake") + 0.1


def test_loading_a_missing_index_gives_a_clear_error(tmp_path):
    with pytest.raises(FileNotFoundError, match="pipeline.py"):
        load_index(tmp_path)


def test_mismatched_index_and_chunks_is_detected(built, tmp_path):
    out, *_ = built
    for name in (INDEX_FILE, CHUNKS_FILE, MANIFEST_FILE):
        (tmp_path / name).write_bytes((out / name).read_bytes())
    lines = (tmp_path / CHUNKS_FILE).read_text(encoding="utf-8").splitlines()
    (tmp_path / CHUNKS_FILE).write_text("\n".join(lines[:-1]) + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="vectors"):
        load_index(tmp_path)


def test_vectors_in_index_are_unit_length(built):
    out, *_ = built
    loaded = load_index(out)
    vectors = loaded.index.reconstruct_n(0, loaded.index.ntotal)
    assert np.allclose(np.linalg.norm(vectors, axis=1), 1.0, atol=1e-5)
