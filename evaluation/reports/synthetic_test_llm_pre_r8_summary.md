# Evaluation summary: synthetic corpus, test split

- Index: `45c3d9422161bc97…`  |  generator: `llm`  |  threshold: 0.6
- Queries: 20 in-corpus, 5 out-of-corpus

## Retrieval (in-corpus queries)

| Metric | Value |
|---|---|
| Precision@1 (document level) | 95.0% |
| Precision@5 (document level) | 55.0% |
| Precision@10 (document level) | 32.0% |
| Capped Precision@1 (vs. best attainable) | 95.0% |
| Capped Precision@5 (vs. best attainable) | 71.6% |
| Capped Precision@10 (vs. best attainable) | 76.1% |
| Hit@1 (a chunk containing the expected fact) | 70.0% |
| Hit@5 (a chunk containing the expected fact) | 100.0% |
| Hit@10 (a chunk containing the expected fact) | 100.0% |
| MRR (first fact-bearing chunk) | 0.8417 |

## Answers and validation

| Metric | Value |
|---|---|
| Pass rate (validated / in-corpus) | 80.0% |
| Mean confidence (in-corpus) | 0.76 |
| Answer correct (expected facts present) | 95.0% |
| **Validated precision** (correct among validated) | 93.8% |
| **Validated but wrong** | 6.2% |
| Correct but flagged for review | 21.1% |
| Out-of-corpus sent to review | 100.0% |
| Out-of-corpus falsely validated | 0.0% |
| Decision accuracy (all queries) | 80.0% |

A high pass rate alone is not evidence of quality: an extractive answer is copied from the evidence, so coverage is near-perfect by construction. Validated precision and the validated-but-wrong rate are the meaningful numbers.

## Threshold sweep

| Threshold | Pass rate | Validated precision | Validated but wrong | Correct but flagged | OOC false accept | Decision accuracy |
|---|---|---|---|---|---|---|
| 0.3 | 100.0% | 95.0% | 5.0% | 0.0% | 0.0% | 96.0% |
| 0.35 | 100.0% | 95.0% | 5.0% | 0.0% | 0.0% | 96.0% |
| 0.4 | 100.0% | 95.0% | 5.0% | 0.0% | 0.0% | 96.0% |
| 0.45 | 95.0% | 94.7% | 5.3% | 5.3% | 0.0% | 92.0% |
| 0.5 | 85.0% | 94.1% | 5.9% | 15.8% | 0.0% | 84.0% |
| 0.55 | 85.0% | 94.1% | 5.9% | 15.8% | 0.0% | 84.0% |
| 0.6 | 80.0% | 93.8% | 6.2% | 21.1% | 0.0% | 80.0% |
| 0.65 | 80.0% | 93.8% | 6.2% | 21.1% | 0.0% | 80.0% |
| 0.7 | 75.0% | 93.3% | 6.7% | 26.3% | 0.0% | 76.0% |
| 0.75 | 70.0% | 92.9% | 7.1% | 31.6% | 0.0% | 72.0% |
| 0.8 | 55.0% | 100.0% | 0.0% | 42.1% | 0.0% | 68.0% |
| 0.85 | 30.0% | 100.0% | 0.0% | 68.4% | 0.0% | 48.0% |
| 0.9 | 10.0% | 100.0% | 0.0% | 89.5% | 0.0% | 32.0% |

## Items for analyst review (5)

- **S02** (VALIDATED BUT WRONG, confidence 0.793): How long must hands be washed with soap and water when visibly dirty?
- **S12** (correct answer withheld, confidence 0.463): In which direction should cleaning proceed through a room?
- **S18** (correct answer withheld, confidence 0.433): Do staff returning after illness still have to wear a mask?
- **S28** (correct answer withheld, confidence 0.569): How long should patients be observed after getting a vaccine?
- **S32** (correct answer withheld, confidence 0.473): Should used needles be put back in their caps?
