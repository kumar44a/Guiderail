# Evaluation summary: real corpus, dev split

- Index: `9bc2368dd16cc348…`  |  generator: `extractive`  |  threshold: 0.6
- Queries: 50 in-corpus, 8 out-of-corpus

## Retrieval (in-corpus queries)

| Metric | Value |
|---|---|
| Precision@1 (document level) | 84.0% |
| Precision@5 (document level) | 76.8% |
| Precision@10 (document level) | 70.4% |
| Capped Precision@1 (vs. best attainable) | 84.0% |
| Capped Precision@5 (vs. best attainable) | 76.8% |
| Capped Precision@10 (vs. best attainable) | 70.4% |
| Hit@1 (a chunk containing the expected fact) | 56.0% |
| Hit@5 (a chunk containing the expected fact) | 78.0% |
| Hit@10 (a chunk containing the expected fact) | 80.0% |
| MRR (first fact-bearing chunk) | 0.6429 |

## Answers and validation

| Metric | Value |
|---|---|
| Pass rate (validated / in-corpus) | 84.0% |
| Mean confidence (in-corpus) | 0.793 |
| Answer correct (expected facts present) | 68.0% |
| **Validated precision** (correct among validated) | 71.4% |
| **Validated but wrong** | 28.6% |
| Correct but flagged for review | 11.8% |
| Out-of-corpus sent to review | 62.5% |
| Out-of-corpus falsely validated | 37.5% |
| Decision accuracy (all queries) | 67.2% |

A high pass rate alone is not evidence of quality: an extractive answer is copied from the evidence, so coverage is near-perfect by construction. Validated precision and the validated-but-wrong rate are the meaningful numbers.

## Threshold sweep

| Threshold | Pass rate | Validated precision | Validated but wrong | Correct but flagged | OOC false accept | Decision accuracy |
|---|---|---|---|---|---|---|
| 0.3 | 100.0% | 68.0% | 32.0% | 0.0% | 87.5% | 60.3% |
| 0.35 | 98.0% | 69.4% | 30.6% | 0.0% | 87.5% | 62.1% |
| 0.4 | 98.0% | 69.4% | 30.6% | 0.0% | 75.0% | 63.8% |
| 0.45 | 96.0% | 70.8% | 29.2% | 0.0% | 75.0% | 65.5% |
| 0.5 | 92.0% | 71.7% | 28.3% | 2.9% | 50.0% | 69.0% |
| 0.55 | 86.0% | 72.1% | 27.9% | 8.8% | 37.5% | 69.0% |
| 0.6 | 84.0% | 71.4% | 28.6% | 11.8% | 37.5% | 67.2% |
| 0.65 | 80.0% | 72.5% | 27.5% | 14.7% | 0.0% | 72.4% |
| 0.7 | 72.0% | 80.6% | 19.4% | 14.7% | 0.0% | 79.3% |
| 0.75 | 68.0% | 82.3% | 17.6% | 17.6% | 0.0% | 79.3% |
| 0.8 | 58.0% | 82.8% | 17.2% | 29.4% | 0.0% | 74.1% |
| 0.85 | 42.0% | 81.0% | 19.1% | 50.0% | 0.0% | 63.8% |
| 0.9 | 36.0% | 77.8% | 22.2% | 58.8% | 0.0% | 58.6% |

## Items for analyst review (23)

- **R07** (correct answer withheld, confidence 0.571): What must a symptomatic visitor do if they are allowed to stay with a patient?
- **R09** (VALIDATED BUT WRONG, confidence 0.728): Where should patients needing droplet precautions be placed in an outpatient setting?
- **T03** (VALIDATED BUT WRONG, confidence 0.905): How often should temperature monitoring devices be calibration tested?
- **R18** (VALIDATED BUT WRONG, confidence 0.65): How long should the entire alcohol handrub procedure take?
- **R28** (VALIDATED BUT WRONG, confidence 1.0): What are the five components of the WHO multimodal hand hygiene improvement strategy?
- **RO5** (VALIDATED BUT OUT OF CORPUS, confidence 0.609): What steam temperature and exposure time are needed to autoclave surgical instruments?
- **R35** (correct answer withheld, confidence 0.5): Should soap and alcohol-based handrub be used concomitantly?
- **R36** (VALIDATED BUT WRONG, confidence 1.0): Should hot water be used for handwashing in health care?
- **RO7** (VALIDATED BUT OUT OF CORPUS, confidence 0.632): What is the recommended dosage of oseltamivir for influenza prophylaxis?
- **N03** (VALIDATED BUT WRONG, confidence 0.664): how accurate does the thermometer have to be
- **N04** (flagged: low confidence, confidence 0.524): what should i set the fridge thermostat to
- **N05** (VALIDATED BUT WRONG, confidence 0.641): after changing the thermostat how long before i check the temperature again
- **N07** (flagged: low confidence, confidence 0.429): how long can mResvia be kept in the fridge
- **N11** (flagged: low confidence, confidence 0.318): how long does norovirus take to make you sick
- **N14** (correct answer withheld, confidence 0.486): how many days of antibiotics are given after environmental exposure
- **N15** (correct answer withheld, confidence 0.543): how many days should mumps patients be isolated
- **N17** (VALIDATED BUT WRONG, confidence 0.675): how long should i rub my hands with sanitiser
- **N18** (VALIDATED BUT WRONG, confidence 0.776): what are the benefits of hand-rub
- **N19** (flagged: low confidence, confidence 0.486): is it ok to wear fake nails around patients
- **N21** (VALIDATED BUT WRONG, confidence 0.663): what percentage alcohol is in the WHO handrub recipe
- **N23** (VALIDATED BUT WRONG, confidence 0.926): can disposable gloves be reused
- **N24** (VALIDATED BUT WRONG, confidence 0.813): what helps with dry cracked skin from hand washing
- **NO1** (VALIDATED BUT OUT OF CORPUS, confidence 0.612): what is the correct paracetamol dose for a child with fever
