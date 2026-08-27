# Per-CIM scan procedure (Trigger A)

Instructions for a Claude session scanning newly ingested CIMs. Follow in order. The spec
(`SPEC.md`) is the authority; this file is the operational sequence.

## 0. Load context

1. Read `framework/tiers.md` (classification), `data/portco-aliases.json` (entity ids),
   `data/exposure-map.md` (portco matching), `state.json` (what has already been scanned).
2. All retrieval is via the Knowledge Vault Documents MCP server. `answer_question` is
   heavier - prefer `search_evidence` with explicit filters.

## 1. Discovery - find CIMs not yet scanned

There is no ingestion-timestamp filter and no list-documents endpoint on the KV server.
The tools filter by `doc_date`, which is the document's date, not when it landed.
Discovery therefore works by wide-window probing plus doc_id diffing:

1. Run `search_evidence` with `filters: {doc_type: "cim", doc_date_gte: <12 months back>}`
   and `k: 50`, once per probe question. Use at least three probes so no single embedding
   angle misses a document: "confidential information memorandum", "investment highlights
   and transaction overview", "financial overview EBITDA growth".
2. Union the `doc_id` values across probes. Any `doc_id` not in `state.json.scanned` is
   treated as newly ingested.
3. The 12-month window plus doc_id diffing is what makes backfill safe: when the ingestion
   lag closes, months-old CIMs will appear as new doc_ids and get scanned then.

### Non-negotiable tool guards (verified defects, spec section 5)

- **`doc_type` is lowercase `"cim"`.** The filter is case-sensitive and fails soft:
  `"CIM"` silently returns unfiltered results with `filter_fallback: true`.
- **Assert `filter_fallback === false` on every filtered call.** If true, abort the run
  and alert Prithvi. Never proceed on a silent fallback.
- **Cross-check `doc_date` against any date embedded in `file_name`** (e.g. a file named
  "Overview 11.29.21" carrying `doc_date: 2025-12-30`). On conflict, prefer the filename
  date and set `doc_date_flagged: true` in the note frontmatter.
- **Never use `query_structured` against the `kv` space** (not provisioned; `dealcloud`
  only). **Never call `recall_user_context`** (requires interactive approval; hangs
  unattended jobs).

## 2. Per-document extraction

For each new doc_id, retrieve enough of the document to classify. Scope every call with
`filters: {doc_type: "cim", company_id: <the doc's company_entity_id>}` and assert
`filter_fallback === false`. Run targeted probes:

- "AI in the EBITDA bridge, margin walk, or pro forma adjustments" (Tier 4 test)
- "AI automation quantified - hours saved, FTEs, cycle time, revenue per employee" (Tier 3)
- "AI product capabilities, roadmap, architecture, machine learning features" (Tier 2)
- "AI in market growth, industry tailwinds, TAM" (Tier 1)
- "headcount reduction or cost savings from automation" (tag: headcount_action_attributed_to_ai)
- "OpenAI Anthropic model provider large language model" (tag: model_provider_named)
- "agentic" (tag: agentic_language)

Record metadata: company name, project codename, sector and what the business actually
does in plain language, doc type and date (CIM / CIP / IM), banker if identifiable from
the disclaimer pages, and `web_url`.

Then classify: tier 0-4 per `framework/tiers.md`, plus supplementary tags. Sanity-check
against the calibration anchors and the golden set (`reference/golden-set.md`).

### Portco identity guards

- A CIM's target may itself collide with a portco name. Known trap: "IPS Group, Inc."
  (Project Burgundy) is not PracticeTek (f/k/a Integrated Practice Solutions). Check
  `data/portco-aliases.json` `_meta.warnings` before asserting any portco relationship.
- When matching a CIM's relevance to a portco, reason from `data/exposure-map.md`
  attributes, not name similarity.

## 3. Note generation

Decision gate, in order:

- Tier >= 2: generate a full note.
- Tier <= 1 but portfolio-relevant (e.g. a direct comp to a portco, like H2 Health vs
  Ivy Rehab): generate a short entry (one or two lines).
- Tier 0 and not portfolio-relevant: log to `state.json` only. No note.

**Hard rule: every note names at least one portco and at least one question. If neither
can be written, the note is not written** (it is still logged as scanned). This is the
forcing function that prevents degradation into a summary feed.

Full note body - five fields, this order, no others:

1. **What it is** - one line on the business. Skip for well-known names.
2. **What they did** - the mechanism, with the seller's own numbers. Not adjectives.
   "Put AI-embedded productivity into the margin walk as a named driver," not
   "leverages AI for efficiency."
3. **Evidence** - what is checkable and what is not. Name the gap explicitly. This bullet
   replaced the RYG badge and carries its full weight.
   Good: "Market sizing is specific and internally consistent. No named customer, no
   company-level P&L proof." Bad: "Evidence is moderate."
4. **Read** - agent inference. Why this matters. Marked as inference by the field itself.
5. **Relevant portcos** - sub-bulleted, each with a `because` clause tied to that portco's
   specific situation per the exposure map. Never a bare list of names.

Sourcing discipline (spec section 8): fields 1-3 are sourced from the document only, no
inference. Fields 4-5 are inference, grounded in known portco facts. Portco-specific
factual claims (exit timing above all) follow this source hierarchy: Knowledge Vault
documents first (board materials, banker materials, sell-side drafts - live and dated),
then the exposure map and portfolio KB (a dated snapshot; say so when it is the source).
The reference digest is a format reference, never a fact source - statements in it are
not evidence. When citing Vault evidence, carry file_name and doc_date, and remember
doc_date lies (defect 2): a PracticeTek co-investor update from April 2024 carries
doc_date 2028-07-31.

### Exhibit reference

Pin the page number at extraction time, from `section_path` or the chunk text. If no page
marker exists, record `exhibit: null` and use a link with the section name - do not guess
a page, and never write the string "page unconfirmed" anywhere.

### Note file format

One file per CIM in `notes/`, named `YYYY-MM-DD_<codename-or-company-slug>.md` (date =
doc_date). YAML frontmatter:

```yaml
---
company: Softdocs
codename: HAVEN
sector: Higher-ed document management SaaS
doc_type: CIM
doc_date: 2026-06-01
doc_date_flagged: false
doc_id: <from search_evidence>
company_entity_id: <from search_evidence>
banker: <name or null>
web_url: <SharePoint url>
tier: 4
tags: [model_provider_named]
exhibit_page: 38          # or null
exhibit_desc: Margin expansion bridge
scanned_at: 2026-08-28
lead_candidate: false     # see step 4
---
```

Body: the five fields as bold-labeled bullets, in the digest entry format (spec section 12).
Style: WCP house style - lead with the answer, no em-dashes (hyphen with spaces), no
mid-sentence bolding, match length to content.

## 4. Escalation evaluation

Mark `lead_candidate: true` only if the note changes a decision someone is currently
holding:

- Touches a live process (portco in market or approaching)
- Touches an in-flight initiative (an active AI workstream at a portco)
- Challenges a thesis assumption (e.g. that a services business's revenue is durable)

Target frequency is roughly one per month. If lead candidates are firing weekly, the bar
has slipped - say so in the digest run rather than promoting them all.

## 5. Persist

1. Append every scanned doc_id to `state.json.scanned` with `{doc_id, company, tier,
   noted: true|false, scanned_at}`.
2. Commit notes + state with message `cim-scan: scan <N> CIMs (<date>)` and push.
3. If any run-level guard fired (filter_fallback true, zero results on all probes when
   documents were expected), alert Prithvi instead of failing silently.
