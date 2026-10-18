# Evaluation summary: real corpus, dev split

- Index: `0682c9a68340eb12…`  |  generator: `extractive`  |  threshold: 0.6
- Queries: 9 in-corpus, 2 out-of-corpus

## Retrieval (in-corpus queries)

| Metric | Value |
|---|---|
| Precision@1 (document level) | 88.9% |
| Precision@5 (document level) | 93.3% |
| Precision@10 (document level) | 95.6% |
| Capped Precision@1 (vs. best attainable) | 88.9% |
| Capped Precision@5 (vs. best attainable) | 93.3% |
| Capped Precision@10 (vs. best attainable) | 95.6% |
| Hit@1 (a chunk containing the expected fact) | 66.7% |
| Hit@5 (a chunk containing the expected fact) | 88.9% |
| Hit@10 (a chunk containing the expected fact) | 88.9% |
| MRR (first fact-bearing chunk) | 0.7593 |

## Answers and validation

| Metric | Value |
|---|---|
| Pass rate (validated / in-corpus) | 88.9% |
| Mean confidence (in-corpus) | 0.9008 |
| Answer correct (expected facts present) | 77.8% |
| **Validated precision** (correct among validated) | 75.0% |
| **Validated but wrong** | 25.0% |
| Correct but flagged for review | 14.3% |
| Out-of-corpus sent to review | 100.0% |
| Out-of-corpus falsely validated | 0.0% |
| Decision accuracy (all queries) | 72.7% |

A high pass rate alone is not evidence of quality: an extractive answer is copied from the evidence, so coverage is near-perfect by construction. Validated precision and the validated-but-wrong rate are the meaningful numbers.

## Threshold sweep

| Threshold | Pass rate | Validated precision | Validated but wrong | Correct but flagged | OOC false accept | Decision accuracy |
|---|---|---|---|---|---|---|
| 0.3 | 100.0% | 77.8% | 22.2% | 0.0% | 50.0% | 72.7% |
| 0.35 | 100.0% | 77.8% | 22.2% | 0.0% | 50.0% | 72.7% |
| 0.4 | 100.0% | 77.8% | 22.2% | 0.0% | 50.0% | 72.7% |
| 0.45 | 100.0% | 77.8% | 22.2% | 0.0% | 0.0% | 81.8% |
| 0.5 | 100.0% | 77.8% | 22.2% | 0.0% | 0.0% | 81.8% |
| 0.55 | 100.0% | 77.8% | 22.2% | 0.0% | 0.0% | 81.8% |
| 0.6 | 88.9% | 75.0% | 25.0% | 14.3% | 0.0% | 72.7% |
| 0.65 | 88.9% | 75.0% | 25.0% | 14.3% | 0.0% | 72.7% |
| 0.7 | 88.9% | 75.0% | 25.0% | 14.3% | 0.0% | 72.7% |
| 0.75 | 88.9% | 75.0% | 25.0% | 14.3% | 0.0% | 72.7% |
| 0.8 | 77.8% | 71.4% | 28.6% | 28.6% | 0.0% | 63.6% |
| 0.85 | 77.8% | 71.4% | 28.6% | 28.6% | 0.0% | 63.6% |
| 0.9 | 77.8% | 71.4% | 28.6% | 28.6% | 0.0% | 63.6% |

## Items for analyst review (3)

- **R07** (correct answer withheld, confidence 0.565): What must a symptomatic visitor do if they are allowed to stay with a patient?
- **R09** (VALIDATED BUT WRONG, confidence 1.0): Where should patients needing droplet precautions be placed in an outpatient setting?
- **T03** (VALIDATED BUT WRONG, confidence 0.904): How often should temperature monitoring devices be calibration tested?
