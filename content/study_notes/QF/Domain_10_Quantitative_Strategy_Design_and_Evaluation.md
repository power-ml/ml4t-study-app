# QF Domain 10 — Quantitative Strategy Design and Evaluation

## Domain cheat-sheet

- **Investment hypothesis, not just correlation.** A defensible hypothesis names a *plausible economic mechanism* (why the signal predicts returns) and the *conditions* under which it should hold, weaken, or reverse. Correlation alone can come from confounding, reverse causality, data leakage, or chance — and searching many arbitrary partitions (ticker-letter groups, etc.) guarantees some spurious "winner" by multiple testing.
- **Signal design & falsifiability.** Translate an idea into a measurable feature (e.g., a past-return lookback for continuation) without picking the lookback that maximized full-sample performance (overfitting). Corroborating variables (volume, fund flows) and pre-specified conditional predictions (liquid vs. illiquid behavior) make the hypothesis *more* falsifiable, not less.
- **Forecast ≠ trade.** The *sign* of a forecast sets direction, but whether to trade depends on **magnitude vs. cost, confidence/uncertainty, risk, and portfolio constraints**. A no-trade threshold reserves capital for signals whose expected *net* edge clears costs. An accurate forecast can still lose money; a positive forecast never *guarantees* profit.
- **Directional accuracy is not P&L.** A 60% hit rate can coexist with a *negative* average return if the wrong calls land on the big moves. Return-weighted objectives capture economic magnitude that classification accuracy discards.
- **Position construction is a separate design problem.** Raw forecast-proportional sizing concentrates risk in high-magnitude / volatile / illiquid names; **volatility scaling** equalizes risk per position, and liquidity/position limits can override an unconstrained signal. **Dollar neutrality ≠ risk neutrality** — equal long/short dollars can still carry beta, sector, factor, and concentration exposures.
- **Backtesting & benchmarks.** Pick a *relevant opportunity-cost* benchmark (the investable index for a long-only equity mandate), not just cash. In-sample = any data used to specify or tune the strategy; a credible **out-of-sample** test freezes the design and runs it on untouched *later* data. **Walk-forward** repeatedly trains on the past and evaluates on subsequent windows while preserving time order. Repeatedly retuning after seeing "holdout" results silently pulls that data back into development.
- **Performance attribution.** Beating the market can come from a static tilt (e.g., persistent tech overweight in a tech rally), not skillful timing. Exposure-matched benchmarks, average-weight counterfactuals, and factor regressions separate genuine timing/selection alpha from compensation for systematic exposures.
- **Turnover, costs, net alpha.** Deploy on **net**, not gross, performance. Small statistically-significant edges can be entirely consumed by spreads, commissions, and market impact at high turnover. Costs scale with dollars traded (turnover × AUM × cost rate) and are *not* constant — they vary with order size, liquidity, volatility, and execution conditions. Reducing turnover (no-trade bands) can improve net returns even if gross accuracy dips slightly.
- **Capacity, liquidity, crowding.** Percentage returns don't survive scaling: larger orders walk the book and add market impact, so a profitable small strategy may not scale. Net edge falls as impact rises with size (0.40% → 0.20% → −0.20% in the worked example). Participation-rate/ADV limits, spreading trades (impact vs. delay/price risk), and **crowding** (correlated positions across independent funds, worst exit liquidity precisely when everyone unwinds) all cap capacity. Maximizing AUM ≠ maximizing net performance.
- **Leverage & exposure.** Leverage magnifies **both** gains and losses (3:1 → a 2% portfolio move is ~6% of equity either way). Financing is neither free nor guaranteed; adverse moves trigger margin calls / forced deleveraging even if the thesis is right. Gross exposure = long + short (600% of equity in the worked case); net-dollar-neutral portfolios can still take big losses when longs fall and shorts rise. Net dollars miss sector/beta/factor/liquidity/concentration risk.
- **Risk controls.** A fixed % stop-loss does not guarantee the exit price (gaps/illiquidity), hits volatile assets differently, and can whipsaw (crystallize a loss right before recovery). Controls tuned to normal conditions may misbehave in gaps/illiquidity/correlated stress. Position sizing and portfolio-level limits *complement* (not replace) stops.
- **Robustness, degradation, live deployment.** Regime shifts change both feature distributions and the feature→return relationship; retraining on recent data is *not* a guaranteed fix and may be the wrong response if the economic mechanism is gone (consider recalibration, redesign, or retirement). Backtest success ≠ production success — implementation assumptions (close-price fills), data quality, broker/order-pipeline failures, and timing separate live from theoretical results. Monitor distributions/residuals, IC, turnover, slippage; use paper trading / staged rollout; compare fills to prices *actually attainable after the decision time*. Retirement decisions should weigh statistical uncertainty, implementation quality, current conditions, and whether the thesis still holds — no single metric or one unlucky week decides it.

