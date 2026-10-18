import json

import pytest

from guiderail.chunker import chunk_corpus
from guiderail.loaders import PdfLoader
from guiderail.loaders.pdf_loader import (
    SOURCES_FILE, clean_pages, is_heading, pages_to_markdown,
)


def make_pdf(pages: list[list[str]]) -> bytes:
    """Build a small valid text PDF (Helvetica) so the loader is tested on a real PDF."""
    def esc(s: str) -> str:
        return s.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")

    n = len(pages)
    kids = " ".join(f"{4 + 2 * i} 0 R" for i in range(n))
    objs = [b"<< /Type /Catalog /Pages 2 0 R >>",
            f"<< /Type /Pages /Kids [{kids}] /Count {n} >>".encode(),
            b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"]
    for i, lines in enumerate(pages):
        objs.append(f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents {5 + 2 * i} 0 R "
                    f"/Resources << /Font << /F1 3 0 R >> >> >>".encode())
        ops = "BT /F1 11 Tf 14 TL 50 740 Td " + " ".join(f"({esc(l)}) Tj T*" for l in lines) + " ET"
        stream = ops.encode("latin-1")
        objs.append(b"<< /Length %d >>\nstream\n" % len(stream) + stream + b"\nendstream")
    out = bytearray(b"%PDF-1.4\n")
    offsets = []
    for i, body in enumerate(objs, start=1):
        offsets.append(len(out))
        out += f"{i} 0 obj\n".encode() + body + b"\nendobj\n"
    xref = len(out)
    out += f"xref\n0 {len(objs) + 1}\n".encode() + b"0000000000 65535 f \n"
    out += b"".join(f"{o:010d} 00000 n \n".encode() for o in offsets)
    out += f"trailer\n<< /Size {len(objs) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode()
    return bytes(out)


def entry(**over):
    base = {"file": "a.pdf", "doc_id": "cdc-test-2020", "agency": "CDC", "title": "Test", "year": 2020,
            "version": 1, "topic": "testing"}
    return {**base, **over}


def write_sources(directory, documents, excluded=()):
    (directory / SOURCES_FILE).write_text(
        json.dumps({"documents": documents, "excluded": list(excluded)}), encoding="utf-8")


PAGES = [
    ["Test Guideline Header", "1. Hand Hygiene", "Clean hands before touching a patient. Use alcohol rub when",
     "hands are not visibly soiled.", "Page 1"],
    ["Test Guideline Header", "2. Personal Protective Equipment", "Wear gloves when contact with blood is likely.",
     "Remove gloves before leaving the room.", "Page 2"],
    ["Test Guideline Header", "3. Vaccination", "Store vaccines between 2 and 8 degrees Celsius.", "Page 3"],
    ["Test Guideline Header", "4. Cleaning", "Clean high-touch surfaces twice a day.", "Page 4"],
    ["Test Guideline Header", "5. Waste", "Place sharps in a puncture-resistant container.", "Page 5"],
]


# ---------- pure cleaning logic ----------

def test_headings_recognised():
    for line in ("1. Hand Hygiene", "2.1 Standard Precautions", "EXECUTIVE SUMMARY", "Executive Summary",
                 "Temperature Monitoring"):
        assert is_heading(line), line


def test_non_headings_rejected():
    for line in (
        "Clean hands before touching a patient.",                       # sentence
        "3. The successful experience with Standard Precautions, first recommended in the",  # wrapped list item
        "HARRELL, Lizzie J., PhD, D(ABMM)",                              # author list
        "Parvovirus B19)",                                               # unbalanced bracket
        "Bavarian Nordic: 844-422-8274",                                 # contact detail
        "• a bullet point", "wear gloves", "Rub hands for",             # bullet, lowercase, ends in function word
        "info@example.org", "x",
    ):
        assert not is_heading(line), line


WORDS = ["alpha", "bravo", "charlie", "delta", "echo", "foxtrot", "golf"]


def test_repeated_headers_and_page_numbers_are_removed():
    body = lambda w: [f"Opening line about {w}.", "Middle line one.", "Middle line two.", f"Closing line about {w}."]
    pages = ["\n".join(["Running Header", *body(w), f"Page {i} of 9"]) for i, w in enumerate(WORDS, start=1)]
    cleaned, removed = clean_pages(pages)
    assert removed == 14                                    # header + page number on each of 7 pages
    assert all(lines == body(w) for lines, w in zip(cleaned, WORDS))


def test_repeated_looking_lines_in_the_middle_of_a_page_are_kept():
    # Differ only in digits and repeat on every page, but sit mid-page: body text, not headers.
    body = lambda w: [f"Opening line about {w}.", f"Second line about {w}.", "Table 1 shows doses.",
                      "Table 2 shows doses.", "Table 3 shows doses.", f"Penultimate line about {w}.",
                      f"Closing line about {w}."]
    pages = ["\n".join(body(w)) for w in WORDS]
    cleaned, removed = clean_pages(pages)
    assert removed == 0 and all("Table 2 shows doses." in lines for lines in cleaned)


def test_repeat_removal_needs_enough_pages():
    cleaned, removed = clean_pages(["Header\nA", "Header\nB"])
    assert removed == 0 and cleaned[0] == ["Header", "A"]


def test_sections_carry_page_numbers_and_reflow_joins_wrapped_lines():
    result = pages_to_markdown(["\n".join(p) for p in PAGES])
    assert "## 1. Hand Hygiene (p. 1)" in result.body
    assert "## 3. Vaccination (p. 3)" in result.body
    assert ("Use alcohol rub when hands are not visibly soiled." in result.body)    # wrapped line rejoined
    assert result.stats.pages == 5 and result.stats.repeated_lines_removed >= 5
    assert result.stats.headings_detected == 5 and not result.stats.page_fallback


def test_hyphenated_line_breaks_are_rejoined():
    result = pages_to_markdown(["Overview of Practice\nThe infec-\ntion control team reviews the plan each year.\n"
                                "Second Heading Here\nSome body text that is long enough to keep.\n"
                                "Third Heading Here\nMore body text that is long enough to keep."])
    assert "infection control team" in result.body


def test_bullets_become_markdown_bullets():
    body = pages_to_markdown(["Recommendations Section\n• Wash hands first\n• Wear a gown today and after\n"
                              "Another Heading Here\nBody text that is long enough to be kept here.\n"
                              "Third Heading Here\nMore body text that is long enough to be kept."]).body
    assert "- Wash hands first\n- Wear a gown today and after" in body


def test_documents_without_headings_fall_back_to_one_section_per_page():
    result = pages_to_markdown(["just some plain running text on page one that goes on",
                                "and more plain running text on page two that goes on"])
    assert result.stats.page_fallback
    assert result.body.startswith("## Page 1") and "## Page 2" in result.body


def test_duplicate_headings_get_unique_labels():
    pages = ["Overview Section\nbody one is long enough to be kept as text.\n"
             "Overview Section\nbody two is long enough to be kept as text.\n"
             "Another Heading\nbody three is long enough to be kept as text.\n"
             "Third Heading\nbody four is long enough to be kept as text."]
    headings = [l for l in pages_to_markdown(pages).body.split("\n") if l.startswith("## ")]
    assert len(headings) == len(set(headings))


# ---------- loader on real (generated) PDFs ----------

def test_loader_reads_a_real_pdf_end_to_end(tmp_path):
    (tmp_path / "a.pdf").write_bytes(make_pdf(PAGES))
    write_sources(tmp_path, [entry()])
    loader = PdfLoader(tmp_path)
    (doc,) = loader.load()
    assert doc.doc_id == "cdc-test-2020" and doc.agency == "CDC" and not doc.synthetic
    assert "## 2. Personal Protective Equipment (p. 2)" in doc.body
    chunks, _ = chunk_corpus([doc])
    assert any("2 and 8 degrees" in c.text and "Vaccination" in c.section for c in chunks)
    assert len({c.chunk_id for c in chunks}) == len(chunks)
    assert loader.stats["cdc-test-2020"].pages == 5


def test_loader_is_deterministic(tmp_path):
    (tmp_path / "a.pdf").write_bytes(make_pdf(PAGES))
    write_sources(tmp_path, [entry()])
    first, second = PdfLoader(tmp_path).load()[0], PdfLoader(tmp_path).load()[0]
    assert first == second and len(first.source_sha256) == 64


def test_excluded_files_are_reported_not_loaded(tmp_path):
    (tmp_path / "a.pdf").write_bytes(make_pdf(PAGES))
    (tmp_path / "fr.pdf").write_bytes(b"not read at all")
    write_sources(tmp_path, [entry()], excluded=[{"file": "fr.pdf", "reason": "French"}])
    loader = PdfLoader(tmp_path)
    assert [d.doc_id for d in loader.load()] == ["cdc-test-2020"]
    assert loader.excluded == [{"file": "fr.pdf", "reason": "French"}]


def test_error_pages_saved_as_pdf_are_rejected(tmp_path):
    (tmp_path / "a.pdf").write_bytes(b"<!DOCTYPE html><html>403 Forbidden</html>")
    write_sources(tmp_path, [entry()])
    with pytest.raises(ValueError, match="not a PDF"):
        PdfLoader(tmp_path).load()


@pytest.mark.parametrize("problem, match", [
    ("no_sources", "sources.json"),
    ("missing_field", "missing"),
    ("missing_file", "not found"),
    ("empty", "lists no documents"),
])
def test_bad_configuration_fails_clearly(tmp_path, problem, match):
    if problem == "missing_field":
        write_sources(tmp_path, [entry(topic="")])
    elif problem == "missing_file":
        write_sources(tmp_path, [entry(file="ghost.pdf")])
    elif problem == "empty":
        write_sources(tmp_path, [])
    with pytest.raises((FileNotFoundError, ValueError), match=match):
        PdfLoader(tmp_path).load()


def test_supersedes_works_for_pdf_documents(tmp_path):
    (tmp_path / "a.pdf").write_bytes(make_pdf(PAGES))
    (tmp_path / "b.pdf").write_bytes(make_pdf(PAGES))
    write_sources(tmp_path, [entry(), entry(file="b.pdf", doc_id="cdc-test-2024", year=2024, version=2,
                                            supersedes="cdc-test-2020")])
    docs = {d.doc_id: d for d in PdfLoader(tmp_path).load()}
    assert docs["cdc-test-2020"].superseded_by == "cdc-test-2024"


# ---------- glyph cleaning ----------

def test_ligature_characters_are_expanded():
    from guiderail.loaders.pdf_loader import clean_glyphs
    assert clean_glyphs("the ﬁve moments, body ﬂuids, signiﬁcant, eﬃcient") == \
        "the five moments, body fluids, significant, efficient"


def test_unmapped_glyph_placeholders_are_removed_but_plain_slashes_survive():
    from guiderail.loaders.pdf_loader import clean_glyphs
    assert clean_glyphs("/g131/g3 access to soap") == " access to soap"
    assert clean_glyphs("tap/faucet and 20/30 seconds and and/or") == "tap/faucet and 20/30 seconds and and/or"

