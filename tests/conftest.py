from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CORPUS_DIR = ROOT / "data" / "guidelines"


@pytest.fixture(scope="session")
def corpus_dir() -> Path:
    return CORPUS_DIR


def write_doc(directory: Path, doc_id: str, *, supersedes: str = "", body: str | None = None,
              extra_front: str = "") -> Path:
    body = body if body is not None else "## Recommendations\n- Do the first thing.\n- Do the second thing."
    text = (
        "---\n"
        f"doc_id: {doc_id}\nagency: WHO\ntitle: Test Guideline\nyear: 2024\nversion: 1\n"
        f"topic: testing\nsupersedes: {supersedes}\nsynthetic: true\n{extra_front}"
        "---\n\n"
        f"{body}\n"
    )
    path = directory / f"{doc_id}.md"
    path.write_text(text, encoding="utf-8")
    return path


@pytest.fixture(scope="session")
def index_path(corpus_dir, tmp_path_factory):
    from guiderail.chunker import chunk_corpus
    from guiderail.index import save_index
    from guiderail.loaders import MarkdownLoader

    out = tmp_path_factory.mktemp("session-index")
    docs = MarkdownLoader(corpus_dir).load()
    chunks, removed = chunk_corpus(docs)
    save_index(out, docs, chunks, duplicates_removed=removed)
    return out


@pytest.fixture(scope="session")
def loaded(index_path):
    from guiderail.index import load_index

    return load_index(index_path)


@pytest.fixture(scope="session")
def service(loaded):
    from guiderail.service import QAService

    return QAService(loaded)


def make_loaded(tmp_path, docs: dict[str, str]):
    """Build a tiny index from {doc_id: body} for focused retriever tests."""
    from guiderail.chunker import chunk_corpus
    from guiderail.index import load_index, save_index
    from guiderail.loaders import MarkdownLoader

    src = tmp_path / "src"
    src.mkdir()
    for doc_id, body in docs.items():
        write_doc(src, doc_id, body=body)
    loaded_docs = MarkdownLoader(src).load()
    chunks, removed = chunk_corpus(loaded_docs, max_words=30)
    save_index(tmp_path / "idx", loaded_docs, chunks, duplicates_removed=removed)
    return load_index(tmp_path / "idx")
