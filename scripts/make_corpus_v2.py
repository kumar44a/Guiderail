"""Build data/guidelines_v2/ from data/guidelines/.

    python scripts/make_corpus_v2.py

Every v1 file is copied byte for byte, then 3 to 4 new `##` sections are appended so each document has at least six chunks (the chunker makes one chunk of a
section of 80 words or fewer). who-linen-laundry-2022 is left as it is on purpose: it is the one-short-chunk hard case. The rules for this experiment are in
evaluation/reports/synthetic2_rules.txt. The text below is invented, like the rest of the synthetic corpus, and has not been clinically reviewed.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC, DST = ROOT / "data" / "guidelines", ROOT / "data" / "guidelines_v2"

ADD: dict[str, list[tuple[str, str]]] = {
"cdc-hand-hygiene-2021": [
 ("Hand hygiene and gloves", "Perform hand hygiene before putting on gloves for any invasive procedure and before handling a central line. Gloves do not replace hand hygiene because they can have small defects and hands can be contaminated during removal. Change gloves between tasks on the same patient when moving from a contaminated body site to a clean one."),
 ("Skin care", "Provide hospital-approved lotion to reduce dryness and dermatitis among staff. Do not use petroleum-based products that can weaken latex gloves. Staff with persistent skin damage should be referred to occupational health within 5 working days. Cuts and open wounds must be covered with a waterproof dressing before patient contact."),
 ("Product selection", "Choose hand rub containing 60 to 95 percent alcohol. Dispenser bottles must be single-use or cleaned and dried before refilling, and must never be topped up. Check expiry dates monthly. Discard any hand rub with no printed expiry date that is more than 12 months past its manufacture date."),
 ("Monitoring and feedback", "Use direct observation by trained auditors for at least 100 hand hygiene opportunities per unit each quarter. Share results with unit managers within 14 days. Units below 85 percent adherence should prepare an improvement plan and be audited again after 8 weeks."),
 ("Outbreaks of Clostridioides difficile", "During an outbreak of Clostridioides difficile, use soap and water for all care of affected patients and increase environmental cleaning. Display a sign at the door of each affected room. Continue the measure until 48 hours after diarrhoea has stopped."),
],
"cdc-isolation-return-to-work-2019": [
 ("Reporting symptoms", "Staff must tell their line manager and occupational health as soon as symptoms start, even if they are mild. A worker who becomes ill at work should leave patient areas at once, wear a medical mask while leaving, and go home. Do not use public transport if a private option exists."),
 ("Occupational health assessment", "Occupational health reviews every absence of more than 3 days before the worker returns. The review checks the date symptoms began, the date of the last fever, the present symptoms, and any contact with patients who are severely immunocompromised. The assessor signs a return-to-work form held in the employee file."),
 ("Records", "Keep a register of all respiratory illness absences by ward. Report the number of absent staff to the infection prevention team every Monday. A ward with 3 or more ill staff in one week should be reviewed for a possible cluster."),
 ("Exceptions in staff shortage", "When staffing is critically short, the director of nursing may ask occupational health to approve an earlier return for a worker who is fever-free and well. The worker must not care for severely immunocompromised patients and must wear a mask. Every exception is recorded with the reason."),
],
"cdc-isolation-return-to-work-2023": [
 ("Reporting symptoms", "Staff must tell their line manager and occupational health as soon as symptoms start, even if they are mild. A worker who becomes ill at work should leave patient areas at once, wear a medical mask while leaving, and go home. Counting of days begins on the day symptoms start, which is day 0."),
 ("Testing", "A rapid antigen test is acceptable for the day 5 test. If the first test on day 5 is positive, repeat it every 48 hours until negative or until day 10. A worker with a positive test on day 10 must stay off work and ask occupational health to review."),
 ("Masking through day 10", "The mask must be a medical mask or a respirator that fits well with no gaps. Staff may remove it only when eating or drinking alone, away from patients and colleagues. Masking stops after day 10 even if mild symptoms such as a cough continue."),
 ("Records and exceptions", "Occupational health records the onset date, return date, test result and masking plan for every absence. A ward manager may ask for an earlier return only during a declared staffing emergency, and the decision is signed by the director of nursing and logged."),
],
"cdc-outbreak-reporting-2022": [
 ("Recognising a cluster", "Look for clusters in the microbiology laboratory report, in ward handover notes and in staff illness records. Two cases of the same organism on one ward within 14 days should trigger a check of typing results. Compare resistance patterns, because an unusual pattern can reveal a cluster early."),
 ("The line list", "The line list should include patient identifier, age, ward, bed, onset date, specimen date, organism, symptoms, device use and outcome. Record the earliest onset date at the top. Review the list every morning and send an updated copy to the outbreak control team by 10:00."),
 ("The outbreak control team", "The team includes an infection prevention nurse, an infectious diseases physician, a microbiologist, a ward manager, an environmental services lead and a communications officer. The chair is the infection prevention physician. The team meets daily at first and twice a week once new cases slow."),
 ("Communication", "Tell patients and visitors on the affected ward what is happening, in plain language, within 24 hours of confirming an outbreak. Send a written update to all staff each Friday. Publish a short summary on the intranet once the outbreak is declared over."),
],
"cdc-ppe-2022": [
 ("Respirator fit and seal checks", "Perform a user seal check every time a tight-fitting respirator is put on. Facial hair that crosses the sealing surface prevents a good fit. Staff who cannot be fit tested should use a powered air-purifying respirator. Fit testing uses a qualitative or quantitative method and each worker is tested for the model and size they will use."),
 ("Gowns", "Use a fluid-resistant gown when splashes of blood or body fluids are likely. A disposable gown should be removed before leaving the patient room and thrown away in the room. Reusable cloth gowns must be laundered after each use. Do not use a gown that is torn or that does not cover the arms and torso."),
 ("Extended use and shortages", "During a shortage, extended use of the same respirator for repeated contacts with one cohort of patients may be allowed, up to 8 hours. Do not touch the front of the respirator. Discard it when it is damaged, soiled, wet or hard to breathe through."),
 ("Training and observation", "Train staff to put on and remove PPE before first use and every year. A trained observer should watch staff during donning and doffing in the first month after a new high-consequence pathogen is identified. Observers use a checklist and correct errors straight away."),
],
"cdc-respiratory-seasons-2023": [
 ("Staff vaccination", "Offer influenza vaccine at work, at no cost, with extended clinic hours including night shifts. Track uptake by unit every two weeks from September. Staff who decline vaccination for non-medical reasons should wear a mask in patient areas during the influenza season and should sign a declination form."),
 ("Visitor restrictions", "When community transmission is high, limit each patient to two visitors at a time. Children under 12 should not visit units caring for infants, transplant patients or patients receiving chemotherapy. Visitors with symptoms are asked to stay home and may be offered a video call instead."),
 ("Admission testing", "Test every patient admitted with fever or respiratory symptoms for influenza, COVID-19 and respiratory syncytial virus using a multiplex test. Aim to report the result within 4 hours. Keep the patient in a single room until the result is available."),
 ("Surge planning", "Identify in advance which wards can be turned into respiratory cohort areas. Stock enough masks, gowns and test kits for 6 weeks of high demand. Hold a tabletop exercise in September with the emergency department, intensive care and the infection prevention team."),
],
"cdc-sharps-injury-2022": [
 ("Safe handling during procedures", "Pass sharps with a tray or neutral zone, not from hand to hand. Announce when a sharp is being passed. Keep the sharp pointing away from yourself and others. Never leave a needle on a bed or in a pocket, and never bend or break a needle by hand."),
 ("Sharps containers", "Mount containers at standing eye level where staff can see the opening. Never push sharps down with your hand, and never reach into a container. Seal the container when it is three quarters full. Containers are collected for treatment and are not opened or emptied."),
 ("After an exposure", "Let the wound bleed freely and wash with soap and water for several minutes. Flush a splash to the eye with clean water or saline for at least 15 minutes. Do not squeeze the wound or apply bleach. Report the injury, the device and how it happened on the incident form."),
 ("Prophylaxis and follow-up", "If the source patient is known to have HIV, begin antiretroviral prophylaxis within 2 hours if possible and no later than 72 hours. Follow-up testing is done at 6 weeks, 3 months and 6 months. Offer counselling to the exposed worker at each visit."),
],
"cdc-vaccination-adult-schedule-2024": [
 ("Hepatitis B", "A hepatitis B series has three doses, given at 0, 1 and 6 months. Test anti-HBs 1 to 2 months after the last dose. A worker whose level is below 10 mIU/mL should repeat the series once and be tested again. Staff who still do not respond are considered non-responders and need counselling about exposures."),
 ("Measles, mumps and rubella", "Acceptable evidence of immunity is written documentation of two doses of vaccine, laboratory evidence of immunity, or laboratory confirmation of the disease. Birth before 1957 is not by itself evidence of immunity for staff in healthcare. Give two doses at least 28 days apart to those without evidence."),
 ("Varicella", "Staff are immune if they have two documented doses of vaccine, a laboratory result showing immunity or a diagnosis of varicella made by a healthcare provider. Staff without evidence receive two doses 4 to 8 weeks apart. Non-immune staff are restricted from duty from day 8 to day 21 after an exposure."),
 ("Contraindications and precautions", "Severe allergy to a vaccine component is a contraindication to that vaccine. Moderate or severe acute illness is a precaution and vaccination is usually delayed. Live vaccines are not given in pregnancy or to people who are severely immunocompromised. Document the reason whenever a vaccine is deferred."),
],
"cdc-vaccination-cold-chain-2024": [
 ("Storage unit set-up", "Place the unit away from direct sunlight and heat sources, with at least 10 centimetres of clear space behind and beside it. Plug it into a dedicated outlet with a warning sign and a plug guard. Allow a newly installed unit to run for 2 to 3 days and record stable temperatures before stocking any vaccine."),
 ("Daily monitoring", "Record the current, minimum and maximum temperatures at the start of each clinic day and again before closing. Staff initial each entry. A reading outside the range is an excursion and must be acted on at once, not at the next scheduled check. Download the data logger report every week."),
 ("Transport", "For off-site clinics pack refrigerated vaccines in a qualified container with conditioned cold packs and a probe. Do not use dry ice for refrigerated vaccines. Keep the container out of direct sun and out of a vehicle boot. Record the temperature at departure, on arrival and every hour."),
 ("Inventory", "Place vaccines with the earliest expiry date at the front so they are used first. Do a stock count every month. Remove expired vaccine at once and keep it separate and labelled until it is disposed of. Keep diluents with their matching vaccine."),
],
"nih-antimicrobial-stewardship-2022": [
 ("Leadership and resources", "The hospital executive must give protected time to the stewardship leads: at least 20 percent of a full-time pharmacist post for every 100 beds. Report outcomes to the hospital quality committee every quarter. Link prescribing data to the electronic health record so audit is not manual."),
 ("Prospective audit and feedback", "A pharmacist reviews all patients on restricted antibiotics every working day. When the review finds an inappropriate prescription, the pharmacist contacts the prescriber the same day and records the advice. Acceptance of the advice is tracked as a programme measure."),
 ("Surgical prophylaxis", "Give prophylactic antibiotic within 60 minutes before the incision. Stop it within 24 hours after surgery in most procedures. Do not continue prophylaxis only because a drain or catheter is still in place. Audit a sample of procedures each month."),
 ("Education", "Teach prescribers the local antibiogram every year. New doctors receive a stewardship briefing within their first two weeks. Provide pocket guidelines for common infections such as community-acquired pneumonia and urinary tract infection."),
],
"nih-evidence-hierarchy-2022": [
 ("Systematic reviews", "A systematic review uses explicit methods to find, select and appraise all relevant studies on a question. A meta-analysis is a statistical combination of results and may be part of a review. Reviews are only as strong as the studies in them and can mislead if they combine studies that differ greatly."),
 ("Randomised controlled trials", "In a randomised trial participants are allocated by chance to an intervention or a comparator. Concealing the allocation from those enrolling people prevents selection bias. Blinding reduces performance and detection bias. Trials that stop early for benefit may overestimate the effect."),
 ("Observational designs", "A cohort study follows groups defined by exposure over time. A case-control study compares people with a disease to people without it and looks back at exposures. Both are open to confounding, which is a mixing of the effects of different factors. Case series have no comparison group."),
 ("Appraisal tools", "Use a standard checklist for each design to judge the risk of bias. For trials, check randomisation, allocation concealment, blinding and loss to follow-up. Two reviewers should appraise each study independently and settle disagreements by discussion or by a third reviewer."),
],
"nih-grading-2021": [
 ("Domains for rating", "Study design sets the starting level. Directness asks whether the studies match the population and outcome of interest. Consistency asks whether results agree across studies. Precision asks whether the confidence interval is narrow enough to support a decision. Each domain is rated and the panel records the reason."),
 ("Strength of evidence categories", "High means the panel is very confident that the true effect is close to the estimate. Moderate means further research may change the estimate. Low means further research is very likely to change it. Insufficient means no conclusion can be drawn."),
 ("Panel process", "A panel has at least seven members, including a methodologist and a patient representative. Members declare conflicts of interest before the first meeting. A recommendation is adopted when at least two thirds of members agree. Dissent is recorded in the minutes."),
 ("Updating", "Review the evidence for each recommendation every three years. Review sooner if a large trial or a safety signal is published. A recommendation that has not been reviewed within five years is marked as out of date on the website."),
],
"nih-shared-decision-making-2023": [
 ("Preparing for the conversation", "Check which options are reasonable for the patient and what the evidence says about each. Allow at least 20 minutes for a first conversation about a major decision. Offer the patient a written summary and a chance to bring a family member or interpreter."),
 ("Presenting risks", "Use natural frequencies such as 5 in 100 rather than percentages. Present benefits and harms in the same format and over the same time period. Use visual aids such as icon arrays. Avoid vague words like rare or common unless they are defined."),
 ("Checking understanding", "Ask the patient to say in their own words what the options are. This teach-back approach finds misunderstandings early. If the patient is unsure, offer more time and a follow-up visit instead of pressing for a decision."),
 ("Decisions that change", "Offer to revisit the decision at set points such as after test results or at three months. Record when the patient changes their mind and why. A decision to decline treatment is a valid decision and the patient should still receive other care."),
],
"nih-vaccine-safety-monitoring-2023": [
 ("What to report", "Report any event that follows vaccination and that the patient, parent or clinician thinks may be related, even if the link is uncertain. Events that must always be reported include anaphylaxis, Guillain-Barre syndrome, seizures within 72 hours and any event that causes hospitalisation."),
 ("The report form", "Complete the form with the patient's age, sex, medical history, other medicines, the vaccine, dose number, the event description, onset date, treatment given and outcome. Do not leave fields blank: write unknown. Send a copy to the clinic's focal point."),
 ("Causality assessment", "Check whether the event follows vaccination at a plausible time, whether other causes exist, whether similar events are known for the vaccine and whether the event recurred on re-exposure. Record each answer. The assessment is repeated if new test results arrive."),
 ("Communicating with families", "Tell the family what is known about the event, what is being done and when they will hear again. Give a named contact and a phone number. Where an event is judged to be a true reaction, record it in the patient's record as an allergy or precaution."),
],
"who-environmental-cleaning-2022": [
 ("Cleaning equipment", "Use colour-coded cloths and mops: red for toilets, blue for general areas, green for kitchens and yellow for isolation rooms. Wash mops at 60 degrees Celsius and dry them fully before reuse. Never leave mops standing in dirty water. Replace worn equipment every three months."),
 ("Terminal cleaning", "After a patient with an infection is discharged, remove all linen and waste, then clean from top to bottom. Wipe the mattress and bed frame, the bedside table, the sink and the bathroom. Allow surfaces to dry before the bed is made. Record the time and the name of the cleaner."),
 ("Spills", "Cover a blood spill with absorbent material, then pour 0.5 percent sodium hypochlorite over it and leave it for 10 minutes. Wearing gloves and an apron, remove the material into a yellow bag. Clean the area with detergent and water and dry it."),
 ("Training and supervision", "New cleaners are trained for two days before working alone. Supervisors inspect at least five rooms per shift using a checklist and an ultraviolet marker or an adenosine triphosphate meter. Rooms scoring under 80 percent are re-cleaned and the cleaner is retrained."),
],
"who-grading-2020": [
 ("Certainty of evidence", "High certainty means further research is very unlikely to change confidence in the estimate. Moderate means it is likely to have an important effect. Low means it is very likely to change the estimate. Very low means any estimate is very uncertain. Rate certainty for each outcome separately."),
 ("Strength of recommendation", "A strong recommendation means most people would want the course of action and it can be adopted as policy in most situations. A conditional recommendation means most people would want it but many would not, so a decision needs discussion. Both types state the direction clearly."),
 ("Evidence to decision", "Panels consider the balance of effects, resource use, equity, acceptability and feasibility before deciding on direction and strength. The table that summarises these judgements is published with the guideline. Costs are reported in local currency where possible."),
 ("Good practice statements", "A good practice statement is used when the benefit is large and obvious and little evidence exists because researchers would never study it. Such statements are rare. They are labelled separately and do not carry a certainty rating."),
],
"who-hand-hygiene-2019": [
 ("Technique", "Apply a palmful of hand rub in a cupped hand. Rub the palms together, then the backs of the hands, between the fingers, the backs of the fingers, the thumbs and the fingertips. Continue until the hands are dry. Do not wipe or rinse after using hand rub."),
 ("Jewellery and nails", "Remove wrist watches and bracelets before patient care. A plain ring may be worn but should be moved to clean beneath it. Keep nails short, with tips less than 0.5 centimetres long. Artificial nails are discouraged because they harbour more organisms."),
 ("Training and audit", "Include hand hygiene in induction and repeat training every year. Audit compliance by direct observation twice a year in each ward. Give each ward its compliance rate and aim for a rise of 5 percentage points between audits."),
 ("Supplies", "Ensure each sink has liquid soap and single-use paper towels. Hand rub should be available at the point of care and in staff areas. Check dispensers weekly and record the check. Report any dispenser that is empty or broken within one working day."),
],
"who-hand-hygiene-2023": [
 ("Technique", "Apply a palmful of hand rub in a cupped hand. Rub the palms together, then the backs of the hands, between the fingers, the backs of the fingers, the thumbs and the fingertips. Continue until the hands are dry. For soap and water, wet the hands, lather for at least 40 seconds, rinse and dry with a single-use towel."),
 ("Jewellery and nails", "Remove wrist watches, bracelets and rings with stones before patient care. A plain wedding band may be worn but should be moved to clean beneath it. Natural nails should be less than 0.5 centimetres long and unvarnished. Chipped nail polish is not permitted in clinical areas."),
 ("Training and audit", "Include hand hygiene in induction and repeat practical training every year. Audit by direct observation every quarter in each ward and report ward rates to the executive. Give wards with less than 80 percent compliance an action plan and a re-audit within 8 weeks."),
 ("Patient and visitor involvement", "Encourage patients and visitors to clean their hands and to ask staff whether they have done so. Place posters at bedsides in the main local languages. Hand rub should be offered at the hospital entrance and at the entry to each ward."),
],
"who-ppe-2024": [
 ("Risk assessment", "Before each task ask three questions: what is the task, what is the patient's infection status and what exposure is likely. Re-assess whenever the task changes. A risk assessment form should be on each ward and be reviewed every six months and after any incident."),
 ("Masks and respirators", "A medical mask protects against droplets and splashes. A respirator filters at least 94 percent of small airborne particles and is needed for tuberculosis, measles and aerosol-generating procedures. Cloth masks are not accepted as PPE in clinical care. Replace a mask when it becomes damp."),
 ("Eye protection", "Goggles must seal around the eyes. A face shield covers the whole face. Prescription glasses are not eye protection. Clean reusable eye protection with detergent and then disinfect it after each use, and store it dry."),
 ("Supply and disposal", "Keep a reserve of at least four weeks of PPE. Dispose of single-use PPE in a yellow infectious waste container. Place PPE stations outside isolation rooms and keep one doffing area with a hand hygiene point and a waste bin."),
],
"who-respiratory-etiquette-2021": [
 ("Triage", "Screen people for cough, fever and breathlessness at the entrance. Give a medical mask to anyone with symptoms and direct them to a separate waiting area. Staff at the entrance should wear a mask and keep one metre away where possible. Record the number screened each day."),
 ("Masks", "Show people how to wear a mask: cover the nose, mouth and chin and press the metal strip to the nose. Do not touch the front of the mask. Replace it when damp, and clean hands before putting on a fresh one. A worn mask is not hung under the chin."),
 ("Ventilation", "Open windows and doors in waiting areas where this is safe. Use fans to push air out, not across other people. Aim for at least 6 air changes per hour in waiting rooms. In rooms with mechanical ventilation, maintenance checks air flow every six months."),
 ("Children and carers", "Do not require young children under 2 years to wear a mask. A carer who accompanies a child with respiratory symptoms should wear a mask. Provide a separate play area for symptomatic children. Teach children to cough into their elbow using simple pictures."),
],
"who-waste-management-2021": [
 ("Waste categories", "Infectious waste includes materials contaminated with blood or body fluids. Sharps include needles, scalpels and broken glass. Pathological waste includes tissues and organs. Pharmaceutical waste includes expired or unused medicines. Chemical waste includes disinfectants and solvents. General waste is similar to household waste."),
 ("Treatment and disposal", "Autoclave or incinerate infectious waste at a licensed facility. Never burn waste in the open air. Sharps containers are sent for treatment when sealed. Bury pathological waste in a lined pit only where no other safe method exists. Record the quantity and method of treatment."),
 ("Containers and labels", "Use leak-proof containers with lids that close tightly. Label each container with the ward and the date. Change bags when they are two thirds full. Do not compress bags by hand or by foot, and never carry a bag against the body."),
 ("Incidents", "A spill of infectious waste is cleaned up immediately using gloves and 0.5 percent sodium hypochlorite. Report any injury to waste handlers on the incident form. Review incidents every month. Provide a hepatitis B vaccine booster as advised by occupational health."),
],
}


def main() -> int:
    DST.mkdir(exist_ok=True)
    for src in sorted(SRC.glob("*.md")):
        text = src.read_text(encoding="utf-8")
        doc_id = src.stem
        extra = ADD.get(doc_id, [])
        if extra:
            text = text.rstrip("\n") + "\n\n" + "\n\n".join(f"## {h}\n{b}" for h, b in extra) + "\n"
            for h, b in extra:
                assert len(b.split()) <= 80, (doc_id, h, len(b.split()))
        (DST / src.name).write_text(text, encoding="utf-8", newline="\n")
    missing = [d for d in ADD if not (SRC / f"{d}.md").exists()]
    assert not missing, missing
    print(f"wrote {len(list(DST.glob('*.md')))} files to {DST.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
