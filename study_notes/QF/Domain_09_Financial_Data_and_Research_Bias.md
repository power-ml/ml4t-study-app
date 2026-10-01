# QF Domain 9 — Financial Data and Research Bias

## Domain cheat-sheet

- **Time-series ordering / look-ahead bias**: a backtest may only use information that was *actually available* at the simulated decision time. Any feature, label, or preprocessing step that pulls in future data leaks look-ahead bias and inflates results.
  - **Random train/test splits break chronology** — they let 2025 rows sit in "training" while 2012 rows sit in "testing," which does NOT simulate deploying in 2012. Autocorrelation between nearby observations also makes randomly split samples unusually similar → over-optimistic scores.
  - **Chronological (train-early / test-late) splits** preserve the direction of time and better represent live deployment.
  - **Centered windows leak the future** (a centered 21-day moving average uses 10 future closes); a **trailing window** uses only past data. Even a trailing feature must be **shifted/lagged** if the current bar's close was not yet known at the decision moment. Feature timing must match the exact time the simulated order could have been placed.
  - **Overlapping labels near a train/test boundary leak** — a 5-day-forward label dated June 30 contains July returns. **Purging** (dropping boundary observations whose label windows cross into the test period) reduces this; longer horizons need *wider* separation. Shuffling rows does not fix overlap (shared future information remains).
  - Using only lagged features does NOT by itself guarantee a leak-free design — leakage can enter via splitting, preprocessing, labels, or universe construction.
- **Survivorship bias**: testing only securities/funds that survived to today (current index members, live hedge funds) systematically omits failures, **overstating returns and understating losses/volatility**. Closure/delisting is correlated with poor performance, so the missingness is *systematic*, not random. Fix with **point-in-time constituent** and **dead-fund** databases; adding more history for the same survivors does NOT restore the missing names.
- **Selection bias**: choosing the market/period/subsample *after* observing results (reporting the 3 best of 20 countries, best decade) overstates how a pre-specified rule would perform. A strong selected subsample does not prove universality. Disclosing the full search and testing on **untouched** data/markets provides genuine validation.
- **Data snooping / multiple testing**: testing many strategies and keeping the "significant" ones manufactures false discoveries. At a 5% threshold, ~50 of 1,000 truly-null signals look significant *by chance*. Selecting the best of many trials is NOT the same as testing one pre-specified strategy. **Multiple-testing corrections** account for the number/structure of hypotheses; a p<0.05 on a mined signal does not prove durable economic value. Retained signals must be validated on data that did not participate in their selection.
- **Reusing the holdout ("p-hacking")**: repeatedly tweaking parameters against the same "test" set until Sharpe looks good makes the holdout part of model development — it is no longer independent. Calling data a "test set" doesn't preserve independence; *functional use* does. Keep a log of all variants; final evaluation must be on a truly untouched dataset. **Winner's curse**: the max of many noisy estimates overstates true performance; freezing the specification before further testing prevents new tuning on validation data. Replication across later periods/markets is stronger evidence than the in-sample result; broad failure suggests the effect did not generalize.
- **Point-in-time (PIT) data and revisions**: financial statements, EPS, and macro series (GDP) get **restated/revised** years later. Using the latest-vintage series as if it were known on the original date embeds hindsight. **Economic reference period ≠ public availability date**: a fiscal year ending Dec 31 with a March 15 release cannot be traded on Jan 2. A PIT / real-time vintage database preserves original releases, revisions, and availability dates. "Cleanest current series" ≠ most realistic historical simulation. Add a conservative processing/execution delay after release.
- **Corporate actions and price adjustments**:
  - **Splits**: a 2-for-1 split halves per-share price and doubles share count → position value ~unchanged; unadjusted prices record a spurious −50% "return." Split-adjusted series place pre/post prices on a comparable basis; total market cap is ~unchanged (not doubled).
  - **Dividends**: a $2 dividend with a $2 ex-date price drop is ~0% total return, but a price-only series shows −4%. Dividend-adjusted **total-return** series capture distributions. Dividends (cash distribution) and splits (unit change) are *different* actions.
  - **Delistings**: ending a series at the last exchange quote ($4) when the investor recovered only $0.50 omits a real −87.5% loss → survivorship-style upward bias. Investigate delisting codes and terminal recovery values rather than treating the last quote as full value.
