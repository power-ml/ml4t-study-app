# QF Domain 7 — CAPM, Alpha, Beta, and Hedging

## Domain cheat-sheet

- **Market model / return decomposition.** A single-factor model writes an asset's return as
  `r = α + β·r_market + ε`:
  - **Market-related (systematic) component** = `β·r_market` — the part explained by the modeled benchmark exposure.
  - **Alpha (α, intercept)** = predicted return when the market return *and* residual are both zero; the benchmark-unexplained expected return.
  - **Residual (ε, idiosyncratic/asset-specific) component** = `actual − predicted` = the part left unexplained after applying the fitted model. A negative residual can coexist with a positive total return (and vice versa) when the other components dominate.
  - Total = intercept + market-related + residual. These simply **sum**.
- **Beta = slope = sensitivity.** `β = Cov(asset, market) / Var(market) = ρ · (σ_asset / σ_market)`.
  - β > 1 → amplifies market moves; β < 1 → dampens; β = 1 → moves with market; β < 0 → moves inverse (negative covariance). Zero covariance → **β = 0** (zero numerator).
  - Beta is an **estimate** of an *average* linear relationship — realized returns still contain residual variation, so beta never "guarantees" an exact move on any given day.
  - Beta measures **exposure, not skill**; a high beta amplifies bull-market returns without producing alpha.
  - Beta is empirical: it can change with return horizon, sample period, frequency, and market regime.
