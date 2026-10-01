# QF Domain 6 — Strategy Evaluation & Performance Attribution

## Domain cheat-sheet

- **Benchmark selection — relevance, not convenience.** A benchmark is the yardstick that separates *skill* from *ordinary exposure you could have bought cheaply*. Choose it by the **decision problem, opportunity set, and risk profile** of the strategy — never because it happens to show the strategy in the best light.
  - **Cash / risk-free rate** = the opportunity cost of capital with little market exposure. Useful for *any* strategy (especially low-beta / market-neutral ones), but it does **not** match the equity risk of a fully-invested long-only book, so "beat cash by X" overstates skill.
  - **A comparable asset-class index** (e.g., a broad large-cap index for a large-cap long-only book) resembles the strategy's investment universe and market exposure, so it separates **general market gains from strategy-specific value**. Beating cash by 9 points while beating the comparable index by only 1 point is the tell that most of the return was market beta, not selection.
  - **Passive buy-and-hold of the traded asset** tests whether an active/learned policy improves on *passive exposure*; a **simple transparent active rule** (e.g., a moving-average crossover) tests whether added complexity beats an *implementable simple rule*. Beating buy-and-hold does **not** make the simple-active comparison unnecessary.
  - **Factor / market-neutral benchmarks** test whether *known factor exposures* (market, size, value, momentum) explain the return. The S&P 500 alone is a poor risk match for a near-zero-beta strategy. **Multiple relevant benchmarks** (opportunity cost + systematic exposure + implementable active rule) are more informative than one convenient one.
  - **Fair comparison** = identical dates, identical starting capital, identical cost assumptions. A return *difference* alone never identifies its *cause* or establishes skill, and a 1-point edge is **not** automatically statistically significant — significance depends on the variability, serial dependence, and number of relative-return observations.
- **In-sample (IS) vs. out-of-sample (OOS) & backtest overfitting.** IS = any data that *influenced* indicator choice, lookbacks, thresholds, or tuning (the model-development sample). OOS = data that did **not** inform the frozen specification.
  - **Strong IS performance never establishes generalization** — it may be fitted noise; it must be checked on untouched data. OOS can be worse precisely because IS choices fit transient relationships.
  - **Freezing the design before examining test results** preserves the test's evidentiary value. The moment the test period feeds back into parameter choices (seeing weak 2024 results, then tweaking parameters), those observations become **part of development** — relabeling them "out-of-sample" cannot undo the information leakage. A fresh holdout or a disciplined **nested / walk-forward** procedure that separates selection from evaluation is required.
  - **Selection bias / multiple testing:** picking the best of N variants (e.g., highest Sharpe of 500) inflates the chosen result — the maximum observed statistic contains selection effects *plus* any genuine skill. More trials ⇒ higher chance one looks strong by luck (the core of **Bailey–López de Prado**: the more configurations tried, the lower the deflated/true Sharpe).
  - **Rolling retraining** (refit each year on prior-year data, record next-year return) is a legitimate forward test *of the updating procedure* — provided **all features also use only information known at decision time** (no lookahead). It does **not** make the annual returns statistically independent (overlapping exposures, persistent regimes, serial correlation create dependence), and repeatedly redesigning after inspecting disappointing segments reintroduces overfitting.
- **Return, volatility, drawdown — three different lenses on the path.**
  - **Cumulative return** compares endpoints: (end − start) / start. $100→$130 = **30%**; $100→$130 vs $100→$125 differ by ending value alone.
  - **CAGR** = (ending/beginning)^(1/years) − 1 — geometric, path-independent between endpoints.
  - **Volatility** = dispersion of periodic returns (standard deviation); **annualize** by ×√(periods per year), e.g., **daily → ×√252**. Equal annual returns do **not** imply equal paths — many return sequences hit the same endpoint.
  - **Maximum drawdown (MDD)** = worst peak-to-trough decline, a **path-dependent** loss measure volatility alone does not convey. $120→$90 is a **−25%** drawdown; recovering $90→$120 needs **+33.3%** (asymmetry of losses). Ending above the initial value does **not** mean full recovery from a *higher* interim peak ($108 is still 10% below the $120 peak). A late recovery does **not** erase the relevance of an earlier drawdown (risk, investor experience, ability to stay invested). Higher ending value is **not** unambiguous superiority once volatility/MDD differ — preference is objective- and risk-tolerance-dependent.
