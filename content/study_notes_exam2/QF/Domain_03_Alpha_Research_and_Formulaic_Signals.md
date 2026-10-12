# QF Domain 3 — Alpha Research & Formulaic Signals

## Domain cheat-sheet

- **What an alpha signal claims (and does not).** An alpha score is a *forecast of benchmark-relative (active) return* — an **expectation across many observations**, not a guarantee on any single name. A high-scored stock can lose on a given day without invalidating the model; predictive quality must be judged over an appropriate **sample** and over the signal's **stated horizon**, never from one noisy realization. Key distinctions:
  - **Active (benchmark-relative) return = asset return − benchmark return.** A stock can have a *positive absolute* return but a *negative active* return if its benchmark rose more. Evaluate outcomes against the signal's forecast target and horizon, not against raw price moves.
  - **Ordering vs. magnitude.** A score can usefully *order* opportunities without being *calibrated* in units of expected return. A unitless rank (0–100) preserves order, **not** proportional distances: a rank of 80 does **not** forecast twice the active return of a rank of 40. Mapping any score to portfolio weights requires separate decisions about **risk, confidence, constraints, and position sizing**.
  - **Forecast magnitude ≠ forecast confidence.** Two names with equal point forecasts can carry very different uncertainty (abundant stable data vs. sparse noisy data). Incorporating confidence can rationally shrink the lower-confidence position under a tracking-error limit; confidence *characterizes* uncertainty — it never *removes* it or converts a forecast into a guaranteed return. Realized active return also depends on market outcomes, exposure, timing, and implementation — not the entry score alone.
- **Time-series vs. cross-sectional signals.** A **time-series** signal evaluates each instrument against *its own history through time* (e.g., a trend/own-return forecast) and can recommend the *same directional position for many names at once* → it tends to carry market/directional exposure. A **cross-sectional** signal ranks instruments *against each other at one point in time* (e.g., carry rank) and identifies relative winners/losers. Consequences:
  - A name can have a **positive absolute forecast yet rank below most peers** — absolute direction and relative attractiveness are different questions and can prescribe different trades.
  - A cross-sectional ranking is **not automatically market-neutral**: neutrality depends on the *portfolio-construction rule* that maps ranks to long/short weights and on the resulting exposures. In a broad rally where every forecast is positive, a market-neutral manager still shorts the bottom decile (expressing *relative* underperformance, not negative absolute returns); a "hold everything positive" directional rule leaves the book broadly long.
  - A relative long-short strategy is evaluated against its **intended benchmark and exposures**, not merely whether the market rose. Combining a time-series and a cross-sectional signal needs **scale alignment** (differing units/distributions otherwise let one signal dominate) and does **not** guarantee independent information — they may share inputs or respond to the same forces.
- **Ranking, scaling, and transformation.** Raw signals with different cross-sectional dispersion across groups let the widest-dispersion group dominate a composite.
  - **Percentile ranking** places each observation relative to peers, reducing dominance from differing numerical scales and preserving *within-group ordering* (a monotonic transform). But percentile *spacing* describes distributional position, **not** equal increments of economic value (90→80 ≠ 60→50 in expected return). Ranking **within** a group (e.g., within industry) reduces unintended group bets. No transformation *creates* information from a non-predictive input.
  - **Cross-sectional z-score** = (raw − universe mean) / universe standard deviation; a z of +2 is "two cross-sectional standard deviations above the mean." Because both the mean and the standard deviation are functions of *all* observations, a single extreme (e.g., a data error) distorts the scaling of *every* name and can produce an oversized position. **Winsorization** caps/replaces tail values at chosen bounds (it does not delete all out-of-bound points) to limit influence — but capping never *proves* the remaining values are economically valid, and it is no substitute for **investigating and correcting bad data**.
  - **Neutralization** (regressing the alpha on a characteristic such as market cap and using the **residual**) removes the component *linearly associated with the specified control in the fitted sample*, reducing an unintended systematic exposure. It does **not** guarantee better out-of-sample returns (risk control vs. performance is an empirical tradeoff), can **discard genuine signal** if the exposure is part of the alpha's true mechanism, and leaves *other* exposures (sector, beta, liquidity) still to be checked.
- **Formulaic alpha construction.** A formulaic alpha is an explicit function of price/volume/volatility inputs (the Kakushadze "101 Formulaic Alphas" style). Fully specifying it requires the **signs, units, missing-value treatment, and denominator floor** — these determine the actual values produced.
  - Behavior follows the algebra: dividing by volatility makes otherwise-similar observations score differently, and a **near-zero denominator** can explode the signal unless floored/safeguarded.
  - **Economic intuition does not establish predictive power** — multiplying several plausible inputs still requires properly designed **out-of-sample** validation. Searching many transformations (square, cube, rank, logs, conditionals) and optimizing lookbacks against *one* sample invites **data-mining / multiple-testing bias**: the highest in-sample Sharpe may be fitting noise and need not identify the best live alpha. Incremental complexity should earn its place through **stable out-of-sample improvement** and an interpretable/defensible mechanism; robustness across *nearby* parameter values is more reassuring than a narrow spike. Strictly monotonic transforms of the same input can yield **identical rankings** despite different magnitudes.
