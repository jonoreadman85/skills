# AI engineering interview pilot

Revision: 2026-10-22.1

Status: extracted snapshot of a pilot proposal. The hiring manager approved preparation of the proposal; the deck still requests pilot endorsement and review before wider adoption. Do not describe it as established department policy.

Scope: Gateway, Governance, Evals and Insights engineering roles at Junior, Mid, Senior and Principal levels. Principal people leadership is specific to this role design, approximately 70% technical and 30% leadership. Other disciplines and Director roles require their own expectations.

## Purpose and competencies

Assess practical delivery, production judgement, verification, trustworthy evidence and observable collaboration. Strong foundations matter more than memorised vendor tools. Assess foundations and implementation; problem framing and design; production safety and improvement; verification and AI judgement; evidence quality; collaboration and ownership. Add coaching, development, planning and delegation for the Principal role described here.

For Governance, the subsequent hiring brief favours full-stack engineers who can contribute to backend work when UI demand is lower. Frontend and backend leanings may complement each other. Do not turn this preference into a requirement for every team or assume a particular frontend framework is mandatory.

## Stages and durations

Publish preparation and tool rules before assessment. Start with 30 minutes of independent reasoning and 60 minutes of practical work with AI, with a break between them. Review that evidence before scheduling the remaining sessions. A clear level mismatch can end the process promptly; one unfamiliar detail or isolated error is insufficient on its own.

- **Junior and Mid:** 90-minute practical stage; 45 minutes production and improvement (including design); 45 minutes collaboration and ownership. Total assessment time: 180 minutes.
- **Senior:** 90-minute practical stage; 45 minutes architecture and design; 45 minutes production and improvement; 60 minutes collaboration and ownership. Total: 240 minutes.
- **Principal:** 90-minute practical stage; 60 minutes architecture and design; 60 minutes production and improvement; 45 minutes coaching and development; 45 minutes planning and partnership (including collaboration). Total: 300 minutes.

Times include introductions and candidate questions. Recruiter calls and breaks add to elapsed time. No session exceeds 60 minutes without a break. Interviewer assignment remains the hiring manager's judgement, not a fixed panel requirement. Target a stage outcome within five working days. Additional assessment needs a named evidence gap and agreed time limit.

Suggested first-portion allocation: 5 minutes context, 15 investigation, 5 follow-up and 5 candidate questions. Suggested implementation allocation: 5 minutes brief, 40 implementation, 10 verification/explanation and 5 candidate questions. These are pilot allocations, not universal optimal durations.

## Candidate preparation and AI rules

Explain stages, timings, competencies and permitted tools in advance; give a representative example and practice environment with the same supported assistant/model configuration. Recruiting handles accommodations and scheduling. Include the ownership opportunity and candidate questions.

Documentation is available in both practical portions. The first portion requires independent explanation and diagnosis without AI. The second permits the supplied assistant for a bounded change. Pause assistant use for direct explanations of decisions or results. Assess understanding, inspection and verification alongside the working result. Use synthetic data and mock services without production credentials.

## Levels and rating anchors

- **Junior:** explains their work, makes sound progress with guidance, tests basics and learns from feedback.
- **Mid:** independently delivers a bounded change through release, including common failures and monitoring.
- **Senior:** owns ambiguous work through production, balances trade-offs and enables others.
- **Principal:** sets direction across the group, handles consequential decisions and develops the people delivering the work.

Apply ratings at the advertised level: **1** substantial gap after clarification; **2** partial capability with material gaps or excessive support needs; **3** meets required scope, judgement and independence; **4** exceeds expected depth or scope with convincing evidence. **Not observed** means inadequate evidence, not a low score. Record hints and clarification.

Independent evidence and scores precede debrief. Use a competency profile rather than an average. Principal candidates must meet both technical and leadership expectations. Investigate serious production-safety, understanding or collaboration concerns with specific observations and follow-up. Avoid impression-based single-interviewer vetoes. Decision options are hire, no hire or insufficient evidence, with the final decision human-led. Consider another level only with an appropriate vacancy and candidate interest.

## Practical exercise options

These are briefs requiring a prepared mock environment and internal dry-run. They are not executable assets in this skill. Select an equivalent core exercise for candidates assessed against the same role and level; use follow-ups for additional depth.

### Gateway: retry handling

A mock gateway retries every failure three times and loses useful errors. Improve failure handling while preserving the overall deadline and cancellation. Supply provider semantics, fake clock, synthetic responses and a test runner. No retry is permitted after streaming begins in the core exercise.

Look for permanent/transient classification, bounded retries within the deadline, cancellation, useful errors and tests for success, permanent failure, repeated transient failure and cancellation. Probe duplication ambiguity, retry amplification, safe telemetry and release consequences at higher levels. Do not require memorised vendor SDK behaviour.

### Governance: authorisation and truthful UI

A signed-in user can edit another team's policy. Add server-side authorisation and useful audit evidence; show a truthful outcome when save fails. Supply two identities, plain-language permission rules, policy store, audit sink and a simple UI or client. Use an appropriate full-stack variant when the role calls for it.

