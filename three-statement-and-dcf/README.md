# Rubrik (RBRK): Three-Statement Model and DCF

A driver-based, fully linked income statement, balance sheet and cash flow model for Rubrik, Inc., FY2024A to FY2031E, with an unlevered discounted cash flow valuation built on top of it.

*Academic exercise. Not investment advice. Historical figures from Rubrik's SEC filings; market inputs as of 13 October 2026.*

This extends the [data security sector revenue study](../README.md) at the top of this repository, which projected Rubrik's revenue from its subscription ARR. The Reconciliation sheet bridges that projection to this model one input at a time.

---

## Contents

- [Results](#results)
- [Workbook structure](#workbook-structure)
- [Revenue build](#revenue-build)
- [How the three statements link](#how-the-three-statements-link)
- [DCF](#dcf)
- [Validation](#validation)
- [Limitations](#limitations)
- [Rebuilding the workbook](#rebuilding-the-workbook)
- [Sources](#sources)

---

## Results

| $m (FY ends 31 Jan) | FY2026A | FY2027E | FY2028E | FY2029E | FY2030E | FY2031E |
|---|---|---|---|---|---|---|
| Exit subscription ARR | 1,462.1 | 1,882.5 | 2,369.0 | 2,929.7 | 3,575.0 | 4,318.6 |
| Revenue | 1,316.2 | 1,689.0 | 2,125.8 | 2,649.3 | 3,252.3 | 3,946.8 |
| Revenue growth | 48.5% | 28.3% | 25.9% | 24.6% | 22.8% | 21.4% |
| Operating income (GAAP) | (345.4) | (270.2) | (191.3) | (79.5) | 81.3 | 256.5 |
| Operating margin | (26.2%) | (16.0%) | (9.0%) | (3.0%) | 2.5% | 6.5% |
| Free cash flow | 237.8 | 328.2 | 619.8 | 858.8 | 1,175.4 | 1,497.7 |

**DCF (base case):** enterprise value $10.4bn, equity value $11.0bn, **$54.91 per share** rolled forward to 13 October 2026, against a share price of $118.47.

**What the market price implies:** holding the discount rate, terminal growth and FY2027E to FY2031E cash flows fixed, the current price requires a steady-state unlevered free cash flow margin of **45.6% after stock-based compensation**, against 18% in the base case. Alternatively, at the base-case margin, it requires a discount rate of about 8% with 5% terminal growth (see the sensitivity grid). The model does not say the market is wrong; it makes explicit what the market is assuming.

## Workbook structure

| Sheet | Contents |
|---|---|
| Guide | How the model flows, colour code, units |
| Assumptions | Every input in one place, each with its source or basis |
| Model | Revenue build, income statement, balance sheet, cash flow statement |
| DCF | Unlevered free cash flow, WACC, terminal value, equity bridge, sensitivity grid, market-implied margin |
| Reconciliation | Bridge from the sector study's revenue projection to this model |
| Checks | Balance check, ties to filings, guidance checks, working-capital backtest |

Colour code: blue text is a typed input (a filed figure or an assumption), black is a formula, green is a link from another sheet. Yellow cells are key judgements. Every projected figure is a formula.

## Revenue build

Revenue is driven by subscription ARR, which is not distorted by the material rights that inflated Rubrik's FY2026 reported revenue.

```
ARR growth in year t = market growth + (FY2027 growth − market growth) × k^t
Revenue              = ratio × (opening ARR + closing ARR) ÷ 2
```

- **FY2027:** Rubrik's guidance midpoints from its Q2 FY2027 release (exit ARR $1,882.5m, revenue $1,689m).
- **Market growth:** 17.12%, the Mordor Intelligence data security market CAGR. Growth above it implies share gain.
- **Decay factor k = 0.75**, calculated in the workbook from Rubrik's filed exit ARR for FY2024 to FY2026: the gap above market growth fell from 22.24pp to 16.70pp, and 16.70 ÷ 22.24 = 0.751.
- **Revenue / average ARR = 1.00** from FY2028, once material rights revenue has run off.

## How the three statements link

- **Costs** are projected as a percentage of revenue, with sales and marketing, R&D and G&A stepping down as the company scales.
- **Net income** flows into the accumulated deficit on the balance sheet and is the first line of the cash flow statement.
- **Stock-based compensation** is a non-cash cost: it is added back in the cash flow statement and added to additional paid-in capital, so equity and cash both reconcile.
- **Working capital** (receivables, deferred commissions, prepaid expenses, payables, accrued liabilities, deferred revenue) is projected from revenue ratios; each change flows into operating cash flow.
- **Deferred revenue** is the largest cash driver: customers pay upfront for multi-year subscriptions, so cash arrives before revenue is recognised.
- **Closing cash** from the cash flow statement becomes balance sheet cash. The balance check row (total assets minus liabilities and equity) is zero in every year.
- **Interest income** is earned on opening cash and investments, which avoids a circular reference.
- **The convertible notes** ($1,150m face, 0% coupon, due 2030) accrete towards face value as non-cash interest.

## DCF

| Input | Value | Basis |
|---|---|---|
| Risk-free rate | 5.2% | US 10-year Treasury, 13 Oct 2026 |
| Equity risk premium | 4.5% | Within the commonly used 4% to 5% range |
| Beta | 1.25 | Top of Rubrik's published range (1.12 to 1.24); under three years of trading history, so a judgement |
| Cost of equity | 10.8% | CAPM |
| Pre-tax cost of debt | 5.0% | The 0% coupon understates the economic cost of a convertible |
| WACC | 10.6% | Market-value weights |
| Terminal growth | 4.0% | Long-run nominal growth |
| Steady-state UFCF margin | 18% | Reached by FY2036 after a five-year fade from FY2031E |

- **Stock-based compensation is treated as a cost**, not added back. It is a real transfer of value to employees, and at 25% of FY2026 revenue (21% projected for FY2027) it is too large to ignore. The DCF sheet shows that adding it back for FY2027E to FY2031E alone would add $7.73 per share.
- **No tax shield on debt**, because Rubrik has $1.35bn of US federal NOLs and pays little cash tax.
- **Terminal value is 66% of enterprise value**, which is why the sensitivity grid (WACC 7.5% to 11%, terminal growth 3% to 5%) matters more than the point estimate.
- **Equity bridge:** enterprise value plus cash and short-term investments ($1,675.8m at 31 Jan 2026) less the convertible at face, divided by 214.4m diluted shares excluding the convertible.

## Validation

**Ties to filings.** FY2026 net income (−$348.8m), cash from operations ($282.9m), free cash flow ($237.8m), total assets ($2,766.5m) and closing cash including restricted cash ($392.7m) match the 10-K and earnings release to the thousand. Every historical input was checked line by line against the FY2026 10-K.

**Guidance.** FY2027 revenue and exit ARR equal the guidance midpoints. FY2027 free cash flow of $328.2m sits inside the $323m to $333m guidance range, but this is a calibration, not a test: the FY2027 deferred revenue ratio was set to produce it.

**Working-capital backtest.** Holding FY2025 working-capital ratios flat and applying them to actual FY2026 revenue would have predicted a $527m cash inflow from working capital. The actual figure was $258m, an overstatement of $269m, of which $262m came from deferred revenue (whose ratio to revenue fell from 160% to 140%). The projection therefore steps the deferred revenue ratio down each year rather than holding it flat.

**Reconciliation.** The bridge from the sector study's revenue projection ends exactly at this model's FY2030 revenue: filed inputs and the re-derived k take 0.3 points off the CAGR, the August 2026 guidance raise adds 0.6, and moving the revenue / ARR ratio to 1.00 adds 1.3.

## Limitations

- **One observation drives k.** Rubrik has three year-end ARR figures as a public company, so the decay factor rests on a single deceleration and carries no error estimate.
- **Costs are ratios, not a bottom-up build.** Headcount, pricing and product mix are not modelled.
- **No buybacks, new debt or dividends** are assumed, so cash and investments build to $6.1bn by FY2031E and interest on them lifts free cash flow margins.
- **The convertible is treated as debt at face.** If Rubrik's share price stays above the conversion price, it is more likely to settle in shares, which would add dilution instead.
- **Beta and the equity risk premium are judgements**, and the value per share is sensitive to both.
- **Guidance, ARR and free cash flow are company-defined non-GAAP measures**, not audited figures.

## Rebuilding the workbook

`build_3s.py` generates the workbook from scratch with Python and openpyxl, so every formula is visible in code. Recalculate in Excel or LibreOffice after building.

```
cd three-statement-dcf
pip install openpyxl
python build_3s.py
```

## Repository structure

```
three-statement-and-dcf/
├── README.md              This file
├── rubrik_3s_dcf.xlsx     Model workbook, live formulas
└── 3s.py            Script that builds the workbook
```

## Sources

- [Rubrik Form 10-K, fiscal year ended 31 January 2026](https://www.sec.gov/Archives/edgar/data/1943896/000194389626000013/rbrk-20260131.htm): all historical income statement, balance sheet and cash flow figures
- [Rubrik Q4 and full year fiscal 2026 results (8-K Exhibit 99.1)](https://www.sec.gov/Archives/edgar/data/1943896/000194389626000004/rubrikinc-991pressrelease1.htm): FY2026 exit ARR and free cash flow
- [Rubrik Q4 and full year fiscal 2025 results (8-K Exhibit 99.1)](https://www.sec.gov/Archives/edgar/data/1943896/000194389625000006/rubrikinc-991pressrelease1.htm): FY2024 and FY2025 exit ARR
- [Rubrik Q1 fiscal 2027 results (8-K Exhibit 99.1)](https://www.sec.gov/Archives/edgar/data/0001943896/000194389626000041/rubrikinc-991pressrelease4.htm): guidance history
- [Rubrik Q2 fiscal 2027 results (8-K Exhibit 99.1)](ADD_LINK): FY2027 guidance used in the model, H1 FY2027 actuals
- Market inputs: 10-year Treasury yield ([Forbes Advisor](https://www.forbes.com/advisor/investing/treasury-rates/), 13 Oct 2026); RBRK share price and beta ([Stock Analysis](https://stockanalysis.com/stocks/rbrk/), 13 Oct 2026)
