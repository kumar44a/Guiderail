# GuideRail: Runbook

How to set up, run, evaluate and extend GuideRail, including how to point it at a real guideline repository.
This file contains no measured numbers; those live in the generated [evaluation report](EVALUATION_REPORT.md).

## 1. Setup

Requirements: Python 3.12 and about a gigabyte of free disk for the virtual environment.

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Windows (PowerShell)**

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

`faiss-cpu` ships wheels for macOS, Windows and Linux. If `pip` cannot find one for your platform or Python version, use Python 3.12.

> **Do not keep the project or its `.venv` in a cloud-synced folder** (iCloud Drive "Documents", OneDrive, Dropbox).
> During development the sync client evicted files to free disk space, which made `import numpy` hang for minutes and made
> source files unreadable ("Operation timed out"). Symptoms: Python starts but imports never finish, or a file shows as
> a cloud placeholder. Keep the project in a plain local folder such as `~/Developer/guiderail`. If a file is stuck, reading it
> once (`cat file > /dev/null`) forces a download.

## 2. Build the index

```bash
python scripts/pipeline.py                      # synthetic corpus -> ./index
python scripts/pipeline.py --check-determinism  # also builds a second copy and compares hashes
```

`index/` contains `guiderail.faiss`, `chunks.jsonl` and `manifest.json`. The manifest records document and chunk counts and the
SHA-256 of the corpus, chunks, vectors and index. It has no timestamps, so identical input gives an identical manifest.
The index is rebuilt, never edited, whenever the corpus or the chunker changes. `index/` and `index_real/` are not committed.

## 3. Run the service

```bash
uvicorn guiderail.api:app --app-dir src --port 9070
```

| Setting | Default | Meaning |
|---|---|---|
| `GUIDERAIL_INDEX_DIR` | `./index` | which index to serve (use `./index_real` for the real PDFs) |
| `GUIDERAIL_THRESHOLD` | `0.6` | confidence at or above which an answer is `validated` (0 to 1) |
| `GUIDERAIL_RERANK_WEIGHT` | `0.5` | lexical re-ranker weight; `0` turns the re-ranker off |
| `GUIDERAIL_GENERATOR` | `extractive` | `extractive` (offline) or `llm` (Claude) |
| `GUIDERAIL_LLM_MODEL` | see `config.py` | model used by the LLM generator |
| `ANTHROPIC_API_KEY` | none | only for `GUIDERAIL_GENERATOR=llm` |

Settings can also be put in a `.env` file in the project root (never committed); the API reads it at start-up. Real environment variables win over `.env`.

Endpoints: `POST /qa`, `GET /health`, and interactive docs at `/docs`. Invalid input returns HTTP 422. If the generator fails (for
example an API error), the request still returns `needs_review` with an abstaining answer, not a server error.

The UI is a thin client: `streamlit run ui/app.py` (set `GUIDERAIL_API_URL` if the API is not on `localhost:9070`).

## 4. The LLM generator (optional)

1. Put `ANTHROPIC_API_KEY=...` and `GUIDERAIL_GENERATOR=llm` in `.env`.
2. `python scripts/live_llm_check.py` makes a handful of **paid** API calls and writes `evaluation/logs/live_llm_run.json` (model,
   request ids, token usage, answers and validator decisions; never the key).
3. The prompt is `prompts/answer_style.txt`. Claude is told to use only the supplied passages, cite chunk ids, and reply
   `NOT_IN_EVIDENCE` when the answer is absent. Its output goes through the same validator as the extractive generator.

`pytest` never calls the API unless you also set `GUIDERAIL_RUN_LIVE=1` (then the `live_llm` test makes one paid call).

LLM runs are not deterministic: two identical runs can differ by a query or two.

## 5. Using real guideline documents

### 5.1 PDFs on disk

1. Put the PDFs in `data/real/`. The PDFs are git-ignored; keep the licence and source of each.
2. Describe each file in `data/real/sources.json`:

   ```json
   { "documents": [ {
       "file": "my-guideline.pdf", "doc_id": "who-example-2024", "agency": "WHO",
       "title": "Full official title", "year": 2024, "version": 1, "topic": "hand_hygiene",
       "supersedes": null, "source_url": "https://...", "note": "anything a reviewer should know" } ],
     "excluded": [ { "file": "other.pdf", "reason": "why it is not used" } ] }
   ```

   Required: `file, doc_id, agency, title, year, version, topic`. If one guideline replaces another, set `supersedes` to the older
   `doc_id`; the retriever then excludes the older version by default. A bad pointer fails at load time.
3. Build and serve:

   ```bash
   python scripts/pipeline.py --real --check-determinism     # data/real -> ./index_real
   GUIDERAIL_INDEX_DIR=index_real uvicorn guiderail.api:app --app-dir src --port 9070
   ```

### 5.2 What the PDF loader does and does not do

It extracts text with `pypdf`; removes page numbers and repeated headers and footers; rejoins hyphenated line breaks; expands
ligature characters and drops unmapped-glyph codes; detects headings (a line followed by a lowercase line is a wrapped sentence, not
a heading); and labels sections with their starting page, so citations read like "Section (p. 41)". If a PDF has almost no
detectable headings it falls back to one section per page.

Known limits, all visible in the evaluation report:

