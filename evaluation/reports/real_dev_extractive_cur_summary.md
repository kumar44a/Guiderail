# Evaluation summary: real corpus, dev split

- Index: `9bc2368dd16cc348…`  |  generator: `extractive`  |  threshold: 0.6
- Queries: 50 in-corpus, 8 out-of-corpus

## Retrieval (in-corpus queries)

| Metric | Value |
|---|---|
| Precision@1 (document level) | 84.0% |
| Precision@5 (document level) | 79.2% |
| Precision@10 (document level) | 74.6% |
| Capped Precision@1 (vs. best attainable) | 84.0% |
| Capped Precision@5 (vs. best attainable) | 79.2% |
| Capped Precision@10 (vs. best attainable) | 74.6% |
| Hit@1 (a chunk containing the expected fact) | 56.0% |
| Hit@5 (a chunk containing the expected fact) | 82.0% |
| Hit@10 (a chunk containing the expected fact) | 86.0% |
| MRR (first fact-bearing chunk) | 0.6566 |

## Answers and validation

| Metric | Value |
|---|---|
| Pass rate (validated / in-corpus) | 86.0% |
| Mean confidence (in-corpus) | 0.8321 |
| Answer correct (expected facts present) | 72.0% |
| **Validated precision** (correct among validated) | 74.4% |
| **Validated but wrong** | 25.6% |
| Correct but flagged for review | 11.1% |
| Out-of-corpus sent to review | 62.5% |
| Out-of-corpus falsely validated | 37.5% |
| Decision accuracy (all queries) | 69.0% |

A high pass rate alone is not evidence of quality: an extractive answer is copied from the evidence, so coverage is near-perfect by construction. Validated precision and the validated-but-wrong rate are the meaningful numbers.

## Threshold sweep

| Threshold | Pass rate | Validated precision | Validated but wrong | Correct but flagged | OOC false accept | Decision accuracy |
|---|---|---|---|---|---|---|
| 0.3 | 100.0% | 72.0% | 28.0% | 0.0% | 100.0% | 62.1% |
| 0.35 | 100.0% | 72.0% | 28.0% | 0.0% | 100.0% | 62.1% |
| 0.4 | 98.0% | 73.5% | 26.5% | 0.0% | 87.5% | 65.5% |
| 0.45 | 98.0% | 73.5% | 26.5% | 0.0% | 87.5% | 65.5% |
| 0.5 | 96.0% | 75.0% | 25.0% | 0.0% | 62.5% | 70.7% |
| 0.55 | 94.0% | 74.5% | 25.5% | 2.8% | 37.5% | 72.4% |
| 0.6 | 86.0% | 74.4% | 25.6% | 11.1% | 37.5% | 69.0% |
| 0.65 | 82.0% | 75.6% | 24.4% | 13.9% | 0.0% | 74.1% |
| 0.7 | 78.0% | 79.5% | 20.5% | 13.9% | 0.0% | 77.6% |
| 0.75 | 78.0% | 79.5% | 20.5% | 13.9% | 0.0% | 77.6% |
| 0.8 | 70.0% | 80.0% | 20.0% | 22.2% | 0.0% | 74.1% |
| 0.85 | 52.0% | 76.9% | 23.1% | 44.4% | 0.0% | 62.1% |
| 0.9 | 46.0% | 73.9% | 26.1% | 52.8% | 0.0% | 56.9% |

## Items for analyst review (21)

- **R07** (correct answer withheld, confidence 0.571): What must a symptomatic visitor do if they are allowed to stay with a patient?
- **R09** (VALIDATED BUT WRONG, confidence 1.0): Where should patients needing droplet precautions be placed in an outpatient setting?
- **T03** (VALIDATED BUT WRONG, confidence 0.905): How often should temperature monitoring devices be calibration tested?
- **R28** (VALIDATED BUT WRONG, confidence 1.0): What are the five components of the WHO multimodal hand hygiene improvement strategy?
- **RO5** (VALIDATED BUT OUT OF CORPUS, confidence 0.609): What steam temperature and exposure time are needed to autoclave surgical instruments?
- **R36** (VALIDATED BUT WRONG, confidence 1.0): Should hot water be used for handwashing in health care?
- **RO7** (VALIDATED BUT OUT OF CORPUS, confidence 0.632): What is the recommended dosage of oseltamivir for influenza prophylaxis?
- **N03** (VALIDATED BUT WRONG, confidence 0.921): how accurate does the thermometer have to be
- **N04** (correct answer withheld, confidence 0.597): what should i set the fridge thermostat to
- **N05** (VALIDATED BUT WRONG, confidence 0.641): after changing the thermostat how long before i check the temperature again
- **N07** (flagged: low confidence, confidence 0.56): how long can mResvia be kept in the fridge
- **N11** (flagged: low confidence, confidence 0.391): how long does norovirus take to make you sick
- **N14** (correct answer withheld, confidence 0.568): how many days of antibiotics are given after environmental exposure
- **N15** (correct answer withheld, confidence 0.543): how many days should mumps patients be isolated
- **N17** (VALIDATED BUT WRONG, confidence 0.675): how long should i rub my hands with sanitiser
- **N18** (VALIDATED BUT WRONG, confidence 0.776): what are the benefits of hand-rub
- **N19** (flagged: low confidence, confidence 0.486): is it ok to wear fake nails around patients
- **N21** (VALIDATED BUT WRONG, confidence 0.663): what percentage alcohol is in the WHO handrub recipe
- **N23** (VALIDATED BUT WRONG, confidence 0.926): can disposable gloves be reused
- **N24** (VALIDATED BUT WRONG, confidence 0.813): what helps with dry cracked skin from hand washing
- **NO1** (VALIDATED BUT OUT OF CORPUS, confidence 0.612): what is the correct paracetamol dose for a child with fever
