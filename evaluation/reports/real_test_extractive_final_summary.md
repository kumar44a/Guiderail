# Evaluation summary: real corpus, test split

- Index: `9bc2368dd16cc348…`  |  generator: `extractive`  |  threshold: 0.6
- Queries: 16 in-corpus, 3 out-of-corpus

## Retrieval (in-corpus queries)

| Metric | Value |
|---|---|
| Precision@1 (document level) | 100.0% |
| Precision@5 (document level) | 90.0% |
| Precision@10 (document level) | 81.9% |
| Capped Precision@1 (vs. best attainable) | 100.0% |
| Capped Precision@5 (vs. best attainable) | 90.0% |
| Capped Precision@10 (vs. best attainable) | 81.9% |
| Hit@1 (a chunk containing the expected fact) | 56.2% |
| Hit@5 (a chunk containing the expected fact) | 81.2% |
| Hit@10 (a chunk containing the expected fact) | 81.2% |
| MRR (first fact-bearing chunk) | 0.6427 |

## Answers and validation

| Metric | Value |
|---|---|
| Pass rate (validated / in-corpus) | 93.8% |
| Mean confidence (in-corpus) | 0.8704 |
| Answer correct (expected facts present) | 62.5% |
| **Validated precision** (correct among validated) | 66.7% |
| **Validated but wrong** | 33.3% |
| Correct but flagged for review | 0.0% |
| Out-of-corpus sent to review | 33.3% |
| Out-of-corpus falsely validated | 66.7% |
| Decision accuracy (all queries) | 63.2% |

A high pass rate alone is not evidence of quality: an extractive answer is copied from the evidence, so coverage is near-perfect by construction. Validated precision and the validated-but-wrong rate are the meaningful numbers.

## Threshold sweep

| Threshold | Pass rate | Validated precision | Validated but wrong | Correct but flagged | OOC false accept | Decision accuracy |
|---|---|---|---|---|---|---|
| 0.3 | 100.0% | 62.5% | 37.5% | 0.0% | 100.0% | 52.6% |
| 0.35 | 100.0% | 62.5% | 37.5% | 0.0% | 100.0% | 52.6% |
| 0.4 | 100.0% | 62.5% | 37.5% | 0.0% | 100.0% | 52.6% |
| 0.45 | 100.0% | 62.5% | 37.5% | 0.0% | 100.0% | 52.6% |
| 0.5 | 93.8% | 66.7% | 33.3% | 0.0% | 100.0% | 57.9% |
| 0.55 | 93.8% | 66.7% | 33.3% | 0.0% | 66.7% | 63.2% |
| 0.6 | 93.8% | 66.7% | 33.3% | 0.0% | 66.7% | 63.2% |
| 0.65 | 87.5% | 71.4% | 28.6% | 0.0% | 66.7% | 68.4% |
| 0.7 | 87.5% | 71.4% | 28.6% | 0.0% | 33.3% | 73.7% |
| 0.75 | 81.2% | 76.9% | 23.1% | 0.0% | 33.3% | 79.0% |
| 0.8 | 75.0% | 83.3% | 16.7% | 0.0% | 33.3% | 84.2% |
| 0.85 | 75.0% | 83.3% | 16.7% | 0.0% | 33.3% | 84.2% |
| 0.9 | 62.5% | 90.0% | 10.0% | 10.0% | 33.3% | 84.2% |

## Items for analyst review (8)

- **R02** (flagged: low confidence, confidence 0.47): What does cohorting mean?
- **R10** (VALIDATED BUT WRONG, confidence 0.879): Which infections are examples that require an airborne infection isolation room?
- **T04** (VALIDATED BUT WRONG, confidence 0.619): How long should temperature logs be kept?
- **RO2** (VALIDATED BUT OUT OF CORPUS, confidence 0.68): How should radioactive waste be disposed of?
- **RO4** (VALIDATED BUT OUT OF CORPUS, confidence 0.918): What is the capital of France?
- **R19** (VALIDATED BUT WRONG, confidence 0.722): How long does the full procedure of washing hands with soap and water take?
- **R23** (VALIDATED BUT WRONG, confidence 1.0): What alcohol concentrations do the WHO-recommended handrub formulations contain?
- **R32** (VALIDATED BUT WRONG, confidence 0.791): At which moments are health-care workers asked to clean their hands?
