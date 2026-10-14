from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

AR = "Arial"
BLUE = Font(name=AR, size=10, color="0000FF")
BLACK = Font(name=AR, size=10, color="000000")
GREEN = Font(name=AR, size=10, color="008000")
BOLD = Font(name=AR, size=10, bold=True)
TITLE = Font(name=AR, size=12, bold=True)
NOTE = Font(name=AR, size=9, italic=True, color="555555")
YEL = PatternFill("solid", fgColor="FFFF00")
TOP = Border(top=Side(style="thin"))

M = '#,##0.0;(#,##0.0);"-"'
P = '0.0%;(0.0%);"-"'
X = '0.00;(0.00);"-"'
D3 = '#,##0.000;(#,##0.000);"-"'

wb = Workbook()

def put(ws, ref, val, font=BLACK, fmt=None, fill=None, bold=False):
    c = ws[ref]
    c.value = val
    c.font = Font(name=AR, size=10, color=font.color, bold=bold) if bold else font
    if fmt:
        c.number_format = fmt
    if fill:
        c.fill = fill
    return c

def label(ws, ref, text, bold=False, note=False):
    c = ws[ref]
    c.value = text
    c.font = NOTE if note else (BOLD if bold else BLACK)
    return c

# =====================================================================
# GUIDE
# =====================================================================
g = wb.active
g.title = "Guide"
lines = [
    ("Rubrik (RBRK): three-statement model and DCF", TITLE),
    ("Academic exercise. Not investment advice. Source data: Rubrik FY2026 Form 10-K and FY2027 Q2 earnings release.", NOTE),
    ("", None),
    ("How the model flows", BOLD),
    ("1. Assumptions: every input lives here. Blue = typed input, yellow = key judgement or a value you should update.", BLACK),
    ("2. Model: revenue build, then income statement, balance sheet and cash flow, FY2024A to FY2031E.", BLACK),
    ("   Revenue comes from the subscription ARR growth-decay curve. Costs and working capital are % of revenue.", BLACK),
    ("   The cash flow statement is built from balance sheet changes; closing cash feeds back into the balance sheet.", BLACK),
    ("3. DCF: unlevered free cash flow from the Model for FY2027E to FY2031E, a five-year fade to FY2036E, then a terminal value.", BLACK),
    ("4. Checks: balance sheet balance, ties to filed numbers, guidance reconciliation, and a backtest of the working-capital method.", BLACK),
    ("5. Reconciliation: bridges the data security sector report's Rubrik revenue projection to this model, one input at a time.", BLACK),
    ("", None),
    ("Colour code", BOLD),
    ("Blue text = hardcoded input (historical filed figures or assumptions). Black = formula. Green = link from another sheet.", BLACK),
    ("", None),
    ("Units", BOLD),
    ("$ millions unless stated. Fiscal year ends 31 January (FY2026 = Feb 2025 to Jan 2026). Percentages stored as fractions.", BLACK),
    ("", None),
    ("Before relying on the DCF output", BOLD),
    ("Update the yellow DCF inputs on the Assumptions sheet: risk-free rate, beta, current share price, and years elapsed.", BLACK),
]
for i, (t, f) in enumerate(lines, start=1):
    c = g.cell(row=i, column=1, value=t)
    if f is not None:
        c.font = f
g.column_dimensions["A"].width = 130

# =====================================================================
# ASSUMPTIONS
# =====================================================================
a = wb.create_sheet("Assumptions")
put(a, "A1", "Rubrik (RBRK): assumptions", TITLE)
label(a, "A2", "$ millions unless stated. Blue = input. Yellow = key judgement or value to update. Notes give the source or basis.", note=True)

label(a, "A4", "Single-value inputs", bold=True)
label(a, "B4", "Value", bold=True)
label(a, "C4", "Source / basis", bold=True)

single = [
    (5, "FY2026 exit subscription ARR", 1462.092, M, False, "Q4 FY2026 earnings release: $1,462,092k"),
    (6, "FY2027 exit subscription ARR, guidance midpoint", 1882.5, M, True, "Q2 FY2027 release: $1,880m to $1,885m"),
    (7, "FY2027 revenue, guidance midpoint", 1689.0, M, True, "Q2 FY2027 release: $1,685m to $1,693m"),
    (8, "Market growth rate (decay floor)", 0.1712, P, True, "Mordor Intelligence data security CAGR; growth above this = share gain"),
    (9, "Decay factor k", 0, X, True, "Formula: FY2026 gap above market growth / FY2025 gap, from filed exit ARR FY2024 to FY2026 (Model row 7), rounded. 16.70pp / 22.24pp = 0.751"),
    (10, "Revenue / average ARR, FY2028E onward", 1.00, X, True, "FY2027 implies about 1.01 incl. residual material rights; about 1.00 excluding them"),
    (11, "Accounts receivable days (DSO)", 70, '0', False, "FY2026 year-end 71 days; FY2025 73 days"),
    (12, "Deferred commissions, current (% revenue)", 0.080, P, False, "FY2026: 8.4%"),
    (13, "Deferred commissions, noncurrent (% revenue)", 0.115, P, False, "FY2026: 12.0%"),
    (14, "Prepaid and other current assets (% revenue)", 0.110, P, False, "FY2026: 13.7%; lower by Jul 2026"),
    (15, "Accounts payable (% revenue)", 0.011, P, False, "FY2026: 1.2%"),
    (16, "Accrued and other current liabilities (% revenue)", 0.150, P, False, "FY2026: 17.5%; lower by Jul 2026"),
    (17, "Deferred revenue: current share of total", 0.60, P, False, "FY2026: 58%; Jul 2026: 61%"),
    (18, "Interest yield on opening cash and investments", 0.035, P, False, "FY2026 about 4.4%; H1 FY2027 annualised about 3.8%. Opening balance avoids a circular reference"),
    (19, "Convertible notes, face value", 1150.0, M, False, "0.00% convertible senior notes due 2030"),
    (20, "Annual accretion of note discount", 4.4, M, False, "Carrying value rose $2.2m in H1 FY2027"),
]
for r, lab, val, fmt, key, note in single:
    label(a, f"A{r}", lab)
    put(a, f"B{r}", val, BLUE, fmt, YEL if key else None)
    label(a, f"C{r}", note, note=True)

