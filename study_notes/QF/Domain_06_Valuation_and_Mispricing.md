# QF Domain 6 — Valuation and Mispricing

## Domain cheat-sheet

- **Market price vs. intrinsic value**: market price is an *observed* transaction/quotation value; intrinsic value is an *estimate* derived from a model and its inputs (expected cash flows, growth, discount rate). The two need not agree, and a gap between them is the *basis* for a trade — not proof of one.
  - Reasonable analysts can defensibly disagree on intrinsic value (different growth forecasts, risk assessments, discount rates, methods). The same market price can look overvalued under one model and undervalued under another.
  - A price move (e.g., on a merger rumor) can reflect the market's **probability-weighted** assessment of multiple outcomes, not a single certain value. Expected value depends on both scenario payoffs *and* their probabilities.
  - Market price does **not** uniquely reveal investors' intrinsic-value estimates or scenario probabilities.
- **Book value / asset-based valuation**: shareholder equity = assets − liabilities; book value per share = equity ÷ shares; price-to-book (P/B) = price ÷ book value per share.
  - Market value can *rationally* exceed book value because of earning power, growth, or unrecorded intangibles (human capital, internally developed brands/client networks). A high P/B is **not** conclusive evidence of overvaluation.
  - Book value is an accounting measure of *recorded* assets less liabilities — not the present value of future profits. P/B comparisons are most informative among firms with similar business models and accounting practices.
  - In **distress/liquidation**, reported book value can *overstate* recovery: assets may realize far below carrying amounts, liquidation creates costs, and creditors are senior — common equity is a residual and may recover nothing even when book equity is positive.
- **Time value of money (TVM)**: a dollar today is worth more than a dollar later. PV = FV / (1+r)^n; FV = PV × (1+r)^n. The discount rate reflects opportunity cost and the risk of the cash flow.
  - A larger nominal amount later is **not** automatically preferable — compare on a PV basis at the appropriate rate. Equal nominal payments at different times have *unequal* PV whenever r ≠ 0; only at r = 0 are they equal.
  - **Compounding** earns returns on prior returns, so growth exceeds simple interest. Longer-dated cash flows are more sensitive to the discount rate; a higher r lowers PV.
- **DCF & dividend valuation**: value = PV of future cash flows. Gordon constant-growth DDM: V = D1 / (r − g), valid only when g < r for a finite positive value.
  - Higher r → lower value; higher g → higher value (narrows the denominator). As g → r the denominator shrinks and valuation becomes explosive/unstable and hypersensitive.
  - **Terminal value** often dominates a DCF's present value, so long-run assumptions deserve careful sensitivity analysis. A precise-looking output is still only as good as its uncertain inputs.
- **Growth-based valuation**: compound projections build growth on prior-year growth, so multi-year cumulative growth ≠ (annual rate × years). Value is highly sensitive to small changes in the growth assumption (nonlinear). A biased starting cash-flow scales the entire projected path.
  - "Growth" vs. "value" are *descriptive* labels, not performance guarantees. A high multiple doesn't preclude undervaluation; a low multiple can reflect genuine impairment (a value trap). Long-run growth should be economically sustainable, not extrapolated from a single strong year.
- **Margin of safety & scenario analysis**: use bear/base/bull cases and probability-weighting to build a valuation *range* and avoid false precision. A margin of safety (buy sufficiently below conservative estimate) cushions estimation error but **cannot** guarantee against loss. Scenarios illuminate model risk but cannot eliminate it.
- **Long/short from mispricing**: go long undervalued, short overvalued. But correct valuation ≠ successful trade — timing/catalyst risk, financing/borrow costs, risk limits, and adverse price paths can force liquidation before convergence. A short has *theoretically unlimited* loss (price can rise without bound); position sizing must reflect downside scenarios, not just central-case upside.

## Common traps

