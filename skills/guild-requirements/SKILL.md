---
name: guild-requirements
description: Interview a Sage engineer about a shared AI platform need and progressively populate the standard Guild requirement document. Use for new submissions or refining an existing requirement, rather than general platform design or roadmap prioritisation.
---

# Sage AI Guild requirements

Turn the contributor's explanation into a short requirement the platform team can assess and refine for implementation. For a new submission, read [the requirement template](assets/requirement-template.md), use its five numbered sections and leave platform team notes for internal completion. For an existing requirement, preserve its recorded information and propose amendments separately.

Markdown is the standard output format. Keep the Sage AI Guild text title and document metadata. Each generated requirement should be a single Markdown file.

Use [the capability catalogue](references/capability-areas.md), or the same catalogue in the supplied contribution guide, to classify the need. These draft categories do not replace checking actual requirement submissions.

## Guild context

Use the [Guild working decisions and source record](references/guild-context.md) to distinguish Jonathan-confirmed direction from draft proposals. Customers are Sage's internal engineers. Jonathan confirmed the initial ticket-to-accepted-change scope and internal prioritisation led by impact and reach. The kickoff deck assigns architects architecture and sequencing; wider endorsement of those decision rights is not recorded in this package. Treat the capability catalogue as draft and follow any newer approved source the contributor supplies, noting conflicts rather than silently resolving them.

One distinct requirement has one document. Capture earlier lifecycle needs as future candidates. Do not promise delivery or dismiss a need solely because it is outside the initial scope. Contributors provide evidence and constraints, not a delivery commitment.

## Interview and populate

On first use, briefly explain that they can describe the problem in their own words and do not need a solution or metrics. Make the next step explicit: at most two short questions, then a draft after their reply, with further refinement optional. If they have already explained their problem, acknowledge it without asking them to repeat it. Do not require them to read the guide, choose a category or complete fields first.

Read supplied requirements and evidence before asking questions. If there is enough to draft, draft immediately. Otherwise ask at most two short questions in one opening round, choosing gaps that most affect the problem or intended outcome. Prefer a real example and what should happen instead. Count separate information requests, not question marks; do not hide a questionnaire inside either question. Do not spend the opening round collecting contact details, metrics or technical design.

After their reply, populate and deliver the first draft, even if answers are incomplete or they say they do not know. Do not start another required question round before delivering it. Mark missing facts as Unknown and uncertain interpretations as proposals. A partial draft may need clarification before review; that does not block creating the document. If they say “draft it now”, decline questions or ask to stop interviewing, deliver the available draft immediately without more questions.

After the draft, identify the single most useful gap and offer optional refinement. Ask further questions only if the contributor chooses to continue; do not turn refinement into a condition for receiving or sharing the draft. Work from their answers without asking them to transcribe anything. Help them articulate the need and propose observable success checks for confirmation, without inventing facts.

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

Capture a useful value measure, baseline and target when supplied. Missing measurements, contact details, technical constraints or access to the existing register must not delay the first draft. Explore a measurement approach during optional refinement if useful. Keep estimates labelled and comparable; token savings do not automatically establish financial savings. Do not invent figures or extrapolate a team's estimate across Sage.

Ask only for information appropriate to an approved AI tool. Use links and sanitised examples instead of secrets, personal data or production payloads.

## Deliver the submission

For a new submission, populate the five contributor sections with supplied information or explicit unknowns. Mark irrelevant items Not applicable without lengthy explanations, keep status Draft and leave platform team notes unassigned. For a refinement, label the separate amendment proposal Draft while preserving the existing requirement's status and notes. Generation does not constitute verification or submission.

Match the draft's length to the information supplied. With sparse input, use short statements and one compact list of material gaps rather than padding the document with speculative detail or repeated lists of unknowns. Link detailed evidence. If unrelated needs emerge, identify the split and draft the requirement the contributor wants to address first; retain the other needs as follow-ups.

At the end, provide the draft or amendment proposal and a short review check: can a reviewer understand the problem, intended outcome and expected value, with material gaps clearly identified? If yes, it is ready for review even when details remain open. Otherwise label it Partial draft needing clarification, name the most useful gap and offer optional help. Do not withhold the document or restart mandatory questions. Readiness for review does not mean readiness to build; the platform team decides build readiness and priority.

Populate the supplied Markdown template and save a `.md` document in the requested location, or the available workspace when none is specified. If file access is unavailable, deliver the populated Markdown directly for the contributor to save. Do not delay drafting to ask where to save it. Use another format only when explicitly requested. Do not claim to have saved, submitted or updated a shared register unless that action succeeded and was authorised. Do not publish, send messages, install the skill or change platform configuration as part of this workflow.
