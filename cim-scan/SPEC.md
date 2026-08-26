# AI-in-CIMs Scan and Weekly Digest - Build Specification

**Owner:** Prithvi Raj (CDAO, Waud Capital Partners)
**Build target:** Claude Code
**Status:** Spec complete, build not started
**Target first send:** Friday (human-reviewed), automated thereafter
**Last updated:** 2026-08-26

---

## 1. Purpose

Scan every CIM ingested into the WCP Knowledge Vault, evaluate how the seller substantiates
any AI claim, and translate what is learned into specific implications for WCP portfolio
companies. Output is a weekly digest sent by an agent to a fixed distribution list.

This is a qualitative market-intelligence instrument, not a metrics dashboard. The value is
in noticing that a seller solved a problem WCP portfolio companies also have.

### What this is not

- Not a KPI tracker. An earlier design scored tier distribution over time and produced
  percentages. That was rejected: the statistics tell you the temperature, not what anyone
  figured out.
- Not a clipping service. A note that summarizes a company's AI features without naming a
  portco and a question has failed and should not be written.
- Not a report on new deals. The trigger is document ingestion, not deal origination.

---

## 2. Design history and rejected alternatives

Recorded so the build does not relitigate settled decisions.

| Decision | Outcome | Reason |
|---|---|---|
| Weekly *reporting* cadence | Adopted | Original objection was that ~1-2 AI-relevant CIMs/week is too thin for trend. Resolved: the digest reports what was ingested, not what changed. Empty-ish weeks are acceptable; a zero reading is a reading. |
| Weekly *scanning* cadence | Rejected in favor of on-ingestion | Scan every CIM as it lands. Notes accumulate. The digest is a collection of accumulated notes, not a batch job. This removes the "nothing happened this week" failure mode. |
| Tier distribution statistics | Rejected | Directionally interesting, operationally useless at ~20 CIMs/month. Single-cell changes are noise. |
| RYG evidence badge alongside tier | Rejected | Two badges is one too many. Evidence quality now carried in prose in the Evidence bullet. Note the known cost: tier and evidence quality are independent axes, so ordering by tier alone can bury a well-evidenced Tier 1 beneath a poorly-evidenced Tier 2. Accepted tradeoff. |
| Separate individual alert emails | Rejected | Folded into the digest as a lead item at the top. One email, not two. |
| Sender = Prithvi | Rejected | Sends from the agent. Consequence: inference must be attributed (see §8). |

---

## 3. Tier framework

The single classification axis. Applied to every CIM.

| Tier | Definition | Test |
|---|---|---|
| **4** | AI named in the EBITDA bridge, margin walk, or pro forma adjustments | Can a buyer underwrite or discount it as a number? |
| **3** | Quantified operationally - hours, FTEs, cycle time, revenue per head - but not carried into the bridge | Are there real numbers that are not P&L numbers? |
| **2** | Positioned as capability. Roadmaps, architecture diagrams, feature lists | Is AI described as something the company has, with no economics? |
| **1** | Ambient. AI describes the market or sector, not the company's economics | Does AI appear only in market tailwinds or industry context? |
| **0** | Silent. No substantive AI mention | |

### Supplementary tags

Capture alongside the tier. These move faster than tiers and are worth trending separately
even though the digest does not report on them.

- `model_provider_named` - seller discloses OpenAI / Anthropic / other. Emerging disclosure
  norm; also the dependency handle for diligence.
- `agentic_language` - the word "agentic" appears. Vocabulary drift indicator.
- `ai_in_market_sizing` - AI appears in TAM or market structure, not just product. Signals a
  more aggressive claim than product positioning.
- `headcount_action_attributed_to_ai` - **the leading indicator.** A cost or headcount
  reduction explicitly linked to automation. The first healthcare CIM that does this is the
  inflection point. Flag prominently when true.

---

## 4. Architecture

### Trigger A - per-CIM scan (on ingestion)

