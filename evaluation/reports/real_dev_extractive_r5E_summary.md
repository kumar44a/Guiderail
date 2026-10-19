# Evaluation summary: real corpus, dev split

- Index: `9bc2368dd16cc348…`  |  generator: `extractive`  |  threshold: 0.6
- Queries: 50 in-corpus, 8 out-of-corpus

## Retrieval (in-corpus queries)

| Metric | Value |
|---|---|
| Precision@1 (document level) | 90.0% |
| Precision@5 (document level) | 81.6% |
| Precision@10 (document level) | 77.8% |
| Capped Precision@1 (vs. best attainable) | 90.0% |
| Capped Precision@5 (vs. best attainable) | 81.6% |
| Capped Precision@10 (vs. best attainable) | 77.8% |
| Hit@1 (a chunk containing the expected fact) | 60.0% |
| Hit@5 (a chunk containing the expected fact) | 82.0% |
| Hit@10 (a chunk containing the expected fact) | 88.0% |
| MRR (first fact-bearing chunk) | 0.6897 |

## Answers and validation

| Metric | Value |
|---|---|
| Pass rate (validated / in-corpus) | 86.0% |
| Mean confidence (in-corpus) | 0.8053 |
| Answer correct (expected facts present) | 74.0% |
| **Validated precision** (correct among validated) | 74.4% |
| **Validated but wrong** | 25.6% |
| Correct but flagged for review | 13.5% |
| Out-of-corpus sent to review | 62.5% |
| Out-of-corpus falsely validated | 37.5% |
| Decision accuracy (all queries) | 67.2% |

A high pass rate alone is not evidence of quality: an extractive answer is copied from the evidence, so coverage is near-perfect by construction. Validated precision and the validated-but-wrong rate are the meaningful numbers.

## Threshold sweep

| Threshold | Pass rate | Validated precision | Validated but wrong | Correct but flagged | OOC false accept | Decision accuracy |
|---|---|---|---|---|---|---|
| 0.3 | 98.0% | 75.5% | 24.5% | 0.0% | 87.5% | 67.2% |
| 0.35 | 98.0% | 75.5% | 24.5% | 0.0% | 87.5% | 67.2% |
| 0.4 | 98.0% | 75.5% | 24.5% | 0.0% | 87.5% | 67.2% |
| 0.45 | 96.0% | 75.0% | 25.0% | 2.7% | 75.0% | 67.2% |
| 0.5 | 92.0% | 73.9% | 26.1% | 8.1% | 50.0% | 67.2% |
| 0.55 | 90.0% | 73.3% | 26.7% | 10.8% | 37.5% | 67.2% |
| 0.6 | 86.0% | 74.4% | 25.6% | 13.5% | 37.5% | 67.2% |
| 0.65 | 82.0% | 73.2% | 26.8% | 18.9% | 0.0% | 69.0% |
| 0.7 | 74.0% | 78.4% | 21.6% | 21.6% | 0.0% | 72.4% |
| 0.75 | 72.0% | 77.8% | 22.2% | 24.3% | 0.0% | 70.7% |
| 0.8 | 62.0% | 77.4% | 22.6% | 35.1% | 0.0% | 65.5% |
| 0.85 | 46.0% | 73.9% | 26.1% | 54.0% | 0.0% | 55.2% |
| 0.9 | 40.0% | 70.0% | 30.0% | 62.2% | 0.0% | 50.0% |

## Items for analyst review (21)

- **R07** (correct answer withheld, confidence 0.571): What must a symptomatic visitor do if they are allowed to stay with a patient?
- **R09** (VALIDATED BUT WRONG, confidence 1.0): Where should patients needing droplet precautions be placed in an outpatient setting?
- **T03** (VALIDATED BUT WRONG, confidence 0.905): How often should temperature monitoring devices be calibration tested?
- **R28** (VALIDATED BUT WRONG, confidence 0.92): What are the five components of the WHO multimodal hand hygiene improvement strategy?
- **RO5** (VALIDATED BUT OUT OF CORPUS, confidence 0.609): What steam temperature and exposure time are needed to autoclave surgical instruments?
- **R35** (correct answer withheld, confidence 0.5): Should soap and alcohol-based handrub be used concomitantly?
- **R36** (VALIDATED BUT WRONG, confidence 1.0): Should hot water be used for handwashing in health care?
- **RO7** (VALIDATED BUT OUT OF CORPUS, confidence 0.632): What is the recommended dosage of oseltamivir for influenza prophylaxis?
- **N03** (VALIDATED BUT WRONG, confidence 0.664): how accurate does the thermometer have to be
- **N04** (correct answer withheld, confidence 0.498): what should i set the fridge thermostat to
- **N05** (flagged: low confidence, confidence 0.589): after changing the thermostat how long before i check the temperature again
- **N11** (flagged: low confidence, confidence 0.189): how long does norovirus take to make you sick
- **N14** (correct answer withheld, confidence 0.486): how many days of antibiotics are given after environmental exposure
- **N17** (VALIDATED BUT WRONG, confidence 0.675): how long should i rub my hands with sanitiser
- **N18** (VALIDATED BUT WRONG, confidence 0.776): what are the benefits of hand-rub
- **N19** (correct answer withheld, confidence 0.439): is it ok to wear fake nails around patients
- **N20** (VALIDATED BUT WRONG, confidence 0.81): how many sinks are needed per patient bed
- **N21** (VALIDATED BUT WRONG, confidence 0.663): what percentage alcohol is in the WHO handrub recipe
- **N23** (VALIDATED BUT WRONG, confidence 0.926): can disposable gloves be reused
- **N24** (VALIDATED BUT WRONG, confidence 0.906): what helps with dry cracked skin from hand washing
- **NO1** (VALIDATED BUT OUT OF CORPUS, confidence 0.612): what is the correct paracetamol dose for a child with fever
