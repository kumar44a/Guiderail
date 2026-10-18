import pytest

from guiderail.loaders import MarkdownLoader, resolve_versions
from tests.conftest import write_doc


def test_loads_front_matter_and_body(tmp_path):
    write_doc(tmp_path, "who-test-2024")
    (doc,) = MarkdownLoader(tmp_path).load()
    assert doc.doc_id == "who-test-2024"
    assert doc.agency == "WHO" and doc.year == 2024 and doc.version == 1
    assert doc.supersedes is None and doc.is_latest
    assert doc.body.startswith("## Recommendations")
    assert len(doc.source_sha256) == 64


def test_supersedes_is_resolved_both_ways(tmp_path):
    write_doc(tmp_path, "who-test-2019")
    write_doc(tmp_path, "who-test-2023", supersedes="who-test-2019")
    docs = {d.doc_id: d for d in MarkdownLoader(tmp_path).load()}
    assert docs["who-test-2019"].superseded_by == "who-test-2023"
    assert not docs["who-test-2019"].is_latest
    assert docs["who-test-2023"].is_latest


def test_documents_are_sorted_by_id(tmp_path):
    for name in ("who-b", "who-a", "who-c"):
        write_doc(tmp_path, name)
    assert [d.doc_id for d in MarkdownLoader(tmp_path).load()] == ["who-a", "who-b", "who-c"]


def test_unknown_supersedes_target_fails(tmp_path):
    write_doc(tmp_path, "who-test-2023", supersedes="who-missing")
    with pytest.raises(ValueError, match="unknown document"):
        MarkdownLoader(tmp_path).load()


def test_double_supersession_fails(tmp_path):
    write_doc(tmp_path, "who-old")
    write_doc(tmp_path, "who-new-a", supersedes="who-old")
    write_doc(tmp_path, "who-new-b", supersedes="who-old")
    with pytest.raises(ValueError, match="superseded by both"):
        MarkdownLoader(tmp_path).load()


def test_missing_front_matter_fails(tmp_path):
    (tmp_path / "bad.md").write_text("## Recommendations\n- x", encoding="utf-8")
    with pytest.raises(ValueError, match="missing front matter"):
        MarkdownLoader(tmp_path).load()


def test_missing_required_field_fails(tmp_path):
    (tmp_path / "bad.md").write_text("---\ndoc_id: bad\nagency: WHO\n---\nbody", encoding="utf-8")
    with pytest.raises(ValueError, match="missing front-matter fields"):
        MarkdownLoader(tmp_path).load()


def test_doc_id_must_match_filename(tmp_path):
    path = write_doc(tmp_path, "who-test-2024")
    path.rename(tmp_path / "other-name.md")
    with pytest.raises(ValueError, match="must match the file name"):
        MarkdownLoader(tmp_path).load()


def test_empty_directory_fails(tmp_path):
    with pytest.raises(FileNotFoundError):
        MarkdownLoader(tmp_path).load()


def test_duplicate_ids_rejected_by_resolver(tmp_path):
    write_doc(tmp_path, "who-test-2024")
    (doc,) = MarkdownLoader(tmp_path).load()
    with pytest.raises(ValueError, match="duplicate doc_id"):
        resolve_versions([doc, doc])


def test_crlf_files_hash_like_lf_files(tmp_path):
    lf, crlf = tmp_path / "lf", tmp_path / "crlf"
    lf.mkdir(), crlf.mkdir()
    path = write_doc(lf, "who-test-2024")
    (crlf / path.name).write_bytes(path.read_bytes().replace(b"\n", b"\r\n"))
    assert MarkdownLoader(lf).load()[0].source_sha256 == MarkdownLoader(crlf).load()[0].source_sha256