```
New document lands in Knowledge Vault with doc_type = "cim"
  -> classify tier
  -> if tier >= 2: generate note
  -> if tier <= 1 but portfolio-relevant (e.g. direct comp to a portco): generate short entry
  -> if tier == 0 and not portfolio-relevant: log only, no note
  -> append note to running store
  -> evaluate escalation criteria (§7); if met, mark as lead-item candidate
```

### Trigger B - weekly digest (Friday morning)

```
Query all notes generated since last digest
  -> order by tier descending
  -> select lead item (highest-escalation note, or none)
  -> render exhibits
  -> assemble email
  -> [PHASE 1] deliver to Prithvi for review, then send
  -> [PHASE 2] send unattended
```

**Do not schedule Phase 2 until the digest has generated correctly under review twice.**

---

## 5. Data sources and tool behavior

All retrieval via the **Knowledge Vault Documents** MCP server
(`https://kv-mcp.gentlesand-60538a1f.westus2.azurecontainerapps.io/mcp`).

### Tools in use

| Tool | Use | Notes |
|---|---|---|
| `search_evidence` | Primary retrieval over prose chunks | Filters: `doc_type`, `doc_date_gte`, `doc_date_lte`, `company_id`. Returns `web_url`, `file_name`, `section_path`, `doc_date`, `is_tabular` |
| `resolve` | Company/entity name to canonical ID | Returns ranked candidates with confidence |
| `query_structured` | DealCloud queries (deal status, dates, sector) | `space="dealcloud"` only |
| `answer_question` | Combined prose + structured | Heavier; use sparingly |

### Observed defects - MUST be handled in the build

These were verified directly and are not hypothetical.

1. **`doc_type` filter is case-sensitive and fails soft.**
   Passing `doc_type: "CIM"` returns `filter_fallback: true` and results are silently
   returned UNFILTERED. The correct value is lowercase `"cim"`.
   **Build requirement:** always assert `filter_fallback === false` on every filtered call.
   Abort and alert if true. Never proceed on a silent fallback.

2. **`doc_date` is unreliable on older documents.**
   Example: a file named "Competitive Overview 11.29.21" carries `doc_date: 2025-12-30`.
   **Build requirement:** cross-check `doc_date` against any date embedded in `file_name`.
   On conflict, prefer the filename date and flag the record.

3. **Entity resolution is fragmented.**
   "Ivy Rehab" resolves to 16 candidates across 8 distinct `company_entity_id` values
   (Ivy Rehab Network ~4,676 docs, Ivy Rehab Physical Therapy ~145, Ivy Rehab for Kids ~175,
   plus low-confidence variants).
   **Build requirement:** maintain an explicit alias map for the 17 portcos rather than
   relying on `resolve` at runtime. Never filter by a single `company_id` for a portco
   without checking the alias set.

4. **`query_structured` against the `kv` space is not provisioned.** Only `dealcloud` works.
   Document-extracted tables are not queryable.

5. **`entity_facts` is Phase 2 and disabled.** Cross-document fact time series unavailable.

6. **`recall_user_context` requires interactive approval.** Not usable in an unattended job.

### BLOCKER - ingestion lag

As of 2026-08-26, the most recent CIM in the document layer is dated **2026-06-30**.
DealCloud shows deals logged through **2026-08-24**. That is roughly an eight-week gap.

A Friday job querying "ingested in the past 7 days" will most likely return zero CIMs and
send an empty digest, which is worse than not sending.

**Build requirements:**
- Pre-flight check: if zero CIMs found in window, do NOT send. Alert Prithvi instead.
- Escalate the lag itself to Sai / the KV extraction pipeline owner. This is a prerequisite,
  not a nice-to-have.
- Interim: the digest window may need to be "ingested since last digest" rather than a
  strict 7-day lookback, to catch backfill when the lag closes.

---

## 6. Per-CIM scan procedure

For each CIM, extract and record:

### Metadata
- Company name and project codename
- Sector / what the business actually does (one line, plain language)
- Document type and date (CIM / CIP / IM)
- Banker, if identifiable
- `web_url` for the source PDF

### Classification
- Tier (0-4)
- Supplementary tags (§3)

