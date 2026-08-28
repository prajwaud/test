# Friday routine - setup instructions

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
2. M365 send raises its interactive prompt - CONFIRMED on the 2026-08-28 verification
   run (Prithvi had to click approve; connectors were fine, the send was not). Two
   mitigations layered for the scheduled firing: (a) .claude/settings.json now
   pre-approves the five MCP tools the run needs, and (b) DIGEST.md reorders delivery
   so notes/state are pushed before the send attempt and a blocked send degrades to a
   ready-to-send draft in Prithvi's Drafts folder. Caveat on (a): the settings file
   lives on the feature branch; a container that clones fresh from main at wake will
   not have it at settings-load time until the branch is merged. Fallback if the send
   stalls Friday: the digest is in Drafts, addressed to all three - one manual click.
   Durable fix if the prompt persists: app-only Graph send per docs/TEST-LOG.md once
   the Entra credentials land.

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
