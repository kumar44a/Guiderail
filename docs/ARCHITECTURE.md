# GuideRail: Architecture

Healthcare Guidelines RAG Assistant: rapid query and validation, built for Spinnaker Analytics.
Status: **all phases implemented, plus the retrieval and validator improvement rounds described in section 7**.
Measured results are not repeated here. They are generated into [EVALUATION_REPORT.md](EVALUATION_REPORT.md) and
[the README](../README.md), so this document cannot drift from the reports.

## 1. Goals and success criteria (from the Spinnaker brief)

| Criterion | Target | Measured by | Where to read the outcome |
|---|---|---|---|
| Deterministic indexing, no API dependency | 100% reproducible | identical hashes across builds and across processes (`index/manifest.json`, `tests/test_index.py`, `scripts/pipeline.py --check-determinism`) | evaluation report, section 2 |
| Retrieval quality | Precision@5 >= 0.65 | `evaluation/run_eval.py` (document-level, plus a capped variant and Hit@K, MRR) | evaluation report, sections 2 and 3 |
| Validation pass rate at threshold 0.6 | >= 80% on in-corpus queries | `evaluation/run_eval.py` | evaluation report, sections 2 and 4 |
| API | stable REST, structured JSON | `tests/test_api.py` | evaluation report, section 2 |

The report also gives *validated precision* (how many validated answers are correct) and out-of-scope false accepts, because a pass
rate alone is easy to inflate with an extractive generator.

## 2. System overview

```
OFFLINE  scripts/pipeline.py  (deterministic: no network, no randomness)
 data/guidelines/*.md  --MarkdownLoader--\
 data/real/*.pdf + sources.json --PdfLoader--> Documents (front matter / sources.json metadata, versions resolved)
   -> Chunker (heading-aware, <= 80 words, oversized units hard-split, dupes dropped within a document)
   -> Embedder (256-D hashed unigram+bigram, md5 buckets and signs, sublinear TF, L2-normalised)
   -> FAISS IndexFlatIP  +  chunks.jsonl  +  manifest.json (SHA-256 of corpus, chunks, vectors, index)

ONLINE   FastAPI  POST /qa {question, top_k}
 [Claude mode, optional] rewrite the question into search keywords
 embed query -> FAISS top 50  +  BM25 top 50 -> reciprocal rank fusion -> drop superseded versions
   -> lexical re-rank of the top 30, then a document-cohesion bonus (round 8) (cosine to the ORIGINAL question stays the reported score)
   -> neighbour fallback for sparse top chunks -> Generator (extractive | LLM) -> Validator -> {answer, citations, confidence, status}

EVALUATION  evaluation/  labeled queries (dev/test) -> retrieval metrics, answer correctness, threshold sweep,
 review list, validator stress test -> reports/*.json -> build_summary.py -> docs/EVALUATION_*.md
```

## 3. Components