- **English only.** The stemmer and stopword list are English. A non-English PDF will index but retrieve poorly.
- **No OCR.** A scanned PDF with no text layer is rejected with a clear error. Pages that are images inside a text PDF simply yield no text.
- **Reference lists** become noise chunks and can attract retrieval.
- **Figures and tables** extract as jumbled fragments, so facts that only appear in a figure are hard to retrieve.
- A file that is really an HTML error page (a blocked download saved as `.pdf`) is rejected.

Public WHO and CDC sites often block scripted downloads, so save PDFs by hand from a browser and record the URL in `sources.json`.

### 5.3 Swapping in a secure repository

The pipeline only needs a list of `Document` objects. To read from an internal document store, a SharePoint library or a gateway,
write a loader and use it in place of `MarkdownLoader` or `PdfLoader` in `scripts/pipeline.py`:

```python
from guiderail.loaders import BaseLoader, resolve_versions
from guiderail.models import Document

class GatewayLoader(BaseLoader):
    def __init__(self, client):            # your authenticated client; credentials come from the environment, never the code
        self.client = client

    def load(self) -> list[Document]:
        docs = [Document(doc_id=r.id, agency=r.agency, title=r.title, year=r.year, version=r.version, topic=r.topic,
                         body=to_markdown(r), source_path=r.uri, source_sha256=sha256_of(r.bytes),
                         supersedes=r.supersedes, synthetic=False)
                for r in self.client.list_guidelines()]
        return resolve_versions(docs)      # fills superseded_by, rejects duplicate ids and dangling pointers
```

Rules that keep the pipeline correct:

- **Body format:** Markdown, with `## Heading` lines starting each section. Everything downstream (chunking, citations) relies on it.
- **Determinism:** `resolve_versions` sorts by `doc_id`. Do not add timestamps, random ids or network-dependent text to the body, and
  fetch content at index-build time only. Run `--check-determinism` after every change.
- **Security:** keep credentials in the environment or a secret manager. Log document ids, not document contents. The index files
  contain the full guideline text, so store `index/` with the same access control as the source. The LLM generator sends retrieved
  passages and the question to the Anthropic API; do not enable it for documents that must not leave your network without approval.
- **Versions:** decide how "latest" is defined in your repository and encode it as `supersedes`. The retriever trusts that field.
- Add a test with a few fixture documents next to `tests/test_loader.py`.

## 6. Evaluation

```bash
python evaluation/check_labels.py                                  # every expected fact must exist in the relevant documents
python evaluation/run_eval.py --corpus synthetic --split dev       # --corpus real, --generator llm, --tag NAME, --threshold X
python evaluation/eval_validator_stress.py                         # answers the generator did not produce
python evaluation/revalidate.py --verify real_dev_llm_final        # re-run the validator on saved answers (no API calls); --compare, --write TAG
python evaluation/build_summary.py                                 # regenerate docs/EVALUATION_*.md
python scripts/check_docs_sync.py                                  # fail if README or reports are stale
```

Discipline that the results depend on:

- Queries are split into **dev** (used to choose changes) and **test** (held out). Change code from dev results only.
- Run the **test** split only after the configuration is frozen. Every test-split run is logged to
  `evaluation/reports/test_split_runs.log`; do not tune on a test split that has already been looked at. Write new queries instead.
- State the accept/reject rule for a change before looking at its result, and commit the rule first.
- Use `--tag` to keep each run's report; the log is built from tagged dev reports.
- A validator change can be judged on saved answers with `revalidate.py` (no API calls). Prove the tool first: `--verify` must reproduce the stored confidences before the change. Commit the accept/reject rules before writing the change (see `evaluation/reports/validator_round2_rules.txt` for an example).
- Adding a document to a corpus changes every number for that corpus. Re-run and keep the old reports under a tag (as `final_3doc`).

## 7. Docker

```bash
docker compose up --build        # API :9070, UI :8501
```

The image builds the synthetic index at build time and fails the build if two builds differ. By default it serves the extractive
generator with no network access. **These files were written but never run**: Docker was not installed on the development machine.
Expect to debug the first build. For the real PDFs, build `index_real` on the host and mount it:
`volumes: ["./index_real:/app/index_real:ro"]` with `GUIDERAIL_INDEX_DIR=/app/index_real`.

## 8. Troubleshooting

| Symptom | Likely cause and fix |
|---|---|
| Python hangs at `import numpy`, files "time out" | project or `.venv` in a cloud-synced folder; move it (section 1) |
| `FileNotFoundError ... sources.json` | describe each PDF in `data/real/sources.json` (section 5.1) |
| `... is not a PDF` | a blocked download saved an error page; re-download in a browser |
| `no extractable text (scanned PDF?)` | needs OCR, which is not supported |
| `uvicorn` fails at start with `... not found; run scripts/pipeline.py first` | build the index first, or point `GUIDERAIL_INDEX_DIR` at one |
| Everything is `needs_review` with the LLM generator | check `ANTHROPIC_API_KEY`; generation errors become abstentions (see the API log) |
| `LABEL PROBLEMS` from `run_eval.py` | an expected fact is not in any chunk of the relevant document; see whether the loader dropped it |
| `pypdf` prints "wrong pointing object" or fontTools notices | harmless extraction warnings |
| Disk full during `pip install` or index build | free space; the venv is the largest item |
