# Evaluation summary: real corpus, dev split

- Index: `9bc2368dd16cc348…`  |  generator: `llm`  |  threshold: 0.6
- Queries: 50 in-corpus, 8 out-of-corpus

## Retrieval (in-corpus queries)

| Metric | Value |
|---|---|
| Precision@1 (document level) | 84.0% |
| Precision@5 (document level) | 79.2% |
| Precision@10 (document level) | 74.6% |
| Capped Precision@1 (vs. best attainable) | 84.0% |
| Capped Precision@5 (vs. best attainable) | 79.2% |
| Capped Precision@10 (vs. best attainable) | 74.6% |
| Hit@1 (a chunk containing the expected fact) | 56.0% |
| Hit@5 (a chunk containing the expected fact) | 82.0% |
| Hit@10 (a chunk containing the expected fact) | 86.0% |
| MRR (first fact-bearing chunk) | 0.6566 |

## Answers and validation

| Metric | Value |
|---|---|
| Pass rate (validated / in-corpus) | 72.0% |
| Mean confidence (in-corpus) | 0.6879 |
| Answer correct (expected facts present) | 78.0% |
| **Validated precision** (correct among validated) | 94.4% |
| **Validated but wrong** | 5.6% |
| Correct but flagged for review | 12.8% |
| Out-of-corpus sent to review | 100.0% |
| Out-of-corpus falsely validated | 0.0% |
| Decision accuracy (all queries) | 87.9% |

A high pass rate alone is not evidence of quality: an extractive answer is copied from the evidence, so coverage is near-perfect by construction. Validated precision and the validated-but-wrong rate are the meaningful numbers.

## Threshold sweep

| Threshold | Pass rate | Validated precision | Validated but wrong | Correct but flagged | OOC false accept | Decision accuracy |
|---|---|---|---|---|---|---|
| 0.3 | 84.0% | 92.9% | 7.1% | 0.0% | 0.0% | 94.8% |
| 0.35 | 84.0% | 92.9% | 7.1% | 0.0% | 0.0% | 94.8% |
| 0.4 | 82.0% | 95.1% | 4.9% | 0.0% | 0.0% | 96.5% |
| 0.45 | 82.0% | 95.1% | 4.9% | 0.0% | 0.0% | 96.5% |
| 0.5 | 80.0% | 95.0% | 5.0% | 2.6% | 0.0% | 94.8% |
| 0.55 | 80.0% | 95.0% | 5.0% | 2.6% | 0.0% | 94.8% |
| 0.6 | 72.0% | 94.4% | 5.6% | 12.8% | 0.0% | 87.9% |
| 0.65 | 68.0% | 97.1% | 2.9% | 15.4% | 0.0% | 87.9% |
| 0.7 | 66.0% | 97.0% | 3.0% | 17.9% | 0.0% | 86.2% |
| 0.75 | 60.0% | 96.7% | 3.3% | 25.6% | 0.0% | 81.0% |
| 0.8 | 56.0% | 96.4% | 3.6% | 30.8% | 0.0% | 77.6% |
| 0.85 | 48.0% | 95.8% | 4.2% | 41.0% | 0.0% | 70.7% |
| 0.9 | 30.0% | 100.0% | 0.0% | 61.5% | 0.0% | 58.6% |

## Items for analyst review (16)

- **R07** (correct answer withheld, confidence 0.571): What must a symptomatic visitor do if they are allowed to stay with a patient?
- **R09** (flagged: low confidence, confidence 0.0): Where should patients needing droplet precautions be placed in an outpatient setting?
- **R28** (flagged: low confidence, confidence 0.0): What are the five components of the WHO multimodal hand hygiene improvement strategy?
- **N01** (correct answer withheld, confidence 0.562): how long does a new fridge take to settle on the right temperature
- **N03** (flagged: low confidence, confidence 0.0): how accurate does the thermometer have to be
- **N04** (correct answer withheld, confidence 0.571): what should i set the fridge thermostat to
- **N05** (flagged: low confidence, confidence 0.0): after changing the thermostat how long before i check the temperature again
- **N07** (flagged: low confidence, confidence 0.0): how long can mResvia be kept in the fridge
- **N11** (flagged: low confidence, confidence 0.0): how long does norovirus take to make you sick
- **N14** (correct answer withheld, confidence 0.568): how many days of antibiotics are given after environmental exposure
- **N15** (correct answer withheld, confidence 0.468): how many days should mumps patients be isolated
- **N17** (VALIDATED BUT WRONG, confidence 0.62): how long should i rub my hands with sanitiser
- **N18** (flagged: low confidence, confidence 0.0): what are the benefits of hand-rub
- **N19** (flagged: low confidence, confidence 0.368): is it ok to wear fake nails around patients
- **N21** (flagged: low confidence, confidence 0.0): what percentage alcohol is in the WHO handrub recipe
- **N24** (VALIDATED BUT WRONG, confidence 0.876): what helps with dry cracked skin from hand washing
