# Start here - context for a new conversation

Paste or upload this repo into a new Claude conversation and point at this file first.

## What you are looking at

The Prithvi WCP Operating System. One component built so far: an automated Daily Executive
Brief that emails Prithvi Raj (Chief Data and AI Officer, Waud Capital Partners) at 5:00am ET
on weekdays, covering the day's calendar and triaged unread mail.

It is designed to run with no human present and no Claude session alive - a scheduled job,
not a chat interaction.

## State of play

**Working and verified:** the prompt loading system, placeholder substitution, the DST hour
guard, and the graceful-degradation path when the Claude API is unreachable.

**Written but never executed:** every Microsoft Graph call. The Entra app registration does
not exist yet, so there are no credentials to run against. Do not describe this code as
working.

**Blocked on:** a person. `ADMIN-ENTRA-REQUEST.md` needs to go to whoever administers Entra
ID at WCP. It returns four values: tenant ID, client ID, client secret, and confirmation that
an Exchange Application Access Policy restricts the credential to praj@waudcapital.com only.
Nothing downstream can be tested before that.

## Decisions already made - please do not relitigate these without new information

**Microsoft Graph app-only auth, not the Microsoft 365 MCP connector.** The connector was
tried first. It works interactively and fails on a schedule: `outlook_send_mail` raises a
permission prompt requiring a human click, and there is nobody there at 5am. This was
confirmed by direct testing, not assumed. Details in `docs/TEST-LOG.md`.

**Claude only does synthesis.** Reading a calendar and filtering unread mail is
deterministic and lives in code. Deciding that a buried PandaDoc execution link is today's
real obligation is judgment, and that is the only part worth an API call.

**Sonnet, not Opus.** Daily triage over bounded input. If output quality disappoints, the
prompt is more likely underspecified than the model underpowered.

**No automated eval or LLM judge.** What makes a good brief for Prithvi is not specifiable
as a metric in advance, and a judge would optimize toward its own idea of an executive
summary. He reads the output and decides.

`docs/TEST-LOG.md` records several dead ends in detail specifically so they are not repeated.
Read it before proposing an approach that touches auth or scheduling.

## Open questions that need Prithvi's input, not a guess

1. **Timezone.** The Outlook mailbox is configured Central and WCP is Chicago-based, but
   Eastern was specified for display. This may have been a copy-through rather than a
   deliberate choice. If it is wrong, every brief is quietly an hour off. Ask before
   trusting the times. One env var, `BRIEF_DISPLAY_TIMEZONE`, controls it.
2. **Triage taxonomy.** The ACTION REQUIRED / NEEDS A REPLY / FYI split is a first guess
   from one hand-assembled brief. It has never been checked against a real reaction.
3. **Length.** The 400-word cap is arbitrary.
4. **Scope.** Currently calendar plus unread inbox. Teams, SharePoint and calendar
   invitations are deliberately excluded until the basic brief proves useful.

## Where to read next

| File | What it gives you |
|---|---|
| `README.md` | Setup sequence and repo map |
| `docs/TEST-LOG.md` | What is proven vs assumed, and the dead ends |
| `docs/ARCHITECTURE.md` | Design, rationale, failure modes |
| `ADMIN-ENTRA-REQUEST.md` | The blocking dependency, forwardable as-is |
| `prompts/README.md` | How to iterate on brief quality, and what to tune first |
| `prompts/system.md` | The actual prompt - the part most worth improving |
| `CLAUDE.md` | Conventions for Claude working inside the repo |

## Useful things to ask for next

- Review `ADMIN-ENTRA-REQUEST.md` before it goes to the admin, especially the permission
  scoping - unscoped, `Mail.Send` as an application permission is a send-as-anyone
  credential for the entire tenant.
- Draft the note to the admin that accompanies the request.
- Improve `prompts/system.md`. It is prose and it is where the brief's quality lives.
- Once credentials exist: walk the setup sequence in `README.md`, then verify the meeting
  times against the real calendar before enabling the schedule.
- Design the second WCP OS component. The brief is component one; the auth pattern and repo
  shape are reusable.

## Note on the contents

`prompts/system.md` and `docs/TEST-LOG.md` contain WCP firm context - portfolio company
names, senior colleagues, one mailbox address. There is no deal data, no financials, and no
captured mail content. Fixtures, which would contain real email, are gitignored and are not
in this archive.