- **Signal decay and holding period.** Alphas have a **decay horizon** — the window over which predictive content persists.
  - **Holding period must match decay horizon.** A signal predictive for 30 minutes but acted on only at a daily rebalance can be **stale before the portfolio trades**; strong short-horizon predictiveness does **not** guarantee daily profitability. Faster decay implies **higher turnover pressure**, and execution timing is part of whether an alpha is *realizable*.
  - **Information coefficient (IC)** — the correlation between forecasts and realized outcomes — can be measured at successive horizons after signal formation. A profile that is strongest at day 1 and decays to statistically-indistinguishable-from-zero by day 10 is evidence of **decaying predictive content**; old scores add little incremental forecasting value. Daily rebalancing is *not* automatically optimal: faster refresh incurs spreads, impact, and capacity costs that can outweigh added gross alpha. **Overlapping/staggered rebalancing** can trade immediacy for lower concentration and turnover. Decay studies must use only **point-in-time** information available at each historical decision (avoid look-ahead bias).
  - Holding past the demonstrated-edge window (e.g., an event signal active days 1–5 held a month) exposes capital *beyond* its predictive period; longer holding does **not** necessarily add cumulative alpha. Reducing turnover helps net results **only if** saved costs exceed alpha lost to slower exits.
- **Combining multiple alpha signals.** Positive standalone performance of each signal does **not** establish that the signals are *independent*.
  - **Correlation reduces incremental diversification.** Highly correlated signals (value & quality) succeed and fail on similar names, so the composite should be judged for **marginal information beyond its components**. A weaker but *less-correlated* alpha can improve a composite more than a stronger redundant one. Equal weighting does **not** equalize *risk contribution* (differing volatilities, scales, correlations, and mappings create unequal risk).
  - **Weighting by estimated IC** (e.g., 0.06/0.04/0.02) is reasonable in principle, but estimates are **noisy** — sampling error makes fine weight distinctions unstable; correlation and **turnover/implementation costs** justify departing from gross-strength weighting; and a small-IC signal can still deserve positive weight for diversifying/cheap/stable information. Standardization aligns scale but does **not** equalize reliability or trading cost.
  - **Effective breadth < raw component count** when components overlap. Four momentum formulas on 9/10/11/12-month returns are **highly correlated** (shared observations and mechanism): averaging reduces sensitivity to one lookback (robustness averaging) but does **not** quadruple independent information. Correlation and incremental-performance analysis distinguish robustness averaging from genuine diversification.
- **Crowding, replication, and realizable alpha.** A paper backtest's **gross** alpha is not the **net, realizable** alpha.
  - **Crowding/alpha decay.** As a public signal is adopted widely, competition can incorporate the information *earlier* (reducing future predictive return), create **crowded positions** that unwind together, and raise **market impact** as more capital chases the same trades. Historical gross alpha is **not** guaranteed to persist; live deterioration can reflect *both* reduced economic alpha *and* higher implementation cost.
  - **Capacity.** Scaling capital requires **larger trades relative to available volume**; higher participation rates raise impact and reduce realizable alpha — net alpha per dollar is **not** invariant to asset level (costs change nonlinearly with scale). Capacity analysis must weigh **liquidity, turnover, execution horizon, and concentration** of opportunities. A strategy can have genuine gross predictive value yet be unattractive after spreads, fees, slippage, and impact.
  - **Replication vs. data snooping.** Searching thousands of formulas raises the chance the "best" is a **chance pattern**. An **economic rationale** supports falsifiable expectations of when/why an alpha persists, helping distinguish information from coincidence; lack of a rationale does **not** mathematically *prove* a signal has zero predictive value, but it raises confidence/governance concerns. **Stability across markets, periods, and reasonable specifications** is robustness evidence. The strongest in-sample backtest should **not** automatically override concerns about replication, multiple testing, capacity, and realizability.

## Common traps