- **Risk-adjusted metrics — match the risk notion to the question.**
  - **Sharpe ratio** = (return − risk-free) / **total volatility**. Penalizes *both* upside and downside deviation (standard deviation is two-sided), so large *positive* swings still inflate the denominator. Example: (10%−2%)/16% = **0.50**; (8%−2%)/8% = **0.75** — the higher-raw-return strategy can have the *lower* Sharpe. Annualize with √252 for daily data. A higher Sharpe does **not** guarantee a smaller max drawdown — different properties.
  - **Sortino ratio** = (return − target) / **downside deviation** — only harmful deviations below the target enter the denominator. Sharpe and Sortino can rank two strategies *differently* even with equal mean and equal total σ, when their downside vs. total variability differ.
  - **Information ratio (IR)** = **active return / tracking error** = mean(active return) / σ(active return). Example: 3%/6% = **0.50**. IR evaluates active return per unit of **benchmark-relative** risk; Sharpe evaluates total excess return per unit of **total** risk. They can be numerically equal yet answer different questions. Changing the benchmark changes both the measured active return *and* the tracking error. (**Grinold & Kahn**: IR ≈ IC × √breadth — the "fundamental law".)
- **Turnover and trading behavior.** Turnover measures *trading intensity* per dollar of portfolio (800% annual = positions largely replaced; 40% = light quarterly rebalance). It diagnoses *implementation demands* but by itself does **not** reveal whether trades are profitable (high turnover can be useful updating *or* unproductive churn).
  - **Equal gross Sharpe ≠ equal net Sharpe** — the high-turnover rule is far more sensitive to spreads, commissions, slippage, and market impact, so identical zero-cost assumptions *conceal* a real disadvantage.
  - Repeated short-horizon **reversals** (buy Mon / sell Tue / buy Wed…) on tiny forecast changes are churn that can consume gross alpha through repeated costs; a **no-trade band** ignores small target changes until the expected benefit exceeds cost. Reducing turnover does **not** guarantee lower risk in every regime (it may leave exposures in place longer).
  - **Net, not gross, is the economically relevant comparison.** A 1.5% gross edge minus 2.0% costs = **−0.5% net** — gross outperformance is *not* sufficient to establish investor value. Matching average market beta does **not** imply matching turnover; longer holding periods cut turnover but trade off responsiveness.
- **Performance attribution — decompose return into exposure vs. skill.**
  - **Factor / CAPM attribution:** expected return from market exposure = r_f + β×(r_m − r_f). A 14% return with β=1.5, r_f=2%, r_m=10% gives 2% + 1.5×8% = **14%** — the entire 4-point edge over the market is **beta**, not alpha. High/leveraged beta magnifies a *rising* market's excess return with no selection skill; a raw return advantage alone never proves positive alpha.
  - **Brinson-style allocation vs. selection:** active return decomposes (additively, by convention) into **allocation** (over/underweighting sectors that out/under-perform), **selection** (picking better names *within* sectors), and interaction/timing effects. 2.5% sector + 1.0% selection − 0.5% timing = **3.0%** total. The aggregate active return alone does **not** reveal *which* source generated it — that is the entire point of attribution.
  - **Dollar neutrality ≠ beta/factor neutrality.** A long high-beta / short low-beta book with zero net dollars still carries positive market beta; a factor regression can reveal positive market and momentum loadings that **explain most of the return**, leaving little residual — which *weakens* a unique-alpha claim. Position labels and net capital can hide economically meaningful factor loadings (**Grinold & Kahn**, factor attribution).
- **Stability, significance, and robustness.**
  - **Concentration:** an 18%/yr result driven almost entirely by two crisis trades (with losses in the other years) is economically dependent on a few extreme observations. Perturbing/removing them is a **sensitivity test**; positive full-period return does **not** guarantee stable subperiod performance. Concentration is not automatic disproof, but it changes the evidence needed.
  - **Statistical vs. economic significance — distinct questions.** Failure to reject a zero-mean null is *limited evidence* for a positive mean; it does **not** prove the true mean is exactly zero (could be low power, noise, dependence, or a genuinely small effect). Conversely, a *statistically* significant edge can still lack **economic** significance if profits don't cover implementation and opportunity costs (expensive infra, tiny dollar profit). The two evaluate different things.
  - **Robustness** = does the finding survive **plausible regimes** (bull/bear/high-vol), **plausible cost assumptions** (2bp optimistic → 8bp plausible), and **small parameter perturbations** (lookback changes)? An edge that vanishes under a plausible cost estimate is economically fragile; sharp result swings from tiny lookback changes signal **parameter instability / overfitting**. Robustness analysis must test dependence on conditions, not merely the preferred specification.

## Common traps

