# QF Domain 1 — Financial Time Series & Market Data Behavior

## Domain cheat-sheet

- **Price level vs. return (the comparability problem).** A raw dollar price change is **not** comparable across securities at different price levels: a $5 move is 20% of a $25 stock but 1% of a $500 stock. **Returns** (changes expressed relative to the amount invested) strip out the arbitrary price scale and make cross-security comparison meaningful. A security's *price level* says nothing about its risk — a high nominal price is not evidence of greater risk. Equal-dollar positions earn according to **percentage** return, not dollar price change.
- **Simple vs. log (continuously compounded) returns.**
  - **Simple return** r_t = P_t/P_{t-1} − 1. Multi-period simple returns **compound geometrically** (1+r_1)(1+r_2)…; they do **not** add. A +10% day then a −10% day gives 1.10 × 0.90 = 0.99 → a −1% compounded result (final wealth $99 on $100), even though the two simple returns *sum* to zero.
  - **Log return** r_t = ln(P_t/P_{t-1}) = ln P_t − ln P_{t-1}. Log returns are **additive across adjacent periods** (log price differences telescope when summed) when prices are positive — convenient for multi-period aggregation.
  - Choosing a return *representation* never changes the underlying investment outcome; it only changes how the same economics are expressed.
- **Normalization.** Dividing a price series by its first value rebases it to 1.0. A normalized value of 1.25 means +25% vs. the chosen start; it makes cumulative growth visually comparable and removes the difference in *initial price levels*. It does **not** equalize future daily returns and does **not** make a nonstationary price process stationary (trends, breaks, changing variance survive rescaling).
- **Autocorrelation & temporal dependence.** The autocorrelation function (ACF) measures linear dependence between a series and its own lags. A negative lag-1 autocorrelation is consistent with **short-horizon reversal** *in sample*; it describes an **average** relationship, not a per-day deterministic sign flip, and must be judged against **sampling variability**. Microstructure effects (bid-ask bounce) can **manufacture** apparent short-lag autocorrelation. A credible estimate is not an automatic tradable edge — turnover, spreads, slippage, and stability all gate net profitability.
- **Lead-lag & look-ahead bias.** Misaligned closing times across markets can make one market *appear* to lead another; calendar labels can hide the true information sequence. Using information not available at the decision time is **look-ahead bias** — a backtest must never let a decision consume a price/close that occurs after it. Contemporaneous correlation establishes neither direction nor causality. Lag direction is defined by chronological order, so reversing the series changes the relationship being tested.
- **Train/test on time series.** **Random shuffling** before splitting leaks future regimes into the training set used to select models for earlier test dates, and lets neighboring (dependent) observations straddle the split, inflating apparent stability. A **chronological split** (train past → test future) mirrors deployment. Time-aware cross-validation (**walk-forward / expanding window**) gives repeated tests while respecting the arrow of time.
- **Rolling windows & time-varying statistics.** Shorter windows (e.g., 20-day vol) react faster but are noisier; longer windows (120-day) are smoother/more stable but lag abrupt changes. There is **no universally superior window** — it is a responsiveness-vs-stability tradeoff, and both estimates can mislead after a regime change. A **centered** window (past + future days) uses unavailable information → look-ahead bias; use a **trailing** window computed from current and past data only, and shift signals so the feature precedes the measured return. Rolling correlations (and vols) are *estimates*, not permanent asset properties; picking a window because it maximized backtest performance invites overfitting.
- **Trend, momentum, mean reversion.** Momentum = past winners tending to keep outperforming at the tested horizon — a **probabilistic tendency**, not a guarantee for every name, and it can reverse sharply. Medium-horizon momentum and short-horizon mean reversion can **coexist** at different horizons/regimes. Pairs/spread trading relies on mean reversion in the **spread**, not each leg; a structural break (merger, financing event) can permanently reset the equilibrium so the old rolling mean becomes a poor estimate, and a longer lookback can *retain obsolete data*. The same price move can support both continuation and reversal stories — context (event type, liquidity, horizon, regime) and risk controls (position limits, staged entry) help manage the uncertainty. Everything should be validated **out of sample**.
- **Stationarity vs. nonstationarity.** A trending price level has a time-varying mean (nonstationary). Fitting a model to trending **levels** can yield high in-sample fit that is **spurious** (shared trends, not predictive structure). Transforming to **returns** often removes level trends but does **not** guarantee stationarity (variance/regimes may still change). A **structural break** can make a large pre-break sample precisely estimate an **obsolete** regime — more observations do **not** compensate for a changed data-generating process. Comparing pre/post-break estimates helps diagnose instability; rolling/regime-aware estimation adapts faster at the cost of more estimation noise.
- **Volatility clustering & heteroskedasticity.** Large absolute returns cluster near other large absolute returns even when **signed** returns are nearly serially uncorrelated — the hallmark of volatility clustering / conditional heteroskedasticity (ARCH/GARCH). Dependence in **squared/absolute** returns can exist with little dependence in signed returns, so predictability of return *magnitude* does **not** imply predictability of *direction*. A constant-volatility assumption understates risk in turbulent periods and overstates it in calm ones; volatility-targeting rules take **more** exposure when measured vol is low, creating hidden vulnerability when a calm→crisis transition hits (correlations and vol rise together, compounding losses). No window *eliminates* regime-transition risk — faster windows still react only after some evidence arrives.
- **Fat tails.** Asset-return distributions are **leptokurtic** (heavy-tailed, excess kurtosis) relative to the normal — large moves occur more often than a Gaussian predicts, which is why rare stressed periods can dominate drawdowns and why full-period averages conceal tail behavior.
- **Information decay & signal-to-noise.** A signal statistically valid at one horizon (first 20 minutes after news) can be **unusable** by a later execution time; delay lets other participants price in the information. Faster decay raises the importance of data/decision/execution **latency**, and the return target must match the signal's useful horizon. **Multiple testing / data snooping**: screening many noisy candidates makes at least one look great by luck, and reporting the in-sample winner is **optimistically biased**; a held-out set helps, but repeatedly reusing it turns it into part of selection. Lack of economic rationale lowers plausibility but does not *prove* zero predictive value — predictiveness is empirical. A larger **gross** forecast need not yield a larger **net** return once latency, turnover, spread, slippage, and impact are charged; a weak-but-stable, scalable, cheap signal can beat a large but fast-decaying one. More rows of high-frequency data ≠ more independent information when adjacent observations are dependent.
- **Adjusted prices, splits & dividends (market-data hygiene).** Use **adjusted** prices for return/backtest work: raw closes contain discontinuities from splits (a 2-for-1 halves the quoted price with no economic loss) and ignore dividends. Split/dividend-adjusted series give economically correct returns and avoid spurious jumps.
- **Survivorship & look-ahead bias in datasets.** A universe containing only *surviving* securities (delisted/bankrupt names dropped) **upward-biases** backtested returns (survivorship bias). Look-ahead bias also enters via point-in-time data: using later-revised fundamentals, index membership known only after the fact, or any value not available at the historical decision time.