## Common traps

- **No inverted-logic questions in this domain.** Every question here uses a standard per-choice Answer Key ("A. False – …", "B. True – …"), i.e., **Normal polarity throughout (True = accurate).** There is no "Answer Key (True = incorrect; False = accurate)" header on any D10 item. Do not invent inversion — grade each statement on its literal truth.
- **"The statement reverses the correct conclusion" negation traps (pervasive).** Many *False* choices are the correct idea stated backwards, so they read plausibly. Examples flagged in the key: G1Q2A/E, G2Q1B/C, G2Q2D, G2Q3B/E, G3Q1D, G3Q2A/D, G4Q1A/C, G5Q1B, G5Q2A, G5Q3C, G6Q1E, G6Q2D, G6Q3C/E, G7Q1A, G7Q2A/D. Always read the sentence's literal claim, decide the true statement, then check whether the choice matches or *flips* it.
- **Double-negative "embedded claim" choices ("A reviewer would be wrong to accept the claim that …").** The inner claim is *accurate*, so "would be wrong to accept it" is **False**. Appears at **G4Q3E** (impact + spreads should be included when material — accept it) and **G6Q1B** (a 2% loss at 3:1 is ~6% of equity — accept it). Parse the inner claim, judge its truth, then negate.
- **"Necessarily / always / guarantees / cannot" absolutes are almost always False.** Statistical significance ⇏ net profitability (G1Q1E); a positive forecast ⇏ guaranteed profit (G2Q1E); accuracy ⇏ profitability (G2Q2A); dollar neutrality ⇏ neutral to all factors (G2Q3D); strong in-sample ⇏ future performance (G3Q2C); faster reaction ⇏ superior (G4Q3C); more AUM ⇏ more profit (G5Q2E); zero net dollars ⇏ no large loss (G6Q2C); a stop ⇏ exact fill (G6Q3A); retraining ⇏ restored performance (G7Q1B).
- **Arithmetic checks matter.** Several choices hinge on a computation: net edge = gross − cost (G4Q2, G4Q3, G5Q2), turnover × AUM × rate = dollar cost (G4Q2), leverage math (G6Q1A, G6Q2B), 12% − 14% = −2 pp underperformance (G3Q1C). Do the math; a plausible-sounding sign or figure is often the wrong one.
- **Gross vs. net, correlation vs. mechanism, accuracy vs. P&L, dollar-neutral vs. risk-neutral** are the four recurring conceptual confusions — most wrong choices collapse one of these distinctions.

## Questions

### [QF-D10G1Q1] Social-media mentions — correlation vs. defensible hypothesis
**Scenario:** A quant team finds high social-media-mention stocks outperform the next day. The PM wants an economic explanation plus evidence the data was available before trading before approving a strategy.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Observed correlation does not prove causation — it can arise from confounding variables, reverse causality, data leakage (look-ahead), or pure chance. |
| B | True | A useful investment hypothesis identifies a plausible mechanism (why mentions might move prices) and the conditions under which the effect should weaken or reverse. |
| C | True | Testing whether the effect survives controls for news, liquidity, and recent returns checks whether a known alternative influence better explains the relationship. |
| D | True | Freezing the signal definition and trading rule *before* validating on an untouched sample reduces selection/tuning bias on the evaluation data. |
| E | False | Statistical significance establishes neither sufficient economic magnitude nor net-of-cost profitability; a real, significant edge can still be uneconomic after costs. |