put(a, "B9", "=ROUND((Model!D7-B8)/(Model!C7-B8),2)", BLACK, X, YEL)
label(a, "A22", "Per-year drivers", bold=True)
years = ["FY2027E", "FY2028E", "FY2029E", "FY2030E", "FY2031E"]
for i, y in enumerate(years):
    label(a, f"{'EFGHI'[i]}22", y, bold=True)
label(a, "C22", "Source / basis", bold=True)

per = [
    (23, "Cost of revenue (% revenue)", [0.205]*5, P, False, "FY2026: 19.9%; H1 FY2027: 20.6%"),
    (24, "Research and development (% revenue)", [0.295, 0.280, 0.265, 0.250, 0.240], P, True, "FY2026: 28.4%; H1 FY2027: 29.6%"),
    (25, "Sales and marketing (% revenue)", [0.520, 0.480, 0.445, 0.415, 0.390], P, True, "FY2026: 58.4%; H1 FY2027: 51.3%"),
    (26, "General and administrative (% revenue)", [0.140, 0.125, 0.115, 0.105, 0.100], P, True, "FY2026: 19.5%; H1 FY2027: 13.8%"),
    (27, "Stock-based compensation (% revenue, memo)", [0.210, 0.190, 0.170, 0.155, 0.140], P, True, "Already inside the cost lines above. FY2026: 25.0%; H1 FY2027: 21.4%"),
    (28, "Depreciation (% revenue)", [0.023]*5, P, False, "PP&E and capitalised software"),
    (29, "Amortisation of acquired intangibles ($m)", [11.0]*5, M, False, "Trailing twelve months to Jul 2026: $11.3m"),
    (30, "Capex incl. capitalised software (% revenue)", [0.026]*5, P, False, "FY2026: 3.4%; H1 FY2027: 2.4%"),
    (31, "Cash taxes (% revenue)", [0.012]*5, P, False, "Mostly foreign; $1.35bn of US federal NOLs"),
    (32, "Deferred revenue, total (% revenue)", [1.274, 1.250, 1.230, 1.220, 1.210], P, True, "FY2025: 160%; FY2026: 140%. FY2027 calibrated to FCF guidance (see Checks)"),
    (33, "Acquisitions ($m)", [23.591, 0, 0, 0, 0], M, False, "Strata.io in FY2027; goodwill $199.6m to $223.2m"),
]
for r, lab, vals, fmt, key, note in per:
    label(a, f"A{r}", lab)
    label(a, f"C{r}", note, note=True)
    for i, v in enumerate(vals):
        put(a, f"{'EFGHI'[i]}{r}", v, BLUE, fmt, YEL if key else None)

label(a, "A35", "DCF inputs", bold=True)
dcf_in = [
    (36, "Valuation date", "31 Jan 2026", None, False, "Last audited balance sheet; model base"),
    (37, "Risk-free rate", 0.052, P, True, "US 10-year Treasury yield, about 5.2% at 13 Oct 2026 close. Update when re-valuing"),
    (38, "Equity risk premium", 0.045, P, True, "Damodaran implied ERP is typically 4% to 5%; update if desired"),
    (39, "Levered beta", 1.25, X, True, "Top of Rubrik's published range (1.12 to 1.24, Oct 2026); Commvault 0.82. Under three years of trading history, so treated as a judgement"),
    (41, "Pre-tax cost of debt", 0.05, P, False, "0% coupon understates the economic cost because of the conversion option"),
    (42, "Tax rate applied to debt", 0.0, P, False, "No cash tax shield while NOLs are being used"),
    (43, "Share price ($), for weights and comparison", 118.47, X, True, "RBRK close, 13 Oct 2026. Update when re-valuing"),
    (44, "Basic shares outstanding (m)", 202.242, M, False, "Class A 157.37m + Class B 44.87m, 31 Jan 2026"),
    (48, "Terminal (perpetuity) growth", 0.04, P, True, "Must sit below WACC; long-run nominal growth"),
    (49, "Steady-state UFCF margin at end of fade", 0.18, P, True, "Judgement. SBC treated as a cost, so this is after SBC"),
    (50, "Diluted shares excluding convertible (m)", 214.4, M, False, "Q4 FY2026 non-GAAP diluted 223.6m less 9.2m from the notes"),
    (51, "Years from valuation date to today", 0.70, X, True, "31 Jan 2026 to 13 Oct 2026 (255 days)"),
]
for r, lab, val, fmt, key, note in dcf_in:
    label(a, f"A{r}", lab)
    put(a, f"B{r}", val, BLUE, fmt, YEL if key else None)
    label(a, f"C{r}", note, note=True)

label(a, "A40", "Cost of equity (CAPM)")
put(a, "B40", "=B37+B39*B38", BLACK, P)
label(a, "C40", "Risk-free + beta x equity risk premium", note=True)
label(a, "A45", "Market value of equity")
put(a, "B45", "=B43*B44", BLACK, M)
label(a, "A46", "Debt at face")
put(a, "B46", "=B19", BLACK, M)
label(a, "A47", "WACC")
put(a, "B47", "=B45/(B45+B46)*B40+B46/(B45+B46)*B41*(1-B42)", BLACK, P)
label(a, "C47", "Market-value weights", note=True)

a.column_dimensions["A"].width = 52
a.column_dimensions["B"].width = 13
a.column_dimensions["C"].width = 70
for col in "DEFGHI":
    a.column_dimensions[col].width = 11
a.freeze_panes = "B5"