- **Inverted-polarity questions (10 of 21 here).** When the body says "each item asserts that its quoted statement is **incorrect**," the Answer Key verdict is flipped relative to the statement's plain truth: **True = the quoted statement is wrong; False = the quoted statement is accurate.** Read the polarity line *first*. Inverted here: **G1Q2, G2Q1, G3Q3, G4Q2, G4Q3, G5Q1, G5Q2, G6Q3, G7Q2, G7Q3.** The remaining 11 are Normal (True = accurate).
- **One bad realization ≠ a broken model.** A single negative return on the top-scored name does not disprove a probabilistic forecast; assess over a sample and over the stated horizon. Absolute return ≠ active return.
- **Rank treated as calibrated return.** Ranks/percentiles preserve *order*, not proportional *distance* or return units; a rank of 80 does not forecast 2× a rank of 40, and percentile spacing is not equal economic increments.
- **Point forecast confused with confidence.** Equal expected returns can have unequal uncertainty; confidence can justify smaller sizing but never removes risk or guarantees a return.
- **Cross-sectional ranking assumed market-neutral.** Neutrality comes from the long/short *construction rule* and resulting exposures, not from ranking itself. Shorting a bottom-decile name expresses *relative* weakness, not a negative absolute forecast.
- **Time-series signal assumed neutral.** Own-history/trend signals can push the same direction across many names → broad market exposure.
- **"Transformation creates information."** Percentile/rank/z-score/winsorization improve comparability and control influence but cannot manufacture predictive power from a non-predictive input, and winsorization never validates the data.
- **Outlier in a cross-sectional z-score.** One extreme shifts the mean *and* standard deviation, rescaling *every* name; winsorize **and** investigate the data — capping is not a data-quality fix.
- **Neutralization is a free win.** Residualizing on a control removes only the *linear in-sample* component, may discard genuine signal if the exposure is part of the mechanism, doesn't guarantee out-of-sample gains, and leaves other exposures uncontrolled.
- **Economic intuition / in-sample Sharpe = validated alpha.** Neither proves live performance; multiple testing and lookback optimization on one sample fit noise. Prefer out-of-sample stability, robustness across nearby parameters, and a defensible mechanism.
- **Denominator with no floor.** Dividing by a near-zero volatility (or volume) term can explode the signal; floors/robust handling are part of the spec.
- **Holding period mismatched to decay.** Acting slowly on a fast-decaying signal captures stale information; strong short-horizon IC does not guarantee daily profit; longer holds don't automatically add cumulative alpha.
- **Daily rebalancing assumed optimal.** Highest day-1 IC does not make daily refresh best — spreads, impact, and capacity can outweigh gross gains; staggered/overlapping schedules are design levers. Decay studies must be point-in-time (no look-ahead).
- **Overlapping components counted as breadth.** Adjacent lookbacks are highly correlated; component count overstates *effective* breadth. Equal weights don't equalize risk contribution; IC-proportional weights are unstable under estimation noise.
- **Gross backtest = realizable alpha.** Crowding erodes future returns and adds impact; capacity is finite and costs scale nonlinearly; net alpha per dollar is not invariant to size.
- **Data-snooped winner over economically grounded signal.** A huge formula search makes extreme in-sample results likely by chance; a mechanism and cross-market/period stability are robustness evidence. Missing rationale raises concern but does not *prove* zero predictive value.
- **Garbled source glyphs.** The slice renders "fi"/"fl" ligatures as mojibake (e.g., "ﬁve-day", "conﬁdence", "proﬁtable", "beneﬁcial", "reﬂects"). These are typesetting artifacts only — read them as "five-day", "confidence", "profitable", "beneficial", "reflects"; no verdicts are affected.

## Questions

### [QF2-D3G1Q1] Alpha score — expectation, not guarantee
**Scenario:** A long-short team's daily alpha score forecasts five-day benchmark-relative return. The top-scored stock lost 2% yesterday and a PM argues the model is invalid; the research lead must clarify what the score does and does not claim.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | An alpha forecast is an *expectation* across observations and can be wrong in an individual case — a positive score is not a guarantee. |
| B | False | One negative realized return cannot prove a probabilistic signal has no information; predictive quality is assessed over an appropriate sample, not one noisy outcome. |
| C | True | A one-day outcome is not automatically aligned with a forecast defined over a five-day horizon — evaluate against the stated horizon. |
| D | True | Active return = asset return − benchmark return, so a positive absolute return can be a negative active return if the benchmark rose more. |
| E | True | Scores can *order* opportunities without being calibrated in units of expected return; magnitude need not equal a return percentage unless calibrated that way. |

**Reference:** Grinold & Kahn, *Active Portfolio Management*, 2nd ed., ch. on information analysis / the forecasting rule of thumb (alpha = expected residual return); Balch ML4T week-9 lectures on alpha signals and benchmark-relative (active) return.

### [QF2-D3G1Q2] Return-unit forecast vs. unitless rank
**Scenario:** A CIO sees Signal X (expected excess return, 40 bps) and Signal Y (unitless 0–100 rank) and wants to allocate twice the capital to a score of 80 as to 40 without examining how either signal was constructed or calibrated.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: X expresses a forecast magnitude in return units while Y may only express relative ordering — different meanings and units. The claim is correct, so the inverted verdict is False. |
| B | True (incorrect) | Wrong: a rank of 80 does not necessarily forecast twice the active return of a rank of 40 — ranks preserve order, not proportional distances or return magnitudes. |
| C | False (accurate) | Correct: mapping either signal into weights requires decisions about risk, confidence, constraints, and sizing — a forecast alone does not fix capital at risk. |
| D | False (accurate) | Correct: a signal can rank securities usefully even if its values are not calibrated expected returns — ordering supports selection without magnitude calibration. |
| E | True (incorrect) | Wrong: realized active return is not determined solely by the entry score — it also depends on market outcomes, exposure, timing, implementation, and the benchmark. |

