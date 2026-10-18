# Evaluation summary: real corpus, dev split

- Index: `0682c9a68340eb12…`  |  generator: `llm`  |  threshold: 0.6
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
| Pass rate (validated / in-corpus) | 55.6% |
| Mean confidence (in-corpus) | 0.6591 |
| Answer correct (expected facts present) | 77.8% |
| **Validated precision** (correct among validated) | 80.0% |
| **Validated but wrong** | 20.0% |
| Correct but flagged for review | 42.9% |
| Out-of-corpus sent to review | 100.0% |
| Out-of-corpus falsely validated | 0.0% |
| Decision accuracy (all queries) | 63.6% |

A high pass rate alone is not evidence of quality: an extractive answer is copied from the evidence, so coverage is near-perfect by construction. Validated precision and the validated-but-wrong rate are the meaningful numbers.

## Threshold sweep

| Threshold | Pass rate | Validated precision | Validated but wrong | Correct but flagged | OOC false accept | Decision accuracy |
|---|---|---|---|---|---|---|
| 0.3 | 88.9% | 87.5% | 12.5% | 0.0% | 0.0% | 90.9% |
| 0.35 | 77.8% | 85.7% | 14.3% | 14.3% | 0.0% | 81.8% |
| 0.4 | 77.8% | 85.7% | 14.3% | 14.3% | 0.0% | 81.8% |
| 0.45 | 77.8% | 85.7% | 14.3% | 14.3% | 0.0% | 81.8% |
| 0.5 | 77.8% | 85.7% | 14.3% | 14.3% | 0.0% | 81.8% |
| 0.55 | 77.8% | 85.7% | 14.3% | 14.3% | 0.0% | 81.8% |
| 0.6 | 55.6% | 80.0% | 20.0% | 42.9% | 0.0% | 63.6% |
| 0.65 | 55.6% | 80.0% | 20.0% | 42.9% | 0.0% | 63.6% |
| 0.7 | 55.6% | 80.0% | 20.0% | 42.9% | 0.0% | 63.6% |
| 0.75 | 55.6% | 80.0% | 20.0% | 42.9% | 0.0% | 63.6% |
| 0.8 | 55.6% | 80.0% | 20.0% | 42.9% | 0.0% | 63.6% |
| 0.85 | 55.6% | 80.0% | 20.0% | 42.9% | 0.0% | 63.6% |
| 0.9 | 22.2% | 50.0% | 50.0% | 85.7% | 0.0% | 36.4% |

## Items for analyst review (5)

- **R01** (correct answer withheld, confidence 0.598): What respiratory protection should staff use when entering an airborne infection isolation room?
- **R07** (correct answer withheld, confidence 0.565): What must a symptomatic visitor do if they are allowed to stay with a patient?
- **R09** (flagged: low confidence, confidence 0.0): Where should patients needing droplet precautions be placed in an outpatient setting?
- **T05** (correct answer withheld, confidence 0.348): What label should be put on vaccines after a temperature excursion?
- **T07** (VALIDATED BUT WRONG, confidence 0.951): What does the backup vaccine coordinator do?