- **Alpha and active performance.** Realized alpha (Jensen's alpha) = `actual return − CAPM-implied return`, where CAPM-implied = `r_f + β·(r_market − r_f)`.
  - Raw return vs. market is **not** risk-adjusted: a high-beta fund "should" beat the market in an up year purely from exposure. Alpha isolates skill from that exposure.
  - One positive observation ≠ persistent skill (luck, residual risk, estimation error). And a positive *point estimate* is not automatically statistically significant — check estimate/standard-error ratio.
  - **Statistical vs. economic significance are distinct.** An effect can be statistically detectable yet vanish after costs (net alpha = gross alpha − implementation cost), or be economically large yet imprecisely estimated.
- **Correlation vs. beta.** Correlation is *standardized directional co-movement* (unitless, in [−1, 1]); beta scales correlation by the *volatility ratio* `σ_asset/σ_market`. They are **not** interchangeable.
  - High correlation can pair with a **low** beta (asset less volatile than the market).
  - High total volatility can pair with a **low** beta (low correlation → most of the volatility is idiosyncratic, unrelated to the market).
- **Portfolio beta = weighted average of component betas** (weights relative to equity). Long positions add, shorts subtract, cash contributes zero.
  - A positive-weighted average lies within the range of the component betas.
  - **Beta-weighted (dollar) exposure** = `Σ (position$ × β)`; portfolio beta relative to equity = net beta-dollars / equity.
  - **Leverage** shows up in **gross** exposure (sum of absolute risky weights), not in signed weights — signed weights can sum to 100% while gross exposure exceeds it.
- **Dollar neutrality ≠ beta (market) neutrality.**
  - **Dollar neutral** = equal long and short *dollar* amounts. **Beta neutral** = beta-weighted exposures cancel.
  - Equal dollars do **not** imply equal market risk when the two legs have different betas; to neutralize beta you generally need **unequal** dollar amounts (short more of a lower-beta leg, less of a higher-beta leg). Hedge ratio = `β_long/β_hedge`.
- **Hedging and residual risk.** A market/index hedge is designed to remove **systematic** return while **retaining** asset-specific (alpha) return before costs.
  - It does **not** eliminate all loss: idiosyncratic / company-specific news, basis risk, liquidity, and model risk remain.
  - Hedges are **imperfect**: beta estimation error and time-varying beta leave unintended exposure; pair trades carry relative-value / relationship-breakdown risk; and financing, trading costs, and imperfect index matching create return drag.

## Common traps

- **No inverted-logic questions in this domain.** Every question here is **Normal polarity (True = accurate)**. There is no "True = incorrect; False = accurate" block in QF Domain 7 — but always re-read each Answer Key line, because the trap below mimics inversion at the *choice* level.
- **Negation-framed "…is not X" choices (the dominant trap).** Many choices assert a *correct* number/relationship in negated form ("The market excess return is **not** 8%", "Portfolio beta is **not** 1.04"). Because the true value *is* that number, the negated claim is **False**, and the Answer Key repeatedly says *"The statement reverses the correct conclusion."* Compute the quantity first, then check whether the "not" makes the sentence lie. Negation-framed False choices: **G1Q1 A, G1Q1 B, G1Q3 B, G2Q3 C, G3Q1 A, G3Q3 B, G3Q3 C, G4Q3 A, G5Q1 C, G5Q1 D, G5Q2 D, G5Q3 C, G5Q3 D, G6Q2 C, G6Q3 A, G7Q2 B, G7Q3 A, G7Q3 B.** (When the "not" statement instead negates a *false* claim, it flips True — e.g., G7Q1 A-style; read carefully.)
- **"Guarantees / must / exactly / every" absolutes are almost always False.** Beta, alpha, correlation, and hedge ratios are *estimates of averages*. Choices claiming a beta "guarantees" an exact move (G2Q1 C), a negative beta "guarantees" a positive return in a decline (G2Q2 C), an in-sample intercept guarantees future alpha (G1Q2 C), one year proves persistent skill (G3Q1 E), or a hedge keeps realized beta "exactly zero in every future period" (G7Q3 D) are wrong.
- **Exposure ≠ skill; raw outperformance ≠ alpha.** A high-beta fund beating the market (G3Q3 D, G3Q3 C) or high raw returns in a bull market (G3Q3 E) reflect systematic exposure, not manager alpha. Comparing fund return to market return without adjusting for beta (G3Q1 D) does **not** risk-adjust.
- **Dollar neutral is not market neutral.** Watch every choice that calls a dollar-balanced book "market neutral" (G6Q1) — beta-weighted exposures must cancel, which usually requires unequal dollars (G6Q2, G7Q2). Conversely a beta-neutral book is typically **not** dollar neutral (G6Q2 D).
- **Hedges retain idiosyncratic risk and alpha.** Choices saying a hedge "eliminates all possible losses" (G7Q1 B) or "cannot retain" a positive asset-specific return (G7Q1 D) invert the purpose of a market hedge: it removes systematic risk and *keeps* residual/alpha, but leaves company-specific, basis, model, and cost risk.

## Questions

### [QF-D7G1Q1] Return decomposition: intercept + market component + residual
**Scenario:** A stock's monthly return is modeled as `0.2% + 1.3 × market return + residual`. In one month the market returns 2.0% and the residual is −0.5%.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Negation trap. The market-related component is `β·r_market = 1.3 × 2.0% = 2.6%`, so "not 2.6%" reverses the correct conclusion. |
| B | False | Negation trap. Total = intercept + market component + residual = `0.2% + 2.6% − 0.5% = 2.3%`, so "not 2.3%" is false. |
| C | False | A negative residual does not force a negative total return — here the positive intercept and positive market component outweigh the −0.5% residual (total = +2.3%). |
| D | True | In `r = α + β·r_market + ε`, the intercept (0.2%) is exactly the predicted return when both the market return and the residual are zero. |
| E | True | The residual is the asset-specific piece left unexplained after applying the fitted intercept and modeled market exposure (actual − predicted). |

**Reference:** Single-factor market model / return decomposition — Bodie-Kane-Marcus *Investments*, "The Index Model" chapter; Investopedia "Systematic vs. Unsystematic Risk."

### [QF-D7G1Q2] Regression interpretation: slope, intercept, residuals, benchmark dependence
**Scenario:** A fund's monthly excess returns are regressed on a broad equity index's excess returns; intercept = 0.15%/month, beta = 0.8, residuals vary substantially.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Beta is the fitted regression slope relating the fund's excess return to the benchmark's excess return. |
| B | True | A beta of 0.8 implies a ~0.8-for-1 expected response: a 1% benchmark excess return maps to ~0.8% fund excess return before the residual. |
| C | False | An in-sample intercept is an *estimate* of average alpha, not a guarantee of exactly 0.15% every future month. |
| D | True | Large residual variation means the benchmark leaves much of the fund's return variation unexplained (idiosyncratic component). |
| E | False | Alpha and beta are measured *relative to the chosen benchmark/model*; a materially different benchmark can change both estimates. "Could not change" reverses this. |

**Reference:** Index-model regression, alpha/beta estimation — Bodie-Kane-Marcus *Investments*, index model & Security Characteristic Line; Investopedia "Jensen's Measure (Alpha)."

### [QF-D7G1Q3] Zero-intercept model: residual as actual minus predicted
**Scenario:** A stock has beta 1.2 and a zero intercept. The market falls 4%; the stock falls only 2%.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | With a zero intercept, predicted market-related return = `1.2 × −4% = −4.8%`. |
| B | False | Negation trap. Residual = actual − predicted = `−2.0% − (−4.8%) = +2.8%`, so "not +2.8%" reverses the correct conclusion. |
| C | False | A positive residual does not force a positive total return — realized total was −2% despite outperforming the −4.8% prediction. |
| D | False | One positive residual is not evidence of persistent alpha; that requires many observations and accounting for estimation uncertainty. |
| E | True | Losing 2% beats the modeled −4.8%, so benchmark-adjusted (residual) performance was positive even though the stock lost money. |

**Reference:** Residual return = actual − model-predicted; benchmark-relative performance — Grinold & Kahn *Active Portfolio Management* (residual return/risk); Bodie-Kane-Marcus index model.

### [QF-D7G2Q1] Beta as market sensitivity (β = 1.5, no alpha/residual)
**Scenario:** A cyclical stock has beta 1.5, interpreted with a simple market model (no alpha, no residual).
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Modeled response to a +4% market = `1.5 × 4% = 6%`. |
| B | True | The same linear exposure gives `1.5 × −4% = −6%` when the market falls 4%. |
| C | False | Beta is an *average* estimated relationship; realized returns also contain residual variation, so it cannot "guarantee exactly 1.5× every day." |
| D | True | A larger beta (1.5 vs. 0.7) means greater modeled sensitivity to the benchmark. |
| E | False | Beta measures market exposure, not stock-selection skill or abnormal (alpha) performance. |

**Reference:** Beta as SCL slope / market sensitivity — Sharpe CAPM; Investopedia "Beta."

### [QF-D7G2Q2] Negative beta: inverse co-movement, hedging value, volatility sign
**Scenario:** An asset has beta −0.4 vs. the equity market; a PM considers adding it to a long-only equity portfolio.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Modeled market component = `−0.4 × 5% = −2%` when the market returns +5%. |
| B | True | A negative slope means the asset moves opposite the market component on average under the fitted model. |
| C | False | Negative beta does not *guarantee* a positive realized return when the market declines — alpha, residuals, and estimation error can override it. |
| D | False | Negative market exposure *can* offset a portfolio's positive market exposure — it provides hedging value, so "cannot provide hedging value" reverses the truth. |
| E | False | Volatility is nonnegative; beta is negative because *covariance* with the market is negative, not because volatility is "negative." |

**Reference:** Negative beta / negative covariance, hedging — Investopedia "Negative Beta"; Bodie-Kane-Marcus (covariance and beta).

### [QF-D7G2Q3] Beta from covariance and variance
**Scenario:** Estimated covariance of a stock with the market is 0.018; market-return variance is 0.012 over the same horizon.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | `β = Cov/Var = 0.018 / 0.012 = 1.5`. |
| B | True | Beta is defined as asset-market covariance divided by market variance — the single-factor regression slope. |
| C | False | Negation trap. Zero covariance ⇒ zero numerator ⇒ **β = 0**, so "would not be zero" reverses the correct conclusion. |
| D | False | A zero beta means no market sensitivity but does not eliminate idiosyncratic (asset-specific) risk. |
| E | True | Beta is an empirical estimate and can vary across frequencies, samples, and market regimes. |

**Reference:** `β = Cov(i,m)/Var(m)` — Sharpe CAPM; Investopedia "How to Calculate Beta."

### [QF-D7G3Q1] Jensen's alpha via CAPM (fund 14%, market 10%, r_f 2%, β 1.2)
**Scenario:** Over one year a fund returns 14%, market 10%, risk-free 2%, fund beta 1.2. Use CAPM expected return = `r_f + β·(r_market − r_f)`.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Negation trap. Market excess return = `10% − 2% = 8%`, so "not 8%" reverses the correct conclusion. |
| B | True | CAPM-implied return = `2% + 1.2 × 8% = 11.6%`. |
| C | True | Realized alpha = `14% − 11.6% = 2.4%` (return above CAPM expectation). |
| D | False | With beta 1.2 the fund carries more market risk than the index; comparing 14% to 10% alone does **not** risk-adjust. |
| E | False | One year of positive alpha may be luck, residual risk, or estimation error — it does not guarantee persistent skill. |

**Reference:** CAPM / SML expected return and Jensen's alpha — Sharpe CAPM; Investopedia "Capital Asset Pricing Model (CAPM)" and "Jensen's Measure."

### [QF-D7G3Q2] Alpha significance vs. economic significance (net of cost)
**Scenario:** A strategy's estimated annual alpha is 1.0% with standard error 0.8%; implementation costs 1.3%/year. A researcher says the positive alpha justifies deployment.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Reported gross alpha estimate is +1.0% (before costs). |
| B | True | Estimate-to-standard-error ratio = `1.0 / 0.8 = 1.25` — only 1.25 SEs above zero. |
| C | False | A positive point estimate alone does not establish conventional two-sided statistical significance (1.25 SEs is short of ~1.96). |
| D | True | Expected net alpha = `1.0% − 1.3% = −0.3%` after costs. |
| E | False | Statistical and economic significance are *distinct*: an effect can be detectable yet uneconomic after costs, or large yet imprecise. "Not distinct" reverses this. |

**Reference:** Statistical vs. economic significance, net-of-cost alpha — Grinold & Kahn (information ratio, t-stat of alpha); CFA curriculum (hypothesis testing / performance evaluation).

### [QF-D7G3Q3] High returns from high beta, not alpha (bull market)
**Scenario:** In a bull market r_f = 2%, market returns 12%, and a fund with beta 1.5 returns 17%. Use CAPM.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Realized market risk premium = `12% − 2% = 10%`. |
| B | False | Negation trap. CAPM-implied return = `2% + 1.5 × 10% = 17%`, which equals the realized 17%, so "not 17%" reverses the correct conclusion. |
| C | False | Negation trap. Realized equals CAPM-implied, so alpha *is* ≈ 0; "not approximately zero" reverses the correct conclusion. |
| D | False | The 5-point outperformance is fully explained by beta 1.5 under CAPM — it is not necessarily manager alpha. |
| E | True | High raw returns can come from high systematic exposure amplifying a bull market, without any abnormal (alpha) performance. |

**Reference:** Beta-driven returns vs. alpha, SML — Sharpe CAPM; Investopedia "Alpha" and "CAPM."

### [QF-D7G4Q1] Beta from correlation and volatility ratio (low-vol stock)
**Scenario:** A low-volatility stock has 0.90 correlation with the market; stock vol 8%, market vol 16%. Use `β = ρ · σ_stock / σ_market`.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | `β = 0.90 × 8% / 16% = 0.45`. |
| B | True | High correlation can pair with beta below one when the stock is less volatile than the market. |
| C | True | Correlation is standardized co-movement; beta additionally reflects the asset-to-market volatility ratio. |
| D | False | Beta-based market component = `0.45 × 2% = 0.9%`, not 1.8% — the choice ignores the low beta. |
| E | False | High positive correlation does not imply beta above one; a low volatility ratio can keep beta below one. |

**Reference:** `β = ρ·(σ_i/σ_m)`, correlation vs. beta — CFA curriculum (correlation, beta); Investopedia "Beta" and "Correlation."

### [QF-D7G4Q2] Low correlation, high volatility ⇒ low beta
**Scenario:** A speculative asset has 30% volatility, the market 15%, correlation 0.20.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | `β = 0.20 × 30% / 15% = 0.40`. |
| B | False | High total volatility does not force beta above one — low correlation drives beta down to 0.40 here. |
| C | True | Low correlation means market co-movement explains only a limited share of the asset's movement; most is idiosyncratic. |
| D | False | Correlation and beta are not interchangeable: correlation is standardized co-movement, beta is the magnitude of market sensitivity. |
| E | False | An investor concerned with *total* risk must look beyond beta — substantial idiosyncratic volatility remains even when beta is modest. |

**Reference:** Idiosyncratic vs. systematic volatility, correlation ≠ beta — Bodie-Kane-Marcus (total vs. systematic risk); Investopedia "Unsystematic Risk."

### [QF-D7G4Q3] Negative beta as hedge diagnostic; leverage scales beta contribution
**Scenario:** An asset has 12% volatility, market 8%, correlation −0.50; a manager compares correlation and beta as hedge diagnostics.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Negation trap. `β = −0.50 × 12% / 8% = −0.75`, so "not −0.75" reverses the correct conclusion. |
| B | True | Negative correlation means the asset moves opposite the market on average over the sample. |
| C | True | Beta scales correlation by the asset-to-market volatility ratio, so its magnitude depends partly on relative volatility. |
| D | False | Ignoring financing, a 2× leveraged position roughly *doubles* the beta contribution relative to equity — it is not the same as an unleveraged position of equal equity. |
| E | True | Both correlation and beta are historical estimates and can change in a future crisis (regime dependence). |

**Reference:** Negative beta, leverage and beta contribution, regime instability — Grinold & Kahn (beta/exposure); Investopedia "Beta" and "Leverage."

### [QF-D7G5Q1] Portfolio beta as weighted average (long-only)
**Scenario:** A fully invested long-only portfolio holds 60% Stock A (β 1.4) and 40% Stock B (β 0.5).
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Stock A's contribution = `0.60 × 1.4 = 0.84`. |
| B | True | Stock B's contribution = `0.40 × 0.5 = 0.20`. |
| C | False | Negation trap. Portfolio beta = `0.84 + 0.20 = 1.04`, so "not 1.04" reverses the correct conclusion. |
| D | False | Negation trap. A positive-weighted average must lie within the component-beta range [0.5, 1.4]; "must not lie between" reverses this. |
| E | False | Beta is market sensitivity, not a guaranteed return premium — a 1.04 beta does not mean "4% more than the market each year." |

**Reference:** Portfolio beta = weighted average of component betas — Bodie-Kane-Marcus (portfolio beta); Investopedia "Portfolio Beta."

### [QF-D7G5Q2] Leveraged portfolio beta and gross exposure
**Scenario:** Weights (vs. equity): +120% in a basket (β 1.1), −40% in another (β 0.8), +20% cash (β 0).
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Long-basket contribution = `1.20 × 1.1 = 1.32`. |
| B | True | Short-basket contribution = `−0.40 × 0.8 = −0.32`. |
| C | True | Cash adds 0, so portfolio beta = `1.32 − 0.32 = 1.00`. |
| D | False | Negation trap. Gross risky exposure = `120% + 40% = 160%` of equity, so "not 160%" reverses the correct conclusion. |
| E | False | Signed weights (incl. cash) summing to 100% does not mean unleveraged — the 160% gross risky exposure reveals leverage. |

**Reference:** Gross vs. net exposure, leverage, beta aggregation — Grinold & Kahn (portfolio exposures); Investopedia "Gross Exposure."

### [QF-D7G5Q3] Beta-weighted dollar exposure with long and short legs
**Scenario:** A fund with $50M equity is long $80M (β 1.25), short $30M low-beta (β 0.5), short $20M market ETF (β 1.0).
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Long beta-weighted exposure = `$80M × 1.25 = $100M`. |
| B | True | Shorts contribute `−($30M × 0.5) − ($20M × 1.0) = −$15M − $20M = −$35M`. |
| C | False | Negation trap. Net beta-weighted exposure = `$100M − $35M = $65M`, so "not +$65M" reverses the correct conclusion. |
| D | False | Negation trap. Portfolio beta vs. equity = `$65M / $50M = 1.3`, so "not 1.3" reverses the correct conclusion. |
| E | False | Beta neutrality requires beta-weighted exposures to cancel; matching short *dollars* ($50M) leaves +$65M net beta exposure, so it is not beta neutral. |

**Reference:** Beta-weighted (beta-dollar) exposure, portfolio beta relative to equity — Grinold & Kahn; Bodie-Kane-Marcus (net beta exposure).

### [QF-D7G6Q1] Dollar neutral ≠ beta (market) neutral
**Scenario:** Long $50M Stock A (β 1.4), short $50M market ETF (β 1.0). The PM calls it "market neutral" because dollar amounts match.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Gross long and short dollar amounts are equal ($50M each) → dollar neutral. |
| B | False | Beta-weighted exposures do not cancel: long `50 × 1.4 = 70` beta-dollars vs. short `50 × 1.0 = 50` → net +20, so it is not beta neutral. |
| C | True | The long side adds 70 beta-dollars while the short removes only 50 — long market exposure exceeds what the short removes. |
| D | True | Equal dollar amounts do not imply equal market risk when betas differ — risk depends on sensitivities, not just dollars. |
| E | False | A *larger* ETF short would be needed to offset Stock A's higher beta; "would not need to be larger" reverses this. |

**Reference:** Dollar neutrality vs. beta/market neutrality — Investopedia "Market-Neutral Strategy"; Grinold & Kahn (beta-neutral construction).

### [QF-D7G6Q2] Beta-neutral hedge requires unequal dollars
**Scenario:** Long $30M of a stock (β 1.5); hedge with a different stock (β 0.75). Ignore alpha, residuals, costs.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Long beta-weighted exposure = `$30M × 1.5 = $45M`. |
| B | False | A $30M short at β 0.75 removes only `$30M × 0.75 = $22.5M` of beta exposure — not enough for beta neutrality. |
| C | False | Negation trap. A $60M short removes `$60M × 0.75 = $45M`, exactly offsetting the long, so "would not make the trade beta neutral" reverses the correct conclusion. |
| D | True | With the $60M short the beta exposures cancel, but the book is net short $30M in dollars → beta neutral yet not dollar neutral. |
| E | False | Different security betas require *unequal* dollar amounts for equal-and-opposite market exposure; beta neutrality does not require equal dollars. |

**Reference:** Beta-adjusted hedge ratio (`hedge$ = long$ · β_long/β_hedge`) — Bodie-Kane-Marcus (hedging with beta); Investopedia "Beta Hedging."

### [QF-D7G6Q3] Same dollars, different betas ⇒ net negative beta
**Scenario:** Long $40M defensive basket (β 0.6), short $40M cyclical basket (β 1.2).
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Negation trap. Both legs are $40M, so the book *is* dollar neutral; "not dollar neutral" reverses the correct conclusion. |
| B | True | Long contribution = `$40M × 0.6 = +$24M` beta-weighted exposure. |
| C | True | Short contribution = `−$40M × 1.2 = −$48M` beta-weighted exposure. |
| D | True | Net beta-weighted exposure = `$24M − $48M = −$24M` (net negative, i.e., net short beta). |
| E | False | Raising the long to $80M would offset beta (`80×0.6 = 48 = 40×1.2`), but $80M long vs. $40M short breaks dollar neutrality — so it cannot be *both*. |

**Reference:** Dollar vs. beta neutrality tradeoff — Investopedia "Market-Neutral Strategy"; Grinold & Kahn (neutral construction).

### [QF-D7G7Q1] Index hedge removes systematic risk, retains idiosyncratic
**Scenario:** A fund owns $10M of a stock (β 1.3) and shorts a broad market ETF (β 1.0) to hedge market exposure.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Stock contributes `$10M × 1.3 = $13M` beta-weighted exposure; a $13M short in a β-1 ETF offsets it. |
| B | False | The hedge targets modeled *market* exposure only — it does not eliminate idiosyncratic, model, liquidity, or other risks, so it cannot remove "all possible losses." |
| C | True | An index hedge does not offset issuer-specific news, so company-specific developments can still move the hedged trade. |
| D | False | A well-matched market hedge is *designed* to remove systematic return while *preserving* asset-specific (alpha) return before costs; "cannot retain that return" reverses the purpose. |
| E | False | If true future beta differs from the estimate, the hedge ratio is imperfect and leaves unintended market exposure — beta estimation error *can* leave exposure. |

**Reference:** Index hedge, systematic vs. idiosyncratic risk, hedge-ratio (beta) error — Bodie-Kane-Marcus (hedging market risk); Investopedia "Hedge" and "Basis Risk."

### [QF-D7G7Q2] Pair trade: dollar neutral vs. beta neutral vs. relative-value risk
**Scenario:** A pair trade is long $5M Stock A (β 1.4) and short Stock B (β 0.7); same industry but the historical relationship can change.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Long beta-weighted exposure = `$5M × 1.4 = $7M`. |
| B | False | Negation trap. Equal $5M long and $5M short *are* dollar neutral, so "would not make the trade dollar neutral" reverses the correct conclusion. |
| C | False | A $5M short at β 0.7 removes only `$5M × 0.7 = $3.5M` of beta exposure — well short of the $7M long, so it is not beta neutral. |
| D | True | A $10M short at β 0.7 removes `$10M × 0.7 = $7M`, offsetting the long side's estimated market beta. |
| E | True | Even a beta-neutral pair trade can lose on relative-value, company-specific, or relationship-breakdown risk. |

**Reference:** Pair trading, dollar vs. beta neutrality, relative-value risk — Investopedia "Pairs Trade"; Grinold & Kahn (residual/relative-value risk).

### [QF-D7G7Q3] Index-future hedge: offsetting market components, retained alpha, residual risk
**Scenario:** A $20M portfolio (β 0.8) shorts $16M of a β-1 index-future equivalent. The market rises 6% and the portfolio earns +2% asset-specific return. Ignore financing/costs initially.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Negation trap. Modeled market-related gain = `$20M × 0.8 × 6% = $960,000`, so "not $960,000" reverses the correct conclusion. |
| B | False | Negation trap. Short index exposure loses `$16M × 6% = $960,000`, so "not $960,000" reverses the correct conclusion — the hedge loss exactly offsets the market gain. |
| C | True | After the two market components cancel, the 2% asset-specific return on $20M = `$400,000` remains before costs. |
| D | False | Beta and hedge relationships change and returns carry basis/residual risk — a hedge cannot guarantee realized beta "exactly zero in every future period." |
| E | True | Real hedges are imperfect: trading costs, financing, imperfect index matching, and changing beta all reduce effectiveness. |

**Reference:** Beta hedge with index futures, basis risk, return drag — Bodie-Kane-Marcus (hedging with index futures); Investopedia "Basis Risk" and "Beta Hedging."

## References (domain-level)

1. **Sharpe — Capital Asset Pricing Model (CAPM):** the Security Market Line, `E(r) = r_f + β·(r_market − r_f)`, and `β = Cov(i,m)/Var(m)` — foundation for expected return, alpha as deviation from the SML, and beta as systematic-risk sensitivity.
2. **Bodie, Kane & Marcus — *Investments*:** the index/market model and Security Characteristic Line, return decomposition into systematic + firm-specific components, portfolio beta, and hedging market risk with index instruments (beta hedge ratio, basis risk).
3. **Grinold & Kahn — *Active Portfolio Management*:** residual (idiosyncratic) return and risk, alpha vs. beta, the information ratio / t-statistic of alpha, and beta-neutral / dollar-neutral portfolio construction and exposures.
4. **CFA Institute curriculum (Portfolio Management / Quantitative Methods):** CAPM and the SML, correlation vs. beta, statistical vs. economic significance and hypothesis testing of alpha, and performance evaluation.
5. **Investopedia:** "Capital Asset Pricing Model (CAPM)" and "Security Market Line," "Beta" / "Negative Beta," "Jensen's Measure (Alpha)," "Market-Neutral Strategy," "Pairs Trade," "Beta Hedging," and "Basis Risk."