**Reference:** Grinold & Kahn, *Active Portfolio Management*, 2nd ed., chapters on information analysis and portfolio construction (forecasts → weights requires risk/constraint decisions); Balch ML4T week-9 on signal scaling and interpretation.

### [QF2-D3G1Q3] Equal point forecasts, unequal confidence
**Scenario:** A model gives two stocks identical expected active returns, but Stock A rests on abundant stable data and Stock B on sparse noisy data. The PM proposes equal positions; the risk officer asks whether confidence should affect sizing under a tight tracking-error limit.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Equal point forecasts do not imply equal uncertainty — forecast magnitude and forecast uncertainty are distinct quantities. |
| B | True | Incorporating confidence can rationally assign a smaller position to the lower-confidence name (Stock B) even when central forecasts match. |
| C | False | A confidence estimate characterizes uncertainty; it cannot convert an uncertain forecast into a guaranteed return. |
| D | True | Historical signal accuracy can inform confidence but cannot eliminate future model risk (past reliability ≠ out-of-sample stability). |
| E | True | Tracking-error and exposure constraints can prevent taking the position implied by an alpha ranking alone — construction reconciles forecasts with limits. |

**Reference:** Grinold & Kahn, *Active Portfolio Management*, 2nd ed., information analysis (shrinking forecasts by confidence/IC) and portfolio construction under risk constraints; Balch ML4T week-9 on confidence-weighted signals.

### [QF2-D3G2Q1] Time-series vs. cross-sectional; neutrality not automatic
**Scenario:** A futures fund runs one model forecasting each contract's own next-month return and another ranking all contracts at today's date. The CRO asks whether they answer the same question and whether either necessarily yields a market-neutral portfolio.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: the first model is time-series because it evaluates each contract against its own history through time. The claim is correct, so the inverted verdict is False. |
| B | False (accurate) | Correct: the second model is cross-sectional because it compares contracts with one another at the same point in time. |
| C | False (accurate) | Correct: a contract can receive a positive absolute forecast yet still rank below most peers — positive need not mean strong relative to others. |
| D | True (incorrect) | Wrong: a cross-sectional ranking does not automatically produce a market-neutral portfolio — neutrality depends on how ranks map to long/short weights and the resulting exposures. |
| E | False (accurate) | Correct: the two models can prescribe different positions because one concerns absolute direction and the other relative attractiveness. |

**Reference:** Grinold & Kahn, *Active Portfolio Management*, 2nd ed., on benchmark-relative construction and neutralization; Kakushadze, "101 Formulaic Alphas" (2016), §2–§3 (cross-sectional operators and dollar-neutrality via construction); Balch ML4T week-9 on time-series vs. cross-sectional signals.

### [QF2-D3G2Q2] Market-neutral vs. directional in a rally
**Scenario:** During a broad rally every stock in a 100-name universe has a positive predicted return. A market-neutral manager still buys the top decile and shorts the bottom decile; a directional manager holds all positively-forecast stocks. The committee compares intended use and benchmarking.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The market-neutral manager can short bottom-ranked stocks even with positive absolute forecasts — shorts express relative underperformance, not negative absolute returns. |
| B | True | The directional rule can create substantial market exposure because every stock passes its positive-forecast threshold → broadly long. |
| C | False | A long-short strategy is evaluated against its intended benchmark and exposures, not merely whether the market rose. |
| D | True | Cross-sectional performance depends on the return *spread* between high- and low-ranked securities. |
| E | False | A positive forecast for every stock does not make ranking impossible — forecasts still differ in magnitude and can be ranked. |

**Reference:** Grinold & Kahn, *Active Portfolio Management*, 2nd ed., on long-short construction, benchmark/active exposures; Balch ML4T week-9 on market-neutral vs. directional portfolios.

### [QF2-D3G2Q3] Combining trend (time-series) and carry (cross-sectional)
**Scenario:** A currency researcher combines a time-series trend score and a cross-sectional carry rank into one portfolio. The head trader warns their scales, horizons, and exposure implications differ; the book must respect dollar-exposure and turnover limits.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | A time-series score can recommend the same directional position for many currencies at once (each assessed against its own history). |
| B | False | A cross-sectional rank identifies stronger/weaker opportunities without necessarily forecasting each currency's absolute sign. |
| C | True | Combining the signals may require scale alignment first — differing units/distributions can otherwise let one signal dominate arbitrarily. |
| D | True | Exposure limits can alter implementable positions even when both signals agree. |
| E | False | Using both a time-series and a cross-sectional signal does not guarantee independent information — they may share inputs, forces, or be correlated. |

