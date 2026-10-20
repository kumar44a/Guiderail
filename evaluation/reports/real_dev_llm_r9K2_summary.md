# Evaluation summary: real corpus, dev split

- Index: `9bc2368dd16cc348…`  |  generator: `llm`  |  threshold: 0.6
- Queries: 65 in-corpus, 13 out-of-corpus

## Retrieval (in-corpus queries)

| Metric | Value |
|---|---|
| Precision@1 (document level) | 90.8% |
| Precision@5 (document level) | 88.6% |
| Precision@10 (document level) | 86.8% |
| Capped Precision@1 (vs. best attainable) | 90.8% |
| Capped Precision@5 (vs. best attainable) | 88.6% |
| Capped Precision@10 (vs. best attainable) | 86.8% |
| Hit@1 (a chunk containing the expected fact) | 52.3% |
| Hit@5 (a chunk containing the expected fact) | 73.9% |
| Hit@10 (a chunk containing the expected fact) | 80.0% |
| MRR (first fact-bearing chunk) | 0.6205 |

## Answers and validation

| Metric | Value |
|---|---|
| Pass rate (validated / in-corpus) | 70.8% |
| Mean confidence (in-corpus) | 0.6674 |
| Answer correct (expected facts present) | 72.3% |
| **Validated precision** (correct among validated) | 84.8% |
| **Validated but wrong** | 15.2% |
| Correct but flagged for review | 17.0% |
| Out-of-corpus sent to review | 100.0% |
| Out-of-corpus falsely validated | 0.0% |
| Decision accuracy (all queries) | 80.8% |

A high pass rate alone is not evidence of quality: an extractive answer is copied from the evidence, so coverage is near-perfect by construction. Validated precision and the validated-but-wrong rate are the meaningful numbers.

## Threshold sweep

| Threshold | Pass rate | Validated precision | Validated but wrong | Correct but flagged | OOC false accept | Decision accuracy |
|---|---|---|---|---|---|---|
| 0.3 | 83.1% | 87.0% | 13.0% | 0.0% | 0.0% | 91.0% |
| 0.35 | 83.1% | 87.0% | 13.0% | 0.0% | 0.0% | 91.0% |
| 0.4 | 83.1% | 87.0% | 13.0% | 0.0% | 0.0% | 91.0% |
| 0.45 | 81.5% | 86.8% | 13.2% | 2.1% | 0.0% | 89.7% |
| 0.5 | 76.9% | 86.0% | 14.0% | 8.5% | 0.0% | 85.9% |
| 0.55 | 75.4% | 85.7% | 14.3% | 10.6% | 0.0% | 84.6% |
| 0.6 | 70.8% | 84.8% | 15.2% | 17.0% | 0.0% | 80.8% |
| 0.65 | 64.6% | 85.7% | 14.3% | 23.4% | 0.0% | 78.2% |
| 0.7 | 63.1% | 87.8% | 12.2% | 23.4% | 0.0% | 79.5% |
| 0.75 | 53.8% | 85.7% | 14.3% | 36.2% | 0.0% | 71.8% |
| 0.8 | 44.6% | 82.8% | 17.2% | 48.9% | 0.0% | 64.1% |
| 0.85 | 41.5% | 81.5% | 18.5% | 53.2% | 0.0% | 61.5% |
| 0.9 | 30.8% | 80.0% | 20.0% | 66.0% | 0.0% | 55.1% |

## Items for analyst review (26)

- **R07** (correct answer withheld, confidence 0.556): What must a symptomatic visitor do if they are allowed to stay with a patient?
- **R09** (flagged: low confidence, confidence 0.0): Where should patients needing droplet precautions be placed in an outpatient setting?
- **R28** (flagged: low confidence, confidence 0.0): What are the five components of the WHO multimodal hand hygiene improvement strategy?
- **R36** (VALIDATED BUT WRONG, confidence 1.0): Should hot water be used for handwashing in health care?
- **N01** (correct answer withheld, confidence 0.562): how long does a new fridge take to settle on the right temperature
- **N03** (VALIDATED BUT WRONG, confidence 0.651): how accurate does the thermometer have to be
- **N04** (correct answer withheld, confidence 0.459): what should i set the fridge thermostat to
- **N05** (flagged: low confidence, confidence 0.0): after changing the thermostat how long before i check the temperature again
- **N07** (correct answer withheld, confidence 0.49): how long can mResvia be kept in the fridge
- **N11** (flagged: low confidence, confidence 0.0): how long does norovirus take to make you sick
- **N14** (correct answer withheld, confidence 0.568): how many days of antibiotics are given after environmental exposure
- **N15** (correct answer withheld, confidence 0.543): how many days should mumps patients be isolated
- **N17** (flagged: low confidence, confidence 0.0): how long should i rub my hands with sanitiser
- **N19** (correct answer withheld, confidence 0.435): is it ok to wear fake nails around patients
- **N21** (flagged: low confidence, confidence 0.0): what percentage alcohol is in the WHO handrub recipe
- **N23** (VALIDATED BUT WRONG, confidence 0.893): can disposable gloves be reused
- **N24** (VALIDATED BUT WRONG, confidence 0.906): what helps with dry cracked skin from hand washing
- **M01** (flagged: low confidence, confidence 0.0): how should hand rub come out of a wall dispenser so staff dont touch it
- **M02** (flagged: low confidence, confidence 0.0): why carry a pocket bottle of hand rub
- **M04** (flagged: low confidence, confidence 0.0): is stronger alcohol better for hand rub
- **M07** (VALIDATED BUT WRONG, confidence 1.0): what to do when there is no running water for hand washing
- **M09** (VALIDATED BUT WRONG, confidence 1.0): when should gloves be worn
- **M15** (flagged: low confidence, confidence 0.0): what kind of room should the vaccine fridge sit in
- **M16** (correct answer withheld, confidence 0.494): how far from the ceiling should a vaccine fridge be
- **M22** (VALIDATED BUT WRONG, confidence 0.602): what help should staff get for skin problems on their hands
- **M24** (flagged: low confidence, confidence 0.0): is hand rub a fire hazard
