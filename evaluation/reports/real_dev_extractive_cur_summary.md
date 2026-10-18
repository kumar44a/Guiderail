# Evaluation summary: real corpus, dev split

- Index: `9bc2368dd16cc348…`  |  generator: `extractive`  |  threshold: 0.6
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
| Pass rate (validated / in-corpus) | 91.7% |
| Mean confidence (in-corpus) | 0.8828 |
| Answer correct (expected facts present) | 79.2% |
| **Validated precision** (correct among validated) | 77.3% |
| **Validated but wrong** | 22.7% |
| Correct but flagged for review | 10.5% |
| Out-of-corpus sent to review | 60.0% |
| Out-of-corpus falsely validated | 40.0% |
| Decision accuracy (all queries) | 69.0% |

A high pass rate alone is not evidence of quality: an extractive answer is copied from the evidence, so coverage is near-perfect by construction. Validated precision and the validated-but-wrong rate are the meaningful numbers.

## Threshold sweep

| Threshold | Pass rate | Validated precision | Validated but wrong | Correct but flagged | OOC false accept | Decision accuracy |
|---|---|---|---|---|---|---|
| 0.3 | 100.0% | 79.2% | 20.8% | 0.0% | 100.0% | 65.5% |
| 0.35 | 100.0% | 79.2% | 20.8% | 0.0% | 100.0% | 65.5% |
| 0.4 | 100.0% | 79.2% | 20.8% | 0.0% | 100.0% | 65.5% |
| 0.45 | 100.0% | 79.2% | 20.8% | 0.0% | 100.0% | 65.5% |
| 0.5 | 100.0% | 79.2% | 20.8% | 0.0% | 60.0% | 72.4% |
| 0.55 | 95.8% | 78.3% | 21.7% | 5.3% | 40.0% | 72.4% |
| 0.6 | 91.7% | 77.3% | 22.7% | 10.5% | 40.0% | 69.0% |
| 0.65 | 91.7% | 77.3% | 22.7% | 10.5% | 0.0% | 75.9% |
| 0.7 | 87.5% | 81.0% | 19.1% | 10.5% | 0.0% | 79.3% |
| 0.75 | 83.3% | 85.0% | 15.0% | 10.5% | 0.0% | 82.8% |
| 0.8 | 79.2% | 84.2% | 15.8% | 15.8% | 0.0% | 79.3% |
| 0.85 | 70.8% | 82.3% | 17.6% | 26.3% | 0.0% | 72.4% |
| 0.9 | 66.7% | 81.2% | 18.8% | 31.6% | 0.0% | 69.0% |

## Items for analyst review (9)

- **R07** (correct answer withheld, confidence 0.571): What must a symptomatic visitor do if they are allowed to stay with a patient?
- **R09** (VALIDATED BUT WRONG, confidence 0.728): Where should patients needing droplet precautions be placed in an outpatient setting?
- **T03** (VALIDATED BUT WRONG, confidence 0.905): How often should temperature monitoring devices be calibration tested?
- **R18** (VALIDATED BUT WRONG, confidence 0.65): How long should the entire alcohol handrub procedure take?
- **R28** (VALIDATED BUT WRONG, confidence 1.0): What are the five components of the WHO multimodal hand hygiene improvement strategy?
- **RO5** (VALIDATED BUT OUT OF CORPUS, confidence 0.609): What steam temperature and exposure time are needed to autoclave surgical instruments?
- **R35** (correct answer withheld, confidence 0.5): Should soap and alcohol-based handrub be used concomitantly?
- **R36** (VALIDATED BUT WRONG, confidence 1.0): Should hot water be used for handwashing in health care?
- **RO7** (VALIDATED BUT OUT OF CORPUS, confidence 0.632): What is the recommended dosage of oseltamivir for influenza prophylaxis?
