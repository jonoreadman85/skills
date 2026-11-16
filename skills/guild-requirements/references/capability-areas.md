# Sage AI Guild capability catalogue

These ten areas summarise the kickoff deck draft v0. The expected value and questions below are prompts for review. The proposed mechanisms remain subject to requirements and architectural assessment; these entries are not complete or accepted specifications.

### AREA 01 Work intake and orchestration

**Purpose:** Coordinate an authorised task through a traceable workflow, including interruption and failure handling.

**Expected value:** Reduce manual handoffs and make incomplete work recoverable.

**Draft assumptions:** The kickoff proposes Jira intake, durable workflows, pause, resume, cancel, bounded retries and owned failure handoffs.

**Open questions:** Which task types and handoffs matter first? Who takes ownership when a run cannot continue?

### AREA 02 Evaluations per repository

**Purpose:** Assess agent performance against representative work for each repository.

**Expected value:** Give teams evidence that changes remain useful and meet their quality expectations.

**Draft assumptions:** The kickoff proposes historical golden tasks, a baseline, scorecards and gates for changes to models, prompts, harnesses and context.

**Open questions:** What representative tasks exist? What evidence and thresholds would make the team confident, including where historical tasks are unavailable?

### AREA 03 Agent identity and access

**Purpose:** Control and attribute the actions an agent is authorised to perform.

**Expected value:** Enable useful access with accountability and limited exposure.

**Draft assumptions:** The deck proposes per-run identity and short-lived scoped access. The AI-generated summary records delegated versus independent identity as an open question.

**Open questions:** What must run on behalf of a user or using an agent identity? Which scopes, attribution and revocation behaviour are required?

### AREA 04 Context and memory

**Purpose:** Provide relevant repository and work context, and retain appropriate state across a task.

**Expected value:** Reduce repeated explanation and lost progress while respecting source permissions.

**Draft assumptions:** The kickoff proposes repository instructions, Jira and document context, run journals and human approval of curated learning.

**Open questions:** Which sources are essential? What can persist, who can read it, and how should stale or incorrect context be corrected?

### AREA 05 Secure execution

**Purpose:** Run agent work in a controlled execution environment.

**Expected value:** Allow engineers to execute useful tasks while containing access and changes.

**Draft assumptions:** The kickoff proposes single-use sandboxes, approved images, restricted egress, governed package access and no long-lived secrets.

**Open questions:** What build tools, packages, network access and environments do real repositories require? Which restrictions would block useful work?

### AREA 06 Policy and guardrails

**Purpose:** Apply platform and team controls to agent actions and allow intervention.

**Expected value:** Support different team needs within common boundaries.

**Draft assumptions:** The kickoff proposes configuration as code, progressively tighter controls, protected-path approvals and a kill switch.

**Open questions:** Which controls are mandatory? Where do teams need configuration, approvals or an emergency stop, and who owns those decisions?

### AREA 07 Agents and models

**Purpose:** Support suitable agent roles and models for different tasks.

**Expected value:** Balance task quality, compatibility and consumption.

**Draft assumptions:** The kickoff proposes plan, code, test and fix roles, a pluggable harness, gateway routing and team or task budgets.

**Open questions:** Which existing workflows need reuse? What capability, model and budget constraints matter for each use case?

### AREA 08 Visibility and collaboration

**Purpose:** Let engineers understand runs, respond to questions and inspect evidence and consumption.

**Expected value:** Reduce uncertainty and make intervention and improvement easier.

**Draft assumptions:** The kickoff proposes Slack questions, evidence on pull requests, cost and usage insights and an audit of actions.

**Open questions:** Where must teams receive and answer questions? What evidence and visibility do contributors and support teams need?

### AREA 09 Review verification and merge

**Purpose:** Verify proposed changes and authorise their acceptance.

**Expected value:** Give teams confidence that the change they accept is the change that was checked.

**Draft assumptions:** The kickoff proposes checks against the exact revision, specialist reviewers, independent merge authorisation, human approval by default and post-merge monitoring.

**Open questions:** Which checks and approvals are needed? What happens when the revision changes or trusted checks fail?

### AREA 10 Onboarding and readiness

**Purpose:** Help teams prepare repositories and start using the platform successfully.

**Expected value:** Make adoption achievable across different stacks and levels of repository maturity.

**Draft assumptions:** The kickoff proposes manual then self-service onboarding, readiness-based autonomy and reduced autonomy after regressions.

**Open questions:** What prevents onboarding today? Which readiness actions belong in team backlogs, and what guidance or platform support is needed?

### Shared constraints and missing requirements

Record relevant isolation, residency, retention, availability and cost constraints in each submission. The kickoff notes identify these as non-functional needs to develop separately. Propose a new area when no existing area fits; link overlaps rather than duplicating them.

### Sources

Verity Agent Guild Kickoff, slides 2 to 5 and speaker notes; ai_guild_kick_off_sumary.rtf, which is AI-generated and requires verification; Jonathan's Guild discovery discussion on 15 November 2026. Purpose, value and question wording in this catalogue is drafted for review.
