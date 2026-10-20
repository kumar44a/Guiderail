# Evaluation summary: real corpus, dev split

- Index: `9bc2368dd16cc348…`  |  generator: `extractive`  |  threshold: 0.6
- Queries: 65 in-corpus, 13 out-of-corpus

## Retrieval (in-corpus queries)

| Metric | Value |
|---|---|
| Precision@1 (document level) | 86.2% |
| Precision@5 (document level) | 85.2% |
| Precision@10 (document level) | 84.0% |
| Capped Precision@1 (vs. best attainable) | 86.2% |
| Capped Precision@5 (vs. best attainable) | 85.2% |
| Capped Precision@10 (vs. best attainable) | 84.0% |
| Hit@1 (a chunk containing the expected fact) | 49.2% |
| Hit@5 (a chunk containing the expected fact) | 76.9% |
| Hit@10 (a chunk containing the expected fact) | 80.0% |
| MRR (first fact-bearing chunk) | 0.5936 |

## Answers and validation

| Metric | Value |
|---|---|
| Pass rate (validated / in-corpus) | 83.1% |
| Mean confidence (in-corpus) | 0.8111 |
| Answer correct (expected facts present) | 63.1% |
| **Validated precision** (correct among validated) | 66.7% |
| **Validated but wrong** | 33.3% |
| Correct but flagged for review | 12.2% |
| Out-of-corpus sent to review | 61.5% |
| Out-of-corpus falsely validated | 38.5% |
| Decision accuracy (all queries) | 64.1% |

A high pass rate alone is not evidence of quality: an extractive answer is copied from the evidence, so coverage is near-perfect by construction. Validated precision and the validated-but-wrong rate are the meaningful numbers.

## Threshold sweep

| Threshold | Pass rate | Validated precision | Validated but wrong | Correct but flagged | OOC false accept | Decision accuracy |
|---|---|---|---|---|---|---|
| 0.3 | 100.0% | 63.1% | 36.9% | 0.0% | 92.3% | 53.8% |
| 0.35 | 100.0% | 63.1% | 36.9% | 0.0% | 92.3% | 53.8% |
| 0.4 | 98.5% | 64.1% | 35.9% | 0.0% | 84.6% | 56.4% |
| 0.45 | 96.9% | 65.1% | 34.9% | 0.0% | 84.6% | 57.7% |
| 0.5 | 92.3% | 65.0% | 35.0% | 4.9% | 69.2% | 59.0% |
| 0.55 | 90.8% | 64.4% | 35.6% | 7.3% | 46.2% | 61.5% |
| 0.6 | 83.1% | 66.7% | 33.3% | 12.2% | 38.5% | 64.1% |
| 0.65 | 76.9% | 68.0% | 32.0% | 17.1% | 15.4% | 68.0% |
| 0.7 | 73.9% | 70.8% | 29.2% | 17.1% | 7.7% | 71.8% |
| 0.75 | 72.3% | 72.3% | 27.7% | 17.1% | 7.7% | 73.1% |
| 0.8 | 66.1% | 72.1% | 27.9% | 24.4% | 0.0% | 71.8% |
| 0.85 | 50.8% | 69.7% | 30.3% | 43.9% | 0.0% | 64.1% |
| 0.9 | 38.5% | 68.0% | 32.0% | 58.5% | 0.0% | 59.0% |

## Items for analyst review (34)

- **R07** (correct answer withheld, confidence 0.513): What must a symptomatic visitor do if they are allowed to stay with a patient?
- **R09** (VALIDATED BUT WRONG, confidence 1.0): Where should patients needing droplet precautions be placed in an outpatient setting?
- **T03** (VALIDATED BUT WRONG, confidence 0.905): How often should temperature monitoring devices be calibration tested?
- **R28** (VALIDATED BUT WRONG, confidence 1.0): What are the five components of the WHO multimodal hand hygiene improvement strategy?
- **RO5** (VALIDATED BUT OUT OF CORPUS, confidence 0.609): What steam temperature and exposure time are needed to autoclave surgical instruments?
- **R36** (VALIDATED BUT WRONG, confidence 1.0): Should hot water be used for handwashing in health care?
- **RO7** (VALIDATED BUT OUT OF CORPUS, confidence 0.632): What is the recommended dosage of oseltamivir for influenza prophylaxis?
- **N03** (VALIDATED BUT WRONG, confidence 0.678): how accurate does the thermometer have to be
- **N04** (correct answer withheld, confidence 0.597): what should i set the fridge thermostat to
- **N05** (VALIDATED BUT WRONG, confidence 0.604): after changing the thermostat how long before i check the temperature again
- **N07** (flagged: low confidence, confidence 0.429): how long can mResvia be kept in the fridge
- **N11** (flagged: low confidence, confidence 0.391): how long does norovirus take to make you sick
- **N14** (correct answer withheld, confidence 0.568): how many days of antibiotics are given after environmental exposure
- **N15** (correct answer withheld, confidence 0.498): how many days should mumps patients be isolated
- **N17** (VALIDATED BUT WRONG, confidence 0.675): how long should i rub my hands with sanitiser
- **N18** (VALIDATED BUT WRONG, confidence 0.776): what are the benefits of hand-rub
- **N19** (flagged: low confidence, confidence 0.486): is it ok to wear fake nails around patients
- **N21** (flagged: low confidence, confidence 0.585): what percentage alcohol is in the WHO handrub recipe
- **N23** (VALIDATED BUT WRONG, confidence 0.926): can disposable gloves be reused
- **N24** (VALIDATED BUT WRONG, confidence 0.813): what helps with dry cracked skin from hand washing
- **N25** (VALIDATED BUT WRONG, confidence 0.873): what languages are the world hand hygiene day posters in
- **NO1** (VALIDATED BUT OUT OF CORPUS, confidence 0.612): what is the correct paracetamol dose for a child with fever
- **M01** (correct answer withheld, confidence 0.46): how should hand rub come out of a wall dispenser so staff dont touch it
- **M03** (flagged: low confidence, confidence 0.569): are elbow operated taps proven to work
- **M04** (VALIDATED BUT WRONG, confidence 0.833): is stronger alcohol better for hand rub
- **M05** (VALIDATED BUT WRONG, confidence 1.0): which cleans hands better, hand rub or soap
- **M06** (VALIDATED BUT WRONG, confidence 0.732): what happens to skin when hands are cleaned very often
- **M07** (VALIDATED BUT WRONG, confidence 1.0): what to do when there is no running water for hand washing
- **M09** (VALIDATED BUT WRONG, confidence 1.0): when should gloves be worn
- **M15** (flagged: low confidence, confidence 0.564): what kind of room should the vaccine fridge sit in
- **M21** (VALIDATED BUT WRONG, confidence 0.872): can hand cleaning products cause serious allergic reactions
- **M22** (VALIDATED BUT WRONG, confidence 0.602): what help should staff get for skin problems on their hands
- **MO1** (VALIDATED BUT OUT OF CORPUS, confidence 0.777): does hand rub expire
- **MO3** (VALIDATED BUT OUT OF CORPUS, confidence 0.674): what is the recommended shelf life of an opened bottle of surgical scrub
