"""Loads real guideline PDFs and turns noisy extracted text into the same markdown body
format the synthetic corpus uses, so chunking, embedding and indexing are unchanged.

Real PDFs have no front matter, so metadata comes from a `sources.json` file next to
them. Cleaning steps (all heuristic, all counted in `LoadStats`):
  1. extract text per page with pypdf
  2. drop page numbers and lines that repeat on many pages (running headers/footers)
  3. join hyphenated line breaks and reflow wrapped lines into paragraphs
  4. detect headings (numbered, ALL CAPS, short Title Case) and make them `## ` sections,
     labelled with the page they start on so citations can point at a page
  5. fall back to one section per page when a document yields almost no headings
"""

from __future__ import annotations

import hashlib
import json
import logging
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

from ..models import Document
from .base import BaseLoader, resolve_versions

SOURCES_FILE = "sources.json"
REQUIRED_FIELDS = ("file", "doc_id", "agency", "title", "year", "version", "topic")
REPEAT_FRACTION = 0.3        # a line on >= 30% of pages is a running header/footer
MIN_PAGES_FOR_REPEATS = 5
MIN_HEADINGS = 3             # fewer detected headings than this -> one section per page
MIN_SECTION_CHARS = 40

_PAGE_NUMBER = re.compile(r"^(page\s+)?\d{1,4}(\s*(of|/)\s*\d{1,4})?$", re.IGNORECASE)
_BULLET = re.compile(r"^\s*([•●▪◦·*\-–—])\s+")
_NUMBERED_HEADING = re.compile(r"^(\d+(\.\d+){0,3}\.?|[IVX]{1,5}\.|[A-Z]\.)\s+[A-Z][^.]*$")
_TERMINAL_PUNCT = (".", ",", ";", ":", "?", "!")
# A line ending in one of these is a wrapped sentence, not a heading.
_FUNCTION_WORDS = frozenset(
    "the of in and to for a an with by on or as at from is are that which than into".split())
_PAIRS = {"(": ")", "[": "]", "“": "”", '"': '"'}


@dataclass
class LoadStats:
    pages: int = 0
    characters: int = 0
    repeated_lines_removed: int = 0
    headings_detected: int = 0
    page_fallback: bool = False
    sections: int = 0


@dataclass
class PdfResult:
    body: str
    stats: LoadStats = field(default_factory=LoadStats)


def extract_pages(path: Path) -> list[str]:
    from pypdf import PdfReader

    logging.getLogger("pypdf").setLevel(logging.ERROR)   # silences benign "wrong pointing object" noise
    reader = PdfReader(str(path))
    return [(page.extract_text() or "") for page in reader.pages]


def _normalise_for_repeat(line: str) -> str:
    return re.sub(r"\d+", "#", " ".join(line.split())).lower()


def _edge_lines(lines: list[str]) -> list[str]:
    """First and last two lines of a page: where running headers and footers live.

    Only edge lines may be dropped as 'repeated', so body text that happens to differ
    from page to page only in its numbers is never deleted.
    """
    return lines[:2] + lines[-2:] if len(lines) > 4 else list(lines)


def clean_pages(pages: list[str]) -> tuple[list[list[str]], int]:
    """Split pages into lines; drop page numbers and repeated headers/footers."""
    split = [[" ".join(l.split()) for l in text.split("\n") if l.strip()] for text in pages]
    removed = 0
    repeated: set[str] = set()
    if len(split) >= MIN_PAGES_FOR_REPEATS:
        counts: Counter[str] = Counter()
        for lines in split:
            counts.update({_normalise_for_repeat(l) for l in _edge_lines(lines)})
        repeated = {k for k, c in counts.items() if c / len(split) >= REPEAT_FRACTION and len(k) < 120}
    cleaned = []
    for lines in split:
        edges = {id(l) for l in _edge_lines(lines)}
        kept = []
        for line in lines:
            if _PAGE_NUMBER.match(line) or (id(line) in edges and _normalise_for_repeat(line) in repeated):
                removed += 1
                continue
            kept.append(line)
        cleaned.append(kept)
    return cleaned, removed


