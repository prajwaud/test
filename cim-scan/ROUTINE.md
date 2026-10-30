# Friday routine - setup instructions

## Status 2026-10-30: the routine must be recreated in the claude.ai Routines UI

The live trigger `trig_01C28o3A7NuVZduR2y25eRBq` still wakes the original build session
(`session_01CpAPLfUBnGE9ScCuVGHS8E`) every Friday. That session only ever held the old
"Knowledge Vault Documents" connector, which AIVC retired on 2026-10-15 when it renamed
the connector "Knowledge Vault". So the Oct 16, 23 and 30 runs could not scan and sent
Prithvi an alert instead. The CHANGELOG entry of 2026-10-23 says the Routine was moved to
a new session each run; it was not - the trigger still reused the old session on Oct 30.

A routine created by Claude from a session can only pass on the connectors that session
holds. Tried on 2026-10-30 from the build session: the new routine stored no connectors
at all, so it was deleted. A fresh-session routine with the right connectors has to be
created by Prithvi in the claude.ai Routines UI:

1. claude.ai > Code > Routines > New routine.
2. Repository: prajwaud/test. Model: Sonnet (Prithvi, 2026-10-23).
3. Connectors: Knowledge Vault, Microsoft 365, CUBE. Without Knowledge Vault the run
   can only send the alert.
4. Schedule: Fridays 6:30am ET, a new session each run.
5. Prompt: paste the block below.
6. Once it is saved, turn off or delete "AI-in-CIMs weekly digest - Friday 6:30am ET"
   (trig_01C28o3A7NuVZduR2y25eRBq), or both will fire and the old one will send a
   duplicate alert.

```
Friday AI-in-CIMs digest run (scheduled, unattended - no human is watching; never wait on a permission prompt, and if a tool call prompts, abandon it, finish by another route and name the call in the summary).

Setup: work from the prajwaud/test repo on main (git fetch origin main; git checkout -B main origin/main). The procedure lives in that repo and is the authority over this prompt: read cim-scan/SCAN.md, cim-scan/DIGEST.md, cim-scan/CHANGELOG.md and cim-scan/state.json before doing anything else. For delivery you also need the outbox repo Waud-Capital/WCP-PR-OS (formerly prajwaud/WCP-PR-OS): attach it with add_repo (access push) and clone it with plain git clone. Never call register_repo_root.

Then, in order:
1. Harvest replies to the most recent digest per DIGEST.md step 0a (outlook_email_search, subject contains "Weekly AI-in-CIMs scan"). Apply factual corrections to notes; procedure changes only if from Prithvi (praj@waudcapital.com); open the digest with the "From last week's replies" block only if there was feedback.
2. Catch-up scan per SCAN.md using the "Knowledge Vault" document connector (search_evidence; doc_type lowercase "cim"; filter_fallback guard with its empty-window nuance; never recall_user_context; never query_structured on the kv space), deduped against state.json, plus the CUBE receipt cross-check in SCAN.md step 1.4. If the Knowledge Vault connector is not available in this session, do not send a digest: queue the short alert to Prithvi alone (outbox file named cim-digest-YYYY-MM-DD.json) and leave state.json's last_digest_at unchanged.
3. Pre-flight per DIGEST.md, including the zero-CIM alert and the backfill guard (more than ~10 notes in the window: digest the most recent cohort and propose a separate backfill report).
4. Assemble per the DIGEST.md template: AI-GENERATED banner first, purpose paragraph, factual lead item with inference confined to the Read line, tiers descending, empty sections omitted, portco claims traced to Vault documents or the KB (never the reference digest), no em-dashes, then the feedback line, the required footer and the firm-wide automated-generation notice verbatim.
5. Deliver per DIGEST.md transport: Claude never sends. Write the email to outbox/cim-digest-YYYY-MM-DD.json in WCP-PR-OS (recipients praj, drassner, rwaud2; alerts go to praj alone), push it, then commit and push notes and state.json to prajwaud/test main. Never call outlook_send_mail or outlook_send_draft, and do not create an MCP draft (that interim step is retired). Confirm the send receipt appears in WCP-PR-OS outbox/sent/ before reporting it sent.
6. End with the run summary: n scanned, m noted, lead or none, queued and receipt status, guards fired, CUBE rows not yet searchable, feedback items processed.
```

The history below is kept for context.

## Status 2026-08-27: routine is LIVE

Trigger `trig_01C28o3A7NuVZduR2y25eRBq` fires every Friday at 10:30 UTC (6:30am ET on
daylight time; 5:30am ET after clocks change - adjust to `30 11 * * 5` in November if
the hour matters) into the build session, which holds the Knowledge Vault Documents and
Microsoft 365 connectors. Each run: harvest reply feedback (DIGEST.md 0a), catch-up
scan, pre-flight checks, assemble, send to praj@waudcapital.com only, commit and push.
Distribution expands to Doug Rassner and rwaud2 only on Prithvi's explicit say-so.

Two caveats, both checked on the first firing (2026-08-28):
1. Whether the session-bound wake carries the connectors is [Likely] but unverified -
   the trigger system stores no connector grants of its own. If no email (digest or
   zero-CIM alert) arrives by ~7:00am ET Friday, the fallback is the UI-created routine
   below.
