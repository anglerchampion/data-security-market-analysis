# Data Security Sector - Revenue Projection

Fundamentals-based screening and three-year revenue projection for the publicly listed data security sector, built entirely from SEC filings and company earnings releases.

*Academic exercise. Not investment advice. Figures sourced from public filings as of August 2026.*

---

## Contents

- [Overview](#overview)
- [Results](#results)
- [Scope definition](#scope-definition)
- [Screening criteria](#screening-criteria)
- [The core problem: reported growth is distorted](#the-core-problem-reported-growth-is-distorted)
- [Method](#method)
- [Deriving the decay factor](#deriving-the-decay-factor)
- [Worked example](#worked-example)
- [Spreadsheet formulas](#spreadsheet-formulas)
- [Company detail](#company-detail)
- [Benchmarks](#benchmarks)
- [Market sizing](#market-sizing)
- [Limitations](#limitations)
- [Repository structure](#repository-structure)
- [Sources](#sources)

---

## Overview

The brief was to identify the highest revenue-growth companies in a chosen high-tech sub-sector and project revenue three to five years forward, using revenue alone - no profitability, cost, or valuation analysis.

Filtering the data security sector on listing, independence, and revenue-disclosure criteria reduces a universe dominated by private and acquired players to three candidates. Examination of their SEC filings shows that reported revenue growth in two of the three is materially distorted by accounting transitions rather than underlying demand — so the projection is built on subscription ARR where a clean series exists, and on reported revenue where it does not.

## Results

| Company | Projection period | 3-year revenue CAGR | Model basis |
|---|---|---|---|
| **Rubrik (RBRK)** | FY2027–FY2030 | **22.9%** | ARR growth-decay, converted to revenue |
| Varonis (VRNS) | FY2026–FY2029 | 19.2% | Revenue growth-decay |
| Commvault (CVLT) | FY2027–FY2030 | 10.2% | Flat guided growth |

Fiscal years differ across companies; periods are not calendar-aligned.

**Recommendation: Rubrik**, ranking first on both raw growth and growth quality. Its subscription ARR growth requires no adjustment for conversions or currency, whereas Varonis's headline SaaS growth substantially reflects migration of existing customers, and Commvault is guiding to growth below the estimated market rate. Rubrik's projection is supported by $2.44bn of remaining performance obligations as of 30 April 2026, approximately 53% of which is expected to be recognised within twelve months.

## Scope definition

**Industry:** Cyber Security
**Sub-industry:** Data Security (on-premise and cloud)

Securing data at rest and in transit across both on-premise and cloud environments. Segments functionally into categories including data security posture management (DSPM), data loss prevention (DLP), data access governance, encryption, and data protection / cyber recovery.

Both Rubrik and Varonis describe themselves in filings as data security companies covering cloud, on-premise, and SaaS environments, which supports the boundary independently of any single vendor's framing.

## Screening criteria

Applied as of August 2026. A company had to meet all four.

**1. High tech sector.**

**2. Publicly listed and filing with the SEC.** Restricting to SEC filers ensures comparable disclosure. Companies on non-US exchanges file under different regimes and were not assessed on a like-for-like basis.

*Excludes:* Veeam, Cohesity, Druva, Proofpoint, Forcepoint, Trellix, BigID, Cyera, Sentra, Baffle, Optiv.

Notably, the two largest players in this sub-industry are both private — Veeam at approximately $2bn annual recurring revenue, and Cohesity at roughly $1.7bn pro-forma revenue following its merger with Veritas.

**3. Independent, not acquired.** An acquired company's revenue is absorbed into the parent's reporting and can no longer be projected independently.

*Excludes:* CyberArk (Palo Alto Networks), Mandiant (Google).

Most acquisitions in this sub-industry involved private targets — Wiz into Google, Dig into Palo Alto, Symmetry Systems into Zscaler, Securiti into Veeam, Veritas into Cohesity, Armis into ServiceNow — so those companies were already excluded at criterion 2. The pattern is consistent: successful data security companies are acquired by platform vendors rather than remaining independent, which is the primary structural reason the independent public universe is small.

**4. Revenue attributable to data security separately disclosed.** A revenue projection requires a disclosed revenue series to project from. Companies selling data security bundled within a broader platform, without breaking out attributable revenue, cannot be modelled.

*Excludes:* Microsoft, IBM, Cisco, Dell, Broadcom, Google, Palo Alto Networks, CrowdStrike, Zscaler, Check Point, ServiceNow.

Exclusion under this criterion reflects disclosure practice, not market position. All remain material competitors.

Companies with separately disclosed data security revenue account for approximately $3bn of an estimated $17bn market — roughly 17%. The remainder sits with private vendors or bundled inside platforms.

**Also considered and out of scope:** Netskope (SSE/SASE) and SailPoint (identity security) are publicly listed, independent, and disclose revenue, but sell outside the defined sub-industry. Major DLP vendors are either private (Proofpoint, Forcepoint, Trellix) or bundle DLP without separate disclosure (Broadcom, Microsoft, Zscaler, Netskope).

**Remaining: Rubrik, Varonis, Commvault.**

The screen is corroborated by the companies' own disclosures. Rubrik's FY2026 10-K names Commvault, Dell EMC, IBM, Veeam and Cohesity as its main competitors; Commvault's FY2026 10-K names Rubrik, Cohesity and Veeam. Every company named by either fails one of the criteria above.

## The core problem: reported growth is distorted

Two of the three companies report revenue growth that does not reflect underlying demand, in opposite directions.

**Rubrik - inflated.** Before FY2026, Rubrik sold hardware appliances directly, and some customers held rights to free next-generation replacement hardware. Rubrik offered Subscription Credits in exchange for relinquishing those rights, and moved appliance sales to contract manufacturers. These credits are accounted for as material rights: they sit in deferred revenue and are recognised as revenue when a customer either exercises or forfeits them — with no corresponding new sale.

This inflated FY2026 reported revenue growth to 48.9%. In Q4 FY2026, $18m of revenue came from material rights; excluding it, quarterly growth was 43% rather than the reported 46%. Rubrik states the benefit continues through fiscal 2027, reducing significantly sequentially.

**Varonis - suppressed.** Varonis is migrating customers from term licences to SaaS. In Q2 2026, SaaS revenue grew 62.2% while total revenue grew only 18.3%, because term licence revenue fell from $32.4m to $4.2m and maintenance from $13.9m to $4.1m - a combined $38m decline against $66m of SaaS growth. Reported SaaS ARR growth of 52% falls to 25% excluding conversions.

**Commvault - clean.** Commvault states its transition from perpetual licensing to subscription is substantially complete, so its reported revenue requires no adjustment. It is nonetheless the slowest grower.

**Consequence for the model:** subscription ARR is unaffected by material rights recognition, so Rubrik is modelled on ARR and converted to revenue at the final step. Varonis does not disclose ARR on a consistent historical basis, but its reported revenue carries no recognition distortion — the SaaS transition is a mix shift between disclosed revenue lines, visible directly in the income statement — so it is modelled on revenue.

## Method

Revenue growth decays as a company scales: a larger base makes any given growth rate harder to sustain, and market penetration rises. The model assumes growth converges exponentially toward the sector's market growth rate.

```
g(t) = terminal + (base growth − terminal) × k^t
```

Where:

| Term | Meaning |
|---|---|
| `g(t)` | growth rate in projection year *t* |
| `terminal` | long-run growth rate the company converges toward |
| `base growth` | growth rate in the base year (*t* = 0) |
| `k` | decay factor — the proportion of the gap above terminal retained each year |
| `t` | years beyond the base year (1, 2, 3…) |

**Shared parameters:**

| Parameter | Value | Basis |
|---|---|---|
| Terminal growth | 17.12% | Sector market CAGR (Mordor Intelligence), flat market share assumption |
| Decay factor (k) | 0.77 | Derived from Rubrik's observed ARR growth deceleration, FY2025→FY2026 |

**ARR-to-revenue conversion (Rubrik only).** ARR is a point-in-time snapshot at fiscal year end; revenue accumulates across the year. Revenue therefore tracks *average* ARR, approximated by the midpoint of opening and closing:

```
Revenue = ratio × (opening ARR + closing ARR) ÷ 2
```

The ratio is calibrated against the two years where both figures are known:

| | Midpoint ARR | Revenue | Ratio |
|---|---|---|---|
| FY2026 | $1,275m | $1,320m | 1.035 |
| FY2027 | $1,647m | $1,602m | 0.973 |

FY2026 runs above 1.00 because material rights inflated revenue that year. **0.97** is used, reflecting the cleaner FY2027 relationship, and is the more conservative of the two.

**Commvault exception.** The decay framework assumes growth *above* the market rate converging *downward* toward it. Commvault's guided FY2027 growth of 10.2% already sits below the 17.12% terminal rate, so there is no gap to decay. Growth is held flat rather than converged upward, as convergence would imply a market share recovery not supported by current guidance.

## Deriving the decay factor

The decay factor is estimated from Rubrik's own disclosed exit subscription ARR, not assumed.

| FY (ends 31 Jan) | Exit subscription ARR | Growth | Gap above 17.12% |
|---|---|---|---|
| 2024 | $784m | — | — |
| 2025 | $1,090m | 39.0% | 21.91pp |
| 2026 | $1,460m | 33.9% | 16.82pp |
| 2027 (guided) | $1,834m | 25.6% | 8.50pp |

```
k = 16.82 ÷ 21.91 = 0.768 ≈ 0.77
```

The gap above terminal retained 77% of its size year over year.

**Why guidance is not used to derive k.** The FY2026→FY2027 step implies k ≈ 0.51 — materially faster decay. Guidance is typically set conservatively, and Rubrik has historically beaten it. Using it would build management's caution into the model as if it were observed deceleration. It is instead used as the bear case.

**Scenario range for Rubrik:**

| Case | k | FY2030 revenue | 3-year CAGR |
|---|---|---|---|
| Bear (guidance-implied decay) | 0.50 | $2,809m | 20.6% |
| **Base (observed decay)** | **0.77** | **$2,970m** | **22.9%** |
| Bull (slower decay) | 0.85 | $3,031m | 23.7% |

The narrow spread indicates the projection is driven primarily by the contracted base and terminal rate rather than by the decay assumption.

## Worked example

Rubrik, FY2027 → FY2028, showing every step.

**Starting point (FY2027, company guidance):** exit ARR $1,834m, revenue $1,602m, ARR growth 25.6%.

**Step 1 — FY2028 ARR growth rate**

```
Gap above terminal in FY2027 = 25.6% − 17.12% = 8.48pp
Decayed gap                  = 8.48 × 0.77   = 6.53pp
FY2028 growth                = 17.12% + 6.53% = 23.65%
```

**Step 2 — FY2028 exit ARR**

```
1,834 × 1.2365 = $2,268m
```

**Step 3 — FY2028 average ARR**

```
(1,834 + 2,268) ÷ 2 = $2,051m
```

**Step 4 — FY2028 revenue**

```
2,051 × 0.97 = $1,996m
```

**Step 5 — FY2028 revenue growth**

```
1,996 ÷ 1,602 − 1 = 24.6%
```

**Note on the FY2028 revenue growth step-up.** FY2027 revenue growth of 21.4% is measured against an FY2026 base inflated by material rights, which depresses it. FY2028 is the first year measured against a substantially cleaner base, so growth reverts to tracking underlying ARR growth before resuming its decline. Subscription ARR growth declines monotonically throughout — 33.9%, 25.6%, 23.6%, 22.1%, 21.0% — which is why the projection is built on ARR.

## Spreadsheet formulas

To rebuild the model from scratch. Inputs in column B, projection rows starting at row 7 with FY2027 as the base year in row 6.

**Inputs:**

| Cell | Value |
|---|---|
| B1 | `0.1712` — terminal growth |
| B2 | `0.77` — decay factor k |
| B3 | `0.97` — revenue / average-ARR ratio |
| C6 | `1834` — FY2027 exit ARR |
| D6 | `0.256` — FY2027 ARR growth |
| E6 | `1602` — FY2027 revenue |

**Paste into row 7, then fill down to rows 8 and 9:**

```excel
D7    =$B$1+($D$6-$B$1)*$B$2^(ROW()-6)
C7    =C6*(1+D7)
E7    =$B$3*(C6+C7)/2
F7    =E7/E6-1
```

**Three-year CAGR:**

```excel
=(E9/E6)^(1/3)-1
```

`ROW()-6` increments the exponent automatically as the formula fills down: row 7 gets `^1`, row 8 `^2`, row 9 `^3`. Format columns D and F and the CAGR cell as percentages.

The workbook in `model/` implements this across all three companies, with every input on a separate Assumptions sheet. Blue cells are inputs; black cells are formulas. Changing any assumption recalculates all three projections.

## Company detail

### Rubrik, Inc. (NASDAQ: RBRK)

Listed April 2024. Fiscal year ends 31 January. Describes itself as a security and AI operations company. Platform covers five data types — enterprise, unstructured data, identity, cloud, and SaaS applications — across four product areas: data protection, data threat analytics and data security posture management, identity security, and cyber recovery. Delivered through Rubrik Security Cloud and Rubrik Agent Cloud (generally available February 2026).

| FY (ends 31 Jan) | Basis | Exit subscription ARR | ARR growth | Revenue | Revenue growth |
|---|---|---|---|---|---|
| 2024 | Reported | $784m | — | $627.9m | — |
| 2025 | Reported | $1,090m | 39.0% | $886.5m | 41.2% |
| 2026 | Reported | $1,460m | 33.9% | $1,320m | 48.9% |
| 2027 | Guidance | $1,834m | 25.6% | $1,602m | 21.4% |
| 2028 | Projected | $2,268m | 23.6% | $1,996m | 24.6% |
| 2029 | Projected | $2,770m | 22.1% | $2,451m | 22.8% |
| 2030 | Projected | $3,351m | 21.0% | $2,970m | 21.5% |

**Three-year revenue CAGR (FY2027–FY2030): 22.9%**

Other disclosed detail: remaining performance obligations of $2.44bn as of 30 April 2026, ~53% recognisable within twelve months. Contracts run one to five years, majority three years. Q1 FY2027 revenue by region — Americas $278.9m (+37.6%), EMEA $92.2m (+42.4%), APAC $16.0m (+45.7%); total +39.0%. US revenue 69% of total. Two partners accounted for 27% and 29% of total revenue, improved from 29% and 32% a year prior.

### Varonis Systems, Inc. (NASDAQ: VRNS)

Listed 2014. Fiscal year is the calendar year. Develops software for data and AI security, threat detection and response, and data privacy and compliance, protecting data in the cloud, on-premises, in SaaS applications, and across AI-driven systems. Core use cases include DSPM and database activity monitoring.

| FY (ends 31 Dec) | Basis | Revenue | Growth |
|---|---|---|---|
| 2024 | Reported | $551.0m | — |
| 2025 | Reported | $623.5m | 13.2% |
| 2026 | Guidance | $737m | 18.2% |
| 2027 | Projected | $882m | 19.7% |
| 2028 | Projected | $1,051m | 19.1% |
| 2029 | Projected | $1,247m | 18.7% |

**Three-year revenue CAGR (FY2026–FY2029): 19.2%**

Base growth of 20.5% is the guided SaaS ARR growth excluding conversions. ARR was not projected because historical ARR is not disclosed on a consistent basis; the projection is built directly on reported revenue. Applying the ARR growth rate to revenue assumes the two grow at the same rate — revenue is still converging toward ARR as legacy lines run off, so this may understate near-term growth.

Note that reported revenue growth rises from 13.2% to a guided 18.2% because the drag from declining term licence and maintenance revenue is easing, not because demand is accelerating.

Other disclosed detail: remaining performance obligations $1,096.7m at 31 December 2025 (54% within twelve months) and $1,084.5m at 30 June 2026 (57%) — broadly flat and shortening in duration. FY2025 revenue by region — US 71%, EMEA 21%, Rest of World 8%. Acquisitions: SlashNext (August 2025), AllTrue.ai (February 2026), with $113.6m spent on acquisitions in H1 2026; a portion of growth is inorganic.

### Commvault Systems, Inc. (NASDAQ: CVLT)

Listed 2006. Fiscal year ends 31 March. Provides cyber resiliency covering data protection, cyber recovery, data security and governance, delivered through Commvault Cloud across on-premise, hybrid, multi-cloud and SaaS environments.

| FY (ends 31 Mar) | Basis | Revenue | Growth |
|---|---|---|---|
| 2024 | Reported | $839.2m | — |
| 2025 | Reported | $995.6m | 18.6% |
| 2026 | Reported | $1,183.7m | 18.9% |
| 2027 | Guidance | $1,305m | 10.2% |
| 2028 | Projected | $1,439m | 10.2% |
| 2029 | Projected | $1,586m | 10.2% |
| 2030 | Projected | $1,749m | 10.2% |

**Three-year revenue CAGR (FY2027–FY2030): 10.2%**

Growth was steady at 18.6% then 18.9% before guidance nearly halved it. Growth held flat per the exception described in [Method](#method).

Other disclosed detail: FY2026 revenue by region — Americas $702.9m (59.4%), International $480.8m (40.6%). Approximately 47% of revenues from outside the United States; note the Americas region includes Canada and Latin America, so this differs from the segment split. Two partners accounted for approximately 32% and 11% of FY2026 revenue. Two restructuring plans initiated in fiscal 2026. Commvault is recasting revenue line items and its Subscription ARR definition from fiscal 2027, so subscription figures are not comparable year over year; total revenue is unaffected, which is why the projection uses it.

## Benchmarks

A projection is only meaningful against the naive alternatives it improves on.

**Rubrik — FY2030 exit ARR:**

| Method | Result |
|---|---|
| Constant FY2026 growth (33.9%) held | $4,403m |
| Constant FY2027 growth (25.6%) held | $3,635m |
| **This model** | **$3,351m** |
| Market growth only, flat share (17.12%) | $2,946m |

The projection falls between naive growth persistence — which assumes the company never decelerates — and pure market-rate growth, which assumes no further share gain. It therefore implies continued but decelerating share gains.

**Varonis — FY2029 revenue:**

| Method | Result |
|---|---|
| Constant 20.5% held | $1,300m |
| **This model** | **$1,247m** |
| Market growth only, flat share | $1,189m |

## Market sizing

Market size is an estimate, not reported data. No regulator or registry measures this market, so every figure is a private firm's model built from vendor surveys and assumptions about private companies. Historical-year estimates are revised between report editions, so figures from different providers or vintages cannot be combined into a series.

**Primary source used throughout:** Mordor Intelligence, data security market — CY2025 $14.7bn, CY2026 $17.21bn, growing at a 17.12% CAGR to $37.93bn by CY2031.

**Range across providers:** published estimates for this market span roughly $15bn to $29bn for the same year, because each provider draws the category boundary differently — some include backup and recovery infrastructure, others limit to security tooling. Narrower definitions (cloud data security, DSPM specifically) produce figures an order of magnitude smaller.

**Sensitivity:** all three companies sit at single-digit market share under every definition, so market size is not the binding constraint on the projections over a three-year horizon. Competitive dynamics — particularly platform vendors bundling data security into broader offerings — are the more material constraint.

## Limitations

- **Rubrik has approximately two years of public reporting.** The decay factor rests on a single year-over-year observation and carries no error estimate.
- **The decay factor is derived from Rubrik** and applied to Varonis as a sector-level assumption; Varonis lacks a comparable clean multi-year ARR series.
- **Terminal growth derives from a market estimate** with material variance across providers, as described above.
- **FY2027 figures for Rubrik and Commvault, and FY2026 for Varonis, are company guidance**, not reported results.
- **ARR, net retention, and forward guidance are company-defined non-GAAP measures** disclosed in earnings releases, not audited figures in SEC filings.
- **Fiscal years differ across companies** and figures are not calendar-aligned. Projection periods therefore cover different calendar spans.
- **The FY2028 revenue-to-ARR ratio assumes material rights effects are exhausted after FY2027.** At 0.94 instead of 0.97, FY2028 revenue would be $1,928m rather than $1,996m.
- **Profitability, cost structure, and valuation are out of scope** per the brief. Revenue growth alone does not determine investment return.

## Repository structure

```
├── README.md
├── report/
│   └── data-security-market-report.pdf    Full written report
└── model/
    └── revenue-projection-model.xlsx      Projection workbook, live formulas
```

The workbook has five sheets: Summary, Assumptions, and one per company. Every projected figure is a formula referencing the Assumptions sheet, so changing any input recalculates all three projections.

## Sources

All figures sourced from SEC filings and company earnings releases, accessed August 2026. Filings are cited to SEC EDGAR, the permanent public record; filing text was accessed via companiesmarketcap.com, which mirrors EDGAR documents.

**Rubrik, Inc. (NASDAQ: RBRK)**
- [Form 10-K, fiscal year ended 31 January 2026](https://www.sec.gov/Archives/edgar/data/1943896/000194389626000013/rbrk-20260131.htm) — competition section, risk factors, revenue recognition, business description
- [Form 10-K, fiscal year ended 31 January 2025](https://www.sec.gov/Archives/edgar/data/1943896/000194389625000012/rbrk-20250131.htm) — prior-year comparatives
- [Form 10-Q, quarter ended 30 April 2026 (Q1 FY2027)](https://www.sec.gov/Archives/edgar/data/1943896/000194389626000047/rbrk-20260430.htm) — quarterly revenue, remaining performance obligations, geographic and concentration disclosure
- [Q4 and full year fiscal 2026 results](https://finance.yahoo.com/news/rubrik-reports-fourth-quarter-fiscal-200500396.html) — FY2026 revenue, exit subscription ARR, material rights quantification, FY2027 guidance

**Varonis Systems, Inc. (NASDAQ: VRNS)**
- [Form 10-K, fiscal year ended 31 December 2025](https://www.sec.gov/ix?doc=/Archives/edgar/data/0001361113/000162828026005450/vrns-20251231.htm) — revenue history, remaining performance obligations, geographic split
- [Form 10-K, fiscal year ended 31 December 2024](https://www.sec.gov/ix?doc=/Archives/edgar/data/0001361113/000162828025004187/vrns-20241231.htm) — prior-year comparatives, market context
- [Form 10-Q, quarter ended 31 March 2026](https://www.sec.gov/ix?doc=/Archives/edgar/data/0001361113/000162828026028411/vrns-20260331.htm)
- [Form 10-Q, quarter ended 30 June 2026](https://www.sec.gov/ix?doc=/Archives/edgar/data/0001361113/000162828026050630/vrns-20260630.htm) — revenue line splits, remaining performance obligations, acquisitions
- [Q2 2026 results](https://www.sec.gov/Archives/edgar/data/1361113/000117184326004948/exh_991.htm) — SaaS ARR, growth excluding conversions, FY2026 guidance

**Commvault Systems, Inc. (NASDAQ: CVLT)**
- [Form 10-K, fiscal year ended 31 March 2026](https://www.sec.gov/ix?doc=/Archives/edgar/data/0001169561/000116956126000017/cvlt-20260331.htm) — revenue by region, competition section, risk factors
- [Q4 and full year fiscal 2026 results](https://www.sec.gov/Archives/edgar/data/1169561/000116956126000013/q4fy26pressrelease.htm) — FY2027 guidance

**Market sizing**
- [Mordor Intelligence, Data Security Market](https://www.mordorintelligence.com/industry-reports/data-security-market)

**Which figures come from where.** Revenue, remaining performance obligations, segment and geographic splits, customer concentration, competition disclosure, and risk factors are from SEC filings. Annual recurring revenue, net revenue retention, material rights quantification, and forward guidance are company-defined measures disclosed in earnings releases rather than filings.
