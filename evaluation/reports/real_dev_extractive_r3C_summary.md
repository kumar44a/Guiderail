# Evaluation summary: real corpus, dev split

- Index: `9bc2368dd16cc348…`  |  generator: `extractive`  |  threshold: 0.6
- Queries: 50 in-corpus, 8 out-of-corpus

## Retrieval (in-corpus queries)

| Metric | Value |
|---|---|
| Precision@1 (document level) | 86.0% |
| Precision@5 (document level) | 81.2% |
| Precision@10 (document level) | 75.6% |
| Capped Precision@1 (vs. best attainable) | 86.0% |
| Capped Precision@5 (vs. best attainable) | 81.2% |
| Capped Precision@10 (vs. best attainable) | 75.6% |
| Hit@1 (a chunk containing the expected fact) | 56.0% |
| Hit@5 (a chunk containing the expected fact) | 82.0% |
| Hit@10 (a chunk containing the expected fact) | 86.0% |
| MRR (first fact-bearing chunk) | 0.6589 |

## Answers and validation

| Metric | Value |
|---|---|
| Pass rate (validated / in-corpus) | 88.0% |
| Mean confidence (in-corpus) | 0.8196 |
| Answer correct (expected facts present) | 72.0% |
| **Validated precision** (correct among validated) | 72.7% |
| **Validated but wrong** | 27.3% |
| Correct but flagged for review | 11.1% |
| Out-of-corpus sent to review | 75.0% |
| Out-of-corpus falsely validated | 25.0% |
| Decision accuracy (all queries) | 69.0% |

A high pass rate alone is not evidence of quality: an extractive answer is copied from the evidence, so coverage is near-perfect by construction. Validated precision and the validated-but-wrong rate are the meaningful numbers.

## Threshold sweep

| Threshold | Pass rate | Validated precision | Validated but wrong | Correct but flagged | OOC false accept | Decision accuracy |
|---|---|---|---|---|---|---|
| 0.3 | 100.0% | 72.0% | 28.0% | 0.0% | 100.0% | 62.1% |
| 0.35 | 98.0% | 73.5% | 26.5% | 0.0% | 100.0% | 63.8% |
| 0.4 | 98.0% | 73.5% | 26.5% | 0.0% | 87.5% | 65.5% |
| 0.45 | 98.0% | 73.5% | 26.5% | 0.0% | 87.5% | 65.5% |
| 0.5 | 96.0% | 72.9% | 27.1% | 2.8% | 50.0% | 69.0% |
| 0.55 | 90.0% | 73.3% | 26.7% | 8.3% | 25.0% | 70.7% |
| 0.6 | 88.0% | 72.7% | 27.3% | 11.1% | 25.0% | 69.0% |
| 0.65 | 82.0% | 75.6% | 24.4% | 13.9% | 0.0% | 74.1% |
| 0.7 | 74.0% | 78.4% | 21.6% | 19.4% | 0.0% | 74.1% |
| 0.75 | 72.0% | 77.8% | 22.2% | 22.2% | 0.0% | 72.4% |
| 0.8 | 66.0% | 78.8% | 21.2% | 27.8% | 0.0% | 70.7% |
| 0.85 | 50.0% | 76.0% | 24.0% | 47.2% | 0.0% | 60.3% |
| 0.9 | 42.0% | 71.4% | 28.6% | 58.3% | 0.0% | 53.4% |

## Items for analyst review (20)

- **R07** (correct answer withheld, confidence 0.571): What must a symptomatic visitor do if they are allowed to stay with a patient?
- **R09** (VALIDATED BUT WRONG, confidence 1.0): Where should patients needing droplet precautions be placed in an outpatient setting?
- **T03** (VALIDATED BUT WRONG, confidence 0.905): How often should temperature monitoring devices be calibration tested?
- **R28** (VALIDATED BUT WRONG, confidence 1.0): What are the five components of the WHO multimodal hand hygiene improvement strategy?
- **RO5** (VALIDATED BUT OUT OF CORPUS, confidence 0.609): What steam temperature and exposure time are needed to autoclave surgical instruments?
- **R35** (correct answer withheld, confidence 0.5): Should soap and alcohol-based handrub be used concomitantly?
- **R36** (VALIDATED BUT WRONG, confidence 1.0): Should hot water be used for handwashing in health care?
- **RO7** (VALIDATED BUT OUT OF CORPUS, confidence 0.632): What is the recommended dosage of oseltamivir for influenza prophylaxis?
- **N03** (VALIDATED BUT WRONG, confidence 1.0): how accurate does the thermometer have to be
- **N05** (VALIDATED BUT WRONG, confidence 0.652): after changing the thermostat how long before i check the temperature again
- **N07** (VALIDATED BUT WRONG, confidence 0.617): how long can mResvia be kept in the fridge
- **N11** (flagged: low confidence, confidence 0.316): how long does norovirus take to make you sick
- **N14** (correct answer withheld, confidence 0.486): how many days of antibiotics are given after environmental exposure
- **N15** (correct answer withheld, confidence 0.543): how many days should mumps patients be isolated
- **N17** (VALIDATED BUT WRONG, confidence 0.645): how long should i rub my hands with sanitiser
- **N18** (VALIDATED BUT WRONG, confidence 0.776): what are the benefits of hand-rub
- **N19** (flagged: low confidence, confidence 0.542): is it ok to wear fake nails around patients
- **N21** (VALIDATED BUT WRONG, confidence 0.663): what percentage alcohol is in the WHO handrub recipe
- **N23** (VALIDATED BUT WRONG, confidence 0.926): can disposable gloves be reused
- **N24** (VALIDATED BUT WRONG, confidence 0.813): what helps with dry cracked skin from hand washing