Look for authorising the authenticated actor against the target resource, no unauthorised mutation, actor/target/version/correlation evidence, confirmed UI outcomes, cross-team and concurrency tests, and an explicit rule for audit-delivery failure. Probe version conflicts, durable audit delivery, duplicate submissions and lost responses without imposing one implementation.

### Evals and data: repeatable aggregation

A dashboard overcounts active users due to retries and mishandles late events. Supply a small SQL or dataframe environment with synthetic event_id, task_id, attempt_id, user_id, team_id, event_time, ingestion_time, event_type and schema_version; define the time zone and eligibility rules.

Look for explicit event grain, deduplication, attempts distinguished from tasks, valid windows/denominators, late-arrival correction, reproducibility and reconciliation tests. Probe contracts, backfills, freshness, coverage and metric interpretation. Data-engineering depth should concern pipelines rather than frontend skill.

## Shared discussion and calibration

Candidate discussion slides 2–5 contain prompts and diagrams without answer notes. Keep internal calibration answers separate from candidate preparation. Equivalent valid reasoning is acceptable.

- **Gateway production:** a routing release precedes latency and provider errors before complaints. The guide supplies synthetic p95 rising from 2.0 to 8.4 seconds and errors from 1% to 8%. Probe segmented signals, containment, safe rollback, recovery evidence and prevention. Fallback must preserve the stated policy constraints.
- **Governance revocation:** the UI confirms revocation but gateway decisions remain cached for ten minutes. Probe enforcement boundaries, identity/resource/version diagnosis, containment, propagation requirements, failed invalidation and availability trade-offs. UI success alone does not prove effective revocation.
- **Evals quality:** before, easier tasks pass 320/400 and harder 240/600; after, 600/800 and 70/200. Overall improves 56% to 67%, but subgroup rates fall 80% to 75% and 40% to 35%. Weighting after rates to the old mix gives 51%; this is descriptive, not causal proof. Probe representative comparisons, stable scoring, uncertainty and rollout criteria. All figures are synthetic.
- **Adoption evidence:** active-user growth does not establish an equal productivity gain. Probe eligible population, duplicates, missing/late events, task mix, outcomes, freshness and reproducibility.
- **Inherited architecture:** discuss what to stabilise, extend or replace using observed incidents, requirements, migration risk, ownership and rollback rather than preference for a rewrite.
- **Collaboration:** use an actual disagreement and a reliability-versus-launch scenario. Probe the candidate's actions, partner perspective, decision authority, options and outcome rather than confidence or personality similarity.
- **Principal leadership:** a strong engineer bypasses agreed controls; an engineer seeks promotion through longer hours; planning must balance reliability, deadlines, integrations and coaching. Look for specific feedback, inquiry, fair opportunities, clear expectations, delegated authority, capacity, follow-through and proportionate escalation.
- **Governance UI:** double save, failed response and concurrent edits. Probe pending/error/success states, retaining input, conflicts, lost-response ambiguity, accessibility and server-side enforcement.

At Junior level, investigate sound progress and response to guidance; Mid, bounded independence; Senior, production trade-offs and safe delivery; Principal, standards, cross-team consequences and developing others. Do not use a Principal checklist to reject Junior candidates.

## Assessment record and pilot review

Record candidate, role/level, session, interviewer, date and playbook revision. For each assessed competency record direct observations, follow-ups, hints/support and rating. Identify missing evidence and next action. Record the recommendation and specific rationale. Preserve interviewer records before debrief; do not infer capability from accent, institution, confidence or similarity to the existing team.

Before candidate use, agree the pilot owner, initial batch size and review date; prepare exercises and dry-run them with scoring calibration. Review actual time, withdrawals, feedback, scoring disagreement and inconclusive exercises. Compare interview evidence with performance/development at three and six months. A small pilot can reveal defects but does not establish predictive validity. Avoid rejection-rate targets.

## Source register and maintenance

Extracted on 22 October 2026 from the following local originals. Filenames are identifiers, not reachable shared links. Original binary files are not bundled. Provide the revised source or configure an accessible departmental source link when refreshing this snapshot.

- `AI_engineering_hiring_proposal.pptx`, slides 2, 5–8 and 13–17: purpose, levels, stages, timings, AI rules, Principal leadership, scoring and pilot. SHA-256: `71933690d2f15c0b16ea99582bf903b426789211d6bb0e64190d89ed772d69f0`.
- `Candidate_discussion_scenarios.pptx`, slides 1–5: candidate-facing scenario scope and synthetic evaluation figures. SHA-256: `680fd8808fa18594ae9c3b7b963ce9f00be27035a0a40640e8eec1696e48906a`.
- `AI_engineering_interviewer_guide.docx`, sections How the process works; Scoring and level expectations; P1–P3; F1–U1; Assessment record and debrief: detailed execution and calibration. SHA-256: `0583165edb3e130d8e863fda6668b6883c356afb6de016bfa0fdbd87883af30c`.
- Hiring-manager clarification in the subsequent CV-review discussion: Governance should favour full-stack capability rather than a dedicated UI position. This is role context, not a change to the interview-loop durations.

The source materials cite external company practices as influences. This snapshot does not assert that those companies currently use a particular process or that the proposed process guarantees better hiring outcomes.
