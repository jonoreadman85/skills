# Department skills

Reusable Codex skills maintained by Jonathan Readman for sharing across the department. Each skill is a self-contained folder under `skills/`. Candidate data and working assessment outputs stay outside this repository.

## Available skills

- [Hiring assessment](skills/hiring-assessment/SKILL.md): assess CVs against role requirements, prepare interviews, review interview evidence and maintain playbooks. Works across roles and levels. Repository context is optional. Includes an AI engineering pilot snapshot; that snapshot is not universal hiring policy.

## Install and use

In Codex, ask the skill installer:

> Use $skill-installer to install skills/hiring-assessment from jonoreadman85/skills.

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
