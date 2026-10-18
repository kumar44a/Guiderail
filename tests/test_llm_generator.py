"""LlmGenerator against a fake client. No network, no API key.

The live path is covered by the `live_llm` test at the bottom, which only runs when
ANTHROPIC_API_KEY is set. Until that has been run and logged, the live call is
unverified; these tests only prove request shape and response handling.
"""

import os
from types import SimpleNamespace

import pytest

from guiderail.generators import ABSTAIN_TEXT, GenerationError
from guiderail.generators.llm import FALLBACK_BETA, LlmGenerator
from guiderail.retriever import Retriever

QUESTION = "What temperature should vaccines be stored at?"


class FakeMessages:
    def __init__(self, response=None, error=None):
        self.response, self.error, self.calls = response, error, []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        if self.error:
            raise self.error
        return self.response


class FakeClient:
    def __init__(self, response=None, error=None):
        self.messages = FakeMessages(response, error)
        self.beta = SimpleNamespace(messages=self.messages)


def _response(text, stop_reason="end_turn"):
    block = SimpleNamespace(type="text", text=text)
    return SimpleNamespace(content=[block], stop_reason=stop_reason, _request_id="req_test")


@pytest.fixture(scope="module")
def hits(loaded):
    return Retriever(loaded).search(QUESTION, top_k=3)


def _cid(hits, i=0):
    return hits[i].chunk.chunk_id


def test_request_shape(hits):
    client = FakeClient(_response("Store at 2 to 8 degrees."))
    LlmGenerator(client=client).generate(QUESTION, hits)
    (call,) = client.messages.calls
    assert call["model"] == "claude-opus-5-5"
    assert call["output_config"] == {"effort": "low"}
    assert call["betas"] == [FALLBACK_BETA] and call["fallbacks"] == "default"
    assert "thinking" not in call and "temperature" not in call       # rejected by this model family
    assert "ONLY the evidence" in call["system"]
    content = call["messages"][0]["content"]
    assert QUESTION in content and all(f"[{h.chunk.chunk_id}]" in content for h in hits)


def test_fallbacks_can_be_disabled(hits):
    client = FakeClient(_response("ok [x#y]"))
    LlmGenerator(client=client, use_fallbacks=False).generate(QUESTION, hits)
    (call,) = client.messages.calls
    assert "betas" not in call and "fallbacks" not in call


def test_citations_are_parsed_validated_and_stripped_from_the_answer(hits):
    text = f"Store refrigerated vaccines between 2 and 8 degrees Celsius [{_cid(hits)}] [fake-doc#nope-0]."
    generated = LlmGenerator(client=FakeClient(_response(text))).generate(QUESTION, hits)
    assert generated.chunk_ids == [_cid(hits)]            # hallucinated id dropped
    assert "[" not in generated.answer and generated.answer.startswith("Store refrigerated vaccines")
    assert not generated.abstained


def test_answer_without_citations_has_no_chunk_ids(hits):
    generated = LlmGenerator(client=FakeClient(_response("Store at 2 to 8 degrees."))).generate(QUESTION, hits)
    assert generated.chunk_ids == [] and not generated.abstained


@pytest.mark.parametrize("text", ["NOT_IN_EVIDENCE", "  NOT_IN_EVIDENCE\n", ""])
def test_not_in_evidence_or_empty_means_abstain(hits, text):
    generated = LlmGenerator(client=FakeClient(_response(text))).generate(QUESTION, hits)
    assert generated.abstained and generated.answer == ABSTAIN_TEXT


def test_refusal_means_abstain(hits):
    generated = LlmGenerator(client=FakeClient(_response("whatever", stop_reason="refusal"))).generate(QUESTION, hits)
    assert generated.abstained


def test_api_failure_raises_generation_error(hits):
    with pytest.raises(GenerationError, match="simulated"):
        LlmGenerator(client=FakeClient(error=RuntimeError("simulated"))).generate(QUESTION, hits)


def test_no_evidence_skips_the_api_call():
    client = FakeClient(_response("x"))
    assert LlmGenerator(client=client).generate(QUESTION, []).abstained
    assert client.messages.calls == []


def test_thinking_and_non_text_blocks_are_ignored(hits):
    response = SimpleNamespace(
        content=[SimpleNamespace(type="thinking", thinking=""), SimpleNamespace(type="text", text=f"Answer [{_cid(hits)}]")],
        stop_reason="end_turn")
    generated = LlmGenerator(client=FakeClient(response)).generate(QUESTION, hits)
    assert generated.answer == "Answer" and generated.chunk_ids == [_cid(hits)]


@pytest.mark.live_llm
@pytest.mark.skipif(not os.environ.get("ANTHROPIC_API_KEY"), reason="needs ANTHROPIC_API_KEY")
def test_live_answer_is_grounded_and_cited(hits):
    generator = LlmGenerator()
    generated = generator.generate(QUESTION, hits)
    print("request id:", generator.last_request_id)
    assert not generated.abstained and generated.chunk_ids