- **No inverted-logic questions in this domain.** All 21 items (G1Q1–G7Q3) use plain "Answer Key:" → **Normal polarity (True = accurate).** There is no "(True = incorrect; False = accurate)" header anywhere in QF-D06, so do not invert. (Flag retained because inverted items *do* appear in sibling domains — always re-check the polarity line per question.)
- **Double-negative "embedded claim" choices** — phrased "*A reviewer would be wrong to accept the claim that* [an accurate statement]." The embedded claim is true and *should* be accepted, so the choice is **False**. Parse the inner claim, confirm it's accurate, then the "would be wrong to accept" wrapper makes the verdict False. Appears in: **G3Q2E, G4Q1C, G6Q1C, G6Q3E, G7Q2B, G7Q2C.**
- **Negation / "reversal" choices** — phrased "is **not** $X" or "would **not**..." where the arithmetic actually *is* X. The Answer Key marks these **False** with "The statement reverses the correct conclusion." Do the math, then negate the negation. Appears in: G2Q1A, G2Q1B, G2Q2B, G2Q3A, G2Q3C, G3Q1D, G3Q2D, G4Q3A, G4Q3B, G5Q1E, G5Q2D, G6Q1A, G6Q3D, G7Q1A.
- **"Guarantee/proof" absolutes are almost always False.** A price-value gap does not *guarantee* a profit (G1Q1D); market price does not *prove* estimates wrong (G1Q2E) or reveal the "true" value (G1Q3E); trading above book does not *prove* overvaluation (G2Q1D); a high P/B is not *conclusive* mispricing (G2Q2C); probability-weighted value does not *guarantee* a positive return (G6Q1D); a margin of safety cannot *guarantee* against loss; a correct thesis is not *sufficient* for a winning trade (G7Q3D).
- **Gordon-model denominator sensitivity**: watch g approaching r — value explodes and becomes *more* (not less) sensitive to error (G5Q2E). Requires g < r for a finite positive value (G4Q2D).
- **Simple vs. compound growth**: cumulative compound growth (e.g., 1.083 ≈ 25.97%) is greater than rate × years (24%) (G5Q1C); annual compounding beats simple interest (G3Q3C).
- **Short-selling payoff mechanics**: gross gain/loss = sell price − cover price; max loss is unbounded (not capped at the initial share price) (G7Q2D). Exiting early (forced cover) forfeits any later favorable move (G7Q3B).

## Questions

### [QF-D6G1Q1] Price vs. estimated value — is a gap enough to buy?
**Scenario:** An analyst pegs intrinsic value at $70 while the stock trades at $55; the PM asks whether the difference alone justifies an immediate buy.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Market price ($55) is an observed trading/quotation value, unlike a model-derived estimate — it is directly observable. |
| B | True | Intrinsic value ($70) depends on the analyst's inputs — expected cash flows, growth, and discount rate — so it is an estimate, not an observed fact. |
| C | True | If the $70 estimate is correct, the stock is undervalued by $70 − $55 = $15 per share. |
| D | False | The estimate may be wrong, and even a correct value can fail to converge within the investor's horizon — a gap does not *guarantee* profit. |
| E | False | Reverses the correct conclusion: reasonable analysts *can* estimate a different intrinsic value using different forecasts, risk assessments, and methods. |

**Reference:** Intrinsic value vs. market price, uncertainty of estimates — Damodaran, *Investment Valuation* (intro chapters on the nature of valuation); Investopedia "Intrinsic Value."

### [QF-D6G1Q2] Two analysts, one company — which value is "true"?
**Scenario:** Analyst A values a software firm at $40 (conservative growth, 12% rate); Analyst B at $65 (stronger growth, 9% rate); shares trade at $50. The committee asks who found the "true" value.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | $50 exceeds A's $40 estimate (overvalued to A) but is below B's $65 estimate (undervalued to B) — the same price reads both ways under defensible models. |
| B | True | A lower discount rate discounts future cash flows less heavily, raising estimated present value, all else equal. |
| C | False | Lower assumed growth reduces projected cash flows and thus lowers estimated value — it does not increase it. |
| D | False | Reverses the correct conclusion: disagreement *can* arise from uncertain forecasts and judgment, not just arithmetic error. |
| E | False | Market price records where trading occurs; it does not reveal a uniquely correct intrinsic value, so it cannot prove both estimates wrong. |