## Common traps

- **Inverted-polarity questions (9 of 21 here).** When the body says "each item asserts that its quoted statement is **incorrect**," the Answer Key verdict is **not** flipped by you — transcribe it verbatim, but read it correctly: **True = the quoted statement is incorrect; False = the quoted statement is correct/accurate.** Read the polarity line *first*. Inverted here: **G1Q1, G2Q3, G3Q1, G4Q1, G5Q2, G5Q3, G6Q2, G7Q2, G7Q3.** The remaining 12 are Normal (True = accurate).
- **Dollar change ⇒ equal performance.** False — equal dollar moves are different percentage returns at different price levels; equal-dollar positions earn by percentage return.
- **Price level ⇒ risk.** A higher quoted price does not prove a security is riskier.
- **Simple returns add / "±10% cancels."** False — multi-period simple returns compound geometrically; +10% then −10% leaves 99%, not 100%. Only **log** returns add across adjacent periods.
- **Changing the return representation changes the outcome.** False — representation is bookkeeping; the economics are unchanged.
- **Normalization makes series stationary / equalizes future returns.** False on both — it only rebases levels and removes the starting-price difference.
- **Autocorrelation ⇒ deterministic sign / guaranteed profit.** False — it is an average, sampling-noisy relationship; microstructure can fake it; profitability needs costs/turnover/stability to clear.
- **Contemporaneous correlation ⇒ causation/direction.** False.
- **Shuffle then split is fine for time series.** False — it leaks future regimes and lets dependent neighbors straddle the split; use chronological / walk-forward splits.
- **Shorter rolling window is always better.** False — faster reaction buys more noise; it is a tradeoff.
- **Centered rolling window in a backtest.** Look-ahead bias — it uses future observations; use trailing windows.
- **Momentum ⇒ every winner wins / rules out mean reversion.** False — probabilistic tendency; continuation and reversal coexist at different horizons.
- **Wide spread deviation / long lookback ⇒ guaranteed convergence / break protection.** False — the spread may re-level; a longer window retains obsolete data.
- **High in-sample fit on trending levels ⇒ real forecast.** Often spurious (shared trends). Nonstationarity does not by itself make every strategy unprofitable.
- **More observations compensate for a regime change.** False — data from a dead regime is systematically misleading, not merely noisy; a large sample can precisely estimate an obsolete regime.
- **Full-sample average / Sharpe is representative.** Pooling hides time variation; a favorable early regime can keep the full-sample average positive after current performance decays.
- **Magnitude predictability ⇒ direction predictability.** False — volatility clustering predicts size, not sign.
- **Shorter vol window eliminates regime risk.** False — it still reacts only after evidence arrives.
- **Statistical significance at one horizon ⇒ tradable at a later horizon.** False — signals decay; align the return target to the signal's useful life.
- **Best of many backtests is unbiased / big gross ⇒ big net / more rows ⇒ more information.** All false — multiple testing biases winners upward; costs eat gross forecasts; dependent observations overstate effective sample size.

