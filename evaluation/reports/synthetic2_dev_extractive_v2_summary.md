# Evaluation summary: synthetic2 corpus, dev split

- Index: `ffe20683ee85c731…`  |  generator: `extractive`  |  threshold: 0.6
- Queries: 20 in-corpus, 5 out-of-corpus

## Retrieval (in-corpus queries)

| Metric | Value |
|---|---|
| Precision@1 (document level) | 95.0% |
| Precision@5 (document level) | 68.0% |
| Precision@10 (document level) | 51.0% |
| Capped Precision@1 (vs. best attainable) | 95.0% |
| Capped Precision@5 (vs. best attainable) | 72.0% |
| Capped Precision@10 (vs. best attainable) | 68.3% |
| Hit@1 (a chunk containing the expected fact) | 60.0% |
| Hit@5 (a chunk containing the expected fact) | 95.0% |
| Hit@10 (a chunk containing the expected fact) | 100.0% |
| MRR (first fact-bearing chunk) | 0.7571 |

## Answers and validation

| Metric | Value |
|---|---|
| Pass rate (validated / in-corpus) | 95.0% |
| Mean confidence (in-corpus) | 0.7953 |
| Answer correct (expected facts present) | 90.0% |
| **Validated precision** (correct among validated) | 89.5% |
| **Validated but wrong** | 10.5% |
| Correct but flagged for review | 5.6% |
| Out-of-corpus sent to review | 60.0% |
| Out-of-corpus falsely validated | 40.0% |
| Decision accuracy (all queries) | 80.0% |

A high pass rate alone is not evidence of quality: an extractive answer is copied from the evidence, so coverage is near-perfect by construction. Validated precision and the validated-but-wrong rate are the meaningful numbers.

## Threshold sweep

| Threshold | Pass rate | Validated precision | Validated but wrong | Correct but flagged | OOC false accept | Decision accuracy |
|---|---|---|---|---|---|---|
| 0.3 | 100.0% | 90.0% | 10.0% | 0.0% | 60.0% | 80.0% |
| 0.35 | 100.0% | 90.0% | 10.0% | 0.0% | 60.0% | 80.0% |
| 0.4 | 100.0% | 90.0% | 10.0% | 0.0% | 60.0% | 80.0% |
| 0.45 | 100.0% | 90.0% | 10.0% | 0.0% | 60.0% | 80.0% |
| 0.5 | 100.0% | 90.0% | 10.0% | 0.0% | 60.0% | 80.0% |
| 0.55 | 100.0% | 90.0% | 10.0% | 0.0% | 40.0% | 84.0% |
| 0.6 | 95.0% | 89.5% | 10.5% | 5.6% | 40.0% | 80.0% |
| 0.65 | 90.0% | 88.9% | 11.1% | 11.1% | 40.0% | 76.0% |
| 0.7 | 85.0% | 88.2% | 11.8% | 16.7% | 40.0% | 72.0% |
| 0.75 | 75.0% | 93.3% | 6.7% | 22.2% | 40.0% | 72.0% |
| 0.8 | 40.0% | 87.5% | 12.5% | 61.1% | 20.0% | 48.0% |
| 0.85 | 30.0% | 83.3% | 16.7% | 72.2% | 0.0% | 44.0% |
| 0.9 | 15.0% | 66.7% | 33.3% | 88.9% | 0.0% | 32.0% |

## Items for analyst review (5)

- **S11** (correct answer withheld, confidence 0.582): What bleach strength is used for blood spills?
- **S15** (VALIDATED BUT WRONG, confidence 0.723): By when should staff be offered the flu vaccine?
- **S23** (VALIDATED BUT WRONG, confidence 1.0): What are the steps of shared decision making?
- **S45** (VALIDATED BUT OUT OF CORPUS, confidence 0.785): How should radioactive waste be disposed of?
- **S47** (VALIDATED BUT OUT OF CORPUS, confidence 0.848): What is the incubation period of influenza?