**Reference:** Correlation vs. causation and multiple-testing/leakage in strategy research — Lopez de Prado, *Advances in Financial ML* (backtesting pitfalls); Investopedia "Backtesting" and "Data mining bias."

### [QF-D10G1Q2] Institutional-demand continuation — translating an idea into a signal
**Scenario:** A manager believes slow institutional demand creates medium-term continuation. The research director wants the idea turned into a measurable signal without simply choosing whichever lookback backtested best.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Reverses the correct conclusion: a defined past-return feature over a stated lookback *is* one valid operationalization of the direction of a continuation effect. |
| B | False | Continuation implies stronger recent performance maps toward a *more positive* forecast/position, not a more negative one. |
| C | True | Volume or fund-flow measures can provide corroborating evidence that persistent institutional demand is actually present (supports the mechanism). |
| D | True | Choosing the lookback solely because it maximizes full-sample performance capitalizes on sample-specific noise — classic overfitting. |
| E | False | Reverses the correct conclusion: pre-specifying expected liquid-vs-illiquid behavior creates conditional predictions that make the hypothesis *more* falsifiable. |

**Reference:** Overfitting from parameter search and falsifiable, mechanism-driven signals — Lopez de Prado, *Advances in Financial ML* (selection bias under multiple testing); Investopedia "Overfitting."

### [QF-D10G1Q3] Ticker-letter partition — chance patterns vs. rationale
**Scenario:** A researcher reports A–M firms beat N–Z firms in one sample. The CIO funds further work only if the team can explain the effect and show it is not a chance partition.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | A partition that merely splits firms into two groups is not an investment hypothesis; a measurable correlation is not by itself a defensible explanation of expected returns. |
| B | True | Searching many arbitrary partitions produces apparently strong results by chance — the multiple-testing / data-snooping problem. |
| C | True | Stability across different time periods (temporal replication) is more persuasive than performance confined to the discovery sample. |
| D | True | A plausible economic channel supports conditional predictions and helps distinguish genuine signal from coincidence. |
| E | False | Leverage magnifies exposure; it creates no evidence that a signal without economic rationale is genuine — it is not a substitute for validation. |

**Reference:** Data-snooping / multiple-testing bias and the deflated Sharpe ratio — Lopez de Prado, *Advances in Financial ML* (deflated Sharpe, backtest overfitting); Investopedia "Data mining bias."

### [QF-D10G2Q1] Three forecasts vs. round-trip cost — forecast is not a trade
**Scenario:** A model predicts +0.04%, +0.01%, −0.03% next-day returns for three stocks with an estimated 0.02% round-trip cost each. The trader asks whether every nonzero forecast should become a trade.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | A forecast's sign helps set direction, but the decision to trade also depends on magnitude, confidence, costs, risk, and portfolio constraints. |
| B | False | Reverses the correct conclusion: the +0.01% expected gross edge *is* smaller than the 0.02% round-trip cost, so it does not clear costs. |
| C | False | Reverses the correct conclusion: a no-trade threshold *can* prevent sub-cost forecasts from generating positions by reserving trades for sufficient expected net value. |
| D | True | Both forecast magnitude and its uncertainty are valid inputs to position sizing — larger, more reliable forecasts can justify more exposure. |
| E | False | A forecast is uncertain; realized returns can differ from predictions, so a positive forecast does not guarantee a profit. |

**Reference:** Net-edge thresholds and cost-aware sizing — Grinold & Kahn, *Active Portfolio Management* (signal-to-trade, forecasting); Investopedia "Transaction costs."

