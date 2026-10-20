# GuideRail: Development notes

This file separates **what an AI generated** from **what was independently checked**, so a reviewer knows how much weight each claim
can bear. It deliberately contains no measured results; those are generated into the [evaluation report](EVALUATION_REPORT.md).

## 1. Who did what

**Claude (Claude Code) wrote** all code, tests, the synthetic corpus text, the labeled queries and expected facts, the validator stress
cases, the evaluation scripts, and every document in this repository, in sessions directed by the project owner.

**The project owner decided or supplied:**

- the build approach (from scratch, using the Spinnaker kit only as a reference; its corpus was not used) and the name GuideRail
- writing our own synthetic corpus, and using real documents as well
- the extras to build: live LLM generator, Streamlit UI, Docker with compose
- the Anthropic API key (kept in a git-ignored `.env`) and permission to spend it on evaluation runs
- the real PDFs, downloaded by hand because the public sites block scripted downloads
- moving the project out of a cloud-synced folder, and the hand hygiene documents
- the review stop after every phase, and the requirement to honour the lessons from an earlier project review

No clinician or domain expert has reviewed the synthetic guideline text, the queries, the expected facts or any answer.

## 2. What was independently checked, and how

"Independently" means checked by a mechanism other than the code that produced the claim. It does **not** mean checked by a human,
except where stated.

| Claim | Check | Reproduce |
|---|---|---|
| Indexing is deterministic | tests compare two builds in one process and a rebuild in a separate process byte for byte; the Docker build repeats it | `pytest tests/test_index.py`; `python scripts/pipeline.py --check-determinism` |
| Components behave as specified | unit tests per module, API contract tests, headless UI tests | `pytest` |
| Every expected fact in the labeled queries exists in the relevant documents | label checker; it caught two label problems that were really loader defects | `python evaluation/check_labels.py` |
| Reported metrics match the runs | docs are generated from `evaluation/reports/*.json`; a check script fails if any doc differs from its generator | `python scripts/check_docs_sync.py` |
| The validator is not trivially permissive | a stress set of hand-written faithful and unfaithful answers, with the true evidence guaranteed present | `python evaluation/eval_validator_stress.py` |
| A retrieval change helped | rules, thresholds and parameters committed first; every change judged against the previous kept state on dev material by `judge_round3.py`; most changes failed and were reverted | `python evaluation/judge_round3.py --step TAG --against TAG` |
| A validator change did what it claims | rules committed before the change; `revalidate.py` first proved it reproduces stored confidences exactly; `judge_round2.py` applies the rules mechanically to dev material | `python evaluation/judge_round2.py` |
| Test-split results were not tuned on | rules committed before runs; every test-split run logged with timestamp and index hash | `evaluation/reports/test_split_runs.log`, `evaluation/reports/rerun_5doc_rules.txt`, `git log` |
| The LLM path really works | a logged live run with model, request ids and token usage; later live runs inside the evaluation reports | `evaluation/logs/live_llm_run.json`, `evaluation/reports/*_llm_*.json` |
| The notebook runs end to end | built and executed by `scripts/build_notebook.py` (no logic in it; it calls the package and shows saved reports); a test checks the saved file has outputs and no error cells | `pytest tests/test_notebook.py` |
| Real PDFs load | the PDF loader was run on actual WHO and CDC documents and chunk output inspected | `python scripts/pipeline.py --real` |

Limits of these checks:

- The **stress set, the queries and the labels were written by the same AI that wrote the system.** Dev/test separation and the label
  checker reduce the risk of fitting, but they cannot remove author bias. The stress set uses the facts (not the wording) of a few
  test-split topics to place the evidence, which the report discloses.
- The single logged live check predates the final LLM prompt. The evaluation's LLM rows were produced with the final prompt.
- Correctness scoring is a fact-string match, a proxy for a clinician's judgement.
- Real-PDF extraction quality was judged by inspecting samples, not by comparing against a ground-truth transcription.

## 3. Not verified

- **Docker.** The Dockerfile and compose file were written without Docker being installed, so they have never been built or run.
- **Windows.** The Windows setup commands were not run on Windows.
- **The Streamlit UI in a real browser.** It is tested headlessly with Streamlit's `AppTest` against the real API app, not by eye.
- **Clinical correctness.** Nothing here has been checked against medical judgement.
- **LLM stability.** Live runs vary slightly; no repeated-run statistics were collected.
- **Any threshold other than 0.6 as a deployment choice.** The sweep is reported but was not validated on fresh queries.

## 4. Mistakes caught during development (kept so the pattern is visible)

- Generated documents once contained hand-typed numbers and narrative claims the data did not support. The fix was structural: the
  documents are now generated from the reports and a script fails when they differ. During Phase 4 a failed edit briefly left a
  stale generated report in the working tree; the sync check is what makes that kind of slip visible.
- Answer matching was exact-substring and under-credited correct paraphrases. It was made stem-aware and one expected-fact alternative
  was added after seeing an LLM answer; both edits are disclosed in the evaluation log.
