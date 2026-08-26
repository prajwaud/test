# Reference digest - PLACEHOLDER

Spec section 15 says the full current draft of the digest (lead item plus all five tier
sections plus Tier 0 entries) should be pasted here from the conversation the spec was
derived from. That conversation is not available to this build session.

**Action for Prithvi: paste the worked example here.** Until then, the output template in
SPEC.md section 12 plus the structural rules below are the only reference:

- Lead item sits above Tier 4 and duplicates content from a lower-tier entry.
- Portco bullets carry `because` clauses, never bare names.
- Evidence bullets name the specific gap.
- Tier 0 entries are one or two lines and only appear when portfolio-relevant.


Final draft below. One structural consequence of the sender change worth flagging first: the "why interesting" bullets carried your first-person inference. Coming from an agent, that voice has to change, and unmarked agent inference sitting next to sourced fact is how a reader stops being able to tell them apart. I've split them - sourced claims stay in What they did and Evidence, and the inference now sits under Read with attribution to the agent.

From: Claude (WCP AI Agent)
To: Prithvi Raj, Doug Rassner, Reeve Waud Jr.
Subject: Weekly AI-in-CIMs scan - 7 ingested, 5 with signal

Automated weekly scan of CIMs ingested into the Knowledge Vault in the past 7 days, read for how sellers substantiate AI claims and what those claims imply for the WCP portfolio. Sourced facts are drawn from the documents; items marked Read are agent inference. Tier definitions at the bottom.

Lead item: a seller is sizing services revenue as their TAM

RxLogix (Project Sunrise) builds its entire investment case on AI moving economics out of services and into software. The pharmacovigilance market is split $5.6B services / $1.25B database / $1.2B application; the services layer declines as AI automates manual work, and technology share of TAM moves from roughly 20-40% to 30-50% by 2030.

The pharmacovigilance detail is not the point. The structure is. This is a seller telling buyers that another company's services revenue is an addressable market.

WCP owns businesses on both sides of that trade. Wherever revenue prices off headcount or hours - Science Exchange, Peritia, Talogy's delivery, Career Certified, HSI - the question is whether someone is currently building a deck that sizes them. The inverse is also a live option: Talogy and HSI could be the application layer rather than the displaced one.

Read: this is an exit-timing and thesis question rather than an operations one, and likely belongs with the S&T deal leads rather than in the AI workstream.

[Exhibit: p.16, three-layer market structure] · CIM · Full entry under Tier 3.

Tier 4 - Underwritten in the EBITDA bridge
Softdocs (Project HAVEN)

Higher-ed document management SaaS · CIM June 2026

What they did: Put AI-embedded productivity into the margin walk as a named driver alongside AWS migration, platform build-out and GTM efficiency, flowing to ~30% billings-based adjusted EBITDA margin expansion 2023A to 2031P. Cost stack mapped by line, COGS 25.6% to 18.6% of billings-based revenue, AI impact assigned to R&D, S&M and G&A. There is no AI section anywhere in the deck.
Evidence: Strongest in the cohort. Because AI sits as a bridge line rather than a narrative claim, a buyer can price it directly. One gap: AI is not sized separately from the other three levers, so the dollars cannot be isolated.
Read: this is the presentation standard. Not an AI slide - a line item next to boring levers, which is what makes it read as credible.
Relevant portcos:
Ivy Rehab - the scribe work is already sized at roughly $2.4-2.6M near-term EBITDA but lives in a separate narrative rather than the bridge. This is the fix.
PracticeTek and TeamSnap - nearest-term software exits, and this is the format a buyer will expect.
Talogy - Multimodal and Parable work is currently a capability story with no P&L placement.
Exhibit: margin expansion bridge and cost-stack chart, "Drivers of EBITDA Margin Expansion" (page unconfirmed) · CIM
Tier 3 - Quantified operationally, not in the bridge
RxLogix (Project Sunrise)

Pharmacovigilance software · CIM May 2026 · Crosstree

What it is: Drug-safety case management for pharma. 14 of 14 required PV modules on a single database, positioned as the only full-stack player.
What they did: See lead item. Also claims 55-75% of all PV activity is automatable today.
Evidence: Market sizing is specific and internally consistent, and the automation claim is broken out by module - agentic, RAG and explainable AI mapped against which products carry them. No named customer, no company-level P&L proof. The market thesis is checkable against third-party PV data; the company's own share of it is not.
Relevant portcos:
Science Exchange - intermediates research services, exactly the layer an application player would target.
Peritia - delivery priced off people.
Talogy and Career Certified - assessment and instruction delivery both wrap a services layer around IP that could be automated out.
HSI - same exposure, with the option to be the application layer instead.
Exhibit: p.16, three-layer market structure · p.32, automation-by-module detail · CIM
Definitive Media Corp (Project Turbo)

Clinical trial technology · CIP May 2026

What it is: Decentralized trial platform (THREAD) plus patient voice analytics (inVibe), selling to pharma sponsors and CROs.
What they did: Denominated AI in headcount leverage rather than cost savings. $325K revenue per FTE today scaling toward $400K+. A solutions design lead goes from ~2 studies per quarter to 32 per year, taking maximum revenue per head from $400K to $1.6M, on a GenAI study builder cutting build time from 8 weeks to 2. Also: AI presentation builder 240 hours to zero, inVibe removing 4 days and 100+ hours per study, a team of three handling 9x concurrent studies.
Evidence: Most granular AI disclosure in the corpus and the only one naming its stack - OpenAI and Anthropic via AWS Bedrock. Every claim is task-level and time-denominated, so it is testable in diligence. None of it reaches the bridge, and the 4x revenue-per-head figure is explicitly flagged as still to be validated.
Read: revenue per FTE is a number buyers already track. WCP maturity reports lead with admin cost reduction percentages instead - the same work, in a currency nobody underwrites.
Relevant portcos:
Fusion Health - maturity report already sized recruiting, timekeeping and coding QA initiatives, but in ROI terms rather than per-head terms.
Science Exchange - revenue tracks coordinator headcount almost directly.
Talogy and Career Certified - delivery capacity is headcount-bound, which is what makes the reframe meaningful.
Exhibit: p.23, efficiency and economics · p.40, revenue-per-head model · CIM
Tier 2 - Positioned as capability, no economics
Health Admins (Project Longhorns)