- **Inverted-polarity questions (10 of 21 here).** When the body says "each item asserts that its quoted statement is **incorrect**," the Answer Key verdict is flipped relative to the statement's truth: **True = the quoted statement is wrong; False = the quoted statement is accurate.** Read the polarity line *first*. Inverted here: **G1Q1, G2Q2, G2Q3, G3Q1, G4Q2, G4Q3, G5Q2, G6Q1, G6Q3, G7Q2.** The remaining 11 are Normal (True = accurate).
- **"Beating cash proves selection skill."** False — a fully-invested long-only book earns most of its return from equity beta; the comparable asset-class index, not cash, isolates skill. Reporting only the weaker benchmark flatters the strategy.
- **"A return difference identifies its cause / a 1-point edge is automatically significant."** Both false — a difference never establishes skill or significance; significance needs variability, dependence, and sample size.
- **"Beating buy-and-hold makes the simple-active comparison unnecessary."** False — a learned policy can beat passive exposure yet lose to a simpler implementable active rule.
- **"Strong in-sample performance establishes generalization."** False — it may be overfitting; only untouched data can check it.
- **"Relabeling a touched period 'out-of-sample' restores independence."** False — once results feed back into parameter choices, terminology cannot undo the leakage; use a new holdout or nested evaluation.
- **"Picking the best of many variants is just good tuning."** False — selection across many trials inflates the chosen statistic; the max observed Sharpe overstates expected future Sharpe (backtest overfitting).
- **"Rolling retraining makes annual returns independent."** False — overlapping exposures, persistent regimes, and serial correlation create dependence; and lookahead in *features* breaks the forward test even if training respects chronology.
- **"Higher ending value ⇒ unambiguously superior."** False once volatility and drawdown differ — preference is risk-tolerance-dependent. Equal annual returns do not imply equal paths.
- **"Ending above the starting value ⇒ fully recovered."** False if an interim peak was higher; recovering a 25% drawdown needs +33.3% (loss asymmetry).
- **"A later recovery erases the earlier drawdown's relevance."** False — drawdown governs risk, investor experience, and the ability to stay invested.
- **"Higher raw return ⇒ higher Sharpe; higher Sharpe ⇒ smaller drawdown."** Both false — risk-adjusted and raw rankings can differ; Sharpe and MDD measure different properties.
- **"Sharpe only penalizes downside / large positive gains don't affect it."** False — standard deviation is two-sided, so big upside swings inflate the Sharpe denominator. Sortino is the downside-only metric.
- **"Equal Sharpe and IR of 0.50 ⇒ same question."** False — Sharpe is total-risk, IR is benchmark-relative (tracking error); equal numbers do not merge the questions. Changing the benchmark changes active return and tracking error.
- **"Equal gross Sharpe ⇒ equal net Sharpe."** False — turnover-driven costs hit the high-turnover strategy far harder; zero-cost assumptions hide it.
- **"Gross outperformance ⇒ economic value."** False — 1.5% gross − 2.0% costs = −0.5% net; net is the relevant comparison.
- **"A return above the market proves alpha."** False — β>1 in a rising market produces exactly the extra return with no selection skill (r_f + β×ERP).
- **"The 3% active return reveals its own sources."** False — only attribution separates allocation, selection, and timing.
- **"Zero net dollar exposure ⇒ zero market/factor beta."** False — long high-beta / short low-beta leaves positive market beta; factor regressions expose hidden loadings.
- **"Little residual after factor adjustment strengthens the alpha claim."** Backwards — it means systematic exposures explain the return, *weakening* the unique-alpha claim.
- **"Positive full-period return ⇒ stable subperiods / robustness."** False — concentration in a few trades and regime/cost/parameter sensitivity can hide behind a positive aggregate.
- **"Failure to reject zero mean proves the mean is zero."** False — it may be low power, noise, dependence, or a small effect.
- **"Statistical significance = economic significance."** False — a detectable edge can still fail to cover implementation and opportunity costs.

## Questions

### [QF2-D6G1Q1] Benchmark relevance — reporting only versus cash
**Scenario:** A long-only, nearly fully-invested large-cap U.S. equity strategy earns 12%; cash earns 3% and a broad large-cap index earns 11%. The researcher reports only the comparison with cash.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: cash is a useful reference for the return available with little market exposure — a low-risk opportunity-cost benchmark — even though it does not match the strategy's equity risk. |
| B | False (accurate) | Correct: the broad large-cap index resembles the strategy's investment universe and market exposure, so it helps separate general market gains from strategy-specific value. |
| C | True (incorrect) | Wrong: beating cash by 9 points does not prove 9 points of selection value — much of the return may be ordinary equity-market exposure rather than selection skill. |
| D | False (accurate) | Correct: reporting only the weaker cash benchmark can make relative performance look more impressive (beats cash by 9 points but the comparable index by only 1). |
| E | True (incorrect) | Wrong: a 1-point edge over the index is not automatically statistically significant — significance depends on the variability, dependence, and number of relative-return observations. |

**Reference:** Grinold & Kahn, *Active Portfolio Management*, 2nd ed., benchmark/active-return and value-added chapters (choosing a relevant benchmark; residual vs. systematic return); Balch ML4T Project 8 (benchmark comparison for a manual/learned strategy).

