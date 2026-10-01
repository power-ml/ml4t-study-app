# QF Domain 1 — Investment Returns and Compounding

## Domain cheat-sheet

- **One-period (holding-period) return:** `r = (P_end − P_begin + income) / P_begin`. The percentage depends on the *starting price*, not the raw dollar change — an $8 move on $80 (10%) is worse than a $4 move on $20 (20%).
- **Linking periods multiplicatively:** cumulative return over consecutive periods is `(1+r1)(1+r2)...(1+rn) − 1`, **not** the sum of the returns. Summing (`r1+r2`) is only a first-order approximation and ignores compounding.
- **Each period's return applies to the value entering that period.** A −6% second-quarter return applies to the *post-first-quarter* balance ($10.8M), not the original ($10M).
- **CAGR (compound annual growth rate):** `CAGR = (V_end / V_begin)^(1/n) − 1` — the single constant annual rate that connects the endpoints. Example: $100M → $121M over 2 yrs ⇒ `(121/100)^(1/2) − 1 = 10%`. Dividing total return by n (21%/2 = 10.5%) is **wrong** — it ignores compounding.
- **Compounding growth factor:** `$1 → (1+r)^n`. `(1.07)^30 ≈ 7.61`. Small annual rate gaps compound into large terminal-wealth gaps; you cannot evaluate a 0.25pp gap by multiplying 0.25% × years.
- **Rule of 72:** doubling time ≈ `72 / (annual % return)`. 72/6 ≈ 12 yrs (exact `ln2/ln1.06 ≈ 11.9`); 72/4 ≈ 18 yrs. It is an approximation, not a guarantee.
- **Arithmetic mean** `(Σri)/n` = best estimate of a *single* future period's return. **Geometric mean** `(Π(1+ri))^(1/n) − 1` = the realized constant compound rate over multiple periods (describes terminal wealth).
- **Volatility drag / Jensen gap:** with any return dispersion, geometric mean ≤ arithmetic mean; they are equal only when every period's return is identical. +30%/−20% ⇒ arithmetic 5% but geometric `√1.04 − 1 ≈ 1.98%`.
- **Annualization units differ:** *returns* compound → `(1+r_period)^(periods/yr) − 1`; *volatility* scales with the **square root of time** → `σ_period × √(periods/yr)` (under i.i.d. assumption). E.g. 1% monthly → `(1.01)^12 − 1 ≈ 12.68%`; 3% monthly σ → `3%×√12 ≈ 10.39%`. Trading-day count (252) drives both figures.
- **Portfolio return = weighted sum of asset returns:** `r_p = Σ wi ri`. An asset's *return* (10%) differs from its *contribution* (weight × return = 6pp at 60% weight). Long weights >0, short weights <0; a negative weight × negative return = positive contribution.
- **Leverage:** invested weight >100% funded by borrowing magnifies both gains and losses; net financing cost (`−borrow% × borrow rate`) is subtracted. 120% ETF at 10% less 20% borrowed at 1% ⇒ `12% − 0.2% = 11.8%`.
- **Gross vs net vs benchmark-relative:** net = gross − fees − costs. Excess (relative) return = fund return − benchmark return. A fund can beat its benchmark on a relative basis while posting a negative absolute return (−6% vs −10% ⇒ +4pp). Hedge-fund fees layer: management fee on capital, then incentive fee on *post-management-fee* profit.
- **Path dependence / sequence-of-returns:** without cash flows, order doesn't matter (multiplication commutes). *With* withdrawals or contributions, order matters — same returns produce different terminal wealth. Equal ± percentage moves don't offset: +50% then −50% ⇒ $100→$150→$75.
- **Recovery asymmetry:** a loss of x% needs a gain larger than x% to recover, because the gain applies to a smaller base. −30% (100→70) needs `100/70 − 1 ≈ 42.86%`, not 30%; a 30% gain only reaches $91M (still 9% below peak).

## Common traps

