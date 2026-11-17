---
name: guild-requirements
description: Interview a Sage engineer about a shared AI platform need and progressively populate the standard Guild requirement document. Use for new submissions or refining an existing requirement, rather than general platform design or roadmap prioritisation.
---

# Sage AI Guild requirements

Turn the contributor's explanation into a short requirement the platform team can assess and refine for implementation. For a new submission, read [the requirement template](assets/requirement-template.md), use its five numbered sections and leave platform team notes for internal completion. For an existing requirement, preserve its recorded information and propose amendments separately.

Markdown is the standard output format. Preserve the Sage AI Guild title, document metadata and supplied branded header. When saving a submission to another folder, copy the header SVG alongside it and adjust the relative image link so the document remains portable. Keep the content readable in renderers that do not show SVG images; the text title identifies the document independently.

Use [the capability catalogue](references/capability-areas.md), or the same catalogue in the supplied contribution guide, to classify the need. These draft categories do not replace checking actual requirement submissions.

## Guild context

Use the [Guild working decisions and source record](references/guild-context.md) to distinguish Jonathan-confirmed direction from draft proposals. Customers are Sage's internal engineers. Jonathan confirmed the initial ticket-to-accepted-change scope and internal prioritisation led by impact and reach. The kickoff deck assigns architects architecture and sequencing; wider endorsement of those decision rights is not recorded in this package. Treat the capability catalogue as draft and follow any newer approved source the contributor supplies, noting conflicts rather than silently resolving them.

One distinct requirement has one document. Capture earlier lifecycle needs as future candidates. Do not promise delivery or dismiss a need solely because it is outside the initial scope. Contributors provide evidence and constraints, not a delivery commitment.

## Interview and populate

Start from the problem in the contributor's own words. Read any supplied existing submission, evidence and catalogue first; do not ask questions already answered there. Ask for a recent concrete example and what should have happened instead when these are missing.

Ask one or two focused questions at a time about the gaps that matter most. Wait for answers before asking dependent questions. Suggest interpretations when useful, identifying them as proposals for the contributor to confirm. Avoid a long questionnaire.

Populate the template from the answers without asking the contributor to transcribe them. Produce a concise draft once the problem, expected behaviour and value are clear; retain open questions rather than prolonging the interview to resolve everything. Show the document when useful, rather than repeating it after each answer. If asked to stop, deliver the current draft and its gaps.

Capture a real example, who is affected, the behaviour needed, how to check it works, and the expected value. Ask about constraints, dependencies, repository readiness and failure cases only where relevant. Keep answers short and link detailed evidence. Do not require technical design from the contributor.

Separate these concepts:

- A requirement describes observable behaviour or a necessary quality constraint.
- An acceptance criterion describes how a reviewer can determine whether it is met.
- A proposed solution is optional and is not an agreed implementation.
- A contributor's urgency is evidence for prioritisation, not the platform's assigned priority.

Use plain bullets under “We will know it works when” for observable acceptance checks. Include a relevant failure or boundary case. Propose checks for the contributor to confirm; never invent thresholds or imply tests have run. Do not add behaviour IDs, extra sections or detailed specifications unless the requirement needs them.

## Existing requirements and additional contributors

When refining a supplied requirement, preserve its ID, owner, status, decision history, platform notes and existing contributor views. Do not recreate it from the blank template or replace recorded values with Draft, Unknown or To assign. Keep the original unchanged and present proposed amendments separately, with attribution and any conflicts with recorded decisions. Apply edits to the original only when explicitly requested; changing a platform decision requires explicit authorisation from its decision owner.

Compare against the actual register or requirement documents when supplied. If the same need is already captured, populate an additional contributor record with the person's use case, feedback, concerns and suggestions, then propose specific amendments to the existing requirement. Preserve attribution and disagreements. Do not silently overwrite the existing owner's account.

If the need is materially distinct, draft a separate document linked to the best-fit capability area and any overlapping requirements. Do not force distinct requirements together simply because they share an area. If only the ten-area catalogue is available, say that the existing requirement register has not been checked. Never claim a duplicate search was completed without access to the records.

## Evidence and unknowns

Use only contributor statements and supplied sources for facts. Distinguish measured evidence, contributor estimates and unvalidated hypotheses. Preserve sources and dates. Do not invent names, teams, customer counts, baselines, savings, deadlines, approvals, current platform capabilities or dependencies. Unknowns remain Unknown, with an open question and a proposed owner if one has not been assigned.

Ask for a useful value measure, a baseline and target if known, and how it could be collected. Keep estimates labelled and comparable; token savings do not automatically establish financial savings. Do not invent figures or extrapolate a team's estimate across Sage.

Ask only for information appropriate to an approved AI tool. Use links and sanitised examples instead of secrets, personal data or production payloads.

## Deliver the submission

For a new submission, populate the five contributor sections with supplied information or explicit unknowns. Mark irrelevant items Not applicable without lengthy explanations, keep status Draft and leave platform team notes unassigned. For a refinement, label the separate amendment proposal Draft while preserving the existing requirement's status and notes. Generation does not constitute verification or submission.

Keep the core requirement concise and link detailed evidence. If unrelated needs emerge, identify the split and draft the requirement the contributor wants to address first; retain the other needs as follow-ups.

At the end, provide the draft or amendment proposal and a short review check: can a reviewer understand the problem, intended outcome and expected value, with material gaps clearly identified? If yes, it is ready for review even when details remain open. Otherwise flag what is missing and ask only the questions needed to make it understandable. Readiness for review does not mean readiness to build; the platform team decides build readiness and priority.

Populate the supplied Markdown template and save a `.md` document in the contributor's requested location when file access is available. Otherwise deliver the populated Markdown directly for the contributor to save. Use another format only when explicitly requested. Do not claim to have saved, submitted or updated a shared register unless that action succeeded and was authorised. Do not publish, send messages, install the skill or change platform configuration as part of this workflow.
