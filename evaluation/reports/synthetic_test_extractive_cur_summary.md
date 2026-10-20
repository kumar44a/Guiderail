# Evaluation summary: synthetic corpus, test split

- Index: `45c3d9422161bc97…`  |  generator: `extractive`  |  threshold: 0.6
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
| Pass rate (validated / in-corpus) | 90.0% |
| Mean confidence (in-corpus) | 0.8248 |
| Answer correct (expected facts present) | 85.0% |
| **Validated precision** (correct among validated) | 88.9% |
| **Validated but wrong** | 11.1% |
| Correct but flagged for review | 5.9% |
| Out-of-corpus sent to review | 100.0% |
| Out-of-corpus falsely validated | 0.0% |
| Decision accuracy (all queries) | 88.0% |

A high pass rate alone is not evidence of quality: an extractive answer is copied from the evidence, so coverage is near-perfect by construction. Validated precision and the validated-but-wrong rate are the meaningful numbers.

## Threshold sweep

| Threshold | Pass rate | Validated precision | Validated but wrong | Correct but flagged | OOC false accept | Decision accuracy |
|---|---|---|---|---|---|---|
| 0.3 | 100.0% | 85.0% | 15.0% | 0.0% | 60.0% | 76.0% |
| 0.35 | 100.0% | 85.0% | 15.0% | 0.0% | 40.0% | 80.0% |
| 0.4 | 100.0% | 85.0% | 15.0% | 0.0% | 40.0% | 80.0% |
| 0.45 | 100.0% | 85.0% | 15.0% | 0.0% | 40.0% | 80.0% |
| 0.5 | 95.0% | 84.2% | 15.8% | 5.9% | 40.0% | 76.0% |
| 0.55 | 90.0% | 88.9% | 11.1% | 5.9% | 40.0% | 80.0% |
| 0.6 | 90.0% | 88.9% | 11.1% | 5.9% | 0.0% | 88.0% |
| 0.65 | 90.0% | 88.9% | 11.1% | 5.9% | 0.0% | 88.0% |
| 0.7 | 90.0% | 88.9% | 11.1% | 5.9% | 0.0% | 88.0% |
| 0.75 | 85.0% | 88.2% | 11.8% | 11.8% | 0.0% | 84.0% |
| 0.8 | 80.0% | 87.5% | 12.5% | 17.6% | 0.0% | 80.0% |
| 0.85 | 45.0% | 88.9% | 11.1% | 52.9% | 0.0% | 60.0% |
| 0.9 | 20.0% | 100.0% | 0.0% | 76.5% | 0.0% | 48.0% |

## Items for analyst review (4)

- **S02** (VALIDATED BUT WRONG, confidence 0.875): How long must hands be washed with soap and water when visibly dirty?
- **S12** (flagged: low confidence, confidence 0.516): In which direction should cleaning proceed through a room?
- **S24** (VALIDATED BUT WRONG, confidence 0.814): What should be recorded in the notes after a shared decision?
- **S32** (correct answer withheld, confidence 0.473): Should used needles be put back in their caps?
