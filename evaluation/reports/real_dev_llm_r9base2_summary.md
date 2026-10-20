# Evaluation summary: real corpus, dev split

- Index: `9bc2368dd16cc348…`  |  generator: `llm`  |  threshold: 0.6
- Queries: 65 in-corpus, 13 out-of-corpus

## Retrieval (in-corpus queries)

| Metric | Value |
|---|---|
| Precision@1 (document level) | 86.2% |
| Precision@5 (document level) | 83.7% |
| Precision@10 (document level) | 82.8% |
| Capped Precision@1 (vs. best attainable) | 86.2% |
| Capped Precision@5 (vs. best attainable) | 83.7% |
| Capped Precision@10 (vs. best attainable) | 82.8% |
| Hit@1 (a chunk containing the expected fact) | 49.2% |
| Hit@5 (a chunk containing the expected fact) | 76.9% |
| Hit@10 (a chunk containing the expected fact) | 80.0% |
| MRR (first fact-bearing chunk) | 0.5947 |

## Answers and validation

| Metric | Value |
|---|---|
| Pass rate (validated / in-corpus) | 69.2% |
| Mean confidence (in-corpus) | 0.6589 |
| Answer correct (expected facts present) | 73.9% |
| **Validated precision** (correct among validated) | 86.7% |
| **Validated but wrong** | 13.3% |
| Correct but flagged for review | 18.8% |
| Out-of-corpus sent to review | 100.0% |
| Out-of-corpus falsely validated | 0.0% |
| Decision accuracy (all queries) | 80.8% |

A high pass rate alone is not evidence of quality: an extractive answer is copied from the evidence, so coverage is near-perfect by construction. Validated precision and the validated-but-wrong rate are the meaningful numbers.

## Threshold sweep

| Threshold | Pass rate | Validated precision | Validated but wrong | Correct but flagged | OOC false accept | Decision accuracy |
|---|---|---|---|---|---|---|
| 0.3 | 83.1% | 88.9% | 11.1% | 0.0% | 0.0% | 92.3% |
| 0.35 | 83.1% | 88.9% | 11.1% | 0.0% | 0.0% | 92.3% |
| 0.4 | 80.0% | 88.5% | 11.5% | 4.2% | 0.0% | 89.7% |
| 0.45 | 80.0% | 88.5% | 11.5% | 4.2% | 0.0% | 89.7% |
| 0.5 | 80.0% | 88.5% | 11.5% | 4.2% | 0.0% | 89.7% |
| 0.55 | 76.9% | 88.0% | 12.0% | 8.3% | 0.0% | 87.2% |
| 0.6 | 69.2% | 86.7% | 13.3% | 18.8% | 0.0% | 80.8% |
| 0.65 | 58.5% | 89.5% | 10.5% | 29.2% | 0.0% | 76.9% |
| 0.7 | 58.5% | 89.5% | 10.5% | 29.2% | 0.0% | 76.9% |
| 0.75 | 56.9% | 89.2% | 10.8% | 31.2% | 0.0% | 75.6% |
| 0.8 | 47.7% | 90.3% | 9.7% | 41.7% | 0.0% | 70.5% |
| 0.85 | 41.5% | 88.9% | 11.1% | 50.0% | 0.0% | 65.4% |
| 0.9 | 30.8% | 90.0% | 10.0% | 62.5% | 0.0% | 59.0% |

## Items for analyst review (26)

- **R07** (correct answer withheld, confidence 0.556): What must a symptomatic visitor do if they are allowed to stay with a patient?
- **R09** (flagged: low confidence, confidence 0.0): Where should patients needing droplet precautions be placed in an outpatient setting?
- **R28** (flagged: low confidence, confidence 0.0): What are the five components of the WHO multimodal hand hygiene improvement strategy?
- **N01** (correct answer withheld, confidence 0.562): how long does a new fridge take to settle on the right temperature
- **N03** (flagged: low confidence, confidence 0.0): how accurate does the thermometer have to be
- **N04** (correct answer withheld, confidence 0.577): what should i set the fridge thermostat to
- **N05** (flagged: low confidence, confidence 0.0): after changing the thermostat how long before i check the temperature again
- **N07** (flagged: low confidence, confidence 0.0): how long can mResvia be kept in the fridge
- **N11** (flagged: low confidence, confidence 0.0): how long does norovirus take to make you sick
- **N14** (correct answer withheld, confidence 0.568): how many days of antibiotics are given after environmental exposure
- **N15** (correct answer withheld, confidence 0.586): how many days should mumps patients be isolated
- **N17** (VALIDATED BUT WRONG, confidence 0.62): how long should i rub my hands with sanitiser
- **N18** (flagged: low confidence, confidence 0.0): what are the benefits of hand-rub
- **N19** (correct answer withheld, confidence 0.388): is it ok to wear fake nails around patients
- **N21** (flagged: low confidence, confidence 0.0): what percentage alcohol is in the WHO handrub recipe
- **N23** (VALIDATED BUT WRONG, confidence 0.851): can disposable gloves be reused
- **N24** (VALIDATED BUT WRONG, confidence 0.778): what helps with dry cracked skin from hand washing
- **M01** (correct answer withheld, confidence 0.398): how should hand rub come out of a wall dispenser so staff dont touch it
- **M03** (correct answer withheld, confidence 0.547): are elbow operated taps proven to work
- **M04** (flagged: low confidence, confidence 0.0): is stronger alcohol better for hand rub
- **M07** (VALIDATED BUT WRONG, confidence 0.973): what to do when there is no running water for hand washing
- **M09** (VALIDATED BUT WRONG, confidence 1.0): when should gloves be worn
- **M15** (flagged: low confidence, confidence 0.0): what kind of room should the vaccine fridge sit in
- **M16** (correct answer withheld, confidence 0.526): how far from the ceiling should a vaccine fridge be
- **M22** (VALIDATED BUT WRONG, confidence 0.602): what help should staff get for skin problems on their hands
- **M24** (flagged: low confidence, confidence 0.0): is hand rub a fire hazard