## Questions

### [QF2-D1G1Q1] Dollar change vs. percentage return across price levels
**Scenario:** A fund compares a $25 stock and a $500 stock that both rose $5; a PM claims identical dollar changes mean identical performance. The risk team must pick a representation supporting cross-security comparison.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: a $5 gain is 20% of $25 but only 1% of $500, so the $25 stock had the larger percentage return. The quoted statement is right, so the inverted verdict is False. |
| B | True (incorrect) | Wrong: equal-dollar positions earn according to percentage return, which differs substantially (20% vs. 1%) here — identical dollar changes do not imply identical performance. |
| C | False (accurate) | Correct: percentage returns express change relative to the amount invested and reduce dependence on arbitrary price scale, so they are generally more comparable than raw dollar changes. |
| D | True (incorrect) | Wrong: a security's quoted price level alone does not establish its economic risk — price level and risk are distinct. |
| E | False (accurate) | Correct: modeling price changes without accounting for the starting price distorts cross-security comparison, since the same dollar move has very different significance at different starting prices. |

**Reference:** Tsay, *Analysis of Financial Time Series*, §1.2 (returns of assets — simple returns and why returns rather than price changes are the comparable unit); Balch ML4T lecture 01-04 (statistical analysis of time series — daily/cumulative returns) and 01-01/01-02 (reading and normalizing price data).

### [QF2-D1G1Q2] Simple vs. log returns and compounding over two periods
**Scenario:** An asset rises 10% then falls 10%; the client assumes it finishes flat. The analyst must explain how return definitions and compounding determine the real result.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | $100 × 1.10 × 0.90 = $99, so final wealth is $99 before costs — the moves do not cancel. |
| B | True | The simple returns sum to zero (+10% − 10%), yet the geometrically compounded return is −1%; arithmetic summation misstates the multi-period result. |
| C | False | Adding simple returns does *not* always give the correct cumulative return — multi-period simple returns must generally be compounded geometrically. |
| D | True | Continuously compounded (log) returns are additive across adjacent periods when prices are positive, because each is a log price difference and the differences telescope when summed. |
| E | False | Switching to log returns changes only the representation, not the actual ending wealth; the investor still ends at $99. |

**Reference:** Tsay, *Analysis of Financial Time Series*, §1.2 (simple vs. continuously compounded/log returns; multiperiod returns and compounding); Balch ML4T lecture 01-04 (daily and cumulative returns).

### [QF2-D1G1Q3] Normalizing price series to a common base
**Scenario:** A team divides each price series by its day-1 value (both start at 1.0) to compare cumulative performance, and asks what the transform preserves and removes.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | A normalized value of 1.25 is exactly price relative to the chosen start — 25% above the starting price. |
| B | False | Rescaling levels does not alter or equalize subsequent percentage changes — future daily returns are unchanged by normalization. |
| C | True | Both series receive a common baseline of 1.0, which removes the difference in initial quoted price levels and eases relative-growth comparison. |
| D | True | Under the stated assumptions (same dates, no omitted distributions/adjustments), ending at 1.30 vs. 1.20 means cumulative gains of 30% vs. 20%, so the first outperformed. |
| E | False | Normalization is a rescaling; it does not remove trends, structural breaks, or other sources of nonstationarity. |

**Reference:** Tsay, *Analysis of Financial Time Series*, §1.2 (returns as scale-free comparisons; §2.1 stationarity for the nonstationarity point); Balch ML4T lecture 01-01/01-04 (normalizing prices to a common starting value for comparison).

