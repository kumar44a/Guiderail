# Evaluation summary: synthetic corpus, dev split

- Index: `45c3d9422161bc97…`  |  generator: `extractive`  |  threshold: 0.6
- Queries: 20 in-corpus, 5 out-of-corpus

## Retrieval (in-corpus queries)

| Metric | Value |
|---|---|
| Precision@1 (document level) | 95.0% |
| Precision@5 (document level) | 60.0% |
| Precision@10 (document level) | 33.5% |
| Capped Precision@1 (vs. best attainable) | 95.0% |
| Capped Precision@5 (vs. best attainable) | 80.8% |
| Capped Precision@10 (vs. best attainable) | 84.9% |
| Hit@1 (a chunk containing the expected fact) | 70.0% |
| Hit@5 (a chunk containing the expected fact) | 100.0% |
| Hit@10 (a chunk containing the expected fact) | 100.0% |
| MRR (first fact-bearing chunk) | 0.825 |

## Answers and validation

| Metric | Value |
|---|---|
| Pass rate (validated / in-corpus) | 95.0% |
| Mean confidence (in-corpus) | 0.794 |
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
| 0.7 | 80.0% | 93.8% | 6.2% | 21.1% | 40.0% | 72.0% |
| 0.75 | 65.0% | 92.3% | 7.7% | 36.8% | 20.0% | 64.0% |
| 0.8 | 50.0% | 90.0% | 10.0% | 52.6% | 20.0% | 52.0% |
| 0.85 | 30.0% | 83.3% | 16.7% | 73.7% | 0.0% | 40.0% |
| 0.9 | 15.0% | 66.7% | 33.3% | 89.5% | 0.0% | 28.0% |

## Items for analyst review (4)

- **S11** (correct answer withheld, confidence 0.578): What bleach strength is used for blood spills?
- **S23** (VALIDATED BUT WRONG, confidence 1.0): What are the steps of shared decision making?
- **S45** (VALIDATED BUT OUT OF CORPUS, confidence 0.745): How should radioactive waste be disposed of?
- **S47** (VALIDATED BUT OUT OF CORPUS, confidence 0.837): What is the incubation period of influenza?
