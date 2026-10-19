# Evaluation summary: real corpus, dev split

- Index: `06008416638099de…`  |  generator: `extractive`  |  threshold: 0.6
- Queries: 50 in-corpus, 8 out-of-corpus

## Retrieval (in-corpus queries)

| Metric | Value |
|---|---|
| Precision@1 (document level) | 84.0% |
| Precision@5 (document level) | 78.8% |
| Precision@10 (document level) | 75.2% |
| Capped Precision@1 (vs. best attainable) | 84.0% |
| Capped Precision@5 (vs. best attainable) | 78.8% |
| Capped Precision@10 (vs. best attainable) | 75.2% |
| Hit@1 (a chunk containing the expected fact) | 58.0% |
| Hit@5 (a chunk containing the expected fact) | 80.0% |
| Hit@10 (a chunk containing the expected fact) | 86.0% |
| MRR (first fact-bearing chunk) | 0.6655 |

## Answers and validation

| Metric | Value |
|---|---|
| Pass rate (validated / in-corpus) | 86.0% |
| Mean confidence (in-corpus) | 0.8046 |
| Answer correct (expected facts present) | 70.0% |
| **Validated precision** (correct among validated) | 76.7% |
| **Validated but wrong** | 23.3% |
| Correct but flagged for review | 5.7% |
| Out-of-corpus sent to review | 50.0% |
| Out-of-corpus falsely validated | 50.0% |
| Decision accuracy (all queries) | 72.4% |

A high pass rate alone is not evidence of quality: an extractive answer is copied from the evidence, so coverage is near-perfect by construction. Validated precision and the validated-but-wrong rate are the meaningful numbers.

## Threshold sweep

| Threshold | Pass rate | Validated precision | Validated but wrong | Correct but flagged | OOC false accept | Decision accuracy |
|---|---|---|---|---|---|---|
| 0.3 | 100.0% | 70.0% | 30.0% | 0.0% | 100.0% | 60.3% |
| 0.35 | 100.0% | 70.0% | 30.0% | 0.0% | 100.0% | 60.3% |
| 0.4 | 100.0% | 70.0% | 30.0% | 0.0% | 87.5% | 62.1% |
| 0.45 | 92.0% | 73.9% | 26.1% | 2.9% | 87.5% | 65.5% |
| 0.5 | 88.0% | 75.0% | 25.0% | 5.7% | 87.5% | 65.5% |
| 0.55 | 88.0% | 75.0% | 25.0% | 5.7% | 62.5% | 69.0% |
| 0.6 | 86.0% | 76.7% | 23.3% | 5.7% | 50.0% | 72.4% |
| 0.65 | 78.0% | 76.9% | 23.1% | 14.3% | 12.5% | 74.1% |
| 0.7 | 72.0% | 77.8% | 22.2% | 20.0% | 0.0% | 74.1% |
| 0.75 | 68.0% | 82.3% | 17.6% | 20.0% | 0.0% | 77.6% |
| 0.8 | 60.0% | 83.3% | 16.7% | 28.6% | 0.0% | 74.1% |
| 0.85 | 50.0% | 84.0% | 16.0% | 40.0% | 0.0% | 69.0% |
| 0.9 | 40.0% | 80.0% | 20.0% | 54.3% | 0.0% | 60.3% |

## Items for analyst review (21)

- **R09** (VALIDATED BUT WRONG, confidence 0.728): Where should patients needing droplet precautions be placed in an outpatient setting?
- **T03** (VALIDATED BUT WRONG, confidence 0.903): How often should temperature monitoring devices be calibration tested?
- **RO1** (VALIDATED BUT OUT OF CORPUS, confidence 0.639): What is the recommended dose of amoxicillin for otitis media?
- **R28** (VALIDATED BUT WRONG, confidence 1.0): What are the five components of the WHO multimodal hand hygiene improvement strategy?
- **RO5** (VALIDATED BUT OUT OF CORPUS, confidence 0.638): What steam temperature and exposure time are needed to autoclave surgical instruments?
- **R36** (VALIDATED BUT WRONG, confidence 1.0): Should hot water be used for handwashing in health care?
- **RO7** (VALIDATED BUT OUT OF CORPUS, confidence 0.636): What is the recommended dosage of oseltamivir for influenza prophylaxis?
- **RO8** (VALIDATED BUT OUT OF CORPUS, confidence 0.673): How should lead aprons be cleaned after X-ray procedures?
- **N03** (flagged: low confidence, confidence 0.421): how accurate does the thermometer have to be
- **N04** (flagged: low confidence, confidence 0.485): what should i set the fridge thermostat to
- **N05** (VALIDATED BUT WRONG, confidence 0.719): after changing the thermostat how long before i check the temperature again
- **N07** (flagged: low confidence, confidence 0.432): how long can mResvia be kept in the fridge
- **N11** (flagged: low confidence, confidence 0.446): how long does norovirus take to make you sick
- **N14** (correct answer withheld, confidence 0.409): how many days of antibiotics are given after environmental exposure
- **N17** (VALIDATED BUT WRONG, confidence 0.638): how long should i rub my hands with sanitiser
- **N18** (VALIDATED BUT WRONG, confidence 0.776): what are the benefits of hand-rub
- **N19** (VALIDATED BUT WRONG, confidence 0.662): is it ok to wear fake nails around patients
- **N20** (correct answer withheld, confidence 0.451): how many sinks are needed per patient bed
- **N21** (flagged: low confidence, confidence 0.55): what percentage alcohol is in the WHO handrub recipe
- **N23** (VALIDATED BUT WRONG, confidence 1.0): can disposable gloves be reused
- **N24** (VALIDATED BUT WRONG, confidence 0.811): what helps with dry cracked skin from hand washing
