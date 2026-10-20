# GuideRail: Technical summary

A research prototype for Spinnaker Analytics: a citation-first question-answering service over healthcare guideline documents.
It is **not** a clinical tool. This summary contains no measured figures on purpose; every number lives in the generated
[evaluation report](EVALUATION_REPORT.md) and in the [README](../README.md) results block, so nothing here can drift from the runs.

## What it does

`POST /qa` takes a question and returns an answer, its citations, a confidence between 0 and 1, and a status of `validated` or
`needs_review` (threshold 0.6). The answer is built only from retrieved guideline passages. A separate validator checks the answer against
that evidence, and anything weakly supported is sent to review instead of being asserted.

## How it works

1. **Deterministic index (offline).** Guideline text is chunked by heading, embedded as 256-dimensional hashed unigram and bigram vectors (MD5 buckets, no model, no network) and stored in a FAISS inner-product index with a manifest of SHA-256 hashes. Two builds, in one process or two, produce identical hashes; the Docker build repeats the check.
2. **Retrieval (online).** FAISS and a BM25 keyword ranking each propose candidates; reciprocal rank fusion merges them; superseded guideline versions are dropped; a lexical re-ranker orders the best of them. An optional Claude step can rewrite the question into search keywords (off by default).
3. **Generation.** Either an extractive generator (picks supporting sentences, no model, default) or a Claude generator that is instructed to use the passages only and to say when the answer is not there.
4. **Validation.** Confidence is evidence coverage (how much of the answer's content is found in the evidence, with penalties for unsupported numbers and negations) times relevance (how well the answer addresses the question). The validator does not depend on the generator, and it is tested on hand-written good and bad answers it did not produce.
5. **Packaging.** FastAPI service, Streamlit client, Dockerfile and compose file, a RUNBOOK (including how to swap in a secure guideline repository through the loader interface) and an executed [walkthrough notebook](../notebooks/guiderail_walkthrough.ipynb).

## How it was evaluated

- A synthetic corpus of invented guidelines (with deliberate hard cases such as superseded versions and near-duplicate agencies) and a corpus of five real WHO and CDC PDFs.
- Labelled question sets split into development, held-out test, and several **sealed** sets written by the project owner that the system was never tuned on. Rules for each change were committed before the change was measured; most retrieval ideas failed their own rules and were reverted.
- Reports cover retrieval Precision@K, Hit@K and MRR, mean confidence, pass rate and validated precision at the threshold, a threshold sweep, and a review list of low-confidence and validated-but-wrong queries.
- Documents are generated from the saved reports, and a script fails the build if they differ.

## Result against the brief

| Criterion | Outcome |
|---|---|
| Deterministic indexing, no external API | Met |
| Stable REST endpoint | Met |
| Precision@5 of at least 0.65 | **Met after a retrieval change**, with caveats. It first missed on the synthetic corpus; a larger corpus (v2) showed the cause was not document size; a document-cohesion re-rank (round 8, rules written first, judged on dev) then cleared 0.65 on a fresh final question set and on the brief's held-out split (where it sits on the threshold). It is a document-level metric and the gain does not carry to the real-PDF weakness (report sections 17 and 18) |
| Validation pass rate of at least 80% at 0.6 | Met by the extractive generator on the synthetic held-out split; not met by the Claude generator on the real-PDF held-out split, and a further experiment (round 9: more passages for Claude, then question rewriting) did not move it beyond run-to-run noise (report section 19) |

The current figures are in the README block and report sections 2 to 4. Read the sealed-set sections (13 to 16; section 17 covers the v2 corpus) before the development tables.

## Limitations (all of them matter)

- **Lexical retrieval.** Matching is by shared words, so a question worded differently from the document often misses the passage that answers it. This is the main weakness on real PDFs. A semantic embedding model would address it and was ruled out for this project.
- **The extractive generator is unsafe on real PDFs.** It can validate figure captions or reference entries as answers, including for questions the documents do not cover. Use the Claude generator for real documents.
- **The Claude generator withholds many correct answers** on real documents, and is nondeterministic.
- **Independent evidence is thin and author-biased.** The synthetic corpus, queries, labels and stress cases were written by the same AI that wrote the system; no clinician has reviewed any guideline text, query, label or answer. The owner's question sets came without expected answers, so the labels are the assistant's reading of the PDFs (one was wrong and was corrected, and many are loosely worded). Only a few sealed questions are out of scope, so false-accept behaviour is barely measured.
- **Answer-correct is a fact-string proxy**, which misses some correct paraphrases and over-credits loose labels.
- **Real-PDF extraction** is lossy (reference lists become noise, figure text is jumbled, image-only pages give no text, no OCR). The French WHO file was excluded.
- **Not run:** Docker and the Windows setup were written but never executed; the Streamlit UI was tested headlessly, not in a browser.

## Reproducing it

See the RUNBOOK, or `pip install -r requirements.txt`, `pytest`, `python scripts/pipeline.py --check-determinism`, `python scripts/check_docs_sync.py`.
The notebook is rebuilt and executed with `pip install -r requirements-notebook.txt` and `python scripts/build_notebook.py`.
What was AI-generated and what was independently checked is in [DEVELOPMENT_NOTES.md](DEVELOPMENT_NOTES.md).
