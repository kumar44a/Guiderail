"""Guards on the real synthetic corpus in data/guidelines."""

import pytest

from guiderail.chunker import chunk_corpus
from guiderail.loaders import MarkdownLoader


@pytest.fixture(scope="module")
def docs(corpus_dir):
    return MarkdownLoader(corpus_dir).load()


def test_corpus_has_expected_breadth(docs):
    assert 20 <= len(docs) <= 25
    assert {d.agency for d in docs} == {"WHO", "NIH", "CDC"}
    assert all(d.synthetic for d in docs)


def test_every_document_is_front_matter_complete(docs):
    for d in docs:
        assert d.title and d.topic and 2015 <= d.year <= 2026 and d.version >= 1


def test_superseding_documents_are_newer(docs):
    by_id = {d.doc_id: d for d in docs}
    pairs = [(d, by_id[d.supersedes]) for d in docs if d.supersedes]
    assert pairs, "corpus must contain at least one superseded version (tests version policy)"
    for newer, older in pairs:
        assert newer.year > older.year and newer.version > older.version
        assert newer.topic == older.topic


def test_corpus_contains_the_deliberate_hard_cases(docs):
    topics = [d.topic for d in docs]
    assert topics.count("hand_hygiene") >= 3      # cross-agency + version overlap
    assert topics.count("ppe") >= 2               # near-duplicate wording across agencies
    assert topics.count("grading") >= 2           # differing terminology (low vs insufficient)
    chunks, _ = chunk_corpus(docs)
    sparse = [d for d in docs if sum(1 for c in chunks if c.doc_id == d.doc_id) == 1]
    assert sparse, "corpus must contain a very short document (tests sparse-section fallback)"


def test_all_chunks_have_text_and_unique_ids(docs):
    chunks, _ = chunk_corpus(docs)
    ids = [c.chunk_id for c in chunks]
    assert len(ids) == len(set(ids))
    assert all(c.text.strip() for c in chunks)
