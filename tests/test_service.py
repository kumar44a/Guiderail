from guiderail.generators import ABSTAIN_TEXT, GenerationError, Generator
from guiderail.service import QAService


def test_in_corpus_question_is_validated_with_citations(service):
    result = service.ask("What temperature should vaccines be stored at?")
    assert result.status == "validated" and result.confidence >= 0.6
    assert result.citations and result.citations[0]["doc_id"] == "cdc-vaccination-cold-chain-2024"
    assert "2 and 8" in result.answer


def test_out_of_corpus_question_abstains(service):
    result = service.ask("How do I bake a chocolate cake?")
    assert result.status == "needs_review" and result.confidence == 0.0
    assert result.answer == ABSTAIN_TEXT and result.citations == []


def test_plausible_but_unindexed_medical_question_is_flagged(service):
    result = service.ask("What is the recommended dose of amoxicillin for otitis media?")
    assert result.status == "needs_review"


def test_answers_cite_current_guidance_not_superseded_versions(service):
    result = service.ask("When can staff return to work after respiratory illness?")
    cited = {c["doc_id"] for c in result.citations}
    assert cited and cited == {"cdc-isolation-return-to-work-2023"}
    assert "5 days" in result.answer


def test_citation_fields_are_complete(service):
    (first, *_) = service.ask("What is shared decision making?").citations
    assert set(first) == {"chunk_id", "doc_id", "title", "agency", "year", "version", "section", "score"}


def test_debug_block_explains_the_decision(service):
    debug = service.ask("What order do I take off PPE?").debug
    assert debug["generator"] == "extractive"
    assert {"confidence", "coverage", "question_support", "retrieval_relevance"} <= set(debug["validation"])
    assert debug["evidence"] and all("via" in e for e in debug["evidence"])


def test_threshold_is_applied(loaded):
    question = "What temperature should vaccines be stored at?"
    assert QAService(loaded, threshold=0.99).ask(question).status == "validated"      # conf 1.0
    assert QAService(loaded, threshold=0.99).ask("How long should I rub hand rub?").status == "needs_review"


def test_ask_is_deterministic(service):
    a = service.ask("How often should high-touch surfaces be cleaned?")
    b = service.ask("How often should high-touch surfaces be cleaned?")
    assert a == b


class _Boom(Generator):
    name = "boom"

    def generate(self, question, hits):
        raise GenerationError("LLM request failed: simulated outage")


def test_generator_failure_degrades_to_abstention(loaded):
    result = QAService(loaded, generator=_Boom()).ask("What is shared decision making?")
    assert result.status == "needs_review" and result.answer == ABSTAIN_TEXT and result.citations == []
    assert "simulated outage" in result.debug["generator_error"]


class _Uncited(Generator):
    name = "uncited"

    def generate(self, question, hits):
        from guiderail.generators import Generated

        return Generated(answer=hits[0].chunk.text.split("\n")[0], chunk_ids=[])


def test_supported_but_uncited_answer_is_not_validated(loaded):
    result = QAService(loaded, generator=_Uncited()).ask("What temperature should vaccines be stored at?")
    assert result.status == "needs_review" and result.citations == []
