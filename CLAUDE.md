# Instructions for Claude instances working in this repo

## What this is

The Prithvi WCP Operating System. Two components:

1. **Daily Executive Brief** - emailed to praj@waudcapital.com at 5:00am ET on weekdays.
   Lives in `src/`, `prompts/`, `docs/`. Blocked on the Entra app registration.
2. **AI-in-CIMs scan and weekly digest** - scans CIMs ingested into the Knowledge Vault,
   classifies how sellers substantiate AI claims, and drafts a Friday digest with
   portco-specific implications. Lives in `cim-scan/`; start at `cim-scan/README.md`
   and `cim-scan/SPEC.md`. Retrieval is via the Knowledge Vault Documents MCP server
   (a Claude-session concern, not Python). Blocked on the KV ingestion lag (owner: Sai).

Prithvi Raj is Chief Data and AI Officer at Waud Capital Partners, a Chicago-based
middle-market PE firm. Outputs may reach Managing Partners, IC members, portco CEOs and LPs,
so default to executive precision and brevity.

## Read these first, in this order

1. `docs/TEST-LOG.md` - what is actually proven versus assumed. Several dead ends are
   documented there specifically so they are not repeated. Reading it will save you hours.
2. `docs/ARCHITECTURE.md` - the design and why the obvious approach was rejected.
3. `ADMIN-ENTRA-REQUEST.md` - the blocking dependency.

## The single most important thing to understand

**Do not try to send email through the Microsoft 365 MCP connector.** It works
interactively and fails unattended, because `outlook_send_mail` raises a permission prompt
that requires a human click. This was tested and confirmed. At 5am there is no human.

This repo uses app-only Microsoft Graph authentication instead: client credentials, no user
context, no browser, no refresh token, no prompt. If you find yourself reaching for
`mcp__Microsoft_365__outlook_send_mail`, stop and reread `docs/TEST-LOG.md`.

## Current blocking dependency

Nothing in this repo can be verified until the Entra app registration exists and returns
four values: tenant ID, client ID, client secret, and confirmation that an Application
Access Policy restricts the app to praj@waudcapital.com.

Until then, all code here is written against the documented Graph contract and is
**unverified**. Say so plainly when reporting status. Do not describe it as working.

## Where the prompt lives

`prompts/system.md`, not in Python. It has YAML frontmatter carrying model, max_tokens and
temperature, and a markdown body. `src/prompt_loader.py` loads it; `{{tz_label}}` is
substituted at runtime.

If asked to change how the brief reads, edit that file - do not move prose into
`synthesize.py`. The separation is the point: the prompt is the part that gets iterated on,
and it should be reviewable as prose.

Log every prompt change in `prompts/CHANGELOG.md` with the reason, not just the diff. Git
holds the diff; the reason is what is irrecoverable later.

## The iteration loop

```bash
make capture    # freeze live data to fixtures/
make tune       # replay it through the current prompt
make compare A=system B=variant
```

Always tune against a fixture, never against live Graph. With live data the inbox changes
under you and you cannot attribute an output change to your edit.

There is deliberately no automated eval or LLM judge. Prithvi is the evaluator. Do not add
a scoring harness unless he asks - a judge would optimize toward its own notion of a good
executive summary rather than his.

## Working conventions

- Communication: lead with the answer, rationale after. Tag factual claims [Certain],
  [Likely], or [Guessing]. Flag data gaps rather than filling them with confident
  approximations. Never use em-dashes; use a hyphen with spaces instead.
- Never commit secrets. `.env` is gitignored. Credentials belong in GitHub Actions
  encrypted secrets.
- Treat all deal, firm, portfolio, and personnel information as confidential.
- Do not widen Graph permissions beyond `Calendars.Read`, `Mail.Read`, `Mail.Send` without
  an explicit decision from Prithvi. Each addition is a new admin conversation and a larger
  blast radius on the credential.

## When credentials arrive - the sequence that matters

Do these in order. Skipping to the schedule is how you end up with a broken job that fails
silently at 5am.

1. `python -m src.daily_brief --dry-run` - reads live Graph data, prints the brief to
   stdout, sends nothing. Confirms auth and both read scopes.
2. Check the printed meeting times against Prithvi's actual calendar. The mailbox is
   Central; see the timezone note in `docs/TEST-LOG.md`. Getting this wrong produces a
   brief that is quietly an hour off every single day.
3. `python -m src.daily_brief` once, manually, and confirm the email arrives.
4. Only then enable the GitHub Actions schedule.
5. Delete the two leftover Claude Code Remote triggers listed at the bottom of
   `docs/TEST-LOG.md`, or they will keep firing and stalling.

## Open questions to put to Prithvi, not to guess at

- Display timezone: Central or Eastern? The mailbox is Central, he specified ET. Unresolved.
- Weekdays only, or all seven days?
- Should the brief cover only the inbox, or also calendar invitations, Teams messages,
  or SharePoint activity? Current scope is calendar plus unread inbox.
- What counts as "notable" unread? The current synthesis prompt groups into ACTION REQUIRED,
  NEEDS A REPLY, and FYI, and demotes vendor cold outreach. That heuristic is a first guess
  and should be tuned against his reaction to a week of real briefs.
