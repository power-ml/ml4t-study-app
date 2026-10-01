# QF Domain 5 — Advanced Portfolio Construction

## Domain cheat-sheet

- **Translating forecasts (alphas) into positions.** Portfolio construction is the step that converts return *views* into *target weights/dollars*. The mapping is a modeling choice, not a given:
  - **Linear sizing** maps a signal to a raw target proportional to the signal, so doubling a signal doubles the raw position and relative magnitudes are preserved (a +2% forecast gets twice the magnitude of a +1% forecast). Positive forecasts → long, negative → short, a **zero forecast → a zero target** (not the largest). A forecast is an *estimate*: the sign/size of a view never guarantees the sign/size of the realized return.
  - **Sign-based (rank/bucket) sizing** uses only the sign (or rank) of a signal, assigning every positive signal the same long target and every negative the same short target. It *discards magnitude*, which makes it **more robust to poorly calibrated / miscalibrated scores** (one extreme numerical score cannot command a proportionally extreme position) but less expressive when magnitudes are informative.
  - **Risk-adjusted / conviction sizing.** Grinold & Kahn's core intuition: position size should scale with *expected return per unit of risk*, not raw return. A mean–variance-style rule sizes by **expected excess return ÷ forecast variance** (equivalently ∝ IC·volatility·score), so two assets with equal expected return but different volatility get *different* sizes — the lower-variance asset gets the larger raw weight. **Confidence scaling** multiplies a raw position by a reliability weight (0.8 vs 0.4 → a 2:1 size ratio); it changes *size*, not the *sign* of the point forecast, and poorly calibrated confidence is itself a source of model/judgment risk. A conviction/confidence score is **not** a calibrated probability of a positive realized return.
  - After raw sizing, portfolios are usually **normalized to a target gross exposure**; a common positive scaling factor changes magnitudes while preserving directions. Equal gross exposure does **not** imply equal risk — risk still depends on volatilities, correlations, and the distribution of weights.