def is_heading(line: str) -> bool:
    words = line.split()
    if not 1 <= len(words) <= 12 or not 3 <= len(line) <= 90 or line.endswith(_TERMINAL_PUNCT):
        return False
    letters = [c for c in line if c.isalpha()]
    if len(letters) < 3 or _BULLET.match(line):
        return False
    if words[-1].lower().strip("()[]") in _FUNCTION_WORDS or "," in line or "@" in line:
        return False
    if sum(c.isdigit() for c in line) > 3 or line.count("(") != line.count(")") or line.count("[") != line.count("]"):
        return False
    if line.count('"') % 2 or line.count("“") != line.count("”"):
        return False
    if _NUMBERED_HEADING.match(line):
        return True
    if len(letters) >= 4 and all(c.isupper() for c in letters):
        return True
    significant = [w for w in words if len(w) > 3 and w[0].isalpha()]
    return (2 <= len(words) <= 8 and len(significant) >= 2
            and all(w[0].isupper() for w in significant) and not line.islower())


def _reflow(lines: list[str]) -> str:
    """Join wrapped lines into paragraphs; keep bullets as separate '- ' lines."""
    out: list[str] = []
    for line in lines:
        bullet = _BULLET.match(line)
        if bullet:
            out.append("- " + line[bullet.end():].strip())
        elif not out:
            out.append(line)
        elif out[-1].endswith("-") and not out[-1].endswith(" -") and line[:1].islower():
            out[-1] = out[-1][:-1] + line                       # un-hyphenate: "infec-" + "tion"
        else:
            out[-1] += " " + line
    return "\n".join(out)


def pages_to_markdown(pages: list[str]) -> PdfResult:
    stats = LoadStats(pages=len(pages), characters=sum(len(p) for p in pages))
    cleaned, stats.repeated_lines_removed = clean_pages(pages)

    sections: list[tuple[str, list[str]]] = []
    seen: Counter[str] = Counter()

    def open_section(title: str, page_no: int) -> None:
        label = f"{title} (p. {page_no})"
        seen[label] += 1
        sections.append((label if seen[label] == 1 else f"{label} [{seen[label]}]", []))

    first_page_no = 1
    open_section("Front matter", first_page_no)
    headings = 0
    for page_no, lines in enumerate(cleaned, start=1):
        for line in lines:
            if is_heading(line):
                headings += 1
                open_section(line.rstrip(":"), page_no)
            else:
                sections[-1][1].append(line)
    stats.headings_detected = headings

    if headings < MIN_HEADINGS:
        stats.page_fallback = True
        sections = [(f"Page {n}", lines) for n, lines in enumerate(cleaned, start=1)]

    parts = []
    for title, lines in sections:
        text = _reflow(lines).strip()
        if len(text) >= MIN_SECTION_CHARS:
            parts.append(f"## {title}\n{text}")
    stats.sections = len(parts)
    return PdfResult(body="\n\n".join(parts), stats=stats)


class PdfLoader(BaseLoader):
    """Loads every non-excluded entry of `<directory>/sources.json`."""

    def __init__(self, directory: Path | str):
        self.directory = Path(directory)
        self.stats: dict[str, LoadStats] = {}
        self.excluded: list[dict] = []

    def load(self) -> list[Document]:
        sources_path = self.directory / SOURCES_FILE
        if not sources_path.is_file():
            raise FileNotFoundError(f"{sources_path} not found; describe each PDF there (see RUNBOOK)")
        sources = json.loads(sources_path.read_text(encoding="utf-8"))
        self.excluded = sources.get("excluded", [])
        docs = [self._load_one(entry) for entry in sources.get("documents", [])]
        if not docs:
            raise ValueError(f"{sources_path} lists no documents")
        return resolve_versions(docs)

    def _load_one(self, entry: dict) -> Document:
        missing = [f for f in REQUIRED_FIELDS if entry.get(f) in (None, "")]
        if missing:
            raise ValueError(f"{SOURCES_FILE}: entry {entry.get('file', '?')!r} missing {missing}")
        path = self.directory / entry["file"]
        if not path.is_file():
            raise FileNotFoundError(f"{path} listed in {SOURCES_FILE} but not found")
        raw = path.read_bytes()
        if not raw.startswith(b"%PDF-"):
            raise ValueError(f"{path.name} is not a PDF (a download may have saved an error page)")
        result = pages_to_markdown(extract_pages(path))
        if not result.body:
            raise ValueError(f"{path.name}: no extractable text (scanned PDF? OCR is not supported)")
        self.stats[entry["doc_id"]] = result.stats
        return Document(
            doc_id=entry["doc_id"], agency=entry["agency"], title=entry["title"],
            year=int(entry["year"]), version=int(entry["version"]), topic=entry["topic"],
            body=result.body, source_path=path.name, source_sha256=hashlib.sha256(raw).hexdigest(),
            supersedes=entry.get("supersedes") or None, synthetic=False,
        )
