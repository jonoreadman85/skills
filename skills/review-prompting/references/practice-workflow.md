# Practice setup and weekly reviews

Use this for a first full review, desktop setup or an explicitly requested weekly review. Keep the three habits short enough to glance at; they are ongoing practices, not completion checkboxes.

## First use and installation

Installation makes the skill available. The first full execution performs the review and then desktop setup. Do not add an install hook, change the generic skill installer, or create a scheduled task as an installation side effect. If the user explicitly requests a trial, a read-only review or no desktop changes, honour that scope.

Choose a private persistent practice directory outside the shared skill checkout and installation. Reuse the directory recorded in the user's task instructions; otherwise use `~/Library/Application Support/review-prompting` on macOS, requesting filesystem access if needed. If that location is unavailable, use an authorised persistent directory, disclose it, and include it in the user's saved task instructions. Store `sticky-state.json` and a small `practice-config.json` here, recording the timezone, canonical Page URL, report destination and any desktop opt-out. Keep paths, Page IDs, report URLs, excerpts and state out of the shared package. Honour a recorded opt-out instead of repeatedly offering setup.

Select three habits from the reviewed evidence. Preserve existing useful habits if there is not enough evidence to replace them; three is a display limit, not a quota of faults to invent. For an initial low-evidence review, clearly label any general practice suggestions. Keep each habit's title and action to one short line. The detailed report holds examples, exercises and reasoning.

If Pages is available, create or reuse a private **Before I prompt** Page for the canonical habits and examples using the Pages writing workflow. Do not change its sharing. For weekly reports, create or update one report per week and retain its returned URL. If Pages is unavailable, use the user's requested report format in the private practice directory, or return the report in chat; do not require a plugin or silently change an established destination.

On macOS, prepare a temporary JSON file containing three habits, then run the bundled helper:

```sh
python3 <skill-dir>/scripts/update_sticky.py --habits <habits.json> --state-dir <private-practice-dir> --dry-run
python3 <skill-dir>/scripts/update_sticky.py --habits <habits.json> --state-dir <private-practice-dir>
```

Input shape:

```json
{
  "habits": [
    {"title": "Give direction", "action": "Explain what misses and give a positive example."},
    {"title": "Replace the whole constraint", "action": "State the full new requirement and what needs updating."},
    {"title": "Verify before correcting", "action": "Ask for the calculation or evidence first."}
  ],
  "report_url": "https://example.org/your-private-report"
}
```

The example habits illustrate the format; use the user's actual review findings. `report_url` is optional and must be a real returned HTTPS link or an absolute local file URI, never the placeholder above. Prefer the latest weekly report link once available. Report links can require the user's sign-in.

The helper creates one **BEFORE I PROMPT** note or updates the matching owned note, verifies text and Float on Top, and records a receipt. It can adopt the existing note from this workflow, identified by its title and habit cue. It refuses ambiguous duplicates, unrecognised notes and later manual edits that conflict with the recorded text. Reconcile conflicts with the user; never delete unrelated notes or change an edit guard to force an overwrite. Preserve existing position and size when updating. When creating, make the note large enough for all three habits.

macOS may require Automation and Accessibility permission for the process running the helper. Use the existing permissions and respect denied access. On failure, stop desktop attempts for that run, finish the independent review/report and explain the exact remaining manual step. Do not repeatedly reopen the file picker, alter permission settings, modify the Stickies database, or claim setup succeeded without a verified receipt. On other platforms, provide the three habits in the requested local format instead. Float on Top requires Stickies to remain running; do not promise visibility in every full-screen Space.

The helper uses macOS UI automation. Initial setup is interactive; a locked, logged-out or otherwise unavailable desktop can block later updates. Keep report generation separate from the desktop update so useful work can complete without GUI access.

## Monday review

Use a local scheduled task with this skill, readable history and a stable private practice directory. A cloud-only task cannot directly update a Mac's Stickies note. Use the configured timezone, not a fixed UTC offset, so daylight saving changes do not move the review's local time. Agree a Monday time when scheduling; if only preparing a proposal, 09:00 local time is a suggested default, not an active schedule.

