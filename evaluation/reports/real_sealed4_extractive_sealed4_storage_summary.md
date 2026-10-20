# Evaluation summary: real corpus, sealed4 split

- Index: `9bc2368dd16cc348…`  |  generator: `extractive`  |  threshold: 0.6
- Queries: 47 in-corpus, 0 out-of-corpus

## Retrieval (in-corpus queries)

| Metric | Value |
|---|---|
| Precision@1 (document level) | 91.5% |
| Precision@5 (document level) | 89.8% |
| Precision@10 (document level) | 86.2% |
| Capped Precision@1 (vs. best attainable) | 91.5% |
| Capped Precision@5 (vs. best attainable) | 89.8% |
| Capped Precision@10 (vs. best attainable) | 86.2% |
| Hit@1 (a chunk containing the expected fact) | 57.5% |
| Hit@5 (a chunk containing the expected fact) | 85.1% |
| Hit@10 (a chunk containing the expected fact) | 89.4% |
| MRR (first fact-bearing chunk) | 0.673 |

## Answers and validation

| Metric | Value |
|---|---|
| Pass rate (validated / in-corpus) | 89.4% |
| Mean confidence (in-corpus) | 0.7777 |
| Answer correct (expected facts present) | 61.7% |
| **Validated precision** (correct among validated) | 69.0% |
| **Validated but wrong** | 30.9% |
| Correct but flagged for review | 0.0% |
| Out-of-corpus sent to review | n/a |
| Out-of-corpus falsely validated | n/a |
| Decision accuracy (all queries) | 72.3% |

A high pass rate alone is not evidence of quality: an extractive answer is copied from the evidence, so coverage is near-perfect by construction. Validated precision and the validated-but-wrong rate are the meaningful numbers.

## Threshold sweep

| Threshold | Pass rate | Validated precision | Validated but wrong | Correct but flagged | OOC false accept | Decision accuracy |
|---|---|---|---|---|---|---|
| 0.3 | 97.9% | 63.0% | 37.0% | 0.0% | n/a | 63.8% |
| 0.35 | 95.7% | 64.4% | 35.6% | 0.0% | n/a | 66.0% |
| 0.4 | 95.7% | 64.4% | 35.6% | 0.0% | n/a | 66.0% |
| 0.45 | 93.6% | 65.9% | 34.1% | 0.0% | n/a | 68.1% |
| 0.5 | 91.5% | 67.4% | 32.6% | 0.0% | n/a | 70.2% |
| 0.55 | 89.4% | 69.0% | 30.9% | 0.0% | n/a | 72.3% |
| 0.6 | 89.4% | 69.0% | 30.9% | 0.0% | n/a | 72.3% |
| 0.65 | 85.1% | 70.0% | 30.0% | 3.5% | n/a | 72.3% |
| 0.7 | 80.8% | 71.0% | 28.9% | 6.9% | n/a | 72.3% |
| 0.75 | 70.2% | 69.7% | 30.3% | 20.7% | n/a | 66.0% |
| 0.8 | 59.6% | 71.4% | 28.6% | 31.0% | n/a | 63.8% |
| 0.85 | 42.5% | 65.0% | 35.0% | 55.2% | n/a | 51.1% |
| 0.9 | 19.1% | 66.7% | 33.3% | 79.3% | n/a | 44.7% |

## Items for analyst review (18)

- **S01** (VALIDATED BUT WRONG, confidence 0.923): What are the specific temperature ranges required for refrigerators, standard freezers, and ultra-cold storage units?
- **S02** (VALIDATED BUT WRONG, confidence 0.985): Which four types of storage units are suitable for storing vaccines, and what is their CDC order of preference?
- **S05** (VALIDATED BUT WRONG, confidence 0.775): What key technical features must a digital data logger (DDL) possess to ensure reliable temperature tracking?
- **S07** (VALIDATED BUT WRONG, confidence 0.912): What information must be shown on a valid Certificate of Calibration Testing for a temperature monitoring device (TMD)?
- **S08** (VALIDATED BUT WRONG, confidence 0.856): How often should routine calibration testing be conducted on temperature monitoring devices?
- **S09** (VALIDATED BUT WRONG, confidence 0.646): What daily schedule and specific data points must staff record on standard temperature logs?
- **S14** (VALIDATED BUT WRONG, confidence 0.896): How should vaccine deliveries be processed and unpacked immediately upon arrival at the facility?
- **S15** (VALIDATED BUT WRONG, confidence 0.845): What are the acceptable containers and packouts approved for non-emergency vaccine transport to off-site or satellite clinics?
- **S17** (VALIDATED BUT WRONG, confidence 0.861): What steps must a provider take to calculate and document a Beyond-Use Date (BUD) when transitioning vaccines between storage states?
- **S22** (VALIDATED BUT WRONG, confidence 0.876): Which specific types of thermometers are not recommended for monitoring vaccines due to accuracy limitations?
- **S25** (VALIDATED BUT WRONG, confidence 0.733): Why must commercial shipping containers and frozen coolant gel packs from distributors never be reused for routine non-emergency transport?
- **S28** (VALIDATED BUT WRONG, confidence 0.758): Why is it unacceptable to pool or combine leftover vaccine from multiple single-dose or multidose vials to create a full dose?
- **S32** (flagged: low confidence, confidence 0.511): Why should staff never silence or reset a temperature alarm without notifying coordinators and investigating the root cause?
- **S35** (flagged: low confidence, confidence 0.0): My storage unit alarm went off during the weekend. What is the immediate, step-by-step troubleshooting workflow I must execute right now?
- **S42** (flagged: low confidence, confidence 0.486): If a clinical worker forgot to manually record a daily temperature on the physical sheet, can they estimate or back-fill the entry?
- **S44** (flagged: low confidence, confidence 0.414): If predrawn doses prepared for a morning clinic are left unused by the end of the shift, can they be refrigerated and administered the following morning?
- **S45** (VALIDATED BUT WRONG, confidence 0.698): If diluents are stored at room temperature but must travel with refrigerated vaccines, how should they be pre-conditioned so they don't elevate the packout temperature?
- **S47** (flagged: low confidence, confidence 0.329): If a digital data logger is accidentally dropped onto the clinic floor, can staff continue using it immediately, or is re-verification required?
