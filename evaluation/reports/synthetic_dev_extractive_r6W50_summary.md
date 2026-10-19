# Evaluation summary: synthetic corpus, dev split

- Index: `33a339cb7982362c…`  |  generator: `extractive`  |  threshold: 0.6
- Queries: 20 in-corpus, 5 out-of-corpus

## Retrieval (in-corpus queries)

| Metric | Value |
|---|---|
| Precision@1 (document level) | 90.0% |
| Precision@5 (document level) | 59.0% |
| Precision@10 (document level) | 34.0% |
| Capped Precision@1 (vs. best attainable) | 90.0% |
| Capped Precision@5 (vs. best attainable) | 71.2% |
| Capped Precision@10 (vs. best attainable) | 78.1% |
| Hit@1 (a chunk containing the expected fact) | 65.0% |
| Hit@5 (a chunk containing the expected fact) | 100.0% |
| Hit@10 (a chunk containing the expected fact) | 100.0% |
| MRR (first fact-bearing chunk) | 0.8042 |

## Answers and validation

| Metric | Value |
|---|---|
| Pass rate (validated / in-corpus) | 90.0% |
| Mean confidence (in-corpus) | 0.7569 |
| Answer correct (expected facts present) | 95.0% |
| **Validated precision** (correct among validated) | 94.4% |
| **Validated but wrong** | 5.6% |
| Correct but flagged for review | 10.5% |
| Out-of-corpus sent to review | 60.0% |
| Out-of-corpus falsely validated | 40.0% |
| Decision accuracy (all queries) | 80.0% |

A high pass rate alone is not evidence of quality: an extractive answer is copied from the evidence, so coverage is near-perfect by construction. Validated precision and the validated-but-wrong rate are the meaningful numbers.

## Threshold sweep

| Threshold | Pass rate | Validated precision | Validated but wrong | Correct but flagged | OOC false accept | Decision accuracy |
|---|---|---|---|---|---|---|
| 0.3 | 100.0% | 95.0% | 5.0% | 0.0% | 80.0% | 80.0% |
| 0.35 | 100.0% | 95.0% | 5.0% | 0.0% | 60.0% | 84.0% |
| 0.4 | 100.0% | 95.0% | 5.0% | 0.0% | 60.0% | 84.0% |
| 0.45 | 95.0% | 94.7% | 5.3% | 5.3% | 60.0% | 80.0% |
| 0.5 | 90.0% | 94.4% | 5.6% | 10.5% | 60.0% | 76.0% |
| 0.55 | 90.0% | 94.4% | 5.6% | 10.5% | 40.0% | 80.0% |
| 0.6 | 90.0% | 94.4% | 5.6% | 10.5% | 40.0% | 80.0% |
| 0.65 | 75.0% | 93.3% | 6.7% | 26.3% | 40.0% | 68.0% |
| 0.7 | 70.0% | 92.9% | 7.1% | 31.6% | 20.0% | 68.0% |
| 0.75 | 65.0% | 92.3% | 7.7% | 36.8% | 20.0% | 64.0% |
| 0.8 | 45.0% | 88.9% | 11.1% | 57.9% | 0.0% | 52.0% |
| 0.85 | 30.0% | 83.3% | 16.7% | 73.7% | 0.0% | 40.0% |
| 0.9 | 10.0% | 100.0% | 0.0% | 89.5% | 0.0% | 32.0% |

## Items for analyst review (5)

- **S11** (correct answer withheld, confidence 0.441): What bleach strength is used for blood spills?
- **S15** (correct answer withheld, confidence 0.492): By when should staff be offered the flu vaccine?
- **S23** (VALIDATED BUT WRONG, confidence 0.855): What are the steps of shared decision making?
- **S45** (VALIDATED BUT OUT OF CORPUS, confidence 0.796): How should radioactive waste be disposed of?
- **S47** (VALIDATED BUT OUT OF CORPUS, confidence 0.671): What is the incubation period of influenza?