### [QF2-D6G1Q2] Comparing a learned policy against passive and simple-active alternatives
**Scenario:** A learned trading policy is evaluated against buy-and-hold of the traded asset and a transparent moving-average strategy with similar long/short permissions — same capital, dates, and cost assumptions.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Buy-and-hold is a natural passive alternative for the same asset — it reveals whether the learned policy improves on passive exposure. |
| B | True | The moving-average rule is a simple implementable active benchmark that tests whether added model complexity beats a simpler active rule. |
| C | True | Identical dates and cost assumptions reduce differences caused by timing or accounting choices, improving fairness. |
| D | False | Beating buy-and-hold does not make the manual-strategy comparison unnecessary — the policy may beat passive exposure yet fail to outperform a simpler active rule. |
| E | False | A benchmark should be chosen by the decision problem, opportunity set, and risk — not because it had the lowest realized return in the test period. |

**Reference:** Grinold & Kahn, 2nd ed., benchmark-selection discussion; Balch ML4T Project 8 (benchmark + manual-strategy comparison under common cost/date assumptions).

### [QF2-D6G1Q3] Market-neutral strategy — one convenient benchmark vs. several relevant ones
**Scenario:** A market-neutral long-short strategy (near-zero estimated market beta) earns 7% and is compared only with the S&P 500 (5%); risk-free is 3%. A reviewer proposes also comparing with cash and a market-neutral factor benchmark.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The S&P 500 carries substantial equity beta whereas the strategy is designed to have near-zero beta, so it is a poor risk match. |
| B | True | Cash is a useful opportunity-cost reference for a low-beta strategy intended to generate return without relying on market direction. |
| C | True | A market-neutral factor benchmark can identify whether known factor exposures explain the return (distinguishing novelty from compensation for known systematic risk). |
| D | False | Earning more than the index does not establish that market neutrality *caused* the extra 2% — a return difference alone identifies neither cause nor skill. |
| E | True | Multiple relevant benchmarks (passive opportunity cost, systematic exposure, active implementation) give more informative evaluation than one convenient benchmark. |

