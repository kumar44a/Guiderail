# Evaluation summary: real corpus, dev split

- Index: `9bc2368dd16cc348…`  |  generator: `llm`  |  threshold: 0.6
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
| Pass rate (validated / in-corpus) | 66.0% |
| Mean confidence (in-corpus) | 0.6549 |
| Answer correct (expected facts present) | 80.0% |
| **Validated precision** (correct among validated) | 90.9% |
| **Validated but wrong** | 9.1% |
| Correct but flagged for review | 25.0% |
| Out-of-corpus sent to review | 100.0% |
| Out-of-corpus falsely validated | 0.0% |
| Decision accuracy (all queries) | 77.6% |

A high pass rate alone is not evidence of quality: an extractive answer is copied from the evidence, so coverage is near-perfect by construction. Validated precision and the validated-but-wrong rate are the meaningful numbers.

## Threshold sweep

| Threshold | Pass rate | Validated precision | Validated but wrong | Correct but flagged | OOC false accept | Decision accuracy |
|---|---|---|---|---|---|---|
| 0.3 | 86.0% | 93.0% | 7.0% | 0.0% | 0.0% | 94.8% |
| 0.35 | 86.0% | 93.0% | 7.0% | 0.0% | 0.0% | 94.8% |
| 0.4 | 84.0% | 92.9% | 7.1% | 2.5% | 0.0% | 93.1% |
| 0.45 | 80.0% | 92.5% | 7.5% | 7.5% | 0.0% | 89.7% |
| 0.5 | 72.0% | 91.7% | 8.3% | 17.5% | 0.0% | 82.8% |
| 0.55 | 70.0% | 91.4% | 8.6% | 20.0% | 0.0% | 81.0% |
| 0.6 | 66.0% | 90.9% | 9.1% | 25.0% | 0.0% | 77.6% |
| 0.65 | 66.0% | 90.9% | 9.1% | 25.0% | 0.0% | 77.6% |
| 0.7 | 58.0% | 93.1% | 6.9% | 32.5% | 0.0% | 74.1% |
| 0.75 | 52.0% | 92.3% | 7.7% | 40.0% | 0.0% | 69.0% |
| 0.8 | 42.0% | 95.2% | 4.8% | 50.0% | 0.0% | 63.8% |
| 0.85 | 38.0% | 94.7% | 5.3% | 55.0% | 0.0% | 60.3% |
| 0.9 | 24.0% | 100.0% | 0.0% | 70.0% | 0.0% | 51.7% |

## Items for analyst review (20)

- **R07** (correct answer withheld, confidence 0.556): What must a symptomatic visitor do if they are allowed to stay with a patient?
- **R09** (flagged: low confidence, confidence 0.0): Where should patients needing droplet precautions be placed in an outpatient setting?
- **T05** (correct answer withheld, confidence 0.369): What label should be put on vaccines after a temperature excursion?
- **R24** (correct answer withheld, confidence 0.5): What is the minimum sink-to-patient bed ratio according to WHO?
- **R28** (flagged: low confidence, confidence 0.0): What are the five components of the WHO multimodal hand hygiene improvement strategy?
- **N01** (correct answer withheld, confidence 0.562): how long does a new fridge take to settle on the right temperature
- **N03** (VALIDATED BUT WRONG, confidence 0.657): how accurate does the thermometer have to be
- **N04** (correct answer withheld, confidence 0.481): what should i set the fridge thermostat to
- **N05** (flagged: low confidence, confidence 0.0): after changing the thermostat how long before i check the temperature again
- **N07** (correct answer withheld, confidence 0.49): how long can mResvia be kept in the fridge
- **N11** (flagged: low confidence, confidence 0.0): how long does norovirus take to make you sick
- **N14** (correct answer withheld, confidence 0.43): how many days of antibiotics are given after environmental exposure
- **N15** (correct answer withheld, confidence 0.498): how many days should mumps patients be isolated
- **N17** (flagged: low confidence, confidence 0.0): how long should i rub my hands with sanitiser
- **N18** (VALIDATED BUT WRONG, confidence 0.776): what are the benefits of hand-rub
- **N19** (correct answer withheld, confidence 0.41): is it ok to wear fake nails around patients
- **N20** (flagged: low confidence, confidence 0.0): how many sinks are needed per patient bed
- **N21** (flagged: low confidence, confidence 0.0): what percentage alcohol is in the WHO handrub recipe
- **N24** (VALIDATED BUT WRONG, confidence 0.877): what helps with dry cracked skin from hand washing
- **N25** (correct answer withheld, confidence 0.46): what languages are the world hand hygiene day posters in