**Reference:** Discount-rate/growth inputs drive value; analyst disagreement — CFA equity valuation curriculum (DCF inputs); Investopedia "Discounted Cash Flow."

### [QF-D6G1Q3] Merger rumor — probability-weighted price
**Scenario:** A rumor lifts shares from $30 to $44; stand-alone value is $34 but a completed deal could be worth $48. The fund weighs trading before confirmation.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The $44 price can reflect a probability-weighted blend of deal ($48) and no-deal ($34) outcomes, not a single certain value. |
| B | False | Comparing $44 only to the $34 stand-alone estimate ignores the credible acquisition scenario and its probability — insufficient to prove mispricing. |
| C | True | A reasonable ex ante price can still produce a loss when the uncertain adverse outcome (deal fails) occurs. |
| D | True | Expected value depends on both scenario payoff magnitudes and their probabilities — a valuation trade must weigh both. |
| E | False | The price increase does not uniquely identify investors' scenario valuations or probabilities with certainty. |

**Reference:** Probability-weighted (expected-value) valuation, merger arbitrage intuition — CFA curriculum (scenario/expected-value analysis); Investopedia "Expected Value," "Risk Arbitrage."

### [QF-D6G2Q1] Quick book-value assessment
**Scenario:** A manufacturer reports $500M assets, $320M liabilities, 30M shares, trading at $9.00. The PM wants a fast book-value read.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Reverses the correct conclusion: equity = assets − liabilities = $500M − $320M = $180M, so equity *is* $180M. |
| B | False | Reverses the correct conclusion: $180M ÷ 30M shares = $6.00, so book value per share *is* $6.00. |
| C | True | P/B = $9.00 ÷ $6.00 = 1.5. |
| D | False | Market value may rationally exceed book value due to earning power, growth, or unrecorded intangibles — trading above book does not prove overvaluation. |
| E | True | A $60M write-down cuts equity to $120M → $120M ÷ 30M = $4.00 per share. |

**Reference:** Book value per share, price-to-book — Investopedia "Book Value Per Share," "Price-to-Book (P/B) Ratio"; CFA financial-statement/asset-based valuation.

### [QF-D6G2Q2] High P/B on an intangible-heavy firm
**Scenario:** A profitable consulting firm with few physical assets but strong human capital and client relationships trades at 4× book value; a client concludes it must be severely overpriced.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Internally developed human capital and client relationships are often not recognized as balance-sheet assets, so book value understates economic value. |
| B | False | Reverses the correct conclusion: book value *is* based on accounting measurement of recorded assets less liabilities, not a direct estimate of future earning power. |
| C | False | A high P/B must be interpreted alongside profitability, asset composition, growth, and accounting choices — it is not conclusive evidence of mispricing. |
| D | True | P/B comparisons are more informative when firms share similar business models and accounting conventions. |
| E | True | A small accounting denominator (few recorded assets) can produce a high P/B even when market value is economically reasonable. |

**Reference:** Limits of accounting book value, intangibles, comparability of multiples — Damodaran on relative valuation/multiples; Investopedia "Price-to-Book Ratio," "Intangible Asset."

### [QF-D6G2Q3] Distressed retailer — liquidation vs. book equity
**Scenario:** A distressed retailer carries inventory at $100M book with $40M total book equity; forced liquidation might fetch only $55M for inventory, plus material closing costs. A distressed-debt team evaluates the equity.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Reverses the correct conclusion: reported book value *can* overstate liquidation proceeds — distressed assets realize less than carrying value and liquidation itself has costs. |
| B | True | Marking inventory from $100M to $55M reduces asset value by $45M. |
| C | False | Reverses the correct conclusion: a $45M markdown *exceeds* the $40M equity cushion, so it does eliminate reported equity (before closing costs). |
| D | True | Creditors have claims senior to common shareholders in liquidation. |
| E | False | Positive book equity does not guarantee positive recovery — markdowns, senior claims, and liquidation costs can leave nothing for common shareholders. |

