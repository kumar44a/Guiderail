# Evaluation summary: real corpus, dev split

- Index: `283415669892d5a9…`  |  generator: `extractive`  |  threshold: 0.6
- Queries: 50 in-corpus, 8 out-of-corpus

## Retrieval (in-corpus queries)

| Metric | Value |
|---|---|
| Precision@1 (document level) | 86.0% |
| Precision@5 (document level) | 81.6% |
| Precision@10 (document level) | 76.0% |
| Capped Precision@1 (vs. best attainable) | 86.0% |
| Capped Precision@5 (vs. best attainable) | 81.6% |
| Capped Precision@10 (vs. best attainable) | 76.0% |
| Hit@1 (a chunk containing the expected fact) | 50.0% |
| Hit@5 (a chunk containing the expected fact) | 78.0% |
| Hit@10 (a chunk containing the expected fact) | 84.0% |
| MRR (first fact-bearing chunk) | 0.6091 |

## Answers and validation

| Metric | Value |
|---|---|
| Pass rate (validated / in-corpus) | 84.0% |
| Mean confidence (in-corpus) | 0.8121 |
| Answer correct (expected facts present) | 68.0% |
| **Validated precision** (correct among validated) | 69.0% |
| **Validated but wrong** | 30.9% |
| Correct but flagged for review | 14.7% |
| Out-of-corpus sent to review | 62.5% |
| Out-of-corpus falsely validated | 37.5% |
| Decision accuracy (all queries) | 63.8% |

A high pass rate alone is not evidence of quality: an extractive answer is copied from the evidence, so coverage is near-perfect by construction. Validated precision and the validated-but-wrong rate are the meaningful numbers.

## Threshold sweep

| Threshold | Pass rate | Validated precision | Validated but wrong | Correct but flagged | OOC false accept | Decision accuracy |
|---|---|---|---|---|---|---|
| 0.3 | 100.0% | 68.0% | 32.0% | 0.0% | 100.0% | 58.6% |
| 0.35 | 100.0% | 68.0% | 32.0% | 0.0% | 100.0% | 58.6% |
| 0.4 | 98.0% | 69.4% | 30.6% | 0.0% | 87.5% | 62.1% |
| 0.45 | 98.0% | 69.4% | 30.6% | 0.0% | 75.0% | 63.8% |
| 0.5 | 92.0% | 69.6% | 30.4% | 5.9% | 62.5% | 63.8% |
| 0.55 | 88.0% | 70.5% | 29.5% | 8.8% | 37.5% | 67.2% |
| 0.6 | 84.0% | 69.0% | 30.9% | 14.7% | 37.5% | 63.8% |
| 0.65 | 80.0% | 70.0% | 30.0% | 17.6% | 0.0% | 69.0% |
| 0.7 | 80.0% | 70.0% | 30.0% | 17.6% | 0.0% | 69.0% |
| 0.75 | 76.0% | 71.0% | 28.9% | 20.6% | 0.0% | 69.0% |
| 0.8 | 66.0% | 69.7% | 30.3% | 32.4% | 0.0% | 63.8% |
| 0.85 | 50.0% | 68.0% | 32.0% | 50.0% | 0.0% | 56.9% |
| 0.9 | 34.0% | 76.5% | 23.5% | 61.8% | 0.0% | 56.9% |

## Items for analyst review (24)

- **R07** (correct answer withheld, confidence 0.571): What must a symptomatic visitor do if they are allowed to stay with a patient?
- **R09** (VALIDATED BUT WRONG, confidence 1.0): Where should patients needing droplet precautions be placed in an outpatient setting?
- **T03** (VALIDATED BUT WRONG, confidence 0.905): How often should temperature monitoring devices be calibration tested?
- **R18** (VALIDATED BUT WRONG, confidence 0.764): How long should the entire alcohol handrub procedure take?
- **R28** (VALIDATED BUT WRONG, confidence 1.0): What are the five components of the WHO multimodal hand hygiene improvement strategy?
- **RO5** (VALIDATED BUT OUT OF CORPUS, confidence 0.609): What steam temperature and exposure time are needed to autoclave surgical instruments?
- **R35** (correct answer withheld, confidence 0.5): Should soap and alcohol-based handrub be used concomitantly?
- **R36** (VALIDATED BUT WRONG, confidence 1.0): Should hot water be used for handwashing in health care?
- **RO7** (VALIDATED BUT OUT OF CORPUS, confidence 0.632): What is the recommended dosage of oseltamivir for influenza prophylaxis?
- **N03** (VALIDATED BUT WRONG, confidence 0.873): how accurate does the thermometer have to be
- **N04** (correct answer withheld, confidence 0.586): what should i set the fridge thermostat to
- **N05** (VALIDATED BUT WRONG, confidence 0.604): after changing the thermostat how long before i check the temperature again
- **N07** (flagged: low confidence, confidence 0.545): how long can mResvia be kept in the fridge
- **N11** (flagged: low confidence, confidence 0.381): how long does norovirus take to make you sick
- **N14** (correct answer withheld, confidence 0.484): how many days of antibiotics are given after environmental exposure
- **N15** (correct answer withheld, confidence 0.498): how many days should mumps patients be isolated
- **N17** (VALIDATED BUT WRONG, confidence 0.85): how long should i rub my hands with sanitiser
- **N18** (VALIDATED BUT WRONG, confidence 0.816): what are the benefits of hand-rub
- **N19** (flagged: low confidence, confidence 0.477): is it ok to wear fake nails around patients
- **N21** (VALIDATED BUT WRONG, confidence 0.735): what percentage alcohol is in the WHO handrub recipe
- **N23** (VALIDATED BUT WRONG, confidence 0.896): can disposable gloves be reused
- **N24** (VALIDATED BUT WRONG, confidence 0.805): what helps with dry cracked skin from hand washing
- **N25** (VALIDATED BUT WRONG, confidence 0.873): what languages are the world hand hygiene day posters in
- **NO1** (VALIDATED BUT OUT OF CORPUS, confidence 0.612): what is the correct paracetamol dose for a child with fever
