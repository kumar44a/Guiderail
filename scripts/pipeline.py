"""Build the GuideRail index: load -> chunk -> embed -> FAISS -> manifest.

    python scripts/pipeline.py                      # build into ./index
    python scripts/pipeline.py --check-determinism  # build twice, compare hashes
"""

from __future__ import annotations

import argparse
import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from guiderail.chunker import DEFAULT_MAX_WORDS, chunk_corpus  # noqa: E402
from guiderail.index import save_index  # noqa: E402
from guiderail.loaders import MarkdownLoader, PdfLoader  # noqa: E402


def build(corpus: Path, out: Path, max_words: int | None = None, loader: str = "markdown") -> dict:
    """GUIDERAIL_MAX_WORDS overrides the chunk budget (used by the evaluation to compare chunk sizes)."""
    max_words = max_words or int(os.environ.get("GUIDERAIL_MAX_WORDS", DEFAULT_MAX_WORDS))
    docs = (PdfLoader if loader == "pdf" else MarkdownLoader)(corpus).load()
    chunks, removed = chunk_corpus(docs, max_words)
    return save_index(out, docs, chunks, duplicates_removed=removed, max_words=max_words)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--corpus", type=Path, default=ROOT / "data" / "guidelines")
    parser.add_argument("--out", type=Path, default=ROOT / "index")
    parser.add_argument("--max-words", type=int, default=DEFAULT_MAX_WORDS)
    parser.add_argument("--check-determinism", action="store_true")
    parser.add_argument("--loader", choices=["markdown", "pdf"], default="markdown")
    parser.add_argument("--real", action="store_true",
                        help="index the real PDFs: --loader pdf --corpus data/real --out index_real")
    args = parser.parse_args()
    if args.real:
        args.loader = "pdf"
        if args.corpus == ROOT / "data" / "guidelines":
            args.corpus = ROOT / "data" / "real"
        if args.out == ROOT / "index":
            args.out = ROOT / "index_real"

    manifest = build(args.corpus, args.out, args.max_words, args.loader)
    counts = manifest["counts"]
    print(f"Indexed {counts['documents']} documents ({counts['superseded_documents']} superseded) "
          f"into {counts['chunks']} chunks -> {args.out}")
    print(f"index_sha256 = {manifest['hashes']['index_sha256']}")

    if args.check_determinism:
        with tempfile.TemporaryDirectory() as tmp:
            second = build(args.corpus, Path(tmp), args.max_words, args.loader)
        if second["hashes"] != manifest["hashes"]:
            print("DETERMINISM CHECK FAILED: hashes differ between builds", file=sys.stderr)
            for key in manifest["hashes"]:
                if manifest["hashes"][key] != second["hashes"][key]:
                    print(f"  {key}: {manifest['hashes'][key]} != {second['hashes'][key]}", file=sys.stderr)
            return 1
        print("Determinism check passed: two independent builds produced identical hashes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