**Reference:** Liquidation/distress value, priority of claims, book value limits — CFA (asset-based valuation, distressed); Investopedia "Liquidation Value," "Absolute Priority Rule."

### [QF-D6G3Q1] $100M today vs. $121M in two years at 10%
**Scenario:** A pension fund can take $100M today or a guaranteed $121M in two years; opportunity cost is 10% annually. The committee asks whether the choices are economically equivalent.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | PV of $121M in two years at 10% = $121M ÷ 1.102 = $100M. |
| B | True | FV of $100M for two years at 10% = $100M × 1.102 = $121M. |
| C | False | At a 10% opportunity cost the two are equivalent; a larger nominal amount later is not strictly preferable once discounted. |
| D | False | Reverses the correct conclusion: at 12%, PV = $121M ÷ 1.122 ≈ $96.46M, which *is* less than $100M. |
| E | True | The discount rate reflects the return on a comparable alternative and the risk of the cash flow. |

**Reference:** Present value / future value, discount-rate selection — Investopedia "Time Value of Money," "Present Value"; CFA quantitative methods (TVM).

### [QF-D6G3Q2] Timing of equal payments (year 1 vs. year 4)
**Scenario:** Two risk-equivalent contracts each pay $50,000 — Contract A at end of year 1, Contract B at end of year 4 — with a positive annual discount rate.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The same payment discounted for fewer periods (year 1) has the higher present value. |
| B | False | Equal nominal payments have equal PV only at a zero rate; with a nonzero rate, timing changes PV. |
| C | True | The longer-dated payment is more sensitive to the discount rate, so a higher rate widens A's PV advantage. |
| D | False | Reverses the correct conclusion: at a zero discount rate both PVs equal their $50,000 nominal amounts (they *are* equal). |
| E | False | The embedded claim (earlier cash allows reinvestment before year 4) is correct and should be accepted, so it is wrong to reject it. |

**Reference:** Discounting and timing sensitivity — Investopedia "Time Value of Money," "Present Value"; CFA quantitative methods (TVM).

### [QF-D6G3Q3] Endowment set-aside vs. future commitment
**Scenario:** An endowment sets aside $100,000 today at 6% annual compounding to meet a forecast $130,000 commitment in five years.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | FV = $100,000 × 1.065 ≈ $133,823. |
| B | True | $133,823 exceeds the $130,000 commitment by ≈ $3,823, so the set-aside is expected to cover it. |
| C | False | Annual compounding earns returns on prior returns, so growth exceeds simple interest of $6,000/year. |
| D | True | A realized return below 6% produces a smaller compound future value, all else equal. |
| E | False | At a positive discount rate, the PV of $130,000 is *less* than $130,000, not greater. |

**Reference:** Compound interest vs. simple interest, future/present value — Investopedia "Compound Interest," "Future Value"; CFA quantitative methods (TVM).

### [QF-D6G4Q1] Dividend discount model — does a higher discount rate raise value?
**Scenario:** An analyst values a stable dividend payer with a DDM; the CFO argues a higher discount rate should *increase* estimated value because investors demand a higher return.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | A higher discount rate discounts future dividends more heavily, lowering present value (the CFO is wrong). |
| B | True | A lower discount rate discounts future cash flows less, raising estimated intrinsic value. |
| C | False | The embedded claim (discount rate = opportunity cost / required return) is correct and should be accepted, so it is wrong to reject it. |
| D | False | The discount rate is a key present-value input; holding dividends constant, value still changes with the rate. |
| E | False | Reverses the correct conclusion: long-duration cash flows are *especially* sensitive to the discount rate, so small changes can materially move value. |

**Reference:** Dividend discount model, discount-rate mechanics — Investopedia "Dividend Discount Model," "Discount Rate"; CFA equity valuation (DDM).