- **Active vs. benchmark-relative weights.** **Active weight = portfolio weight − benchmark weight.** A long-only fund expresses a *negative* view by **underweighting** (holding less than the benchmark weight, even zero) without shorting; a zero holding against a 4% benchmark weight is a −4% active weight. **Active share** measures the fraction of the portfolio that deviates from the benchmark; it is distinct from expected return (equal expected returns do not imply equal active share) and does **not** by itself guarantee out- or under-performance. **Net exposure** = long − short; **gross exposure** = |long| + |short|. A +$120M / −$120M book has **zero net, $240M gross**; zero net exposure does **not** mean zero market/factor/idiosyncratic risk, and comparing strategies by net alone hides gross and risk composition.
- **Mean–variance optimization (Markowitz) and its instability.** MVO chooses weights to maximize `wᵀμ − (λ/2)·wᵀΣw` (or min variance for a target return), tracing the **efficient frontier** (Markowitz, *Portfolio Selection*, 1952; Balch ML4T 02-10). It explicitly trades expected reward against risk and uses the **covariance structure** — so equal expected returns do **not** imply equal weights, and portfolio variance is generally **not** the weighted average of individual volatilities (cross-asset covariance terms matter). Its weakness: MVO is an **error-maximizer** — tiny changes in noisy expected-return inputs can produce large, extreme, or reversed weights (a few-bp revision moving a weight from 2% to 28%), and it over-trusts the precise *ordering* of estimates. The optimizer *transforms* inputs; it does **not** validate their accuracy, so a large recommended weight is not evidence the forecast is correct.
- **Risk models & covariance estimation.** Diversification comes from **imperfect co-movement**: an equal-weight pair of equal-volatility assets is lower-risk when their correlation is lower (the −0.20 pair beats the +0.90 pair). **Marginal risk contribution** depends on a position's weight *and* its covariance with the rest of the portfolio, so equal dollar weights do **not** create equal risk contributions — a high-volatility, highly-correlated holding can contribute far more than its capital weight, and trimming it can cut portfolio risk without changing the number of holdings. Different *instruments* (momentum vs. carry sleeves) can still share common market/sector/style exposures, so portfolio-level aggregation reveals overlaps that per-sleeve reports hide; sample covariance is itself an estimate that drifts, motivating rebalancing of risk budgets when volatilities/correlations change.
- **Shrinkage.** Sample estimates (especially expected returns, and sample covariance with many assets) are noisy. **Shrinkage** pulls estimates toward a structured target — expected returns toward a common/grand mean, the covariance matrix toward a structured target (Ledoit & Wolf shrinkage estimator) — reducing cross-sectional dispersion and extreme allocations driven by small estimated differences, at the cost of some in-sample fit.
- **Robust optimization.** Robust methods explicitly account for input uncertainty rather than treating point estimates as truth: shrinkage, weight penalties/regularization, position caps, resampling/bootstrap sensitivity analysis, and scaling back positions when the estimated return spread is unstable. They deliberately **trade some in-sample optimality for less fragile, more stable out-of-sample weights**. Robustness ≠ equal weighting; many unequal-weight portfolios are robust. Out-of-sample / rolling evaluation is the relevant test of whether optimization benefits survive estimation error.
- **Constraints & implementability.** Real mandates impose **gross/net leverage limits, single-position caps, sector/benchmark-relative bands, long-only, liquidity/participation limits, and turnover limits**. Constraints (a) make the unconstrained optimum infeasible, (b) force displaced capital toward other holdings or cash, (c) reduce how fully forecasts are expressed, and (d) can make the final portfolio differ materially from a naïve ranking of forecasts — while **reducing damage from estimation-error-driven extreme weights**. A gross limit is about **sum of absolute** positions, so a 100% net figure says nothing about gross-limit compliance or any single position cap. Constraints that lower a backtest return are not automatically removable: they often reflect genuine risk limits, capacity, mandates, or legal requirements.
- **Turnover / transaction-cost-aware optimization.** A cost-aware objective nets expected improvement against implementation cost (spread, market impact, commissions, slippage, taxes), so **current holdings matter** (cost depends on the trade from current to target, not the target alone). It may **decline to trade** when the incremental benefit is below cost (keep 4% rather than chase a 4.3% frictionless target), use **turnover penalties / no-trade bands / signal thresholds** to suppress churn from small or noisy forecast changes, and recognize that a frictionless-optimal portfolio can be economically inferior after costs. A turnover penalty **lowers** the objective value of trade-intensive changes (it does not make trading more attractive). The goal is maximum **net** value — not zero turnover; some high-value trades remain worthwhile. Splitting one oversized order into intraday child orders does **not** change its combined share of the day's volume, so a participation-rate breach is not fixed by slicing alone; a liquidity-aware optimizer instead builds more slowly or targets a smaller size, and turnover must be checked at the **portfolio** level. Ignoring implementability makes simulated results more optimistic than live.

## Common traps

