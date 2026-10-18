# Evaluation summary: synthetic corpus, dev split

- Index: `dbe74cc65585202e…`  |  generator: `extractive`  |  threshold: 0.6
- Queries: 20 in-corpus, 5 out-of-corpus

## Retrieval (in-corpus queries)

| Metric | Value |
|---|---|
| Precision@1 (document level) | 90.0% |
| Precision@5 (document level) | 54.0% |
| Precision@10 (document level) | 29.0% |
| Capped Precision@1 (vs. best attainable) | 90.0% |
| Capped Precision@5 (vs. best attainable) | 73.3% |
| Capped Precision@10 (vs. best attainable) | 76.0% |
| Hit@1 (a chunk containing the expected fact) | 60.0% |
| Hit@5 (a chunk containing the expected fact) | 100.0% |
| Hit@10 (a chunk containing the expected fact) | 100.0% |
| MRR (first fact-bearing chunk) | 0.7667 |

## Answers and validation

| Metric | Value |
|---|---|
| Pass rate (validated / in-corpus) | 90.0% |
| Mean confidence (in-corpus) | 0.7682 |
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
| 0.5 | 95.0% | 94.7% | 5.3% | 5.3% | 60.0% | 80.0% |
| 0.55 | 95.0% | 94.7% | 5.3% | 5.3% | 40.0% | 84.0% |
| 0.6 | 90.0% | 94.4% | 5.6% | 10.5% | 40.0% | 80.0% |
| 0.65 | 85.0% | 94.1% | 5.9% | 15.8% | 40.0% | 76.0% |
| 0.7 | 85.0% | 94.1% | 5.9% | 15.8% | 40.0% | 76.0% |
| 0.75 | 65.0% | 92.3% | 7.7% | 36.8% | 20.0% | 64.0% |
| 0.8 | 45.0% | 88.9% | 11.1% | 57.9% | 20.0% | 48.0% |
| 0.85 | 25.0% | 80.0% | 20.0% | 79.0% | 0.0% | 36.0% |
| 0.9 | 10.0% | 100.0% | 0.0% | 89.5% | 0.0% | 32.0% |

## Items for analyst review (5)

- **S05** (correct answer withheld, confidence 0.402): Which infections require soap and water instead of hand rub?
- **S11** (correct answer withheld, confidence 0.578): What bleach strength is used for blood spills?
- **S23** (VALIDATED BUT WRONG, confidence 0.859): What are the steps of shared decision making?
- **S45** (VALIDATED BUT OUT OF CORPUS, confidence 0.73): How should radioactive waste be disposed of?
- **S47** (VALIDATED BUT OUT OF CORPUS, confidence 0.837): What is the incubation period of influenza?
