# Evaluation summary: real corpus, sealed2 split

- Index: `9bc2368dd16cc348…`  |  generator: `llm`  |  threshold: 0.6
- Queries: 48 in-corpus, 2 out-of-corpus

## Retrieval (in-corpus queries)

| Metric | Value |
|---|---|
| Precision@1 (document level) | 87.5% |
| Precision@5 (document level) | 80.4% |
| Precision@10 (document level) | 79.8% |
| Capped Precision@1 (vs. best attainable) | 87.5% |
| Capped Precision@5 (vs. best attainable) | 80.4% |
| Capped Precision@10 (vs. best attainable) | 79.8% |
| Hit@1 (a chunk containing the expected fact) | 31.2% |
| Hit@5 (a chunk containing the expected fact) | 68.8% |
| Hit@10 (a chunk containing the expected fact) | 81.2% |
| MRR (first fact-bearing chunk) | 0.4696 |

## Answers and validation

| Metric | Value |
|---|---|
| Pass rate (validated / in-corpus) | 60.4% |
| Mean confidence (in-corpus) | 0.525 |
| Answer correct (expected facts present) | 47.9% |
| **Validated precision** (correct among validated) | 69.0% |
| **Validated but wrong** | 31.0% |
| Correct but flagged for review | 13.0% |
| Out-of-corpus sent to review | 50.0% |
| Out-of-corpus falsely validated | 50.0% |
| Decision accuracy (all queries) | 74.0% |

A high pass rate alone is not evidence of quality: an extractive answer is copied from the evidence, so coverage is near-perfect by construction. Validated precision and the validated-but-wrong rate are the meaningful numbers.

## Threshold sweep

| Threshold | Pass rate | Validated precision | Validated but wrong | Correct but flagged | OOC false accept | Decision accuracy |
|---|---|---|---|---|---|---|
| 0.3 | 68.8% | 66.7% | 33.3% | 4.3% | 50.0% | 74.0% |
| 0.35 | 66.7% | 68.8% | 31.2% | 4.3% | 50.0% | 76.0% |
| 0.4 | 66.7% | 68.8% | 31.2% | 4.3% | 50.0% | 76.0% |
| 0.45 | 66.7% | 68.8% | 31.2% | 4.3% | 50.0% | 76.0% |
| 0.5 | 64.6% | 71.0% | 29.0% | 4.3% | 50.0% | 78.0% |
| 0.55 | 60.4% | 69.0% | 31.0% | 13.0% | 50.0% | 74.0% |
| 0.6 | 60.4% | 69.0% | 31.0% | 13.0% | 50.0% | 74.0% |
| 0.65 | 58.3% | 67.9% | 32.1% | 17.4% | 50.0% | 72.0% |
| 0.7 | 52.1% | 72.0% | 28.0% | 21.7% | 50.0% | 74.0% |
| 0.75 | 43.8% | 71.4% | 28.6% | 34.8% | 50.0% | 70.0% |
| 0.8 | 27.1% | 84.6% | 15.4% | 52.2% | 0.0% | 72.0% |
| 0.85 | 10.4% | 100.0% | 0.0% | 78.3% | 0.0% | 64.0% |
| 0.9 | 8.3% | 100.0% | 0.0% | 82.6% | 0.0% | 62.0% |

## Items for analyst review (29)

- **V01** (VALIDATED BUT WRONG, confidence 0.702): What is the overarching purpose and primary goal of the WHO Guidelines on Hand Hygiene in Health Care?
- **V02** (flagged: low confidence, confidence 0.0): What are the specific components of the "My 5 Moments for Hand Hygiene" framework?
- **V04** (VALIDATED BUT WRONG, confidence 0.773): What is the recommended duration and sequence of steps for performing hand hygiene using an alcohol-based handrub?
- **V05** (VALIDATED BUT WRONG, confidence 0.807): What is the recommended duration and step-by-step technique for washing hands with soap and water?
- **V06** (VALIDATED BUT WRONG, confidence 0.75): When should hand hygiene be performed during patient care even if gloves are worn?
- **V07** (flagged: low confidence, confidence 0.0): What are the 5 core elements of the WHO Multimodal Hand Hygiene Improvement Strategy?
- **V08** (flagged: low confidence, confidence 0.0): How does proper hand hygiene impact the incidence of health care-associated infections (HCAIs) and cross-transmission?
- **V10** (correct answer withheld, confidence 0.534): What is the optimal concentration range of alcohol (ethanol or isopropanol) required for effective antimicrobial efficacy?
- **V12** (flagged: low confidence, confidence 0.342): Why are alcohol-based handrubs considered superior to handwashing with plain soap for routine decontamination?
- **V14** (VALIDATED BUT WRONG, confidence 0.781): What are the criteria for selecting suitable hand hygiene products in health-care facilities?
- **V19** (flagged: low confidence, confidence 0.0): What are the recommended guidelines regarding the length and maintenance of natural fingernails for healthcare providers?
- **V21** (flagged: low confidence, confidence 0.0): What evidence grading categories (e.g., Category IA, IB, IC, II) does WHO use to classify its recommendations?
- **V24** (correct answer withheld, confidence 0.534): How do educational campaigns and visual workplace reminders influence long-term behavioral change?
- **V27** (flagged: low confidence, confidence 0.0): Why should healthcare workers not use soap and alcohol-based handrub concomitantly?
- **V28** (VALIDATED BUT WRONG, confidence 0.68): What are the limitations of alcohol-based handrubs against bacterial spores, specifically Clostridium difficile?
- **V30** (flagged: low confidence, confidence 0.489): Why is the reuse of disposable medical gloves strongly discouraged?
- **V33** (flagged: low confidence, confidence 0.0): Why do physicians and male health-care personnel consistently demonstrate lower baseline compliance rates than nurses?
- **V34** (VALIDATED BUT WRONG, confidence 0.667): What self-reported reasons do health-care workers give for failing to adhere to hand hygiene protocols?
- **V35** (VALIDATED BUT WRONG, confidence 0.789): What is the fire hazard risk associated with alcohol-based handrub dispensers, and what are the actual incident statistics?
- **V36** (flagged: low confidence, confidence 0.0): What safety precautions must be taken to prevent intentional or accidental ingestion of alcohol handrubs in psychiatric and pediatric units?
- **V37** (VALIDATED BUT WRONG, confidence 0.836): Does frequent use of alcohol-based handrubs lead to significant dermal absorption of alcohol into the bloodstream?
- **V39** (flagged: low confidence, confidence 0.0): Why should soap dispensers never be topped up or partially refilled with new soap?
- **V40** (flagged: low confidence, confidence 0.0): Why are surgical scrub brushes no longer recommended for routine surgical hand antisepsis?
- **V42** (VALIDATED BUT OUT OF CORPUS, confidence 0.751): How does donning gloves on damp or wet hands exacerbate skin damage and irritation?
- **V43** (flagged: low confidence, confidence 0.0): Why is prolonged surgical scrubbing (e.g., 10 minutes) considered unnecessary and discouraged?
- **V46** (correct answer withheld, confidence 0.281): How do automated or sensor sinks occasionally lead to lower compliance or technical issues?
- **V47** (flagged: low confidence, confidence 0.0): Which antiseptic agents have poor or non-existent residual persistence on the skin?
- **V48** (flagged: low confidence, confidence 0.0): What non-enveloped viruses exhibit reduced susceptibility to standard alcohol concentrations?
- **V50** (flagged: low confidence, confidence 0.0): What institutional barriers prevent health-care facilities from maintaining an effective patient safety culture?
