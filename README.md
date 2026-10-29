# Department skills

Reusable Codex skills maintained by Jonathan Readman for sharing across the department. Each skill is a self-contained folder under `skills/`. Candidate data, private conversation history and working assessment outputs stay outside this repository.

## Available skills

- [Hiring assessment](skills/hiring-assessment/SKILL.md): assess CVs against role requirements, prepare interviews, review interview evidence and maintain playbooks. Works across roles and levels. Repository context is optional. Includes an AI engineering pilot snapshot; that snapshot is not universal hiring policy.
- [Review prompting](skills/review-prompting/SKILL.md): review prompting across accessible coding-agent conversations, distinguish user choices from agent or tool failures, and teach improvements with evidence, rewrites and practice exercises. Supports single-prompt trials, first-use macOS sticky-note setup and weekly achievement/practice reports.

## Install and use

In Codex, ask the skill installer:

> Use $skill-installer to install skills/hiring-assessment from jonoreadman85/skills.

For the prompting review skill:

> Use $skill-installer to install skills/review-prompting from jonoreadman85/skills.

> $review-prompting Review my accessible Codex conversations from the past month. Explain coverage, identify the most consequential prompting patterns and give me practical lessons.

> $review-prompting Review this prompt as a single-message trial. Do not infer recurring habits or historical outcomes.

The prompting skill uses available conversation tools, readable local transcripts or supplied exports. Installation does not grant access to history or guarantee coverage of all machines and hosts. It does not modify reviewed conversations or publish their contents.

On the first full review, the skill creates or adopts one **Before I prompt** sticky note on macOS and keeps setup state outside the package. Single-prompt trials and read-only reviews skip desktop setup. Accessibility and Automation access may be needed; a blocked desktop update does not prevent the report. Installation itself runs no setup or scheduler hook.

> $review-prompting Run my weekly review for the previous complete Monday-to-Sunday week. Report evidenced achievements, assess my previous three habits, and update my existing sticky note. Keep the report concise and explain coverage.

For Monday scheduling, configure a local task with the user's timezone, history access, private practice directory and report destination. Scheduling is separate from installing the skill; the computer and desktop app must be running, with an available GUI session for the sticky update. See [practice setup and weekly reviews](skills/review-prompting/references/practice-workflow.md). The package includes a calendar-week helper and a guarded sticky updater, not a background service.

Weekly reviews capture their original habit baseline before assessment. Stable habit IDs preserve introduction dates through wording changes; reruns reuse the captured baseline and report rather than assessing the week against newly selected habits. Report history is retained independently of desktop-update success.

Private repository installation requires GitHub access. Installing a skill does not grant access to candidate documents or source slides. After installation, start a new chat if the skill is not yet listed.

Example requests:

> $hiring-assessment Assess the attached CVs against this job description. Keep eligibility, level evidence and interview recommendations separate.

> $hiring-assessment Prepare an interview for this candidate using the AI engineering pilot at the advertised Mid level.

> $hiring-assessment Assess this candidate for the attached leadership role. Use the supplied interview guidance rather than the AI engineering pilot.

> $hiring-assessment Update the AI engineering playbook from these revised slides. Explain the substantive changes and unresolved conflicts.

Inputs can be attachments, pasted material, accessible files or supported connected sources. No dedicated project folder or code checkout is required by the skill. Start with the role brief and candidate evidence; ask for a repository only when it adds relevant context.

## Maintaining skills

Edit the repository copy and review changes before sharing them. Keep each skill's entry point concise, with substantial role-specific guidance in linked references. Record source and revision information when updating a playbook. Do not present pilot proposals as adopted departmental policy.

Consumers need to refresh their installed copies after changes are merged. Repository edits do not automatically refresh every colleague's installation. Record the playbook revision in generated interview packs so earlier decisions remain interpretable.

The hiring skill's [maintenance workflow](skills/hiring-assessment/references/maintenance.md) distinguishes the source checkout from installed copies. Updates are prepared in this repository, published within the authorised scope, and then applied to installations after checking for local edits. The installer refuses an existing destination; preserve local differences instead of deleting a skill to force reinstallation.

## Scope of this first version

The hiring method is derived from the existing hiring discussions. The AI engineering reference is extracted from the proposal deck, candidate scenario deck and interviewer guide reviewed on 22 October 2026. It includes the process and exercise summaries, not the source binaries or a runnable practical environment. It has not yet been validated through a live hiring pilot.

The repository starts private. Sharing the URL does not grant access; colleagues require repository access. No collaborators or teams are added automatically.