### [QF2-D1G2Q1] Lag-one autocorrelation and tradable edge
**Scenario:** Daily returns show lag-1 autocorrelation −0.18. The head trader wants a buy-after-down / sell-after-up rule; research warns a historical estimate is not automatically a tradable edge.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Negative serial correlation means adjacent returns tended to move oppositely in the sample — consistent with short-horizon reversal. |
| B | False | Autocorrelation is an average relationship, not a deterministic rule; it does not prove tomorrow's return has the opposite sign of today's. |
| C | True | Even a nonzero estimate carries substantial statistical uncertainty — it must be judged relative to sampling variability and the number of observations. |
| D | True | Bid-ask bounce and other microstructure features can create apparent short-lag autocorrelation in recorded prices. |
| E | False | A credible negative autocorrelation does not guarantee positive net returns — forecast strength, turnover, spreads, slippage, and stability all affect realizable profit. |

**Reference:** Tsay, *Analysis of Financial Time Series*, §2.1–§2.2 (stationarity, autocorrelation function, serial correlation and its statistical testing); Balch ML4T time-series/statistical-analysis lecture (01-04).

### [QF2-D1G2Q2] Lead-lag across markets and look-ahead bias
**Scenario:** Market A closes before Market B; a researcher uses A's close-to-close return to predict B's next session. The PM asks whether the lead-lag relationship is genuine and usable or a timestamp artifact.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Closing times must be aligned first, because calendar labels can obscure the true information sequence across different trading hours. |
| B | True | Using information not yet available at the proposed trade time would create look-ahead bias — a backtest cannot consume a close that occurs after the decision. |
| C | False | A contemporaneous correlation alone does not establish which market causes the other to move — correlation implies neither direction nor causality. |
| D | True | A stable lead-lag relationship could support forecasting even when same-period correlation is imperfect, if earlier observations carry information about later outcomes. |
| E | False | Reversing chronological order changes the relationship being tested — lag direction is defined by time order, so lagged interpretations do not survive reversal. |

**Reference:** Tsay, *Analysis of Financial Time Series*, §2.1–§2.2 (serial/cross-correlation, lagged relationships); Balch ML4T backtesting/time-series lectures on look-ahead bias and data alignment (01-04).

### [QF2-D1G2Q3] Shuffling time-series data before train/test split
**Scenario:** An ML team randomly shuffles daily observations before splitting train/test. The lead says shuffling gives independent examples; the risk officer worries about persistent conditions and lagged features. Goal: estimate future-deployment performance.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: random shuffling lets later-period observations influence model selection for earlier test observations — the training set can hold regimes that are future relative to test dates. |
| B | False (accurate) | Correct: a chronological split (train past → deploy into future) more closely matches real deployment and preserves the actual information flow. |
| C | True (incorrect) | Wrong: observation order is *not* irrelevant once features exist — ordering remains central to leakage control, temporal dependence, and the meaning of a forecast. |
| D | False (accurate) | Correct: nearby dates split across train and test share regime information, weakening effective separation and making performance look more stable than it is. |
| E | False (accurate) | Correct: a time-aware evaluation can still use multiple folds (walk-forward / expanding window) as long as each fold respects the direction of time. |

**Reference:** Tsay, *Analysis of Financial Time Series*, §2.1 (temporal dependence / stationarity — why time ordering matters); Balch ML4T lectures on backtesting, train/test discipline, and avoiding look-ahead/leakage (01-04 and ML4T assessment/backtesting lecture).

### [QF2-D1G3Q1] 20-day vs. 120-day rolling volatility
**Scenario:** A researcher compares a 20-day and a 120-day rolling volatility. The PM wants fast reaction but worries about noise, and will use the estimate to adjust exposure in both calm and fast-changing markets.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: the 20-day estimate reacts faster — shorter windows place more weight on recent observations. |
| B | False (accurate) | Correct: the 120-day estimate is usually more stable because longer windows smooth short-term fluctuations. |
| C | True (incorrect) | Wrong: a shorter window is not always superior — faster reaction comes with greater estimation noise. |
| D | False (accurate) | Correct: window length creates the central responsiveness-vs-stability tradeoff. |
| E | False (accurate) | Correct: both estimates can become misleading after a structural regime change, because historical estimates fail when the underlying process shifts. |

**Reference:** Tsay, *Analysis of Financial Time Series*, §2.1 (sample moments, time-varying statistics) and ch.3 (volatility estimation); Balch ML4T lecture 01-04 (rolling mean/standard deviation, Bollinger Bands, rolling volatility).

### [QF2-D1G3Q2] Rolling correlation instability
**Scenario:** A risk-parity fund's 60-day equity-bond rolling correlation swings from −0.35 to +0.25 under stress. The CRO cautions against treating either value as a permanent asset property.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | A positive recent rolling correlation reflects a tendency to co-move over that window — not perfect agreement, but same-direction tendency. |
| B | True | A change in estimated correlation can alter expected diversification; higher correlation generally reduces the diversification benefit, all else equal. |
| C | False | A correlation of +0.25 is neither perfect nor deterministic — the assets are not guaranteed to rise and fall together every day. |
| D | True | A longer window reacts more slowly to abrupt changes because older observations remain in the estimate and dilute recent moves. |
| E | True | Choosing a window solely because it produced the best historical result fits sample-specific noise — a form of overfitting. |