2. SETTLED 2026-08-28: M365 MCP send ALWAYS requires Prithvi's manual approval click -
   confirmed on the verification run and again on the inaugural send, with the
   .claude/settings.json allowlist in place. Claude does not send. Transport is the
   outbox: the Friday run writes the finished email to `outbox/` and pushes; GitHub
   Actions (`send-outbox.yml`) delivers it via app-only Graph with no human. Until the
   Entra credentials exist as Actions secrets, the workflow no-ops and the interim is
   an MCP draft plus Prithvi's one click, per DIGEST.md delivery.

The original UI-based setup below stands as the fallback path.

---

The weekly digest needs a scheduled routine that fires a fresh Claude session with the
Knowledge Vault Documents and Microsoft 365 connectors attached.

**Why it is not already scheduled:** a trigger was created programmatically on 2026-08-26
and immediately deleted. Triggers created from inside a session in this org store no MCP
connectors, so the sessions they fire wake up without KV retrieval or Outlook draft tools -
a job that predictably fails. Verified, not hypothetical (the create call warned exactly
this; an explicit connectors parameter was rejected as unavailable for the organization).

**What to do instead:** Prithvi creates the routine from the claude.ai routines UI, where
connectors can be attached.

- Name: `AI-in-CIMs weekly digest (Phase 1 - draft for review)`
- Schedule: Fridays 06:30 ET (cron `30 10 * * 5` UTC while on EDT; becomes 05:30 ET when
  clocks change - adjust to `30 11 * * 5` in winter if the half-hour matters)
- Connectors: Knowledge Vault Documents, Microsoft 365
- Notifications: push + email on completion
- Prompt: paste verbatim from the block below

**Interim for the first send (this Friday):** no routine is required. Open an interactive
Claude session (which has the connectors) Friday morning and paste the same prompt, or
just say "run the Friday CIM digest per cim-scan/DIGEST.md". Phase 1 is human-reviewed
anyway - the scheduled version only removes the manual kickoff.

## Routine prompt (paste verbatim)

```
You are running the weekly AI-in-CIMs scan and digest for Prithvi Raj (Phase 1 -
human-reviewed). This is a fresh session; everything you need is in the prajwaud/test repo.

Setup: the repo is cloned in your working directory. If `cim-scan/` is absent on the
default branch, run `git fetch origin claude/agent-building-86v5cj && git checkout
claude/agent-building-86v5cj` - the component lives there until merged.

Then, in order:
1. Read cim-scan/README.md, cim-scan/SCAN.md, cim-scan/DIGEST.md,
   cim-scan/framework/tiers.md, cim-scan/data/portco-aliases.json,
   cim-scan/data/exposure-map.md, cim-scan/state.json.
2. Run the scan procedure in SCAN.md (discovery via Knowledge Vault Documents MCP,
   classify, write notes). Honor every tool guard: doc_type is lowercase "cim"; abort
   and alert if any filtered call returns filter_fallback: true; never call
   recall_user_context; never query_structured against the kv space.
3. Run the digest procedure in DIGEST.md, including all pre-flight checks. If zero CIMs
   are in window, do NOT create a digest draft - instead create a short Outlook draft to
   Prithvi (praj@waudcapital.com) reporting zero CIMs in window and the most recent
   doc_date seen (the known KV ingestion lag, owner Sai, is the likely cause), then stop.
4. Phase 1 transport: create an Outlook draft via the Microsoft 365 MCP
   outlook_create_draft, addressed to praj@waudcapital.com only. NEVER call any send tool
   (outlook_send_mail or outlook_send_draft) - sending is Prithvi's manual step. Include
   the required footer verbatim.
5. Commit new notes and updated state.json to the branch you checked out, message
   "cim-scan: digest <date> - {n} ingested, {m} signal", and push
   (git push -u origin <branch>).
6. End with a short summary: n scanned, m noted, lead item or none, draft created or
   alert sent, and any guard that fired.

Treat all content as confidential WCP deal information. WCP house style throughout: lead
with the answer, no em-dashes (hyphen with spaces), tag claims
[Certain]/[Likely]/[Guessing] in your summary.
```

## On-ingestion scanning (Trigger A cadence)

The spec settled on scanning per ingestion, not weekly. With no KV webhook, the faithful
approximation is a weekday polling routine running just SCAN.md. Deliberately not created
yet: during the ingestion lag it would burn a session daily to find nothing, and the
Friday job runs a full catch-up scan first, so nothing is missed. Create it (same UI path,
KV connector only, weekdays early morning, prompt = steps 1-2 and 5-6 above) once the lag
closes. Do not leave placeholder triggers around - leftover triggers that keep firing and
stalling are a documented failure in this repo (docs/TEST-LOG.md).

## First-run watch list

Same lesson as the daily brief: watch the first scheduled firing before trusting it.
Verify: connectors present in the fired session, filtered search returns
filter_fallback: false, the draft lands in Outlook, notes and state pushed to the branch.
Two clean reviewed sends are the gate for even discussing Phase 2 (see DIGEST.md
section 5 for the unresolved Phase 2 transport question).