- **Inverted-polarity questions (10 of 21 here).** When the body says "each item asserts that its quoted statement is incorrect," the Answer-Key verdict is flipped relative to the quoted claim's truth: **True = the quoted statement is wrong; False = the quoted statement is accurate.** Read the polarity line *first*. Inverted here: **G1Q3, G2Q1, G2Q3, G3Q2, G3Q3, G4Q2, G4Q3, G5Q1, G6Q2, G7Q3.** The other 11 are Normal (True = accurate).
- **Zero forecast ⇒ largest / special position.** Under linear sizing a zero signal maps to a *zero* target, not the largest; magnitude scales with |forecast|.
- **Forecast guarantees the trade.** A view is an uncertain estimate; neither its sign nor magnitude guarantees a positive realized return.
- **Long-only must short to express a negative view.** False — a long-only fund expresses a negative view by *underweighting* (holding less than, or zero of, the benchmark weight). An underweight does **not** require a negative dollar holding.
- **Lower portfolio weight ⇒ model forecasts a negative return.** False — a lower weight can simply reflect a less attractive relative forecast or benchmark allocation.
- **Equal expected returns ⇒ equal weights.** False — risk, covariance, confidence, costs, and constraints all legitimately produce unequal weights.
- **Equal gross exposure (or equal individual volatilities) ⇒ equal risk.** False — portfolio risk depends on covariances and the weight distribution, not gross exposure or standalone volatilities alone.
- **Zero net exposure ⇒ zero risk / compliant with gross limit / caps satisfied.** All false — gross exposure sums absolute positions; a market-neutral book can carry large factor/basis/idiosyncratic risk and still breach a gross or per-position cap.
- **Active share ⇒ performance.** Higher active share can lead to out- *or* under-performance; it is a deviation measure, not a return guarantee, and is distinct from expected return.
- **Equal dollar weights ⇒ equal risk contributions.** False — marginal risk contribution depends on weight *and* covariance with the portfolio; a volatile, correlated name can dominate risk.
- **Portfolio volatility = weighted average of asset volatilities.** False — covariance/correlation terms mean it is generally not a simple weighted average.
- **Different securities ⇒ independent strategy risks.** False — different instruments can share market/sector/style/macro exposures.
- **Confidence scaling flips the sign / is a calibrated probability.** False — it rescales *size*; an "80% confidence" is not a guarantee of positive realized returns 80% of the time.
- **A large optimized weight proves the forecast is right.** False — the optimizer transforms inputs; instability under small perturbations signals over-reliance on noisy estimates, not forecast validity.
- **Leverage makes estimation error irrelevant.** False — leverage *magnifies* the consequences of forecast error.
- **Robust ⇒ equal weights.** False — many unequal-weight portfolios are robust; shrinkage/penalties temper extremes without forcing equal weighting.
- **Any nonzero gap to the frictionless target should trigger a trade / turnover penalties make trades more attractive / minimize turnover at any price.** All false — compare expected improvement to cost; penalties *lower* the value of churny changes; the objective is net value, not zero (or minimal) trading.
- **Splitting a too-large order makes it compliant.** False — intraday slicing does not change the order's combined share of daily volume; reduce size or extend the horizon instead.
- **Constraints that hurt the backtest should be removed for live trading.** False — constraints often encode real mandates, risk/capacity limits, or legal requirements; ignoring implementability inflates simulated vs. live results.
- **Garbled source symbols.** The slice renders the ligatures **ﬁ** and **ﬂ** as single glyphs (e.g., "ﬁnal", "beneﬁt", "conﬁdence", "diversiﬁcation", "ﬂuctuations", "satisﬁed", "magniﬁes", "reﬂect"). These are OCR/ligature artifacts for "fi"/"fl", not content errors; they are normalized to plain text here. The recurring footer `NNN Rev:081020261230` is a page-footer stamp, not question content.

## Questions

### [QF2-D5G1Q1] Linear forecast-to-position mapping
**Scenario:** A researcher forecasts one-month excess returns of +2% (Stock A), −1% (Stock B), and 0% (Stock C). An unconstrained rule maps each forecast *linearly* to a target position — positive forecasts long, negative short.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | A positive forecast maps to a long position under the stated rule. |
| B | True | A negative forecast maps to a short position under the stated rule. |
| C | False | A zero forecast maps to a *zero* target under this linear rule, not the largest position; magnitude scales with the absolute forecast. |
| D | True | Linear sizing makes magnitudes proportional to absolute forecasts: 2% versus 1% is a 2:1 magnitude. |
| E | False | Forecasts are uncertain estimates; realized returns can differ in sign and magnitude from the forecast. |

**Reference:** Grinold & Kahn, *Active Portfolio Management*, 2nd ed. (forecasting and translating alphas into positions); Balch ML4T 02-10 (Portfolio Optimization & Efficient Frontier — sizing from views).

### [QF2-D5G1Q2] Long-only underweights and active weight
**Scenario:** A long-only fund converts cross-sectional scores to weights, requires nonnegative holdings, and overweights the best / underweights the worst. One low-scored stock has a 4% benchmark weight.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Holding less than the 4% benchmark weight is an underweight — a negative benchmark-relative view without shorting. |
| B | False | A long-only portfolio can express the negative view through an underweight; it need not short. |
| C | True | Active weight = portfolio − benchmark, so a 0% holding is 0% − 4% = −4% active. |
| D | True | Long-only, sector, leverage, and other constraints change how the same forecast becomes a position. |
| E | False | A lower weight can reflect a less attractive relative forecast or benchmark allocation, not a forecast of negative absolute return. |

**Reference:** Grinold & Kahn, *Active Portfolio Management*, 2nd ed. (benchmark-relative/active weights, long-only constraints); Balch ML4T 02-10.

