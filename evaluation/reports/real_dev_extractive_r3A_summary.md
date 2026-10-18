# Evaluation summary: real corpus, dev split

- Index: `109f609db011848c…`  |  generator: `extractive`  |  threshold: 0.6
- Queries: 50 in-corpus, 8 out-of-corpus

## Retrieval (in-corpus queries)

| Metric | Value |
|---|---|
| Precision@1 (document level) | 86.0% |
| Precision@5 (document level) | 75.2% |
| Precision@10 (document level) | 68.6% |
| Capped Precision@1 (vs. best attainable) | 86.0% |
| Capped Precision@5 (vs. best attainable) | 75.2% |
| Capped Precision@10 (vs. best attainable) | 68.6% |
| Hit@1 (a chunk containing the expected fact) | 56.0% |
| Hit@5 (a chunk containing the expected fact) | 76.0% |
| Hit@10 (a chunk containing the expected fact) | 80.0% |
| MRR (first fact-bearing chunk) | 0.6422 |

## Answers and validation

| Metric | Value |
|---|---|
| Pass rate (validated / in-corpus) | 84.0% |
| Mean confidence (in-corpus) | 0.7977 |
| Answer correct (expected facts present) | 66.0% |
| **Validated precision** (correct among validated) | 69.0% |
| **Validated but wrong** | 30.9% |
| Correct but flagged for review | 12.1% |
| Out-of-corpus sent to review | 62.5% |
| Out-of-corpus falsely validated | 37.5% |
| Decision accuracy (all queries) | 65.5% |

A high pass rate alone is not evidence of quality: an extractive answer is copied from the evidence, so coverage is near-perfect by construction. Validated precision and the validated-but-wrong rate are the meaningful numbers.

## Threshold sweep

| Threshold | Pass rate | Validated precision | Validated but wrong | Correct but flagged | OOC false accept | Decision accuracy |
|---|---|---|---|---|---|---|
| 0.3 | 100.0% | 66.0% | 34.0% | 0.0% | 87.5% | 58.6% |
| 0.35 | 98.0% | 67.3% | 32.6% | 0.0% | 87.5% | 60.3% |
| 0.4 | 98.0% | 67.3% | 32.6% | 0.0% | 75.0% | 62.1% |
| 0.45 | 96.0% | 68.8% | 31.2% | 0.0% | 75.0% | 63.8% |
| 0.5 | 92.0% | 69.6% | 30.4% | 3.0% | 50.0% | 67.2% |
| 0.55 | 86.0% | 69.8% | 30.2% | 9.1% | 37.5% | 67.2% |
| 0.6 | 84.0% | 69.0% | 30.9% | 12.1% | 37.5% | 65.5% |
| 0.65 | 78.0% | 71.8% | 28.2% | 15.2% | 12.5% | 70.7% |
| 0.7 | 74.0% | 75.7% | 24.3% | 15.2% | 12.5% | 74.1% |
| 0.75 | 70.0% | 77.1% | 22.9% | 18.2% | 0.0% | 75.9% |
| 0.8 | 60.0% | 76.7% | 23.3% | 30.3% | 0.0% | 70.7% |
| 0.85 | 46.0% | 69.6% | 30.4% | 51.5% | 0.0% | 58.6% |
| 0.9 | 36.0% | 72.2% | 27.8% | 60.6% | 0.0% | 56.9% |

## Items for analyst review (24)

- **R07** (correct answer withheld, confidence 0.571): What must a symptomatic visitor do if they are allowed to stay with a patient?
- **R09** (VALIDATED BUT WRONG, confidence 0.728): Where should patients needing droplet precautions be placed in an outpatient setting?
- **T03** (VALIDATED BUT WRONG, confidence 0.905): How often should temperature monitoring devices be calibration tested?
- **R18** (VALIDATED BUT WRONG, confidence 0.659): How long should the entire alcohol handrub procedure take?
- **R22** (VALIDATED BUT WRONG, confidence 0.912): For which outbreak pathogens is washing with soap and water preferred over alcohol handrub?
- **R28** (VALIDATED BUT WRONG, confidence 1.0): What are the five components of the WHO multimodal hand hygiene improvement strategy?
- **RO5** (VALIDATED BUT OUT OF CORPUS, confidence 0.609): What steam temperature and exposure time are needed to autoclave surgical instruments?
- **R35** (correct answer withheld, confidence 0.5): Should soap and alcohol-based handrub be used concomitantly?
- **R36** (VALIDATED BUT WRONG, confidence 1.0): Should hot water be used for handwashing in health care?
- **RO7** (VALIDATED BUT OUT OF CORPUS, confidence 0.724): What is the recommended dosage of oseltamivir for influenza prophylaxis?
- **N03** (VALIDATED BUT WRONG, confidence 0.664): how accurate does the thermometer have to be
- **N04** (flagged: low confidence, confidence 0.525): what should i set the fridge thermostat to
- **N05** (VALIDATED BUT WRONG, confidence 0.641): after changing the thermostat how long before i check the temperature again
- **N07** (flagged: low confidence, confidence 0.429): how long can mResvia be kept in the fridge
- **N11** (flagged: low confidence, confidence 0.318): how long does norovirus take to make you sick
- **N14** (correct answer withheld, confidence 0.486): how many days of antibiotics are given after environmental exposure
- **N15** (correct answer withheld, confidence 0.543): how many days should mumps patients be isolated
- **N17** (VALIDATED BUT WRONG, confidence 0.634): how long should i rub my hands with sanitiser
- **N18** (VALIDATED BUT WRONG, confidence 0.894): what are the benefits of hand-rub
- **N19** (flagged: low confidence, confidence 0.484): is it ok to wear fake nails around patients
- **N21** (VALIDATED BUT WRONG, confidence 0.76): what percentage alcohol is in the WHO handrub recipe
- **N23** (VALIDATED BUT WRONG, confidence 0.926): can disposable gloves be reused
- **N24** (VALIDATED BUT WRONG, confidence 0.894): what helps with dry cracked skin from hand washing
- **NO1** (VALIDATED BUT OUT OF CORPUS, confidence 0.612): what is the correct paracetamol dose for a child with fever
