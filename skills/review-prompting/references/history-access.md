# History access and coverage

Read this for cross-conversation reviews. Discover capabilities at invocation time; tool names and transcript storage differ between coding-agent environments.

## Retrieval order

1. Use provided transcripts or conversation references when the user selected them. Otherwise discover native conversation-list and conversation-read tools. Use their actual schemas, access checks, pagination and archived-history options. Prefer reading without resuming a conversation. A tool for Slack or Teams threads is not a Codex chat-history tool.
2. If native history tools are unavailable, check whether authorised local Codex history is readable. Determine the configured Codex data directory, using `CODEX_HOME` when set and the conventional `~/.codex` location as a candidate otherwise. Stored transcripts may be under `sessions/` and `archived_sessions/`; verify existence and actual format instead of assuming them. Enumerate candidate files before reading contents. An index or `history.jsonl` alone may omit assistant responses and outcome evidence.
3. Inspect a small transcript to understand its schema, then extract relevant user/assistant turns and outcome evidence while preserving event order and source locations. Distinguish original user messages from injected context, compaction summaries, quoted prompts, tool content and subagent messages. Deduplicate archived copies and shared fork ancestry; do not count the same incident repeatedly. Avoid dumping an entire history store into model context.
4. If neither route yields readable transcripts, proceed with the current chat or supplied messages and disclose the limitation. Request exported transcripts only if necessary to fulfil the historical portion. Do not imply that account access, a local history index or documentation proves access to every chat on other machines or hosts.

Do not read credentials or unrelated account/configuration files to obtain history. Do not bypass access controls or silently send transcripts to an external service. Use read-only retrieval; an unavailable reader does not justify launching a new server or changing the user's configuration.

## Full review and sampling

For an explicit request for all chats, enumerate and paginate all accessible in-scope sources, including archives when supported. Review in batches. Track coverage in an authorised scratch location if needed; do not claim full coverage before reading the exchanges. Report inaccessible, malformed and truncated records separately and continue with independent readable records.

If exhaustive review is impractical, explain the limitation. For a historical review with no stated extent, a reasonable starting sample is up to ten recent independent conversations within any requested period. When outcome/context metadata permits, include different task types and outcomes rather than only visible failures. Record the selection rule and any selection bias. Do not silently substitute a sample for an explicit exhaustive request; label interim findings as partial and identify the remaining scope.

For each reviewed conversation, retain a compact evidence record: source ID/location, date, task/goal, completeness, material exchanges, outcome evidence and tentative findings. Count discovered, fully reviewed, partially reviewed and excluded conversations separately; explain exclusions. Keep scratch evidence out of the shared skill package and avoid retaining unnecessary private content.

Summaries can help locate an exchange but cannot substantiate exact quotations or a missing-information claim. If only summaries remain, state the reduced evidence quality. A long conversation can be reviewed in chunks, preserving the relevant initial instructions, subsequent changes and closure. Do not claim complete coverage of omitted sections.