### [QF-D6G4Q2] Gordon constant-growth DDM valuation
**Scenario:** A utility pays $3.00 next year with 4% perpetual growth; the analyst uses a 9% required return in the constant-growth DDM.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Gordon model: V = $3.00 ÷ (0.09 − 0.04) = $3.00 ÷ 0.05 = $60.00. |
| B | True | Raising r to 10% gives V = $3.00 ÷ (0.10 − 0.04) = $3.00 ÷ 0.06 = $50.00. |
| C | False | Raising g to 5% narrows the denominator (0.09 − 0.05 = 0.04), *raising* value to $75.00 — not reducing it. |
| D | True | The model requires g < r; if g ≥ r the perpetuity formula yields no finite positive value. |
| E | False | The $60.00 output is highly dependent on uncertain dividend, growth, and required-return assumptions — not "certain." |

**Reference:** Gordon growth model, g < r constraint — Investopedia "Gordon Growth Model," "Dividend Discount Model"; CFA equity valuation (constant-growth DDM).

### [QF-D6G4Q3] Two-stage DCF with dominant terminal value
**Scenario:** A DCF projects FCF of $10M (yr 1) and $12M (yr 2) plus a $120M terminal value at end of year 2, all discounted at 10%.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Reverses the correct conclusion: PV of year-1 FCF = $10M ÷ 1.10 ≈ $9.09M (it *is* ≈ $9.09M). |
| B | False | Reverses the correct conclusion: ($12M + $120M) ÷ 1.102 ≈ $109.09M (it *is* ≈ $109.09M). |
| C | True | Enterprise value ≈ $9.09M + $109.09M ≈ $118.18M. |
| D | False | Terminal value alone contributes ≈ $99.17M ($120M ÷ 1.102) — well over half of the ≈ $118.18M total, not less than half. |
| E | True | A valuation dominated by terminal value is especially sensitive to long-run assumptions, warranting sensitivity analysis. |

**Reference:** Multi-period DCF, terminal value, sensitivity — Damodaran on DCF/terminal value; Investopedia "Discounted Cash Flow," "Terminal Value"; CFA equity valuation (FCFF/DCF).

### [QF-D6G5Q1] Compounding a growth projection
**Scenario:** A firm generates $5.0M annual FCF; an analyst projects 8% annual growth for three years, and the risk committee asks the team to verify the compounding logic.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Year-1 FCF = $5.0M × 1.08 = $5.40M. |
| B | True | Year-3 FCF = $5.0M × 1.083 ≈ $6.30M. |
| C | False | Compound three-year growth is ≈ 25.97% (1.083 − 1), not exactly 24% (8% × 3) — simple multiplication understates it. |
| D | True | Each year's growth compounds on the prior year's enlarged base — growth applied to earlier growth. |
| E | False | Reverses the correct conclusion: an overstated starting value scales the *entire* projected path, so each cash flow *is* biased upward. |

**Reference:** Compound growth vs. simple growth, projection base sensitivity — Investopedia "Compound Annual Growth Rate (CAGR)," "Compound Interest"; CFA (growth forecasting). 

### [QF-D6G5Q2] Sensitivity of DDM value to perpetual growth
**Scenario:** A mature firm's next dividend is $2.00; analyst uses a 10% required return with 4% perpetual growth, but a colleague proposes bumping growth to 5% based on one strong year.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | At 4% growth: V = $2.00 ÷ (0.10 − 0.04) ≈ $33.33. |
| B | True | At 5% growth: V = $2.00 ÷ (0.10 − 0.05) = $40.00. |
| C | False | The value rises ≈ 20% ($33.33 → $40.00), far more than 1% — sensitivity is nonlinear, not one-for-one. |
| D | False | Reverses the correct conclusion: long-run growth *should* be economically sustainable and *not* extrapolated mechanically from a single strong year. |
| E | False | As g approaches r the denominator shrinks, making valuation *more* sensitive and unstable — not less. |

**Reference:** Gordon-model denominator sensitivity, sustainable growth — Investopedia "Gordon Growth Model," "Sustainable Growth Rate"; CFA equity valuation (growth assumptions).

