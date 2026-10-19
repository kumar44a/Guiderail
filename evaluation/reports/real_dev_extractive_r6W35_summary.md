# Evaluation summary: real corpus, dev split

- Index: `1886e6a2fec92f2e…`  |  generator: `extractive`  |  threshold: 0.6
- Queries: 50 in-corpus, 8 out-of-corpus

## Retrieval (in-corpus queries)

| Metric | Value |
|---|---|
| Precision@1 (document level) | 90.0% |
| Precision@5 (document level) | 78.8% |
| Precision@10 (document level) | 75.0% |
| Capped Precision@1 (vs. best attainable) | 90.0% |
| Capped Precision@5 (vs. best attainable) | 78.8% |
| Capped Precision@10 (vs. best attainable) | 75.0% |
| Hit@1 (a chunk containing the expected fact) | 50.0% |
| Hit@5 (a chunk containing the expected fact) | 74.0% |
| Hit@10 (a chunk containing the expected fact) | 92.0% |
| MRR (first fact-bearing chunk) | 0.6027 |

## Answers and validation

| Metric | Value |
|---|---|
| Pass rate (validated / in-corpus) | 88.0% |
| Mean confidence (in-corpus) | 0.8201 |
| Answer correct (expected facts present) | 66.0% |
| **Validated precision** (correct among validated) | 72.7% |
| **Validated but wrong** | 27.3% |
| Correct but flagged for review | 3.0% |
| Out-of-corpus sent to review | 75.0% |
| Out-of-corpus falsely validated | 25.0% |
| Decision accuracy (all queries) | 74.1% |

A high pass rate alone is not evidence of quality: an extractive answer is copied from the evidence, so coverage is near-perfect by construction. Validated precision and the validated-but-wrong rate are the meaningful numbers.

## Threshold sweep

| Threshold | Pass rate | Validated precision | Validated but wrong | Correct but flagged | OOC false accept | Decision accuracy |
|---|---|---|---|---|---|---|
| 0.3 | 98.0% | 65.3% | 34.7% | 3.0% | 100.0% | 55.2% |
| 0.35 | 96.0% | 66.7% | 33.3% | 3.0% | 100.0% | 56.9% |
| 0.4 | 96.0% | 66.7% | 33.3% | 3.0% | 100.0% | 56.9% |
| 0.45 | 96.0% | 66.7% | 33.3% | 3.0% | 87.5% | 58.6% |
| 0.5 | 94.0% | 68.1% | 31.9% | 3.0% | 75.0% | 62.1% |
| 0.55 | 92.0% | 69.6% | 30.4% | 3.0% | 75.0% | 63.8% |
| 0.6 | 88.0% | 72.7% | 27.3% | 3.0% | 25.0% | 74.1% |
| 0.65 | 86.0% | 74.4% | 25.6% | 3.0% | 0.0% | 79.3% |
| 0.7 | 80.0% | 75.0% | 25.0% | 9.1% | 0.0% | 77.6% |
| 0.75 | 72.0% | 77.8% | 22.2% | 15.2% | 0.0% | 77.6% |
| 0.8 | 62.0% | 77.4% | 22.6% | 27.3% | 0.0% | 72.4% |
| 0.85 | 54.0% | 77.8% | 22.2% | 36.4% | 0.0% | 69.0% |
| 0.9 | 44.0% | 77.3% | 22.7% | 48.5% | 0.0% | 63.8% |

## Items for analyst review (20)

- **R09** (VALIDATED BUT WRONG, confidence 0.728): Where should patients needing droplet precautions be placed in an outpatient setting?
- **T03** (VALIDATED BUT WRONG, confidence 0.902): How often should temperature monitoring devices be calibration tested?
- **T07** (VALIDATED BUT WRONG, confidence 1.0): What does the backup vaccine coordinator do?
- **RO1** (VALIDATED BUT OUT OF CORPUS, confidence 0.64): What is the recommended dose of amoxicillin for otitis media?
- **R28** (VALIDATED BUT WRONG, confidence 0.919): What are the five components of the WHO multimodal hand hygiene improvement strategy?
- **RO5** (VALIDATED BUT OUT OF CORPUS, confidence 0.639): What steam temperature and exposure time are needed to autoclave surgical instruments?
- **R36** (VALIDATED BUT WRONG, confidence 1.0): Should hot water be used for handwashing in health care?
- **N03** (flagged: low confidence, confidence 0.484): how accurate does the thermometer have to be
- **N04** (flagged: low confidence, confidence 0.571): what should i set the fridge thermostat to
- **N05** (VALIDATED BUT WRONG, confidence 0.721): after changing the thermostat how long before i check the temperature again
- **N07** (correct answer withheld, confidence 0.275): how long can mResvia be kept in the fridge
- **N11** (flagged: low confidence, confidence 0.522): how long does norovirus take to make you sick
- **N12** (VALIDATED BUT WRONG, confidence 0.884): how soon after measles exposure should the vaccine be given
- **N14** (flagged: low confidence, confidence 0.571): how many days of antibiotics are given after environmental exposure
- **N17** (flagged: low confidence, confidence 0.339): how long should i rub my hands with sanitiser
- **N18** (VALIDATED BUT WRONG, confidence 0.775): what are the benefits of hand-rub
- **N19** (VALIDATED BUT WRONG, confidence 0.664): is it ok to wear fake nails around patients
- **N21** (VALIDATED BUT WRONG, confidence 0.635): what percentage alcohol is in the WHO handrub recipe
- **N23** (VALIDATED BUT WRONG, confidence 0.929): can disposable gloves be reused
- **N24** (VALIDATED BUT WRONG, confidence 0.811): what helps with dry cracked skin from hand washing
