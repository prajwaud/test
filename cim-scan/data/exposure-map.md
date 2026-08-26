# Portfolio exposure map

The reusable asset that makes CIM-to-portco matching fast (spec section 10). Four
attributes per portco. Every `Relevant portcos` because-clause in a note should trace to
a fact here.

Seeded 2026-08-26 from: the March 2026 Portfolio Context & Knowledge Base (via the
wcp-portfolio-kb org skill), the maturity reports named in spec section 10 (UVP 2025-12-12,
PromptCare 2025-11-02, Fusion Health 2025-11-24), and agent inference where no source
exists. Tags: [KB] = March 2026 knowledge base, [MR] = maturity report per spec,
[Likely] / [Guessing] = agent inference, unreviewed. Maintain quarterly; Prithvi has not
reviewed this seed.

Attribute definitions:
- `labor_linked_revenue` - does revenue price off headcount or hours? Exposure to
  services-to-software displacement.
- `admin_fte_concentration` - where is back-office headcount concentrated, how large?
  Automation opportunity size.
- `referral_constrained` - is growth bound by referral volume rather than cost? Whether
  AI-as-credibility beats AI-as-savings.
- `services_layer_position` - does it have a services layer that could be displaced, or
  could it become the application layer?

---

## Healthcare services

### Ivy Rehab (outpatient PT, 354+ clinics)
- labor_linked_revenue: Yes - visit/unit-based clinician revenue; payroll ~50% of revenue [KB].
- admin_fte_concentration: Front desk, scheduling, and centralized RCM; documentation burden on therapists [Likely].
- referral_constrained: Yes - physician referral volume drives visits; volumes were soft in 3Q25 (visits -4.4%) [KB].
- services_layer_position: Pure services; documentation (scribe), scheduling, and payor contracting analytics are the automatable layer [Likely]. Watch any PT/rehab CIM (H2 Health is a direct comp).

### PromptCare (specialty infusion + complex respiratory)
- labor_linked_revenue: Partially - nursing/RT hours deliver care but revenue is per-script/per-patient [Likely].
- admin_fte_concentration: Intake, benefits verification, and RCM (denials, collections) on a ~$550M+ revenue base; DSO reduction is a named lever [KB]. Above portfolio average on RCM automation pilots, otherwise Emerging tier 1.8/5 [MR].
- referral_constrained: Yes - hospital discharge and physician referrals [Likely].
- services_layer_position: RCM and intake automation are the opportunity; uneven acquired-entity data quality is the named AI risk [KB]. 12-month exit window limits scope [KB].

### UVP (ophthalmology/optometry platform)
- labor_linked_revenue: Yes - provider visit and procedure revenue; provider shortages cap growth [KB].
- admin_fte_concentration: 50+ FTE in RCM/Operations [MR]; call center, scheduling, cancellation recovery named as the only AI scope for the exit window [KB].
- referral_constrained: Partially - optometry-to-surgical referral funnel matters; access/throughput is the binding constraint [Likely].
- services_layer_position: Services with an automatable access/RCM layer; existing Waystar relationship is the vendor handle [MR]. 6-12 month exit window - CIM findings here are exit-narrative-relevant, not build-relevant [KB].

### Altocare (senior care franchise + staffing)
- labor_linked_revenue: Yes for staffing (caregiver hours); franchise royalty stream is not [KB].
- admin_fte_concentration: Franchise support, scheduling, payroll; franchisee data fragmented [KB].
- referral_constrained: Growth binds on franchisee recruitment and caregiver supply more than referrals [KB].
- services_layer_position: Care delivery not displaceable; franchisee back-office and central support are the automatable layer [Likely].

### Apotheco (specialty dermatology pharmacy)
- labor_linked_revenue: No - per-script economics, but thin 4% EBITDA margin makes labor cost per script decisive [KB].
- admin_fte_concentration: Prior auth and appeals processing is the named efficiency lever; ~60K+ scripts/month [KB].
- referral_constrained: Yes - ~3,500+ prescribing dermatologist relationships are the volume engine; AI-as-credibility with prescribers matters [KB].
- services_layer_position: PA automation could displace or supercharge its own ops; exit narrative as tech-enabled pharmacy platform makes seller AI framing in pharmacy CIMs directly relevant [KB]. 12-month exit window [KB].

### PNH (multi-segment healthcare services + supply chain)
- labor_linked_revenue: Mixed across segments [Guessing - segment detail is a data gap].
- admin_fte_concentration: RCM (triage, denial prevention, collections) is the primary EBITDA lever [KB].
- referral_constrained: Varies by segment [Guessing].
- services_layer_position: Severe data fragmentation prevents AI deployment today; ~2-3% margin leaves no room for AI spend error [KB]. CIM lessons here are mostly cautionary comps.

### APDerm (dermatology, MA/NH)
- labor_linked_revenue: Yes - provider visit revenue; mix shifting to aesthetics [KB].
- admin_fte_concentration: Scheduling, RCM, prior auth across 8 locations [Likely].
- referral_constrained: Partially - PCP referrals for medical derm, direct-to-consumer for aesthetics [Likely].
- services_layer_position: Ambient documentation and PA automation are the standard plays; regional scale limits build appetite [Likely].

