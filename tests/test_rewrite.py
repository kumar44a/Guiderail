"""Query rewriting against a fake client: request shape, cleaning, failure handling, caching, and that only SEARCH sees the rewrite."""

import json
from types import SimpleNamespace

import numpy as np
import pytest
from fastapi.testclient import TestClient

from guiderail.api import create_app
from guiderail.embeddings import embed
from guiderail.generators import Generated, Generator
from guiderail.retriever import Retriever
from guiderail.rewrite import QueryRewriter, clean_rewrite
from guiderail.service import QAService


class FakeMessages:
    def __init__(self, text="advantages benefits hand rub handrub", error=None):
        self.text, self.error, self.calls = text, error, []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        if self.error:
            raise self.error
        return SimpleNamespace(content=[SimpleNamespace(type="text", text=self.text)], _request_id="req_rw",
                               usage=SimpleNamespace(input_tokens=50, output_tokens=8))


def client(**kw):
    return SimpleNamespace(messages=FakeMessages(**kw))


def test_request_shape():
    c = client()
    assert QueryRewriter(client=c).rewrite("what are the benefits of hand rub") == "advantages benefits hand rub handrub"
    (call,) = c.messages.calls
    assert call["model"] == "claude-haiku-4-5-20251001" and call["max_tokens"] <= 200 and "temperature" not in call
    assert "guideline" in call["system"] and "what are the benefits of hand rub" in call["messages"][0]["content"]
    assert "betas" not in call and "thinking" not in call


@pytest.mark.parametrize("raw, question, expected", [
    ("Keywords: advantages benefits", "q", "advantages benefits"),
    ('"advantages benefits"', "q", "advantages benefits"),
    ("advantages   benefits\nExplanation: I added synonyms.", "q", "advantages benefits"),
    ("", "q", None), ("   \n ", "q", None),
    ("What are the benefits", "what are the benefits", None),            # same as the question: nothing gained
    ("w " * 300, "q", ("w " * 100).strip()),                              # capped at 200 characters
])
def test_clean_rewrite(raw, question, expected):
    assert clean_rewrite(raw, question) == expected


def test_a_failed_call_returns_none_and_is_not_cached():
    rewriter = QueryRewriter(client=client(error=RuntimeError("boom")))
    assert rewriter.rewrite("anything") is None and rewriter.cache == {}


def test_cache_avoids_repeat_calls_and_survives_a_restart(tmp_path):
    path = tmp_path / "cache.json"
    c = client()
    first = QueryRewriter(client=c, cache_path=path)
    assert first.rewrite("q one") == first.rewrite("q one") and len(c.messages.calls) == 1
    again = QueryRewriter(client=client(error=RuntimeError("must not be called")), cache_path=path)
    assert again.rewrite("q one") == "advantages benefits hand rub handrub"
    assert json.loads(path.read_text(encoding="utf-8")) == {"q one": "advantages benefits hand rub handrub"}


def test_unusable_rewrites_are_cached_as_none_so_the_call_is_not_repeated(tmp_path):
    c = client(text="")
    r = QueryRewriter(client=c, cache_path=tmp_path / "c.json")
    assert r.rewrite("q") is None and r.rewrite("q") is None and len(c.messages.calls) == 1


def test_hit_score_stays_the_cosine_to_the_original_question(loaded):
    question = "what are the benefits of hand rub"
    retriever = Retriever(loaded, rerank_weight=0.5, hybrid=True)
    plain = {h.chunk.chunk_id: h.score for h in retriever.search(question, top_k=10)}
    for hit in retriever.search(question, top_k=10, rewrite="vaccine refrigerator temperature"):
        vec = loaded.index.reconstruct(next(i for i, c in enumerate(loaded.chunks) if c.chunk_id == hit.chunk.chunk_id))
        assert hit.score == pytest.approx(float(np.dot(embed(question), vec)), abs=1e-5)
        if hit.chunk.chunk_id in plain:
            assert hit.score == pytest.approx(plain[hit.chunk.chunk_id], abs=1e-5)


def test_the_rewrite_changes_what_is_searched(loaded):
    retriever = Retriever(loaded, rerank_weight=0.5, hybrid=True)
    q = "what is the thing"
    assert [h.chunk.chunk_id for h in retriever.search(q, top_k=5)] != \
           [h.chunk.chunk_id for h in retriever.search(q, top_k=5, rewrite="vaccine refrigerator storage temperature")]


class Spy(Generator):
    name = "spy"

    def __init__(self):
        self.seen = None

    def generate(self, question, hits):
        self.seen = question
        return Generated.abstain()


def test_generator_and_validator_see_only_the_original_question(loaded):
    spy = Spy()
    service = QAService(loaded, generator=spy, rewriter=QueryRewriter(client=client(text="vaccine refrigerator storage")))
    result = service.ask("what is the thing", top_k=5)
    assert spy.seen == "what is the thing"
    assert result.debug["rewrite"] == "vaccine refrigerator storage"


def test_no_rewriter_means_no_rewrite_and_the_debug_field_is_empty(loaded):
    assert QAService(loaded).ask("what temperature for vaccines", top_k=3).debug["rewrite"] is None


def test_api_exposes_the_rewrite_in_debug_only(index_path):
    app = create_app(index_dir=index_path, rewriter=QueryRewriter(client=client(text="vaccine storage temperature")))
    with TestClient(app) as c:
        body = {"question": "how cold for the vaccines"}
        assert "debug" not in c.post("/qa", json=body).json()
        assert c.post("/qa?debug=true", json=body).json()["debug"]["rewrite"] == "vaccine storage temperature"


def test_offline_mode_never_builds_a_rewriter(index_path, monkeypatch):
    monkeypatch.delenv("GUIDERAIL_GENERATOR", raising=False)
    with TestClient(create_app(index_dir=index_path)) as c:
        assert c.app.state.service.rewriter is None


def test_request_arguments_are_accepted_by_the_installed_sdk():
    """The fake client accepts anything, which once hid an argument the real SDK rejects. Check against the real signature."""
    import inspect

    import anthropic

    real = anthropic.Anthropic(api_key="not-a-real-key")          # no network call is made
    c = client()
    QueryRewriter(client=c).rewrite("a question")
    accepted = inspect.signature(real.messages.create).parameters
    has_var_kw = any(p.kind is inspect.Parameter.VAR_KEYWORD for p in accepted.values())
    unknown = [k for k in c.messages.calls[0] if k not in accepted] if not has_var_kw else []
    assert not unknown, f"the installed SDK does not accept: {unknown}"
