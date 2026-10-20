# Evaluation summary: synthetic corpus, test split

- Index: `45c3d9422161bc97…`  |  generator: `llm`  |  threshold: 0.6
- Queries: 20 in-corpus, 5 out-of-corpus

## Retrieval (in-corpus queries)

| Metric | Value |
|---|---|
| Precision@1 (document level) | 95.0% |
| Precision@5 (document level) | 65.0% |
| Precision@10 (document level) | 36.0% |
| Capped Precision@1 (vs. best attainable) | 95.0% |
| Capped Precision@5 (vs. best attainable) | 83.5% |
| Capped Precision@10 (vs. best attainable) | 83.9% |
| Hit@1 (a chunk containing the expected fact) | 70.0% |
| Hit@5 (a chunk containing the expected fact) | 100.0% |
| Hit@10 (a chunk containing the expected fact) | 100.0% |
| MRR (first fact-bearing chunk) | 0.8417 |

## Answers and validation

| Metric | Value |
|---|---|
| Pass rate (validated / in-corpus) | 70.0% |
| Mean confidence (in-corpus) | 0.7353 |
| Answer correct (expected facts present) | 90.0% |
| **Validated precision** (correct among validated) | 100.0% |
| **Validated but wrong** | 0.0% |
| Correct but flagged for review | 22.2% |
| Out-of-corpus sent to review | 100.0% |
| Out-of-corpus falsely validated | 0.0% |
| Decision accuracy (all queries) | 84.0% |

A high pass rate alone is not evidence of quality: an extractive answer is copied from the evidence, so coverage is near-perfect by construction. Validated precision and the validated-but-wrong rate are the meaningful numbers.

## Threshold sweep

| Threshold | Pass rate | Validated precision | Validated but wrong | Correct but flagged | OOC false accept | Decision accuracy |
|---|---|---|---|---|---|---|
| 0.3 | 100.0% | 90.0% | 10.0% | 0.0% | 0.0% | 92.0% |
| 0.35 | 100.0% | 90.0% | 10.0% | 0.0% | 0.0% | 92.0% |
| 0.4 | 85.0% | 100.0% | 0.0% | 5.6% | 0.0% | 96.0% |
| 0.45 | 80.0% | 100.0% | 0.0% | 11.1% | 0.0% | 92.0% |
| 0.5 | 75.0% | 100.0% | 0.0% | 16.7% | 0.0% | 88.0% |
| 0.55 | 75.0% | 100.0% | 0.0% | 16.7% | 0.0% | 88.0% |
| 0.6 | 70.0% | 100.0% | 0.0% | 22.2% | 0.0% | 84.0% |
| 0.65 | 70.0% | 100.0% | 0.0% | 22.2% | 0.0% | 84.0% |
| 0.7 | 70.0% | 100.0% | 0.0% | 22.2% | 0.0% | 84.0% |
| 0.75 | 70.0% | 100.0% | 0.0% | 22.2% | 0.0% | 84.0% |
| 0.8 | 55.0% | 100.0% | 0.0% | 38.9% | 0.0% | 72.0% |
| 0.85 | 35.0% | 100.0% | 0.0% | 61.1% | 0.0% | 56.0% |
| 0.9 | 20.0% | 100.0% | 0.0% | 77.8% | 0.0% | 44.0% |

## Items for analyst review (6)

- **S02** (flagged: low confidence, confidence 0.397): How long must hands be washed with soap and water when visibly dirty?
- **S04** (flagged: low confidence, confidence 0.375): Are artificial fingernails allowed for clinical staff?
- **S12** (correct answer withheld, confidence 0.428): In which direction should cleaning proceed through a room?
- **S18** (correct answer withheld, confidence 0.377): Do staff returning after illness still have to wear a mask?
- **S28** (correct answer withheld, confidence 0.569): How long should patients be observed after getting a vaccine?
- **S32** (correct answer withheld, confidence 0.473): Should used needles be put back in their caps?