For each run:

1. Run `python3 <skill-dir>/scripts/week_window.py --timezone <IANA-timezone>` to compute the previous complete calendar week: Monday 00:00 inclusive through the next Monday 00:00 exclusive in the user's timezone. State the dates. Use `report_key` to identify the saved weekly report. For a later rerun, supply the original offset-bearing reference time with `--as-of` so it targets the same week, unless asked otherwise.
2. Read the previous report and practice state if available. Retrieve that week's exchanges using the history-access guidance. Use earlier turns only where needed for context; do not count earlier events as this week's achievements. Exclude subagents, shared fork ancestry and the scheduled review's own output from independent evidence. Report sampling and inaccessible records.
3. Identify concrete results visible in that week. Separate observed completion, assistant claims, user-reported outcomes and open work. Do not equate a generated document with its acceptance, a commit with deployment, or a passing test with comprehensive correctness.
4. Assess the previous three habits against relevant opportunities in the reviewed material after those habits were introduced. Use the recorded introduction dates or the actual earlier review; earlier exchanges in the same week can establish a baseline but cannot demonstrate application of a lesson not yet given. Use **Applied**, **Still practising**, **No relevant opportunity observed**, or **Insufficient evidence**. Cite specific user choices. Missing evidence is not regression. Distinguish observed practice from a claim that prompting caused a better result.
5. Choose three habits for the next week. Retain useful practices; replace one when stronger evidence supports a more valuable focus. Explain changes briefly. Do not rotate habits merely to make the report look new or declare a habit mastered after one example.
6. Save or update one dated weekly report at the established destination. Reuse the same Page or file for a rerun; check existing state before creating anything. Retain source references and report revisions where conclusions change. Update the canonical habits Page if configured, then update the existing sticky using the helper. Record report publication and sticky update as separate outcomes; a desktop failure must not erase a successful report.
7. Return a short summary and the report link, plus the three habits. State any blocked desktop update or coverage limitation. If there were no accessible relevant conversations, say so, preserve the habits and avoid invented achievements or improvement claims.

Keep the weekly report concise, normally around 300 words plus essential source references:

- **What you achieved:** up to three concrete results with outcome evidence.
- **How you applied last week's habits:** the three practices, observations and source references.
- **Your next three habits:** short actions and one small practice exercise.
- **Coverage and limits:** reviewed dates, selection, completeness and comparison limitations.

A first weekly run has no baseline unless an earlier review is actually available. Report the week's evidence and establish the baseline; do not reconstruct personal progress from memory.

## Schedule setup

Discover the current scheduled-task capabilities and follow their actual schema. Reuse a matching task when update tools permit it; avoid duplicates. Scheduling needs the user's requested scope, local Monday time, timezone, history access, report destination and private practice directory. Keep machine paths and permissions in the user's local task, not the shared skill. Do not write scheduler internals, create launch agents, or substitute hosted Page automations if the intended local scheduler is unavailable. Explain the missing setup and leave the manual weekly workflow usable.

Suggested task instructions, to adapt to the user's configured destinations:

> Use $review-prompting in weekly mode. Review the previous complete Monday-to-Sunday week in my configured timezone. Read my saved practice state and accessible coding-agent history. Report evidenced achievements and how I applied my previous three habits; distinguish claims, unknown outcomes and missing opportunities. Save one concise weekly report at my established private destination, update my canonical habits list, and refresh the existing BEFORE I PROMPT sticky note without creating duplicates or overwriting manual edits. Preserve useful habits when evidence is sparse. Return the report link, next three habits, coverage and any blocked desktop update. Never modify reviewed chats or the shared skill.

Local scheduled tasks need the computer on, the desktop app running and an available GUI session for Stickies. An accepted schedule is not proof that future desktop updates will succeed; validate the first run in the intended execution context.