| Module | Responsibility |
|---|---|
| `loaders/` | `BaseLoader` (one method, `load() -> list[Document]`) is the swap point for a real repository. `MarkdownLoader` reads the synthetic corpus. `PdfLoader` reads real PDFs described in `sources.json` (see the RUNBOOK for its cleaning steps and limits). `resolve_versions` turns `supersedes` into `superseded_by` and rejects bad pointers at load time. |
| `chunker.py` | Split by `##` heading, pack bullets and sentences to a word budget, hard-split oversized units, drop duplicates within a document only (near-duplicates *across* agencies are kept on purpose). |
| `text.py` | Tokeniser, light English stemmer and stopword list. Negations are kept because they change meaning. |
| `embeddings.py` | The only place text becomes vectors. Lexical by design: it matches shared words, not meaning. Method string `hash-ngram-md5-v1` is recorded in the manifest. |
| `index.py` | Build, save and load the FAISS `IndexFlatIP` over unit vectors (cosine), with the manifest. |
| `lexicon.py` | Corpus document-frequency and idf weights used by the re-ranker, the extractive generator and the validator. |
| `bm25.py` | BM25 keyword ranking over the whole vocabulary (textbook parameters) and reciprocal rank fusion. Built from the chunks at load time, so the index files and their hashes are unchanged. |
| `retriever.py` | Hybrid search (FAISS and BM25 each propose 50 candidates; fusion decides which 30 enter re-ranking), the version filter (superseded chunks excluded unless asked), the lexical re-ranker, and a controlled neighbour fallback: if one of the best few hits is very short, its neighbouring chunk is added once and marked `via="neighbor"`. |
| `rewrite.py` | Optional, Claude mode only, off by default. One small-model call turns the question into search keywords that are appended for searching. The generator and validator see the original question. Failures fall back silently. |
| `generators/extractive.py` | Default, no model. Scores single lines by idf-weighted question overlap plus credit for title and section context, keeps the top lines within a relative cutoff, and follows list lead-ins ("...:") and anaphoric continuations ("This..."). |
| `generators/llm.py` | Optional. Claude answers from the retrieved passages only, cites chunk ids, and replies `NOT_IN_EVIDENCE` when the answer is absent. The prompt is `prompts/answer_style.txt`. Request id, model and usage are recorded. The SDK import is lazy. Failures raise `GenerationError`, which the service turns into an abstention. |
| `validator.py` | **v2.** `confidence = coverage x relevance`, independent of the generator. *Coverage*: idf-weighted share of the answer's content words found in the evidence or its source metadata, halved when the answer contains a number-with-unit or a negation that the evidence does not. *Relevance*: half the rescaled top retrieval score plus half the share of question terms that the **answer** addresses. `validated` requires confidence at or above the threshold (default 0.6) **and** a citation. Three narrow rules came from the improvement rounds: a leading "Yes," or "No," is not scored as a content term or a negation claim; a number's unit is only checked when the next word is a real unit; a number fused with a footnote in the PDF text ("10.303") also supports its integer part; and question terms found in the cited passages' text count as addressed. |
| `service.py` | `QAService.ask()` wires retrieval, generation and validation; it is the only place that does. |
| `api.py` | FastAPI app. Index loaded in the lifespan handler; `.env` read at start-up. Pydantic validates input. |
| `evalkit.py` | Metrics (document-level and capped Precision@K, Hit@K, MRR), answer-correctness matching, threshold sweep, review list, Wilson intervals, label validation, validator stress harness. |
| `ui/app.py` | Streamlit client over `/qa` and `/health`. Display only. |

## 4. API contract

```
POST /qa[?debug=true]
  request : { "question": str (1..1000 chars), "top_k": int = 5 (1..20) }
  response: { "answer": str,
              "citations": [ { "chunk_id", "doc_id", "title", "agency", "year", "version", "section", "score" } ],
              "confidence": float (0..1),
              "status": "validated" | "needs_review",
              "debug": {...}  (only with ?debug=true) }
GET /health -> { "status": "ok", "version", "index_sha256", "documents", "chunks", "generator", "threshold" }
```

Invalid input is HTTP 422. Abstention is a normal 200 response with `needs_review` and no citations, never a guess. A generator
failure is also an abstention, so the endpoint does not return 5xx for a model outage.

## 5. Corpora

- **Synthetic** (`data/guidelines/`): written for this project in WHO, CDC and NIH style. Every file has front matter (`doc_id`, `agency`,
  `title`, `year`, `version`, `topic`, `supersedes`, `synthetic`). Hard cases are deliberate: superseded versions with a changed
  recommendation, WHO and CDC near-duplicates, different terminology for the same idea, and a document with a single short chunk.
  The text is invented and **not clinically reviewed**; it must never be used for care decisions.
- **Real** (`data/real/`): public WHO and CDC PDFs registered in `sources.json` (the PDFs are not committed). They exercise the PDF
  loader on genuinely noisy text and are where the system is weakest. One file was excluded because it was not English.

## 6. Evaluation design

- Labeled queries per corpus: in-corpus (with expected facts, optional forbidden values, relevant documents) and out-of-corpus
  (should abstain). Split into **dev** (used to choose changes) and **test** (held out, run after the configuration is frozen, every
  run logged). `evaluation/check_labels.py` verifies each expected fact exists in the relevant documents.
- **Retrieval:** document-level Precision@K as the brief defines it, a capped variant (divided by the best attainable score, since most
  synthetic documents have only a few chunks), Hit@K (does a chunk containing the fact appear) and MRR.
