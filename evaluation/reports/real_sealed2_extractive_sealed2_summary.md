# Evaluation summary: real corpus, sealed2 split

- Index: `9bc2368dd16cc348…`  |  generator: `extractive`  |  threshold: 0.6
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
| Pass rate (validated / in-corpus) | 85.4% |
| Mean confidence (in-corpus) | 0.7794 |
| Answer correct (expected facts present) | 54.2% |
| **Validated precision** (correct among validated) | 53.7% |
| **Validated but wrong** | 46.3% |
| Correct but flagged for review | 15.4% |
| Out-of-corpus sent to review | 0.0% |
| Out-of-corpus falsely validated | 100.0% |
| Decision accuracy (all queries) | 50.0% |

A high pass rate alone is not evidence of quality: an extractive answer is copied from the evidence, so coverage is near-perfect by construction. Validated precision and the validated-but-wrong rate are the meaningful numbers.

## Threshold sweep

| Threshold | Pass rate | Validated precision | Validated but wrong | Correct but flagged | OOC false accept | Decision accuracy |
|---|---|---|---|---|---|---|
| 0.3 | 100.0% | 54.2% | 45.8% | 0.0% | 100.0% | 52.0% |
| 0.35 | 100.0% | 54.2% | 45.8% | 0.0% | 100.0% | 52.0% |
| 0.4 | 100.0% | 54.2% | 45.8% | 0.0% | 100.0% | 52.0% |
| 0.45 | 100.0% | 54.2% | 45.8% | 0.0% | 100.0% | 52.0% |
| 0.5 | 97.9% | 53.2% | 46.8% | 3.9% | 100.0% | 50.0% |
| 0.55 | 91.7% | 54.5% | 45.5% | 7.7% | 100.0% | 52.0% |
| 0.6 | 85.4% | 53.7% | 46.3% | 15.4% | 100.0% | 50.0% |
| 0.65 | 81.2% | 56.4% | 43.6% | 15.4% | 100.0% | 54.0% |
| 0.7 | 77.1% | 56.8% | 43.2% | 19.2% | 50.0% | 56.0% |
| 0.75 | 66.7% | 56.2% | 43.8% | 30.8% | 50.0% | 54.0% |
| 0.8 | 52.1% | 64.0% | 36.0% | 38.5% | 50.0% | 60.0% |
| 0.85 | 27.1% | 69.2% | 30.8% | 65.4% | 0.0% | 58.0% |
| 0.9 | 22.9% | 63.6% | 36.4% | 73.1% | 0.0% | 54.0% |

## Items for analyst review (28)

- **V01** (VALIDATED BUT WRONG, confidence 0.635): What is the overarching purpose and primary goal of the WHO Guidelines on Hand Hygiene in Health Care?
- **V02** (VALIDATED BUT WRONG, confidence 0.778): What are the specific components of the "My 5 Moments for Hand Hygiene" framework?
- **V04** (VALIDATED BUT WRONG, confidence 0.813): What is the recommended duration and sequence of steps for performing hand hygiene using an alcohol-based handrub?
- **V05** (VALIDATED BUT WRONG, confidence 0.784): What is the recommended duration and step-by-step technique for washing hands with soap and water?
- **V06** (VALIDATED BUT WRONG, confidence 0.771): When should hand hygiene be performed during patient care even if gloves are worn?
- **V07** (VALIDATED BUT WRONG, confidence 0.778): What are the 5 core elements of the WHO Multimodal Hand Hygiene Improvement Strategy?
- **V08** (VALIDATED BUT WRONG, confidence 0.804): How does proper hand hygiene impact the incidence of health care-associated infections (HCAIs) and cross-transmission?
- **V09** (VALIDATED BUT WRONG, confidence 0.91): What are the validated formulations recommended by WHO for the local production of alcohol-based handrubs?
- **V10** (correct answer withheld, confidence 0.534): What is the optimal concentration range of alcohol (ethanol or isopropanol) required for effective antimicrobial efficacy?
- **V12** (VALIDATED BUT WRONG, confidence 0.838): Why are alcohol-based handrubs considered superior to handwashing with plain soap for routine decontamination?
- **V14** (VALIDATED BUT WRONG, confidence 0.952): What are the criteria for selecting suitable hand hygiene products in health-care facilities?
- **V19** (flagged: low confidence, confidence 0.528): What are the recommended guidelines regarding the length and maintenance of natural fingernails for healthcare providers?
- **V21** (VALIDATED BUT WRONG, confidence 0.735): What evidence grading categories (e.g., Category IA, IB, IC, II) does WHO use to classify its recommendations?
- **V24** (flagged: low confidence, confidence 0.507): How do educational campaigns and visual workplace reminders influence long-term behavioral change?
- **V27** (VALIDATED BUT WRONG, confidence 0.92): Why should healthcare workers not use soap and alcohol-based handrub concomitantly?
- **V28** (VALIDATED BUT WRONG, confidence 0.68): What are the limitations of alcohol-based handrubs against bacterial spores, specifically Clostridium difficile?
- **V30** (flagged: low confidence, confidence 0.574): Why is the reuse of disposable medical gloves strongly discouraged?
- **V32** (VALIDATED BUT WRONG, confidence 0.925): What are the primary risk factors observed for poor hand hygiene adherence among healthcare workers?
- **V34** (VALIDATED BUT WRONG, confidence 0.613): What self-reported reasons do health-care workers give for failing to adhere to hand hygiene protocols?
- **V35** (VALIDATED BUT WRONG, confidence 0.755): What is the fire hazard risk associated with alcohol-based handrub dispensers, and what are the actual incident statistics?
- **V36** (VALIDATED BUT WRONG, confidence 0.745): What safety precautions must be taken to prevent intentional or accidental ingestion of alcohol handrubs in psychiatric and pediatric units?
- **V37** (VALIDATED BUT WRONG, confidence 0.836): Does frequent use of alcohol-based handrubs lead to significant dermal absorption of alcohol into the bloodstream?
- **V39** (correct answer withheld, confidence 0.561): Why should soap dispensers never be topped up or partially refilled with new soap?
- **V42** (VALIDATED BUT OUT OF CORPUS, confidence 0.832): How does donning gloves on damp or wet hands exacerbate skin damage and irritation?
- **V44** (VALIDATED BUT OUT OF CORPUS, confidence 0.66): Why can wearing gloves create a false sense of security and lead to missed hand hygiene opportunities?
- **V46** (correct answer withheld, confidence 0.498): How do automated or sensor sinks occasionally lead to lower compliance or technical issues?
- **V47** (correct answer withheld, confidence 0.563): Which antiseptic agents have poor or non-existent residual persistence on the skin?
- **V48** (VALIDATED BUT WRONG, confidence 0.818): What non-enveloped viruses exhibit reduced susceptibility to standard alcohol concentrations?