**Reference:** Tsay, *Analysis of Financial Time Series*, §2.1 (time-varying covariance/correlation, stationarity) ; Balch ML4T lecture 01-04 and 01-07 (rolling statistics; correlation and portfolio statistics; overfitting cautions in parameter selection).

### [QF2-D1G3Q3] Centered vs. trailing rolling windows and look-ahead
**Scenario:** A model buys when price falls >2 rolling std below its 30-day mean, but the analyst computes each day's mean/std from a *centered* window (15 prior + 15 future days). Can this backtest represent trading at each day's close?
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | A centered window pulls in future observations that were unavailable at the historical decision time. |
| B | True | Using those future-containing statistics exposes the backtest to look-ahead bias — it is evaluated with knowledge it could not have had live. |
| C | True | A trailing window (current and past observations only) better matches real-time availability. |
| D | False | A 30-observation rolling statistic is not fully defined from the first observation — early dates lack a complete window unless the implementation allows shorter warm-up windows or missing values. |
| E | True | A correctly computed trailing signal may still need shifting so it precedes the measured return — feature and return timestamps must reflect whether the trade occurs before or after the signal price. |

**Reference:** Tsay, *Analysis of Financial Time Series*, §2.1 (rolling/sample statistics; filtration/information set at time t); Balch ML4T lecture 01-04 (rolling mean/std, Bollinger Bands) and backtesting lectures on look-ahead bias and signal/return timing.

### [QF2-D1G4Q1] Momentum / return continuation across horizons
**Scenario:** A commodity fund sees six-month winners keep outperforming the next month and calls it momentum; the risk committee notes horizon/regime dependence and sudden-reversal risk.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: the pattern is consistent with return continuation at the tested horizons — past winners continuing to outperform is exactly what momentum exploits. |
| B | True (incorrect) | Wrong: momentum is a probabilistic tendency; it does not imply every positive-six-month contract will gain next month. |
| C | False (accurate) | Correct: a momentum strategy can suffer when established trends reverse sharply, rapidly turning trend-following positions into losses. |
| D | True (incorrect) | Wrong: medium-horizon momentum does not rule out short-horizon mean reversion — continuation and reversal can coexist at different horizons or conditions. |
| E | False (accurate) | Correct: the relationship should be tested out of sample before being treated as stable, since sample-specific trends can reflect noise, selection, or a temporary regime. |

**Reference:** Tsay, *Analysis of Financial Time Series*, §2.1–§2.2 (serial dependence / autocorrelation underpinning momentum and reversal); Balch ML4T lectures on technical indicators, momentum, and out-of-sample validation (01-04 and the technical-analysis/ML strategy lectures).

### [QF2-D1G4Q2] Pairs trading and mean reversion in a spread
**Scenario:** A market-neutral desk trades a related pair when the spread strays far from its rolling average, expecting reversion; the PM worries a merger/financing event could permanently change the relationship.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The trade relies on mean reversion in the spread (the relative relationship), not necessarily reversion in each stock's price. |
| B | False | A wide historical deviation does not guarantee convergence — the spread may keep diverging or settle at a new level. |
| C | True | A structural change can make the old rolling mean a poor estimate of the current equilibrium, since past observations may describe a relationship that no longer holds. |
| D | False | Extending the lookback does not always protect against breaks — a longer window retains obsolete data and delays recognizing a new regime. |
| E | True | An economically grounded relationship strengthens the case for testing the spread but does not eliminate model risk or assure convergence. |

**Reference:** Tsay, *Analysis of Financial Time Series*, §2.1 (stationarity of a spread; cointegration-style mean reversion) and ch.8 (multivariate/cointegration context); Balch ML4T lectures on mean reversion, pairs/spread trading, and regime risk.

### [QF2-D1G4Q3] Interpreting a large price jump — momentum vs. reversal
**Scenario:** After an 8% jump on high volume, one researcher expects a persistent trend, another a reversal. The committee asks what can be concluded from price alone while limiting exposure to a wrong read.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The same move can support both momentum and mean-reversion hypotheses — continuation and reversal models assign different meanings to the same initial move. |
| B | False | Price history alone does not guarantee which mechanism generated the move — a price path does not uniquely identify its generating process. |
| C | True | Conditional evidence (event type, liquidity, horizon, prior regime) can help distinguish whether the move is likely to persist or reverse. |
| D | False | A strategy that works after average moves need not work after large event-driven jumps — event-driven observations can have different dynamics. |
| E | True | Position limits or staged entry reduce the consequence of over-committing to either uncertain interpretation. |