Third-party benefits administrator · CIP May 2026

What it is: TPA administering self-funded health plans - claims processing, eligibility, member services.
What they did: Presented a comprehensive agentic roadmap to fully automate all TPA capabilities. Separately, the EBITDA adjustments summary carries a corporate headcount reduction reflecting a normalized go-forward cost structure. The document never connects the two.
Evidence: Weak on the AI itself. The roadmap is initiatives under development with no sizing, no pilot results, no timeline. The headcount adjustment is quantified but stands on its own as a cost normalization, not as an automation outcome.
Read: the sequencing lesson, cutting both ways. As a playbook - roadmaps get no credit, annualized reductions do, and the action has to land early enough to sit in the trailing period. As a diligence tell - an automation roadmap and a headcount cut sitting unlinked in the same deck is worth probing.
Relevant portcos:
UVP - maturity report shows 50+ FTE concentrated in RCM and Operations at 7/10 readiness with an existing Waystar relationship. Closest analog in the portfolio.
Mopec - AR follow-up automation already in flight; the headcount question follows directly.
PromptCare - scores 1.8/5 overall but above portfolio average on RCM automation pilots. Same shape: pilots ahead of realized reductions.
Exhibit: agentic roadmap and EBITDA adjustments summary (pages unconfirmed) · CIM
Tier 1 - Ambient market context
ImageCare Radiology (Project Goldfinch)

Outpatient diagnostic imaging, New Jersey · CIM May 2026

What it is: Multi-site outpatient imaging, positioned on payor shift away from hospital-based imaging at 2-3x the cost.
What they did: Deployed FDA-cleared AI across all 3D mammography studies, among the first radiology groups in its markets, positioned entirely as clinical credibility with referring providers. Delivered at no additional cost to patients. The EBITDA bridge ($17.5M reported to $24.2M pro forma) runs on new billing and pre-authorization contract savings plus an Aetna rate increase. AI appears nowhere in it.
Evidence: The deployment is real and verifiable - FDA clearance, applied across all studies. What is absent is any link to volume, referral capture or margin. Credible fact, no economic claim attached.
Read: healthcare's AI silence may be a deliberate choice rather than a gap. Where referral volume is the binding constraint rather than admin cost, credibility with referrers may be worth more than a savings line, and giving it away free reinforces that.
Relevant portcos:
Ivy Rehab - the ROI framing on scribe has met CFO skepticism; a referral-source framing is untested.
APDerm - derm volume is referral-driven and the same logic applies.
Concierge Home Care - referral relationships, not admin cost, are the growth constraint.
Exhibit: p.36, technology-enabled differentiation in breast imaging · EBITDA bridge (page unconfirmed) · CIM
Tier 0 - Silent
H2 Health · outpatient PT, 271 clinics · CIM June 2026. Relevant to Ivy Rehab as a direct comp. Full 2026E EBITDA bridge ($23.8M to $34.6M, p.16) built entirely from organic growth and M&A. Scalable technology infrastructure is 1 of 9 stated attributes; AI appears nowhere in the growth levers. A platform this size went to market in June with no AI story at all. CIM
Harmar (Project Empower) · mobility products · CIP May 2026. Pro forma adjustments are A/P optimization and a new FedEx contract. No portfolio read.

Tier 4 - AI named in the EBITDA bridge or margin walk; a buyer can underwrite or discount it. Tier 3 - quantified operationally (hours, FTEs, cycle time, revenue per head) but not carried into the bridge. Tier 2 - positioned as a capability; roadmaps, architecture, feature lists, no economics. Tier 1 - ambient; AI describes the market, not the company's economics. Tier 0 - silent.

Generated by Claude against the WCP Knowledge Vault. Portfolio inferences are agent-generated and unreviewed. Reply to Prithvi with corrections.

What Friday actually requires

Three things stand between this and an automated send, in order of severity.

Ingestion lag is the blocker. Documents in the Vault stop at June 30 while DealCloud shows deals logged through August 24. A job that runs Friday querying "ingested in the past 7 days" will most likely return zero CIMs and send an empty digest. That is worse than not sending. This needs Sai before anything is scheduled - it is the same defect flagged earlier this week.

Page pinning. Softdocs and Longhorns came through as section headers with no page markers. The scan has to capture the page at extraction time, not reconstruct it after. Two entries above carry page unconfirmed, which should never appear in a live send.

Slide images are not built. Rendering an exhibit means pulling the PDF from SharePoint and rasterizing the page. Tooling exists, chain does not. Worth testing on the Softdocs margin bridge first since that is the exhibit people will want to see.

Realistic call: Friday is achievable for a human-reviewed send - I generate it Friday morning, you scan it in five minutes, it goes out under the agent's name. Fully automated with images is more like two weeks, and depends on the ingestion fix landing first. I would not schedule an unattended send until it has run correctly under review twice.

One flag: earlier you said the list was Doug, RWaud and you; now R2. I have used R2. Say if that was a slip.

Next action: confirm reviewed-send for Friday, and I will write this up as a skill tonight so it generates on trigger rather than being rebuilt each week. In parallel, the ingestion lag needs to go to Sai today if Friday is real.
