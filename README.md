# Prithvi WCP Operating System

Personal automation system for Prithvi Raj, Chief Data and AI Officer, Waud Capital Partners.

First component: an automated Daily Executive Brief emailed at 5:00am ET on weekdays -
the day's calendar plus triaged unread mail, synthesized rather than dumped.

Runs entirely on its own. No Claude session, no chat window, no human in the loop.

## Current status

| Component | State |
|---|---|
| Architecture | Decided - app-only Microsoft Graph. See `docs/ARCHITECTURE.md` |
| Entra app registration | **Blocked on admin** - see `ADMIN-ENTRA-REQUEST.md` |
| Graph client | Written, unverified against live credentials |
| Prompt + iteration harness | Written and exercised (degraded path verified) |
| Scheduled runner | Written, never fired |
| End-to-end | Not yet - blocked on credentials |

Nothing has run against live Graph credentials, because they do not exist yet. Syntax, the
prompt loader, the DST hour guard, and the graceful-degradation path are verified.
Everything touching Graph is written against the documented contract and unproven.
See `docs/TEST-LOG.md` for the full proven-versus-assumed breakdown.

## Why app-only auth

The obvious approach - have Claude read and send through the Microsoft 365 connector - works
interactively and fails on a schedule. The send tool raises a permission prompt requiring a
human click, and at 5am there is no human. Confirmed by direct testing.

App-only (client credentials) authentication removes the human entirely: no browser, no
interactive consent, no refresh token to expire, no prompt. It also means the system does not
depend on a Claude session surviving overnight in a container that gets reclaimed on idle.

Claude is retained for one thing: deciding what matters today. That is judgment. Reading a
calendar is not, and stays in code.

## Setup

1. **Get the credentials.** Send `ADMIN-ENTRA-REQUEST.md` to whoever administers Entra.
   Nothing works before this. It asks for three application permissions and an Exchange
   access policy scoping the credential to one mailbox.
2. `cp .env.example .env` and fill in the four values.
3. `make install`
4. `make dry-run` - reads live data, prints the brief, sends nothing.
5. **Check the meeting times against your real calendar.** The mailbox is Central and the
   display default is Eastern. If that is wrong, every brief is quietly an hour off.
6. `make send` once, manually, and confirm the email arrives.
7. Only then enable the GitHub Actions schedule.

## Improving the brief over time

The brief's quality is almost entirely in `prompts/system.md`. It is a markdown file, not a
Python string, so it can be edited and reviewed like prose.

```bash
make capture                      # freeze today's real data as a fixture
$EDITOR prompts/system.md         # change the prose
make tune                         # replay the same data through the new prompt
make compare A=system B=tighter   # two prompts, identical input, side by side
```

The fixture matters: iterating against live Graph means the inbox shifts under you and you
cannot tell whether the output changed because of your edit or because mail arrived. Frozen
input makes your edit the only variable.

Full guidance, including what is worth tuning first, is in `prompts/README.md`. Log every
change and its reason in `prompts/CHANGELOG.md`.

## Repo layout

```
.
├── ADMIN-ENTRA-REQUEST.md      Forward to the Entra admin. The blocking dependency.
├── CLAUDE.md                   Context for Claude instances working here
├── Makefile                    make help
├── prompts/
│   ├── system.md               The live prompt. This is the part worth iterating on.
│   ├── README.md               How to iterate, and what to tune first
│   └── CHANGELOG.md            Every prompt change and why
├── docs/
│   ├── ARCHITECTURE.md         Design, rationale, failure modes
│   └── TEST-LOG.md             Proven vs assumed. Read before redoing any of it.
├── src/
│   ├── graph_client.py         Auth, calendar read, mail read, send
│   ├── formatting.py           Raw payload to model input
│   ├── prompt_loader.py        Loads prompts/*.md with frontmatter
│   ├── synthesize.py           The Claude call, with graceful degradation
│   ├── capture.py              Snapshot live data to fixtures/
│   ├── tune.py                 Replay fixtures through prompts. Sends nothing.
│   └── daily_brief.py          Entry point
├── .github/workflows/
│   └── daily-brief.yml         Paired cron plus hour guard - 5am ET year-round
├── fixtures/                   Gitignored. Contains real mail content.
└── runs/                       Gitignored. Saved tuning outputs.
```

## Confidentiality

`fixtures/` and `runs/` hold real calendar entries and real email content - deal, firm and
personnel information. Both are gitignored and must stay that way. Do not paste their
contents anywhere external.
