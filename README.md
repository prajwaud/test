# Prithvi WCP Operating System

Personal automation system for Prithvi Raj, Chief Data and AI Officer, Waud Capital Partners.

First component: an automated Daily Executive Brief delivered by email at 5:00am ET every
weekday - calendar for the day plus triaged unread mail, synthesized rather than dumped.

## Current status

| Component | State |
|---|---|
| Architecture decided | Done - app-only Microsoft Graph, see `docs/ARCHITECTURE.md` |
| Entra app registration | **Blocked on admin** - see `ADMIN-ENTRA-REQUEST.md` |
| Graph client | Written, untested (no credentials yet) |
| Brief synthesis | Written, untested |
| Scheduled runner | Written, untested |
| End-to-end verified | Not yet |

Nothing in this repo has been executed against live credentials. Everything is written
against the documented Graph API contract and needs a first real run before it should be
trusted. See `docs/TEST-LOG.md` for what has actually been proven versus assumed.

## Why app-only auth

The obvious path - have Claude use the Microsoft 365 connector to read and send - works
interactively but fails unattended. Confirmed by testing: the send call requires a human
to click an approval prompt, and there is nobody present at 5am. Details and evidence in
`docs/TEST-LOG.md`.

App-only (client credentials) authentication removes the human from the loop entirely:
no browser, no interactive consent, no refresh token to expire, no permission prompt.
It also means the system does not depend on a long-lived Claude session surviving
overnight in a container that gets reclaimed after inactivity.

## Repo layout

```
.
├── ADMIN-ENTRA-REQUEST.md     Standalone permission request - forward to IT/Entra admin
├── CLAUDE.md                  Context and instructions for Claude instances
├── docs/
│   ├── ARCHITECTURE.md        Design and rationale
│   └── TEST-LOG.md            What was proven, what failed, what is unknown
├── src/
│   ├── graph_client.py        Auth, calendar read, mail read, send
│   ├── synthesize.py          Claude API call that triages and writes the brief
│   └── daily_brief.py         Entry point
├── .github/workflows/
│   └── daily-brief.yml        Scheduled runner
├── .env.example
└── requirements.txt
```

## Getting started

1. Have the Entra admin complete `ADMIN-ENTRA-REQUEST.md`. Nothing works before this.
2. Copy `.env.example` to `.env` and fill in the four values the admin returns.
3. `pip install -r requirements.txt`
4. `python -m src.daily_brief --dry-run` - reads live data, prints the brief, sends nothing.
5. `python -m src.daily_brief` - sends for real.
6. Only after a successful manual run, enable the GitHub Actions schedule.
