# Outbox - the boundary between Claude and email

Claude sessions never send email; every M365 MCP send raises an interactive permission
prompt that requires a human click (confirmed three times, most recently on the
2026-08-28 inaugural digest). Claude assembles the finished email and commits it here
as JSON; GitHub Actions (`.github/workflows/send-outbox.yml`) sends it via app-only
Graph with zero human involvement.

- Entry schema and semantics: docstring of `src/send_outbox.py`.
- Recipients must be on `recipients-allowlist.json` - adding one is a human-reviewed
  commit, never something an automated session does silently.
- `sent/` holds receipts. The presence of any receipt is the signal to Claude runs
  that the Graph path is live (see cim-scan/DIGEST.md delivery).
- Blocked on the same Entra app registration as the daily brief
  (ADMIN-ENTRA-REQUEST.md, secrets GRAPH_TENANT_ID / GRAPH_CLIENT_ID /
  GRAPH_CLIENT_SECRET / BRIEF_MAILBOX in Actions). The workflow no-ops cleanly until
  the secrets exist.
- Confidentiality: entries contain deal content, same as cim-scan/notes/. This repo is
  private and must stay that way.