### Concierge Home Care (home health, NE Florida)
- labor_linked_revenue: Yes - visit-based, Medicare-concentrated [KB].
- admin_fte_concentration: Intake, OASIS documentation, coding, scheduling [Likely]; below-market margins (10.9%) make back-office cost material [KB].
- referral_constrained: Yes, strongly - hospital and physician referral relationships drive census; AI-as-credibility with referral sources beats AI-as-savings here [Likely].
- services_layer_position: OASIS coding and documentation automation is the canonical home-health use case [Likely]. KB visibility is stale (2019-era data) - verify before strong claims [KB].

### Fusion Health (locums staffing + MA in-home evaluations)
- labor_linked_revenue: Yes - the purest case in the portfolio: revenue prices off placed clinician hours [KB]. Highest services-to-software displacement exposure; any staffing CIM claiming AI-driven recruiter productivity is directly relevant.
- admin_fte_concentration: Recruiting, credentialing, timekeeping and invoicing; four initiatives sized: recruiting, sales & segmentation, timekeeping & invoicing, coding QA & audits, with Deploy / Reshape / Invent classification [MR].
- referral_constrained: No - growth binds on clinician supply and client demand [KB].
- services_layer_position: Classic displacement target; organizational distress currently consumes management attention, so findings are watch-list, not action items [KB].

## Software / technology

### PracticeTek (retail health practice management SaaS + payments)
- labor_linked_revenue: No - SaaS + payments attach [KB].
- admin_fte_concentration: Support and onboarding across 15+ acquired brands; integration complexity is the constraint [KB].
- referral_constrained: No [KB].
- services_layer_position: Is the application layer for ~42K practices; agentic front-desk and RCM features in competitor CIMs are direct product-roadmap signal [Likely]. Do not confuse with IPS Group (Project Burgundy) - see alias map warnings.

### TeamSnap (youth sports SaaS)
- labor_linked_revenue: No [KB].
- admin_fte_concentration: Support and sales; over-automation already flagged as a lead-quality risk [KB].
- referral_constrained: No - payments penetration and TS ONE migration are the levers [KB].
- services_layer_position: Application layer; AI is product surface, not cost story [Likely].

### Talogy (talent assessment SaaS + services)
- labor_linked_revenue: Partially - services/consulting delivery and report generation consume billable capacity [KB].
- admin_fte_concentration: Report generation and RFP solutioning are the named automation levers [KB].
- referral_constrained: No [KB].
- services_layer_position: High AI existential risk - core assessment workflows exposed to substitution; regulatory scrutiny on AI in employment decisions cuts both ways [KB]. Any CIM claiming AI-native assessment or agentic HR tooling is directly relevant.

### Career Certified (compliance education platform)
- labor_linked_revenue: No [KB].
- admin_fte_concentration: Content production and course maintenance [Likely].
- referral_constrained: No - CAC/marketing-driven; churn-sensitive valuation [KB].
- services_layer_position: Content commoditization risk is named: AI-native competitors can replicate course content at lower cost [KB]. CIMs claiming AI content generation economics (e.g. agentic marketing engines, CAC claims) are directly relevant.

### HSI (EHS training and compliance SaaS)
- labor_linked_revenue: No [KB].
- admin_fte_concentration: Content production; ops leverage is the margin story (44-45% toward 50%+) [KB].
- referral_constrained: No [KB].
- services_layer_position: Application layer; training-content generation claims in ed/compliance CIMs are comp signal [Likely].

### Science Exchange (biopharma R&D procurement orchestration)
- labor_linked_revenue: No - platform take-rate/SaaS [KB].
- admin_fte_concentration: Supplier onboarding and sourcing ops [Likely].
- referral_constrained: No - enterprise sales cycle is the constraint [KB].
- services_layer_position: Could become the agentic application layer over its ~$350M order-level dataset; the named risk is giving AI away free instead of pricing it [KB]. CIMs that price AI SKUs (vs bundling) are directly relevant.

## Industrial / life sciences services

### Mopec (pathology equipment, consumables, service)
- labor_linked_revenue: No - product and service-contract revenue [KB].
- admin_fte_concentration: Quoting, order management, field-service dispatch; ERP migration consuming bandwidth [KB].
- referral_constrained: No - capital sales cycle [KB].
- services_layer_position: Low displacement exposure; install-base intelligence (renewal/cross-sell prediction) is the AI opportunity [KB].

### Peritia (pharma services platform, f/k/a PharmAlliance)
- labor_linked_revenue: Yes - consulting/services hours [Likely]. Note: the March 2026 KB covers BioBridges, not Peritia; BioBridges attributes (308 billable consultants, AI copilots for protocol drafting and regulatory content, commoditization risk if AI erodes consulting value) are the closest available proxy [KB, stale].
- admin_fte_concentration: Project staffing, utilization matching [Likely].
- referral_constrained: Relationship/BD-driven rather than referral-constrained [Guessing].
- services_layer_position: Medical writing and regulatory content are directly genAI-exposed - both as displacement risk and as an AI-enabled delivery opportunity [Likely]. Services-to-software CIM theses (e.g. RxLogix/Sunrise) are directly relevant.

---

Open items for Prithvi's review: PNH segment detail, Peritia identity vs BioBridges in the
KB, Concierge staleness, and whether EHSInsight is an HSI add-on (alias map).