**Reference:** Kakushadze, "101 Formulaic Alphas" (2016), §2 (combining alphas, scaling/normalization); Grinold & Kahn, *Active Portfolio Management*, 2nd ed., on combining signals and constraints; Balch ML4T week-9.

### [QF2-D3G3Q1] Within-industry percentile ranking
**Scenario:** Raw earnings-surprise signals differ in dispersion across industries, so technology dominates the composite. The PM considers converting to within-industry percentile ranks before selecting top/bottom deciles.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Percentile ranking places each observation relative to peers rather than its raw scale, reducing dominance from different numerical scales across industries. |
| B | True | Percentile ranks preserve ordering within each ranked group — a monotonic rank transform retains ordinal information. |
| C | False | Percentile spacing describes distributional position, not equal increments of economic value, so 90→80 need not equal 60→50 in expected return. |
| D | True | Ranking within industries reduces unintended industry bets relative to ranking all raw values together. |
| E | False | Transformation can improve comparability but cannot create genuine information from a non-predictive input. |

**Reference:** Kakushadze, "101 Formulaic Alphas" (2016), §2–§3 (rank operator, cross-sectional normalization); Balch ML4T week-9 on ranking and signal transformation.

### [QF2-D3G3Q2] Cross-sectional z-score and winsorization
**Scenario:** A factor model forms a cross-sectional z-score (subtract universe mean, divide by standard deviation). A data error creates an extreme score that shifts both statistics and produces an oversized position; the committee considers winsorizing inputs before standardization.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | A z-score of +2 means the raw observation is two cross-sectional standard deviations above the mean under the stated calculation. |
| B | True | An extreme observation affects the mean and standard deviation used to scale every security — both statistics are functions of all observations. |
| C | True | Winsorization generally limits (caps/replaces) extreme values at chosen bounds rather than deleting every out-of-bound observation. |
| D | False | Capping controls influence but does not prove a remaining extreme score reflects economically valid information. |
| E | True | Data-quality investigation remains necessary even if winsorization shrinks the position — a transformation is not a substitute for correcting erroneous inputs. |

**Reference:** Kakushadze, "101 Formulaic Alphas" (2016), §2 (standardization/winsorization of alpha inputs); Grinold & Kahn, *Active Portfolio Management*, 2nd ed., on robust forecast scaling; Balch ML4T week-9.

### [QF2-D3G3Q3] Size-neutralization via regression residual
**Scenario:** A valuation alpha strongly favors small caps. To get stock-specific selection rather than a persistent size bet, the researcher regresses the alpha on market cap and uses the residual as a neutralized signal. The CIO asks what this removes and whether it is always beneficial.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: the residual removes the component linearly associated with market cap in the fitted sample. The claim is correct, so the inverted verdict is False. |
| B | False (accurate) | Correct: neutralization can reduce an unintended systematic size exposure by isolating variation beyond the chosen relationship. |
| C | True (incorrect) | Wrong: neutralization does not necessarily improve out-of-sample returns — risk control vs. predictive performance is an empirical tradeoff, not a guaranteed gain. |
| D | False (accurate) | Correct: if size exposure is part of the alpha's genuine mechanism, removing it can also remove useful predictive information. |
| E | False (accurate) | Correct: after neutralization the portfolio still needs checks for other exposures and constraints (sector, beta, liquidity). |

**Reference:** Grinold & Kahn, *Active Portfolio Management*, 2nd ed., on factor neutralization and residual (characteristic-neutral) alphas; Kakushadze, "101 Formulaic Alphas" (2016), §2 (neutralization operators); Balch ML4T week-9 on factor exposure control.

### [QF2-D3G4Q1] Price-volume-volatility formula specification
**Scenario:** A desk proposes alpha = 20-day return × (current volume / average volume) ÷ recent volatility. The research director likes the intuition but requires documenting the formula's behavior before backtesting.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Holding other inputs fixed, a larger positive return produces a larger positive alpha — with positive volume and volatility terms the formula increases with return. |
| B | True | Dividing by volatility makes otherwise-similar observations score differently; lower measured volatility raises the magnitude when the numerator is unchanged. |
| C | True | If volatility approaches zero the formula can generate unstable/extremely large values unless safeguarded — a near-zero denominator motivates floors. |
| D | False | Multiplying several plausible inputs does not guarantee the combination predicts future returns — intuition must be validated out-of-sample. |
| E | True | The signs, units, missing-value treatment, and denominator floor are part of fully specifying the alpha — they determine the actual values produced. |

**Reference:** Kakushadze, "101 Formulaic Alphas" (2016), §1–§4 (formula definitions, operators, denominator handling, specification detail); Balch ML4T week-9 on constructing formulaic signals.

