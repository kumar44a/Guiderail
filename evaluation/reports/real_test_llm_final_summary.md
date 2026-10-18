# Evaluation summary: real corpus, test split

- Index: `0682c9a68340eb12…`  |  generator: `llm`  |  threshold: 0.6
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
| Pass rate (validated / in-corpus) | 62.5% |
| Mean confidence (in-corpus) | 0.6814 |
| Answer correct (expected facts present) | 87.5% |
| **Validated precision** (correct among validated) | 100.0% |
| **Validated but wrong** | 0.0% |
| Correct but flagged for review | 28.6% |
| Out-of-corpus sent to review | 100.0% |
| Out-of-corpus falsely validated | 0.0% |
| Decision accuracy (all queries) | 80.0% |

A high pass rate alone is not evidence of quality: an extractive answer is copied from the evidence, so coverage is near-perfect by construction. Validated precision and the validated-but-wrong rate are the meaningful numbers.

## Threshold sweep

| Threshold | Pass rate | Validated precision | Validated but wrong | Correct but flagged | OOC false accept | Decision accuracy |
|---|---|---|---|---|---|---|
| 0.3 | 87.5% | 100.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| 0.35 | 87.5% | 100.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| 0.4 | 87.5% | 100.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| 0.45 | 75.0% | 100.0% | 0.0% | 14.3% | 0.0% | 90.0% |
| 0.5 | 75.0% | 100.0% | 0.0% | 14.3% | 0.0% | 90.0% |
| 0.55 | 62.5% | 100.0% | 0.0% | 28.6% | 0.0% | 80.0% |
| 0.6 | 62.5% | 100.0% | 0.0% | 28.6% | 0.0% | 80.0% |
| 0.65 | 62.5% | 100.0% | 0.0% | 28.6% | 0.0% | 80.0% |
| 0.7 | 62.5% | 100.0% | 0.0% | 28.6% | 0.0% | 80.0% |
| 0.75 | 62.5% | 100.0% | 0.0% | 28.6% | 0.0% | 80.0% |
| 0.8 | 62.5% | 100.0% | 0.0% | 28.6% | 0.0% | 80.0% |
| 0.85 | 50.0% | 100.0% | 0.0% | 42.9% | 0.0% | 70.0% |
| 0.9 | 37.5% | 100.0% | 0.0% | 57.1% | 0.0% | 60.0% |

## Items for analyst review (3)

- **R02** (correct answer withheld, confidence 0.427): What does cohorting mean?
- **R06** (flagged: low confidence, confidence 0.0): What should patients wear when they must be moved outside an airborne infection isolation room?
- **T04** (correct answer withheld, confidence 0.52): How long should temperature logs be kept?
