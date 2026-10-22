# Maintaining the shared hiring skill

## Source and installation

Authoritative repository: `https://github.com/jonoreadman85/skills`.
Skill path within it: `skills/hiring-assessment`.

The folder loaded by Codex is often an installed copy. Check whether the working folder is actually part of the authoritative repository, using its Git root and remote. A matching filename or folder name is not sufficient. Prefer a known source checkout in the current workspace or user-provided location; do not scan unrelated projects for one.

If the checkout is unavailable, clone it into an appropriate working location when access and the task allow. Otherwise prepare a reviewable patch or replacement reference in the user's working area and explain what remains to publish. Do not silently edit an installation and report the shared skill updated. Candidate packs belong outside either skill copy.

## Prepare the update

Compare the supplied source with the current reference and source register. Preserve unrelated content and existing user edits. State material differences and distinguish explicitly adopted changes from proposals or unresolved conflicts. Ask only for a decision that affects the update; continue preparing unaffected changes. Keep the last resolved guidance in force for disputed sections and identify the pending change.

Edit the source checkout. Advance a playbook revision only for applied playbook changes; record source name/link, version/date, sections or slides, and content hash for local files. Do not change source-document hashes when only editing the method. Existing candidate packs retain their original playbook revision unless a refresh is requested.

Validate changed frontmatter and reference links, check the diff for candidate data and unintended changes, and use focused synthetic scenarios when changing behaviour. Run the skill-creator validator if available; do not claim behavioural verification from a syntax check alone.

## Publish and refresh

Use the publication scope already authorised in the conversation. When publishing is authorised, commit and push the reviewed changes or use the requested PR workflow. Otherwise finish the local patch and identify publication as outstanding. Do not change repository visibility or collaborators as part of an update.

Record the source commit and verify that the intended remote branch contains it. Update an installed copy only if requested or already authorised. Before replacing files, check for local divergence; preserve any edits rather than blindly overwrite them. If no prior baseline is available and contents differ, compare them and resolve the intended changes first. Refresh only this skill, and verify its contents match the chosen source version. Installer tools may refuse an existing destination; do not delete that destination to force a reinstall.

Report separately: source prepared, remote published, local installation refreshed, and any unresolved policy question. Consumers need to update their own copies; one push does not synchronise every colleague's installation. A newly refreshed skill is available on the next turn.