- **Inverted-logic questions in this slice: NONE.** All 21 questions (G1Q1–G7Q3) use a plain `Answer Key:` — True = accurate statement, False = inaccurate. Do not assume inversion just because rationales say "reverses the correct conclusion" (that phrase describes the *choice's* embedded double negative, not the question's polarity).
- **Double-negative "embedded claim" choices — the real trap here.** Many choices are phrased as a negation, e.g. "Its CAGR is **not** 10% per year" or "The two-year cumulative return is **not** 4%." When the underlying fact IS true (CAGR *is* 10%), the negated statement is **False**. Read the whole sentence: verdict tracks the *negated* statement, and the rationale "reverses the correct conclusion" is your signal the writer buried a truth inside a "not."
- **"A reviewer would be wrong to accept the claim that..." choices.** These flip twice. If the underlying claim is correct, then "would be wrong to accept it" is itself **False** (rationale: "The underlying claim is correct and should be accepted"). Examples: G1Q3-A, G3Q3-A/B, G4Q2-E, G7Q3-C.
- **Summing instead of compounding.** Adding periodic returns (8% + −6% = 2%; +50% + −50% = 0%) is only an approximation and understates the compounding effect; the exact link is multiplicative. Classic distractor in G1Q2-C, G3Q1, G7Q1.
- **Arithmetic-for-geometric substitution.** Reporting the arithmetic mean as "the return you actually earned" overstates realized compound growth whenever returns vary (volatility drag). G3Q1-E, G3Q3-D.
- **Volatility annualized like a return.** Choices that scale σ by the period count (×12 or ×252) instead of by √(periods) are False — σ scales with √time. G4Q1-D, G4Q2-D.
- **Leverage "nets out."** Claims that a 100% *net* exposure means leverage is irrelevant ignore *gross* exposure and financing; both the >100% position and the borrow cost matter. G5Q3-D, G5Q2-D.

## Questions

### [QF-D1G1Q1] One-period returns, multiplicative linking, and price-vs-percentage
**Scenario:** A stock bought at $50 closes month 1 at $55 and month 2 at $52.25 (no dividends/costs). A junior analyst must explain the two monthly returns and the full-period return.
**Answer polarity:** Normal (True = accurate)

| Choice | Verdict | Why |
|---|---|---|
| A. First-month return is 10%. | True | HPR = (55 − 50)/50 = 5/50 = **10%**. Return is measured against the beginning value of that period. |
| B. Second-month return is −5%, relative to the $55 start-of-month value. | True | (52.25 − 55)/55 = −2.75/55 = **−5%**. The base is the value *entering* month 2 ($55), not the original $50. |
| C. Two-month cumulative return is 5% because the monthly returns sum to 5%. | False | Returns compound, not add: (1.10)(0.95) − 1 = 1.045 − 1 = **4.5%**. Summing (10% − 5% = 5%) ignores the interaction term and overstates the true link. |
| D. One dollar invested would **not** be worth $1.045 at the end. | False | Double-negative embedded claim: $1 actually *does* grow to $1 × 1.10 × 0.95 = **$1.045**. The negated statement reverses the correct conclusion, so it is False. |
| E. The $2.25 increase represents the same % return regardless of initial purchase price. | False | Percentage return = dollar change ÷ *starting price*, so it depends on the base. $2.25 on $55 (≈4.1%) differs from $2.25 on any other base. |

**Reference:** CFA curriculum — Time Value of Money / holding-period return; Investopedia, "Holding Period Return."

### [QF-D1G1Q2] Linking quarterly returns and applying each to the running balance
**Scenario:** A fund returns +8% in Q1 and −6% in Q2 (no cash flows or fees). The chair asks whether reporting a simple 2% first-half number is accurate.
**Answer polarity:** Normal (True = accurate)

| Choice | Verdict | Why |
|---|---|---|
| A. First-half cumulative return = (1.08)(0.94) − 1. | True | Consecutive periodic returns link multiplicatively via growth factors; this is the exact cumulative-return formula. |
| B. First-half cumulative return is 1.52%. | True | (1.08)(0.94) − 1 = 1.0152 − 1 = **1.52%**. |
| C. Adding the quarterly returns gives the exact cumulative return when periods are consecutive. | False | 8% + (−6%) = 2% ≠ 1.52%. Addition drops the cross-product (0.08 × −0.06); it is only an approximation. |
| D. On $10M start, the half-year ends at $10.152M. | True | $10M × 1.0152 = **$10.152M**, consistent with the 1.52% compounded return. |
| E. The Q2 dollar loss is **not** computed on the post-Q1 value. | False | Embedded double negative: the −6% *does* apply to the post-Q1 balance ($10.8M). The statement reverses the correct conclusion, so it is False. |

