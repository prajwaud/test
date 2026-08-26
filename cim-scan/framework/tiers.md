# Tier framework

The single classification axis. Applied to every CIM. Source of truth: `../SPEC.md` section 3.

| Tier | Definition | Test |
|---|---|---|
| **4** | AI named in the EBITDA bridge, margin walk, or pro forma adjustments | Can a buyer underwrite or discount it as a number? |
| **3** | Quantified operationally - hours, FTEs, cycle time, revenue per head - but not carried into the bridge | Are there real numbers that are not P&L numbers? |
| **2** | Positioned as capability. Roadmaps, architecture diagrams, feature lists | Is AI described as something the company has, with no economics? |
| **1** | Ambient. AI describes the market or sector, not the company's economics | Does AI appear only in market tailwinds or industry context? |
| **0** | Silent. No substantive AI mention | |

There is one badge, not two. Evidence quality is carried in prose in the Evidence bullet,
never as a second badge. Known cost, accepted: ordering by tier alone can bury a
well-evidenced Tier 1 beneath a poorly-evidenced Tier 2.

## Boundary rulings

- **3 vs 4:** Naming AI as a driver in the bridge or margin walk is sufficient for Tier 4,
  even without isolated dollar sizing (per spec section 16, decision 3 - Softdocs precedent).
  Isolated sizing is better but not required. If testing shows this producing false
  positives, flag to Prithvi rather than silently tightening.
- **2 vs 3:** The number must be the company's own operational metric. A vendor's claimed
  benchmark ("tools like ours save 30%") is Tier 2.
- **1 vs 2:** Tier 2 requires the company to claim AI as something it has or is building.
  AI in the competitive landscape or TAM narrative alone is Tier 1.
- **0 vs 1:** A single boilerplate mention ("we monitor emerging technologies including AI")
  is still Tier 0. Tier 1 requires AI to do real work in the market framing.

## Supplementary tags

Captured alongside the tier on every note. Not reported in the digest, but trended
separately - these move faster than tiers.

- `model_provider_named` - seller discloses OpenAI / Anthropic / other. Emerging disclosure
  norm and the dependency handle for diligence.
- `agentic_language` - the word "agentic" appears. Vocabulary drift indicator.
- `ai_in_market_sizing` - AI appears in TAM or market structure, not just product. A more
  aggressive claim than product positioning.
- `headcount_action_attributed_to_ai` - the leading indicator. A cost or headcount reduction
  explicitly linked to automation. The first healthcare CIM that does this is the inflection
  point. Flag prominently when true.

## Calibration anchors

Use these to sanity-check a classification before writing the note.

**Top of the scale:**
- **Percipience (Project Hummingbird, Sept 2025)** - best-constructed AI value case in the
  corpus. Named client MSIG, realized vs projected split: ~$3M realized savings, 40%
  underwriting process improvement across 11.8k submissions, $5M+ projected over three
  years, $21M+ total quantified benefit. Tier 4 with strong evidence.
- **Med Learning Group (Project Slapshot)** - AI enablement as a discrete bar in the
  2026B-2031E margin bridge, 31.8% to 34.2%. Tier 4.
- **Softdocs (Project HAVEN, June 2026)** - AI in the margin walk as a named driver,
  COGS 25.6% to 18.6%, without isolated dollar sizing. Tier 4 by the boundary ruling above.
- **FunctionAbility (Project Domus, June 2025)** - only healthcare services CIM in the
  corpus with a "Realized Benefits From Automation" exhibit. 2 FTE saved in back-office.

**Bottom of the scale:**
- **Claira (Project Focus, 2025)** - AI-native positioning built on press clippings, with
  the cost argument being that OpenAI API pricing will decline. A dependency described as
  an advantage. Tier 2, weakest evidence in the corpus. If a note reads like Claira,
  the Evidence bullet must say so.

**The structural observation this instrument tracks:** software clusters at Tier 2-4,
healthcare services clusters at Tier 0-1, roughly 6% Tier 4 overall and zero Tier 4 in
healthcare services as of the May-June 2026 baseline. Watch for the first healthcare
services CIM that breaks the pattern.