### [QF-D10G2Q2] 60% hit rate — directional accuracy vs. P&L
**Scenario:** A classifier calls market up/down correctly on 60% of days, but its correct calls cluster on tiny moves while several wrong calls coincide with large declines.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Directional accuracy treats small and large outcomes alike and ignores costs and sizing, so it is not sufficient to establish profitability. |
| B | True | Trading P&L depends on the signed size of each realized outcome, not merely the count of correct calls. |
| C | True | A 60% hit rate can coexist with a negative average return when a few large losses outweigh many small gains. |
| D | False | Reverses the correct conclusion: sizing that ignores confidence and downside exposure *can* worsen the large-error problem by over-allocating to uncertain, high-consequence calls. |
| E | True | A return-weighted objective reflects economic magnitude more directly than hit rate, capturing information classification accuracy omits. |

**Reference:** Return-weighted vs. accuracy objectives — Lopez de Prado, *Advances in Financial ML* (labeling, meta-labeling, sample weights); Investopedia "Win rate vs. risk/reward."

### [QF-D10G2Q3] Forecast-proportional sizing — position construction risk
**Scenario:** A market-neutral fund sizes positions proportional to predicted return, but the model keeps assigning its biggest positions to volatile, thinly traded stocks. The risk manager wants a safer construction rule.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Raw forecast-proportional sizing mechanically gives large weights to large-magnitude forecasts, concentrating risk unless additional controls intervene. |
| B | False | Reverses the correct conclusion: scaling forecasts by volatility *does* help — it lowers the allocation to a high-risk security for a given forecast, equalizing risk across names. |
| C | True | Liquidity and position limits can constrain trades even when a forecast is strong (tradability/concentration override the raw signal). |
| D | False | Dollar neutrality (equal long/short dollars) does not guarantee neutrality to beta, sector, style, or other factor exposures. |
| E | False | Reverses the correct conclusion: converting forecasts into portfolio weights *is* a distinct design problem — construction must turn predictions into feasible, risk-controlled actions. |

**Reference:** Volatility scaling, risk-based position construction, and residual factor exposure — Grinold & Kahn, *Active Portfolio Management* (portfolio construction, risk models); Investopedia "Market-neutral strategy."

### [QF-D10G3Q1] Long-only vs. investable index — benchmark selection
**Scenario:** A long-only U.S. equity model earned 12% while its investable index earned 14%. The committee wants the strategy compared with meaningful alternatives before any success claim.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | A zero-return cash benchmark is insufficient — beating cash may just reward taking equity-market risk during a rising market. |
| B | True | The investable index is a plausible opportunity-cost benchmark: it is the passive exposure actually available to a long-only U.S. equity mandate. |
| C | True | Arithmetic: 12% − 14% = −2 percentage points per year, so the strategy underperformed the index before further risk adjustment. |
| D | False | Reverses the correct conclusion: differences in beta, sector, risk, costs, and constraints *do* matter — raw return alone does not explain *why* the strategy differed from its benchmark. |
| E | True | Comparing with a simple/naive alternative tests whether the added model complexity delivers incremental value worth its cost. |

**Reference:** Benchmark/opportunity-cost selection and performance attribution — CFA curriculum (performance evaluation, benchmark quality); Grinold & Kahn, *Active Portfolio Management* (benchmarks, residual return).

### [QF-D10G3Q2] Tune-and-report on same years — in-sample vs. out-of-sample
**Scenario:** A researcher tunes a strategy on 2010–2022 and reports on those same years. The head of research wants evidence it could survive live deployment starting in 2023.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Reverses the correct conclusion: the 2010–2022 result *is* in-sample precisely because that data helped determine the final strategy — data used for specification/tuning is part of the development sample. |
| B | True | Testing the frozen strategy on later, untouched data better approximates prospective use of the fixed rule (a credible out-of-sample assessment). |
| C | False | Strong in-sample performance guarantees nothing after 2022 — the strategy may be overfit or the return-generating process may change. |
| D | False | Reverses the correct conclusion: walk-forward *can* repeatedly train on past data and evaluate on subsequent periods while preserving temporal order — each evaluation window follows the fitting information. |
| E | True | Retuning after observing each out-of-sample result eventually folds those observations into development, eroding the holdout's independence. |

