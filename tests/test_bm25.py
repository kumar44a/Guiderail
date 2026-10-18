import numpy as np

from guiderail.bm25 import Bm25, reciprocal_rank_fusion
from guiderail.models import Chunk
from guiderail.retriever import Retriever
from tests.conftest import make_loaded


def chunk(i, text, section="S"):
    return Chunk(f"d#s-{i}", "d", "WHO", "T", 2024, 1, "t", section, i, text, True)


CHUNKS = [chunk(0, "Wash hands with soap and water for forty seconds."),
          chunk(1, "Alcohol-based handrub needs twenty seconds to dry."),
          chunk(2, "Store vaccines in a refrigerator between two and eight degrees."),
          chunk(3, "Handrub dispensers belong at the point of care.")]


def test_rank_orders_by_term_overlap_and_prefers_rarer_terms():
    bm = Bm25(CHUNKS)
    ranked = [i for i, _ in bm.rank(["handrub", "dispens"], 4)]
    assert ranked[0] == 3 and ranked[1] == 1
    assert [i for i, _ in bm.rank(["refrigerator"], 4)] == [2]


def test_rank_honours_the_allowed_filter_limit_and_unknown_terms():
    bm = Bm25(CHUNKS)
    assert [i for i, _ in bm.rank(["handrub"], 4, allowed=lambda i: i != 3)] == [1]
    assert len(bm.rank(["second", "water", "handrub"], 2)) == 2
    assert bm.rank(["nonexistentterm"], 4) == [] and bm.rank([], 4) == []


def test_rank_is_deterministic_and_breaks_ties_by_position():
    twins = [chunk(0, "alpha beta"), chunk(1, "alpha beta")]
    assert [i for i, _ in Bm25(twins).rank(["alpha"], 2)] == [0, 1]
    assert Bm25(CHUNKS).rank(["handrub", "second"], 4) == Bm25(CHUNKS).rank(["handrub", "second"], 4)


def test_fusion_rewards_agreement_and_is_stable():
    assert reciprocal_rank_fusion([[1, 2, 3], [3, 1, 9]])[:3] == [1, 3, 2]   # 1 and 3 appear in both lists
    assert reciprocal_rank_fusion([[5], [5]]) == [5]
    assert reciprocal_rank_fusion([[1, 2], [2, 1]]) == [1, 2]          # exact tie -> lower id first
    assert reciprocal_rank_fusion([]) == []


def test_hybrid_search_keeps_the_version_policy_and_is_deterministic(loaded):
    plain = Retriever(loaded, rerank_weight=0.5)
    hybrid = Retriever(loaded, rerank_weight=0.5, hybrid=True)
    q = "return to work after respiratory illness"
    a, b = hybrid.search(q, top_k=10), hybrid.search(q, top_k=10)
    assert [h.chunk.chunk_id for h in a] == [h.chunk.chunk_id for h in b]
    assert len(a) == 10 and all(h.chunk.is_latest for h in a)
    assert "who-hand-hygiene-2019" not in {h.chunk.doc_id for h in hybrid.search("hand rub", top_k=20)}
    assert all(-1.0 <= h.score <= 1.0 for h in a)


def test_hybrid_can_surface_a_chunk_the_dense_search_ranks_outside_its_pool(tmp_path, monkeypatch):
    from guiderail import retriever as r
    filler = {f"who-f{i}": "## Notes\n- General infection control notes number %d about gowns masks and gloves for staff." % i for i in range(12)}
    filler["who-target"] = "## Notes\n- Zephyrine rinse must be applied to clean skin before the incision."
    loaded = make_loaded(tmp_path, filler)
    monkeypatch.setattr(r, "FUSION_POOL", 2)           # a tiny dense pool: the target cannot get in through FAISS alone
    dense_only = [h.chunk.doc_id for h in Retriever(loaded).search("zephyrine rinse", top_k=3)]
    hybrid = [h.chunk.doc_id for h in Retriever(loaded, hybrid=True).search("zephyrine rinse", top_k=3)]
    assert "who-target" in hybrid