- **Answers:** correct = every expected fact present (stem-aware) and no forbidden value. *Validated precision* and out-of-scope false
  accepts are the meaningful validation metrics.
- **Validator stress test** (`evaluation/validator_stress.jsonl`): hand-written faithful and unfaithful answers, with the true evidence
  guaranteed present, so the validator is scored on answers its own generator did not produce.
- **Threshold sweep** and a **low-confidence review list** (CSV per run) for analysts.
- **Discipline:** accept/reject rules fixed before each run, tagged reports for every experiment, test-split runs logged.

## 7. Decisions and rejected experiments

Every change below was measured on dev material under accept/reject rules committed beforehand (`evaluation/reports/*_rules.txt`), and the
numbers are in [EVALUATION_REPORT.md](EVALUATION_REPORT.md) sections 10 to 12 and [EVALUATION_LOG.md](EVALUATION_LOG.md).

Accepted: context-aware sentence scoring, validator v2, list-continuation rules, lexical re-ranker (weights 0.5 and 1.0 performed alike, the smaller was
kept), a tightened LLM prompt, the yes/no response marker, hybrid BM25 + FAISS retrieval, and the three validator refinements above.

Tried and reverted: idf-weighted embeddings (two variants); scaling relevance by unknown question words; joining or doubling compound spellings
("hand rub"/"handrub"); a hand-written synonym table; three variants of reference-list removal; 50- and 35-word chunks.

Built and available but off by default: Claude question rewriting. It met its (higher) retrieval bar narrowly, was safe end to end, and showed no end-to-end
benefit, so it ships as an opt-in setting.

Decisions worth knowing:

- Embeddings are hashed n-grams because the brief requires deterministic, API-free indexing. Paraphrases and synonyms are the cost.
- The default threshold is the brief's 0.6 and was **not** moved on test-split evidence.
- The re-ranker changes order only; `Hit.score` stays the cosine so the validator's relevance input is unchanged.
- Superseded versions are excluded by default because answering from a withdrawn recommendation is the worse error.
- A relevance term in the validator is measured against the answer, not the evidence set, so an on-topic sentence does not validate an
  unrelated question.
- PDF-loader fixes (ligatures, glyph placeholders, wrapped lettered recommendations taken as headings) were made after the label check
  caught them, before any query was run on the five-document corpus; see the evaluation report, section 9.

## 8. Known limitations

- Lexical matching: paraphrases, synonyms and swapped plausible values can slip through the validator or be wrongly flagged.
- Near-domain out-of-scope questions can be answered with on-topic sentences by the extractive path and validated.
- Real PDFs: reference lists become noise chunks, figure text is jumbled, image-only pages give no text, no OCR.
- On an independent sealed question set (evaluation report, section 13) the system was far weaker than on its development questions; the development figures are optimistic.
- Natural questions worded differently from the document often miss the passage that answers them on real PDFs, because matching is lexical. Offline fixes were tried and mostly failed; closing the gap needs semantic matching, which conflicts with the deterministic, API-free design unless a local model is accepted.
- The LLM generator is nondeterministic and still withholds a share of correct answers on real documents at the default threshold.
- Document-level Precision@5 first missed 0.65; a larger corpus (v2) showed document size was not the cause, and a document-cohesion re-rank (round 8) then cleared the target on a fresh final set. That is a document-level metric; it does not fix passages missed because of wording differences on real PDFs.
- Samples are small and the dev/test discipline has limits (see the evaluation report's limitations section).
- Docker files and the Windows setup instructions were written but not run on a machine of that kind.

## 9. Phases

| Phase | Output | Status |
|---|---|---|
| 0 Foundations | structure, CLAUDE.md, pinned dependencies, this document | done |
| 1 Corpus and index | corpus, loaders, chunker, embedder, FAISS, manifest | done |
| 2 RAG service | retriever, generators, validator, `/qa`, `/health` | done |
| 3 Evaluation | labeled sets, metrics, sweep, stress test, reports (re-run on the five-document real corpus) | done |
| 4 Packaging | README with generated stats, RUNBOOK, Docker, Streamlit, DEVELOPMENT_NOTES, docs-sync check | done (Docker unrun) |
| 5 Submission | executed notebook, technical summary, metrics, limitations | done (Docker unrun) |
