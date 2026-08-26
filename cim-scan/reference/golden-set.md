# Golden set - May/June 2026 baseline reference classification

The regression target (spec sections 13-14). A build change is acceptable only if
re-classification of these 18 CIMs matches this table for at least 16 of 18, with
disagreements explainable rather than arbitrary.

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

Reference finding: roughly 6% Tier 4 overall, zero Tier 4 in healthcare services.
Healthcare clusters at Tier 0-1; software clusters at Tier 2-4. The software-minus-
healthcare gap is the structural observation the digest exists to track qualitatively.

## Known documents outside this set

A live discovery probe on 2026-08-26 surfaced June 2026 CIMs not in this table:
IPS Group (Project Burgundy, 2026-06-01), Innovative Sleep Centers (Project Lion,
2026-06-01), Venture Speech & Occupational Therapy (Project Piedmont, 2026-06-01).
The golden set is the classification reference, not an exhaustive inventory of the
window - the regression run scores only the 18 rows above, and other documents found
in the same window are scanned normally, not scored.

## Running the regression

1. Discover the May-June 2026 cohort per `../SCAN.md` step 1 with
   `doc_date_gte: 2026-03-01`, `doc_date_lte: 2026-06-30`.
2. Classify each of the 18 without consulting the Tier column (the Note column will
   leak the answer to a careless reader - classify from the documents).
3. Score matches; for each miss, write one sentence on why. 16/18 or better passes.
