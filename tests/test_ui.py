"""Drives ui/app.py headlessly with Streamlit's AppTest, routing its HTTP calls into the real FastAPI app."""

import httpx
import pytest
from fastapi.testclient import TestClient
from streamlit.testing.v1 import AppTest

from guiderail.api import create_app
from tests.conftest import ROOT

UI = str(ROOT / "ui" / "app.py")


@pytest.fixture()
def routed(index_path, monkeypatch):
    with TestClient(create_app(index_dir=index_path, threshold=0.6)) as client:
        def strip(url):
            return "/" + url.split("//", 1)[1].split("/", 1)[1]

        monkeypatch.setattr(httpx, "get", lambda url, **kw: client.get(strip(url)))
        monkeypatch.setattr(httpx, "post", lambda url, **kw: client.post(strip(url), params=kw.get("params"), json=kw.get("json")))
        yield client


def run_question(text: str) -> AppTest:
    at = AppTest.from_file(UI, default_timeout=30).run()
    at.text_input[0].set_value(text)
    at.button[0].click()
    return at.run()


def test_sidebar_shows_service_health(routed):
    at = AppTest.from_file(UI, default_timeout=30).run()
    assert not at.exception
    assert any("API online" in s.value for s in at.success)


def test_validated_answer_is_shown_with_citations(routed):
    at = run_question("What temperature should refrigerated vaccines be stored at?")
    assert not at.exception
    assert any(s.value == "validated" for s in at.success)
    assert len(at.dataframe) == 1


def test_out_of_corpus_question_shows_needs_review(routed):
    at = run_question("How do I bake a chocolate cake?")
    assert not at.exception
    assert any(w.value == "needs_review" for w in at.warning)
    assert any("not validated" in i.value for i in at.info)


def test_blank_question_is_rejected_before_calling_the_api(routed):
    at = run_question("   ")
    assert any("Type a question" in w.value for w in at.warning)


def test_unreachable_api_is_reported_not_raised(monkeypatch):
    def boom(*a, **k):
        raise httpx.ConnectError("refused")

    monkeypatch.setattr(httpx, "get", boom)
    monkeypatch.setattr(httpx, "post", boom)
    at = run_question("anything")
    assert not at.exception
    assert any("not reachable" in e.value or "Could not reach" in e.value for e in at.error)