- Two experiments (idf-weighted embeddings, scaling relevance by unknown words) were tried, failed their pre-set rules and were reverted.
- A test asserted that an oversized unit stays whole; real data proved that wrong, so the chunker changed and the test was replaced.
- The PDF loader's repeated-line removal deleted body text that differed only in digits; it was restricted to edge lines.
- Adding two documents revealed three more loader defects (ligatures, glyph placeholders, wrapped recommendations read as headings).
  They were fixed before any query was run on the larger corpus, and the first written rule claiming the older PDFs were unaffected
  turned out to be wrong; the report keeps both statements.
- `.env` was read only when the LLM client looked up its key, so a generator or threshold set in `.env` would have been ignored by the
  API. Found while writing the RUNBOOK; fixed and tested.
- Validator round 2: a candidate fix for ratio numbers was dropped because only one instance existed, so it could only have been fitted to that case. One expected-fact list (R36) omitted a passive phrasing and counts two substantively right answers as wrong; it was left unedited and disclosed. A shell edit (`sed -i` on macOS) failed and silently skipped the regeneration of the documents; the output showed old numbers and it was redone.
- Retrieval rounds 3 to 6: most ideas failed their own rules and were reverted (see the evaluation report, section 11). A first version of the reference-list rule was written without looking at the data and could not fire on the real reference lists; it was found by reading the documents and replaced before any retrieval measurement, with the replacement registered first.
- The sealed run, on questions the owner wrote and the assistant labelled from the PDFs, was much weaker than every development number. A follow-up hypothesis (reference lists are the cause) was tested on fresh questions written without system output in front of the author and was not supported, so it was reverted rather than shipped. The development numbers should be read as optimistic; the sealed numbers as the better guide.
- The owner's ten sealed questions came without expected answers, so their labels are the assistant's judgement from the PDF text; the owner was asked to check them. One question (U10) was left unscored because the documents answer it only indirectly.
- The owner's second batch (50 questions, V01 to V50) was labelled by the assistant from the PDF text before the run. After the run, one label (V42) turned out to be wrong: the documents do answer it, and the assistant's keyword search had missed the wording. It was corrected and disclosed (rules file, report section 14); the saved reports keep the original label. The rules file also named the wrong ids for the out-of-scope questions; that is corrected there too. The questions are long and compound and about a third have loose expected facts, so answer-correct figures over-credit.
- The owner's CDC isolation (47 scored) and vaccine storage (47 scored) question sets were labelled from the PDF text before any run, all as answerable. Six questions the assistant could not classify were left unscored instead of being called out of scope; run afterwards, three of them proved answerable. Because no scored question is out of scope in either set, they say nothing about false accepts. About half carry loose expected facts, so answer-correct over-credits; the fact-string matcher also marks some paraphrased correct answers wrong.
- Precision@5 on the synthetic corpus missed 0.65 and I first blamed the corpus (documents of 3 or 4 chunks cap the score). I tested that with a v2 corpus (same text plus new sections, 7 to 9 chunks each, fresh test questions, rules committed first). The target was still missed on the held-out split (the dev split on v2 would have met it), so the explanation was withdrawn rather than defended. v2 was built after seeing the miss and by the same author, so it is not independent evidence either way. I then looked at which documents filled the lower ranks for the v2 test questions, which exposed those questions; a document-cohesion re-rank was designed from that (round 8), judged only on dev material under rules written first, and its claim checked on a fresh final set written beforehand. It cleared 0.65 there. The sealed sets were not re-run on it, and a Claude re-run was lost to an empty API credit balance and discarded.
- Round 9 tried to lift the Claude pass rate on real PDFs: rules and a judge script were committed first; two candidates (more passages, then more passages plus question rewriting) were run on dev against two baseline runs and neither cleared the rule, so both stay off and the target is reported as not met. The two baseline runs differed by one question, which shows how little a one- or two-question gain means for a nondeterministic generator.
- A label for a fresh question (M15) was wrong because the PDF loader joins hyphenated line breaks ("well-ventilated" became "wellventilated"); the label check caught it before any run and the label now accepts both spellings.
- The Claude question-rewrite call passed an argument (`temperature`) that the installed SDK rejects. The fake-client tests could not see it; the first live run did (all rewrites failed safely and no request was sent). A test now checks the request arguments against the real SDK signature.
- One full test run stalled for several minutes under heavy machine load and did not reproduce; the cause was not established.
- The project lived in a cloud-synced folder whose eviction made imports hang and files unreadable. It was moved out, and the RUNBOOK
  warns about it.

## 5. Reproducing everything

```bash
pip install -r requirements.txt
pytest
python scripts/pipeline.py --check-determinism
python evaluation/check_labels.py
python evaluation/run_eval.py --corpus synthetic --split dev          # real corpus needs the PDFs listed in data/real/sources.json
python scripts/check_docs_sync.py
```

The real PDFs are not in the repository. `data/real/sources.json` lists each file, its source and why any file was excluded.
