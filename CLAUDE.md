# CLAUDE.md: GuideRail conventions

Read this before making changes. `docs/ARCHITECTURE.md` is the source of truth for
design; if the two disagree, flag the conflict instead of guessing.

## Project

GuideRail is a citation-first RAG assistant over healthcare guideline documents
(WHO/NIH/CDC-style). It answers only from retrieved evidence, validates every answer
against that evidence, and abstains (`needs_review`) when support is weak.
Built for Spinnaker Analytics. The corpus is synthetic; the code is production-shaped.

## Non-negotiable rules

1. **No hand-typed numbers in docs.** Doc count, chunk count, test count, Precision@K,
   pass rate: all come from `index/manifest.json` and `evaluation/reports/*.json`,
   injected by `scripts/check_docs_sync.py --write`. Never type them into the README.
2. **Logic lives in `src/guiderail/` and `scripts/`, never in notebooks or the UI.**
   Notebooks and Streamlit only call the API or import the package and display results.
3. **Run `pytest` and `python scripts/check_docs_sync.py` before every commit.**
4. **Validator independence.** The validator must never be scored only on answers the
   generator produced from the same text. Keep the adversarial test set
   (`evaluation/validator_stress.jsonl`) green.
5. **Deterministic indexing.** No network, no unseeded randomness, no `hash()`. Two
   builds must produce identical index hashes (recorded in the manifest).
6. **Paths via `pathlib.Path`; all text I/O with `encoding="utf-8"`.**
7. **Surface blockers early.** If something needs the owner (API key, real documents,
   a decision), ask immediately. Do not route around it with a mock and defer it.
8. **Honest limitations.** Anything not run live or not verified is stated as such.

## AI-assisted vs verified

`docs/DEVELOPMENT_NOTES.md` records what Claude generated and what was independently
verified (tests run, metrics reproduced, design decisions). Keep it current.

## Environment

- Python 3.12, `.venv` in the project root, dependencies pinned in `requirements.txt`.
- `faiss-cpu` is a deliberate dependency (the brief requires FAISS). Wheels exist for
  macOS and Windows; document the install in the RUNBOOK.
- `.env` holds `ANTHROPIC_API_KEY` (optional live-LLM path only). Never commit it.
