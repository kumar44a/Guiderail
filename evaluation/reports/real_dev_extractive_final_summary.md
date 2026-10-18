# Evaluation summary: real corpus, dev split

- Index: `9bc2368dd16cc348…`  |  generator: `extractive`  |  threshold: 0.6
- Queries: 16 in-corpus, 3 out-of-corpus

## Retrieval (in-corpus queries)

| Metric | Value |
|---|---|
| Precision@1 (document level) | 93.8% |
| Precision@5 (document level) | 85.0% |
| Precision@10 (document level) | 84.4% |
| Capped Precision@1 (vs. best attainable) | 93.8% |
| Capped Precision@5 (vs. best attainable) | 85.0% |
| Capped Precision@10 (vs. best attainable) | 84.4% |
| Hit@1 (a chunk containing the expected fact) | 68.8% |
| Hit@5 (a chunk containing the expected fact) | 81.2% |
| Hit@10 (a chunk containing the expected fact) | 87.5% |
| MRR (first fact-bearing chunk) | 0.7465 |

## Answers and validation

| Metric | Value |
|---|---|
| Pass rate (validated / in-corpus) | 93.8% |
| Mean confidence (in-corpus) | 0.8711 |
| Answer correct (expected facts present) | 75.0% |
| **Validated precision** (correct among validated) | 73.3% |
| **Validated but wrong** | 26.7% |
| Correct but flagged for review | 8.3% |
| Out-of-corpus sent to review | 66.7% |
| Out-of-corpus falsely validated | 33.3% |
| Decision accuracy (all queries) | 68.4% |

A high pass rate alone is not evidence of quality: an extractive answer is copied from the evidence, so coverage is near-perfect by construction. Validated precision and the validated-but-wrong rate are the meaningful numbers.

## Threshold sweep

| Threshold | Pass rate | Validated precision | Validated but wrong | Correct but flagged | OOC false accept | Decision accuracy |
|---|---|---|---|---|---|---|
| 0.3 | 100.0% | 75.0% | 25.0% | 0.0% | 100.0% | 63.2% |
| 0.35 | 100.0% | 75.0% | 25.0% | 0.0% | 100.0% | 63.2% |
| 0.4 | 100.0% | 75.0% | 25.0% | 0.0% | 100.0% | 63.2% |
| 0.45 | 100.0% | 75.0% | 25.0% | 0.0% | 100.0% | 63.2% |
| 0.5 | 100.0% | 75.0% | 25.0% | 0.0% | 66.7% | 68.4% |
| 0.55 | 100.0% | 75.0% | 25.0% | 0.0% | 33.3% | 73.7% |
| 0.6 | 93.8% | 73.3% | 26.7% | 8.3% | 33.3% | 68.4% |
| 0.65 | 93.8% | 73.3% | 26.7% | 8.3% | 0.0% | 73.7% |
| 0.7 | 87.5% | 78.6% | 21.4% | 8.3% | 0.0% | 79.0% |
| 0.75 | 81.2% | 84.6% | 15.4% | 8.3% | 0.0% | 84.2% |
| 0.8 | 75.0% | 83.3% | 16.7% | 16.7% | 0.0% | 79.0% |
| 0.85 | 62.5% | 80.0% | 20.0% | 33.3% | 0.0% | 68.4% |
| 0.9 | 62.5% | 80.0% | 20.0% | 33.3% | 0.0% | 68.4% |

## Items for analyst review (6)

- **R07** (correct answer withheld, confidence 0.571): What must a symptomatic visitor do if they are allowed to stay with a patient?
- **R09** (VALIDATED BUT WRONG, confidence 0.728): Where should patients needing droplet precautions be placed in an outpatient setting?
- **T03** (VALIDATED BUT WRONG, confidence 0.905): How often should temperature monitoring devices be calibration tested?
- **R18** (VALIDATED BUT WRONG, confidence 0.65): How long should the entire alcohol handrub procedure take?
- **R28** (VALIDATED BUT WRONG, confidence 1.0): What are the five components of the WHO multimodal hand hygiene improvement strategy?
- **RO5** (VALIDATED BUT OUT OF CORPUS, confidence 0.609): What steam temperature and exposure time are needed to autoclave surgical instruments?