**Reference:** Tsay, *Analysis of Financial Time Series*, §1.3 (distributional properties, heavy tails / large moves) and §2.1–§2.2 (dependence structure); Balch ML4T lectures on technical signals, event behavior, and risk control / position sizing.

### [QF2-D1G5Q1] Fitting price levels vs. returns — spurious fit
**Scenario:** A team fits a model to the *price level* of a decades-trending index, reports excellent in-sample fit, and the sponsor treats a stable residual plot as proof of generalization. Validation suspects common trends.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | A trending price level has a mean that changes through time, which is inconsistent with a constant unconditional mean (nonstationary). |
| B | True | High in-sample fit between trending series can arise without a useful forecast — shared trends create strong-looking but spurious fits. |
| C | True | Transforming prices to returns can produce a more stable series but does not guarantee stationarity — variance, regimes, or other properties may still change. |
| D | False | A nonstationary input does not necessarily make every strategy unprofitable — nonstationarity creates modeling challenges, not a determinate profitability verdict. |
| E | True | Out-of-sample testing across periods can expose dependence on a particular historical trend; performance that vanishes out of sample is evidence against a stable relationship. |

**Reference:** Tsay, *Analysis of Financial Time Series*, §2.1 (stationarity) and ch.2 (unit-root/nonstationary processes, spurious regression between trending series); Balch ML4T lectures on time-series properties, returns transformation, and out-of-sample evaluation (01-04).

### [QF2-D1G5Q2] Structural break and obsolete regime estimates
**Scenario:** A credit model was calibrated in a low-rate, low-default era; after a policy shift rates and spreads move persistently higher, but the PM keeps the old parameters because the training sample is large. The risk officer asks how a structural break should affect confidence.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: a large historical sample can estimate an obsolete regime very precisely — low sampling error does not ensure the relationship still applies. |
| B | True (incorrect) | Wrong: more observations do not always compensate for a changed data-generating process — data from a different regime can be systematically misleading, not merely noisy. |
| C | False (accurate) | Correct: a structural break can change the relevance of pre-break observations, which may no longer describe current conditions. |
| D | False (accurate) | Correct: rolling or regime-aware estimation adapts faster but introduces greater estimation noise — it trades sample size for relevance. |
| E | False (accurate) | Correct: comparing parameter estimates before and after the suspected break helps diagnose instability, since material changes argue against a constant-parameter assumption. |

**Reference:** Tsay, *Analysis of Financial Time Series*, §2.1 (stationarity) and ch.2 (structural breaks / parameter stability, time-varying parameters); Balch ML4T lectures on regime change and backtest robustness.

### [QF2-D1G5Q3] Pooled Sharpe ratio hides time variation
**Scenario:** A long-short fund assumes constant mean/variance of daily returns; a review finds average return fell after competitors copied the signal and volatility rose after a market-structure change. The CIO wants one historical Sharpe for allocation but an honest current read.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: pooling all periods into one estimate can conceal time variation in both return and risk — a single summary blends different conditions. |
| B | True (incorrect) | Wrong: a positive full-sample average return does not imply the current expected return is positive — a favorable earlier regime can dominate the average after recent deterioration. |
| C | False (accurate) | Correct: changes in competition can contribute to nonstationarity in an alpha strategy, as crowding alters the payoff to a formerly effective signal. |
| D | False (accurate) | Correct: subperiod and rolling analyses can reveal instability that a full-sample statistic hides, showing whether performance concentrates in particular intervals. |
| E | True (incorrect) | Wrong: detecting a change in sample statistics does not by itself identify the exact economic cause — causal attribution requires additional evidence. |

**Reference:** Tsay, *Analysis of Financial Time Series*, §2.1 (stationarity, time-varying moments) and ch.3 (time-varying volatility); Balch ML4T lecture 01-07 (Sharpe ratio and portfolio statistics) with time-series stability caveats (01-04).

### [QF2-D1G6Q1] Volatility clustering and constant-vol risk limits
**Scenario:** An options market maker observes large absolute returns clustering together even though signs are hard to predict. The current risk limit assumes the same volatility every day; the head of risk weighs whether recent turbulence should change tomorrow's exposure.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Clusters of high- and low-magnitude periods are the hallmark of volatility clustering (persistent conditional variance). |
| B | False | Weak autocorrelation in *signed* returns does not rule out persistence in squared/absolute returns — volatility dependence can coexist with little signed serial correlation. |
| C | True | Volatility clustering makes a single constant-volatility estimate slow to reflect change — it understates risk in turbulent periods and overstates it in calm ones. |
| D | False | Predictability of return *magnitude* does not imply predictability of *direction* — forecasting size is distinct from forecasting sign. |
| E | True | Reducing exposure after volatility rises is a valid risk-control response even without any directional forecast — exposure can be scaled to risk. |