### [QF2-D3G4Q2] Transformation search and overfitting
**Scenario:** A researcher tests a linear momentum score, its square, cube, rank, and dozens of nested log/conditional versions. The most complicated formula wins in-sample Sharpe by a small margin. The committee asks whether complexity is justified under explainability and robust out-of-sample requirements.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: searching many transformations increases the opportunity to select a formula that fits noise — multiple testing raises selection bias. The claim is correct, so the inverted verdict is False. |
| B | False (accurate) | Correct: a nonlinear transformation can be useful when the economic relationship is genuinely nonlinear. |
| C | True (incorrect) | Wrong: the highest in-sample Sharpe does not necessarily identify the best live alpha — it may reflect overfitting. |
| D | False (accurate) | Correct: incremental complexity should be supported by stable out-of-sample improvement and an interpretable/defensible mechanism. |
| E | False (accurate) | Correct: two formulas that are monotonic transforms of the same input can produce identical rankings even though raw magnitudes differ. |

**Reference:** Kakushadze, "101 Formulaic Alphas" (2016), §1 (parsimony, out-of-sample caution); Grinold & Kahn, *Active Portfolio Management*, 2nd ed., on overfitting and multiple testing in forecasting; Balch ML4T week-9 on data snooping / backtest overfitting.

### [QF2-D3G4Q3] Lookback optimization and data-mining bias
**Scenario:** A team builds a price-volume alpha (5-day return, 20-day average volume, 60-day volatility) and the PM asks to optimize all three lookbacks against the same backtest until performance peaks. Trading costs rise sharply for the shortest-horizon variants.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: the selected lookbacks define the alpha's effective memory and responsiveness. The claim is correct, so the inverted verdict is False. |
| B | False (accurate) | Correct: optimizing many parameter combinations on one sample can create data-mining bias. |
| C | True (incorrect) | Wrong: parameter choices are not harmless — changing a lookback alters the data summarized, the forecast timing, and often the resulting positions. |
| D | False (accurate) | Correct: a more responsive specification may raise turnover and reduce net performance despite stronger gross results. |
| E | False (accurate) | Correct: robustness across nearby parameter values can be more reassuring than a narrow performance spike at one combination. |

**Reference:** Kakushadze, "101 Formulaic Alphas" (2016), §1 (lookback windows, robustness); Grinold & Kahn, *Active Portfolio Management*, 2nd ed., on data mining and turnover/cost tradeoffs; Balch ML4T week-9 on parameter overfitting.

### [QF2-D3G5Q1] Decay horizon vs. rebalance frequency mismatch
**Scenario:** A formulaic alpha predicts well for 30 minutes but the portfolio rebalances once daily. The research lead argues it should still work because the forecast direction is correct.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: the signal's holding period is mismatched with its decay horizon — it fades much faster than the rebalance schedule. The claim is correct, so the inverted verdict is False. |
| B | False (accurate) | Correct: a signal can become stale before the portfolio acts on it, so delayed action can eliminate the predictive value. |
| C | True (incorrect) | Wrong: strong short-horizon predictiveness does not guarantee daily profitability — a correct 30-minute forecast may not survive a daily hold. |
| D | False (accurate) | Correct: faster signal decay often implies higher turnover pressure to capture it. |
| E | False (accurate) | Correct: execution timing is part of whether an alpha is realizable. |

**Reference:** Grinold & Kahn, *Active Portfolio Management*, 2nd ed., on information horizon, turnover, and the information coefficient; Kakushadze, "101 Formulaic Alphas" (2016), §4 (holding/decay); Balch ML4T week-9 on signal decay and holding period.

### [QF2-D3G5Q2] Event-driven decay vs. one-month hold
**Scenario:** An event-driven signal earns most of its return in the first two days after an announcement and shows no reliable effect after day five. To cut turnover, the PM proposes holding every position for one month. The team must assess whether lower frequency preserves the edge.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: holding a month exposes capital beyond the period in which the signal has demonstrated predictive value. The claim is correct, so the inverted verdict is False. |
| B | True (incorrect) | Wrong: a longer holding period does not necessarily increase cumulative alpha — extra time can add risk or unrelated returns after the edge disappears. |
| C | False (accurate) | Correct: positions can be stale once the event information has been incorporated into prices. |
| D | False (accurate) | Correct: the exit rule should be evaluated against the signal's observed decay profile and implementation costs. |
| E | False (accurate) | Correct: reducing turnover improves net results only if saved costs exceed any alpha lost to slower exits or fewer refreshed positions. |

**Reference:** Grinold & Kahn, *Active Portfolio Management*, 2nd ed., on signal decay, turnover, and net-of-cost performance; Kakushadze, "101 Formulaic Alphas" (2016), §4 (holding period); Balch ML4T week-9 on event signals and decay.

