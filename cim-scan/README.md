# AI-in-CIMs scan and weekly digest

Second component of the Prithvi WCP Operating System. Scans every CIM ingested into the
Knowledge Vault, evaluates how the seller substantiates AI claims, and translates the
findings into portco-specific implications in a weekly Friday digest. Qualitative
market-intelligence instrument, not a metrics dashboard.

Spec: `SPEC.md` (the authority, 2026-08-26). This README is the operator view.

## Status - as of 2026-08-26

Built and grounded, not yet exercised end to end. What is proven vs assumed:

- [Certain] KV Documents MCP retrieval works from a Claude session: filtered
  `search_evidence` with lowercase `doc_type: "cim"` returned `filter_fallback: false`
  in this build session.
- [Certain] The ingestion lag is real and current: the most recent CIM in the document
  layer is dated 2026-06-30 (H2 Health), verified live 2026-08-26. DealCloud runs weeks
  ahead. **This is the blocker - escalate to Sai / the KV extraction pipeline owner.**
- [Certain] The alias map (`data/portco-aliases.json`) reflects live resolve() output
  from 2026-08-26.
- [Likely] The scan and digest procedures will run unattended in a scheduled fresh
  session. Unverified - the first scheduled run must be watched, same lesson as the
  daily brief (docs/TEST-LOG.md).
- [Guessing] Nothing. Gaps are flagged, not filled.

## Layout

| Path | What |
|---|---|
| `SPEC.md` | The build spec. Settled decisions live here; do not relitigate section 2. |
| `SCAN.md` | Per-CIM scan procedure (Trigger A) including tool-defect guards |
| `DIGEST.md` | Friday digest procedure (Trigger B) including pre-flight checks and Phase 1/2 gating |
| `framework/tiers.md` | Tier framework, boundary rulings, calibration anchors |
| `data/portco-aliases.json` | 17-portco entity-id alias map (built from live resolve calls) |
| `data/exposure-map.md` | 17-portco exposure map, four attributes each, seeded and tagged |
| `reference/golden-set.md` | May-June 2026 18-CIM regression reference |
| `reference/reference-digest.md` | Worked-example placeholder - Prithvi to paste |
| `notes/` | Accumulated per-CIM notes (the store the digest reads) |
| `state.json` | Scan ledger and digest history |
| `CHANGELOG.md` | Procedure changes with reasons |

## Prerequisites, ordered (spec section 17)

1. **Close the ingestion lag** - blocking. Owner: Sai / KV extraction pipeline. Without
   it, Friday finds zero CIMs in window and the pre-flight guard alerts instead of
   sending. While escalating, also request an ingestion-timestamp filter or
   list-documents endpoint (discovery currently approximates ingestion via doc_id
   diffing - see CHANGELOG).
2. **Pin pages at extraction** - built into SCAN.md; verify on real documents.
3. **Exhibit rendering** - not built (net-new). Test first on the Softdocs (HAVEN)
   margin expansion bridge. Until built, DIGEST.md falls back to links.
4. **Exposure map review** - seeded; Prithvi to review the tagged inferences and the
   open items at the bottom of `data/exposure-map.md`.

## Phasing

- **Phase 1 (now):** Friday morning run generates the digest and creates an Outlook
  draft addressed to Prithvi only. He reviews, adds Doug Rassner and rwaud2, and sends.
  No send tool is ever called by the agent.
- **Phase 2 (gated):** unattended send. Requires: two consecutive reviewed sends without
  correction, lag closed, exhibit rendering built, and a transport decision - M365 MCP
  send fails unattended (proven, docs/TEST-LOG.md), and the pending app-only Graph
  credential is policy-restricted to praj@waudcapital.com, which conflicts with the
  spec's sender-is-the-agent requirement for a three-recipient distribution. Options:
  add a dedicated agent mailbox to the Application Access Policy, or decide to send from
  Prithvi's mailbox. Prithvi decides; do not widen the Graph permission scope without him.

## Acceptance criteria not yet demonstrated

From spec section 13: golden-set regression (2), which needs a full scan run over the
May-June cohort; exhibit page pinning on real docs (7); and end-to-end unattended
execution (1). Everything else is encoded in the procedures and checked per run.
