import pytest
from fastapi.testclient import TestClient

from guiderail.api import create_app


@pytest.fixture(scope="module")
def client(index_path):
    with TestClient(create_app(index_dir=index_path, threshold=0.6)) as c:
        yield c


def test_qa_returns_exactly_the_contract_fields(client):
    r = client.post("/qa", json={"question": "What temperature should vaccines be stored at?", "top_k": 5})
    assert r.status_code == 200
    body = r.json()
    assert set(body) == {"answer", "citations", "confidence", "status"}
    assert body["status"] in {"validated", "needs_review"} and 0 <= body["confidence"] <= 1
    assert body["status"] == "validated" and body["citations"][0]["doc_id"] == "cdc-vaccination-cold-chain-2024"


def test_top_k_defaults_when_omitted(client):
    assert client.post("/qa", json={"question": "What is shared decision making?"}).status_code == 200


def test_out_of_corpus_question_returns_needs_review_not_an_error(client):
    r = client.post("/qa", json={"question": "How do I bake a chocolate cake?"})
    assert r.status_code == 200
    assert r.json()["status"] == "needs_review" and r.json()["citations"] == []


def test_debug_flag_adds_validation_details_only_when_asked(client):
    q = {"question": "What order do I take off PPE?"}
    assert "debug" not in client.post("/qa", json=q).json()
    debug = client.post("/qa?debug=true", json=q).json()["debug"]
    assert "validation" in debug and "evidence" in debug


@pytest.mark.parametrize("payload", [
    {},
    {"question": ""},
    {"question": "   "},
    {"question": "x" * 1001},
    {"question": "hand hygiene", "top_k": 0},
    {"question": "hand hygiene", "top_k": 21},
    {"question": "hand hygiene", "top_k": "many"},
    {"question": 123},
])
def test_invalid_requests_get_422(client, payload):
    assert client.post("/qa", json=payload).status_code == 422


def test_wrong_method_is_405(client):
    assert client.get("/qa").status_code == 405


def test_health_reports_index_identity(client, index_path):
    import json

    manifest = json.loads((index_path / "manifest.json").read_text(encoding="utf-8"))
    body = client.get("/health").json()
    assert body["status"] == "ok" and body["generator"] == "extractive" and body["threshold"] == 0.6
    assert body["index_sha256"] == manifest["hashes"]["index_sha256"]
    assert body["documents"] == manifest["counts"]["documents"] and body["chunks"] == manifest["counts"]["chunks"]


def test_openapi_documents_both_routes(client):
    paths = client.get("/openapi.json").json()["paths"]
    assert "/qa" in paths and "/health" in paths


def test_service_unavailable_before_startup(index_path):
    client = TestClient(create_app(index_dir=index_path))      # no `with`: lifespan never runs
    assert client.post("/qa", json={"question": "hand hygiene"}).status_code == 503


def test_missing_index_fails_fast_with_a_clear_message(tmp_path):
    with pytest.raises(FileNotFoundError, match="pipeline.py"):
        with TestClient(create_app(index_dir=tmp_path)):
            pass