# =====================================================================
# MODEL
# =====================================================================
m = wb.create_sheet("Model")
put(m, "A1", "Rubrik (RBRK): integrated three-statement model", TITLE)
label(m, "A2", "$ millions. Fiscal year ends 31 January. A = reported (SEC filings), E = projected.", note=True)
hdr = ["FY2024A", "FY2025A", "FY2026A", "FY2027E", "FY2028E", "FY2029E", "FY2030E", "FY2031E"]
for i, h in enumerate(hdr):
    c = m.cell(row=3, column=2 + i, value=h)
    c.font = BOLD
    c.alignment = Alignment(horizontal="right")
P_COLS = ["E", "F", "G", "H", "I"]
ALL = ["B", "C", "D"] + P_COLS

def hist(row, vals, fmt=M):
    for col, v in zip(["B", "C", "D"], vals):
        if v is not None:
            put(m, f"{col}{row}", v, BLUE, fmt)

def proj(row, fn, fmt=M, font=BLACK, cols=P_COLS):
    for col in cols:
        prev = chr(ord(col) - 1)
        put(m, f"{col}{row}", fn(col, prev), font, fmt)

# ---------------- Revenue build ----------------
label(m, "A5", "REVENUE BUILD", bold=True)
label(m, "A6", "Exit subscription ARR")
put(m, "B6", 784.029, BLUE, M)
put(m, "C6", 1092.584, BLUE, M)
put(m, "D6", "=Assumptions!B5", GREEN, M)
put(m, "E6", "=Assumptions!B6", GREEN, M)
proj(6, lambda c, p: f"={p}6*(1+{c}7)", cols=["F", "G", "H", "I"])

label(m, "A7", "Subscription ARR growth")
put(m, "C7", "=C6/B6-1", BLACK, P)
put(m, "D7", "=D6/C6-1", BLACK, P)
put(m, "E7", "=E6/D6-1", BLACK, P)
proj(7, lambda c, p: f"=Assumptions!$B$8+($E$7-Assumptions!$B$8)*Assumptions!$B$9^{c}8", P, cols=["F", "G", "H", "I"])

label(m, "A8", "Decay step (years after FY2027)")
for i, col in enumerate(P_COLS):
    put(m, f"{col}8", i, BLUE, '0')

label(m, "A9", "Average subscription ARR (opening + closing) / 2")
proj(9, lambda c, p: f"=({p}6+{c}6)/2")

label(m, "A10", "Revenue / average ARR")
put(m, "E10", "=E12/E9", BLACK, X)
proj(10, lambda c, p: "=Assumptions!$B$10", X, GREEN, cols=["F", "G", "H", "I"])

# ---------------- Income statement ----------------
label(m, "A11", "INCOME STATEMENT", bold=True)
label(m, "A12", "Revenue", bold=True)
hist(12, [627.892, 886.544, 1316.191])
put(m, "E12", "=Assumptions!B7", GREEN, M)
proj(12, lambda c, p: f"={c}9*{c}10", cols=["F", "G", "H", "I"])

label(m, "A13", "  Revenue growth")
for col in ["C", "D"] + P_COLS:
    prev = chr(ord(col) - 1)
    put(m, f"{col}13", f"={col}12/{prev}12-1", BLACK, P)

label(m, "A14", "Cost of revenue")
hist(14, [144.962, 265.748, 261.877])
proj(14, lambda c, p: f"={c}12*Assumptions!{c}23")

label(m, "A15", "Gross profit", bold=True)
for col in ALL:
    put(m, f"{col}15", f"={col}12-{col}14", BLACK, M)
label(m, "A16", "  Gross margin")
for col in ALL:
    put(m, f"{col}16", f"={col}15/{col}12", BLACK, P)

label(m, "A17", "Research and development")
hist(17, [206.527, 531.615, 373.682])
proj(17, lambda c, p: f"={c}12*Assumptions!{c}24")
label(m, "A18", "Sales and marketing")
hist(18, [482.532, 867.518, 769.019])
proj(18, lambda c, p: f"={c}12*Assumptions!{c}25")
label(m, "A19", "General and administrative")
hist(19, [100.377, 355.695, 257.029])
proj(19, lambda c, p: f"={c}12*Assumptions!{c}26")
label(m, "A20", "Total operating expenses")
for col in ALL:
    put(m, f"{col}20", f"=SUM({col}17:{col}19)", BLACK, M)

label(m, "A21", "Operating income (EBIT)", bold=True)
for col in ALL:
    put(m, f"{col}21", f"={col}15-{col}20", BLACK, M)
label(m, "A22", "  Operating margin")
for col in ALL:
    put(m, f"{col}22", f"={col}21/{col}12", BLACK, P)

label(m, "A23", "Interest income")
hist(23, [11.216, 25.353, 52.157])
proj(23, lambda c, p: f"=({p}34+{p}35)*Assumptions!$B$18")
label(m, "A24", "Interest expense")
hist(24, [-30.295, -41.253, -17.227])
proj(24, lambda c, p: f"=-({c}52-{p}52)")
label(m, "A25", "Other income / (expense), incl. debt extinguishment")
hist(25, [-1.884, 1.480, -15.987])
for col in P_COLS:
    put(m, f"{col}25", 0, BLUE, M)

label(m, "A26", "Pre-tax income")
for col in ALL:
    put(m, f"{col}26", f"={col}21+{col}23+{col}24+{col}25", BLACK, M)
label(m, "A27", "Income tax expense")
hist(27, [26.689, 6.368, 22.355])
proj(27, lambda c, p: f"={c}12*Assumptions!{c}31")
label(m, "A28", "Net income", bold=True)
for col in ALL:
    put(m, f"{col}28", f"={col}26-{col}27", BLACK, M)

