from guiderail.generators import ABSTAIN_TEXT, ExtractiveGenerator
from guiderail.lexicon import Lexicon
from guiderail.retriever import Retriever


def _generate(loaded, question, top_k=5):
    retriever = Retriever(loaded)
    hits = retriever.expand_sparse(retriever.search(question, top_k))
    return ExtractiveGenerator(Lexicon(loaded.chunks)).generate(question, hits), hits


def test_answer_is_copied_from_cited_evidence(loaded):
    generated, hits = _generate(loaded, "what temperature should vaccines be stored at")
    assert not generated.abstained and generated.chunk_ids
    evidence = {h.chunk.chunk_id: h.chunk.text for h in hits}
    for sentence in generated.answer.split(". "):
        assert any(sentence.strip(". ") in evidence[cid] for cid in generated.chunk_ids)
    assert "2 and 8 degrees" in generated.answer


def test_cited_ids_exist_and_are_unique(loaded):
    generated, hits = _generate(loaded, "when should staff return to work")
    known = {h.chunk.chunk_id for h in hits}
    assert set(generated.chunk_ids) <= known
    assert len(generated.chunk_ids) == len(set(generated.chunk_ids))


def test_abstains_on_stopword_only_question(loaded):
    generator = ExtractiveGenerator(Lexicon(loaded.chunks))
    assert generator.generate("what is the", []).abstained


def test_abstains_with_no_evidence(loaded):
    assert ExtractiveGenerator(Lexicon(loaded.chunks)).generate("hand hygiene", []).abstained


def test_abstains_when_no_sentence_overlaps_the_question(loaded):
    generated, _ = _generate(loaded, "chocolate cake recipe")
    assert generated.abstained and generated.answer == ABSTAIN_TEXT and generated.chunk_ids == []


def test_sentence_count_is_capped(loaded):
    retriever = Retriever(loaded)
    hits = retriever.search("hand hygiene soap water alcohol rub", top_k=10)
    generated = ExtractiveGenerator(Lexicon(loaded.chunks), max_sentences=2).generate(
        "hand hygiene soap water alcohol rub", hits)
    assert generated.answer.count("\n") == 0
    assert len([s for s in generated.answer.split(". ") if s]) <= 3  # 2 sentences, allowing an inner period


def test_generation_is_deterministic(loaded):
    first, _ = _generate(loaded, "how should high-touch surfaces be cleaned")
    second, _ = _generate(loaded, "how should high-touch surfaces be cleaned")
    assert first == second
