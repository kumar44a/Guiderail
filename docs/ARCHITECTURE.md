# GuideRail: Architecture

Healthcare Guidelines RAG Assistant: rapid query and validation.
Status: **draft for owner review (Phase 0)**. Nothing below is implemented yet.

## 1. Goals and success criteria (from the Spinnaker brief)

| Criterion | Target | Measured by |
|---|---|---|
| Deterministic indexing, no API dependency | 100% reproducible | identical index hash across builds (`index/manifest.json`) |
| Retrieval quality | Precision@5 >= 0.65 | `evaluation/eval_retrieval.py` |
| Validation pass rate at threshold 0.6 | >= 80% (on in-corpus queries) | `evaluation/eval_validation.py` |
| API | stable REST, structured JSON | schema tests + OpenAPI |

## 2. System overview

```
OFFLINE: scripts/pipeline.py (deterministic)
 data/guidelines/*.md -> Loader -> Chunker -> Embedder (256-D) -> FAISS IndexFlatIP
   (+ front-matter:       BaseLoader  heading-     hashed n-grams,    + chunks.jsonl
    agency, year,         interface   aware,       md5-seeded,        + manifest.json
    version, supersedes)              deduped      L2-normalized      (counts, hashes)

ONLINE: FastAPI
 POST /qa {question, top_k}
   -> embed query -> FAISS top-k -> version filter -> Generator -> Validator -> response
                                    (latest wins,     extractive     independent    {answer, citations[],
                                     dupes collapsed) (or LLM, opt.) coverage +     confidence, status}
                                                                      retrieval score
EVALUATION: evaluation/
 labeled queries (in-corpus + out-of-corpus) -> P@1/5/10 -> threshold sweep -> validator stress test
   -> reports/*.json + summary.md + low_confidence.csv
```

## 3. Components

| Module | Responsibility |
|---|---|
| `loaders/` | `BaseLoader` interface; `MarkdownLoader` (corpus), `PdfLoader` (real documents). The corpus connector is the one swap point for a secure gateway. |
| `chunker.py` | Split by heading, then by sentence window; carry metadata (doc id, agency, year, version, section). Drop near-duplicate chunks. |
| `embeddings.py` | The only place text becomes vectors. Hashed unigram + bigram features into 256-D, md5-based signs and buckets, L2-normalized. |
| `index.py` | Build, save, load FAISS `IndexFlatIP`. Writes `manifest.json` (doc/chunk counts, SHA-256 of index and chunks). |
| `retriever.py` | Embed query, search, apply version policy (prefer latest non-superseded), return scored chunks. |
| `generator.py` | `ExtractiveGenerator` (default): pick best-matching sentences, cite each. `LlmGenerator` (optional): Claude answers from the evidence only. Both return answer plus the sentences they used. |
| `validator.py` | Scores support independently of the generator: stemmed, stopword-filtered token coverage of the answer against **all retrieved evidence**, combined with retrieval score. Maps to `validated` or `needs_review` at the threshold (default 0.6). |
| `api.py` | FastAPI app: `POST /qa`, `GET /health` (index hash, counts). Pydantic schemas. |
| `ui/app.py` | Streamlit client over `/qa`. No logic. |

## 4. API contract

```
POST /qa
  request : { "question": str, "top_k": int = 5 }     (top_k validated 1..20)
  response: { "answer": str,
              "citations": [ { "doc_id", "title", "agency", "year", "version", "section", "score" } ],
              "confidence": float,                     (0..1)
              "status": "validated" | "needs_review" }
GET /health -> { "status": "ok", "index_sha256": str, "documents": int, "chunks": int }
```
Abstention returns an empty or hedged answer with `needs_review`, never a guess.

## 5. Corpus (we write our own)

- Roughly 20 to 25 distinct synthetic documents across WHO, NIH, CDC style, with real-looking
  clinical specifics: hand hygiene, PPE, isolation and return-to-work, vaccination cold
  chain, environmental cleaning, respiratory etiquette, evidence grading, shared decision
  making.
- Front-matter on every file: `agency`, `year`, `version`, `supersedes`, `topic`.
- Deliberate hard cases: a superseded version with a changed recommendation (tests version
  policy), near-duplicate wording across agencies, and sections with very little text.
- A small real-document set (public WHO/CDC PDFs, supplied or downloaded by the owner)
  exercises the PDF loader on noisy text. These are listed in the RUNBOOK with source URLs.

## 6. Evaluation design

- **Retrieval:** labeled at document and section level (not topic family). P@1/5/10 reported.
- **Validation pass rate:** in-corpus queries only. Out-of-corpus queries are reported
  separately and are expected to abstain.
- **Validator stress test:** fabricated, paraphrased, partly supported and off-topic answers
  must score low. This is how a high pass rate is earned. Without it the metric is
  trivially near 1.0 for an extractive generator, and the report says so.
- **Threshold sweep:** 0.3 to 0.9. Shows validated vs abstained, and pass rate on correct vs
  out-of-corpus queries, to justify the chosen threshold.
- **Low-confidence list:** `needs_review` queries with reasons, for analyst review.
- **Live LLM run:** if the LLM generator ships, a logged real run is required (see section 8).

## 7. Traceability to the Equifile review

| Review point | Where addressed |
|---|---|
| Numbers must reconcile with artifacts | `check_docs_sync.py`, manifest, generated README stats |
| Only 3 synthetic docs, no real data | Own richer corpus plus real-document set |
| PDF loader only a future swap | `PdfLoader` exercised on real documents, outputs shown |
| Groundedness trivially 1.0 | Independent validator, stress test, honest note in report |
| Short sections gave thin results | Controlled neighbor-chunk fallback, deduped, cited |
| Live model path never run | `LlmGenerator` with logged live run (blocked on API key) |
| Separate AI-assisted from verified | `DEVELOPMENT_NOTES.md` |
| Modular, tested per stage, honest limitations | One module per stage, tests mirror modules, limitations section |

## 8. Open items and risks

- **API key:** the live LLM generator needs `ANTHROPIC_API_KEY`. Owner to provide before Phase 2,
  otherwise the live run is reported as not done.
- **Real documents:** owner to supply or approve a short list of public PDFs.
- **Spinnaker questions:** whether versioned and duplicate files are intentional in their kit,
  and how "latest" should be defined in their gateway.
- **Hash embeddings are lexical.** They match on shared words, not meaning, so paraphrased
  queries can miss. This is a documented limitation of the no-API requirement.
- **Docker:** needs a Dockerfile and compose. Not testable on this machine unless Docker is installed.

## 9. Phases

| Phase | Output | Exit check |
|---|---|---|
| 0 Foundations | structure, CLAUDE.md, pinned deps, this document | owner approves |
| 1 Corpus and index | corpus, loaders, chunker, embedder, FAISS, manifest | two builds give identical hashes |
| 2 RAG service | retriever, generators, validator, `/qa`, `/health` | schema and abstention tests pass |
| 3 Evaluation | labeled sets, P@K, sweep, stress test, reports | reports generated from runs |
| 4 Packaging | README (generated stats), RUNBOOK, Docker, Streamlit, DEVELOPMENT_NOTES | setup works from docs alone |
| 5 Submission | executed notebook or logs, metrics, technical summary, limitations | docs-sync and pytest green |
