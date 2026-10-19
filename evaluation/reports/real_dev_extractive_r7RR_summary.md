# Evaluation summary: real corpus, dev split

- Index: `44609f8e43e22326…`  |  generator: `extractive`  |  threshold: 0.6
- Queries: 65 in-corpus, 13 out-of-corpus

## Retrieval (in-corpus queries)

| Metric | Value |
|---|---|
| Precision@1 (document level) | 86.2% |
| Precision@5 (document level) | 80.0% |
| Precision@10 (document level) | 74.2% |
| Capped Precision@1 (vs. best attainable) | 86.2% |
| Capped Precision@5 (vs. best attainable) | 80.0% |
| Capped Precision@10 (vs. best attainable) | 74.2% |
| Hit@1 (a chunk containing the expected fact) | 50.8% |
| Hit@5 (a chunk containing the expected fact) | 76.9% |
| Hit@10 (a chunk containing the expected fact) | 80.0% |
| MRR (first fact-bearing chunk) | 0.6063 |

## Answers and validation

| Metric | Value |
|---|---|
| Pass rate (validated / in-corpus) | 84.6% |
| Mean confidence (in-corpus) | 0.8189 |
| Answer correct (expected facts present) | 63.1% |
| **Validated precision** (correct among validated) | 65.5% |
| **Validated but wrong** | 34.5% |
| Correct but flagged for review | 12.2% |
| Out-of-corpus sent to review | 46.2% |
| Out-of-corpus falsely validated | 53.8% |
| Decision accuracy (all queries) | 60.3% |

A high pass rate alone is not evidence of quality: an extractive answer is copied from the evidence, so coverage is near-perfect by construction. Validated precision and the validated-but-wrong rate are the meaningful numbers.

## Threshold sweep

| Threshold | Pass rate | Validated precision | Validated but wrong | Correct but flagged | OOC false accept | Decision accuracy |
|---|---|---|---|---|---|---|
| 0.3 | 100.0% | 63.1% | 36.9% | 0.0% | 84.6% | 55.1% |
| 0.35 | 100.0% | 63.1% | 36.9% | 0.0% | 84.6% | 55.1% |
| 0.4 | 98.5% | 64.1% | 35.9% | 0.0% | 84.6% | 56.4% |
| 0.45 | 98.5% | 64.1% | 35.9% | 0.0% | 76.9% | 57.7% |
| 0.5 | 95.4% | 64.5% | 35.5% | 2.4% | 69.2% | 59.0% |
| 0.55 | 93.8% | 63.9% | 36.1% | 4.9% | 53.8% | 60.3% |
| 0.6 | 84.6% | 65.5% | 34.5% | 12.2% | 53.8% | 60.3% |
| 0.65 | 78.5% | 66.7% | 33.3% | 17.1% | 15.4% | 66.7% |
| 0.7 | 73.9% | 70.8% | 29.2% | 17.1% | 7.7% | 71.8% |
| 0.75 | 70.8% | 73.9% | 26.1% | 17.1% | 7.7% | 74.4% |
| 0.8 | 61.5% | 72.5% | 27.5% | 29.3% | 0.0% | 70.5% |
| 0.85 | 52.3% | 70.6% | 29.4% | 41.5% | 0.0% | 65.4% |
| 0.9 | 41.5% | 66.7% | 33.3% | 56.1% | 0.0% | 59.0% |

## Items for analyst review (36)

- **R07** (correct answer withheld, confidence 0.57): What must a symptomatic visitor do if they are allowed to stay with a patient?
- **R09** (VALIDATED BUT WRONG, confidence 1.0): Where should patients needing droplet precautions be placed in an outpatient setting?
- **T03** (VALIDATED BUT WRONG, confidence 0.906): How often should temperature monitoring devices be calibration tested?
- **R28** (VALIDATED BUT WRONG, confidence 1.0): What are the five components of the WHO multimodal hand hygiene improvement strategy?
- **RO5** (VALIDATED BUT OUT OF CORPUS, confidence 0.605): What steam temperature and exposure time are needed to autoclave surgical instruments?
- **R36** (VALIDATED BUT WRONG, confidence 1.0): Should hot water be used for handwashing in health care?
- **RO7** (VALIDATED BUT OUT OF CORPUS, confidence 0.631): What is the recommended dosage of oseltamivir for influenza prophylaxis?
- **N03** (VALIDATED BUT WRONG, confidence 0.921): how accurate does the thermometer have to be
- **N04** (correct answer withheld, confidence 0.597): what should i set the fridge thermostat to
- **N05** (VALIDATED BUT WRONG, confidence 0.638): after changing the thermostat how long before i check the temperature again
- **N07** (flagged: low confidence, confidence 0.564): how long can mResvia be kept in the fridge
- **N11** (flagged: low confidence, confidence 0.398): how long does norovirus take to make you sick
- **N14** (correct answer withheld, confidence 0.574): how many days of antibiotics are given after environmental exposure
- **N15** (correct answer withheld, confidence 0.495): how many days should mumps patients be isolated
- **N17** (VALIDATED BUT WRONG, confidence 0.681): how long should i rub my hands with sanitiser
- **N18** (VALIDATED BUT WRONG, confidence 0.781): what are the benefits of hand-rub
- **N19** (flagged: low confidence, confidence 0.489): is it ok to wear fake nails around patients
- **N21** (VALIDATED BUT WRONG, confidence 0.665): what percentage alcohol is in the WHO handrub recipe
- **N23** (VALIDATED BUT WRONG, confidence 0.926): can disposable gloves be reused
- **N24** (VALIDATED BUT WRONG, confidence 0.818): what helps with dry cracked skin from hand washing
- **NO1** (VALIDATED BUT OUT OF CORPUS, confidence 0.601): what is the correct paracetamol dose for a child with fever
- **M01** (correct answer withheld, confidence 0.514): how should hand rub come out of a wall dispenser so staff dont touch it
- **M03** (flagged: low confidence, confidence 0.567): are elbow operated taps proven to work
- **M04** (VALIDATED BUT WRONG, confidence 0.724): is stronger alcohol better for hand rub
- **M05** (VALIDATED BUT WRONG, confidence 1.0): which cleans hands better, hand rub or soap
- **M06** (VALIDATED BUT WRONG, confidence 0.738): what happens to skin when hands are cleaned very often
- **M07** (VALIDATED BUT WRONG, confidence 1.0): what to do when there is no running water for hand washing
- **M09** (VALIDATED BUT WRONG, confidence 1.0): when should gloves be worn
- **M15** (flagged: low confidence, confidence 0.562): what kind of room should the vaccine fridge sit in
- **M21** (VALIDATED BUT WRONG, confidence 0.873): can hand cleaning products cause serious allergic reactions
- **M22** (VALIDATED BUT WRONG, confidence 0.605): what help should staff get for skin problems on their hands
- **M24** (VALIDATED BUT WRONG, confidence 0.685): is hand rub a fire hazard
- **MO1** (VALIDATED BUT OUT OF CORPUS, confidence 0.792): does hand rub expire
- **MO2** (VALIDATED BUT OUT OF CORPUS, confidence 0.603): which hand rub brand is best for children
- **MO3** (VALIDATED BUT OUT OF CORPUS, confidence 0.683): what is the recommended shelf life of an opened bottle of surgical scrub
- **MO4** (VALIDATED BUT OUT OF CORPUS, confidence 0.633): what is the speed limit on highways
