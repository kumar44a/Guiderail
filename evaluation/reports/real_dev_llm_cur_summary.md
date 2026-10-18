# Evaluation summary: real corpus, dev split

- Index: `9bc2368dd16cc348…`  |  generator: `llm`  |  threshold: 0.6
- Queries: 24 in-corpus, 5 out-of-corpus

## Retrieval (in-corpus queries)

| Metric | Value |
|---|---|
| Precision@1 (document level) | 95.8% |
| Precision@5 (document level) | 86.7% |
| Precision@10 (document level) | 82.9% |
| Capped Precision@1 (vs. best attainable) | 95.8% |
| Capped Precision@5 (vs. best attainable) | 86.7% |
| Capped Precision@10 (vs. best attainable) | 82.9% |
| Hit@1 (a chunk containing the expected fact) | 70.8% |
| Hit@5 (a chunk containing the expected fact) | 87.5% |
| Hit@10 (a chunk containing the expected fact) | 91.7% |
| MRR (first fact-bearing chunk) | 0.7789 |

## Answers and validation

| Metric | Value |
|---|---|
| Pass rate (validated / in-corpus) | 75.0% |
| Mean confidence (in-corpus) | 0.7435 |
| Answer correct (expected facts present) | 83.3% |
| **Validated precision** (correct among validated) | 94.4% |
| **Validated but wrong** | 5.6% |
| Correct but flagged for review | 15.0% |
| Out-of-corpus sent to review | 100.0% |
| Out-of-corpus falsely validated | 0.0% |
| Decision accuracy (all queries) | 86.2% |

A high pass rate alone is not evidence of quality: an extractive answer is copied from the evidence, so coverage is near-perfect by construction. Validated precision and the validated-but-wrong rate are the meaningful numbers.

## Threshold sweep

| Threshold | Pass rate | Validated precision | Validated but wrong | Correct but flagged | OOC false accept | Decision accuracy |
|---|---|---|---|---|---|---|
| 0.3 | 87.5% | 95.2% | 4.8% | 0.0% | 0.0% | 96.5% |
| 0.35 | 87.5% | 95.2% | 4.8% | 0.0% | 0.0% | 96.5% |
| 0.4 | 83.3% | 95.0% | 5.0% | 5.0% | 0.0% | 93.1% |
| 0.45 | 83.3% | 95.0% | 5.0% | 5.0% | 0.0% | 93.1% |
| 0.5 | 83.3% | 95.0% | 5.0% | 5.0% | 0.0% | 93.1% |
| 0.55 | 79.2% | 94.7% | 5.3% | 10.0% | 0.0% | 89.7% |
| 0.6 | 75.0% | 94.4% | 5.6% | 15.0% | 0.0% | 86.2% |
| 0.65 | 75.0% | 94.4% | 5.6% | 15.0% | 0.0% | 86.2% |
| 0.7 | 75.0% | 94.4% | 5.6% | 15.0% | 0.0% | 86.2% |
| 0.75 | 62.5% | 93.3% | 6.7% | 30.0% | 0.0% | 75.9% |
| 0.8 | 62.5% | 93.3% | 6.7% | 30.0% | 0.0% | 75.9% |
| 0.85 | 58.3% | 92.9% | 7.1% | 35.0% | 0.0% | 72.4% |
| 0.9 | 54.2% | 92.3% | 7.7% | 40.0% | 0.0% | 69.0% |

## Items for analyst review (7)

- **R07** (correct answer withheld, confidence 0.571): What must a symptomatic visitor do if they are allowed to stay with a patient?
- **R09** (flagged: low confidence, confidence 0.0): Where should patients needing droplet precautions be placed in an outpatient setting?
- **T05** (correct answer withheld, confidence 0.369): What label should be put on vaccines after a temperature excursion?
- **R18** (flagged: low confidence, confidence 0.0): How long should the entire alcohol handrub procedure take?
- **R24** (correct answer withheld, confidence 0.5): What is the minimum sink-to-patient bed ratio according to WHO?
- **R28** (flagged: low confidence, confidence 0.0): What are the five components of the WHO multimodal hand hygiene improvement strategy?
- **R36** (VALIDATED BUT WRONG, confidence 0.924): Should hot water be used for handwashing in health care?
