import pytest

from guiderail.retriever import Retriever, top_retrieval_score
from tests.conftest import make_loaded

HAND_RUB_Q = "how long should I rub alcohol hand rub"


def test_returns_top_k_sorted_by_score(loaded):
    hits = Retriever(loaded).search(HAND_RUB_Q, top_k=5)
    assert len(hits) == 5
    assert [h.score for h in hits] == sorted((h.score for h in hits), reverse=True)


def test_superseded_documents_are_excluded_by_default(loaded):
    retriever = Retriever(loaded)
    default_docs = {h.chunk.doc_id for h in retriever.search(HAND_RUB_Q, top_k=20)}
    assert "who-hand-hygiene-2019" not in default_docs
    assert "who-hand-hygiene-2023" in default_docs
    with_old = {h.chunk.doc_id for h in retriever.search(HAND_RUB_Q, top_k=20, include_superseded=True)}
    assert "who-hand-hygiene-2019" in with_old


def test_top_k_is_filled_even_when_superseded_chunks_crowd_the_top(loaded):
    hits = Retriever(loaded).search("return to work after respiratory illness symptom onset", top_k=10)
    assert len(hits) == 10
    assert all(h.chunk.is_latest for h in hits)


def test_empty_or_stopword_query_returns_nothing(loaded):
    retriever = Retriever(loaded)
    assert retriever.search("", top_k=5) == []
    assert retriever.search("the of and", top_k=5) == []
    assert retriever.search("hand hygiene", top_k=0) == []


def test_top_k_larger_than_index_is_capped(loaded):
    hits = Retriever(loaded).search("hand hygiene", top_k=20)
    assert len(hits) <= loaded.index.ntotal


def test_top_retrieval_score_ignores_neighbors(loaded):
    hits = Retriever(loaded).search("vaccine storage temperature", top_k=3)
    assert top_retrieval_score(hits) == hits[0].score
    assert top_retrieval_score([]) == 0.0


def test_sparse_chunk_pulls_in_its_neighbor_once(tmp_path):
    loaded = make_loaded(tmp_path, {
        "who-a": "## Scope\nShort scope.\n\n## Recommendations\n- Isolate patients with measles in a negative pressure room "
                 "and restrict visitors to those with documented immunity to measles.",
    })
    retriever = Retriever(loaded)
    hits = retriever.search("short scope", top_k=1)
    assert [h.chunk.section for h in hits] == ["Scope"]
    expanded = retriever.expand_sparse(hits)
    assert [h.via for h in expanded] == ["retrieval", "neighbor"]
    assert expanded[1].chunk.section == "Recommendations"
    assert len(retriever.expand_sparse(expanded)) == 2   # already present, not added again


def test_full_length_chunk_is_not_expanded(tmp_path):
    long_bullet = " ".join(["word"] * 40)
    loaded = make_loaded(tmp_path, {"who-a": f"## Recommendations\n- {long_bullet}\n\n## Notes\n- Another note about measles."})
    retriever = Retriever(loaded)
    hits = retriever.search("word", top_k=1)
    assert retriever.expand_sparse(hits) == hits


# ---------- lexical re-ranking ----------

def test_reranking_lifts_the_fact_bearing_chunk(loaded):
    question = "At what moments should healthcare workers clean their hands during patient care?"
    plain = [h.chunk.chunk_id for h in Retriever(loaded).search(question, top_k=5)]
    reranked = [h.chunk.chunk_id for h in Retriever(loaded, rerank_weight=0.5).search(question, top_k=5)]
    target = "who-hand-hygiene-2023#recommendations-0"
    assert target not in plain and target in reranked        # the five-moments bullet was at rank 10


def test_reranking_keeps_cosine_as_the_reported_score(loaded):
    question = "how long should I rub alcohol hand rub"
    plain = {h.chunk.chunk_id: h.score for h in Retriever(loaded).search(question, top_k=20)}
    for hit in Retriever(loaded, rerank_weight=0.5).search(question, top_k=5):
        assert hit.score == pytest.approx(plain[hit.chunk.chunk_id], abs=1e-6)


def test_reranking_is_deterministic_and_off_by_default_in_the_class(loaded):
    question = "how often should high-touch surfaces be cleaned"
    a = Retriever(loaded, rerank_weight=0.5).search(question, top_k=5)
    b = Retriever(loaded, rerank_weight=0.5).search(question, top_k=5)
    assert [h.chunk.chunk_id for h in a] == [h.chunk.chunk_id for h in b]
    assert Retriever(loaded).rerank_weight == 0.0


def test_reranking_still_honours_the_version_policy(loaded):
    hits = Retriever(loaded, rerank_weight=0.5).search("return to work after respiratory illness", top_k=10)
    assert all(h.chunk.is_latest for h in hits) and len(hits) == 10