**Reference:** In-sample/out-of-sample discipline and walk-forward analysis — Investopedia "In-sample vs. out-of-sample," "Walk-forward optimization"; Lopez de Prado, *Advances in Financial ML* (cross-validation in finance, purging/embargo).

### [QF-D10G3Q3] Sector-rotation with a persistent tilt — attribution
**Scenario:** A sector-rotation strategy beats the market but held a persistent tech overweight during a tech-led rally. The client wants to know how much return came from timing vs. static exposure.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Broad-market outperformance alone does not prove rotation added alpha — a persistent sector tilt can explain the result without successful timing. |
| B | True | A sector- or exposure-matched benchmark creates a more informative counterfactual for attribution. |
| C | True | Comparing against a fixed portfolio holding the strategy's *average* sector weights isolates the value of dynamic timing from the average allocation. |
| D | True | Factor regression can reveal that known systematic exposures explain part of the excess return (compensation for risk, not unique skill). |
| E | False | A positive total return does not make attribution unnecessary — investors need to know which exposures produced returns and whether they match the intended process. |

**Reference:** Return attribution, factor regression, and exposure-matched benchmarks — Grinold & Kahn, *Active Portfolio Management* (attribution, factor models); CFA curriculum (performance attribution).

### [QF-D10G4Q1] Small edge at high turnover — gross vs. net
**Scenario:** A model with a small, statistically significant edge trades every few minutes, earning 8% annually before costs; estimated spreads, commissions, and impact total ~10% annually at that turnover.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Reverses the correct conclusion: the strategy *is* profitable on a gross basis — 8% before costs is positive. |
| B | False | It is not profitable on a net basis: estimated 10% costs exceed the 8% gross return. |
| C | False | Reverses the correct conclusion: high turnover *can* make a statistically useful signal economically unviable — small edges get consumed by implementation costs. |
| D | True | Deployment decisions must be based on net, not gross, performance. |
| E | True | Reducing turnover can improve net economics even if gross predictive accuracy falls slightly. |

**Reference:** Turnover, transaction-cost realism, and gross-vs-net alpha — Investopedia "Transaction costs," "Turnover ratio"; Grinold & Kahn, *Active Portfolio Management* (cost of trading, net alpha).

### [QF-D10G4Q2] $10M at 40% daily turnover — first-order cost estimate
**Scenario:** A daily strategy manages $10M and turns over 40% of value daily (turnover = dollars traded ÷ portfolio value), with an average one-way cost of 0.10% of dollars traded.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | 40% × $10M = $4M traded per day under the stated turnover definition. |
| B | True | 0.10% × $4M = $4,000 estimated daily trading cost. |
| C | False | $3,000 gross profit − $4,000 cost = a $1,000 estimated daily net loss, so it is not profitable after costs. |
| D | True | A turnover-aware position rule (less unnecessary rebalancing) can cut implementation drag separately from the forecast model. |
| E | False | The 0.10% rate need not stay constant — spreads and market impact vary with order size, liquidity, volatility, and execution conditions. |

**Reference:** Turnover-to-cost arithmetic and variable market impact — Investopedia "Transaction costs," "Market impact"; Lopez de Prado, *Advances in Financial ML* (transaction-cost modeling).

### [QF-D10G4Q3] Two signal versions — net return and no-trade bands
**Scenario:** Two versions of a signal have identical 9% gross returns; Version A costs ~2% annually and Version B costs ~6%. The PM prefers B because it reacts faster to every forecast change.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | 9% gross − 2% cost = 7% net for Version A (before other fees). |
| B | True | 9% gross − 6% cost = 3% net for Version B (before other fees). |
| C | False | Faster reaction does not make B superior — its higher implementation cost leaves it with lower estimated net performance. |
| D | False | Reverses the correct conclusion: a no-trade band *can* reduce turnover by leaving small target-weight changes unexecuted, avoiding costs that exceed their benefit. |
| E | False | Double-negative embedded claim: the inner claim — that cost estimates should include market impact as well as explicit commissions when material — is correct and should be accepted, so "a reviewer would be wrong to accept it" is false. Impact/spread can dominate explicit fees. |