**Reference:** Bodie-Kane-Marcus, *Investments* — multi-period returns; Investopedia, "Cumulative Return."

### [QF-D1G1Q3] Percentage return vs dollar change across differently priced stocks
**Scenario:** Stock 1 rises $80→$88; Stock 2 rises $20→$24. A client calls Stock 1 the better performer because it gained more dollars. Evaluate (ignore dividends/costs).
**Answer polarity:** Normal (True = accurate)

| Choice | Verdict | Why |
|---|---|---|
| A. A reviewer would be **wrong to accept** the claim that the first stock earned 10%. | False | Twisted claim: the first stock *did* earn (88−80)/80 = **10%**, so accepting it is correct — "would be wrong to accept" is therefore False. |
| B. The second stock earned a 20% return. | True | (24 − 20)/20 = 4/20 = **20%**. |
| C. The first stock had the larger dollar price change per share. | True | +$8 (Stock 1) vs +$4 (Stock 2). Dollar change and percentage return are different metrics. |
| D. The first stock outperformed the second on a percentage-return basis. | False | 10% < 20%; the smaller, lower-priced stock had the higher percentage return. |
| E. With equal dollar amounts invested, the second investment would **not** produce the larger dollar profit. | False | Embedded double negative: with equal starting capital, the higher percentage return (20%) *does* produce the larger dollar profit. Reverses the correct conclusion, so False. |

**Reference:** CFA curriculum — return measurement basics; Investopedia, "Rate of Return."

### [QF-D1G2Q1] CAGR vs simple average of total return
**Scenario:** A private investment grows $100M→$121M over two years with no interim cash flows; the board asks for its CAGR to compare against annually quoted alternatives.
**Answer polarity:** Normal (True = accurate)

| Choice | Verdict | Why |
|---|---|---|
| A. Total two-year return is 21%. | True | 121/100 − 1 = **21%** cumulative. |
| B. Its CAGR is **not** 10% per year. | False | Embedded double negative: CAGR = (121/100)^(1/2) − 1 = √1.21 − 1 = **10%**. So it *is* 10%; the negation reverses the correct conclusion → False. |
| C. A 10.5% annual simple average is the realized annual compound growth rate. | False | 21%/2 = 10.5% ignores compounding. The true compound rate is 10% (since (1.10)2 = 1.21, not (1.105)2). |
| D. Compounding a 10% annual return for two years produces a 21% cumulative return. | True | (1.10)2 − 1 = 1.21 − 1 = **21%** — confirms 10% is the correct CAGR. |
| E. CAGR is the constant annual rate connecting the beginning and ending values. | True | By definition CAGR is the single geometric rate that maps V_begin to V_end over n periods. |

**Reference:** CFA curriculum — geometric mean / CAGR; Investopedia, "Compound Annual Growth Rate (CAGR)."

### [QF-D1G2Q2] Fee drag and long-horizon compounding
**Scenario:** Option 1 earns 8% gross less a 1% annual fee; Option 2 earns 7.25% with no fee, over 30 years, compounding annually (ignore taxes). Why does a small fee matter?
**Answer polarity:** Normal (True = accurate)

| Choice | Verdict | Why |
|---|---|---|
| A. Option 1's net rate is **not** 7% under the simplified fee assumption. | False | Embedded double negative: 8% gross − 1% fee = **7%** net under the stated simplification. The negation reverses this, so False. |
| B. At 7% net, $1 grows to ≈$7.61 over 30 years. | True | (1.07)^30 ≈ **7.61**. |
| C. At 7.25%, $1 grows to more than at 7% over the same horizon. | True | Same start and horizon, higher positive compound rate ⇒ greater terminal wealth ((1.0725)^30 > (1.07)^30). |
| D. The 0.25pp difference equals 0.25% × 30 in terminal-wealth terms. | False | Terminal wealth is exponential in the rate; you cannot linearize the gap by multiplying the rate difference by years. |
| E. Repeated compounding **cannot** make a small annual difference economically meaningful over a long horizon. | False | Embedded double negative: it *can* — each year's difference changes the base later returns compound on, so gaps widen over time. Reverses the correct conclusion → False. |

**Reference:** Bodie-Kane-Marcus, *Investments* — costs and compounding; Investopedia, "Compound Interest."

### [QF-D1G2Q3] Rule of 72 doubling-time intuition
**Scenario:** A client with a 6%-expected account asks how long it might take to double, acknowledging returns aren't guaranteed.
**Answer polarity:** Normal (True = accurate)

