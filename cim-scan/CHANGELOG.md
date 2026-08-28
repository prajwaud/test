# cim-scan changelog

## 2026-08-28 - transport moved outside Claude (outbox + app-only Graph)

Reason: the inaugural send ALSO required Prithvi's manual approval click - the third
confirmation, and proof the .claude/settings.json allowlist does not clear the M365 MCP
send prompt in this org. Two prior run records overclaimed unattended sends; both
corrected. Decision (Prithvi): build the send path outside Claude. Implemented:
`outbox/` queue with a recipient allowlist, `src/send_outbox.py` (app-only Graph,
reusing the daily brief's graph_client with HTML + multi-recipient support), and
`.github/workflows/send-outbox.yml` (push-triggered plus Friday backstop; no-ops until
the Entra secrets exist - same credential the daily brief awaits, no new admin ask).
DIGEST.md delivery rewritten: Claude assembles and queues; it never sends. Interim
until credentials land: queue plus an MCP draft for Prithvi's one click, gated on the
absence of receipts in outbox/sent/.

## 2026-08-26 - provenance rule after Prithvi challenged an exit-timing claim

The v2 test digest said "PracticeTek and TeamSnap are the nearest software exits" -
inherited verbatim from the reference digest, unverified. The KB says TeamSnap ~2 years
and Career Certified ~24 months are nearest; PracticeTek is 3-5 years. Rule added: the
reference digest is a format reference only, never a fact source. Every portco-specific
claim (exit timing especially) must trace to the KB, the exposure map, or a Vault
document, or be dropped. Softdocs note corrected.

## 2026-08-26 - digest revisions from Prithvi's test-run review

Two standing rules added to DIGEST.md section 3, reason: Prithvi reviewed the first test
send and flagged (1) the project's purpose was not clear upfront - a first-time reader
(Doug, R2) should not have to infer what the instrument is; (2) the lead item's framing
was too opinionated - the headline editorialized ("healthcare is not writing one")
instead of naming the company and the fact. Fix: purpose paragraph opens every digest;
lead item is factual with inference confined to the Read line. Tier-by-tier entry format
unchanged - explicitly confirmed good.

Log every change to SCAN.md, DIGEST.md, framework/tiers.md, or the exposure map here with
the reason, not just the diff. Git holds the diff; the reason is what is irrecoverable
later. Same convention as prompts/CHANGELOG.md for the daily brief.

## 2026-08-26 - test run (Phase 1, recipient: Prithvi only)

First end-to-end run over the June 2026 cohort (8 docs). Findings worth recording:

- Discovery surfaced 30+ CIMs in the March-June window vs the golden set's 18. The
  backlog (20+ March-May docs) is deliberately deferred to a one-time backfill report
  per the pre-flight backfill guard.
- Golden-set overlap regression: 4/5 exact (Softdocs 4, BryteBridge 2, H2 0, ADL 0);
  DynamicAccess returned no AI evidence in top chunks vs reference Tier 1 - explainable,
  logged in state.json. Full 18-doc regression still pending.
- New defect verified: company_entity_ea789e59 conflates IPS Group (Burgundy) with
  Integrated Practice Solutions (PracticeTek) and a 2016 doc. Alias map warning updated;
  scans must filter per doc_id.
- Page pinning worked where chunk text carried markers (Softdocs p.39, BryteBridge p.41
  and p.72, H2 p.16); the Softdocs margin bridge could not be pinned and correctly fell
  back to a section-name link.

## 2026-08-26 - initial build

Built from the AI-in-CIMs scan spec (SPEC.md, 2026-08-26). Decisions made at build time:

- Note storage: repo files under notes/ (spec section 16 q1 - simplest durable option).
- Backfill: separate one-time report when the ingestion lag closes, guarded by the
  >10-notes pre-flight check in DIGEST.md (spec section 16 q2 recommendation adopted).
- Tier 3/4 boundary: naming AI as a bridge driver suffices for Tier 4 (spec section 16
  q3, decision as written).
- Non-CIM documents: out of scope for v1 (spec section 16 q4).
- Discovery: no ingestion-timestamp filter exists on the KV server, so discovery is
  wide-window (12-month doc_date) multi-probe search plus doc_id diffing against
  state.json. Flagged to raise with Sai alongside the lag escalation - an
  ingested-since filter or list-documents endpoint would make discovery exact.
- Alias map built from 17 live resolve() calls on 2026-08-26, hand-reviewed.
- Exposure map seeded from the March 2026 portfolio KB + the three maturity reports in
  spec section 10; inference tagged [Likely]/[Guessing]; awaiting Prithvi's review.
- Phase 1 transport: outlook_create_draft only, no send call ever. Phase 2 transport is
  an open question - M365 MCP send is proven to fail unattended (docs/TEST-LOG.md), and
  the pending app-only Graph credential is policy-scoped to praj@waudcapital.com, which
  conflicts with sender-is-the-agent. Needs a decision before Phase 2.