### [QF2-D3G5Q3] Information-coefficient decay profile
**Scenario:** A market-neutral fund measures a signal's information coefficient at days 1, 5, 10, and 20 after formation. It is strongest on day 1, declines steadily, and is statistically indistinguishable from zero by day 10. The head trader asks whether daily rebalancing is automatically optimal despite limited liquidity.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The pattern is evidence the signal's predictive content decays with age — the forecast/outcome association weakens farther from formation. |
| B | True | A day-ten coefficient near zero suggests ten-day-old scores provide little incremental forecasting value (indistinguishable from noise). |
| C | False | Daily rebalancing need not maximize net performance despite the highest day-1 coefficient — faster refresh can incur spreads, impact, and capacity costs that outweigh added gross alpha. |
| D | True | Overlapping positions or staggered rebalancing can be evaluated to balance decay, turnover, and liquidity (trading immediacy for lower concentration). |
| E | True | The decay study should use only point-in-time information available at each historical decision — otherwise look-ahead bias makes the decay profile unreliable. |

**Reference:** Grinold & Kahn, *Active Portfolio Management*, 2nd ed., on the information coefficient, information horizon, and turnover; Balch ML4T week-9 on measuring IC decay and point-in-time backtesting.

### [QF2-D3G6Q1] Correlated signals and diversification
**Scenario:** A multi-factor fund equal-weights value, quality, and momentum alphas. Each has positive standalone performance, but value and quality are highly correlated in its universe. The CIO assumes three signals give three independent diversification sources.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Positive standalone performance does not establish independence — individual usefulness and pairwise dependence are separate properties. |
| B | True | High correlation between value and quality reduces incremental diversification — correlated signals succeed and fail on similar names. |
| C | False | Equal weighting does not guarantee equal risk contribution — differing volatilities, scales, correlations, and mappings create unequal contributions. |
| D | True | The combined signal should be evaluated for marginal information beyond its components (does combination add value after overlap). |
| E | True | A weaker but less-correlated alpha can improve a composite more than a stronger redundant one — diversifying information aids aggregate consistency. |

**Reference:** Grinold & Kahn, *Active Portfolio Management*, 2nd ed., on combining signals, correlation, and risk decomposition; Kakushadze, "101 Formulaic Alphas" (2016), §2 (alpha correlations); Balch ML4T week-9 on combining alphas.

### [QF2-D3G6Q2] IC-proportional weighting under noise
**Scenario:** A platform outputs three standardized alphas with estimated ICs of 0.06, 0.04, 0.02. The PM wants weights proportional to those estimates. The validation lead notes the estimates are noisy, the first two signals are correlated, and the third trades much less frequently.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Weighting by estimated strength may be reasonable, but estimation uncertainty makes exact weights unstable — sampling error undermines fine distinctions. |
| B | True | Correlation among alphas matters because it affects the incremental information each contributes — a strong signal adds less when it duplicates another. |
| C | False | The smallest-IC signal can still deserve positive weight — it may add diversifying, stable, or inexpensive predictive information. |
| D | True | Turnover and implementation costs can justify a different weighting from one based only on gross predictive strength. |
| E | True | Standardization aligns numerical scale but does not make signals equally reliable or equally costly to trade. |

**Reference:** Grinold & Kahn, *Active Portfolio Management*, 2nd ed., on optimal signal weighting, IC estimation error, and net-of-cost contribution; Balch ML4T week-9 on weighting alphas by information coefficient.

### [QF2-D3G6Q3] Four overlapping momentum windows — effective breadth
**Scenario:** A fund builds a composite from four momentum formulas using 9-, 10-, 11-, and 12-month returns. The backtest is smoother than any single component, and the team calls it a four-alpha ensemble. The model-risk committee asks whether the apparent breadth is genuine.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: the four alphas are likely highly correlated because their inputs and horizons substantially overlap. The claim is correct, so the inverted verdict is False. |
| B | False (accurate) | Correct: averaging nearby specifications can reduce sensitivity to any single lookback choice. |
| C | True (incorrect) | Wrong: using four formulas does not quadruple independent information — redundant transformations do not create proportional independent content. |
| D | False (accurate) | Correct: the ensemble may still be useful, but its effective breadth is likely smaller than its raw component count. |
| E | False (accurate) | Correct: correlation and incremental-performance analysis help distinguish robustness averaging from genuine alpha diversification. |

**Reference:** Grinold & Kahn, *Active Portfolio Management*, 2nd ed., on breadth, effective breadth, and correlated bets (Fundamental Law); Kakushadze, "101 Formulaic Alphas" (2016), §2 (correlation among similar alphas); Balch ML4T week-9 on ensemble breadth.

### [QF2-D3G7Q1] Crowding and alpha decay
**Scenario:** A once-profitable public valuation signal is now followed by many large managers. The paper backtest still shows attractive gross returns at closing prices, but live orders increasingly move prices and subsequent returns weaken. The committee asks whether popularity changes the opportunity.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Competition can cause prices to adjust earlier, reducing the signal's future predictive return (information is incorporated before later traders act). |
| B | True | Shared use can create crowded positions many funds try to exit simultaneously, amplifying losses and liquidity pressure during unwinds. |
| C | False | Historical gross alpha is not guaranteed to persist after a strategy becomes widely known — alpha decays as information diffuses and competitors adapt. |
| D | True | Market impact can increase as more capital attempts to trade the same opportunities (crowded demand consumes liquidity). |
| E | True | Live deterioration can reflect both reduced economic alpha and higher implementation costs — realized performance combines opportunity and cost. |

