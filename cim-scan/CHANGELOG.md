# cim-scan changelog

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
