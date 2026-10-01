# QF Domain 2 — Risk and Risk-Adjusted Performance

## Domain cheat-sheet

- **Volatility / variance / standard deviation** measure *dispersion of returns around the mean*, not a fixed loss.
  - **Variance** = average of squared deviations from the mean (units = squared returns). **Standard deviation (σ)** = √variance, back in the same units as returns.
  - Squaring gives **outliers disproportionate weight** — one extreme observation can dominate measured dispersion.
  - **Equal average returns do NOT imply equal risk**: a constant-return series has zero variance; an alternating series with the same mean is more dispersed.
  - A "24% volatility" is a spread estimate, *not* a guaranteed loss of 24% or a frequency of loss. Low volatility does **not** eliminate tail risk, estimation error, or the possibility of loss.
  - Every included observation affects **both** the mean and the dispersion — you cannot drop a point's effect from one and not the other.
- **Downside risk & drawdown** are *path-dependent* — they depend on the order of returns, unlike σ.
  - **Drawdown** = decline from a prior *peak (high-water mark)*, measured `(trough − peak)/peak`. **Maximum drawdown (MDD)** = largest such peak-to-subsequent-trough drop over the path.
  - Drawdown is measured from the running peak, **not** from inception or to the ending value — a fund up on inception can still have had a deep drawdown.
  - **Recovery asymmetry**: a loss of `L` needs a gain of `1/(1−L) − 1` to recover. −25% needs +33.3%; a fall from 125→90 needs +38.9% to regain 125.
  - σ and MDD are **not** the same feature: a strategy can show low volatility for years and then suffer a severe drawdown. Deep interim losses matter because withdrawals, governance/liquidity limits, or behavior can force loss realization even if the strategy later recovers.