**Reference:** Net-return arithmetic, no-trade bands, and full-cost accounting (impact + spread + commissions) — Grinold & Kahn, *Active Portfolio Management* (rebalancing, cost control); Investopedia "Transaction costs," "Bid-ask spread."

### [QF-D10G5Q1] $5M to $500M in small caps — capacity and impact
**Scenario:** A strategy earned strong returns at $5M in small-cap stocks; an investor wants $500M, but the head trader warns many positions would be a large fraction of average daily volume.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Percentage returns at $5M need not survive at $500M — scaling can worsen execution and prevent obtaining historical positions at observed prices. |
| B | False | Reverses the correct conclusion: larger orders *can* consume available depth and create greater market impact, walking the order book. |
| C | True | Participation-rate or average-daily-volume limits can constrain feasible position changes to a manageable share of liquidity. |
| D | True | Spreading trades over time may cut immediate impact but introduces delay and price risk (prices can move before completion). |
| E | True | Capacity analysis must account for how the strategy's own trading moves execution prices — a scalable backtest cannot assume unlimited fills at unaffected historical prices. |

**Reference:** Capacity, market depth, and impact from own trading — Investopedia "Market impact," "Liquidity"; Lopez de Prado, *Advances in Financial ML* (strategy capacity).

### [QF-D10G5Q2] Rising impact vs. size — capacity and net edge
**Scenario:** A relative-value strategy has a 0.50% gross edge per trade; estimated round-trip impact is 0.10% at $1M, 0.30% at $5M, and 0.70% at $10M. The PM asks whether more capital always means proportionally more profit.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Reverses the correct conclusion: at $1M the net edge *is* 0.40% (0.50% − 0.10%), so "not 0.40%" is false. |
| B | True | At $5M, net edge = 0.50% − 0.30% = 0.20% before other costs. |
| C | False | At $10M, net edge = 0.50% − 0.70% = −0.20% before other costs — negative, not positive. |
| D | True | Rising impact consumes an increasing share of the fixed gross opportunity, so percentage return can decline as size grows. |
| E | False | Maximizing AUM and maximizing net performance are not the same objective — added capital can reduce returns/profits once capacity constraints bind. |

**Reference:** Return degradation with size and the capacity/AUM tradeoff — Lopez de Prado, *Advances in Financial ML* (capacity); Investopedia "Market impact," "Diseconomies of scale in funds."

### [QF-D10G5Q3] Crowding and correlated exits — shared signals
**Scenario:** Several funds start trading similar signals in the same securities; the CRO sees faster price adjustment, crowded entries, and sharp losses when many funds try to exit at once.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Crowding/competition can pull information into prices sooner, reducing the size or duration of the original opportunity. |
| B | True | Independent firms using similar data and models can create correlated positions without any explicit coordination. |
| C | False | Reverses the correct conclusion: exit liquidity *can* be worse precisely when crowded strategies unwind — simultaneous selling overwhelms buyers and amplifies impact. |
| D | False | Diversifying fund *names* does not guarantee diversified *exposure* — different managers can hold substantially overlapping positions and risks. |
| E | True | Capacity estimates from calm, uncrowded periods may be optimistic; stress and competitor activity can materially reduce executable capacity. |

**Reference:** Crowding, correlated unwinds, and stress-conditional capacity — Investopedia "Crowded trade," "Liquidity risk"; CFA curriculum (liquidity and market structure risk).