label(m, "A29", "Memo: stock-based compensation (inside costs above)")
hist(29, [5.715, 913.913, 329.374])
proj(29, lambda c, p: f"={c}12*Assumptions!{c}27")
label(m, "A30", "Memo: depreciation and amortisation")
hist(30, [24.305, 28.868, 37.115])
proj(30, lambda c, p: f"={c}12*Assumptions!{c}28+Assumptions!{c}29")
label(m, "A31", "Memo: EBIT excluding SBC")
for col in ALL:
    put(m, f"{col}31", f"={col}21+{col}29", BLACK, M)

# ---------------- Balance sheet ----------------
label(m, "A33", "BALANCE SHEET", bold=True)
BSC = ["C", "D"] + P_COLS

def bs_hist(row, c_val, d_val):
    put(m, f"C{row}", c_val, BLUE, M)
    put(m, f"D{row}", d_val, BLUE, M)

label(m, "A34", "Cash and cash equivalents")
bs_hist(34, 186.331, 380.196)
proj(34, lambda c, p: f"={c}87")
label(m, "A35", "Short-term investments")
bs_hist(35, 518.813, 1295.579)
proj(35, lambda c, p: f"={p}35")
label(m, "A36", "Accounts receivable")
bs_hist(36, 177.627, 256.773)
proj(36, lambda c, p: f"={c}12*Assumptions!$B$11/365")
label(m, "A37", "Deferred commissions, current")
bs_hist(37, 91.919, 110.651)
proj(37, lambda c, p: f"={c}12*Assumptions!$B$12")
label(m, "A38", "Prepaid and other current assets")
bs_hist(38, 102.951, 180.365)
proj(38, lambda c, p: f"={c}12*Assumptions!$B$14")
label(m, "A39", "Total current assets", bold=True)
for col in BSC:
    put(m, f"{col}39", f"=SUM({col}34:{col}38)", BLACK, M)

label(m, "A40", "Property and equipment, net")
bs_hist(40, 53.194, 83.830)
proj(40, lambda c, p: f"={p}40-{c}78-{c}12*Assumptions!{c}28")
label(m, "A41", "Deferred commissions, noncurrent")
bs_hist(41, 132.465, 157.592)
proj(41, lambda c, p: f"={c}12*Assumptions!$B$13")
label(m, "A42", "Goodwill")
bs_hist(42, 100.343, 199.606)
proj(42, lambda c, p: f"={p}42+Assumptions!{c}33")
label(m, "A43", "Other assets, noncurrent (incl. intangibles)")
bs_hist(43, 59.331, 101.944)
proj(43, lambda c, p: f"={p}43-Assumptions!{c}29")
label(m, "A44", "Total assets", bold=True)
for col in BSC:
    put(m, f"{col}44", f"={col}39+SUM({col}40:{col}43)", BLACK, M)

label(m, "A46", "Accounts payable")
bs_hist(46, 10.439, 15.329)
proj(46, lambda c, p: f"={c}12*Assumptions!$B$15")
label(m, "A47", "Accrued expenses and other current liabilities")
bs_hist(47, 162.602, 229.976)
proj(47, lambda c, p: f"={c}12*Assumptions!$B$16")
label(m, "A48", "Deferred revenue, current")
bs_hist(48, 777.135, 1068.754)
proj(48, lambda c, p: f"={c}12*Assumptions!{c}32*Assumptions!$B$17")
label(m, "A49", "Total current liabilities", bold=True)
for col in BSC:
    put(m, f"{col}49", f"=SUM({col}46:{col}48)", BLACK, M)
label(m, "A50", "Deferred revenue, noncurrent")
bs_hist(50, 642.370, 776.547)
proj(50, lambda c, p: f"={c}12*Assumptions!{c}32*(1-Assumptions!$B$17)")
label(m, "A51", "Other liabilities, noncurrent")
bs_hist(51, 61.821, 64.771)
proj(51, lambda c, p: f"={p}51")
label(m, "A52", "Convertible senior notes, net")
bs_hist(52, 0, 1130.721)
proj(52, lambda c, p: f"=MIN({p}52+Assumptions!$B$20,Assumptions!$B$19)")
label(m, "A53", "Debt, noncurrent (term loan, repaid FY2026)")
bs_hist(53, 322.341, 0)
proj(53, lambda c, p: f"={p}53")
label(m, "A54", "Total liabilities", bold=True)
for col in BSC:
    put(m, f"{col}54", f"={col}49+SUM({col}50:{col}53)", BLACK, M)

label(m, "A56", "Common stock, par value")
bs_hist(56, 0.005, 0.005)
proj(56, lambda c, p: f"={p}56")
label(m, "A57", "Additional paid-in capital")
bs_hist(57, 2291.829, 2662.861)
proj(57, lambda c, p: f"={p}57+{c}29")
label(m, "A58", "Accumulated other comprehensive income (loss)")
bs_hist(58, -8.235, 3.733)
proj(58, lambda c, p: f"={p}58")
label(m, "A59", "Accumulated deficit")
bs_hist(59, -2837.333, -3186.161)
proj(59, lambda c, p: f"={p}59+{c}28")
label(m, "A60", "Total stockholders' equity (deficit)", bold=True)
for col in BSC:
    put(m, f"{col}60", f"=SUM({col}56:{col}59)", BLACK, M)
label(m, "A61", "Total liabilities and equity", bold=True)
for col in BSC:
    put(m, f"{col}61", f"={col}54+{col}60", BLACK, M)
label(m, "A62", "Balance check: assets minus liabilities and equity (must be zero)", bold=True)
for col in BSC:
    put(m, f"{col}62", f"=ROUND({col}44-{col}61,3)", BLACK, D3)

# ---------------- Cash flow ----------------
label(m, "A64", "CASH FLOW STATEMENT", bold=True)
label(m, "A65", "Net income")
for col in ALL:
    put(m, f"{col}65", f"={col}28", BLACK, M)
label(m, "A66", "Depreciation and amortisation")
for col in ALL:
    put(m, f"{col}66", f"={col}30", BLACK, M)