| Choice | Verdict | Why |
|---|---|---|
| A. Rule of 72 estimates ≈12 years to double at 6%. | True | 72 / 6 = **12 years** (approximate). |
| B. The estimate is 72 divided by the annual percentage return. | True | That is the standard Rule-of-72 formula. |
| C. The Rule of 72 guarantees doubling in the estimated period. | False | It is an approximation on an *assumed* rate — no guarantee of realized performance. |
| D. The exact doubling time at 6% is **not** slightly less than 12 years. | False | Embedded double negative: exact time = ln(2)/ln(1.06) ≈ **11.9 years**, which *is* slightly less than 12. The negation reverses this → False. |
| E. If the net return fell to 4%, the Rule of 72 would imply a longer doubling time. | True | 72 / 4 = **18 years** > 12 — lower rate means longer doubling time. |

**Reference:** Investopedia, "Rule of 72"; CFA curriculum — compounding intuition.

### [QF-D1G3Q1] Arithmetic vs geometric mean with a +30% / −20% pair
**Scenario:** A fund returns +30% then −20%; the analyst reports a 5% average. The committee asks whether that describes realized compound growth (no cash flows/fees).
**Answer polarity:** Normal (True = accurate)

| Choice | Verdict | Why |
|---|---|---|
| A. The arithmetic average return is 5%. | True | (30% + (−20%))/2 = **5%**. |
| B. The two-year cumulative return is **not** 4%. | False | Embedded double negative: (1.30)(0.80) − 1 = 1.04 − 1 = **4%**. So it *is* 4%; the negation reverses this → False. |
| C. The geometric average is **not** ≈1.98% per year. | False | Embedded double negative: geometric mean = √(1.04) − 1 ≈ **1.98%**. So it *is* ≈1.98%; negation reverses → False. |
| D. Investing $100 would produce $110.25 after two years. | False | Terminal value = $100 × 1.30 × 0.80 = **$104**, not $110.25 (which would be (1.05)2). |
| E. The arithmetic average overstates the annualized compound growth achieved. | True | 5% arithmetic > 1.98% geometric — the classic volatility-drag gap. |

**Reference:** CFA curriculum — arithmetic vs geometric mean; Investopedia, "Geometric Mean."

### [QF-D1G3Q2] Choosing arithmetic vs geometric mean by task
**Scenario:** An analyst must pick an averaging method for (a) estimating a representative one-year expected return and (b) describing the constant annual rate earned over the full sample.
**Answer polarity:** Normal (True = accurate)

