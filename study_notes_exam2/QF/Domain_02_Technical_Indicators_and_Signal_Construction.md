# QF Domain 2 — Technical Indicators & Signal Construction

## Domain cheat-sheet

- **Moving averages (SMA vs. EMA) — window length is a lag/noise tradeoff.**
  - A **simple moving average (SMA)** of window *n* assigns **equal weight** (1/*n*) to every price currently inside the window. An **exponential moving average (EMA)** assigns **geometrically declining weight** to older observations, so recent prices contribute more.
  - A **shorter window reacts faster** (recent data is a larger share of the average) but is **noisier** and crosses thresholds more often; a **longer window smooths more** short-term variation but **reacts later** to a genuine, lasting change. Neither is universally "best" — it is a horizon/noise/cost/turnover tradeoff.
  - **Lag is intrinsic, not eliminable.** Every backward-looking average still reacts **after** prices change. A shorter window *reduces* lag; it does **not** "eliminate" it. EMA weighting changes sensitivity and effective memory but **cannot anticipate** a move before prices move — both SMA and EMA are computed from already-observed prices.
  - Changing the smoothing scheme (SMA→EMA) does **not** change the economic *meaning* (a summary of past prices) and does **not** guarantee a superior signal.
- **Momentum / rate-of-change (ROC).** Common definition: `momentum = P_t / P_{t−k} − 1` over a *k*-day lookback (e.g., $55/$50 − 1 = 10%).
  - **Positive momentum only means the price rose over the chosen lookback** — it is a *historical calculation*, not a forecast. Continuation is a separate, **probabilistic hypothesis** the calculation never proves.
  - **Endpoint-based ROC ignores the path**: two assets with the same start/end can show identical momentum despite very different trajectories, volatilities, and drawdowns.
  - **Rolling-window artifacts**: measured momentum can shift sharply when an **influential old observation leaves the window**, even if the current price barely moves. A single extreme move can dominate the measure.
  - **Lookback choice matters**: a different *k* can change the magnitude *or sign* of momentum; longer lookbacks keep more old trend data embedded and **delay** recognition that a trend has broken; shortening is **not** "always better" (faster detection trades against noise, turnover, false reversals).
- **Bollinger Bands (volatility-based).** Middle band = *n*-day moving average (location/central tendency); upper/lower bands = mean ± (multiplier × rolling standard deviation) (time-varying dispersion). Worked value: mean $100, σ $4, 2σ ⇒ upper band = $100 + 2($4) = **$108**; a $109 close is **$1 above** the upper band.
  - Band width is driven by **rolling volatility** at a fixed multiplier — **wider bands mean higher recent dispersion, not higher expected return**. Bands can widen while the mean barely moves.
  - A band touch/breach describes the **current relative position only** — it **does not** mathematically determine the next return. The same breach can be read as *mean-reversion* (expect pullback) or *breakout* (expect continuation); the interpretation is a **strategy hypothesis**, not arithmetic.
  - Volatility inputs are **backward-looking**, so bands adjust **after** a shock begins. In a persistent downtrend the mean and lower band drift **down together** — price can hug the lower band for a long time without reverting. A 2σ band does **not** make breaches impossible (even under a normal model, and financial returns are not normal).
- **Oscillators / relative strength (e.g., RSI-style, bounded 0–100).** Conventional labels: >70 "overbought," <30 "oversold."
  - **Thresholds are decision rules layered onto a continuous indicator** by the designer — they convert the indicator into categories/actions; they are not inherent truths.
  - **"Overbought" ≠ "will fall."** An oscillator can **stay above 70 through a long uptrend**; the label is an interpretation of past relative strength, not a deterministic reversal forecast. A **bounded indicator scale does not bound the asset's losses**.
  - **Confirmation rules** (wait for the oscillator to fall back below the threshold before entering) seek evidence that strength is weakening; they **enter later**, may miss part of a genuine reversal, and do **not** eliminate all false signals.
  - **Divergence** (price makes a new high while the oscillator does not) is a *possible warning*, not proof of a decline; different lookbacks produce different divergence patterns, and testing many definitions on one sample raises **data-mining risk**.
- **Normalization & comparability (percentage returns, z-scores, ranks).**
  - **Raw dollar changes are not comparable across price levels.** Dividing each change by its starting price gives a **percentage ROC** (a $20 stock +$2 = 10% beats a $400 stock +$8 = 2%); ranking by raw dollars spuriously favors high-priced names.
  - **Z-score** = (raw − mean) / standard deviation, standardizing against an asset's own history. Worked: (4−1)/1.5 = **2**; (8−6)/0.5 = **4** → the second is more unusual *relative to its own distribution* despite a lower-looking raw gap. Z-scores depend entirely on the **mean and σ estimates** used and do **not** remove nonstationarity/regime change — historical normalization can itself mislead when the distribution shifts.
  - **Rank/percentile transforms** are robust to scale and to extreme magnitudes (an outlier just gets the top rank) and support cross-sectional comparison, but **discard cardinal information**: ranks preserve *order*, not spacing, so very different magnitude spreads can produce identical orderings.
  - **Comparability improves measurement, not predictiveness.** Normalizing/ranking never *guarantees* positive expected returns or profitability.
- **Lookback windows, lag & overfitting.**
  - A rolling window replaces old data only as it advances, so after a regime change a long (e.g., 120-day) estimate stays near its old level for weeks — this is **a consequence of construction (smoothing), not a bug**. Shortening the window displaces old-regime data sooner but a short post-change sample can be **noisy/unrepresentative** — it does **not** guarantee an accurate new-regime estimate. Comparing multiple horizons helps reveal a transition.
  - **Parameter search overfits.** Scanning many lookbacks (e.g., 2–250 days) and picking the single best in-sample Sharpe creates **multiple-comparison/selection bias**; a **broad plateau** of similar performance is more trustworthy than a lone sharp optimum. Same formula ≠ immune to overfitting, so **out-of-sample evaluation is still required**. The economically appropriate lookback should match the **hypothesized lifetime/forecast horizon** of the information.
- **Combining indicators into a signal.**
  - **More indicators ≠ more information.** Indicators built from the same price trend (momentum, MA crossover, price/MA ratio) can be **highly correlated**; combining redundant signals adds little diversification — **independence matters more than count**.
  - **Conflicting indicators demand an explicit combination rule** (require agreement, weight them, let one filter the other). **Averaging raw values is arbitrary** unless scales, signs, and economic meanings are aligned (hence normalize first). Requiring confirmation reduces trades and can **miss single-indicator opportunities**.
  - A **hard zero-crossing threshold on a composite** can create high turnover from tiny score changes.
- **From indicator to strategy / look-ahead bias.**
  - An **indicator value is not a strategy.** A crossover, momentum reading, band touch, or composite score must be translated into explicit **entry/exit thresholds, position, sizing, holding period, and execution rules** before it is complete.
  - **Net ≠ gross.** Turnover, spreads, slippage, and market impact can turn a grossly profitable rule unprofitable; aggressive trading plus limited liquidity/capacity erodes the edge. Risk controls (stops, sizing, diversification) affect realized losses **separately** from how the indicator is calculated.
  - **Avoid look-ahead/in-sample contamination**: using the same history to both pick parameters (band multiplier, lookback) and judge performance overfits; a good backtest does **not** remove the need to model costs and sizing.

## Common traps

- **Inverted-polarity questions (10 of 21 here).** When the body says "each item asserts that its quoted statement is incorrect," the Answer Key verdict is flipped relative to the quoted claim's truth: **True = the quoted statement is wrong; False = the quoted statement is accurate.** Read the polarity line *first*. Inverted here: **G1Q1, G1Q2, G2Q3, G3Q1, G4Q1, G4Q2, G5Q2, G6Q1, G7Q1, G7Q2.** The remaining 11 are Normal (True = accurate).
- **"Shorter MA eliminates lag."** False — a shorter window *reduces* lag; every backward-looking average still reacts *after* prices move.
- **"EMA/weighting anticipates the move" or "guarantees a better signal."** False — EMA and SMA are both computed from observed prices; weighting changes sensitivity/memory, not the ability to predict, and never guarantees superiority.
- **"More stable indicator ⇒ more profitable."** False — stability alone determines nothing about forecasts, positions, costs, or P&L.
- **Momentum = forecast.** False — positive momentum only says the price rose over the lookback; continuation is a separate probabilistic assumption. Changing the lookback can flip the sign.
- **Endpoint ROC captures the path / equal momentum ⇒ equal risk.** False — endpoint comparison ignores the trajectory; identical cumulative moves can carry very different volatility/drawdown. A single extreme day can dominate, and the measure jumps when that day rolls out of the window.
- **"Shortening the lookback always improves the strategy."** False — faster detection is traded against noise sensitivity, turnover, and false reversals.
- **Band breach ⇒ next return known.** False — crossing the upper/lower band describes current relative position only; it does not determine the next move. Mean-reversion vs. breakout is a hypothesis choice.
- **Wider Bollinger Bands ⇒ higher expected return.** False — width reflects higher recent *volatility*, not expected return; bands can widen with the mean nearly unchanged.
- **"2σ band makes breaches impossible."** False — breaches remain possible even under a normal model, and returns need not be normal; in a downtrend price can ride the lower band as mean and band drift down.
- **"Overbought ⇒ price will fall" / bounded scale ⇒ bounded losses.** Both false — the oscillator can stay extreme through a persistent trend; a bounded indicator does not bound asset losses.
- **"Waiting for confirmation eliminates all false signals."** False — the oscillator can reverse briefly then resume; confirmation only enters later and reduces (not removes) false signals, possibly surrendering part of a real move.
- **Divergence ⇒ decline has begun.** False — divergence is a warning, not proof; lookback choice changes the pattern; testing many definitions mines noise.
- **Ranking by raw dollar change / "normalization guarantees profit."** False — compare percentage returns (or z-scores/ranks); normalization improves comparability, never predictiveness or profitability.
- **"Z-scoring removes nonstationarity/regime change."** False — z-scores depend on the mean/σ estimates and can mislead when the distribution shifts; it standardizes scale, not stationarity.
- **Ranks preserve magnitudes.** False — ranks preserve order, not spacing; identical orderings can hide very different raw spreads, and ranking discards cardinal information.
- **Slow adjustment of a long rolling window = software bug.** False — it is a construction consequence of smoothing; the window still holds many prior-regime points. A shorter window is faster but can be noisy/unrepresentative, not guaranteed accurate.
- **Picking the best in-sample lookback is deployable / "same formula ⇒ no overfit."** False — parameter search creates selection bias; out-of-sample validation is still required; prefer a broad performance plateau over a sharp optimum; match lookback to the information's hypothesized horizon.
- **More indicators ⇒ more diversification/information.** False — correlated, same-source indicators add little; independence matters more than count; averaging unaligned scales/signs is arbitrary.
- **Good gross backtest ⇒ deployable / costs irrelevant.** False — turnover, spreads, slippage, impact, capacity, sizing, and execution all govern net performance; an indicator is not a strategy until these are specified.

## Questions

### [QF2-D2G1Q1] 10-day vs. 100-day SMA — responsiveness, smoothing, lag
**Scenario:** An equity PM compares a 10-day SMA with a 100-day SMA for a trend overlay, wanting prompt reaction to turns without trading on every short-lived fluctuation. The quant team must explain the implications of the two windows.
**Answer polarity:** **Inverted (True = the quoted statement is INCORRECT; False = the quoted statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: the 10-day average responds faster — fewer historical observations let recent prices affect the average more quickly. |
| B | False (accurate) | Correct: the 100-day average smooths more short-term variation — the longer window spreads each short-term move across more observations. |
| C | True (incorrect) | Wrong: a shorter window *reduces* lag but does not *eliminate* it — any backward-looking average still reacts after prices change. |
| D | False (accurate) | Correct: increasing responsiveness also increases sensitivity to noise and turnover — faster indicators cross thresholds more often on temporary fluctuations. |
| E | True (incorrect) | Wrong: the 100-day average need not be more profitable — indicator stability alone does not determine forecasts, positions, costs, or profitability. |

**Reference:** Balch ML4T lecture 02-06 (Technical Analysis — moving averages, lag vs. smoothing); Project 6 (Indicator Evaluation). Standard TA: Murphy, *Technical Analysis of the Financial Markets* (moving-average windows and lag).

### [QF2-D2G1Q2] 20-day SMA vs. 20-day EMA — weighting and economic meaning
**Scenario:** A futures desk chooses between a 20-day SMA and a 20-day EMA. The head trader wants recent changes to matter more; the risk officer asks whether exponential weighting changes the indicator's economic meaning or guarantees a superior signal.
**Answer polarity:** **Inverted (True = the quoted statement is INCORRECT; False = the quoted statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: a conventional EMA assigns greater weight to more recent observations — contributions decline with age. |
| B | False (accurate) | Correct: a 20-day SMA assigns equal arithmetic weight to all prices currently inside its window. |
| C | False (accurate) | Correct: the EMA can react differently from the SMA at the same nominal window — different weighting produces different sensitivity and effective memory. |
| D | True (incorrect) | Wrong: exponential weighting does not guarantee crossovers occur before prices move — both measures are computed from observed prices and cannot anticipate a move from the weighting rule alone. |
| E | False (accurate) | Correct: neither method by itself establishes that a detected trend will continue — an average summarizes past prices; continuation is an added empirical assumption. |

**Reference:** Balch ML4T lecture 02-06 (Technical Analysis — SMA vs. EMA weighting). Standard TA: Murphy, *Technical Analysis of the Financial Markets* (exponential smoothing).

### [QF2-D2G1Q3] Moving-average crossover — is the crossover itself predictive?
**Scenario:** A family office buys an index when its 20-day MA crosses above its 80-day MA and sells on reversal. After a strong trending backtest, the committee asks whether the crossover alone proves the rule is predictive and deployable under a strict turnover budget.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The fast average rising above the slow average indicates recent prices are stronger on average than the longer-window history. |
| B | False | A crossover concerns the two averages; the current price need not be above both averages at the crossing time. |
| C | True | Small reversals around the averages in a range-bound market can repeatedly trigger opposing trades (whipsaws). |
| D | True | Turnover, spreads, slippage, and impact can consume the apparent gross edge, making a gross-profitable rule unprofitable net. |
| E | True | An indicator value does not alone specify holdings, risk exposure, or execution — it must be translated into explicit position/sizing/execution rules. |

**Reference:** Balch ML4T lecture 02-06 (Technical Analysis — crossovers) and Project 6 (Indicator Evaluation); Project 8 framing on indicator→strategy and net-of-cost performance. Standard TA: Murphy (MA crossover systems and whipsaws).

### [QF2-D2G2Q1] 20-day momentum — calculation vs. continuation
**Scenario:** A long-short team defines 20-day momentum as current price / price 20 days earlier − 1. A stock moved $50→$55; the PM wants to buy solely because momentum is positive. The risk lead asks the team to separate the calculation from the continuation assumption.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The rate of change is $55/$50 − 1 = 0.10 = 10%. |
| B | True | A current price above the comparison price yields a positive value — positive momentum means the price rose over the lookback. |
| C | False | Positive momentum does not guarantee a positive next-20-day return — continuation is a probabilistic hypothesis, not a consequence of the historical calculation. |
| D | True | A different starting date and price can change the magnitude or even the sign of measured momentum. |
| E | True | The indicator does not specify entry thresholds, sizing, holding period, or exits — a trading rule must still map momentum to a position. |

**Reference:** Balch ML4T lecture 02-06 (Technical Analysis — momentum / rate-of-change); Project 6 (Indicator Evaluation). Standard TA: Murphy (momentum and ROC indicators).

### [QF2-D2G2Q2] Endpoint momentum — path dependence and rolling windows
**Scenario:** A commodity fund ranks contracts by three-month momentum. One was flat then jumped 18% on day one of the window; another rose gradually to the same total return. The CIO asks whether the endpoint indicator distinguishes these paths and how it changes as the window rolls.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | An endpoint rate-of-change uses only beginning and ending prices, so it can assign the same momentum despite different paths. |
| B | True | When the 18% jump leaves the lookback window, the first contract's measured momentum can change sharply even if its current price barely moves. |
| C | False | Equal endpoint momentum does not prove equal volatility or drawdown — identical cumulative changes can come from paths with very different risk. |
| D | True | A single extreme move can dominate the cumulative return measured over the window. |
| E | False | A smoother historical path may raise confidence but cannot guarantee future momentum persistence. |

**Reference:** Balch ML4T lecture 02-06 (Technical Analysis — lookback/rolling-window behavior); Project 6 (Indicator Evaluation). Standard TA: Murphy (rate-of-change windows).

### [QF2-D2G2Q3] Momentum breakdown — lag of a backward-looking signal
**Scenario:** A momentum fund thrived in an orderly advance but suffered when a policy shock reversed leadership. The PM wants to hold all positions because they still have the highest trailing momentum. The risk committee evaluates how fast a backward-looking signal recognizes a breakdown.
**Answer polarity:** **Inverted (True = the quoted statement is INCORRECT; False = the quoted statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: a security can retain positive trailing momentum after price has begun to reverse — earlier gains keep the window's cumulative return positive during the initial reversal. |
| B | False (accurate) | Correct: longer lookbacks can delay recognition that a trend has broken — more historical trend data stays embedded in the longer-window statistic. |
| C | True (incorrect) | Wrong: shortening the lookback does not *always* improve the strategy — faster detection is traded against greater noise sensitivity, turnover, and false reversals. |
| D | False (accurate) | Correct: a market shock can turn recent winners into losers before trailing rankings fully adjust — momentum is backward-looking, so abrupt changes outpace its adjustment. |
| E | False (accurate) | Correct: stop, sizing, diversification, or complementary-signal rules can affect losses even though they do not change the original momentum calculation — risk controls govern exposure separately. |

**Reference:** Balch ML4T lecture 02-06 (Technical Analysis — indicator lag) and Project 6 (Indicator Evaluation); Project 8 on risk controls separate from signal construction. Standard TA: Murphy (lagging nature of trend indicators).

### [QF2-D2G3Q1] Bollinger Bands — construction and interpretation
**Scenario:** An asset manager builds 20-day Bollinger Bands at ±2 rolling σ. Today mean = $100, σ = $4, close = $109. The PM wants to short immediately because the close is above the upper band; the quant warns the interpretation depends on the strategy hypothesis.
**Answer polarity:** **Inverted (True = the quoted statement is INCORRECT; False = the quoted statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: the upper band is $100 + 2($4) = $108. |
| B | False (accurate) | Correct: the $109 close exceeds the $108 upper band by $1. |
| C | True (incorrect) | Wrong: closing above the upper band does not mathematically guarantee a negative next change — the threshold describes current relative position, not the next return. |
| D | False (accurate) | Correct: a mean-reversion strategy may read the breach differently from a breakout strategy — one expects reversal, the other treats it as trend continuation. |
| E | False (accurate) | Correct: the band combines a location estimate (moving average = central tendency) with a time-varying dispersion estimate (rolling standard deviation = variability). |

**Reference:** Balch ML4T lecture 02-06 (Technical Analysis — Bollinger Bands); Project 6 (Indicator Evaluation). Standard TA: Bollinger, *Bollinger on Bollinger Bands* (band construction and interpretation).

### [QF2-D2G3Q2] Band widening — volatility vs. expected return
**Scenario:** A dashboard shows the distance between an asset's upper and lower Bollinger Bands doubled during a shock. The CRO asks whether widening necessarily means expected return rose and whether comparisons with the prior quiet period remain straightforward.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | With the multiplier fixed, wider bands are consistent with a larger rolling standard deviation — distance from the mean is multiplier × rolling volatility. |
| B | True | Band widening can occur even if the rolling mean changes very little — dispersion can rise without a comparable shift in the average. |
| C | False | Wider bands do not prove higher expected return — band width estimates recent variability, not expected return. |
| D | True | A fixed dollar move is less extreme relative to the bands in a high-volatility period — larger dispersion makes it smaller in standardized terms. |
| E | True | Because volatility estimates are backward-looking, the bands adjust with some delay after the shock has already begun. |

**Reference:** Balch ML4T lecture 02-06 (Technical Analysis — volatility-based bands); Project 6 (Indicator Evaluation). Standard TA: Bollinger, *Bollinger on Bollinger Bands* (bandwidth and volatility).

### [QF2-D2G3Q3] Lower-band buy rule — downtrends and in-sample fitting
**Scenario:** A pension fund tests a rule that buys when price touches the lower Bollinger Band and exits at the moving average. It did well in a range-bound sample, but the committee worries about prolonged declines and using the same data to pick the multiplier and lookback.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Buying at the lower band embeds the assumption that sufficiently low relative prices tend to revert upward. |
| B | True | In a persistent downtrend, price can repeatedly touch or follow the lower band while the mean and bands drift down, without quickly reverting. |
| C | False | A two-standard-deviation band does not make breaches impossible — observations beyond 2σ remain possible even under a normal model, and returns need not be normal. |
| D | True | Choosing parameters for the best in-sample result can overfit noise and fail to generalize. |
| E | False | A successful band backtest does not remove the need to model transaction costs and position sizing — net performance and risk depend on how the signal becomes trades. |

**Reference:** Balch ML4T lecture 02-06 (Technical Analysis — Bollinger Bands) and Project 6 (Indicator Evaluation); Project 8 on overfitting and net-of-cost evaluation. Standard TA: Bollinger, *Bollinger on Bollinger Bands*.

### [QF2-D2G4Q1] Bounded oscillator — what 70/30 thresholds do and don't imply
**Scenario:** A desk uses a 0–100 oscillator, calling >70 overbought and <30 oversold. A client thinks the labels mean the desk can short every >70 and buy every <30 with near certainty. The PM asks research to clarify what the thresholds imply.
**Answer polarity:** **Inverted (True = the quoted statement is INCORRECT; False = the quoted statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: a bounded oscillator can remain above 70 while a strong uptrend persists — persistent gains keep a recent-strength measure elevated. |
| B | True (incorrect) | Wrong: "overbought" does not guarantee a negative next return — the label interprets past relative strength, not a deterministic reversal forecast. |
| C | False (accurate) | Correct: thresholds convert a continuous indicator into categories/actions chosen by the designer — the cutoffs are decision rules layered on the indicator. |
| D | False (accurate) | Correct: the usefulness of 70/30 should be evaluated for the asset, horizon, and implementation — a conventional threshold need not work equally across markets, regimes, or horizons. |
| E | True (incorrect) | Wrong: the indicator's bounded scale does not establish bounded asset losses — bounds on an indicator impose no bounds on the asset's return or strategy loss. |

**Reference:** Balch ML4T lecture 02-06 (Technical Analysis — oscillators / relative strength); Project 6 (Indicator Evaluation). Standard TA: Wilder, *New Concepts in Technical Trading Systems* (RSI and overbought/oversold thresholds).

### [QF2-D2G4Q2] Confirmation rule — waiting for the oscillator to exit the extreme
**Scenario:** A currency strategy uses a relative-strength oscillator for reversals. During a sustained appreciation it repeatedly enters overbought and each early short loses. The head trader considers requiring the oscillator to fall back below the threshold before entering, rather than shorting on the first crossing.
**Answer polarity:** **Inverted (True = the quoted statement is INCORRECT; False = the quoted statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: requiring a move back below the threshold seeks evidence that recent strength has started to weaken — the exit from the extreme indicates a change in the oscillator. |
| B | False (accurate) | Correct: the confirmation rule may enter later than shorting immediately on entering overbought — it necessarily waits for an additional indicator event. |
| C | True (incorrect) | Wrong: waiting for confirmation does not eliminate all false reversal signals — the oscillator can reverse briefly, then resume the prior trend. |
| D | False (accurate) | Correct: persistent trends are a risk for strategies that read oscillator extremes mechanically as reversals — extreme readings may reflect genuine strength, not exhaustion. |
| E | False (accurate) | Correct: a later entry can change both the opportunity captured and the risk incurred — delay avoids some premature trades but may surrender part of a genuine reversal. |

**Reference:** Balch ML4T lecture 02-06 (Technical Analysis — oscillator signals and confirmation); Project 6 (Indicator Evaluation). Standard TA: Wilder, *New Concepts in Technical Trading Systems* (RSI signal timing).

### [QF2-D2G4Q3] Bearish divergence — is it a complete strategy?
**Scenario:** A quant sees a stock make a new price high while its oscillator stays below its previous peak, calls it a bearish divergence, and recommends a full short. The CRO asks whether the divergence is a complete strategy and whether the conclusion follows mechanically.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The divergence indicates the oscillator measured less recent strength at the new high than at the earlier high — price and oscillator failed to confirm each other. |
| B | False | Divergence does not guarantee a sustained decline has begun — it is a possible warning, not proof of a future path. |
| C | True | Different oscillator lookbacks can produce different divergence patterns — the lookback determines which gains/losses contribute. |
| D | True | Entry timing, sizing, exit rules, and costs remain necessary even if the divergence carries predictive information. |
| E | True | Evaluating many divergence definitions on the same sample increases data-mining risk — selecting the best historical formulation can capitalize on noise. |

**Reference:** Balch ML4T lecture 02-06 (Technical Analysis — divergence) and Project 6 (Indicator Evaluation); Project 8 on data-mining risk and indicator→strategy. Standard TA: Wilder / Murphy (divergence analysis).

### [QF2-D2G5Q1] Percentage return vs. raw dollar change — comparability across price levels
**Scenario:** A cross-sectional strategy compares a $20 stock that gained $2 with a $400 stock that gained $8. The analyst ranks by raw dollar change and concludes the second has 4× the momentum. The PM wants a measure comparable across quoted price levels.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The returns are $2/$20 = 10% and $8/$400 = 2%. |
| B | True | Ranking by raw dollar change can favor high-priced securities even when their percentage performance is weaker — a larger base yields a larger dollar move from a smaller proportional change. |
| C | True | Dividing each dollar change by its starting price creates a percentage rate-of-change measure, expressing the change relative to the initial level. |
| D | False | Normalizing does not guarantee positive returns — comparability improves measurement but does not establish predictiveness or profitability. |
| E | True | Under percentage return the $20 stock (10%) ranks above the $400 stock (2%) in this example. |

**Reference:** Balch ML4T lecture 02-06 (Technical Analysis — normalization of indicators); Project 6 (Indicator Evaluation). Standard reference: percentage-return normalization in cross-sectional comparison (Grinold & Kahn, *Active Portfolio Management*, signal construction).

### [QF2-D2G5Q2] Z-scores — standardizing a signal across markets
**Scenario:** A global macro fund compares a signal across markets with different volatilities. Market one: raw 4, mean 1, σ 1.5. Market two: raw 8, mean 6, σ 0.5. The risk team proposes z-scores so allocation does not follow raw scale.
**Answer polarity:** **Inverted (True = the quoted statement is INCORRECT; False = the quoted statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: the first market's z-score is (4 − 1)/1.5 = 2. |
| B | False (accurate) | Correct: the second market's z-score is (8 − 6)/0.5 = 4. |
| C | False (accurate) | Correct: the second market is more unusual relative to its own distribution despite the first's lower raw value — four estimated standard deviations is more extreme than two under this scaling. |
| D | True (incorrect) | Wrong: z-scoring does not remove all effects of nonstationarity and regime change — historical normalization can itself mislead when the distribution changes. |
| E | False (accurate) | Correct: a z-score depends on the mean and standard-deviation estimates used — different estimation windows or samples change both inputs and therefore the score. |

**Reference:** Balch ML4T lecture 02-06 (Technical Analysis — normalization / z-scoring of indicators); Project 6 (Indicator Evaluation). Standard reference: Grinold & Kahn, *Active Portfolio Management* (standardizing signals; nonstationarity caveats).

### [QF2-D2G5Q3] Percentile ranks — robustness vs. lost information
**Scenario:** A market-neutral fund converts each day's continuous alpha indicator into cross-sectional percentile ranks before selecting the top/bottom deciles. The CIO likes rank robustness but asks what information is lost and whether ranks solve every comparability problem.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Ranking reduces the direct influence of an extreme magnitude beyond its position as largest/smallest — an outlier receives the top rank regardless of how far it lies above the next value. |
| B | False | Ranks do not preserve the exact numerical distance between pairs of raw signals — they preserve order, not original spacing. |
| C | True | Two days can share identical rank ordering even when the spreads between raw signal values differ greatly — many magnitude sets generate the same ordering. |
| D | True | Cross-sectional ranking supports comparison when raw scales differ but discards useful magnitude information — it trades cardinal information for scale robustness. |
| E | False | Ranking does not guarantee the top-decile securities have positive expected returns — a high relative value is not proof of positive predictive value. |

**Reference:** Balch ML4T lecture 02-06 (Technical Analysis — ranking/normalization); Project 6 (Indicator Evaluation). Standard reference: Grinold & Kahn, *Active Portfolio Management* (rank transforms vs. cardinal signals).

### [QF2-D2G6Q1] 5-day vs. 60-day — early reaction vs. signal stability
**Scenario:** A systematic fund tests 5-day and 60-day versions of the same indicator. The 5-day turns positive right after a short rally but reverses several times; the 60-day changes only after the rally persists. The committee must choose between early reaction and stability.
**Answer polarity:** **Inverted (True = the quoted statement is INCORRECT; False = the quoted statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: the 5-day version places greater emphasis on the most recent observations — recent data is a larger share of the shorter window. |
| B | False (accurate) | Correct: the 60-day version is likely to react later to an abrupt, lasting change — older observations dilute the initial effect of the new condition. |
| C | False (accurate) | Correct: the extra reversals in the 5-day signal may increase turnover — more frequent position changes generally require more trading. |
| D | True (incorrect) | Wrong: the 60-day indicator can still generate false signals despite being smoother — smoothing reduces noise but cannot ensure every detected trend persists. |
| E | False (accurate) | Correct: window selection creates a tradeoff rather than a universally best horizon — the right balance depends on signal horizon, noise, costs, and objectives. |

**Reference:** Balch ML4T lecture 02-06 (Technical Analysis — lookback windows, lag, responsiveness); Project 6 (Indicator Evaluation). Standard TA: Murphy (window length tradeoffs).

### [QF2-D2G6Q2] 120-day rolling window — slow adjustment after a regime change
**Scenario:** A risk-controlled strategy uses a 120-day rolling indicator. After a sudden regime change it stays near its prior level for weeks though recent observations look very different. The CRO asks whether the slow adjustment is a software error or a construction consequence.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The window still contains many observations from the prior regime — a rolling 120-day calculation replaces old data only as the window advances. |
| B | True | The delayed reaction can be an intended consequence of smoothing, not an implementation bug — stability comes partly from limiting the influence of a few recent points. |
| C | True | Shortening the window would make old-regime observations leave the calculation sooner — fewer observations displace the prior sample faster. |
| D | False | A shorter window does not guarantee an accurate estimate of the new regime — a short post-change sample may be noisy or unrepresentative. |
| E | True | Comparing multiple horizons can reveal disagreement between recent and longer-term conditions, helping identify a transition. |

**Reference:** Balch ML4T lecture 02-06 (Technical Analysis — rolling-window lag); Project 6 (Indicator Evaluation). Standard TA: Murphy (rolling-statistic adjustment).

### [QF2-D2G6Q3] Lookback optimization — overfitting and out-of-sample evidence
**Scenario:** A researcher tests every lookback from 2 to 250 days and reports 37 days gave the highest in-sample Sharpe. The PM wants to deploy that exact value; model governance requires evidence that the performance is not an isolated historical accident.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Searching many lookbacks increases the chance one parameter looks strong due to noise — parameter search creates multiple-comparison and selection effects. |
| B | True | A broad region of similar performance around 37 days can give more confidence than a single sharp optimum, all else equal — local robustness is less dependent on one fitted value. |
| C | False | Out-of-sample evaluation is not unnecessary — parameter selection can overfit even when the underlying formula is unchanged. |
| D | True | Transaction costs can vary with lookback because shorter-horizon versions change positions more frequently, raising turnover and expense. |
| E | True | The economically appropriate lookback should relate to the hypothesized lifetime of the information — the measurement horizon should match the signal's mechanism and forecast horizon. |

**Reference:** Balch ML4T lecture 02-06 (Technical Analysis — parameter choice) and Project 6 (Indicator Evaluation); Project 8 on overfitting and out-of-sample validation. Standard reference: Bailey et al. on backtest overfitting / multiple comparisons.

### [QF2-D2G7Q1] Three price-trend indicators — correlation vs. independent information
**Scenario:** A team combines momentum, moving-average crossover, and a price-to-moving-average ratio into one strategy. The head trader assumes three indicators provide three independent sources of information.
**Answer polarity:** **Inverted (True = the quoted statement is INCORRECT; False = the quoted statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: the indicators may be highly correlated because they are all derived from price trends — all three may capture similar trend information. |
| B | True (incorrect) | Wrong: combining redundant indicators does not necessarily increase diversification — redundancy provides limited incremental information. |
| C | False (accurate) | Correct: conflicting indicators require a rule for how the final trading signal is formed — the strategy must specify how signals interact. |
| D | False (accurate) | Correct: a useful indicator can still produce an unprofitable strategy after costs — trading costs and implementation can eliminate the edge. |
| E | False (accurate) | Correct: indicator count alone does not determine information diversity — independence matters more than raw count. |

**Reference:** Balch ML4T lecture 02-06 (Technical Analysis — combining indicators); Project 6 (Indicator Evaluation). Standard reference: Grinold & Kahn, *Active Portfolio Management* (information from correlated signals; breadth vs. redundancy).

### [QF2-D2G7Q2] Momentum vs. mean-reversion conflict — resolving into one signal
**Scenario:** An asset manager combines a momentum signal and a mean-reversion oscillator. Momentum says long; the oscillator labels the asset overbought and says short. The PM asks the quant team to resolve the conflict while keeping the strategy transparent for model governance.
**Answer polarity:** **Inverted (True = the quoted statement is INCORRECT; False = the quoted statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: the conflict can arise because the indicators encode different hypotheses about continuation and reversal — one extrapolates strength, the other treats an extreme as a possible reversal. |
| B | True (incorrect) | Wrong: averaging the two raw values is not meaningful without checking scales or directions — unaligned scales, signs, and economic meanings make a raw average arbitrary. |
| C | False (accurate) | Correct: a decision rule could require agreement, assign weights, or let one indicator filter the other — these are distinct, testable ways to map multiple inputs into one position. |
| D | False (accurate) | Correct: requiring confirmation may reduce the number of trades and can also cause the strategy to miss opportunities seen by only one indicator — greater selectivity trades breadth for agreement. |
| E | False (accurate) | Correct: transparency about conflict resolution is part of specifying the strategy, not merely documenting the indicators — a deployable system must define how every signal state becomes an action. |

**Reference:** Balch ML4T lecture 02-06 (Technical Analysis — combining conflicting indicators); Project 6 (Indicator Evaluation); Project 8 on indicator→strategy specification. Standard reference: Grinold & Kahn, *Active Portfolio Management* (signal combination rules).

### [QF2-D2G7Q3] Composite score — indicator quality vs. implementable strategy
**Scenario:** A desk builds a composite from a normalized trend signal, a volume-confirmation signal, and a volatility filter. The gross backtest looks attractive, but it trades aggressively whenever the score crosses zero. The COO asks whether indicator quality alone justifies deployment under capacity and cost constraints.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Normalizing component signals can prevent one component from dominating solely because of numerical scale — scale alignment makes weights more interpretable. |
| B | True | A volume signal may add information distinct from price trend, but its incremental value must be tested rather than assumed — correlation and forecasting evidence determine complementarity. |
| C | True | Frequent movement around the zero threshold can create high turnover even when the composite changes only slightly — a hard zero cutoff repeatedly reverses the prescribed trade on small sign changes. |
| D | False | Strong gross returns do not guarantee spreads, slippage, and impact are unimportant — aggressive trading and limited liquidity can materially reduce or eliminate gross performance. |
| E | True | Position sizing, execution rules, risk limits, and net-of-cost validation are required to turn the composite indicator into an implementable strategy — a predictive score is only one component. |

**Reference:** Balch ML4T lecture 02-06 (Technical Analysis — composite signals) and Project 6 (Indicator Evaluation); Project 8 on net-of-cost evaluation, capacity, and execution. Standard reference: Grinold & Kahn, *Active Portfolio Management* (gross vs. realizable performance).

## References (domain-level)

1. **Balch — ML4T lecture 02-06 (Technical Analysis):** moving averages (SMA vs. EMA; equal vs. exponential weighting; window length as a lag/smoothing tradeoff), momentum / rate-of-change, Bollinger Bands (location + rolling-volatility bands, bandwidth), oscillators / relative strength (overbought/oversold thresholds, confirmation, divergence), normalization and z-scoring of indicators, lookback windows / lag / responsiveness, and combining indicators into signals.
2. **Balch — ML4T Project 6 (Indicator Evaluation):** constructing and evaluating technical indicators (price/SMA ratio, Bollinger Band %, momentum, etc.); separating an indicator's calculation from any continuation/forecast claim; the distinction between an indicator value and an implementable rule.
3. **Balch — ML4T Project 8 (Strategy Evaluation) framing:** translating indicators into explicit position/sizing/execution rules, modeling transaction costs (commissions, impact), avoiding in-sample parameter overfitting, and net-of-cost (realizable) vs. gross performance.
4. **Standard technical-analysis references (section level, not page-specific):**
   - Bollinger, *Bollinger on Bollinger Bands* — band construction (mean ± multiplier × rolling σ), bandwidth as volatility, and mean-reversion vs. breakout interpretation (G3 questions).
   - Wilder, *New Concepts in Technical Trading Systems* — RSI and bounded oscillators, overbought/oversold thresholds, and signal timing (G4 questions).
   - Murphy, *Technical Analysis of the Financial Markets* — moving-average systems and crossovers, momentum/ROC, lagging nature of trend indicators, and window-length tradeoffs (G1, G2, G6).
5. **Signal-construction / normalization (for G5, G7):** Grinold & Kahn, *Active Portfolio Management* — standardizing and ranking signals, combining correlated vs. independent signals (breadth vs. redundancy), and gross vs. realizable alpha. Used only to characterize normalization and signal-combination theory, not the TA indicators themselves.
6. **Backtest-overfitting caveat (for G6Q3):** Bailey, Borwein, López de Prado & Zhu, "The Probability of Backtest Overfitting" — multiple-comparison/selection bias from scanning many parameters and the need for out-of-sample evidence.

<!-- Source note: slices/QF2_D02.txt is a PDF text extraction containing ligature artifacts (ﬂ→fl, ﬁ→fi): e.g. "ﬂuctuation"→fluctuation, "proﬁtable"→profitable, "inﬂuence"→influence, "beneﬁt"→benefit, "conﬁrmation"→confirmation, "diversiﬁcation"→diversification, "deﬁnition"→definition, "signiﬁcant"→significant. Page numbers (606–620) and "Rev:081020261230" footers are PDF artifacts, not question content. All verdicts above are copied verbatim from the slice Answer Keys; no verdict was flipped. -->
