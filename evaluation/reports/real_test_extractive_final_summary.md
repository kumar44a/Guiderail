# Evaluation summary: real corpus, test split

- Index: `0682c9a68340eb12…`  |  generator: `extractive`  |  threshold: 0.6
- Queries: 8 in-corpus, 2 out-of-corpus

## Retrieval (in-corpus queries)

| Metric | Value |
|---|---|
| Precision@1 (document level) | 100.0% |
| Precision@5 (document level) | 100.0% |
| Precision@10 (document level) | 92.5% |
| Capped Precision@1 (vs. best attainable) | 100.0% |
| Capped Precision@5 (vs. best attainable) | 100.0% |
| Capped Precision@10 (vs. best attainable) | 92.5% |
| Hit@1 (a chunk containing the expected fact) | 37.5% |
| Hit@5 (a chunk containing the expected fact) | 100.0% |
| Hit@10 (a chunk containing the expected fact) | 100.0% |
| MRR (first fact-bearing chunk) | 0.5708 |

## Answers and validation

| Metric | Value |
|---|---|
| Pass rate (validated / in-corpus) | 100.0% |
| Mean confidence (in-corpus) | 0.8706 |
| Answer correct (expected facts present) | 62.5% |
| **Validated precision** (correct among validated) | 62.5% |
| **Validated but wrong** | 37.5% |
| Correct but flagged for review | 0.0% |
| Out-of-corpus sent to review | 50.0% |
| Out-of-corpus falsely validated | 50.0% |
| Decision accuracy (all queries) | 60.0% |

A high pass rate alone is not evidence of quality: an extractive answer is copied from the evidence, so coverage is near-perfect by construction. Validated precision and the validated-but-wrong rate are the meaningful numbers.

## Threshold sweep

| Threshold | Pass rate | Validated precision | Validated but wrong | Correct but flagged | OOC false accept | Decision accuracy |
|---|---|---|---|---|---|---|
| 0.3 | 100.0% | 62.5% | 37.5% | 0.0% | 100.0% | 50.0% |
| 0.35 | 100.0% | 62.5% | 37.5% | 0.0% | 100.0% | 50.0% |
| 0.4 | 100.0% | 62.5% | 37.5% | 0.0% | 100.0% | 50.0% |
| 0.45 | 100.0% | 62.5% | 37.5% | 0.0% | 100.0% | 50.0% |
| 0.5 | 100.0% | 62.5% | 37.5% | 0.0% | 100.0% | 50.0% |
| 0.55 | 100.0% | 62.5% | 37.5% | 0.0% | 50.0% | 60.0% |
| 0.6 | 100.0% | 62.5% | 37.5% | 0.0% | 50.0% | 60.0% |
| 0.65 | 87.5% | 71.4% | 28.6% | 0.0% | 50.0% | 70.0% |
| 0.7 | 87.5% | 71.4% | 28.6% | 0.0% | 0.0% | 80.0% |
| 0.75 | 75.0% | 83.3% | 16.7% | 0.0% | 0.0% | 90.0% |
| 0.8 | 75.0% | 83.3% | 16.7% | 0.0% | 0.0% | 90.0% |
| 0.85 | 75.0% | 83.3% | 16.7% | 0.0% | 0.0% | 90.0% |
| 0.9 | 62.5% | 100.0% | 0.0% | 0.0% | 0.0% | 100.0% |

## Items for analyst review (4)

- **R02** (VALIDATED BUT WRONG, confidence 0.711): What does cohorting mean?
- **R10** (VALIDATED BUT WRONG, confidence 0.874): Which infections are examples that require an airborne infection isolation room?
- **T04** (VALIDATED BUT WRONG, confidence 0.617): How long should temperature logs be kept?
- **RO2** (VALIDATED BUT OUT OF CORPUS, confidence 0.678): How should radioactive waste be disposed of?