### [QF-D10G6Q1] 3:1 leverage — magnifying gains and losses
**Scenario:** A fund has $10M equity and borrows to hold $30M of a risky portfolio (3:1 gross exposure). The risk committee asks how leverage changes outcomes before financing costs.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | 2% × $30M = $0.6M gain = 6% of $10M equity before costs. |
| B | False | Double-negative embedded claim: the inner claim — a 2% loss produces ~6% loss on equity ($0.6M is 6% of equity) — is correct and should be accepted, so "a reviewer would be wrong to accept it" is false. |
| C | False | Leverage magnifies both favorable *and* adverse portfolio returns — losses are not left unchanged. |
| D | True | Adverse moves can trigger margin calls or forced deleveraging even if the long-run thesis remains valid, because lenders/brokers set collateral needs by current conditions. |
| E | False | Reverses the correct conclusion: financing cost and availability *do* affect the realized benefit of leverage — borrowing is neither free nor guaranteed to remain available. |

**Reference:** Leverage math, margin/funding risk, and symmetric magnification — Investopedia "Leverage," "Margin call"; CFA curriculum (leverage and financing risk).

### [QF-D10G6Q2] Market-neutral gross vs. net exposure
**Scenario:** A market-neutral portfolio holds $120M long and $120M short against $40M of equity. The CRO worries the team reports only zero net dollar exposure.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | $120M long − $120M short = $0 net dollar exposure. |
| B | True | Gross exposure = $120M + $120M = $240M; $240M / $40M = 6, i.e., 600% of investor equity. |
| C | False | Zero net dollars does not preclude large losses — high gross exposure, imperfect hedges, and correlated adverse moves can create substantial losses. |
| D | False | Reverses the correct conclusion: longs and shorts *can* both lose — longs can fall while shorts rise, harming both sides of the relative trade. |
| E | True | Sector, beta, factor, liquidity, and concentration limits capture economically important risks that net dollar exposure alone does not measure. |

**Reference:** Gross vs. net exposure and residual risk in long/short books — Investopedia "Gross exposure," "Net exposure"; Grinold & Kahn, *Active Portfolio Management* (long/short risk).

### [QF-D10G6Q3] Fixed 5% stop-loss — risk-control limits
**Scenario:** A desk proposes an automatic 5% stop-loss on every position. The PM expects it to prevent large losses; the quant warns volatile assets cross the threshold on ordinary noise and gaps can bypass the intended exit.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | A stop-loss does not guarantee execution at exactly 5% below entry — a gap or lack of liquidity can cause a fill well beyond the trigger. |
| B | True | A fixed percentage threshold affects assets differently: a 5% move can be routine for one asset and exceptional for another. |
| C | False | Reverses the correct conclusion: frequent stop-outs *can* crystallize losses just before a valid signal recovers (whipsaw when prices reverse after the threshold). |
| D | True | Position sizing and portfolio-level exposure limits complement — rather than necessarily replace — stop-loss rules, addressing different dimensions of risk. |
| E | False | Reverses the correct conclusion: risk controls *should* be evaluated for behavior during gaps, illiquidity, and correlated stress — controls designed for normal conditions may fail there. |

**Reference:** Stop-loss mechanics (gaps, slippage, whipsaw) and layered risk controls — Investopedia "Stop-loss order," "Slippage"; CFA curriculum (risk management, stress testing).

### [QF-D10G7Q1] Low-vol training, high-vol deployment — regime dependence
**Scenario:** A model that did well in a low-volatility training period loses money in a high-volatility regime after deployment. The research lead asks whether to retrain immediately or whether the failure reflects a deeper change.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Reverses the correct conclusion: a regime shift *can* change both feature distributions and the conditional feature→return relationship. |
| B | False | Retraining on recent observations does not always restore profitability — recent data may be limited/noisy, and the predictive relationship may have disappeared. |
| C | True | Comparing live inputs and outcomes against training distributions (distribution/residual monitoring) helps diagnose drift. |
| D | True | Breaking down performance by volatility regime can reveal dependence hidden by an overall backtest average. |
| E | True | Recalibration, redesign, or retirement should be considered when the original economic relationship no longer holds — retraining is not the only response. |

**Reference:** Regime dependence, model drift, and retrain/retire decisions — Lopez de Prado, *Advances in Financial ML* (structural breaks, drift); Investopedia "Regime change," "Model risk."