**Reference:** Grinold & Kahn, 2nd ed., factor models and benchmark-relative risk; Balch ML4T Project 8 (choosing benchmarks matched to a strategy's risk profile).

### [QF2-D6G2Q1] In-sample design, out-of-sample test on a frozen strategy
**Scenario:** A team uses 2015–2021 data to choose indicators, lookbacks, and thresholds, freezes the strategy, and evaluates it once on untouched 2022–2024 data.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | 2015–2021 is in-sample because it influenced strategy design — data used for selection or tuning are part of the development sample. |
| B | True | The untouched 2022–2024 period is out-of-sample for the frozen strategy — those observations did not inform the specification. |
| C | False | Strong in-sample performance alone does not establish generalization — it may reflect overfitting and must be checked on unseen data. |
| D | True | Freezing the design before examining test results preserves the test's evidentiary value by preventing feedback into the evaluated version. |
| E | True | Out-of-sample performance can be worse because in-sample choices may have fit noise or transient relationships. |

**Reference:** Bailey & López de Prado, "The Probability of Backtest Overfitting" / "Pseudo-Mathematics and Financial Charlatanism" (IS vs. OOS, overfitting); Balch ML4T Project 8 (in-sample vs. out-of-sample testing).

### [QF2-D6G2Q2] Selecting the best of 500 variants, then re-tuning on the test year
**Scenario:** A researcher tests 500 parameter combinations on 2018–2023 and selects the highest-Sharpe one; after weak 2024 results, changes two parameters and reports the improved 2024 performance as out-of-sample.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: selecting the best of 500 variants creates strategy-selection bias — searching many alternatives raises the chance one looks strong because of noise. |
| B | False (accurate) | Correct: the selected strategy's in-sample Sharpe can overstate its expected future Sharpe because the maximum observed result contains selection effects plus any genuine skill. |
| C | False (accurate) | Correct: once 2024 results influence parameter changes, 2024 is no longer untouched test data — the feedback makes those observations part of development. |
| D | True (incorrect) | Wrong: labeling the revised strategy's 2024 performance "out-of-sample" does not restore independence — terminology cannot undo information leakage from the test period. |
| E | False (accurate) | Correct: a later untouched period or disciplined nested evaluation would be needed for a cleaner test — separating selection from evaluation provides less contaminated evidence. |

**Reference:** Bailey & López de Prado (deflated Sharpe ratio; the more configurations tried, the lower the true expected Sharpe; information leakage); Balch ML4T Project 8 (overfitting a backtest).

### [QF2-D6G2Q3] Rolling annual retraining as a forward test
**Scenario:** A model is retrained at the start of each year using only prior-year data, then its return is recorded during the following year without further changes until the next retraining.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: the design respects chronological availability only if all features also use information known at each decision time — both training and feature construction must avoid future information. |
| B | False (accurate) | Correct: each following-year segment is a forward test of the model fitted before that year began — the model is specified from earlier observations. |
| C | True (incorrect) | Wrong: retraining does not necessarily make the annual test returns independent — overlapping exposures, persistent regimes, and serially correlated returns can create dependence. |
| D | False (accurate) | Correct: combining the annual forward segments evaluates the realistic rolling updating *procedure*, not one permanently fixed model. |
| E | False (accurate) | Correct: repeatedly redesigning the procedure after inspecting disappointing forward segments would weaken the evaluation — post-hoc changes adapt to purported test evidence. |

**Reference:** Bailey & López de Prado (walk-forward / backtest overfitting; dependence in financial series); Balch ML4T Project 8 (rolling retraining and lookahead-bias avoidance).

### [QF2-D6G3Q1] Comparing two strategies on return, volatility, and drawdown
**Scenario:** Both begin at $100. Strategy A ends at $130 (vol 28%, max drawdown 35%); Strategy B ends at $125 (vol 12%, max drawdown 10%).
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: Strategy A's cumulative return is ($130 − $100)/$100 = 30%. |
| B | False (accurate) | Correct: Strategy B's cumulative return is ($125 − $100)/$100 = 25%. |
| C | True (incorrect) | Wrong: A is not unambiguously superior — it also has materially greater volatility and drawdown, so preference depends on the objective and risk tolerance. |
| D | False (accurate) | Correct: maximum drawdown captures a peak-to-trough loss that volatility alone may not convey — the severity of a realized decline from a prior peak. |
| E | False (accurate) | Correct: investors with different risk tolerances could reasonably prefer different strategies — the return/loss tradeoff is investor-dependent. |

**Reference:** Balch ML4T Project 8 (portfolio statistics — cumulative return, volatility, maximum drawdown; interpreting return vs. risk measures).

### [QF2-D6G3Q2] Drawdown and recovery arithmetic
**Scenario:** A portfolio rises $100→$120, falls to $90, and recovers to $108 by the end of the test (ignore external cash flows).
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The decline from $120 to $90 is ($90 − $120)/$120 = −25% drawdown. |
| B | True | Ending cumulative return from $100 is ($108 − $100)/$100 = 8%. |
| C | False | Ending above $100 does not mean full recovery from the $120 peak — at $108 the portfolio is still 10% below the prior peak. |
| D | True | Returning from $90 to $120 requires ($120 − $90)/$90 = 33.3%, which exceeds the 25% drawdown (loss asymmetry). |
| E | True | Maximum drawdown and cumulative return describe different aspects of the path — endpoints vs. intervening peaks and troughs. |

**Reference:** Balch ML4T Project 8 (cumulative return vs. drawdown; path dependence of drawdown and recovery asymmetry).

### [QF2-D6G3Q3] Equal annual returns, different paths
**Scenario:** Strategies X and Y both earn 10%. X: small daily moves, 8% annualized volatility. Y: nearly flat, then a sharp gain after several large losses, 24% volatility and a larger max drawdown.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Equal annual returns do not imply equal paths — many different return sequences produce the same annual endpoint. |
| B | True | Volatility distinguishes the dispersion of their periodic returns — Y's returns vary more strongly under the reported estimates. |
| C | True | Drawdown distinguishes the severity of experienced losses from prior peaks — a path-dependent peak-to-trough measure. |
| D | False | Y's final 10% does not erase its earlier drawdown — drawdown matters for risk, investor experience, and the ability to remain invested. |
| E | True | Reporting return, volatility, and drawdown together describes reward, variability, and realized loss path — more complete than return alone. |

**Reference:** Balch ML4T Project 8 (reporting return, volatility, and drawdown jointly; why equal endpoints hide different risk paths).

### [QF2-D6G4Q1] Sharpe ratios and raw-return vs. risk-adjusted ranking
**Scenario:** Risk-free 2%. Strategy A earns 10% at 16% volatility; Strategy B earns 8% at 8% volatility. Use the simple annual Sharpe = (return − risk-free)/volatility.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Strategy A's Sharpe = (10% − 2%)/16% = 0.50. |
| B | True | Strategy B's Sharpe = (8% − 2%)/8% = 0.75. |
| C | True | A has the higher raw return but B the higher Sharpe — raw-return and risk-adjusted rankings differ. |
| D | True | The Sharpe ratio measures excess return per unit of total volatility under this calculation (excess return scaled by standard deviation). |
| E | False | A higher Sharpe does not guarantee a smaller maximum drawdown — the two measure different properties and need not rank strategies identically. |

**Reference:** Balch ML4T Project 8 (Sharpe ratio definition and annualization, √252 for daily data); Grinold & Kahn, 2nd ed., risk-adjusted return measures.

### [QF2-D6G4Q2] Sharpe vs. Sortino under asymmetric returns
**Scenario:** Two strategies share the same average return and standard deviation. Strategy N has roughly symmetric fluctuations; Strategy P has frequent small losses but occasional large gains (substantial upside volatility). Sharpe and Sortino are compared at the same target.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: the Sharpe ratio penalizes both upside and downside deviations through total standard deviation, which treats deviations on both sides of the mean as variability. |
| B | False (accurate) | Correct: the Sortino ratio focuses its risk denominator on harmful deviations below the target (downside deviation relative to a target/required return). |
| C | False (accurate) | Correct: Strategy P's large positive gains can increase its Sharpe denominator even though they are not downside losses — upside variation contributes to total variance. |
| D | True (incorrect) | Wrong: the two metrics need not rank the strategies identically despite equal average return — differences in downside versus total variability can make rankings disagree. |
| E | False (accurate) | Correct: metric choice should reflect which notion of risk is relevant — a metric is informative only insofar as its reward and risk definitions match the decision. |

**Reference:** Grinold & Kahn, 2nd ed., risk-adjusted performance measures (total vs. downside risk); Balch ML4T Project 8 (Sharpe ratio and risk-measure selection).

### [QF2-D6G4Q3] Information ratio vs. Sharpe ratio
**Scenario:** An active fund has average annual active return 3% and tracking error (σ of active return) 6%. Separately, total portfolio return is 9%, risk-free 3%, total volatility 12%.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: the information ratio = 3% / 6% = 0.50 (active return per unit of tracking error). |
| B | False (accurate) | Correct: the Sharpe ratio = (9% − 3%) / 12% = 0.50. |
| C | False (accurate) | Correct: the information ratio evaluates active return per unit of benchmark-relative risk — its denominator is tracking error, the variability of active returns. |
| D | True (incorrect) | Wrong: equal numerical values (both 0.50) do not make Sharpe and information ratio the same question — one is total, the other benchmark-relative evaluation. |
| E | False (accurate) | Correct: changing the benchmark can change the measured active return and tracking error — both are defined relative to the selected benchmark. |

**Reference:** Grinold & Kahn, 2nd ed., Information Ratio and the Fundamental Law of Active Management (IR = active return / tracking error ≈ IC×√breadth); Balch ML4T Project 8 (Sharpe vs. benchmark-relative metrics).

### [QF2-D6G5Q1] Turnover, trading costs, and gross vs. net Sharpe
**Scenario:** Strategy H rebalances daily (800% annual turnover); Strategy L rebalances a diversified portfolio quarterly (40% turnover). Their reported gross Sharpe ratios are equal, but transaction costs are not yet deducted.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Strategy H generally requires more trading per dollar of portfolio value — its holdings are changed much more extensively over the year. |
| B | False | Equal gross Sharpe ratios do not imply equal net Sharpe ratios — different trading costs can alter net returns and risk-adjusted performance. |
| C | True | Strategy H is likely more sensitive to spreads, commissions, and market impact — more frequent/larger trading exposes more capital to frictions. |
| D | True | Turnover is informative about trading intensity but does not by itself reveal whether trades are profitable (useful updating vs. unproductive churn). |
| E | True | Applying identical zero-cost assumptions can conceal an important implementation difference that is likely much larger for the high-turnover rule. |

**Reference:** Balch ML4T Project 8 and the market-simulator / transaction-cost material (turnover, commissions, impact; gross vs. net performance).

### [QF2-D6G5Q2] No-trade band to suppress churn from a noisy signal
**Scenario:** A noisy signal makes a strategy buy Monday, sell Tuesday, buy Wednesday, sell Thursday though the underlying forecast barely changes. The team considers a no-trade band around the current position.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: the repeated reversals are evidence of short holding periods and possible churn — positions are opened and closed repeatedly over a few days. |
| B | False (accurate) | Correct: a no-trade band can reduce transactions caused by small signal changes — small target changes are ignored until their expected benefit is meaningful. |
| C | True (incorrect) | Wrong: reducing turnover does not necessarily reduce portfolio risk in every market condition — less frequent trading can leave exposures in place longer and does not guarantee lower risk. |
| D | False (accurate) | Correct: frequent reversals can consume gross alpha through repeated transaction costs — each reversal may pay spreads, commissions, slippage, or impact. |
| E | False (accurate) | Correct: a useful evaluation should examine both trading behavior and resulting net performance — turnover diagnoses implementation demands while net results show the economic effect. |

**Reference:** Balch ML4T Project 8 / market-simulator material (no-trade bands, turnover control, cost drag on gross alpha).

### [QF2-D6G5Q3] Active vs. passive after trading costs
**Scenario:** A passive benchmark holds the same stocks all year; an active strategy trades monthly to keep the same average market beta but exploit security-level forecasts. Before costs it outperforms by 1.5%; estimated trading costs are 2.0%.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Matching average market beta does not imply matching turnover — exposure level and trading intensity are distinct characteristics. |
| B | True | A 1.5% gross advantage minus 2.0% cost gives a −0.5% net active return — about 0.5 point below the benchmark, all else equal. |
| C | False | Gross outperformance is not sufficient to establish economic value — the strategy underperforms after the stated implementation costs. |
| D | True | Longer holding periods could reduce turnover but might delay responses to changing forecasts — a responsiveness-versus-cost tradeoff. |
| E | True | Comparing active and passive strategies should include the costs required by their different trading behavior — net implementable performance is the relevant comparison. |

**Reference:** Balch ML4T Project 8 (gross vs. net return; incorporating transaction costs when comparing active and passive strategies).

### [QF2-D6G6Q1] CAPM-style attribution — beta vs. alpha
**Scenario:** A strategy earns 14% with risk-free 2%, market 10%, estimated market beta 1.5. Using expected return from market exposure = r_f + β×(r_m − r_f), ignore estimation error.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: the return associated with the strategy's estimated market exposure is 2% + 1.5 × (10% − 2%) = 14%. |
| B | False (accurate) | Correct: the realized return (14%) equals the simplified beta-implied return in this example. |
| C | True (incorrect) | Wrong: the 4-point advantage over the market does not prove positive alpha — the extra market sensitivity fully explains the difference under the simplified calculation. |
| D | False (accurate) | Correct: high beta can produce a return above the market in a rising market without security-selection skill — leveraged/high-beta exposure magnifies positive market excess return. |
| E | False (accurate) | Correct: attribution helps distinguish exposure-driven return from residual performance — raw return comparisons alone can confuse systematic risk with skill. |

**Reference:** Grinold & Kahn, 2nd ed., factor models and performance attribution (systematic/beta return vs. residual alpha; CAPM decomposition); Balch ML4T Project 8 (beta vs. alpha interpretation).

### [QF2-D6G6Q2] Allocation vs. selection vs. timing attribution
**Scenario:** An equity fund beats its benchmark by 3%: +2.5% from overweighting an outperforming technology sector, +1.0% from stock selection within sectors, −0.5% from poor market-timing. Treat the components as additive.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The components sum to the 3% active return: 2.5% + 1.0% − 0.5% = 3.0%. |
| B | True | Sector allocation made the largest positive contribution — the 2.5% sector effect exceeds the other positive contribution. |
| C | False | Security selection contributed positively (+1.0%), not negatively, under the stated attribution. |
| D | True | Market timing reduced performance — its contribution is −0.5%. |
| E | False | The 3% active return alone does not reveal the same source information — it does not identify whether allocation, selection, or timing generated it. |

**Reference:** Grinold & Kahn, 2nd ed., performance attribution (Brinson-style allocation vs. selection vs. interaction/timing decomposition of active return).

### [QF2-D6G6Q3] Hidden factor exposure in a "market-neutral" book
**Scenario:** A nominally market-neutral strategy has zero net dollar exposure but is long high-beta and short low-beta stocks. It gains strongly in a rally; a factor regression later shows positive market and momentum exposure with little unexplained residual.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True (incorrect) | Wrong: zero net dollar exposure does not guarantee zero market beta — dollar neutrality does not equal beta or factor neutrality. |
| B | False (accurate) | Correct: different betas on the long and short books can create systematic market exposure — long high-beta and short low-beta can leave positive market sensitivity. |
| C | False (accurate) | Correct: momentum exposure may explain part of the performance if momentum did well — returns from a rewarded factor are not necessarily strategy-specific alpha. |
| D | False (accurate) | Correct: little residual return after factor adjustment weakens the unique-alpha claim — most performance is accounted for by measured systematic exposures. |
| E | False (accurate) | Correct: performance attribution can reveal exposures not obvious from net capital invested — position labels or net exposure can conceal meaningful factor loadings. |

**Reference:** Grinold & Kahn, 2nd ed., multi-factor risk/attribution models (factor loadings vs. residual alpha; why dollar neutrality is not factor neutrality).

### [QF2-D6G7Q1] Return concentrated in a few trades
**Scenario:** A strategy earns 18% annually over four years, but nearly all profit comes from two trades during one crisis month; it loses modestly in each of the other three calendar years.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The high average return may be economically dependent on a few extreme observations — a small number of trades account for most of the result. |
| B | True | Removing or perturbing the two crisis trades is a useful sensitivity test — it reveals how fragile the conclusion is to those observations. |
| C | False | Positive full-period performance does not guarantee stable subperiod performance — the strategy lost in most individual years. |
| D | True | The strategy may be valuable if the crisis gains are repeatable, but the concentration requires investigation — it changes the evidence needed to support the claim. |
| E | True | Reporting only the aggregate annualized return conceals consistency information that subperiod and trade-level analysis would reveal. |

**Reference:** Bailey & López de Prado (sensitivity to a few observations; robustness of backtested performance); Balch ML4T Project 8 (interpreting concentrated backtest results).

### [QF2-D6G7Q2] Statistical versus economic significance
**Scenario:** A strategy's mean monthly net return is positive, but a test cannot reject a zero mean at conventional levels. It requires expensive infrastructure and produces only a very small expected dollar profit at the available capital.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: the sample provides limited statistical evidence that the true mean is positive — not strong enough to reject the zero-mean null under the chosen test. |
| B | True (incorrect) | Wrong: failure to reject zero does not prove the true expected return is exactly zero — it may reflect low power, noise, dependence, or a truly small effect. |
| C | False (accurate) | Correct: even a statistically significant return might lack economic significance if profits do not cover implementation and opportunity costs — detectability does not ensure it is worth implementing. |
| D | False (accurate) | Correct: the small expected dollar profit raises an economic-significance concern independent of the test statistic — usable value after real resource and capital requirements. |
| E | True (incorrect) | Wrong: statistical and economic significance do not evaluate identical questions — one concerns evidence against a statistical null, the other practical magnitude and value. |

**Reference:** Bailey & López de Prado (statistical significance of backtested returns, deflated Sharpe); Grinold & Kahn, 2nd ed. (economic vs. statistical significance of active returns); Balch ML4T Project 8.

### [QF2-D6G7Q3] Robustness to regime, costs, and parameters
**Scenario:** A strategy does well in a bull market but poorly in a bear market and a high-volatility period. Its advantage disappears when transaction costs rise from an optimistic 2 bp to a plausible 8 bp, and small lookback changes produce sharply different results.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The results indicate sensitivity to market regime — performance differs materially across bull, bear, and high-volatility conditions. |
| B | True | The cost test suggests the economic conclusion is fragile to implementation assumptions — the advantage vanishes under a plausible alternative cost estimate. |
| C | False | Strong performance in one regime does not guarantee robustness — robustness requires examining dependence on conditions, not merely one aggregate endpoint. |
| D | True | Sharp changes from small lookback adjustments can indicate parameter instability or overfitting — a stable relation should not require an exceptionally precise arbitrary setting. |
| E | True | Robustness analysis should include plausible regimes, costs, and parameter perturbations rather than only the preferred specification. |

**Reference:** Bailey & López de Prado (parameter sensitivity, cost assumptions, and backtest overfitting); Balch ML4T Project 8 (robustness checks across regimes, costs, and parameters).

## References (domain-level)

1. **Grinold & Kahn — *Active Portfolio Management*, 2nd ed.:** benchmark selection and the definition of active (residual) return vs. systematic return; the **Information Ratio** and the **Fundamental Law of Active Management** (IR = active return / tracking error ≈ IC × √breadth); **performance attribution** — Brinson-style allocation vs. selection vs. interaction/timing, and multi-factor attribution separating factor-loading return from residual alpha (G1, G4, G6, G7).
2. **Bailey & López de Prado — backtest overfitting literature** ("The Probability of Backtest Overfitting"; "Pseudo-Mathematics and Financial Charlatanism: The Effects of Backtest Overfitting on Out-of-Sample Performance"; the **Deflated Sharpe Ratio**): in-sample vs. out-of-sample evaluation, selection bias from testing many configurations, dependence in financial series, and statistical vs. economic significance of backtested results (G2, G7).
3. **Balch — ML4T, Project 8 (Strategy Evaluation / "Strategy Learner" and the market simulator):** cumulative return, volatility, and maximum drawdown; the Sharpe ratio and its annualization (√252 for daily data); benchmark and manual-strategy comparison under common dates/capital/cost assumptions; turnover, transaction costs, and gross-vs-net performance; interpreting beta vs. alpha and robustness of backtested results (all groups).

*Note on source fidelity: all A–E verdicts are transcribed verbatim from `slices/QF2_D06.txt`; inverted-polarity items are rendered as "True (incorrect)" / "False (accurate)" without flipping the slice's verdict. The source slice contains PDF ligature artifacts in words such as "signiﬁcant", "proﬁt", "ﬁt/ﬁtted", "ﬂows", "ﬂuctuations", "speciﬁc(ation)", "diversiﬁed", and "magniﬁes" (ﬁ/ﬂ ligatures); these are rendered here with normal "fi"/"fl" spelling.*