### [QF-D6G5Q3] Growth vs. value labels and future returns
**Scenario:** A PM compares a high-multiple fast-growing tech stock with a low-multiple slow-growing industrial; a client labels them "growth" and "value" and assumes the labels dictate future returns.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | A growth stock's valuation depends heavily on expectations of future expansion (much value sits in far-future cash flows). |
| B | False | Reverses the correct conclusion: a value stock *can* still be overvalued if a low multiple reflects deteriorating fundamentals (a value trap), not mispricing. |
| C | False | A high multiple alone does not determine price relative to intrinsic value — a growth stock *can* be undervalued. |
| D | True | If expected growth fails to materialize, both forecast cash flows and the multiple can fall, cutting the growth stock's valuation substantially. |
| E | True | Growth/value are descriptive inputs, not performance guarantees — either can outperform depending on price, realized fundamentals, and expectations. |

**Reference:** Growth vs. value characteristics, value traps — Investopedia "Growth Stock," "Value Stock," "Value Trap"; CFA equity (style classification).

### [QF-D6G6Q1] Probability-weighted scenario value
**Scenario:** A team estimates bear/base/bull values of $40/$60/$90 at 25%/50%/25% probabilities; shares trade at $50. The PM asks whether the scenario analysis supports buying.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Reverses the correct conclusion: 0.25($40) + 0.50($60) + 0.25($90) = $62.50 (it *is* $62.50). |
| B | True | ($62.50 − $50) ÷ $62.50 = 20% below the probability-weighted estimate. |
| C | False | The embedded claim (a fall from $50 to $40 is a 20% loss) is correct and should be accepted, so it is wrong to reject it. |
| D | False | One outcome will actually occur, probabilities may be wrong, and price may not converge — the weighted value does not guarantee a positive return. |
| E | True | A scenario framework exposes downside, central, and upside assumptions rather than hiding them in a single point estimate. |

**Reference:** Expected value, scenario analysis, valuation ranges — CFA (scenario/sensitivity analysis); Investopedia "Expected Value," "Scenario Analysis."

### [QF-D6G6Q2] Reporting a valuation range vs. false precision
**Scenario:** A model outputs an intrinsic value of $73.42; the CRO asks for a reasonable range because revenue growth, margins, and the discount rate are uncertain.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Reporting $73.42 without sensitivity analysis implies more precision than uncertain inputs justify (false precision). |
| B | True | A valuation range shows how plausible combinations of assumptions affect the conclusion. |
| C | False | A bear case uses *less* favorable assumptions than the base and bull cases — not assumptions at least as optimistic as the bull case. |
| D | True | If every plausible scenario yields a value below market price, the analysis does not support an undervaluation thesis. |
| E | False | Scenario analysis illuminates model risk but cannot *eliminate* it — omitted variables, structural errors, and poor probability judgments remain. |

**Reference:** Valuation ranges, avoiding false precision, model risk — Damodaran on uncertainty in valuation; Investopedia "Sensitivity Analysis," "Scenario Analysis."

### [QF-D6G6Q3] Margin-of-safety rule check
**Scenario:** A value fund requires a 25% margin of safety vs. its conservative estimate; the analyst values a firm at $80 conservatively and its stock trades at $62. The committee asks whether it clears the rule.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | A 25% discount to $80 = $80 × (1 − 0.25) = $60 maximum purchase price. |
| B | True | ($80 − $62) ÷ $80 = 22.5% below the estimate. |
| C | False | The 22.5% discount is *smaller* than the required 25%, so the stock does not satisfy the rule at $62. |
| D | False | Reverses the correct conclusion: a revised $72 estimate gives a permitted price of $72 × 0.75 = $54 (it *does* fall to $54). |
| E | False | The embedded claim (a margin of safety reduces exposure to estimation error but cannot guarantee against loss) is correct and should be accepted. |

**Reference:** Margin of safety — Graham, *The Intelligent Investor* (margin-of-safety principle); Investopedia "Margin of Safety."

