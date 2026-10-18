# Evaluation summary: real corpus, dev split

- Index: `0682c9a68340eb12…`  |  generator: `extractive`  |  threshold: 0.6
- Queries: 9 in-corpus, 2 out-of-corpus

## Retrieval (in-corpus queries)

| Metric | Value |
|---|---|
| Precision@1 (document level) | 77.8% |
| Precision@5 (document level) | 93.3% |
| Precision@10 (document level) | 92.2% |
| Capped Precision@1 (vs. best attainable) | 77.8% |
| Capped Precision@5 (vs. best attainable) | 93.3% |
| Capped Precision@10 (vs. best attainable) | 92.2% |
| Hit@1 (a chunk containing the expected fact) | 33.3% |
| Hit@5 (a chunk containing the expected fact) | 66.7% |
| Hit@10 (a chunk containing the expected fact) | 77.8% |
| MRR (first fact-bearing chunk) | 0.4825 |

## Answers and validation

| Metric | Value |
|---|---|
| Pass rate (validated / in-corpus) | 88.9% |
| Mean confidence (in-corpus) | 0.8691 |
| Answer correct (expected facts present) | 44.4% |
| **Validated precision** (correct among validated) | 50.0% |
| **Validated but wrong** | 50.0% |
| Correct but flagged for review | 0.0% |
| Out-of-corpus sent to review | 100.0% |
| Out-of-corpus falsely validated | 0.0% |
| Decision accuracy (all queries) | 63.6% |

A high pass rate alone is not evidence of quality: an extractive answer is copied from the evidence, so coverage is near-perfect by construction. Validated precision and the validated-but-wrong rate are the meaningful numbers.

## Threshold sweep

| Threshold | Pass rate | Validated precision | Validated but wrong | Correct but flagged | OOC false accept | Decision accuracy |
|---|---|---|---|---|---|---|
| 0.3 | 100.0% | 44.4% | 55.6% | 0.0% | 50.0% | 45.5% |
| 0.35 | 100.0% | 44.4% | 55.6% | 0.0% | 50.0% | 45.5% |
| 0.4 | 100.0% | 44.4% | 55.6% | 0.0% | 50.0% | 45.5% |
| 0.45 | 100.0% | 44.4% | 55.6% | 0.0% | 50.0% | 45.5% |
| 0.5 | 100.0% | 44.4% | 55.6% | 0.0% | 0.0% | 54.5% |
| 0.55 | 100.0% | 44.4% | 55.6% | 0.0% | 0.0% | 54.5% |
| 0.6 | 88.9% | 50.0% | 50.0% | 0.0% | 0.0% | 63.6% |
| 0.65 | 88.9% | 50.0% | 50.0% | 0.0% | 0.0% | 63.6% |
| 0.7 | 88.9% | 50.0% | 50.0% | 0.0% | 0.0% | 63.6% |
| 0.75 | 77.8% | 57.1% | 42.9% | 0.0% | 0.0% | 72.7% |
| 0.8 | 66.7% | 50.0% | 50.0% | 25.0% | 0.0% | 63.6% |
| 0.85 | 66.7% | 50.0% | 50.0% | 25.0% | 0.0% | 63.6% |
| 0.9 | 66.7% | 50.0% | 50.0% | 25.0% | 0.0% | 63.6% |

## Items for analyst review (5)

- **R07** (flagged: low confidence, confidence 0.557): What must a symptomatic visitor do if they are allowed to stay with a patient?
- **R09** (VALIDATED BUT WRONG, confidence 0.723): Where should patients needing droplet precautions be placed in an outpatient setting?
- **T01** (VALIDATED BUT WRONG, confidence 1.0): What temperature range must vaccine refrigerators maintain?
- **T03** (VALIDATED BUT WRONG, confidence 0.904): How often should temperature monitoring devices be calibration tested?
- **T07** (VALIDATED BUT WRONG, confidence 1.0): What does the backup vaccine coordinator do?