**Reference:** Tsay, *Analysis of Financial Time Series*, ch.3 (conditional heteroscedastic models — ARCH/GARCH, volatility clustering; §1.3 heavy tails); Balch ML4T lecture 01-04 (rolling volatility) on time-varying risk.

### [QF2-D1G6Q2] Volatility targeting and regime transitions
**Scenario:** A volatility-targeting fund levered up during a long calm period as measured vol fell; a sudden crisis then drives correlations and volatility up together. The CRO questions whether recent estimates created hidden vulnerability.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: low recent volatility can lead a vol-targeting rule to take more exposure, since targeting a fixed risk level permits larger positions when estimated vol is low. |
| B | False (accurate) | Correct: if volatility were truly constant, the model would exclude a low→high volatility transition by assumption, even though reality can violate it. |
| C | False (accurate) | Correct: a sudden calm→crisis transition can leave the fund overexposed before backward-looking estimates catch up. |
| D | False (accurate) | Correct: rising cross-asset correlations during stress reduce diversification just as individual-asset risk rises, compounding portfolio losses. |
| E | True (incorrect) | Wrong: a shorter volatility window does not eliminate all regime-transition risk — faster adaptation still occurs only after some evidence arrives and cannot anticipate every discontinuous change. |

**Reference:** Tsay, *Analysis of Financial Time Series*, ch.3 (GARCH / volatility clustering; time-varying correlation, multivariate volatility ch.10) ; Balch ML4T lecture 01-04 (rolling volatility) and 01-07 (risk/leverage considerations).

### [QF2-D1G6Q3] Regime-conditioned performance analysis
**Scenario:** A systematic equity strategy does well in calm, rising markets but loses in abrupt high-vol reversals. The committee has seen only full-period averages; the CIO wants to know whether returns compensate for regime-dependent risk, so the team splits results by regime.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Full-period averages can conceal poor performance concentrated in a crisis regime — aggregation obscures when and under what conditions losses occur. |
| B | False | Strong performance in the most common regime does not guarantee acceptable max drawdown — rare stressed periods can dominate drawdown. |
| C | True | Regime-conditioned analysis can reveal that behavior depends on market state, exposing conditional strengths and vulnerabilities. |
| D | True | Defining regimes *after* seeing the losses creates selection and overfitting concerns — post hoc boundaries may be chosen to tell a favorable story and need independent validation. |
| E | False | A regime-sensitive strategy need not be discarded — exposure scaling, diversification, hedging, or explicit regime handling may mitigate the sensitivity. |

**Reference:** Tsay, *Analysis of Financial Time Series*, ch.3 (regime/volatility states; Markov switching ch.4) and §1.3 (tail behavior / drawdowns); Balch ML4T lectures on performance evaluation, drawdown, and overfitting (01-07, 01-04).

### [QF2-D1G7Q1] Signal decay vs. execution horizon
**Scenario:** A news signal predicts returns most strongly in the first 20 minutes, but the portfolio rebalances only at the next day's close. The research director cites the original significant event study; the trading team must decide if the information survives to execution.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | A signal can be statistically valid at one horizon yet unusable at a later execution time — predictive power is horizon-specific and may disappear before the trade. |
| B | True | Delayed rebalancing lets other participants incorporate the information first, eroding the opportunity. |
| C | False | Significance at 20 minutes does not guarantee positive next-day net returns — predictiveness need not persist to the next day or survive costs. |
| D | True | Faster decay increases the importance of data, decision, and execution latency, because delay consumes more of a short-lived signal's useful life. |
| E | True | The return target should match the horizon over which the signal retains information — horizon alignment is needed to evaluate and use the forecast coherently. |

**Reference:** Tsay, *Analysis of Financial Time Series*, ch.1 (market efficiency, information incorporation; high-frequency data ch.5) ; Balch ML4T lectures on signal horizon, execution/latency, and realistic backtesting.

