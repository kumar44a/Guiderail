# Evaluation summary: synthetic corpus, dev split

- Index: `57b6796b8ead173d…`  |  generator: `extractive`  |  threshold: 0.6
- Queries: 20 in-corpus, 5 out-of-corpus

## Retrieval (in-corpus queries)

| Metric | Value |
|---|---|
| Precision@1 (document level) | 90.0% |
| Precision@5 (document level) | 64.0% |
| Precision@10 (document level) | 39.5% |
| Capped Precision@1 (vs. best attainable) | 90.0% |
| Capped Precision@5 (vs. best attainable) | 68.0% |
| Capped Precision@10 (vs. best attainable) | 72.4% |
| Hit@1 (a chunk containing the expected fact) | 75.0% |
| Hit@5 (a chunk containing the expected fact) | 100.0% |
| Hit@10 (a chunk containing the expected fact) | 100.0% |
| MRR (first fact-bearing chunk) | 0.8542 |

## Answers and validation

| Metric | Value |
|---|---|
| Pass rate (validated / in-corpus) | 95.0% |
| Mean confidence (in-corpus) | 0.7817 |
| Answer correct (expected facts present) | 95.0% |
| **Validated precision** (correct among validated) | 94.7% |
| **Validated but wrong** | 5.3% |
| Correct but flagged for review | 5.3% |
| Out-of-corpus sent to review | 60.0% |
| Out-of-corpus falsely validated | 40.0% |
| Decision accuracy (all queries) | 84.0% |

A high pass rate alone is not evidence of quality: an extractive answer is copied from the evidence, so coverage is near-perfect by construction. Validated precision and the validated-but-wrong rate are the meaningful numbers.

## Threshold sweep

| Threshold | Pass rate | Validated precision | Validated but wrong | Correct but flagged | OOC false accept | Decision accuracy |
|---|---|---|---|---|---|---|
| 0.3 | 100.0% | 95.0% | 5.0% | 0.0% | 80.0% | 80.0% |
| 0.35 | 100.0% | 95.0% | 5.0% | 0.0% | 60.0% | 84.0% |
| 0.4 | 100.0% | 95.0% | 5.0% | 0.0% | 60.0% | 84.0% |
| 0.45 | 100.0% | 95.0% | 5.0% | 0.0% | 60.0% | 84.0% |
| 0.5 | 100.0% | 95.0% | 5.0% | 0.0% | 60.0% | 84.0% |
| 0.55 | 100.0% | 95.0% | 5.0% | 0.0% | 40.0% | 88.0% |
| 0.6 | 95.0% | 94.7% | 5.3% | 5.3% | 40.0% | 84.0% |
| 0.65 | 90.0% | 94.4% | 5.6% | 10.5% | 40.0% | 80.0% |
| 0.7 | 85.0% | 94.1% | 5.9% | 15.8% | 40.0% | 76.0% |
| 0.75 | 60.0% | 91.7% | 8.3% | 42.1% | 40.0% | 56.0% |
| 0.8 | 40.0% | 87.5% | 12.5% | 63.2% | 0.0% | 48.0% |
| 0.85 | 30.0% | 83.3% | 16.7% | 73.7% | 0.0% | 40.0% |
| 0.9 | 10.0% | 100.0% | 0.0% | 89.5% | 0.0% | 32.0% |

## Items for analyst review (4)

- **S11** (correct answer withheld, confidence 0.564): What bleach strength is used for blood spills?
- **S23** (VALIDATED BUT WRONG, confidence 0.857): What are the steps of shared decision making?
- **S45** (VALIDATED BUT OUT OF CORPUS, confidence 0.796): How should radioactive waste be disposed of?
- **S47** (VALIDATED BUT OUT OF CORPUS, confidence 0.773): What is the incubation period of influenza?