| Choice | Verdict | Why |
|---|---|---|
| A. Arithmetic mean is generally more relevant for estimating a single future period's average outcome. | True | The arithmetic mean is the unbiased estimator of a single-period expected return from a sample. |
| B. Geometric mean describes the constant compound rate linking beginning to ending wealth over multiple periods. | True | The geometric mean reproduces realized multi-period terminal wealth. |
| C. The geometric mean is computed by adding periodic returns and dividing by n. | False | That is the *arithmetic* mean. Geometric mean multiplies growth factors and takes the n-th root: (Π(1+ri))^(1/n) − 1. |
| D. When returns vary and compound wealth stays positive, geometric mean cannot exceed arithmetic mean. | True | Return dispersion forces geometric ≤ arithmetic (Jensen's inequality / volatility drag); equal only with zero dispersion. |
| E. Arithmetic and geometric means are always identical when the sample has both + and − returns. | False | They are equal only when *every* periodic return is identical — mixed signs alone do not make them equal. |

**Reference:** CFA curriculum — mean return measures; Bodie-Kane-Marcus, *Investments* — average returns.

### [QF-D1G3Q3] Same arithmetic mean, different terminal wealth (volatility drag)
**Scenario:** Strategy A earns +10% each year; Strategy B earns +40% then −20%. Both average 10% arithmetically. Does $100 grow to the same terminal wealth?
**Answer polarity:** Normal (True = accurate)

| Choice | Verdict | Why |
|---|---|---|
| A. A reviewer would be **wrong to accept** the claim that Strategy A ends with $121. | False | Twisted claim: A *does* end at $100 × 1.10 × 1.10 = **$121**, so accepting it is correct → "wrong to accept" is False. |
| B. A reviewer would be **wrong to accept** the claim that Strategy B ends with $112. | False | Twisted claim: B *does* end at $100 × 1.40 × 0.80 = **$112**, so accepting it is correct → "wrong to accept" is False. |
| C. Both strategies have the same geometric average because their arithmetic averages are equal. | False | A's geometric = 10%; B's = √(1.12) − 1 ≈ **5.83%**. Equal arithmetic means do not imply equal geometric means. |
| D. Strategy B's greater return variability creates volatility drag vs its arithmetic average. | True | B's dispersion pulls compound growth (5.83%) below its 10% arithmetic mean — textbook volatility drag. |
| E. Strategy A has a 10% geometric average return. | True | Identical 10% returns each year ⇒ geometric mean = **10%** (no dispersion, no drag). |

**Reference:** Investopedia, "Volatility Drag"; CFA curriculum — geometric vs arithmetic returns.

### [QF-D1G4Q1] Annualizing a monthly return and monthly volatility
**Scenario:** A strategy earns 1% each month; risk reports 3% monthly volatility. Monthly returns compound; for volatility they are i.i.d. with stable variance. Give the annual figures.
**Answer polarity:** Normal (True = accurate)

| Choice | Verdict | Why |
|---|---|---|
| A. Compounded annual return ≈ 12.68%. | True | (1.01)^12 − 1 ≈ **12.68%**. |
| B. Multiplying 1% by 12 gives the exact compounded annual return. | False | 12% is a simple approximation; it omits intra-year compounding (the true value is 12.68%). |
| C. Annualized volatility ≈ 10.39%. | True | 3% × √12 ≈ 3% × 3.464 ≈ **10.39%** under i.i.d. scaling. |
| D. Monthly volatility is annualized by multiplying by 12. | False | Volatility scales with **√time**, not time: ×√12, not ×12. |
| E. Return and volatility use different common annualization rules here. | True | Returns compound (^12) while volatility scales by √12 — two distinct rules. |

**Reference:** CFA curriculum — annualizing returns and volatility; Investopedia, "Annualized Volatility."

### [QF-D1G4Q2] Annualizing daily figures with a 252-day count
**Scenario:** A desk sees a 0.04% mean daily return and 1.2% daily volatility, using 252 trading days, returns i.i.d.
**Answer polarity:** Normal (True = accurate)

| Choice | Verdict | Why |
|---|---|---|
| A. Mean daily × 252 gives an arithmetic annualized-return approximation of 10.08%. | True | 0.04% × 252 = **10.08%** (arithmetic/simple annualization). |
| B. Compounding 0.04% for 252 days gives ≈10.60% effective annual return. | True | (1.0004)^252 − 1 ≈ **10.60%** (compounded > simple). |
| C. Annualized volatility is **not** ≈19.05%. | False | Embedded double negative: 1.2% × √252 ≈ 1.2% × 15.87 ≈ **19.05%**. So it *is* ≈19.05%; negation reverses → False. |
| D. Annualized volatility = 1.2% × 252. | False | Volatility scales with √252, not 252 — the ×252 version massively overstates it. |
| E. A reviewer would be **wrong to accept** that the trading-day count affects both annualized figures. | False | Twisted claim: both the return (×252) and volatility (×√252) *do* use the day count, so the underlying claim is correct → "wrong to accept" is False. |

**Reference:** Bodie-Kane-Marcus, *Investments* — annualization conventions; Investopedia, "Trading Days / Annualizing."

### [QF-D1G4Q3] Putting monthly and annual returns on a consistent basis
**Scenario:** Strategy X earns 1.5% monthly; Strategy Y earns 14% annually. A flawed report called X superior by comparing 1.5 vs 14 directly. Put them on a consistent basis (X earns 1.5% every month).
**Answer polarity:** Normal (True = accurate)

| Choice | Verdict | Why |
|---|---|---|
| A. The two quoted returns should **not** be converted to the same horizon before comparison. | False | Embedded double negative: valid comparison *requires* consistent units/horizons. The negation reverses this → False. |
| B. Strategy X's effective annual return ≈ 19.56%. | True | (1.015)^12 − 1 ≈ **19.56%**. |
| C. Multiplying 1.5% by 12 gives an exact effective annual return of 18%. | False | 18% omits monthly compounding; it is a simple approximation, not the exact effective rate (19.56%). |
| D. Under the constant-return assumption, Strategy X has the higher annual return. | True | 19.56% (X) > 14% (Y) once both are annualized. |
| E. Comparing a monthly figure directly with an annual figure can mislead even when both are percentages. | True | Percentage notation alone does not equalize measurement periods — horizon must match. |

**Reference:** CFA curriculum — time-scale consistency; Investopedia, "Effective Annual Rate."

### [QF-D1G5Q1] Weighted portfolio return and asset-return-vs-contribution
**Scenario:** A fund starts 60% equities / 40% bonds; equities return +10%, bonds −5%, no rebalancing or cash flow. Find the pre-fee portfolio return.
**Answer polarity:** Normal (True = accurate)

| Choice | Verdict | Why |
|---|---|---|
| A. Equities contribute 6 percentage points. | True | 0.60 × 10% = **6.0pp** contribution. |
| B. Bonds contribute −2 percentage points. | True | 0.40 × (−5%) = **−2.0pp** contribution. |
| C. The portfolio return is 5%, the simple average of the two asset returns. | False | Must weight by allocation: 0.60×10% + 0.40×(−5%) = 4%. Equal-weight average (2.5%... or the 5% midpoint) does not apply. |
| D. The portfolio return is **not** 4%. | False | Embedded double negative: 6% + (−2%) = **4%**. So it *is* 4%; the negation reverses this → False. |
| E. Equity return and its portfolio contribution are the same because the return was positive. | False | Return (10%) ≠ contribution (6pp); contribution = weight × return, so the 60% weight makes them differ regardless of sign. |

**Reference:** CFA curriculum — portfolio return aggregation; Investopedia, "Weighted Average Return."

### [QF-D1G5Q2] Long-short weights and contribution signs
**Scenario:** A 130/30 fund is 130% long Stock A, 30% short Stock B (net 100%, gross 160%). A rises 6%, B rises 2%. Ignore financing/fees/rebalancing.
**Answer polarity:** Normal (True = accurate)

| Choice | Verdict | Why |
|---|---|---|
| A. Stock A contributes 7.8 percentage points. | True | 1.30 × 6% = **7.8pp** (leveraged long weight). |
| B. The short contributes −0.6pp because Stock B rose. | True | −0.30 × 2% = **−0.6pp**; a short loses when the shorted asset rises. |
| C. The portfolio return is **not** 7.2%. | False | Embedded double negative: 7.8% + (−0.6%) = **7.2%**. So it *is* 7.2%; the negation reverses → False. |
| D. 100% net exposure means leverage has no effect on return. | False | Gross exposure is 160%; the leveraged long and the short both affect return and risk regardless of net exposure. |
| E. If Stock B had fallen 2% instead, the short would have contributed positively. | True | −0.30 × (−2%) = **+0.6pp**; negative weight × negative return = positive contribution. |

**Reference:** Bodie-Kane-Marcus, *Investments* — long/short weights and leverage; Investopedia, "130-30 Strategy."

### [QF-D1G5Q3] Leverage and financing cost in portfolio return
**Scenario:** A portfolio invests 120% in a market ETF, financing the extra 20% by borrowing at 1% for the period. The ETF returns 10%. Give the pre-other-fee return, making leverage explicit.
**Answer polarity:** Normal (True = accurate)

| Choice | Verdict | Why |
|---|---|---|
| A. The ETF position contributes 12 percentage points. | True | 1.20 × 10% = **12pp** (levered long). |
| B. Borrowing cost reduces return by 0.2pp. | True | 0.20 borrowed × 1% = **0.2%** of portfolio capital, a drag. |
| C. The resulting portfolio return is **not** 11.8%. | False | Embedded double negative: 12% − 0.2% = **11.8%**. So it *is* 11.8%; negation reverses → False. |
| D. With 100% net invested weight, return must equal the ETF's 10%. | False | Borrowing creates 120% levered exposure; both the enlarged position and the financing cost move the return away from 10%. |
| E. If the ETF lost 10%, leverage would **not** magnify the loss before financing costs. | False | Embedded double negative: a 120% position contributes −12% vs −10% unlevered — leverage *does* magnify the loss. Reverses the correct conclusion → False. |

**Reference:** CFA curriculum — leverage and return; Investopedia, "Leverage / Margin."

### [QF-D1G6Q1] Gross, net, and benchmark-relative return
**Scenario:** A fund earns 12% gross; transaction costs = 2% and management fee = 1% of beginning capital (subtract both directly). Benchmark earns 8%. Did the strategy add value after costs?
**Answer polarity:** Normal (True = accurate)

| Choice | Verdict | Why |
|---|---|---|
| A. Net return is 9%. | True | 12% − 2% − 1% = **9%** under the stated simplification. |
| B. Gross excess return over benchmark is **not** 4 percentage points. | False | Embedded double negative: 12% − 8% = **4pp**. So it *is* 4pp; negation reverses → False. |
| C. Net excess return over benchmark is 1 percentage point. | True | 9% − 8% = **1pp**. |
| D. Since gross beat the benchmark, net must too regardless of costs. | False | Large enough costs/fees can erase or reverse gross outperformance — here they cut the 4pp gross edge to 1pp. |
| E. Reporting only the 12% gross return would overstate the investor's retained return. | True | The investor keeps 9% net, not 12% — gross overstates what is actually retained. |

**Reference:** CFA curriculum — gross vs net and excess return; Investopedia, "Excess Return / Net Return."

### [QF-D1G6Q2] Hedge-fund management + incentive fee waterfall
**Scenario:** A fund earns 15% on $100M; charges a 2% management fee on beginning capital and a 20% incentive fee on profit *after* the management fee (ignore high-water marks). Compute the simplified net.
**Answer polarity:** Normal (True = accurate)

| Choice | Verdict | Why |
|---|---|---|
| A. The management fee is **not** $2 million. | False | Embedded double negative: 2% × $100M = **$2M**. So it *is* $2M; negation reverses → False. |
| B. Profit remaining after the management fee is $13 million. | True | Gross profit $15M − $2M mgmt fee = **$13M**. |
| C. The incentive fee is $3 million because it is always 20% of gross profit. | False | Per the agreement, incentive fee = 20% of *post-management-fee* profit = 20% × $13M = **$2.6M**, not 20% of $15M. |
| D. The investor's net profit is **not** $10.4 million. | False | Embedded double negative: $15M − $2M − $2.6M = **$10.4M**. So it *is* $10.4M; negation reverses → False. |
| E. The investor's net return is 10.4%. | True | $10.4M / $100M beginning capital = **10.4%**. |

**Reference:** Bodie-Kane-Marcus, *Investments* — hedge fund fee structures; Investopedia, "Two and Twenty / Incentive Fee."

### [QF-D1G6Q3] Absolute vs benchmark-relative performance
**Scenario:** A tech long-only fund loses 6% while its tech benchmark loses 10%. A client says the manager failed (negative absolute return); the manager says it succeeded (beat benchmark). Distinguish the claims.
**Answer polarity:** Normal (True = accurate)

| Choice | Verdict | Why |
|---|---|---|
| A. The fund's absolute return is −6%. | True | Absolute performance is the fund's own return: **−6%**. |
| B. The fund's benchmark-relative return is **not** +4 percentage points. | False | Embedded double negative: −6% − (−10%) = **+4pp**. So it *is* +4pp; negation reverses → False. |
| C. The fund can have a negative absolute return and a positive relative return simultaneously. | True | Losing less than the benchmark (−6% vs −10%) yields positive *relative* performance despite the absolute loss. |
| D. Beating the benchmark means every investor objective was necessarily achieved. | False | Investors may also hold capital-preservation, risk, liability, or absolute-return objectives that a relative win doesn't satisfy. |
| E. Replacing the tech benchmark with cash could materially change the relative assessment. | True | Excess return depends on the chosen benchmark; vs cash (≈0%), −6% would look like underperformance — benchmark suitability matters. |

**Reference:** CFA curriculum — benchmark selection and relative performance; Investopedia, "Absolute vs Relative Return."

### [QF-D1G7Q1] Equal ± percentage moves do not offset
**Scenario:** A strategy gains 50% year 1, loses 50% year 2. The manager claims a 0% average means the portfolio finished where it started. Assess.
**Answer polarity:** Normal (True = accurate)

| Choice | Verdict | Why |
|---|---|---|
| A. The arithmetic average of the two returns is **not** 0%. | False | Embedded double negative: (50% + (−50%))/2 = **0%**. So it *is* 0%; the negation reverses this → False. |
| B. The portfolio finishes with the same value it started with. | False | $100 × 1.50 × 0.50 = **$75** — a 25% loss, not breakeven. |
| C. A 50% loss requires a 100% gain to recover fully. | True | To grow $75 back to $150 requires 150/75 − 1 = **100%** — recovery gain exceeds the loss %. |
| D. The geometric average return over the two years is **not** negative. | False | Embedded double negative: terminal wealth ($75) < start ($100), so the compound (geometric) rate *is* negative. Negation reverses → False. |
| E. Gains and losses can leave terminal wealth below the start even at 0% arithmetic average. | True | Returns compound multiplicatively; equal % up/down moves don't cancel (volatility drag). |

**Reference:** Investopedia, "Volatility Drag / Recovery Math"; CFA curriculum — geometric returns.

### [QF-D1G7Q2] Sequence-of-returns risk with withdrawals
**Scenario:** Two retirees start with $1M and withdraw $100k at each year-end. Portfolio A: +20% then −20%; Portfolio B: −20% then +20%. The adviser claims order can't matter. Ignore taxes/fees.
**Answer polarity:** Normal (True = accurate)

| Choice | Verdict | Why |
|---|---|---|
| A. Before withdrawals, the same two returns would **not** produce the same terminal wealth regardless of order. | False | Embedded double negative: without cash flows, multiplication commutes — (1.20)(0.80) = (0.80)(1.20), so order *does not* matter and terminal wealth *is* the same. Negation reverses → False. |
| B. After Year 1 return and withdrawal, Portfolio A has $1.1 million. | True | $1M × 1.20 − $100k = $1.2M − $0.1M = **$1.1M**. |
| C. After both years, Portfolio A has $800,000. | False | $1.1M × 0.80 − $100k = $880k − $100k = **$780,000**, not $800k. |
| D. After both years, Portfolio B has $740,000. | True | $1M × 0.80 − $100k = $700k; then $700k × 1.20 − $100k = $840k − $100k = **$740,000**. |
| E. Withdrawals create sequence-of-returns risk even though both have equal arithmetic and geometric averages. | True | Withdrawals change the capital exposed to later returns, so ordering ($780k vs $740k) matters — sequence risk. |

**Reference:** CFA curriculum — sequence-of-returns / cash-flow-weighted returns; Investopedia, "Sequence Risk."

### [QF-D1G7Q3] Drawdown and recovery asymmetry
**Scenario:** A strategy falls from a $100M peak to $70M, then recovers to $91M. The manager claims the 30% gain erased the 30% drawdown. Verify.
**Answer polarity:** Normal (True = accurate)

| Choice | Verdict | Why |
|---|---|---|
| A. The decline from $100M to $70M is **not** a 30% drawdown. | False | Embedded double negative: (70 − 100)/100 = **−30%**. So it *is* a 30% drawdown; negation reverses → False. |
| B. A 30% gain on $70M raises the portfolio to $91M. | True | $70M × 1.30 = **$91M**. |
| C. A reviewer would be **wrong to accept** that recovering $70M→$100M needs ≈42.86%. | False | Twisted claim: 100/70 − 1 ≈ **42.86%** is correct, so accepting it is right → "wrong to accept" is False. |
| D. A loss of x% is always recovered by a gain of x%. | False | The recovery gain applies to a smaller post-loss base, so it must exceed x% (30% loss needs ≈42.86% gain). |
| E. At $91M the portfolio remains 9% below its prior peak. | True | (91 − 100)/100 = **−9%**; the 30% gain did not restore the peak. |

**Reference:** Investopedia, "Drawdown / Recovery"; CFA curriculum — return asymmetry.

## References (domain-level)

- **CFA Program Curriculum** — Quantitative Methods: Time Value of Money, Rates of Return, and Statistical Measures of Asset Returns (arithmetic vs geometric mean, holding-period and money-/time-weighted returns).
- **Bodie, Kane & Marcus, *Investments*** — chapters on rates of return, risk and return over multiple periods, portfolio return aggregation, leverage, and hedge-fund fee structures.
- **Investopedia** — "Compound Annual Growth Rate (CAGR)," "Geometric Mean," "Arithmetic vs Geometric Mean," "Rule of 72," "Volatility Drag," "Annualized Volatility," "Sequence Risk," "Drawdown."
- **Investopedia** — "Holding Period Return," "Excess/Net Return," "Effective Annual Rate," and "Weighted Average Return" for periodic-return and portfolio-aggregation mechanics.
