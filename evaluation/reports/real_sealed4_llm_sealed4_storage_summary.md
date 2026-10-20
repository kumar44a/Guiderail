# Evaluation summary: real corpus, sealed4 split

- Index: `9bc2368dd16cc348…`  |  generator: `llm`  |  threshold: 0.6
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
| Pass rate (validated / in-corpus) | 83.0% |
| Mean confidence (in-corpus) | 0.6672 |
| Answer correct (expected facts present) | 78.7% |
| **Validated precision** (correct among validated) | 92.3% |
| **Validated but wrong** | 7.7% |
| Correct but flagged for review | 2.7% |
| Out-of-corpus sent to review | n/a |
| Out-of-corpus falsely validated | n/a |
| Decision accuracy (all queries) | 91.5% |

A high pass rate alone is not evidence of quality: an extractive answer is copied from the evidence, so coverage is near-perfect by construction. Validated precision and the validated-but-wrong rate are the meaningful numbers.

## Threshold sweep

| Threshold | Pass rate | Validated precision | Validated but wrong | Correct but flagged | OOC false accept | Decision accuracy |
|---|---|---|---|---|---|---|
| 0.3 | 83.0% | 92.3% | 7.7% | 2.7% | n/a | 91.5% |
| 0.35 | 83.0% | 92.3% | 7.7% | 2.7% | n/a | 91.5% |
| 0.4 | 83.0% | 92.3% | 7.7% | 2.7% | n/a | 91.5% |
| 0.45 | 83.0% | 92.3% | 7.7% | 2.7% | n/a | 91.5% |
| 0.5 | 83.0% | 92.3% | 7.7% | 2.7% | n/a | 91.5% |
| 0.55 | 83.0% | 92.3% | 7.7% | 2.7% | n/a | 91.5% |
| 0.6 | 83.0% | 92.3% | 7.7% | 2.7% | n/a | 91.5% |
| 0.65 | 78.7% | 94.6% | 5.4% | 5.4% | n/a | 91.5% |
| 0.7 | 66.0% | 96.8% | 3.2% | 18.9% | n/a | 83.0% |
| 0.75 | 59.6% | 96.4% | 3.6% | 27.0% | n/a | 76.6% |
| 0.8 | 40.4% | 100.0% | 0.0% | 48.6% | n/a | 61.7% |
| 0.85 | 25.5% | 100.0% | 0.0% | 67.6% | n/a | 46.8% |
| 0.9 | 10.6% | 100.0% | 0.0% | 86.5% | n/a | 31.9% |

## Items for analyst review (11)

- **S02** (flagged: low confidence, confidence 0.0): Which four types of storage units are suitable for storing vaccines, and what is their CDC order of preference?
- **S08** (flagged: low confidence, confidence 0.0): How often should routine calibration testing be conducted on temperature monitoring devices?
- **S09** (VALIDATED BUT WRONG, confidence 0.613): What daily schedule and specific data points must staff record on standard temperature logs?
- **S28** (VALIDATED BUT WRONG, confidence 0.75): Why is it unacceptable to pool or combine leftover vaccine from multiple single-dose or multidose vials to create a full dose?
- **S30** (flagged: low confidence, confidence 0.0): Why must diluents never be placed into a freezer unit, even during transport?
- **S32** (flagged: low confidence, confidence 0.0): Why should staff never silence or reset a temperature alarm without notifying coordinators and investigating the root cause?
- **S35** (flagged: low confidence, confidence 0.0): My storage unit alarm went off during the weekend. What is the immediate, step-by-step troubleshooting workflow I must execute right now?
- **S42** (flagged: low confidence, confidence 0.0): If a clinical worker forgot to manually record a daily temperature on the physical sheet, can they estimate or back-fill the entry?
- **S44** (correct answer withheld, confidence 0.299): If predrawn doses prepared for a morning clinic are left unused by the end of the shift, can they be refrigerated and administered the following morning?
- **S45** (VALIDATED BUT WRONG, confidence 0.671): If diluents are stored at room temperature but must travel with refrigerated vaccines, how should they be pre-conditioned so they don't elevate the packout temperature?
- **S47** (flagged: low confidence, confidence 0.0): If a digital data logger is accidentally dropped onto the clinic floor, can staff continue using it immediately, or is re-verification required?
