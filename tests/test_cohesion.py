from guiderail import config
from guiderail.index import load_index
from guiderail.retriever import Retriever


def test_default_cohesion_is_the_kept_round_8_value(monkeypatch):
    monkeypatch.delenv("GUIDERAIL_DOC_COHESION", raising=False)
    assert config.doc_cohesion() == 0.5
    monkeypatch.setenv("GUIDERAIL_DOC_COHESION", "0")
    assert config.doc_cohesion() == 0.0


def test_cohesion_changes_order_only_and_keeps_scores_and_members(index_path):
    loaded = load_index(index_path)
    q = "How long should hands be rubbed with hand rub?"
    plain = Retriever(loaded, rerank_weight=0.5, hybrid=True, doc_cohesion=0.0)
    coherent = Retriever(loaded, rerank_weight=0.5, hybrid=True, doc_cohesion=0.5)
    a, b = plain._search_hybrid(q, *_prep(plain, q), 30, False), coherent._search_hybrid(q, *_prep(coherent, q), 30, False)
    assert {h.chunk.chunk_id for h in a} == {h.chunk.chunk_id for h in b}            # same candidates
    assert {h.chunk.chunk_id: h.score for h in a} == {h.chunk.chunk_id: h.score for h in b}   # Hit.score is untouched


def _prep(r, q):
    from guiderail.embeddings import embed
    v = embed(q)
    return v, v