label(m, "A67", "Stock-based compensation")
for col in ALL:
    put(m, f"{col}67", f"={col}29", BLACK, M)
label(m, "A68", "Non-cash interest (note accretion)")
hist(68, [10.117, 34.256, 0])
proj(68, lambda c, p: f"={c}52-{p}52")
label(m, "A69", "Other non-cash items")
hist(69, [-0.899, -6.008, 7.119])
for col in P_COLS:
    put(m, f"{col}69", 0, BLUE, M)
label(m, "A70", "Change in accounts receivable")
hist(70, [17.157, -44.255, -79.786])
proj(70, lambda c, p: f"=-({c}36-{p}36)")
label(m, "A71", "Change in deferred commissions (net of amortisation)")
hist(71, [-30.618, -38.513, -43.859])
proj(71, lambda c, p: f"=-(({c}37+{c}41)-({p}37+{p}41))")
label(m, "A72", "Change in prepaid and other assets")
hist(72, [2.251, -48.818, -111.727])
proj(72, lambda c, p: f"=-({c}38-{p}38)")
label(m, "A73", "Change in accounts payable")
hist(73, [-1.012, 4.479, 4.479])
proj(73, lambda c, p: f"={c}46-{p}46")
label(m, "A74", "Change in accrued and other liabilities")
hist(74, [22.872, 45.882, 63.225])
proj(74, lambda c, p: f"=({c}47-{p}47)+({c}51-{p}51)")
label(m, "A75", "Change in deferred revenue")
hist(75, [299.752, 313.244, 425.796])
proj(75, lambda c, p: f"=({c}48+{c}50)-({p}48+{p}50)")
label(m, "A76", "Cash from operating activities", bold=True)
for col in ALL:
    put(m, f"{col}76", f"=SUM({col}65:{col}75)", BLACK, M)

label(m, "A78", "Capex incl. capitalised software")
hist(78, [-20.008, -26.599, -45.068])
proj(78, lambda c, p: f"=-{c}12*Assumptions!{c}30")
label(m, "A79", "Acquisitions")
hist(79, [-90.328, 0, -21.259])
proj(79, lambda c, p: f"=-Assumptions!{c}33")
label(m, "A80", "Net (purchases) / maturities of investments")
hist(80, [16.713, -356.843, -763.762])
proj(80, lambda c, p: f"=-({c}35-{p}35)")
label(m, "A81", "Cash from investing activities", bold=True)
for col in ALL:
    put(m, f"{col}81", f"=SUM({col}78:{col}80)", BLACK, M)

label(m, "A83", "Cash from financing activities")
hist(83, [95.949, 398.023, 736.501])
for col in P_COLS:
    put(m, f"{col}83", 0, BLUE, M)
label(m, "A84", "Effect of exchange rates")
hist(84, [-1.355, -6.274, 9.826])
for col in P_COLS:
    put(m, f"{col}84", 0, BLUE, M)
label(m, "A85", "Net change in cash", bold=True)
for col in ALL:
    put(m, f"{col}85", f"={col}76+{col}81+{col}83+{col}84", BLACK, M)
label(m, "A86", "Opening cash")
hist(86, [140.606, 137.059, 193.594])
proj(86, lambda c, p: f"={p}34")
label(m, "A87", "Closing cash", bold=True)
for col in ALL:
    put(m, f"{col}87", f"={col}86+{col}85", BLACK, M)
label(m, "A88", "Historical opening and closing cash include restricted cash (about $12.5m at FY2026); projected cash equals balance sheet cash.", note=True)

label(m, "A90", "Free cash flow (operating cash flow less capex)", bold=True)
for col in ALL:
    put(m, f"{col}90", f"={col}76+{col}78", BLACK, M)
label(m, "A91", "  Free cash flow margin")
for col in ALL:
    put(m, f"{col}91", f"={col}90/{col}12", BLACK, P)

for r in (12, 21, 28, 39, 44, 49, 54, 60, 61, 76, 81, 85, 87, 90):
    for col in ALL:
        m[f"{col}{r}"].border = TOP
m.column_dimensions["A"].width = 58
for col in ALL:
    m.column_dimensions[col].width = 11
m.freeze_panes = "B4"