- **Sharpe ratio** = (return − risk-free rate) / total volatility = **excess return per unit of total risk**.
  - The **risk-free rate must be subtracted** first (that's what makes it *excess* return). Higher Sharpe = more reward per unit of σ.
  - Raw return alone is insufficient — a higher-return fund can have a *lower* Sharpe if its volatility is disproportionately larger.
  - **Annualization**: under IID daily returns, Sharpe scales by **√T** (e.g., ×√252), NOT ×252. Numerator and denominator must share the same time scale.
  - The √time rule **breaks** under autocorrelation or time-varying volatility; Sharpe also under-describes **non-normal** (skewed, fat-tailed) distributions and identical Sharpes can hide very different loss/drawdown profiles.
- **Sortino ratio** = (return − minimum acceptable return, "MAR") / **downside deviation** (dispersion of returns *below* the target only).
  - Sharpe penalizes upside and downside volatility equally; **Sortino penalizes only shortfalls**, so it aligns with a client who fears losses but welcomes upside surprises.
  - Large *positive* deviations do **not** raise downside deviation. Similar total σ can mask very different downside behavior → Sortino can rank funds differently than Sharpe.
  - The **chosen target/MAR is not optional**: it defines the numerator (excess over target) and which outcomes count as shortfalls; changing it can flip the comparison.
  - With **few/no observed downside months** the denominator is near-zero → the ratio is unstable or undefined; a benign short sample makes tail-selling strategies look artificially safe.
- **Information ratio (IR)** = **active return** / **tracking error** = benchmark-relative reward per unit of active risk.
  - **Active return** = portfolio return − benchmark return. **Tracking error** = volatility (std dev) of the benchmark-relative (active) returns, usually annualized.
  - IR measures skill of *active management* vs. a benchmark; Sharpe measures total risk-adjusted return vs. the *risk-free* rate. Different reference returns, different risk denominators.
  - A larger raw excess return is **not** better if it used proportionally more tracking error (e.g., 2%/2.5% = 0.80 beats 4%/8% = 0.50).
  - A portfolio can have a modest Sharpe yet a strong IR (tracks a risky benchmark closely and adds consistent value) — the two properties are distinct.
- **Risk-return tradeoffs are investor-specific.** Higher expected return normally comes with higher risk; the "right" choice depends on horizon, liquidity needs, drawdown tolerance, governance, and willingness/capacity to bear loss. There is **no universal ranking** — a single summary statistic cannot capture all constraints.
- **Limitations of risk metrics** (why raw metrics mislead):
  - σ treats upside and downside symmetrically → two funds with equal σ can have opposite skew/tail behavior; a downside measure distinguishes them.
  - Metrics are **sample-period sensitive**: choosing a calm window (excluding a crisis) lowers apparent risk and flatters performance. Recency alone doesn't make a window valid.
  - **Non-normal / fat-tailed** returns make extremes more likely than a normal model implies; historical estimates are unstable and can be **gamed** by selective windows or methodology.
  - **Backtest overfitting**: extensive model/hyperparameter selection inflates the chosen backtest; low backtested MDD is an observed statistic, not a guaranteed future bound. Out-of-sample, sensitivity, and stress testing probe robustness a headline metric conceals.

## Common traps

- **No inverted-logic questions in this domain.** All 21 items (QF-D2G1Q1 ... QF-D2G7Q3) use a plain `Answer Key:` (normal polarity: True = accurate, False = inaccurate). There is *no* "True = incorrect; False = accurate" block anywhere in QF_D02, so do not invert — but stay alert, since sibling domains do embed the trap.
- **Double-negative "embedded claim" choices** — the phrasing *"A reviewer would be wrong to accept the claim that [an accurate statement]"*. The embedded claim is true, so being "wrong to accept" it is **False**. Parse the inner claim, judge it, then negate. Appears in **G2Q3C** and **G6Q1D** (both marked **False**, "the underlying claim is correct and should be accepted").
- **"Reverses the correct conclusion" negation choices** — statements written in the negative that flip a *true* fact into a false claim (e.g., "is not a 28% drawdown," "the annualized Sharpe is not ~0.79," "tracking error is not 6%," "Manager B's IR is not 0.50," "Sharpe is not ~0.53"). These read plausibly but the Key marks them **False**. Compute the number, then check whether the "not" makes the sentence lie. Seen in G2Q1A/B, G3Q2B, G4Q1A, G5Q1B, G5Q2B, G6Q2A.
- **Equal means / equal ending wealth / equal σ ≠ equal risk.** Recurring bait: identical averages (G1Q1C), identical terminal wealth (G2Q3A), or identical σ (G7Q1B) are offered as proof of identical risk. Always **False** — dispersion, path, skew, and tails can differ.
- **Volatility ≠ a guaranteed loss.** "24% volatility means it loses 24% one year in two" (G1Q2C) and "lower volatility guarantees no large loss" (G1Q2D) are both **False** — σ is a dispersion estimate, not a loss magnitude or frequency.
- **Annualization scale trap.** Sharpe scales by **√T**, not T (G3Q2C False, G3Q2B/E False). Numerator and denominator must be on the same time base.
- **A high Sharpe/Sortino does not prove tail safety** (G3Q3A, G4Q3A False) — especially for short samples of tail-selling ("disaster insurance") strategies where the denominator is tiny and the loss simply hasn't shown up yet.

## Questions

### [QF-D2G1Q1] Same average return, different dispersion
**Scenario:** Two market-neutral strategies each average 1% monthly: Strategy A returned exactly 1% every month, Strategy B alternated +5% / −3%. The CRO asks whether identical averages imply identical risk.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Every A observation equals its mean, so each deviation is 0 → variance = mean of squared deviations = 0. A perfectly constant series has zero historical variance. |
| B | True | B's returns swing far from the 1% mean (+4 and −4 deviations) while A's do not, so B has strictly greater historical dispersion. |
| C | False | Equal *arithmetic means* say nothing about spread; two series with the same mean can have any variance. Equal average ≠ equal σ. |
| D | True | Variance is in squared-return units; σ = √variance restores the original return units — the reason σ is the more interpretable risk figure. |
| E | False | A's constant path is the *smoother* one; B's alternating ±returns form the rougher, more volatile path. The statement is backwards. |

**Reference:** Variance/standard deviation as dispersion — Investopedia "Standard Deviation" & "Volatility"; CFA curriculum (measures of dispersion).

### [QF-D2G1Q2] Interpreting volatility estimates for two funds
**Scenario:** Fund X = 12% return / 10% vol; Fund Y = 14% return / 24% vol. A growth-seeking but uncertainty-averse client asks how to read the volatility figures.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | 14% > 12%: Fund Y does have the higher expected *raw* return (before adjusting for risk). |
| B | True | A 24% σ vs. 10% σ means Y's outcomes are estimated to spread far more widely around its mean — greater dispersion. |
| C | False | σ is a dispersion measure, not a fixed loss size or a "one-in-two-years" frequency. Volatility does not promise a specific loss. |
| D | False | Lower σ reduces expected dispersion but does not eliminate tail events, estimation error, or the possibility of a large loss. |
| E | False | Choosing Y "solely for its 14% return" *would* ignore materially higher risk (24% vs. 10% σ). The statement's double negative reverses the correct conclusion. |

**Reference:** Volatility interpretation, risk-return tradeoff — Investopedia "Volatility"; CFA (return-risk tradeoff).

### [QF-D2G1Q3] Extreme observation and selective exclusion
**Scenario:** 23 months clustered near 0.5%, then a −18% 24th month. The PM wants to drop the last month as "unrepresentative" before showing risk stats to the committee.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | A return far from the rest creates a large squared deviation and generally *raises* measured variance. Saying it "will not increase" variance reverses the truth. |
| B | True | Variance squares deviations, so a large deviation is weighted disproportionately — one outlier can dominate the statistic. |
| C | True | Removing a point only because it worsens reported risk understates the risk investors actually bore → a misleading comparison. |
| D | False | Every included observation affects the *mean* as well as dispersion. The −18% shifts the average return too. |
| E | True | A data error and a genuine tail exposure require different treatment, so a risk review should establish the cause before deciding how to handle the point. |

**Reference:** Effect of outliers on variance; data-integrity vs. genuine tail — Investopedia "Variance," "Outlier"; CFA (sample statistics).

### [QF-D2G2Q1] Drawdown from the high-water mark
**Scenario:** NAV path $100 → $125 → $90 → $110. The manager touts the $10 gain from inception; an investor asks the risk team to describe the loss from the high-water mark.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | ($90 − $125)/$125 = **−28%**, so the decline *is* a 28% drawdown. The negation makes the statement false. |
| B | False | The max drawdown *is* measured from the $125 peak to the $90 trough (largest peak-to-subsequent-trough decline). The "not" reverses it. |
| C | False | Drawdown is measured from a prior peak, not from inception-to-ending. Ending above $100 does not mean "no drawdown." |
| D | True | To climb from $90 back to $125 needs $125/$90 − 1 ≈ **38.9%** — the recovery-asymmetry math. |
| E | True | At $110, ($110 − $125)/$125 = **−12%**, so the fund is still 12% below its prior peak. |

**Reference:** Drawdown / maximum drawdown definition, recovery asymmetry — Investopedia "Maximum Drawdown," "Drawdown."

### [QF-D2G2Q2] Low volatility can still hide a severe drawdown
**Scenario:** Strategy A fluctuates often but never falls >6% from a peak; Strategy B looks stable for years then loses 30% before recovering. The committee has a 15% drawdown tolerance and asks if ordinary volatility captures its concern.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | A 30% drawdown exceeds the stated 15% tolerance, so B violates it during the loss. |
| B | True | A rare large loss can follow a long calm stretch — low volatility for most of a sample does not preclude a deep drawdown. |
| C | False | σ measures dispersion around the mean; drawdown measures a path-dependent peak-to-trough loss. They are *not* the same feature. |
| D | False | The scenario fixes A's MDD at 6% and B's at 30%; frequent small fluctuations do not make A's max drawdown larger. |
| E | True | A deep enough loss can trigger governance, liquidity, or behavioral constraints even if the strategy later recovers — path and depth matter operationally. |

**Reference:** Volatility vs. drawdown distinction — Investopedia "Maximum Drawdown"; CFA (path-dependent risk / downside risk).

### [QF-D2G2Q3] Equal ending wealth, different interim path
**Scenario:** Two strategies share annualized σ and ending wealth. Strategy X had a 25% midyear drawdown then recovered; Strategy Y stayed within 8% of its peak. The family office may need to withdraw capital during the year.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Identical endpoints can conceal very different interim losses and liquidity consequences — equal ending wealth does not prove equal path-dependent risk. |
| B | True | X's 25% max drawdown exceeds Y's 8% bound, so X had the larger MDD. |
| C | False | *Embedded-claim double negative.* The inner claim (interim withdrawals make loss timing/depth relevant) is correct and should be accepted; a withdrawal during a deep drawdown forces loss realization and leaves less capital to recover — so "a reviewer would be wrong to accept" it is false. |
| D | False | Recovery asymmetry: a 25% loss needs 1/0.75 − 1 ≈ **33.3%** gain to recover, not 25%. |
| E | True | σ and drawdown describe different aspects of risk; reporting both reveals differences hidden by ending wealth or volatility alone. |

**Reference:** Path dependence, recovery asymmetry, complementary risk measures — Investopedia "Maximum Drawdown," "Drawdown"; CFA (liquidity risk).

### [QF-D2G3Q1] Sharpe vs. raw return
**Scenario:** Fund A = 12% / 20% vol; Fund B = 9% / 8% vol; risk-free = 2%. The client initially prefers A for its higher raw return.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Excess return = return − rf. A: 12 − 2 = 10%; B: 9 − 2 = 7%. A has the higher excess return. |
| B | True | Sharpe = excess/σ. A: 10/20 = **0.50**; B: 7/8 = **0.875**. B has the higher Sharpe despite lower raw return. |
| C | False | Raw return ignores risk. A earned more but per unit of volatility B is more efficient, so "must be better" is false. |
| D | False | The risk-free rate *must* be subtracted — Sharpe uses *excess* return. Saying it should not be reverses the definition. |
| E | True | A higher Sharpe means more excess return per unit of total volatility — the core interpretation. |

**Reference:** Sharpe ratio definition — Investopedia "Sharpe Ratio"; CFA (risk-adjusted performance).

### [QF-D2G3Q2] Annualizing the Sharpe ratio (√time)
**Scenario:** Daily excess return 0.04%, daily σ 0.80%. Head of trading wants an annualized Sharpe over 252 IID trading days.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Daily Sharpe = 0.04%/0.80% = **0.05**. |
| B | False | Annualized = 0.05 × √252 ≈ **0.79**, so it *is* ~0.79; the "not" makes the statement false. |
| C | False | Under IID returns the ratio scales by **√252**, not ×252 — mean scales with T while σ scales with √T, so the ratio scales with √T. |
| D | True | The √time adjustment assumes IID returns; autocorrelation or time-varying volatility breaks it. |
| E | False | If the mean is annualized, σ must also be put on the annual scale — numerator and denominator must use compatible time units. Saying it "must not" reverses the rule. |

**Reference:** Sharpe annualization / √time rule — Investopedia "Sharpe Ratio" (annualizing); CFA (return/volatility scaling).

### [QF-D2G3Q3] Sharpe under skewed, fat-tailed returns
**Scenario:** A short-volatility strategy reports a high historical Sharpe from small steady gains before one rare severe loss; the CRO warns the distribution is skewed and fat-tailed.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | A high historical Sharpe summarizes past excess-return-to-σ; it does not prove low tail risk, especially in a benign window. |
| B | True | σ (the Sharpe denominator) does not capture skewness, fat tails, or discontinuous losses — it incompletely describes non-normal risk. |
| C | True | If the estimation window contains few/no tail events, rare losses are underrepresented and the strategy looks unusually stable. |
| D | False | The same Sharpe can arise from very different return paths and loss distributions, so equal Sharpe ≠ equal drawdown profile. |
| E | True | Drawdown, downside metrics, stress tests, and tail analysis expose risks Sharpe misses — the committee should supplement it. |

**Reference:** Sharpe limitations under non-normality — Investopedia "Sharpe Ratio" (limitations); CFA (skewness/kurtosis, tail risk).

### [QF-D2G4Q1] Sortino aligns with downside concern
**Scenario:** Two funds share the same average return above a 3% MAR. Fund A's variability is mostly upside surprises; Fund B often falls below 3%. The client cares about shortfalls, not positive surprises.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Sortino relates return above a target to *downside* deviation, so it *is* more aligned than Sharpe with a downside concern. The "not" reverses this. |
| B | True | Sharpe uses total σ, which counts upside and downside deviations alike — it does not distinguish favorable from unfavorable moves. |
| C | False | Downside deviation counts only observations *below* the target; large positive returns do not increase it. |
| D | True | With similar total σ, A (upside-driven variability) can have a better Sortino than B (frequent shortfalls) — downside behavior differs. |
| E | True | The chosen target drives both shortfall identification and the ratio's value, so it must be specified to interpret Sortino. Saying it can be ignored is false. |

**Reference:** Sortino ratio / downside deviation vs. Sharpe — Investopedia "Sortino Ratio," "Downside Deviation."

### [QF-D2G4Q2] Computing and comparing Sortino ratios
**Scenario:** Strategy X = 8% return / 4% downside deviation; Strategy Y = 10% / 8% downside deviation; MAR = 2%. Which delivered more return above target per unit of downside risk?
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Sortino = (return − MAR)/downside deviation = (8 − 2)/4 = **1.5**. |
| B | True | Y: (10 − 2)/8 = **1.0**. |
| C | False | Y's higher raw return is more than offset by its larger downside deviation, so higher raw return does not make its Sortino higher. |
| D | True | X's Sortino 1.5 > Y's 1.0, so X has better downside-adjusted performance under these inputs. |
| E | False | Changing the MAR *would* change both numerators and which outcomes count as shortfalls, so it can affect the comparison. Saying it "could not" reverses the truth. |

**Reference:** Sortino calculation and MAR sensitivity — Investopedia "Sortino Ratio," "Downside Deviation."

### [QF-D2G4Q3] Sortino unreliable on a short benign sample
**Scenario:** A fund shows a very high Sortino from only 18 months with no month below its 0% target; the strategy sells disaster insurance and can incur rare losses. Due diligence questions reliability.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | No observed negative months does not prove no downside risk — an unobserved tail event can still be plausible and central to the strategy. |
| B | True | With little/no downside deviation the denominator is near zero → the ratio is extremely large or undefined (division by ~0). |
| C | False | A short sample *can* fail to capture rare events; rare-loss strategies look exceptionally safe in benign windows. The "cannot fail" phrasing reverses this. |
| D | False | Downside focus helps with one Sharpe limitation but does not eliminate sampling, tail, or estimation problems. |
| E | True | Stress testing and a longer, relevant history help assess downside exposure absent from the observed record. |

**Reference:** Sortino instability with near-zero denominator, short-sample tail risk — Investopedia "Sortino Ratio" (limitations); CFA (sampling/estimation risk).

### [QF-D2G5Q1] Information ratio basics
**Scenario:** Active manager returned 11% vs. an 8% benchmark, with 6% annualized tracking error. The board asks whether active risk was used efficiently rather than riding a rising market.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Active return = portfolio − benchmark = 11 − 8 = **3%**. |
| B | False | Tracking error is the volatility of benchmark-relative returns, given as 6% annualized — so it *is* 6%. The "not" reverses it. |
| C | True | IR = active return / tracking error = 3/6 = **0.50**. |
| D | False | A benchmark and a risk-free asset serve different roles; benchmark return drives active-return analysis, not the Sharpe risk-free rate. |
| E | True | A positive IR means realized return exceeded the benchmark per unit of tracking error (positive numerator over active-risk denominator). |

**Reference:** Information ratio & tracking error — Grinold & Kahn "Active Portfolio Management" (Information Ratio); Investopedia "Information Ratio," "Tracking Error."

### [QF-D2G5Q2] IR ranking vs. raw excess return
**Scenario:** Manager A beat the benchmark by 2% with 2.5% tracking error; Manager B by 4% with 8% tracking error. The foundation wants consistent benchmark-relative performance but favors B for its larger excess.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | IR = 2%/2.5% = **0.80** for Manager A. |
| B | False | B's IR = 4%/8% = **0.50**, so "not 0.50" is false. |
| C | False | B earned more active return but used proportionally far more active risk, so it did not use risk more efficiently. |
| D | True | A's IR 0.80 > B's 0.50, so A ranks higher by information ratio. |
| E | False | IR alone does not settle the choice — mandate constraints, estimate reliability, fees, capacity, and risk tolerance also matter. |

**Reference:** IR comparison and selection caveats — Grinold & Kahn "Active Portfolio Management"; Investopedia "Information Ratio."

### [QF-D2G5Q3] Information ratio vs. Sharpe ratio
**Scenario:** A portfolio earned 10% / 12% total σ vs. a 9% benchmark, tracking error 2%, risk-free 3%. The CIO asks analysts to separate an IR evaluation from a Sharpe evaluation.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Active return = 10 − 9 = 1%; IR = 1/2 = **0.50**. |
| B | True | Sharpe = (10 − 3)/12 = 7/12 ≈ **0.58**. |
| C | False | IR uses **tracking error** (volatility of active returns), not total portfolio volatility. |
| D | True | Sharpe measures return above the risk-free rate; IR measures return above a benchmark — different reference returns and risk denominators. |
| E | False | A portfolio *can* have a modest Sharpe yet a strong IR if it tracks a risky benchmark closely and adds consistent value — the properties are distinct, so "cannot" reverses the truth. |

**Reference:** IR vs. Sharpe (reference return & denominator) — Grinold & Kahn "Active Portfolio Management"; Investopedia "Information Ratio," "Sharpe Ratio."

### [QF-D2G6Q1] Higher return does not auto-win
**Scenario:** Strategy A = 9% / 7% vol; Strategy B = 13% / 18% vol. The endowment needs ≥8% expected return but strongly values spending stability; the committee asks if B's higher return automatically makes it preferable.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | 9% and 13% both exceed the 8% requirement. |
| B | True | Differences are 13 − 9 = 4 percentage points of return and 18 − 7 = 11 percentage points of volatility. |
| C | False | Rational investors weigh risk, constraints, funding needs, and preferences — not just the highest expected return, so B is not "necessarily preferable." |
| D | False | *Embedded-claim double negative.* The inner claim (spending-stability concern makes the volatility difference relevant) is correct and should be accepted; a more volatile path may disrupt planned spending — so "would be wrong to accept" it is false. |
| E | False | A risk-adjusted comparison *can* inform the decision (it just doesn't dictate a universal choice). Saying it "cannot inform" reverses the correct conclusion. |

**Reference:** Risk-return tradeoff, investor objectives/constraints — CFA (portfolio objectives & constraints); Investopedia "Risk-Return Tradeoff."

### [QF-D2G6Q2] Leverage: raw return vs. Sharpe
**Scenario:** Leveraged strategy earned 18% / 30% vol; unlevered earned 10% / 10% vol; risk-free 2%. A PM argues the leveraged one is superior because it earned nearly twice the raw return.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | Leveraged Sharpe = (18 − 2)/30 ≈ **0.53**, so "not ~0.53" is false. |
| B | True | Unlevered Sharpe = (10 − 2)/10 = **0.80**. |
| C | False | The leveraged strategy has the higher raw return but the *lower* Sharpe (0.53 < 0.80), so "both higher" is false. |
| D | True | On a Sharpe basis, the unlevered strategy (0.80 > 0.53) used total risk more efficiently over the period. |
| E | True | Return and σ alone omit leverage constraints, tail losses, and implementation costs — the comparison does not address these. |

**Reference:** Leverage and risk-adjusted return — Investopedia "Sharpe Ratio," "Leverage"; CFA (leverage effects on risk).

### [QF-D2G6Q3] Suitability is investor-specific
**Scenario:** A retiree dependent on near-term withdrawals (cannot tolerate a 20% drawdown) and a well-capitalized prop firm (35% drawdown limit, long-dated capital) consider the same volatile strategy. An adviser asks if one universal ranking should govern both.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | The same strategy *can* be acceptable to one investor and unsuitable for another — suitability depends on objectives, horizon, liquidity, and loss-bearing capacity. The claim reverses this. |
| B | True | The retiree's withdrawal needs make loss timing and drawdown particularly relevant (losses near withdrawals impair spending and recovery capital). |
| C | False | A positive expected return does not prevent an unacceptable interim loss, so the retiree's drawdown limit stays relevant. |
| D | False | Liquidity needs, horizon, and behavioral tolerance require information beyond one summary statistic. |
| E | True | Strategy selection should tie measured risk and expected return to each decision maker's capacity and willingness to bear loss — evaluation is investor-specific. |

**Reference:** Investor-specific suitability, drawdown tolerance — CFA (IPS, risk tolerance/ability); Investopedia "Risk Tolerance," "Maximum Drawdown."

### [QF-D2G7Q1] Standard deviation treats upside and downside alike
**Scenario:** A venture fund and a loss-prone trading strategy report the same annual σ, but the venture fund's deviations were mostly large gains while the trading strategy's were mostly losses. An LP asks if σ alone makes their risk equally attractive.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | σ squares deviations regardless of sign, so equal-sized moves above and below the mean count symmetrically. |
| B | False | Equal σ does not imply identical skewness or tail behavior — distributions can share a σ yet differ greatly in shape. |
| C | True | A downside-focused measure (downside deviation, loss-based analysis) can distinguish the loss-heavy strategy from the gain-heavy one that σ obscures. |
| D | True | Large positive surprises raise measured σ even though investors welcome them — σ counts favorable dispersion as "risk." |
| E | False | σ is imperfect but still informative about dispersion; "no useful information" overstates the limitation. |

**Reference:** σ symmetry limitation, downside measures — Investopedia "Standard Deviation," "Downside Deviation"; CFA (skewness/kurtosis).

### [QF-D2G7Q2] Sample-period selection and metric gaming
**Scenario:** A manager markets a Sharpe computed only over the most recent three calm years, omitting an earlier crisis. A due-diligence analyst worries the window and presentation choices make the comparison unreliable.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Estimated means, volatility, and ratios depend on the observations included, so a risk-adjusted metric can change materially with the sample period. |
| B | False | Excluding a relevant stress period *can* make risk look lower and performance more favorable — the "cannot" reverses the truth. |
| C | False | Relevance depends on the strategy and regime; recency alone does not make the three-year window uniquely valid. |
| D | True | Applying the same disclosed methodology over an economically comparable period across strategies improves comparability and reduces presentation bias. |
| E | False | Arithmetic precision does not cure biased sample selection or bad assumptions — a precisely computed ratio can still mislead. |

**Reference:** Sample-period sensitivity, metric gaming — Investopedia "Sharpe Ratio" (limitations), "Backtesting bias"; CFA (survivorship/selection bias).

### [QF-D2G7Q3] Backtest overfitting and fat tails
**Scenario:** An ML strategy shows an excellent backtested Sharpe and low max drawdown after extensive hyperparameter tuning. The risk committee notes the estimates come from one sample, returns are fat-tailed, and many variants were tried.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Choosing the best of many trials capitalizes on noise → selection bias inflates the chosen backtest's reported performance. |
| B | False | Historical estimates are *not* guaranteed to persist live — regime change, implementation, estimation error, and overfitting can alter results. |
| C | True | Fat tails assign more probability to extreme outcomes than a normal model implies, making extremes more plausible. |
| D | False | Backtested max drawdown is an observed sample statistic, not a guaranteed future upper bound. |
| E | True | Out-of-sample testing, sensitivity analysis, and stress testing provide evidence beyond headline historical metrics and probe robustness. |

**Reference:** Backtest overfitting, fat tails, MDD as sample statistic — Investopedia "Backtesting," "Fat Tail," "Maximum Drawdown"; CFA (data-mining/overfitting bias).

## References (domain-level)

1. **Grinold & Kahn — *Active Portfolio Management*:** definition and use of the Information Ratio (active return / tracking error), active risk, and the distinction between active management skill and total risk-adjusted return — for the G5 (information ratio) questions.
2. **CFA Institute curriculum — Quantitative Methods & Portfolio Management:** measures of dispersion (variance, standard deviation, downside deviation), skewness/kurtosis and non-normality, risk-adjusted performance (Sharpe, Sortino, Information Ratio), and investor objectives/constraints (IPS, risk tolerance vs. ability) — foundational across all seven topic groups.
3. **Investopedia — Sharpe Ratio:** definition, excess-return-over-risk-free construction, √time annualization, and limitations under non-normal returns — G3 and G6.
4. **Investopedia — Sortino Ratio & Downside Deviation:** downside-only risk measurement, minimum acceptable return (MAR), and instability with near-zero downside samples — G4.
5. **Investopedia — Standard Deviation / Volatility / Variance:** dispersion measurement, symmetric treatment of upside and downside, and sensitivity to outliers — G1 and G7.
6. **Investopedia — Maximum Drawdown / Drawdown:** peak-to-trough (high-water-mark) loss, path dependence, recovery asymmetry, and drawdown vs. volatility — G2 and G6. (Also "Backtesting," "Fat Tail," "Value at Risk" for the metric-limitation items in G7.)