### [QF-D6G7Q1] Long position sizing under upside/downside
**Scenario:** A fund estimates a stock worth $80 trades at $60, with a $45 bear case, and a possible strategic-review catalyst within six months. The PM considers going long.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Reverses the correct conclusion: ($80 − $60) ÷ $60 ≈ 33.3% (convergence *would* produce ≈ 33.3% gain). |
| B | True | ($60 − $45) ÷ $60 = 25% loss to the bear case. |
| C | True | A strategic review may act as a catalyst, but its occurrence and price effect are uncertain. |
| D | False | Buying below estimated value does not remove timing risk — price can stay below value or fall further for a long time. |
| E | True | Position sizing should reflect the full payoff distribution (downside scenarios), not just the central-case upside. |

**Reference:** Catalyst/timing risk, position sizing from payoff distribution — CFA (portfolio construction, risk); Investopedia "Catalyst," "Margin of Safety," "Risk Management."

### [QF-D6G7Q2] Short-sale payoff and risk review
**Scenario:** A short seller thinks a $120 stock is worth $90, but there is no near-term catalyst, borrow costs are high, and enthusiasm is rising. The risk manager reviews the trade.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Selling at $120 and repurchasing at $90 yields a $30 gross gain per share before costs. |
| B | False | The embedded claim ($30 ÷ $120 = 25% gross return before financing/borrow fees) is correct and should be accepted. |
| C | False | The embedded claim (repurchasing at $150 after selling at $120 = $30 loss per share before costs) is correct and should be accepted. |
| D | False | A stock's price can rise without bound, so an uncovered short has theoretically *unlimited* loss — not capped at the $120 share price. |
| E | True | High borrow costs and uncertain timing can make the trade unsuccessful even if the $90 valuation is ultimately correct. |

**Reference:** Short-selling mechanics, unlimited loss, carrying costs — Investopedia "Short Selling," "Short Squeeze," "Cost of Carry"; CFA (short positions, financing).

### [QF-D6G7Q3] Correct thesis, losing trade (forced cover)
**Scenario:** A fund shorts a $50 stock it values at $30; momentum drives it to $85, breaching a risk limit and forcing a cover; two years later the stock falls to $28. The committee evaluates the original thesis.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The eventual decline to $28 is consistent with (though not alone proof of) the original overvaluation thesis. |
| B | False | The fund exited at $85 and did not participate in the later decline, so the realized trade was a loss, not a profit. |
| C | True | Shorting at $50 and covering at $85 is a $35 loss per share before costs. |
| D | False | A correct long-run thesis is not sufficient — adverse interim moves can force liquidation or exhaust capital before convergence. |
| E | True | Financing, risk limits, catalysts, and timing all matter in translating a valuation view into a successful trade; value and trade viability are distinct. |

**Reference:** Value vs. trade outcome, forced liquidation, "markets can stay irrational longer than you can stay solvent" — CFA (risk limits, drawdown); Investopedia "Short Squeeze," "Margin Call," "Risk Management."

## References (domain-level)

1. **Damodaran — *Investment Valuation* / *The Dark Side of Valuation*:** intrinsic value vs. price, DCF and terminal-value mechanics, relative valuation/multiples, and the role of uncertainty and assumptions in valuation.
2. **CFA Program Curriculum — Equity Valuation & Quantitative Methods:** discounted cash flow (FCFF/FCFE), dividend discount models (constant-growth/Gordon), time value of money, scenario/sensitivity analysis, and asset-based/liquidation valuation.
3. **Investopedia:** "Intrinsic Value," "Discounted Cash Flow," "Dividend Discount Model," "Gordon Growth Model," "Book Value Per Share," "Price-to-Book (P/B) Ratio," "Time Value of Money," "Present/Future Value," "Compound Interest," "Terminal Value," "Growth/Value Stock," "Margin of Safety," "Short Selling."
4. **Benjamin Graham — *The Intelligent Investor*:** the margin-of-safety principle and buying below conservative intrinsic-value estimates.
5. **General finance principles:** mean reversion / convergence of price to fair value, expected-value (probability-weighted) valuation, and the distinction between a correct valuation thesis and a successful trade (timing, catalyst, and financing risk).