# =====================================================================
# DCF
# =====================================================================
d = wb.create_sheet("DCF")
put(d, "A1", "Rubrik (RBRK): discounted cash flow", TITLE)
label(d, "A2", "$ millions. Valuation date 31 Jan 2026. End-of-year discounting. SBC treated as an operating cost (not added back).", note=True)
DC = ["C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]
MC = ["E", "F", "G", "H", "I"]
for i, col in enumerate(DC):
    put(d, f"{col}3", f"FY{2027+i}E", BOLD).alignment = Alignment(horizontal="right")
    put(d, f"{col}4", "Explicit" if i < 5 else "Fade", NOTE)
    put(d, f"{col}5", i + 1, BLUE, '0')
label(d, "A4", "Stage")
label(d, "A5", "Year (t)")

label(d, "A6", "Revenue")
label(d, "A7", "  Revenue growth")
label(d, "A8", "EBIT (after SBC)")
label(d, "A9", "Less: cash taxes")
label(d, "A10", "Plus: depreciation and amortisation")
label(d, "A11", "Less: capex")
label(d, "A12", "Plus / (less): change in net working capital")
label(d, "A13", "Unlevered free cash flow", bold=True)
label(d, "A14", "  UFCF margin")
label(d, "A15", "Memo: stock-based compensation")
label(d, "A16", "Memo: UFCF if SBC were added back")
label(d, "A17", "Discount factor")
label(d, "A18", "Present value of UFCF")

for col, mc in zip(DC[:5], MC):
    put(d, f"{col}6", f"=Model!{mc}12", GREEN, M)
    put(d, f"{col}7", f"=Model!{mc}13", GREEN, P)
    put(d, f"{col}8", f"=Model!{mc}21", GREEN, M)
    put(d, f"{col}9", f"=-Model!{mc}27", GREEN, M)
    put(d, f"{col}10", f"=Model!{mc}30", GREEN, M)
    put(d, f"{col}11", f"=Model!{mc}78", GREEN, M)
    put(d, f"{col}12", f"=SUM(Model!{mc}70:{mc}75)", GREEN, M)
    put(d, f"{col}13", f"=SUM({col}8:{col}12)", BLACK, M)
    put(d, f"{col}14", f"={col}13/{col}6", BLACK, P)
    put(d, f"{col}15", f"=Model!{mc}29", GREEN, M)
    put(d, f"{col}16", f"={col}13+{col}15", BLACK, M)
for col in DC[5:]:
    prev = chr(ord(col) - 1)
    put(d, f"{col}6", f"={prev}6*(1+{col}7)", BLACK, M)
    put(d, f"{col}7", f"=$G$7-($G$7-Assumptions!$B$48)*({col}$5-5)/5", BLACK, P)
    put(d, f"{col}14", f"=$G$14+(Assumptions!$B$49-$G$14)*({col}$5-5)/5", BLACK, P)
    put(d, f"{col}13", f"={col}6*{col}14", BLACK, M)
for col in DC:
    put(d, f"{col}17", f"=1/(1+Assumptions!$B$47)^{col}5", BLACK, '0.000')
    put(d, f"{col}18", f"={col}13*{col}17", BLACK, M)
    d[f"{col}13"].border = TOP

label(d, "A20", "VALUATION", bold=True)
val_rows = [
    (21, "Sum of PV of UFCF, FY2027E to FY2036E", "=SUM(C18:L18)", M),
    (22, "Terminal-year UFCF (FY2037)", "=L13*(1+Assumptions!B48)", M),
    (23, "Terminal value at end of FY2036", "=C22/(Assumptions!B47-Assumptions!B48)", M),
    (24, "PV of terminal value", "=C23*L17", M),
    (25, "Enterprise value", "=C21+C24", M),
    (26, "  Terminal value as % of enterprise value", "=C24/C25", P),
    (27, "Plus: cash and short-term investments (31 Jan 2026)", "=Model!D34+Model!D35", M),
    (28, "Less: convertible notes at face", "=Assumptions!B19", M),
    (29, "Equity value", "=C25+C27-C28", M),
    (30, "Diluted shares excluding convertible (m)", "=Assumptions!B50", M),
    (31, "Implied value per share at 31 Jan 2026 ($)", "=C29/C30", X),
    (32, "Rolled forward to today at the cost of equity ($)", "=C31*(1+Assumptions!B40)^Assumptions!B51", X),
    (33, "Current share price ($)", "=Assumptions!B43", X),
    (34, "Implied upside / (downside)", "=C32/C33-1", P),
]
for r, lab, f, fmt in val_rows:
    label(d, f"A{r}", lab, bold=r in (25, 29, 31, 32))
    font = GREEN if "Assumptions!" in f or "Model!" in f else BLACK
    put(d, f"C{r}", f, font, fmt)

label(d, "A36", "SENSITIVITY: implied value per share at valuation date ($)", bold=True)
label(d, "A37", "Holds the UFCF path fixed and varies the discount rate and the perpetuity growth used in the terminal value.", note=True)
label(d, "B38", "WACC \\ g", bold=True)
gs = [0.030, 0.035, 0.040, 0.045, 0.050]
ws_ = [0.075, 0.080, 0.085, 0.090, 0.095, 0.100, 0.105, 0.110]
for j, gv in enumerate(gs):
    put(d, f"{'CDEFG'[j]}38", gv, BLUE, P)
for i, wv in enumerate(ws_):
    r = 39 + i
    put(d, f"B{r}", wv, BLUE, P)
    for j in range(5):
        col = "CDEFG"[j]
        f = (f"=(SUMPRODUCT($C$13:$L$13,1/(1+$B{r})^$C$5:$L$5)"
             f"+$L$13*(1+{col}$38)/($B{r}-{col}$38)/(1+$B{r})^10"
             f"+$C$27-$C$28)/$C$30")
        put(d, f"{col}{r}", f, BLACK, X)

label(d, "A47", "Value per share added if SBC were treated as non-cash in FY2027E to FY2031E only ($)", bold=True)
put(d, "C47", "=SUMPRODUCT(C15:G15,C17:G17)/C30", BLACK, X)
label(d, "A48", "Shows how much of a DCF value can come from one accounting choice. Not used in the base case.", note=True)
label(d, "A50", "MARKET-IMPLIED ASSUMPTION", bold=True)
label(d, "A51", "Value per share today is linear in the steady-state UFCF margin: value = A + B x margin. Solving for the margin that returns the current share price.", note=True)
label(d, "A52", "A: value per share today with a zero steady-state margin ($)")
put(d, "C52", "=(SUMPRODUCT(C13:G13,C17:G17)+SUMPRODUCT(H6:L6*(1-(H5:L5-5)/5)*H17:L17)*$G$14+C27-C28)/C30*(1+Assumptions!B40)^Assumptions!B51", BLACK, X)
label(d, "A53", "B: value per share added per 100% of steady-state margin ($)")
put(d, "C53", "=(SUMPRODUCT(H6:L6*(H5:L5-5)/5*H17:L17)+L6*(1+Assumptions!B48)/(Assumptions!B47-Assumptions!B48)*L17)/C30*(1+Assumptions!B40)^Assumptions!B51", BLACK, X)
label(d, "A54", "Check: A + B x base-case margin equals the rolled-forward value above")
put(d, "C54", '=IF(ABS(C52+C53*Assumptions!B49-C32)<0.01,"PASS","CHECK")', BLACK)
label(d, "A55", "Steady-state UFCF margin implied by the current share price", bold=True)
put(d, "C55", "=(C33-C52)/C53", BLACK, P)
label(d, "A56", "Compare with the base case (Assumptions B49). Same WACC, terminal growth and FY2027E to FY2031E cash flows.", note=True)

d.column_dimensions["A"].width = 58
d.column_dimensions["B"].width = 10
for col in DC:
    d.column_dimensions[col].width = 11
d.freeze_panes = "C6"

# =====================================================================
# RECONCILIATION
# =====================================================================
rc = wb.create_sheet("Reconciliation")
put(rc, "A1", "Reconciliation: sector report revenue projection to this model", TITLE)
label(rc, "A2", "$ millions. Each column changes one input from the column to its left. Same growth-decay method throughout; only the inputs differ.", note=True)
SC = ["C", "D", "E", "F", "G"]
heads = ["A. Sector model as first built", "B. Filed FY2026 exit ARR", "C. k from filed ARR (corrected sector model)", "D. August 2026 guidance", "E. Revenue / ARR 1.00 from FY2028 (this model)"]
for col, h in zip(SC, heads):
    c = put(rc, f"{col}3", h, BOLD)
    c.alignment = Alignment(wrap_text=True, horizontal="center", vertical="top")
rc.row_dimensions[3].height = 54
label(rc, "A4", "What changed", bold=True)
whats = ["Rounded inputs ($1,460m, k 0.77)", "$1,462.1m from the Q4 FY2026 release", "16.70pp / 22.24pp = 0.75", "Q2 FY2027 release: ARR $1,882.5m, revenue $1,689m", "Material rights treated as exhausted after FY2027"]
for col, w in zip(SC, whats):
    c = label(rc, f"{col}4", w, note=True)
    c.alignment = Alignment(wrap_text=True, horizontal="center", vertical="top")
rc.row_dimensions[4].height = 40
label(rc, "A6", "Inputs", bold=True)
inp = {
    7: ("FY2026 exit subscription ARR", [1460, 1462.092, 1462.092, "=Model!D6", "=Model!D6"], M),
    8: ("FY2027 exit subscription ARR", [1834, 1834, 1834, "=Assumptions!B6", "=Assumptions!B6"], M),
    9: ("FY2027 revenue", [1602, 1602, 1602, "=Assumptions!B7", "=Assumptions!B7"], M),
    10: ("Decay factor k", [0.77, 0.77, 0.75, "=Assumptions!B9", "=Assumptions!B9"], X),
    11: ("Revenue / average ARR, FY2028 onward", [0.97, 0.97, 0.97, 0.97, "=Assumptions!B10"], X),
    12: ("Market growth (decay floor)", ["=Assumptions!B8"] * 5, P),
}
for r, (lab, vals, fmt) in inp.items():
    label(rc, f"A{r}", lab)
    for col, val in zip(SC, vals):
        font = GREEN if isinstance(val, str) else BLUE
        put(rc, f"{col}{r}", val, font, fmt)
label(rc, "A14", "Projection", bold=True)
calc = [
    (15, "FY2027 ARR growth", lambda c: f"={c}8/{c}7-1", P),
    (16, "FY2028 ARR growth", lambda c: f"={c}12+({c}15-{c}12)*{c}10", P),
    (17, "FY2029 ARR growth", lambda c: f"={c}12+({c}15-{c}12)*{c}10^2", P),
    (18, "FY2030 ARR growth", lambda c: f"={c}12+({c}15-{c}12)*{c}10^3", P),
    (19, "FY2028 exit ARR", lambda c: f"={c}8*(1+{c}16)", M),
    (20, "FY2029 exit ARR", lambda c: f"={c}19*(1+{c}17)", M),
    (21, "FY2030 exit ARR", lambda c: f"={c}20*(1+{c}18)", M),
    (22, "FY2028 revenue", lambda c: f"={c}11*({c}8+{c}19)/2", M),
    (23, "FY2029 revenue", lambda c: f"={c}11*({c}19+{c}20)/2", M),
    (24, "FY2030 revenue", lambda c: f"={c}11*({c}20+{c}21)/2", M),
    (25, "Three-year revenue CAGR, FY2027 to FY2030", lambda c: f"=({c}24/{c}9)^(1/3)-1", P),
]
for r, lab, fn, fmt in calc:
    label(rc, f"A{r}", lab, bold=r in (24, 25))
    for col in SC:
        put(rc, f"{col}{r}", fn(col), BLACK, fmt)
label(rc, "A27", "Change from previous column", bold=True)
label(rc, "A28", "FY2030 revenue ($m)")
label(rc, "A29", "Three-year CAGR (percentage points)")
for i, col in enumerate(SC[1:], start=1):
    prev = SC[i - 1]
    put(rc, f"{col}28", f"={col}24-{prev}24", BLACK, M)
    put(rc, f"{col}29", f"=({col}25-{prev}25)*100", BLACK, '0.00;(0.00);"-"')
label(rc, "A31", "Ties", bold=True)
label(rc, "A32", "Scenario C equals revenue-projection-model.xlsx, Rubrik!E8")
put(rc, "B32", 2948.555, BLUE, M)
put(rc, "C32", '=IF(ABS(E24-B32)<0.01,"PASS","CHECK")', BLACK)
label(rc, "A33", "Scenario E equals Model FY2030E revenue")
put(rc, "B33", "=Model!H12", GREEN, M)
put(rc, "C33", '=IF(ABS(G24-B33)<0.01,"PASS","CHECK")', BLACK)
label(rc, "A35", "The submitted sector report PDF shows FY2028 to FY2030 revenue of 1,996 / 2,451 / 2,978 and a 22.9% CAGR. They match the unrounded FY2027 ratio (about 0.973) to within $1m, although the report states 0.97. Scenario A is the spreadsheet as first built.", note=True)
rc.column_dimensions["A"].width = 52
rc.column_dimensions["B"].width = 11
for col in SC:
    rc.column_dimensions[col].width = 19
rc.freeze_panes = "B5"

# =====================================================================
# CHECKS
# =====================================================================
k = wb.create_sheet("Checks")
put(k, "A1", "Integrity and validation checks", TITLE)
for col, t in zip("ABCD", ["Check", "Model value", "Target", "Result"]):
    label(k, f"{col}3", t, bold=True)

bal = ",".join(f"ABS(Model!{c}62)" for c in BSC)
checks = [
    (4, "Balance sheet balances, all years (max absolute difference)", f"=MAX({bal})", 0, D3, '=IF(B4<0.001,"PASS","CHECK")'),
    (5, "FY2026 net income ties to 10-K", "=Model!D28", -348.828, M, '=IF(ABS(B5-C5)<0.001,"PASS","CHECK")'),
    (6, "FY2026 cash from operations ties to 10-K", "=Model!D76", 282.908, M, '=IF(ABS(B6-C6)<0.001,"PASS","CHECK")'),
    (7, "FY2026 free cash flow ties to earnings release", "=Model!D90", 237.840, M, '=IF(ABS(B7-C7)<0.001,"PASS","CHECK")'),
    (8, "FY2026 total assets ties to 10-K", "=Model!D44", 2766.536, M, '=IF(ABS(B8-C8)<0.001,"PASS","CHECK")'),
    (9, "FY2026 closing cash incl. restricted ties to 10-K", "=Model!D87", 392.740, M, '=IF(ABS(B9-C9)<0.001,"PASS","CHECK")'),
    (10, "FY2027 revenue equals guidance midpoint", "=Model!E12", 1689.0, M, '=IF(ABS(B10-C10)<0.001,"PASS","CHECK")'),
    (11, "FY2027 exit ARR equals guidance midpoint", "=Model!E6", 1882.5, M, '=IF(ABS(B11-C11)<0.001,"PASS","CHECK")'),
    (13, "Terminal growth below WACC", "=Assumptions!B48", "=Assumptions!B47", P, '=IF(B13<C13,"PASS","FAIL")'),
]
for r, lab, f, tgt, fmt, res in checks:
    label(k, f"A{r}", lab)
    put(k, f"B{r}", f, GREEN, fmt)
    tfont = GREEN if isinstance(tgt, str) else BLUE
    put(k, f"C{r}", tgt, tfont, fmt)
    put(k, f"D{r}", res, BLACK)
label(k, "A12", "FY2027 free cash flow within guidance ($323m to $333m)")
put(k, "B12", "=Model!E90", GREEN, M)
put(k, "C12", "323 to 333", BLUE)
put(k, "D12", '=IF(AND(B12>=323,B12<=333),"IN RANGE","OUTSIDE")', BLACK)

label(k, "A14", "Reconciliation bridge ends at Model FY2030E revenue")
put(k, "B14", "=Reconciliation!G24", GREEN, M)
put(k, "C14", "=Model!H12", GREEN, M)
put(k, "D14", '=IF(ABS(B14-C14)<0.001,"PASS","CHECK")', BLACK)

label(k, "A15", "Context (not pass/fail)", bold=True)
label(k, "A16", "FY2027E operating margin vs H1 FY2027 actual")
put(k, "B16", "=Model!E22", GREEN, P)
put(k, "C16", -0.1529, BLUE, P)
label(k, "D16", "H1 FY2027: operating loss $124.5m on revenue $814.3m", note=True)
label(k, "A17", "Note: the FY2027 deferred revenue ratio is set so modelled FCF matches the guidance midpoint. Row 12 is a calibration, not an independent test.", note=True)

label(k, "A19", "BACKTEST: would holding FY2025 working-capital ratios have predicted FY2026 cash flow?", bold=True)
label(k, "A20", "Uses actual FY2026 revenue and FY2025 balance-sheet ratios; compares the implied working-capital cash effect with what Rubrik reported.", note=True)
bt = [
    (21, "FY2025 receivables / revenue", "=Model!C36/Model!C12", P),
    (22, "FY2025 deferred commissions / revenue", "=(Model!C37+Model!C41)/Model!C12", P),
    (23, "FY2025 prepaid / revenue", "=Model!C38/Model!C12", P),
    (24, "FY2025 payables / revenue", "=Model!C46/Model!C12", P),
    (25, "FY2025 accrued / revenue", "=Model!C47/Model!C12", P),
    (26, "FY2025 deferred revenue / revenue", "=(Model!C48+Model!C50)/Model!C12", P),
    (27, "Predicted FY2026 working-capital cash effect",
     "=-(B21*Model!D12-Model!C36)-(B22*Model!D12-(Model!C37+Model!C41))-(B23*Model!D12-Model!C38)"
     "+(B24*Model!D12-Model!C46)+(B25*Model!D12-Model!C47)+(B26*Model!D12-(Model!C48+Model!C50))", M),
    (28, "Actual FY2026 working-capital cash effect", "=SUM(Model!D70:D75)", M),
    (29, "Prediction error (predicted minus actual)", "=B27-B28", M),
    (30, "  of which: deferred revenue", "=(B26*Model!D12-(Model!C48+Model!C50))-Model!D75", M),
]
for r, lab, f, fmt in bt:
    label(k, f"A{r}", lab, bold=r in (29,))
    font = GREEN if f.startswith("=Model") or f.startswith("=(Model") or f.startswith("=SUM(Model") else BLACK
    put(k, f"B{r}", f, font, fmt)
label(k, "A31", "Holding the deferred revenue ratio flat would have overstated FY2026 operating cash flow by most of the error above. The ratio fell from 160% to 140%, so the projection steps it down rather than holding it.", note=True)

label(k, "A33", "DCF market-implied margin solve reproduces the base value", bold=True)
put(k, "D33", "=DCF!C54", GREEN)
k.column_dimensions["A"].width = 70
for col in "BCD":
    k.column_dimensions[col].width = 14

out_path = Path(__file__).resolve().parent / "rubrik_3s_dcf.xlsx"
wb.save(out_path)
print(f"saved to {out_path}")