### [QF2-D1G7Q2] Multiple testing / data snooping
**Scenario:** A team tests 2,000 random indicators and promotes the highest in-sample Sharpe; the winner has no economic rationale but a strong backtest. The CIO asks whether searching many alternatives changes how to interpret the result.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: testing many noisy candidates increases the chance that at least one looks successful by luck — multiple testing produces extreme apparent winners even with no genuine signal. |
| B | True (incorrect) | Wrong: selecting the best in-sample indicator makes its reported performance optimistically biased, not unbiased. |
| C | False (accurate) | Correct: a held-out test set (data excluded from selection) offers more credible evidence about whether the pattern generalizes. |
| D | False (accurate) | Correct: repeatedly checking the same test set while revising the indicator turns that set into part of selection, leaking information into model development. |
| E | True (incorrect) | Wrong: lack of economic rationale does not prove zero predictive value — rationale affects plausibility/confidence, but predictive value is an empirical question. |

**Reference:** Tsay, *Analysis of Financial Time Series*, ch.1 (statistical inference pitfalls; §2.x hypothesis testing on autocorrelations); Balch ML4T lectures on overfitting, data snooping / multiple testing, and in-sample vs. out-of-sample validation.

### [QF2-D1G7Q3] Gross forecast vs. net realizability
**Scenario:** A low-turnover signal gives a small but consistent forecast across many names; a competing high-frequency signal has a larger gross forecast but decays within seconds and needs heavy trading. The PM wants to choose by forecast magnitude; the head trader emphasizes realizability.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: a larger gross forecast need not produce a larger net return — latency, turnover, spread, slippage, and impact can consume it. |
| B | False (accurate) | Correct: signal decay and trading cost should be evaluated together, because the signal must survive long enough to be captured at acceptable cost. |
| C | False (accurate) | Correct: a persistent signal can remain useful with slower execution even if its instantaneous forecast is smaller — a longer useful life eases and cheapens implementation. |
| D | True (incorrect) | Wrong: high-frequency observations do not automatically give independent evidence — nearby observations can be highly dependent, so row count overstates effective information. |
| E | False (accurate) | Correct: a weak signal observed repeatedly can still be valuable if it is sufficiently stable, scalable, and cheap to implement — realizable value depends on repeatability and implementation, not just magnitude. |

**Reference:** Tsay, *Analysis of Financial Time Series*, ch.1 (returns, transaction costs context) and §2.1 (dependence inflating effective sample size); Balch ML4T lectures on transaction costs, turnover, signal decay, and realistic net-of-cost backtesting (01-07, 01-04).

## References (domain-level)

1. **Tsay — *Analysis of Financial Time Series*:** §1.2 (returns of assets — simple vs. continuously compounded/log returns, multiperiod compounding, why returns rather than price changes are the comparable unit); §1.3 (distributional properties of returns — heavy/fat tails, excess kurtosis); ch.2 §2.1 (stationarity, time-varying moments, nonstationary/unit-root processes, spurious regression, structural breaks) and §2.2 (autocorrelation function, serial correlation, testing); ch.3 (conditional heteroscedastic models — ARCH/GARCH, volatility clustering) and ch.4/ch.10 (regime switching, multivariate/time-varying volatility and correlation) for the volatility-regime questions; ch.5 (high-frequency data) and ch.1 (market efficiency / information incorporation) for signal-decay context. Section-level only; no specific page numbers are asserted.
2. **Balch — ML4T (Georgia Tech), 01-xx mini-course / Time Series lecture:** 01-01 and 01-02 (reading, combining, and normalizing stock price data to a common base); 01-04 (statistical analysis of time series — daily and cumulative returns, rolling mean/standard deviation, Bollinger Bands, rolling volatility, and the look-ahead-bias caution for centered windows); 01-05 (incomplete/adjusted data — split- and dividend-adjusted prices); 01-06 (histograms, return distributions, fat tails/kurtosis); 01-07 (Sharpe ratio and portfolio statistics, with time-series stability caveats). ML4T backtesting/strategy lectures are referenced at the section level for look-ahead bias, train/test discipline, transaction costs/turnover, overfitting and data snooping. No invented lecture numbers beyond the 01-xx series and the general backtesting lectures.

> **Source-fidelity note:** All A–E verdicts above are transcribed verbatim from `slices/QF2_D01.txt` (never flipped). Inverted-polarity items (G1Q1, G2Q3, G3Q1, G4Q1, G5Q2, G5Q3, G6Q2, G7Q2, G7Q3) are rendered as "True (incorrect)" / "False (accurate)" to match the slice's "True – the quoted statement is incorrect" / "False – the quoted statement is correct" answer-key wording. The source text contains `fi`/`fl` **ligature glyphs** (ﬁ, ﬂ) in words such as "signiﬁcance," "ﬁnishes," "ﬂuctuations," "proﬁtability," "diversiﬁcation," and "conﬁdence"; these were normalized to plain `fi`/`fl` here. They are a PDF-extraction artifact, not content errors, and no verdicts or statement meanings were affected.