- **Missing, stale, and irregular data**:
  - **Forward-filling** a non-trading price repeats the last value → artificial zero returns, then a jump when a real trade prints; this understates measured volatility/autocorrelation and biases correlations. A stale quote ≠ an executable price (liquidity, spreads, depth matter).
  - **Non-synchronous calendars**: filling a U.S. holiday with the prior close and aligning it to a foreign market that traded distorts the "same-day" relationship (returns cover different information intervals). Align common trading intervals or model lead-lag.
  - **Informative missingness**: if firms omit a disclosure when results are poor, missingness carries information. **Mean imputation** attenuates the true signal and falsely assumes missing-at-random; imputed values are modeling choices, not observations. Add a **missingness indicator** and run sensitivity analyses.
- **Nonstationarity and regime change**: return distributions and relationships shift over time (structural breaks, strategy decay). A historical beta need not hold after a firm doubles leverage / changes industry; more data from the *old* regime yields a precise-but-obsolete estimate. Rolling estimates, stability/break tests, and per-regime (stress) reporting reveal instability. A positive full-sample average can mask severe regime-specific tail losses (e.g., a short-vol strategy's 2020 loss); dropping an adverse-but-relevant regime is itself selection bias. Widespread adoption can shrink/accelerate an edge below net-profitability after costs; retraining does not *guarantee* useful structure exists in the new regime.

## Common traps

- **No inverted-logic questions in this domain.** Every question in this slice uses the standard Answer Key form ("A. True – ..." / "B. False – ...", True = accurate). There is no "True = incorrect; False = accurate" polarity flip here — but always re-read each Answer Key line before trusting that.
- **Negation-flip distractors are the dominant trap.** Most *False* choices are phrased as "cannot," "does not," "guarantees," "necessarily," "is irrelevant," or "reverses the correct conclusion." The Answer Key repeatedly tags these False with the note "The statement reverses the correct conclusion." Read each choice for a hidden negation before answering. Examples: G1Q2C, G1Q3D, G2Q1E, G2Q2B/E, G3Q1C, G4Q3B, G5Q1C/D, G6Q1C(no)/G6Q3C, G7Q1D/E, G7Q3A.
- **Embedded double-negative "claim" choice — [QF-D9G4Q2] C.** "A reviewer would be *wrong to accept the claim that* delaying first use until public availability would improve temporal validity." The inner claim is *accurate*, so the choice (which calls it wrong) is **False**. Parse the inner claim, judge its truth, then negate. Same pattern in **[QF-D9G5Q3] E** ("Researchers should *not* investigate delisting codes ... rather than automatically treating the last quote as full value" → False, because they *should* investigate).
- **"It became historical / it's public, therefore it was known" fallacy.** Later availability (a restatement, a delayed 10-K, revised GDP, public data) does NOT make information available at the historical decision time. See G1Q2D, G4Q1C/E, G4Q2D, G4Q3D.
- **Significance / in-sample strength ≠ durable value.** A single low p-value, a max Sharpe among many trials, or a favorable selected subsample does not prove persistence, universality, or net-of-cost profitability (G2Q3C, G3Q1E, G3Q3A/C).
- **"More data" red herrings.** Adding years for the same survivors doesn't remove survivorship bias (G2Q2D); more observations from an obsolete regime just make a stale estimate precise (G7Q1C).

## Questions

### [QF-D9G1Q1] Random split of time-series destroys chronology
**Scenario:** A researcher randomly assigns daily 2010–2025 observations to train/test sets for a model using lagged returns to predict the next day's return.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Reverses the truth: random assignment does *not* preserve chronological order, so it absolutely can put 2025 in training while 2012 is in testing — that is exactly the problem with random splits. |
| B | False | A random split does not simulate training-as-of-2012; future observations can influence a model that is then evaluated on earlier dates (temporal leakage). |
| C | True | Autocorrelation and overlapping regimes make nearby (randomly separated) observations unusually similar, so random-split test scores are over-optimistic. |
| D | True | Training on an earlier period and testing on a later one preserves the arrow of time and better mimics live deployment. |
| E | False | Using only lagged features does not guarantee a leak-free design — leakage can still enter via splitting, preprocessing, labels, or universe construction. |

**Reference:** Look-ahead bias & chronological splits — Investopedia "Look-Ahead Bias"; Lopez de Prado, *Advances in Financial Machine Learning*, ch. 7 (cross-validation in finance).

### [QF-D9G1Q2] Centered moving-average feature leaks future prices
**Scenario:** A feature equals the day's close minus a centered 21-day average (10 prior days, current day, 10 following days), used to trade at that day's close.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Ten *future* closing prices enter the feature that drives the current trade — those prices were unavailable at trade time. |
| B | True | The centered calculation lets future information affect a past decision, the definition of look-ahead bias. |
| C | False | Reverses the truth: replacing the centered window with a *trailing* window uses only information available by the decision time, so it *does* remove this use of future prices. |
| D | False | Later availability is irrelevant — prices that only became historical afterward were not knowable at the original trade time, so the backtest is not valid. |
| E | True | Even a trailing calculation must be shifted/lagged if the day's close was not yet known when the simulated order was placed; feature timing must match execution timing. |

**Reference:** Look-ahead bias in feature construction — Investopedia "Look-Ahead Bias"; Lopez de Prado, *AFML*, ch. 3 (labeling) & ch. 7.

### [QF-D9G1Q3] Overlapping forward-return labels across the train/test boundary
**Scenario:** A model predicts 5-day-forward returns (labels use t+1...t+5). Training ends June 30, testing starts July 1, with no removal of overlapping boundary labels.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | A June 30 label's five-day forward window extends into July, so a training label literally contains test-period returns. |
| B | False | The calendar boundary alone does not separate the economic information — label windows can cross the nominal boundary. |
| C | True | Purging boundary observations whose label windows overlap the test period prevents test-period outcomes from leaking into training labels. |
| D | False | Reverses the truth: longer forward horizons create *longer* overlap regions, so they *do* require wider separation around the boundary. |
| E | False | Shuffling rows only changes order; the shared future-return information in overlapping labels remains, so it does not solve the overlap. |

**Reference:** Purging/embargo for overlapping labels — Lopez de Prado, *AFML*, ch. 7 (purged k-fold CV); Investopedia "Look-Ahead Bias."

### [QF-D9G2Q1] Backtest on current index members (survivorship)
**Scenario:** A strategy is tested on today's members of a major index, 2005–2025; removed/bankrupt firms are excluded, and results look unusually strong.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The sample contains only firms that survived into the present universe — the textbook setup for survivorship bias. |
| B | True | Systematically omitting failed firms drops the poor outcomes, inflating measured historical performance. |
| C | False | Today's membership was not known or available in 2005, so it does not recreate the historical opportunity set. |
| D | True | A point-in-time constituent database reconstructs who was actually in the index at each date, improving the design. |
| E | False | Reverses the truth: omitting failures can distort *both* return estimates *and* apparent risk (understating losses and volatility). |

**Reference:** Survivorship bias — Investopedia "Survivorship Bias"; CFA curriculum (backtesting / data biases).

### [QF-D9G2Q2] Surviving-hedge-fund database
**Scenario:** An analyst studies today's operating hedge funds back to inception; funds that closed before the download date are absent.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Requiring current operation conditions the sample on survival to today. |
| B | False | Reverses the truth: poorly performing funds *are* more likely to close and disappear, making the missingness systematic, not random. |
| C | True | Omitting failed funds raises the measured average return and suppresses observed downside relative to what a real investor faced. |
| D | False | Adding more history for the *same* surviving funds does not restore the missing (dead) funds, so it does not remove the bias. |
| E | False | Reverses the truth: a database that includes dead funds and their final returns *does* support a less biased analysis. |

**Reference:** Survivorship bias in fund data — Investopedia "Survivorship Bias"; CFA curriculum (hedge-fund performance databases).

### [QF-D9G2Q3] Reporting the best 3 of 20 countries (selection bias)
**Scenario:** After inspecting 20 countries over 30 years, a researcher reports a value strategy only for the 3 best countries and 1 best decade, without disclosing how they were chosen.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Choosing which evidence to present *after* seeing outcomes is selection bias — the result influenced the sample. |
| B | True | Cherry-picking winners from many candidates favors unusually strong realized results, overstating pre-specified performance. |
| C | False | A favorable selected subsample does not establish general validity; it may be luck from a wide search. |
| D | False | Reverses the truth: disclosing the full search *does* help readers gauge how many opportunities produced the apparent winner. |
| E | True | Testing the pre-specified rule on untouched countries or later dates checks whether the finding generalizes. |

**Reference:** Selection/data-snooping bias — Investopedia "Data Snooping"; Bailey & Lopez de Prado (backtest overfitting; multiple trials).

### [QF-D9G3Q1] 1,000 signals with no true power (multiple testing)
**Scenario:** A team tests 1,000 truly-null signals and keeps every one significant at the 5% level.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Under the simplified assumption, 5% of 1,000 true nulls ≈ 50 false positives arise by chance. |
| B | False | Selecting the best of 1,000 trials is *not* equivalent to testing one pre-specified strategy — the search vastly raises the chance of a lucky winner. |
| C | False | Reverses the truth: multiple-testing adjustments *do* reduce false discoveries by accounting for the number/structure of hypotheses tested. |
| D | True | Retained signals must be evaluated on data that did not participate in their selection (independent validation). |
| E | False | A single p<0.05 on a selected signal can be spurious; it does not prove persistence, magnitude, or profitability after costs. |

**Reference:** Multiple testing / deflated Sharpe — Bailey & Lopez de Prado, "The Probability of Backtest Overfitting"; Investopedia "Data Snooping."

### [QF-D9G3Q2] Repeatedly tuning against the same holdout (p-hacking)
**Scenario:** A developer reruns the same nominal holdout, changing parameters after each disappointing result, until the Sharpe looks attractive.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Reverses the truth: the holdout *is* becoming part of model development, because its outcomes are guiding design choices. |
| B | True | Repeated feedback lets the developer fit dataset-specific noise — overfitting to the holdout. |
| C | False | Labeling data a "test set" does not preserve independence; functional use (guiding revisions) determines it. |
| D | True | A final evaluation on a truly untouched dataset gives a more credible generalization estimate. |
| E | True | Logging all attempted variants makes the extent of the search (multiple testing / researcher degrees of freedom) transparent. |

**Reference:** Data-snooping / p-hacking — Investopedia "Data Snooping"; Bailey & Lopez de Prado (backtest overfitting).

### [QF-D9G3Q3] Max-Sharpe specification, then out-of-sample validation
**Scenario:** A strategy chosen for the highest Sharpe among 200 U.S.-equity variants is then evaluated, unretuned, on later U.S. data and several international markets.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Reverses the truth: the max Sharpe of many noisy estimates *is* subject to a winner's curse — the best of many overstates true performance. |
| B | True | Freezing the specification before further testing prevents validation outcomes from being turned into more tuning (avoids selection on validation data). |
| C | False | Failure in every new dataset would *weaken*, not strengthen, the robustness claim — it suggests the original result did not generalize. |
| D | False | Reverses the truth: success across later periods and different markets *is* more persuasive than the selected in-sample result alone (replication evidence). |
| E | True | International validation is informative only if market-structure, cost, instrument, and implementation differences are considered. |

**Reference:** Winner's curse / out-of-sample replication — Bailey & Lopez de Prado (backtest overfitting); CFA curriculum (out-of-sample testing).

### [QF-D9G4Q1] Vendor EPS series with later restatements (point-in-time)
**Scenario:** A 2026 backtest uses a vendor's current historical EPS series that already incorporates restatements issued years after the original reports, assuming each revised value was known on the original quarter-end.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Treating later restatements as historically known injects information investors did not have on the decision date. |
| B | True | Restated data can differ from the values originally reported. |
| C | False | The economic reference period (the quarter described) and the public availability date are distinct, so assigning a value to its quarter ≠ assigning it to when it was first observable. |
| D | True | A point-in-time database preserves original releases, revisions, and availability dates so the researcher can reconstruct what was knowable at each date. |
| E | False | The cleanest current series may be accurate retrospectively but unrealistic for contemporaneous decisions, so it does not necessarily give the most realistic simulation. |

**Reference:** Point-in-time data & restatements — Investopedia "Point-in-Time Data"; CFA curriculum (data preparation / look-ahead bias).

### [QF-D9G4Q2] Trading annual statements before their release date
**Scenario:** A strategy ranks firms on annual statements (fiscal year ends Dec 31, released March 15) but first trades Jan 2 using the completed fiscal-year figures.
**Answer polarity:** Normal (True = accurate). **Embedded double-negative in C.**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The figures were not released until March 15, so a Jan 2 trade uses them before their stated release date. |
| B | False | Reverses the truth: the ~2.5-month publication lag *is* economically relevant — the strategy cannot use a disclosure while it remained unavailable. |
| C | False | Embedded double-negative: the inner claim (delaying first use until public availability improves temporal validity) is *correct and should be accepted*, so saying a reviewer "would be wrong to accept" it is false. |
| D | False | The measurement period (year ending Dec 31) does not determine the publication date, so investors did not know the figures on Dec 31. |
| E | True | A conservative extra processing/execution delay is appropriate because the strategy could not trade instantaneously at release. |

**Reference:** Publication lag / availability dates — Investopedia "Look-Ahead Bias" & "Point-in-Time Data"; CFA curriculum (data timing).

### [QF-D9G4Q3] Latest-vintage GDP traded on original announcement dates
**Scenario:** A macro strategy uses the latest historical GDP-growth series to trade each original announcement date, though several past estimates were materially revised after those trades.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The latest-vintage series may embed revisions that were unavailable on the original announcement dates. |
| B | False | Reverses the truth: a real-time *vintage* database is precisely what preserves the values actually published at each historical date. |
| C | True | Macro revisions can change both the model's inputs and the apparent historical strength of the signal. |
| D | False | Public data can still be revised after the historical decision point, so "public" does not make revision bias impossible. |
| E | True | Comparing initial-release vs. later-revised results reveals whether the backtest depends on hindsight-cleaned data (vintage sensitivity). |

**Reference:** Real-time/vintage macro data — Investopedia "Point-in-Time Data"; CFA curriculum (data revisions).

### [QF-D9G5Q1] 2-for-1 split recorded as −50% on unadjusted prices
**Scenario:** A $100 stock splits 2-for-1 overnight, opens near $50 with each share replaced by two; a program using unadjusted prices records a −50% return.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Two shares near $50 replace one near $100, so the apparent decline is not a 50% economic loss to the shareholder. |
| B | True | Ignoring the change in share count mistakes a unit-of-account change for a real loss — a false return signal. |
| C | False | Reverses the truth: a properly split-adjusted series *should* remove this mechanical discontinuity by placing pre/post prices on a comparable basis. |
| D | False | Reverses the truth: position value *is* approximately unchanged — shares double while per-share price roughly halves. |
| E | False | Shares outstanding and price adjust inversely, so market cap is ~unchanged (absent other news), not doubled. |

**Reference:** Corporate-action (split) adjustment — Investopedia "Adjusted Closing Price" / stock splits; CFA curriculum (return calculation).

### [QF-D9G5Q2] Dividend vs. price-only return
**Scenario:** A $50 stock pays a $2 dividend and closes next day at $48 with no other news; one backtest uses price returns only, another includes the dividend.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Reverses the truth: the price-only return *is* −4% = ($48 − $50)/$50. |
| B | True | Total return ≈ 0%: ($48 + $2 − $50)/$50, since the $2 dividend offsets the $2 price decline (before taxes/costs). |
| C | True | Treating the ex-dividend price drop as a pure loss ignores the cash received, understating total return. |
| D | True | A dividend-adjusted total-return series is appropriate when the investor receives and retains or reinvests distributions. |
| E | False | Dividend adjustments (a cash distribution) and split adjustments (a change in share units, no cash) address different actions. |

**Reference:** Total-return vs. price return, dividend adjustment — Investopedia "Total Return" / "Adjusted Closing Price"; CFA curriculum (return measurement).

### [QF-D9G5Q3] Delisting recovery omitted from the series
**Scenario:** A distressed stock last trades at $4, is delisted, and the dataset ends the return history there with no delisting return — but the investor actually receives $0.50 in liquidation.
**Answer polarity:** Normal (True = accurate). **Embedded negative phrasing in E.**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Ending the series at $4 omits the substantial further loss down to the $0.50 recovery. |
| B | False | Reverses the truth: the economic return *is* −87.5% = ($0.50 − $4.00)/$4.00. |
| C | True | Omitting adverse delisting outcomes creates survivorship-related upward bias, since disappearing securities often have poor terminal outcomes. |
| D | False | The terminal value the investor realizes remains part of portfolio performance even after exchange trading stops. |
| E | False | Reverses the truth (double-negative): researchers *should* investigate delisting codes, cash recoveries, and terminal returns rather than treating the last quote as full value. |

**Reference:** Delisting returns & survivorship — Investopedia "Survivorship Bias" / delisting; CFA curriculum (data handling).

### [QF-D9G6Q1] Forward-filling an illiquid bond
**Scenario:** An illiquid bond last trades at $100 Monday, does not trade Tue–Thu (dataset forward-fills $100 while peers decline), then trades Friday at $94.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Repeating $100 mechanically produces zero recorded daily returns for Tue–Thu. |
| B | False | Absence of a trade does not prove the tradable market value stayed constant — the filled price is not evidence of unchanged value. |
| C | False | Reverses the truth: forward-filling *does* defer the accumulated price change until Friday, when a new transaction price arrives. |
| D | True | Artificial zero returns followed by a jump distort measured daily volatility and autocorrelation. |
| E | True | A stale quote can differ from a price at which the full position could actually trade (executable value depends on liquidity, spreads, depth). |

**Reference:** Stale prices / forward-filling — Investopedia "Stale Price"; Lopez de Prado, *AFML* (data structuring / illiquidity).

### [QF-D9G6Q2] Non-synchronous U.S./foreign calendars
**Scenario:** On a U.S. holiday the ETF does not trade but the foreign index does; the researcher fills the ETF with its prior close and treats same-calendar-date returns as synchronized.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Reverses the truth: the unchanged filled price *does* create a mechanical zero return for the holiday. |
| B | False | Reverses the truth: different trading calendars *do* create non-synchronous observations (one market open, one closed). |
| C | True | The apparent same-day relationship is distorted because the two returns cover different information intervals (news incorporated at different times). |
| D | False | Forward filling does not guarantee an unbiased correlation — artificial zeros and timing mismatch bias it. |
| E | True | Aligning common trading intervals or explicitly modeling lead-lag timing improves the analysis. |

**Reference:** Non-synchronous trading / calendar mismatch — Investopedia "Stale Price" / non-synchronous data; CFA curriculum (data alignment).

### [QF-D9G6Q3] Informative missingness and mean imputation
**Scenario:** Firms omit a newly requested disclosure when results are poor; a researcher replaces every missing value with the cross-sectional mean and treats missingness as random.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Because poor performers are described as more likely to omit the value, the missingness itself carries information about firm performance. |
| B | True | Replacing systematically poor observations with an average attenuates or hides the relationship between the disclosure and poor outcomes. |
| C | False | Imputed values are modeling choices, not genuine observations of what the firms would have reported. |
| D | True | A missingness indicator can capture the information carried by the absence itself, letting you test whether missing records have distinct outcomes. |
| E | False | Reverses the truth: sensitivity analyses under alternative missing-data assumptions *do* improve credibility by showing how much conclusions depend on the imputation rule. |

**Reference:** Missing-not-at-random / imputation bias — CFA curriculum (data cleaning / missing data); Investopedia (data-cleaning bias).

### [QF-D9G7Q1] Stale beta after a leverage/industry change
**Scenario:** A stock's beta was 0.8 in a long low-vol period; after a major acquisition it doubles leverage and changes industries, but the risk system keeps the old estimate indefinitely.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Beta depends on business and financial exposures that can change, so the historical estimate need not stay valid. |
| B | True | A major acquisition and leverage change can be a structural break — the return-generating process may differ before/after. |
| C | False | More observations from the *old* regime make an estimate precise for a relationship that no longer applies — not more accurate for the new regime. |
| D | False | Reverses the truth: rolling estimates and stability/break tests *can* help detect changing exposure. |
| E | False | Reverses the truth: parameter uncertainty *should* be considered, since hedge performance is sensitive to error and drift in the estimated beta. |

**Reference:** Nonstationarity / structural breaks in beta — CFA curriculum (nonstationarity, rolling regressions); Investopedia "Nonstationary."

### [QF-D9G7Q2] Short-vol strategy — full-sample average hides regime risk
**Scenario:** A short-volatility strategy is steady 2012–2019, suffers a severe 2020 loss, recovers in later calm markets, and is proposed for deployment because its full-sample average return is positive.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | A positive full-sample average can conceal materially different regime-specific risks (aggregation masks tail losses). |
| B | True | The 2020 loss is important evidence about the strategy's exposure to stressed conditions (short-vol accumulates gains but is exposed to rare shocks). |
| C | False | Removing 2020 solely because it is unfavorable is selection bias — excluding an economically relevant regime does not improve validity. |
| D | True | Stress testing and per-regime reporting provide information beyond the overall mean (whether the edge depends on a particular environment). |
| E | False | Recovery in calm markets does not prove future crisis losses cannot recur — the underlying exposure remains. |

**Reference:** Regime-conditional / stress analysis — CFA curriculum (scenario & stress testing); Lopez de Prado, *AFML* (strategy risk under regimes).

### [QF-D9G7Q3] Mean-reversion decay after crowding
**Scenario:** A mean-reversion relationship was stable under high costs and few participants; after market-structure changes and widespread algorithm adoption, deviations become smaller and reverse faster than the strategy can execute.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Reverses the truth: changes in market structure and competitor behavior *can* cause strategy decay by altering available opportunities. |
| B | False | A historically existing relationship need *not* remain stationary once widely exploited — crowding and institutional change can remove it. |
| C | True | Smaller, faster deviations can eliminate net profitability after costs even if some mean reversion remains (the gross edge is too small/brief to capture). |
| D | True | Monitoring live feature distributions, execution quality, and performance helps detect drift between training and deployment. |
| E | False | Retraining does not *guarantee* adaptation — it cannot ensure useful predictive structure exists or that the new sample represents future regimes. |

**Reference:** Strategy decay / nonstationarity & crowding — Lopez de Prado, *AFML* (backtesting, strategy decay); CFA curriculum (nonstationarity).

## References (domain-level)

1. **Lopez de Prado — *Advances in Financial Machine Learning*:** ch. 7 (purged/embargoed cross-validation, why random splits leak in time series), ch. 3 (labeling, meta-labeling), ch. 11–12 (backtesting pitfalls, backtest overfitting, strategy decay) — core for look-ahead bias, overlapping labels, and multiple-testing on backtests.
2. **Bailey & Lopez de Prado — backtest-overfitting work** ("The Probability of Backtest Overfitting"; deflated Sharpe ratio; "Pseudo-Mathematics and Financial Charlatanism"): multiple testing, selection bias, winner's curse, and why the max Sharpe of many trials overstates true performance.
3. **CFA Institute curriculum (Quantitative Methods / Backtesting & Simulation, Big Data / Data Science):** survivorship and look-ahead bias, point-in-time data, data snooping, out-of-sample and stress testing, nonstationarity and structural breaks.
4. **Investopedia — bias & data reference articles:** "Survivorship Bias," "Look-Ahead Bias," "Data Snooping," "Point-in-Time Data," "Stale Price," "Adjusted Closing Price"/stock splits, and "Total Return" — plain-language definitions for each trap in this domain.