### [QF2-D5G1Q3] Linear vs. sign-based mapping (information in magnitude)
**Scenario:** Rule L is linear (doubling a signal doubles the raw target); Rule S uses only the sign (every positive signal → same long target, every negative → same short target). Both are later normalized to the same gross exposure.
**Answer polarity:** **Inverted (True = the quoted statement is INCORRECT; False = the quoted statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | The quoted statement is correct: linear mapping assigns larger raw positions to larger-magnitude signals, preserving relative magnitude information. |
| B | True (incorrect) | The quoted statement is incorrect: Rule S assigns the *same* raw long target to all positive signals, so it cannot distinguish +0.1 from +2.0. |
| C | False (accurate) | The quoted statement is correct: a common positive scaling factor (gross normalization) changes magnitudes while preserving signs/directions. |
| D | False (accurate) | The quoted statement is correct: discarding magnitude makes a sign-based rule less sensitive to extreme, poorly calibrated numerical scores. |
| E | True (incorrect) | The quoted statement is incorrect: equal gross exposure does not guarantee equal risk — risk depends on volatilities, correlations, and the weight distribution. |

**Reference:** Grinold & Kahn, *Active Portfolio Management*, 2nd ed. (information content of signals, scaling to risk/exposure); Balch ML4T 02-10.

### [QF2-D5G2Q1] Risk-adjusted sizing (return ÷ variance)
**Scenario:** Two stocks have equal 6% expected excess return, but Stock H has 30% forecast volatility and Stock L has 15%. The manager sizes by expected excess return ÷ forecast variance, assuming independence.
**Answer polarity:** **Inverted (True = the quoted statement is INCORRECT; False = the quoted statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | The quoted statement is correct: expected return divided by variance is explicitly a risk-adjusted mapping — it uses both return and risk. |
| B | False (accurate) | The quoted statement is correct: with equal expected returns, the lower-variance asset (L) receives the larger raw weight. |
| C | True (incorrect) | The quoted statement is incorrect: risk, covariance, confidence, costs, and constraints can justify different weights despite equal expected returns. |
| D | False (accurate) | The quoted statement is correct: sizing can trade expected reward against risk rather than ranking by return alone. |
| E | True (incorrect) | The quoted statement is incorrect: the inputs remain estimates and can be wrong even inside a formal sizing rule. |

**Reference:** Grinold & Kahn, *Active Portfolio Management*, 2nd ed. (risk-adjusted position sizing, expected return per unit risk); Markowitz, *Portfolio Selection* (1952) (reward-vs-variance tradeoff); Balch ML4T 02-10.

### [QF2-D5G2Q2] Confidence scaling of equal point forecasts
**Scenario:** A model forecasts +4% for both Stocks A and B. The team assigns 80% confidence to A and 40% to B, then scales each raw position by its confidence, holding other inputs equal.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Equal forecasts scaled by 0.8 and 0.4 give a 2:1 position ratio. |
| B | True | Confidence scaling distinguishes forecasts with equal point estimates but different perceived reliability. |
| C | False | Confidence scaling changes position *size*, not necessarily the *sign* of the +4% point forecast. |
| D | True | Subjective, poorly calibrated confidence can cause systematic over- or undersizing — a real source of model/judgment risk. |
| E | False | A confidence score is not automatically a calibrated probability of a positive realized return. |

**Reference:** Grinold & Kahn, *Active Portfolio Management*, 2nd ed. (information coefficient, confidence/strength of signal in sizing); Balch ML4T 02-10.

### [QF2-D5G2Q3] Position caps vs. the unconstrained optimum
**Scenario:** An optimizer puts 35% in one stock because its estimated return is slightly highest. The mandate caps any position at 10%; the manager worries small forecast errors create excess concentration.
**Answer polarity:** **Inverted (True = the quoted statement is INCORRECT; False = the quoted statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | The quoted statement is correct: a 35% allocation violates a 10% maximum, so the unconstrained solution is infeasible. |
| B | False (accurate) | The quoted statement is correct: the displaced capital must be reassigned to other holdings or cash consistently with the remaining rules. |
| C | False (accurate) | The quoted statement is correct: a cap limits exposure when a noisy input would otherwise dominate the portfolio. |
| D | True (incorrect) | The quoted statement is incorrect: constraining the unconstrained optimum generally *reduces* its model-implied expected return. |
| E | False (accurate) | The quoted statement is correct: a concentration limit sacrifices some forecast utilization to control concentration/estimation-error risk. |

**Reference:** Grinold & Kahn, *Active Portfolio Management*, 2nd ed. (constraints and their cost to the optimal solution); Balch ML4T 02-10.

### [QF2-D5G3Q1] Computing active weights
**Scenario:** Benchmark: A 5%, B 3%, C 0%. A long-only active portfolio holds A 8%, B 1%, C 2%. Remaining holdings not shown.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Active weight = 8% − 5% = +3%. |
| B | True | 1% is two percentage points below the 3% benchmark weight → −2% active, even though the holding is positive. |
| C | True | A 2% holding against a 0% benchmark weight is a +2% active weight. |
| D | False | A long-only fund can underweight a constituent while keeping a positive holding — an underweight needs no negative position. |
| E | True | Active weight is defined as portfolio weight minus benchmark weight for each asset. |

**Reference:** Grinold & Kahn, *Active Portfolio Management*, 2nd ed. (active weights, benchmark-relative allocation); Balch ML4T 02-10.

### [QF2-D5G3Q2] Active share vs. expected return and tracking error
**Scenario:** Portfolio X holds every benchmark stock near its benchmark weight; Portfolio Y is long-only, fully invested, excludes many benchmark stocks, and concentrates in a subset. Both have the same model expected total return.
**Answer polarity:** **Inverted (True = the quoted statement is INCORRECT; False = the quoted statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | The quoted statement is correct: larger deviations from benchmark weights generally produce higher active share, so Y > X. |
| B | True (incorrect) | The quoted statement is incorrect: equal expected total return and active share measure different properties and need not coincide. |
| C | False (accurate) | The quoted statement is correct: a zero holding creates an underweight equal to the negative of the positive benchmark weight — no shorting needed. |
| D | True (incorrect) | The quoted statement is incorrect: greater active share can lead to either out- or under-performance; it guarantees neither. |
| E | False (accurate) | The quoted statement is correct: tracking error depends on active weights and the covariance structure, not active share alone. |

**Reference:** Grinold & Kahn, *Active Portfolio Management*, 2nd ed. (active risk/tracking error, active weights vs. return); Balch ML4T 02-10.

### [QF2-D5G3Q3] Net vs. gross exposure in a long-short book
**Scenario:** A benchmark-neutral long-short strategy holds +$120M long and −$120M short active positions. A separate long-only fund expresses negative views mainly through underweights. The teams compare capital and risk use.
**Answer polarity:** **Inverted (True = the quoted statement is INCORRECT; False = the quoted statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | The quoted statement is correct: +$120M and −$120M sum to zero net exposure. |
| B | False (accurate) | The quoted statement is correct: gross exposure adds absolute long and short: $120M + $120M = $240M. |
| C | True (incorrect) | The quoted statement is incorrect: zero net exposure can still carry substantial basis, factor, covariance, and security-specific risk. |
| D | False (accurate) | The quoted statement is correct: the long-only fund expresses a negative view via an underweight, without a negative dollar holding. |
| E | False (accurate) | The quoted statement is correct: comparing by net exposure alone can conceal differences in gross exposure and risk. |

**Reference:** Grinold & Kahn, *Active Portfolio Management*, 2nd ed. (long-short construction, gross/net exposure, risk decomposition); Balch ML4T 02-10.

### [QF2-D5G4Q1] Correlation and equal-weight portfolio risk
**Scenario:** Two assets each have 20% annualized volatility. Corr(A,B) = +0.90, Corr(A,C) = −0.20. The optimizer considers equal-weight two-asset portfolios with equal expected returns.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Lower correlation reduces the covariance term, so the A-C equal-weight portfolio has lower volatility than A-B. |
| B | False | Portfolio volatility depends on both individual variances and cross-asset covariance, not individual volatilities alone. |
| C | True | Diversification arises from imperfect co-movement — covariance determines how much combining positions reduces risk. |
| D | True | B closely tracks A (+0.90), so adding B diversifies less than adding the more independent C (−0.20). |
| E | False | An estimated negative correlation is uncertain and does not dictate perfect offsetting in every future period. |

**Reference:** Markowitz, *Portfolio Selection* (1952) (variance of a weighted sum, diversification via covariance); Grinold & Kahn, *Active Portfolio Management*, 2nd ed. (risk models); Balch ML4T 02-10.

### [QF2-D5G4Q2] Equal dollar weights ≠ equal risk contributions
**Scenario:** A four-stock portfolio has equal dollar weights. Three stocks are stable and weakly correlated; the fourth is highly volatile and strongly correlated with one of the others. The manager claims equal capital weights mean equal risk contributions.
**Answer polarity:** **Inverted (True = the quoted statement is INCORRECT; False = the quoted statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | The quoted statement is correct: equal dollar weights need not create equal risk contributions, which also depend on volatility and covariance. |
| B | False (accurate) | The quoted statement is correct: the volatile, correlated stock can contribute more risk than its 25% capital weight suggests. |
| C | False (accurate) | The quoted statement is correct: marginal risk contribution depends on a position's weight and its covariance with the portfolio. |
| D | False (accurate) | The quoted statement is correct: trimming the high-volatility holding can lower portfolio risk even with the holding count unchanged. |
| E | True (incorrect) | The quoted statement is incorrect: covariance terms mean portfolio volatility is generally *not* a simple weighted average of asset volatilities. |

**Reference:** Grinold & Kahn, *Active Portfolio Management*, 2nd ed. (marginal contribution to risk, risk decomposition); Markowitz (1952); Balch ML4T 02-10.

### [QF2-D5G4Q3] Hidden common exposures across sleeves
**Scenario:** A multi-strategy fund gives equal risk budgets to momentum, value, and carry sleeves. Momentum and carry hold different securities but have become strongly positively correlated; value stays weakly correlated. The fund evaluates the combined portfolio.
**Answer polarity:** **Inverted (True = the quoted statement is INCORRECT; False = the quoted statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | The quoted statement is correct: different securities do not guarantee independent risks — sleeves can share market/sector/style/macro exposures. |
| B | False (accurate) | The quoted statement is correct: stronger momentum-carry correlation raises their combined covariance and reduces diversification benefit. |
| C | True (incorrect) | The quoted statement is incorrect: equal standalone volatility does not produce equal risk contributions — weights and correlation with the rest matter. |
| D | False (accurate) | The quoted statement is correct: portfolio-level aggregation reveals common exposures not visible in separate sleeve reports. |
| E | False (accurate) | The quoted statement is correct: rebalancing risk budgets is reasonable when correlations or volatilities change materially. |

**Reference:** Grinold & Kahn, *Active Portfolio Management*, 2nd ed. (factor/common-exposure risk, aggregation, risk budgeting); Balch ML4T 02-10.

### [QF2-D5G5Q1] Gross-exposure and position-cap constraints
**Scenario:** An unconstrained optimizer proposes 180% long / 80% short (260% gross, 100% net). The mandate caps gross exposure at 150% and prohibits any single position above 8% of capital.
**Answer polarity:** **Inverted (True = the quoted statement is INCORRECT; False = the quoted statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | The quoted statement is correct: 260% gross exceeds the 150% limit, so the gross-exposure constraint is violated. |
| B | True (incorrect) | The quoted statement is incorrect: 100% net does not establish gross-limit compliance — gross sums absolute positions and can be high even when longs and shorts net substantially. |
| C | False (accurate) | The quoted statement is correct: the optimizer must at least cut gross exposure, and individual weights must also be checked. |
| D | False (accurate) | The quoted statement is correct: a leverage constraint can require scaling or dropping forecast-driven trades, limiting forecast expression. |
| E | True (incorrect) | The quoted statement is incorrect: aggregate 100% net exposure gives no assurance about the size of any single 8%-capped holding. |

**Reference:** Grinold & Kahn, *Active Portfolio Management*, 2nd ed. (leverage/position constraints and implementation); Balch ML4T 02-10.

### [QF2-D5G5Q2] Sector and liquidity constraints
**Scenario:** A model heavily favors technology and disfavors utilities; its unconstrained portfolio puts 55% in tech, but the mandate limits any sector to ±10 percentage points from benchmark. Several favored tech stocks are hard to trade at size.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The sector band keeps technology within its permitted benchmark-relative range, preventing every favored tech position at its unconstrained size. |
| B | True | A theoretically attractive position may be costly or impossible to execute at scale — liquidity constrains it. |
| C | False | Independently generated forecasts can still aggregate into a concentrated common sector exposure, so sector limits are relevant. |
| D | True | Feasibility rules change which signals can be expressed and by how much, so the final portfolio can differ from a forecast ranking. |
| E | False | Constraints may encode real mandates, risk limits, capacity, or legal requirements; a lower backtest return is not reason enough to remove them. |

**Reference:** Grinold & Kahn, *Active Portfolio Management*, 2nd ed. (sector/factor constraints, transaction costs and capacity); Balch ML4T 02-10.

### [QF2-D5G5Q3] Participation and turnover limits
**Scenario:** A small-cap strategy wants to buy 12% of a stock's average daily volume (ADV) daily for two weeks. Policy limits participation to 5% of ADV and total portfolio turnover to 20% per month. The optimizer ignored both.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | 12% of ADV exceeds the stated 5% participation maximum. |
| B | False | Splitting one order into several intraday orders does not change their combined share of the day's volume. |
| C | True | A liquidity-aware optimizer can build the position more slowly or target a smaller size to stay within limits. |
| D | True | Turnover is an aggregate of all buys and sells, so it must be checked across the portfolio, not just this security. |
| E | True | Ignoring implementability lets a backtest assume trades and prices unachievable in practice, making simulated results optimistic. |

**Reference:** Grinold & Kahn, *Active Portfolio Management*, 2nd ed. (market impact, turnover, implementation shortfall); Balch ML4T 02-10.

### [QF2-D5G6Q1] Sensitivity to noisy expected-return inputs
**Scenario:** An optimizer uses expected returns differing by a few basis points. A small revision to one stock's forecast moves its weight from 2% to 28% with risk nearly unchanged. The team suspects over-sensitivity to noisy inputs.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Large weight changes from tiny input changes are evidence of sensitivity to uncertain estimates and merit investigation. |
| B | True | Expected-return estimates are often noisy, so their precise ordering should not be treated as certain. |
| C | True | Shrinking forecasts toward a common mean reduces cross-sectional dispersion and the extreme allocations driven by small differences. |
| D | False | The optimizer transforms inputs; a 28% recommendation does not prove the revised forecast is correct. |
| E | True | Position caps or regularization improve stability at the cost of departing from the unconstrained point-estimate optimum. |

**Reference:** Markowitz (1952) (mean-variance sensitivity); Ledoit & Wolf (shrinkage of noisy estimates); Grinold & Kahn, *Active Portfolio Management*, 2nd ed. (robustness/regularization); Balch ML4T 02-10.

### [QF2-D5G6Q2] Leverage, estimation error, and robustness
**Scenario:** A researcher estimates returns from a short sample. The unconstrained optimizer recommends highly leveraged long A / short B because their estimated returns differ a lot. Bootstrap samples often reverse the ordering.
**Answer polarity:** **Inverted (True = the quoted statement is INCORRECT; False = the quoted statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | The quoted statement is correct: frequent ordering reversals in resamples show the relative-return estimate is uncertain. |
| B | False (accurate) | The quoted statement is correct: extreme opposing weights amplify losses if the forecast ordering is wrong. |
| C | False (accurate) | The quoted statement is correct: sensitivity analysis (perturbing returns, risks, correlations) tests whether the allocation stays reasonable. |
| D | True (incorrect) | The quoted statement is incorrect: leverage *magnifies* the effect of estimation error rather than making uncertainty irrelevant. |
| E | False (accurate) | The quoted statement is correct: a robust process might scale back both positions rather than fully trust one noisy point estimate. |

**Reference:** Grinold & Kahn, *Active Portfolio Management*, 2nd ed. (robust construction, resampling/sensitivity); Ledoit & Wolf (shrinkage); Markowitz (1952); Balch ML4T 02-10.

### [QF2-D5G6Q3] Corner solutions vs. shrinkage/penalized allocations
**Scenario:** Across rolling out-of-sample periods, Method E picks extreme corner solutions with the highest in-sample expected return; Method R uses shrinkage and weight penalties, giving less extreme allocations, slightly lower in-sample return, but more stable out-of-sample performance.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | A higher in-sample objective is conditional on estimated inputs that may not persist, so it does not guarantee better realized performance. |
| B | True | Method R trades some reliance on point estimates for greater allocation stability. |
| C | True | Stable weights reduce turnover caused solely by small forecast fluctuations. |
| D | False | Robustness does not require equal weights; many unequal-weight portfolios can be robust. |
| E | True | Out-of-sample evidence reveals whether apparent optimization benefits survive estimation error. |

**Reference:** Grinold & Kahn, *Active Portfolio Management*, 2nd ed. (robustness, out-of-sample validation); Ledoit & Wolf (shrinkage); Balch ML4T 02-10.

### [QF2-D5G7Q1] Cost-aware rebalancing decisions
**Scenario:** An optimizer recommends a major rebalance because forecasts changed slightly; the trades would incur substantial transaction costs while the expected return improvement is small.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | A cost-aware optimizer may decline to trade when the expected benefit does not exceed implementation cost. |
| B | False | Current holdings determine how much trading is required, so they cannot be ignored. |
| C | True | Rebalancing/turnover penalties discourage low-value trading. |
| D | True | A frictionless-optimal portfolio can be economically inferior once costs are netted out. |
| E | True | Trading thresholds prevent small forecast changes from triggering large, uneconomic trades. |

**Reference:** Grinold & Kahn, *Active Portfolio Management*, 2nd ed. (transaction-cost-aware optimization, turnover); Balch ML4T 02-10.

### [QF2-D5G7Q2] No-trade region around a frictionless target
**Scenario:** A fund holds 4% in Stock A; the new frictionless target is 4.3%, but buying the extra 0.3% crosses a wide spread and incurs impact. A cost-aware model estimates the incremental benefit is smaller than the cost.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Holding 4% can be optimal under a cost-aware objective when incremental cost exceeds incremental benefit. |
| B | True | The existing position matters because cost depends on the trade from current to target holdings. |
| C | False | Not every nonzero gap to the frictionless target should trigger a trade — small improvements may be uneconomic after spreads, impact, and taxes. |
| D | True | A no-trade region lets small forecast changes pass without immediate rebalancing. |
| E | True | If trading costs later decline enough, moving closer to the frictionless target can become worthwhile. |

**Reference:** Grinold & Kahn, *Active Portfolio Management*, 2nd ed. (no-trade regions, transaction costs); Balch ML4T 02-10.

### [QF2-D5G7Q3] Turnover penalties and signal thresholds
**Scenario:** A daily strategy flips between full long and full short when a noisy forecast crosses zero. The frictionless backtest shows attractive gross returns, but live turnover and costs are high. The team considers a stronger signal threshold and a penalty proportional to traded dollars.
**Answer polarity:** **Inverted (True = the quoted statement is INCORRECT; False = the quoted statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | The quoted statement is correct: forecast noise near zero can flip the target repeatedly when the rule has no buffer. |
| B | False (accurate) | The quoted statement is correct: a stronger entry/reversal threshold creates a no-trade range that suppresses weak-signal trading. |
| C | True (incorrect) | The quoted statement is incorrect: a turnover penalty *lowers* the objective value of trade-intensive changes, making them less attractive. |
| D | False (accurate) | The quoted statement is correct: gross backtest performance can overstate net performance when frequent trading is costly. |
| E | False (accurate) | The quoted statement is correct: a cost-aware rule compares expected improvement with implementation cost rather than minimizing turnover at any price. |

**Reference:** Grinold & Kahn, *Active Portfolio Management*, 2nd ed. (turnover penalties, net-of-cost optimization); Balch ML4T 02-10.

## References (domain-level)

1. **Grinold & Kahn — *Active Portfolio Management*, 2nd ed.:** translating alphas/forecasts into positions (the information coefficient, risk-adjusted and confidence-weighted sizing); active vs. benchmark-relative weights, active risk/tracking error and active share; risk models and the marginal contribution to risk; leverage, position, sector, and turnover constraints and their cost to the optimal solution; transaction-cost-aware optimization and robustness to estimation error. Primary reference for G1–G7.
2. **Markowitz — *Portfolio Selection* (1952) / mean-variance optimization:** the efficient frontier, reward-vs-variance tradeoff, portfolio variance as a function of weights and the covariance matrix (not a weighted average of volatilities), and the well-known sensitivity ("error-maximization") of MVO weights to noisy expected-return inputs. Supports G1Q1, G2Q1, G4Q1, G4Q2, G6Q1, G6Q2.
3. **Ledoit & Wolf — shrinkage estimation:** shrinking noisy sample estimates (expected returns toward a common mean; the sample covariance matrix toward a structured target) to reduce extreme, unstable allocations — the robustness lever behind G6Q1, G6Q2, G6Q3.
4. **Balch — ML4T lecture 02-10 (Portfolio Optimization & the Efficient Frontier):** building and optimizing a portfolio, sizing from views, the efficient frontier, and why real-world constraints, costs, and estimation error change the implemented portfolio. Section-level support across all seven groups.