### Note content (only if tier >= 2, or tier <= 1 with portfolio relevance)

Five fields, in this order:

1. **What it is** - one line on the business. Include only when the reader would not
   otherwise know the company. Skip for well-known names.
2. **What they did** - the mechanism, with the seller's own numbers. Not adjectives.
   "Put AI-embedded productivity into the margin walk as a named driver" - not
   "leverages AI for efficiency."
3. **Evidence** - what is checkable and what is not. Name the gap explicitly. This bullet
   replaced the RYG badge and carries its full weight, so it must be specific.
   Good: "Market sizing is specific and internally consistent... No named customer, no
   company-level P&L proof."
   Bad: "Evidence is moderate."
4. **Read** - agent inference. Why this matters. Must be marked as inference (§8).
5. **Relevant portcos** - sub-bulleted, each with a `because` clause tied to that portco's
   specific situation. Never a bare list of names.

### Exhibit
- Page number(s), pinned **at extraction time**. See §9.

### Hard rule

**Every note names at least one portco and at least one question.** If neither can be
written, the note is not written. This is the forcing function that prevents degradation
into a summary feed.

---

## 7. Lead item / escalation criteria

A note is promoted to lead item only if it changes a decision someone is currently holding:

- Touches a live process (portco in market or approaching)
- Touches an in-flight initiative (an active AI workstream at a portco)
- Challenges a thesis assumption (e.g. that a services business's revenue is durable)

Target frequency is roughly one per month. **If lead items are firing weekly, the bar has
slipped and should be reviewed.**

At most one lead item per digest. If two qualify, pick the one with the shorter fuse and
demote the other to its tier section.

If none qualify, the digest opens directly at Tier 4 with no lead item. Do not manufacture one.

---

## 8. Voice and attribution rules

The email sends from the agent, not from Prithvi. This has a specific consequence.

**Sourced fact and agent inference must be visually separable.** A reader must never have to
guess which is which.

- `What it is`, `What they did`, `Evidence` - sourced from the document only. No inference.
- `Read` - agent inference. This is where the "why interesting" judgment lives.
- `Relevant portcos` - inference, but grounded. Each `because` clause should reference a
  known fact about that portco (from maturity reports, board materials, or the exposure map).

### Style

WCP house style applies:
- Lead with the answer. Rationale follows.
- No em-dashes. Use a hyphen with spaces ( - ).
- No mid-sentence bolding.
- Never open with affirmations ("great question," "notably," "importantly").
- Match length to content. Do not pad a thin note to match a rich one.
- PE vocabulary without definition: portco, EBITDA, MOIC, hold period, add-on, platform,
  IC, CIM, FDD, QoE, LOI, value creation, multiple expansion.

### Footer (required on every send)

```
Generated by Claude against the WCP Knowledge Vault. Portfolio inferences are
agent-generated and unreviewed. Reply to Prithvi with corrections.
```

---

## 9. Exhibit rendering

**Status: not built. This is net-new work.**

Requirement: when a note references a specific exhibit (an EBITDA walk, a market structure
chart, a cost-stack chart), include a rendered image of that page inline.

### Pipeline

```
web_url (SharePoint) -> fetch PDF -> rasterize target page to PNG -> embed in email
```

### Requirements

- Page number must be pinned **at extraction time**, not reconstructed later. Two entries in
  the current draft carry "page unconfirmed" because `section_path` came through without a
  page marker. That string must never appear in a live send.
- If a page cannot be pinned, fall back to a link with the section name and omit the image.
  Do not guess a page number.
- Test first on the Softdocs (HAVEN) margin expansion bridge. That is the exhibit readers
  will most want to see and the best validation case.

---

## 10. Portfolio exposure map

The reusable asset that makes matching fast. Build once, maintain quarterly.

For each of the 17 portcos, record four attributes:

| Attribute | Question |
|---|---|
| `labor_linked_revenue` | Does revenue price off headcount or hours? Determines exposure to services-to-software displacement. |
| `admin_fte_concentration` | Where is back-office headcount concentrated, and how large? Determines automation opportunity size. |
| `referral_constrained` | Is growth bound by referral volume rather than cost? Determines whether AI-as-credibility beats AI-as-savings. |
| `services_layer_position` | Does it have a services layer that could be displaced, or could it become the application layer? |

### Portfolio companies

Ivy Rehab, Altocare, TeamSnap, Apotheco, Fusion Health, UVP, Talogy, Career Certified,
Mopec, PromptCare, PNH, APDerm, Concierge Home Care, HSI, Science Exchange, Peritia,
PracticeTek.

### Known inputs already in the Vault

Use these to seed the map rather than starting from scratch:

- **UVP AI Maturity & Value Creation Report** (2025-12-12) - 50+ FTE in RCM/Operations,
  7/10 readiness, existing Waystar relationship, value pools identified for RCM automation,
  AI-powered scheduling, AI for talent acquisition.
- **PromptCare AI Maturity & Value Creation Report** (2025-11-02) - Emerging tier 1.8/5,
  below portfolio average on automation/data integration/operationalization, above average
  on RCM automation pilots.
- **Fusion Health AI Maturity & Value Creation Report** (2025-11-24) - four initiatives
  sized: recruiting, sales & segmentation, timekeeping & invoicing, coding QA & audits,
  with Deploy / Reshape / Invent classification.
- **WCP CoE Center of Excellence deck** - AI maturity assessment methodology, portfolio
  baseline approach.
- **WCP AI Strategy Partner deck** - Level 1-4 firm maturity ladder (Automate Faster /
  Think with AI / Do What Was Below the ROI Line / Build Proprietary Tools off Proprietary
  Data).

Also available: `wcp-portfolio-kb` organization skill.

---

## 11. Delivery

| Field | Value |
|---|---|
| Sender | Claude (WCP AI Agent) |
| Recipients | Prithvi Raj, Doug Rassner, rwaud2 |
| Schedule | Friday morning |
| Subject format | `Weekly AI-in-CIMs scan - {n} ingested, {m} with signal` |
| Transport | Microsoft 365 MCP (`outlook_create_draft` then `outlook_send_draft`) |

### Phasing

- **Phase 1 (target: this Friday):** agent generates Friday morning, Prithvi reviews, then
  sends. Draft created via `outlook_create_draft`; send is a separate explicit step.
- **Phase 2 (target: ~2 weeks, gated on ingestion fix + exhibit rendering):** unattended send.

Do not move to Phase 2 until two consecutive reviewed sends have gone out without
correction.

### Window language

Use **"ingested in the past 7 days"** or **"ingested since last digest."**
Never "last week" or "new this week" - the CIMs themselves may be months old. The claim is
about ingestion, not origination.

---

## 12. Output template

````markdown
**From:** Claude (WCP AI Agent)
**To:** Prithvi Raj, Doug Rassner, rwaud2
**Subject:** Weekly AI-in-CIMs scan - {n} ingested, {m} with signal

Automated weekly scan of CIMs ingested into the Knowledge Vault in the past 7 days, read for
how sellers substantiate AI claims and what those claims imply for the WCP portfolio. Sourced
facts are drawn from the documents; items marked **Read** are agent inference. Tier
definitions at the bottom.

---

## Lead item: {one-line framing of why this changes something}

{2-4 paragraphs. The mechanism, the numbers, why the specific vertical does not matter, and
which portcos sit on either side of it.}

**Read:** {the agent's call on where this belongs and who should own it.}

[Exhibit: p.{n}, {description}] · [CIM]({web_url}) · Full entry under Tier {n}.

---

# Tier 4 - Underwritten in the EBITDA bridge

### {Company} ({Project})
*{sector} · {doc_type} {month year}{ · banker}*

- **What it is:** {one line}
- **What they did:** {mechanism with seller's numbers}
- **Evidence:** {what is checkable, what is not, named gap}
- **Read:** {agent inference}
- **Relevant portcos:**
  - {Portco} - {because clause tied to that portco's specific situation}
  - {Portco} - {because clause}
- **Exhibit:** p.{n}, {description} · [CIM]({web_url})

---

# Tier 3 - Quantified operationally, not in the bridge
{entries}

# Tier 2 - Positioned as capability, no economics
{entries}

# Tier 1 - Ambient market context
{entries}

# Tier 0 - Silent
- **{Company}** · {sector} · {doc}. {Portfolio relevance if any, else omit entirely.}
  {One or two lines max.} [CIM]({web_url})

---

*Tier 4 - AI named in the EBITDA bridge or margin walk; a buyer can underwrite or discount
it. Tier 3 - quantified operationally (hours, FTEs, cycle time, revenue per head) but not
carried into the bridge. Tier 2 - positioned as a capability; roadmaps, architecture,
feature lists, no economics. Tier 1 - ambient; AI describes the market, not the company's
economics. Tier 0 - silent.*

*Generated by Claude against the WCP Knowledge Vault. Portfolio inferences are
agent-generated and unreviewed. Reply to Prithvi with corrections.*
````

Notes on the template:
- Omit any tier section that has no entries. Do not print an empty header.
- Tier 0 entries are one or two lines only, and only when there is portfolio relevance
  (e.g. a direct comp). Otherwise log and omit.
- The lead item duplicates a full entry further down. That is intentional - the lead is the
  framing, the entry is the detail.

---

## 13. Acceptance criteria

The build is done when all of the following pass:

1. A CIM landing in the Vault triggers a scan without manual invocation.
2. Tier classification on the 18-CIM May-June baseline matches the reference classification
   in §14 for at least 16 of 18. Disagreements must be explainable, not arbitrary.
3. Every generated note names at least one portco with a `because` clause.
4. No note is generated that names zero portcos.
5. All filtered `search_evidence` calls assert `filter_fallback === false`.
6. Zero CIMs in window produces an alert to Prithvi, not an empty send.
7. Every exhibit reference carries a pinned page number or falls back to a link with no
   image. The string "page unconfirmed" never appears in output.
8. Digest renders with tier sections in descending order, empty sections omitted.
9. Footer attribution present on every send.
10. No em-dashes anywhere in output.

### Regression test

Run against the May-June 2026 cohort and compare to §14. This is the golden set.

---

## 14. Reference classification - May/June 2026 baseline

The golden set. 18 CIMs identified in the document layer for the May-June 2026 window.
Tier assignments below are the reference.

| Company | Project | Sector | Date | Tier | Note |
|---|---|---|---|---|---|
| Softdocs | HAVEN | Higher-ed doc mgmt SaaS | 2026-06 | 4 | AI in margin walk, COGS 25.6% -> 18.6% |
| RxLogix | Sunrise | Pharmacovigilance software | 2026-05-21 | 3 | Services-to-software displacement thesis |
| Definitive Media | Turbo | Clinical trial tech | 2026-05-06 | 3 | Revenue per FTE, names model stack |
| Health Admins | Longhorns | TPA | 2026-05-01 | 2 | Agentic roadmap + unlinked headcount cut |
| BryteBridge | Starlight | Compliance filings | 2026-06-01 | 2 | Agentic marketing engine, CAC claims |
| CampusESP | RLS | Higher-ed engagement | 2026-05-01 | 2 | Agentic layer over Q&A |
| Wellnecity | Bobcats | Benefits analytics | 2026-05-01 | 2 | AI/ML insights in dated product roadmap |
| ENET Holdings | Carrera | Energy transaction data | 2026-05-01 | 2 | AI/ML predictive valuation, future state |
| Mantra Health | Matterhorn | Behavioral health | 2026-04-30 | 2 | "Advantageous AI entry strategy" |
| ImageCare Radiology | Goldfinch | Outpatient imaging | 2026-05-01 | 1 | FDA-cleared AI as referral credibility |
| DynamicAccess | Florence | Vascular access | 2026-06-01 | 1 | Tech platform differentiation |
| Quantilope | Apex | Market research SaaS | 2026-04-21 | 2 | $15M invested 2023-25, data moat claim |
| Kinexon | New York | Sports/industrial IoT | 2026-04-01 | 2 | "Proprietary AI flywheel," no numbers |
| H2 Health | - | Outpatient PT, 271 clinics | 2026-06-30 | 0 | Direct Ivy comp, zero AI content |
| Harmar MidCo | Empower | Mobility products | 2026-05-01 | 0 | A/P optimization, FedEx contract |
| ADL Final Mile | Omaha | Final-mile logistics | 2026-06-09 | 0 | Bridge from implemented savings |
| Jones Technical Institute | Steven | Trade education | 2026-05-01 | 0 | Margin from scale, not AI |
| Elite Medical Staffing | Arnie | Healthcare staffing | 2026-03 | 0 | - |

### Reference finding

Roughly 6% Tier 4 overall. **Zero Tier 4 in healthcare services.** Healthcare clusters at
Tier 0-1; software clusters at Tier 2-4. The software-minus-healthcare gap is the structural
observation the digest exists to track qualitatively.

Additional Tier 4 examples from outside the window, useful as calibration anchors:
- **Percipience (Project Hummingbird, Sept 2025)** - best-constructed AI value case in the
  full corpus. Named client MSIG, realized vs projected split: ~$3M realized savings, 40%
  underwriting process improvement across 11.8k submissions, $5M+ projected over three
  years, $21M+ total quantified benefit.
- **Med Learning Group (Project Slapshot)** - AI enablement as a discrete bar in the
  2026B-2031E margin bridge, 31.8% to 34.2%.
- **FunctionAbility (Project Domus, June 2025)** - only healthcare services CIM in the corpus
  with a "Realized Benefits From Automation" exhibit. 2 FTE saved in back-office.

Calibration anchor at the bottom:
- **Claira (Project Focus, 2025)** - AI-native positioning built on press clippings, with the
  cost argument being that OpenAI API pricing will decline. A dependency described as an
  advantage. Tier 2, weakest evidence in the corpus.

---

## 15. Worked example

The full current draft of the digest - lead item plus all five tier sections plus Tier 0
entries - is the reference output. It is reproduced in the conversation this spec was
derived from and should be pasted into the repo as `reference-digest.md` before building.

Key structural features to preserve:
- Lead item sits above Tier 4 and duplicates content from a lower-tier entry.
- Portco bullets carry `because` clauses, never bare names.
- Evidence bullets name the specific gap.
- Tier 0 entries are one or two lines and only appear when portfolio-relevant.

---

## 16. Open questions for the builder

1. **Note storage.** Where do accumulated notes live between digests? Options: a SharePoint
   markdown file, a Databricks table, or a local repo file. Needs to survive the week and be
   queryable by date. Recommend simplest durable option.
2. **Backfill on lag close.** When the ingestion gap closes, a large batch will land at once.
   Should the first post-fix digest cover everything, or should backfill be a separate
   one-time report? Recommend a separate one-time report to avoid a 40-entry email.
3. **Tier boundary 3/4.** Softdocs names AI as a driver without isolating the dollars.
   Current spec calls that Tier 4. The stricter reading requires separate sizing. Decision:
   naming it as a bridge driver is sufficient for Tier 4. Isolated sizing is better but not
   required. Flag if this produces false positives in testing.
4. **Non-CIM documents.** Management presentations, teasers, and IC memos also contain AI
   content. Out of scope for v1. Revisit after the CIM flow is stable.

---

## 17. Immediate prerequisites

Ordered. The first is blocking.

1. **Close the ingestion lag.** Documents stop at 2026-06-30; DealCloud runs to 2026-08-24.
   Owner: Sai / KV extraction pipeline. Without this, Friday sends an empty email.
2. **Pin pages at extraction.** `section_path` alone is insufficient. Two current entries
   carry "page unconfirmed."
3. **Build exhibit rendering.** Test on the Softdocs margin bridge.
4. **Build the portfolio exposure map.** Four columns, 17 rows. Seed from the maturity
   reports in §10.