### [QF-D10G7Q2] Close-price fills vs. live execution — backtest vs. production
**Scenario:** A backtest assumes fills at the close, but live orders arrive after the close signal is computed and execute at worse prices; the desk also reports rejected orders and missing data absent from research.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Reverses the correct conclusion: the discrepancy *can* arise from implementation assumptions even when the predictive model behaves as coded — timing/execution/system failures separate live from theoretical results. |
| B | False | Backtest success alone does not validate the production data and order pipeline — a historical simulation doesn't test every live data, software, broker, and execution dependency. |
| C | True | Paper trading or staged deployment exposes operational problems before full capital is committed (controlled rollout with limited financial risk). |
| D | False | Reverses the correct conclusion: monitoring timestamps, order status, fills, slippage, and data quality *does* help locate the performance gap by linking forecasts to submitted trades and realized outcomes. |
| E | True | Valid production evaluation compares realized execution against prices *actually attainable after the decision time* — respecting when the signal became available and an order could reach the market. |

**Reference:** Implementation shortfall, execution realism, and staged deployment — Lopez de Prado, *Advances in Financial ML* (backtesting realism, false discoveries); Investopedia "Implementation shortfall," "Slippage," "Paper trading."

### [QF-D10G7Q3] Falling information coefficient — monitoring and retirement rules
**Scenario:** A deployed signal's six-month rolling information coefficient falls from 0.06 to near zero, turnover rises, and net returns turn negative. The committee wants a rule that neither ignores decay nor retires after one unlucky week.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Several related diagnostics (signal quality, costs, exposures, outcomes) together provide stronger evidence than a single short-term P&L observation. |
| B | False | Reverses the correct conclusion: predefined review thresholds *can* reduce emotional reactions — governance set in advance makes escalation/review more consistent. |
| C | True | A declining information coefficient alongside higher costs explains deteriorating net returns: weaker predictive value cuts gross opportunity while higher turnover adds drag. |
| D | False | A statistically significant original backtest does not justify continuing indefinitely — historical evidence does not guarantee the relationship persists after deployment. |
| E | True | A retirement decision should weigh statistical uncertainty, implementation quality, current market conditions, and whether the economic thesis still holds — no single metric distinguishes temporary underperformance from permanent decay. |

**Reference:** Signal decay monitoring (information coefficient), governance thresholds, and retirement criteria — Grinold & Kahn, *Active Portfolio Management* (information coefficient, fundamental law of active management); Lopez de Prado, *Advances in Financial ML* (deflated Sharpe, strategy decay).

## References (domain-level)

1. **Lopez de Prado — *Advances in Financial Machine Learning*:** backtest overfitting and selection bias under multiple testing, the **deflated Sharpe ratio**, purged/embargoed cross-validation and walk-forward, transaction-cost/market-impact realism, strategy capacity, structural breaks/drift, and false discoveries in strategy research (D10 G1, G3, G4, G5, G7).
2. **Grinold & Kahn — *Active Portfolio Management*:** the **fundamental law of active management** (information coefficient × breadth), signal-to-position construction and risk models, benchmarks/residual return, attribution, net-of-cost alpha, and long/short exposure (D10 G2, G3, G4, G6, G7).
3. **CFA Program Curriculum:** performance evaluation and attribution, benchmark quality, leverage and financing/margin risk, liquidity and market-structure risk, and risk management/stress testing (D10 G3, G5, G6).
4. **Investopedia:** "Backtesting," "Data mining bias," "Overfitting," "In-sample vs. out-of-sample," "Walk-forward optimization," "Transaction costs," "Market impact," "Turnover ratio," "Leverage," "Margin call," "Gross/Net exposure," "Stop-loss order," "Slippage," "Implementation shortfall," "Crowded trade" (definitional anchors across all groups).
5. **Concept references (durable):** turnover-to-cost arithmetic (turnover × AUM × cost rate), gross-vs-net alpha, dollar-neutral vs. risk-neutral exposure, and the accuracy-vs-P&L distinction — standard quantitative-strategy evaluation concepts underlying D10 G2, G4, G5, G6.