**Reference:** Grinold & Kahn, *Active Portfolio Management*, 2nd ed., on alpha decay, transaction costs, and implementation; Kakushadze, "101 Formulaic Alphas" (2016), §1 (crowding/decay of public alphas); Balch ML4T week-9 on crowding and realizable alpha.

### [QF2-D3G7Q2] Capacity and market impact at scale
**Scenario:** A small-cap strategy reports 8% annualized gross alpha assuming execution at the daily close with no price impact. The fund plans to deploy ten times the tested capital although many target names trade modest daily volume. The COO requests a capacity assessment.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: scaling capital can require larger trades relative to available market volume. The claim is correct, so the inverted verdict is False. |
| B | False (accurate) | Correct: larger participation rates can increase market impact and reduce realizable alpha. |
| C | True (incorrect) | Wrong: an unchanged formula does not keep net alpha per dollar constant at every asset level — trading costs and opportunity availability change nonlinearly with scale. |
| D | False (accurate) | Correct: capacity analysis should consider liquidity, turnover, execution horizon, and concentration of opportunities. |
| E | False (accurate) | Correct: a strategy can have genuine gross predictive value yet be economically unattractive after spreads, fees, slippage, and impact. |

**Reference:** Grinold & Kahn, *Active Portfolio Management*, 2nd ed., on transaction-cost modeling, capacity, and the gap between paper and realizable alpha; Balch ML4T week-9 on capacity and market impact.

### [QF2-D3G7Q3] Data-snooped formula vs. economically grounded signal
**Scenario:** A researcher searches thousands of obscure price-volume formulas and selects one with exceptional history but no plausible economic explanation. A simpler competitor, linked to delayed investor response, performs somewhat less in-sample but survives across markets and periods. The governance committee must choose which to develop.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: testing thousands of formulas increases the risk the selected result is a chance pattern. The claim is correct, so the inverted verdict is False. |
| B | False (accurate) | Correct: an economic rationale can guide tests of when and why an alpha should persist or fail — a mechanism supports falsifiable expectations. |
| C | True (incorrect) | Wrong: lack of an economic rationale does not mathematically prove the first signal has no predictive value — a pattern can be predictive without a known explanation (though governance concerns remain). |
| D | False (accurate) | Correct: stability across markets, periods, and reasonable specifications provides robustness evidence (harder to attribute to sample noise). |
| E | True (incorrect) | Wrong: the strongest in-sample backtest should not automatically override concerns about replication, multiple testing, and realizability — selection must account for overfitting, independent validation, costs, capacity, and feasibility. |

**Reference:** Kakushadze, "101 Formulaic Alphas" (2016), §1 (data mining, multiple testing, importance of economic grounding); Grinold & Kahn, *Active Portfolio Management*, 2nd ed., on out-of-sample validation and robustness; Balch ML4T week-9 on data snooping and replication.

## References (domain-level)

1. **Kakushadze, Z. (2016), "101 Formulaic Alphas"** (*Wilmott Magazine*; arXiv:1601.00991): §1 (overview, parsimony, data mining and multiple-testing cautions, crowding/decay of public alphas); §2 (alpha operators — rank, standardization/normalization, winsorization, neutralization, correlations among alphas); §3 (cross-sectional construction, dollar/market neutrality via construction rules); §4 (holding period, turnover, signal decay). Primary source for formulaic alpha construction, cross-sectional ranking/neutralization, and specification detail (signs, units, denominator handling).
2. **Grinold, R. & Kahn, R., *Active Portfolio Management*, 2nd ed.:** information analysis and the forecasting rule of thumb (alpha = expected residual/active return; refining raw signals by confidence/IC); the **information coefficient** (correlation of forecasts with outcomes) and **information horizon**; **active vs. absolute return** and benchmark-relative evaluation; **portfolio construction** mapping forecasts to weights under risk/tracking-error and exposure constraints; **factor neutralization** and residual (characteristic-neutral) alphas; **combining signals**, correlation, and risk decomposition; **breadth / effective breadth** and correlated bets (Fundamental Law); **transaction costs, turnover, and capacity** separating gross from realizable alpha; overfitting and multiple-testing caution.
3. **Balch, T. — ML4T lectures (Georgia Tech), week 9 (Alpha / signal research):** alpha signals and benchmark-relative return; time-series vs. cross-sectional signals; ranking, scaling (z-score), winsorization, and factor-exposure neutralization; constructing and specifying formulaic price-volume-volatility signals; data snooping / backtest overfitting and lookback optimization; signal decay, information-coefficient decay, holding period and turnover; combining alphas and weighting by information coefficient; crowding, capacity, market impact, and realizable alpha.
