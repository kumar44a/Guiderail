from guiderail.chunker import chunk_corpus, chunk_document, dedupe_within_document
from guiderail.loaders import MarkdownLoader
from tests.conftest import write_doc


def _doc(tmp_path, body, doc_id="who-test-2024"):
    write_doc(tmp_path, doc_id, body=body)
    return MarkdownLoader(tmp_path).load()[0]


def test_chunks_carry_section_and_metadata(tmp_path):
    doc = _doc(tmp_path, "## Scope\nApplies to all staff.\n\n## Recommendations\n- Wash hands.\n- Wear gloves.")
    chunks = chunk_document(doc)
    assert [c.section for c in chunks] == ["Scope", "Recommendations"]
    assert chunks[0].text == "Applies to all staff."
    assert chunks[1].text == "Wash hands.\nWear gloves."
    assert all(c.agency == "WHO" and c.year == 2024 and c.is_latest for c in chunks)
    assert [c.position for c in chunks] == [0, 1]


def test_chunk_never_crosses_a_section(tmp_path):
    doc = _doc(tmp_path, "## A\n- one two three.\n\n## B\n- four five six.")
    assert [c.section for c in chunk_document(doc, max_words=100)] == ["A", "B"]


def test_long_section_is_split_on_unit_boundaries(tmp_path):
    bullets = "\n".join(f"- bullet number {i} has exactly seven words." for i in range(10))
    doc = _doc(tmp_path, f"## Recommendations\n{bullets}")
    chunks = chunk_document(doc, max_words=20)
    assert len(chunks) > 1
    assert all(len(c.text.split()) <= 20 for c in chunks)
    assert sum(c.text.count("bullet number") for c in chunks) == 10  # nothing lost or cut mid-bullet


def test_oversized_unit_is_hard_split_without_losing_words(tmp_path):
    # Real PDF tables extract as one long run with no sentence boundary (found on real data:
    # a 1,834-word chunk). The chunker must split it, keeping every word.
    doc = _doc(tmp_path, "## A\n- " + " ".join(f"w{i}" for i in range(50)))
    chunks = chunk_document(doc, max_words=10)
    assert len(chunks) == 5 and all(len(c.text.split()) <= 10 for c in chunks)
    assert " ".join(c.text for c in chunks).split() == [f"w{i}" for i in range(50)]


def test_prose_is_split_into_sentences_then_packed(tmp_path):
    doc = _doc(tmp_path, "## Scope\nFirst sentence here. Second sentence here. Third sentence here.")
    assert len(chunk_document(doc, max_words=6)) == 2   # two 3-word sentences fit per chunk
    chunks = chunk_document(doc, max_words=5)           # now only one fits
    assert [c.text for c in chunks] == [
        "First sentence here.", "Second sentence here.", "Third sentence here."]


def test_short_document_gives_a_single_chunk(tmp_path):
    doc = _doc(tmp_path, "## Recommendations\n- Bag linen at the point of use.")
    assert len(chunk_document(doc)) == 1


def test_text_before_first_heading_is_preamble(tmp_path):
    doc = _doc(tmp_path, "Intro text.\n\n## Scope\nBody.")
    assert chunk_document(doc)[0].section == "Preamble"


def test_chunk_ids_are_unique_and_stable(tmp_path):
    bullets = "\n".join(f"- bullet number {i} has exactly seven words." for i in range(10))
    doc = _doc(tmp_path, f"## Recommendations\n{bullets}")
    ids = [c.chunk_id for c in chunk_document(doc, max_words=20)]
    assert len(ids) == len(set(ids))
    assert ids == [c.chunk_id for c in chunk_document(doc, max_words=20)]
    assert ids[0] == "who-test-2024#recommendations-0"


def test_no_empty_chunks(tmp_path):
    doc = _doc(tmp_path, "## Empty\n\n## Real\n- Something.")
    assert all(c.text.strip() for c in chunk_document(doc))


def test_dedupe_only_within_a_document(tmp_path):
    write_doc(tmp_path, "who-a", body="## A\n- same text.\n\n## B\n- same text.")
    write_doc(tmp_path, "who-b", body="## A\n- same text.")
    docs = MarkdownLoader(tmp_path).load()
    chunks, removed = chunk_corpus(docs)
    assert removed == 1                      # who-a's repeat
    assert sorted(c.doc_id for c in chunks) == ["who-a", "who-b"]  # who-b keeps its copy
    again, removed_again = dedupe_within_document(chunks)
    assert removed_again == 0 and again == chunks


def test_superseded_flag_propagates(tmp_path):
    write_doc(tmp_path, "who-old")
    write_doc(tmp_path, "who-new", supersedes="who-old")
    chunks, _ = chunk_corpus(MarkdownLoader(tmp_path).load())
    flags = {c.doc_id: c.is_latest for c in chunks}
    assert flags == {"who-new": True, "who-old": False}
