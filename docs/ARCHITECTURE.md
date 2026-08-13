# Architecture

## Shape

```
GitHub Actions cron (09:00 + 10:00 UTC)
  │
  ├─ guard: exit unless it is 05:00 in America/New_York
  │         (two cron entries + a local-hour check gives exact 5am ET year-round,
  │          without the DST drift a single fixed-UTC cron produces)
  │
  ├─ graph_client.get_token()          client credentials, fresh token per run
  ├─ graph_client.get_todays_events()  GET /users/{mailbox}/calendarView
  ├─ graph_client.get_unread()         GET /users/{mailbox}/messages?$filter=isRead eq false
  │
  ├─ synthesize.build_brief()          Claude API - triage and prose
  │
  └─ graph_client.send_mail()          POST /users/{mailbox}/sendMail
```

No Claude Code session, no MCP connector, no browser, no human.

## Why not the Microsoft 365 MCP connector

It was the first approach tried and it does not survive contact with a schedule.

`outlook_send_mail` raises an interactive permission prompt. Reads pass through; writes do
not. Confirmed by direct test - see `docs/TEST-LOG.md`. There is nobody at 5am to click it.

Secondary reasons, each sufficient on its own:

- A trigger that spawns a fresh session gets no connector tools at all. The `connectors`
  parameter on `create_trigger` is disabled org-wide for WCP.
- A trigger bound to an existing session does keep its connectors, but depends on that
  session's container surviving overnight. Containers are reclaimed after inactivity.
- OAuth access tokens live about an hour. The refresh behaviour across a long idle gap was
  never cleanly proven.

App-only auth removes all four problems at once. Client credentials mint a fresh token on
every run, so there is no refresh path to fail and no session to keep alive.

## Why Claude is still in the loop

Only for synthesis. Reading a calendar and filtering unread mail is mechanical and belongs
in code, where it is deterministic and cheap. Deciding that a PandaDoc execution link
buried in a thread is the thing Prithvi must act on today, and that two vendor cold emails
are not, is judgment. That is the part worth an API call.

Model: Sonnet. The task is triage and short prose over a bounded input, not deep reasoning.
Opus is not warranted for a daily job and the cost compounds over a year.

## Failure modes and how each surfaces

| Failure | Surfaces as | Handling |
|---|---|---|
| Client secret expired | 401 from token endpoint | Job fails loudly in Actions; set a calendar reminder before expiry |
| Access policy misconfigured | 403 on the mailbox call | Job fails loudly; check `Test-ApplicationAccessPolicy` |
| Empty calendar | Valid state, not an error | Brief says "No meetings today" |
| No unread mail | Valid state, not an error | Brief says "No notable unread" |
| Anthropic API down | Exception in synthesis | Falls back to sending an unsynthesized raw brief rather than nothing |
| Graph throttling (429) | Retry-After header | Honoured with backoff |

The design principle: a partially degraded brief that arrives beats a perfect brief that
does not. The only unrecoverable failure is silence, so the synthesis step degrades rather
than aborts.

## What is deliberately not built yet

- SharePoint or Teams context. Scope creep until the basic brief is proven useful.
- HTML formatting. Plain text first; confirm the content is right before styling it.
- Multi-user support. This is Prithvi's system. Generalizing to other WCP staff is a
  different problem with different auth implications and should not be designed
  speculatively.
