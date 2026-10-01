# QF Domain 4 — Portfolio Optimization

## Domain cheat-sheet

- **Portfolio weights & budget constraint.** Weights `w_i` are the fraction of capital in each asset. **Fully invested** ⇒ `Σ w_i = 1` (100%). Meeting the sum-of-weights (budget) constraint alone does NOT rule out negative or >100% weights — you need *separate* sign/bound constraints for that.
  - **Long-only**: every `w_i ≥ 0` (no shorts). A negative weight is a **short position**; a weight > 1 is a **levered long**.
  - **Net exposure** = `Σ w_i` (signed). **Gross exposure** = `Σ |w_i|`. Net can be 100% while gross far exceeds 100% (e.g., 120/30/−50 → net 100%, gross 200%) — offsetting longs/shorts create **leverage** even at 100% net.
  - **Position bounds** (min/max per asset, e.g. 5%–35%) shrink the feasible set and can change the optimum *even when expected returns and the covariance matrix are unchanged*. Five 5% minimums pre-commit 25% of capital; three 35% maxes already sum to 105% (infeasible under a 100% budget).
- **Minimum-variance & the Global Minimum-Variance (GMV) portfolio.**
  - Portfolio variance: `σ_p2 = Σ_i Σ_j w_i w_j σ_ij` = `wTΣw`. For two assets: `σ_p2 = w12σ12 + w22σ22 + 2w1w2·ρ12σ1σ2`. Covariance `σ_ij = ρ_ij σ_i σ_j`.
  - **GMV** = feasible portfolio with the *lowest* variance overall — a risk objective, not a return objective. It generally is NOT the single lowest-volatility asset: **diversification** (imperfect/negative correlation) can push a combination below the volatility of any component alone.
  - Identifying GMV requires the **covariance matrix**, not merely a ranking of stand-alone volatilities. Moving off GMV trades higher risk for higher expected return.
- **Maximum-Sharpe & the tangency portfolio.**
  - **Sharpe ratio** = `(E[R_p] − R_f) / σ_p` = excess return per unit of volatility. Maximizing Sharpe considers *both* excess return and risk — the highest-return portfolio is NOT automatically max-Sharpe.
  - The **tangency portfolio** is the risky-asset portfolio with the maximum Sharpe ratio; graphically the **Capital Allocation Line (CAL)** drawn from `R_f` is tangent to the efficient frontier there (steepest slope = highest Sharpe). With lending/borrowing at `R_f`, investors hold a mix of the tangency portfolio + risk-free asset — the mix (not a different risky portfolio) sets their risk level.
  - Changing `R_f` changes the excess-return numerator by the same amount for all portfolios but divides by *different* `σ`, so the Sharpe *ranking* can flip when candidates have different volatilities. Raising `R_f` (risky returns fixed) *lowers* every excess return. Tangency ≠ GMV in general.
- **Efficient frontier.** Set of portfolios offering the **minimum risk for each target return** (equivalently max return per risk). A portfolio is **dominated** if another offers ≥ return at ≤ risk (with one strict). The frontier is the *upper* branch above the GMV point; anything below the GMV return is dominated by GMV. Interior/dominated portfolios are **inefficient**. An **efficient** portfolio cannot raise return without raising risk, nor cut risk without cutting return.
- **Estimation error / error-maximization.** MV optimization is highly sensitive to its inputs, *especially expected returns*. Small changes in expected-return estimates can produce large swings in weights ("**error maximization**" — the optimizer over-weights assets with over-estimated returns). Extreme/concentrated allocations often reflect **noise, not genuine edge**. Similar covariance matrices do NOT guarantee similar solutions if expected-return vectors differ. Numerical precision ≠ input accuracy. **Garbage in, garbage out**: exact math can't rescue bad inputs. Remedies: **shrinkage** (e.g., Ledoit-Wolf), longer/alternative samples, stress scenarios, position bounds, regularization.
- **Constraints & practical design.** Long-only, leverage/gross-exposure caps, sector/asset-class limits, and **turnover** limits change the feasible set. A constraint is **binding** when the optimum sits on its boundary. Constraints can only *reduce* the in-sample (modeled) objective value (the unconstrained feasible set contains all constrained portfolios) — but they improve real-world robustness, implementability, and control of concentrated estimation error. **One-way turnover** here = `1⁄2 · Σ|Δw_i|`; a binding turnover cap spreads movement toward the target across several rebalances.
- **In-sample vs. out-of-sample.** Using the same data to choose weights *and* to report performance is **in-sample** and flatters the strategy by fitting noise that won't repeat. Real **out-of-sample (OOS)** tests apply fixed weights to later, previously unused data. **Ex post** ("after the fact") optimal weights use information not available at decision time → **look-ahead bias**; correct math doesn't cure improper timing. Large weight swings across adjacent estimation windows signal instability; the *ex post* optimal portfolio need not stay optimal next period.

## Common traps

- **No inverted-logic questions in this slice.** All 21 items use **Normal polarity** (`Answer Key:` with plain True/False; "True" = accurate). There is no "True = incorrect; False = accurate" block here — but confirm the polarity line on every question anyway, since sibling domains do invert.
- **Double-negative "embedded claim" choices are the primary trap.** Many *false* choices are phrased as a negation of a true fact, and the key stamps them **False** with "*reverses the correct conclusion.*" Parse the inner fact, judge its truth, then apply the negation. Offenders: **G1Q2D** ("gross exposure is *not* 200%" — it is), **G1Q3A** ("would *not* violate" — it does), **G2Q2C** ("variance is *not* 0.0100" — it is), **G2Q3C** ("removing a constraint *cannot* enlarge the feasible set" — it can), **G3Q1B** ("Sharpe is *not* 0.50" — it is), **G3Q2D** ("*cannot* combine tangency with risk-free" — you can), **G3Q3A** ("Sharpe is *not* 0.80" — it is), **G4Q1A/B** ("*not* dominated" — both are dominated), **G4Q3B/C**, **G5Q1D**, **G5Q2D**, **G5Q3E**, **G6Q1A/C**, **G6Q2B**, **G6Q3D/E**, **G7Q1A**, **G7Q2C**, **G7Q3B**.
- **Worst offender — G7Q2A: a stacked double negative.** "Ex post weights use information that *was not unavailable* at the start of that year." "not unavailable" = "available" → the statement claims the info was available; the key marks it **False** because full-year returns were in fact *not* knowable at year start. Read these letter-by-letter.
- **Net vs. gross exposure.** A portfolio summing to 100% net (satisfying a budget/net-exposure rule) can still be heavily levered — gross = Σ of absolute weights. "Weights sum to 100% ⇒ no leverage" is always wrong when shorts exist.
- **Objective confusion.** GMV minimizes *variance* (not return); max-Sharpe maximizes *excess-return-per-risk* (not raw return); efficient ≠ "numerically in the middle." Watch choices that swap one objective's property onto another.
- **Constraints can't raise the modeled optimum.** Any choice claiming a constraint *must improve* the modeled Sharpe/objective is false — restricting the feasible set can only hold or lower the in-sample optimum; its payoff is robustness/implementability, not a higher backtest number.

## Questions

### [QF-D4G1Q1] Fully-invested, long-only endowment weights
**Scenario:** A university endowment holds 40% equities, 35% bonds, 15% real estate, 10% cash; policy requires full investment and prohibits borrowing and short selling. The committee tests which statements about the weights hold.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | 0.40 + 0.35 + 0.15 + 0.10 = 1.00, so `Σw_i = 1` — the fully-invested (budget) constraint is satisfied. |
| B | True | A long-only rule is exactly the constraint `w_i ≥ 0` for every asset; no negative (short) positions are allowed. |
| C | False | A −10% bond weight is a **short position**; shorting is prohibited, so it violates the policy no matter how the other weights are rebalanced to keep the sum at 100%. |
| D | True | Whether a 10% residual "is cash" depends on how the model defines its investable universe and budget constraint — if cash is already an explicit asset, an unallocated residual is a different thing. Definitional, so the statement can hold. |
| E | False | The sum-of-weights (budget) constraint alone does not forbid negative weights: weights can sum to 1 while some are negative and others exceed 1. Only explicit sign/bound constraints prevent that. |

**Reference:** Portfolio weights & budget constraint; long-only constraints — Markowitz mean-variance framework; Investopedia "Portfolio Weight," "Long/Short constraints."

### [QF-D4G1Q2] Net vs. gross exposure and leverage
**Scenario:** A hedge fund proposes 120% Stock A, 30% Stock B, −50% Stock C. The mandate permits shorting and requires 100% net exposure; the risk committee reviews the leverage.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Net exposure = signed sum = 1.20 + 0.30 − 0.50 = 1.00, meeting the 100% net-exposure requirement. |
| B | True | A −50% weight is a **short position** in Stock C (negative weight = short exposure). |
| C | False | 100% *net* exposure does not imply no leverage — offsetting long (+120/+30) and short (−50) positions create leverage; gross exposure exceeds 100%. |
| D | False | **Double negative.** Gross exposure = `Σ|w_i|` = |1.20| + |0.30| + |−0.50| = 2.00 = 200%. The claim "gross is *not* 200%" reverses the correct conclusion. |
| E | False | **Double negative.** A long-only constraint *would* make this allocation infeasible because the −50% weight violates `w ≥ 0`. "Would not make it infeasible" reverses the truth. |

**Reference:** Net vs. gross exposure, leverage from long/short — Investopedia "Gross Exposure," "Net Exposure"; Grinold & Kahn on long-short construction.

### [QF-D4G1Q3] Position bounds and feasibility
**Scenario:** A retirement plan optimizes among five funds with a 5% minimum and 35% maximum weight each, fully invested. The committee checks whether several proposed allocations are feasible.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | **Double negative.** Three funds at 35% already sum to 105% > 100%, leaving no feasible positive allocation for the other two required holdings — so it *does* violate the fully-invested budget. "Would not violate" reverses the conclusion. |
| B | True | A weight at exactly its bound (5%) satisfies a `w ≥ 5%` constraint; bounds are met at their endpoints unless stated as strict inequalities. |
| C | False | A 40% weight exceeds the 35% maximum for that fund; the per-asset upper bound is violated regardless of how the other four weights are set. |
| D | True | Five mandatory 5% minimums consume 5 × 5% = 25% of capital up front, leaving 75% for the optimizer to distribute. |
| E | True | Bounds reshape the **feasible set**, so they can change which portfolio is optimal even when expected returns and the covariance matrix are unchanged. |

**Reference:** Position (box) constraints and feasible set — Markowitz optimization with bounds; Investopedia "Portfolio Constraints."

### [QF-D4G2Q1] Global minimum-variance portfolio definition
**Scenario:** A risk-averse foundation asks for the global minimum-variance portfolio; a trustee assumes it must be 100% in the single lowest-volatility asset.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The GMV portfolio is by definition the feasible portfolio minimizing `σ_p2 = wTΣw` over the entire feasible set. |
| B | False | **Double negative.** It *can* combine assets: with imperfect (or negative) co-movement, diversification drives portfolio volatility below that of the least-volatile component alone. "Cannot combine" reverses the correct conclusion. |
| C | True | GMV depends on the full covariance structure (`σ_ij = ρ_ij σ_i σ_j`), so you need covariance information, not just a ranking of stand-alone volatilities. |
| D | False | GMV minimizes variance; the highest-expected-return portfolio is a different objective (top of the frontier), not GMV. |
| E | False | **Double negative.** Minimizing risk does not require maximizing return, so GMV's expected return *can* be lower than other feasible portfolios'. "Cannot be lower" reverses the truth. |

**Reference:** GMV portfolio, role of covariance/diversification — Markowitz (1952); Investopedia "Minimum Variance Portfolio," "Efficient Frontier."

### [QF-D4G2Q2] Two-asset variance with negative correlation
**Scenario:** Two assets each have 20% annual volatility and −0.50 correlation. The manager compares 100% in either asset with a 50/50 allocation.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Single-asset variance = `σ2 = 0.202 = 0.0400`. |
| B | True | Covariance = `ρσ1σ2 = −0.50 × 0.20 × 0.20 = −0.0200`. |
| C | False | **Double negative.** 50/50 variance = `0.25(0.0400) + 0.25(0.0400) + 2(0.5)(0.5)(−0.0200) = 0.0100`. "Is not 0.0100" reverses the correct calculation. |
| D | True | Volatility = `√0.0100 = 0.10 = 10%` — diversification cut it from 20% (single asset) to 10%. |
| E | False | At `ρ = +1`, equal-volatility assets give no risk reduction: `σ_p = 20%`, not 10%. Correlation drives the diversification benefit. |

**Reference:** Two-asset portfolio variance, correlation & diversification — Markowitz mean-variance; CFA curriculum "Portfolio Risk and Return."

### [QF-D4G2Q3] Removing a return constraint reaches GMV
**Scenario:** A manager minimizes variance subject to an 8% required return. After dropping that requirement, the optimizer picks a portfolio with 6% return and lower volatility.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | With the 8% target imposed, the solution is the minimum-variance portfolio *conditional on* that return constraint (a point on the frontier at 8%). |
| B | True | With no target-return floor, the variance objective can select the overall lowest-risk feasible portfolio — plausibly the GMV (here 6%). |
| C | False | **Double negative.** Removing a constraint *enlarges* the feasible set: all previously feasible portfolios remain, plus lower-return ones become eligible. "Cannot enlarge" reverses the truth. |
| D | False | The objective was risk minimization, so the return it happens to select (6%) does not establish the maximum achievable return. |
| E | False | **Double negative.** Moving up from GMV trades more variance for more return, so a higher-return portfolio *can* have higher variance than GMV. "Cannot also have higher variance" reverses the conclusion. |

**Reference:** Constrained minimum-variance vs. GMV, feasible-set expansion — Markowitz frontier; Investopedia "Efficient Frontier."

### [QF-D4G3Q1] Sharpe ratio comparison
**Scenario:** With a 2% risk-free rate, Portfolio A returns 10% at 16% volatility; Portfolio B returns 8% at 8% volatility.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Expected excess return = `10% − 2% = 8%`. |
| B | False | **Double negative.** A's Sharpe = `(0.10 − 0.02)/0.16 = 0.08/0.16 = 0.50`. "Is not 0.50" reverses the correct value. |
| C | True | B's Sharpe = `(0.08 − 0.02)/0.08 = 0.06/0.08 = 0.75`. |
| D | False | Maximizing Sharpe weighs excess return *and* volatility; A's higher raw return doesn't make it max-Sharpe (its Sharpe 0.50 < B's 0.75). |
| E | True | B's Sharpe (0.75) exceeds A's (0.50), so B has the higher excess return per unit of volatility under the stated inputs. |

**Reference:** Sharpe ratio definition & ranking — Sharpe (1966); Investopedia "Sharpe Ratio"; CFA curriculum.

### [QF-D4G3Q2] Tangency portfolio and the Capital Allocation Line
**Scenario:** A mean-variance analyst identifies the tangency portfolio of risky assets and explains it to a committee that can also lend/borrow at the modeled risk-free rate.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The tangency portfolio is the risky portfolio with the maximum Sharpe ratio given the model's inputs and feasible set. |
| B | True | Graphically, the CAL from the risk-free asset is **tangent** to the risky efficient frontier at the tangency portfolio (the steepest line = highest Sharpe). |
| C | False | Investors do *not* all hold only the tangency portfolio; risk tolerance sets the mix between the tangency portfolio and risk-free lending/borrowing. |
| D | False | **Double negative.** Investors *can* combine the tangency portfolio with the risk-free asset to choose different risk levels — that mix moves them along the CAL. "Cannot combine" reverses the truth. |
| E | False | The tangency (max-Sharpe) portfolio and the GMV (min-variance) portfolio are different objectives and generally different portfolios. |

**Reference:** Tangency portfolio, Capital Allocation Line, two-fund separation — Investopedia "Tangency Portfolio," "Capital Allocation Line"; CFA curriculum "Portfolio Risk and Return."

### [QF-D4G3Q3] Risk-free rate changes the Sharpe ranking
**Scenario:** Portfolio X: 9% return, 10% vol; Portfolio Y: 13% return, 20% vol. The committee studies how the assumed risk-free rate affects their Sharpe ratios.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | **Double negative.** At `R_f = 1%`, X's Sharpe = `(0.09 − 0.01)/0.10 = 0.80`. "Is not 0.80" reverses the correct value. |
| B | True | At `R_f = 1%`, Y's Sharpe = `(0.13 − 0.01)/0.20 = 0.12/0.20 = 0.60`. |
| C | True | At `R_f = 5%`: X = `(0.09 − 0.05)/0.10 = 0.40`; Y = `(0.13 − 0.05)/0.20 = 0.40` — equal Sharpe ratios. |
| D | True | Subtracting the same `R_f` divides by different volatilities, so changing `R_f` can change the Sharpe *ranking* when candidates differ in volatility (X leads at 1%, tie at 5%). |
| E | False | Raising `R_f` with risky returns fixed *lowers* excess return (`E[R] − R_f`) for both — it does not increase it. |

**Reference:** Sharpe ratio sensitivity to the risk-free rate — Sharpe (1966); Investopedia "Sharpe Ratio," "Risk-Free Rate."

### [QF-D4G4Q1] Dominance and efficiency among three portfolios
**Scenario:** Portfolio A: 7% return / 9% vol; B: 7% / 12%; C: 9% / 12%. The committee assesses which are efficient.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | **Double negative.** A *does* dominate B — same 7% return at lower volatility (9% < 12%). "B is not dominated by A" reverses the truth. |
| B | False | **Double negative.** C *also* dominates B — higher return (9% > 7%) at equal 12% volatility. "Not also dominated by C" reverses the truth. |
| C | False | Lying "numerically between" A and C does not make B efficient; B is dominated by both, so it is off the frontier. |
| D | True | This is the definition of mean-variance efficiency: an efficient portfolio can't raise return without raising risk, nor cut risk without cutting return. |
| E | True | Neither A nor C dominates the other — C's higher return comes with higher risk — so both can be efficient. |

**Reference:** Dominated vs. efficient portfolios, efficient frontier — Markowitz (1952); Investopedia "Efficient Frontier."

### [QF-D4G4Q2] Tracing the frontier via minimum variance at target returns
**Scenario:** An optimizer finds minimum volatility for target returns 5%, 7%, 9%, 11%. The GMV portfolio has a 6% expected return.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | For each target, the optimizer solves for the lowest-variance feasible portfolio meeting that return — this constructs the frontier point-by-point. |
| B | True | The **upper** branch, starting at the GMV point, is the mean-variance efficient frontier (portfolios above GMV give the efficient risk-return tradeoffs). |
| C | False | A portfolio targeting 5% is *below* the GMV's 6% return; GMV offers a higher return at no greater risk, so the 5% portfolio is **dominated** and inefficient. |
| D | True | Moving up the efficient frontier means accepting more volatility for higher expected return. |
| E | False | Most feasible portfolios are interior or dominated (inefficient); only the frontier portfolios are efficient. |

**Reference:** Frontier construction, GMV as the frontier's turning point — Markowitz mean-variance; Investopedia "Efficient Frontier."

### [QF-D4G4Q3] Adding a low-correlation asset shifts the frontier
**Scenario:** A new low-correlation asset becomes investable. The team reruns the optimization with the same return targets and otherwise unchanged inputs.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Expanding the investable set cannot worsen the minimum variance at a given target: the optimizer can still choose any previously feasible portfolio, so the minimized objective can only stay equal or improve. |
| B | False | **Double negative.** Useful diversification *can* shift the frontier outward (lower risk for a given return). "Cannot shift outward" reverses the truth. |
| C | False | **Double negative.** If the new asset gets zero weight everywhere, the selected portfolios and frontier are unchanged. "Cannot remain unchanged" reverses the conclusion. |
| D | False | Adding an asset does not force positive weight in every efficient portfolio — it may be unattractive or redundant at some or all frontier points. |
| E | True | A frontier shift reflects changes in *feasible* (model-implied) risk-return combinations; it is not a guarantee about realized future performance. |

**Reference:** Diversification & frontier improvement, model-conditional frontier — Markowitz; Investopedia "Efficient Frontier," "Diversification."

### [QF-D4G5Q1] Extreme weights as estimation error
**Scenario:** A mean-variance optimizer using historical inputs assigns 78% to one small-cap stock plus small shorts. The CIO asks whether it found a uniquely attractive opportunity.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | MV optimization is highly sensitive to inputs — small changes in expected-return estimates can produce large weight shifts (**error maximization**). |
| B | True | An extreme allocation can reflect **estimation error** (noisy forecasts) rather than genuine economic attractiveness. |
| C | False | In-sample optimality does not guarantee the weights stay optimal out of sample. |
| D | False | **Double negative.** Realistic position limits *can* produce a more stable, implementable portfolio. "Cannot produce a more stable portfolio" reverses the truth. |
| E | True | Historical optimization can **overfit** the sample used to estimate inputs, exploiting sample-specific noise. |

**Reference:** Estimation error, error maximization, constraints for stability — Michaud (1989) "The Markowitz optimization enigma"; Investopedia "Estimation Error."

### [QF-D4G5Q2] Different windows, different max-Sharpe allocations
**Scenario:** Two analysts estimate expected returns for the same four assets from different historical windows. Covariance estimates are similar, but their max-Sharpe allocations differ sharply.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Expected returns are **estimates** subject to forecast error, not certainties. |
| B | True | Small differences in expected returns can be **amplified** into large differences in optimized weights. |
| C | False | Similar covariance matrices do not guarantee similar max-Sharpe portfolios — different expected-return vectors can materially change the solution. |
| D | False | **Double negative.** Comparing allocations across windows *does* reveal sensitivity to the chosen sample; large swings are evidence of instability. "Cannot reveal sensitivity" reverses the truth. |
| E | False | Reporting more decimal places does not reduce the uncertainty in the estimated inputs — precision ≠ accuracy. |

**Reference:** Input sensitivity of MV weights — Michaud (1989); Investopedia "Estimation Error"; CFA curriculum on inputs to optimization.

### [QF-D4G5Q3] Understated covariance and garbage-in-garbage-out
**Scenario:** A covariance matrix understates the link between two tech stocks (calm-period sample). The optimizer assigns both large weights and reports substantial diversification.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Understated covariance makes the holdings look more independent than they are, so the optimizer **overstates** the diversification benefit. |
| B | True | If realized covariance is higher than estimated, the larger cross-covariance term raises realized portfolio variance above forecast (`σ_p2` rises with `w_i w_j σ_ij`). |
| C | False | Solving the specified model exactly cannot make an incorrect covariance assumption accurate — computation ≠ correct inputs. |
| D | True | **Shrinkage**, longer/alternative samples, and stress scenarios are legitimate ways to test or reduce reliance on one noisy covariance estimate. |
| E | False | **Double negative.** "Garbage in, garbage out" applies precisely because a mathematically correct optimizer *can* still produce a poor allocation from poor estimates. The statement's "cannot still produce a poor allocation" reverses the truth. |

**Reference:** Covariance estimation error, shrinkage, garbage-in-garbage-out — Ledoit & Wolf shrinkage; Investopedia "Covariance," "Estimation Error."

### [QF-D4G6Q1] Constraints on a leveraged, high-turnover proposal
**Scenario:** An unconstrained optimizer recommends 160% equities, −60% bonds, with heavy monthly rebalancing. A pension plan cannot short, permits no leverage, and wants to limit trading costs.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | **Double negative.** The −60% bond position is a short, which violates the long-only policy, so the allocation *is* infeasible. "Is not infeasible" reverses the truth. |
| B | True | A gross-exposure/leverage constraint limits total long + short exposure and can prevent the 160% long financed by the bond short. |
| C | False | **Double negative.** A turnover constraint *does* limit how far new weights move from current weights. "Cannot limit" reverses the truth. |
| D | False | Adding constraints cannot *improve* the modeled maximum Sharpe — restricting the feasible set can only hold or lower the in-sample objective (though it aids real-world robustness). |
| E | True | A constrained portfolio may give up some in-sample objective value in exchange for being implementable/holdable by the institution. |

**Reference:** Long-only/leverage/turnover constraints, feasible-set restriction — Grinold & Kahn "Active Portfolio Management"; Investopedia "Portfolio Constraints."

### [QF-D4G6Q2] Binding sector cap
**Scenario:** A fund caps any sector at 30%. Its unconstrained max-Sharpe solution puts 55% in technology because estimated tech returns are slightly higher.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | A 55% technology allocation exceeds the 30% cap, so the unconstrained solution is infeasible under the constraint. |
| B | False | **Double negative.** Cutting technology from 55% to ≤ 30% requires reallocating **at least 25 percentage points** away from tech. The phrasing "at least 25 pp must *not* be reassigned" reverses the correct conclusion. |
| C | False | The constrained optimum cannot have a *higher* modeled Sharpe than the unconstrained one — the unconstrained feasible set contains all constrained portfolios, so it attains at least as high an objective. |
| D | True | A cap limits the damage if the optimizer exaggerated technology's attractiveness — it reduces exposure to estimation error concentrated in one sector forecast. |
| E | True | If tech lands exactly at 30%, the sector constraint is **binding** (optimum sits on the boundary; relaxing it could change the solution). |

**Reference:** Sector limits, binding constraints, constrained vs. unconstrained objective — Investopedia "Binding Constraint," "Portfolio Constraints"; Grinold & Kahn.

### [QF-D4G6Q3] One-way turnover constraint
**Scenario:** A fund holds 50% A / 50% B. The optimizer proposes 20% A / 80% B, but the mandate caps one-way turnover (defined as half the sum of absolute weight changes) at 10% per rebalance.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | A falls 50% → 20% (−30 pp); B rises 50% → 80% (+30 pp). |
| B | True | One-way turnover = `1⁄2(|−30%| + |+30%|) = 1⁄2(60%) = 30%`. |
| C | False | The required 30% turnover exceeds the 10% cap, so the proposed trade violates the limit. |
| D | False | **Double negative.** Moving 10 pp from A to B (→ 40% A / 60% B) gives one-way turnover of exactly 10%, which *is* feasible. "Could not be 40%/60%" reverses the truth. |
| E | False | **Double negative.** A binding turnover cap *can* cause the portfolio to adjust toward the target gradually over several rebalances rather than immediately. "Cannot cause ... over several rebalances" reverses the conclusion. |

**Reference:** Turnover constraints and phased rebalancing — Grinold & Kahn "Active Portfolio Management"; Investopedia "Portfolio Turnover."

### [QF-D4G7Q1] In-sample optimization and evaluation
**Scenario:** A researcher uses ten years of monthly returns to estimate inputs, choose weights, and report performance over the *same* ten years, beating an equal-weight benchmark in that sample.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | **Double negative.** The comparison *is* in-sample — the same observations drove both weight selection and performance measurement. "Is not in sample" reverses the truth. |
| B | True | Choosing the best weights for the historical sample can capitalize on **noise** that won't repeat (overfitting). |
| C | False | In-sample outperformance does not guarantee superior future performance even if the optimizer solved the problem correctly — estimated relationships may not persist. |
| D | True | Evaluating the fixed weights on later, previously unused data provides a genuine **out-of-sample** test. |
| E | True | Repeatedly revising the strategy after inspecting the test period contaminates its independence — the test data becomes part of development. |

**Reference:** In-sample vs. out-of-sample, overfitting portfolio weights — Investopedia "Backtesting," "Overfitting"; ISLR ch.5 (validation) by analogy.

### [QF-D4G7Q2] Ex post optimal weights and look-ahead bias
**Scenario:** A team computes each calendar year's ex post optimal portfolio using that year's *complete* returns, then presents the sequence as a strategy an investor could have followed in real time.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | **Stacked double negative.** "Uses information that *was not unavailable*" = "was available." Full-year returns reveal outcomes an investor could **not** know at the year's start, so the info was *not* available — the statement is false. |
| B | True | Applying hindsight-selected (ex post) weights as if known earlier creates **look-ahead bias**. |
| C | False | **Double negative.** A realistic simulation *must* estimate weights using only information available before each decision. "Would not need to" reverses the truth. |
| D | False | Each annual optimization being mathematically valid does not make the sequence a valid backtest — correct math doesn't cure improper timing of the information used. |
| E | True | Expected returns, volatilities, and correlations change across periods, so the portfolio optimal after one year need not stay optimal during the next. |

**Reference:** Look-ahead bias, ex post vs. ex ante optimization — Investopedia "Look-Ahead Bias," "Backtesting"; Grinold & Kahn on realistic implementation.

### [QF-D4G7Q3] Rolling-window weight instability
**Scenario:** A manager estimates optimal weights on rolling five-year windows. The allocation swings from 70% Asset A in one window to 15% in the next, while an equal-weight portfolio stays comparatively stable.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | A large allocation reversal from modest sample changes indicates an **unstable** estimated optimum (high sensitivity to inputs). |
| B | False | **Double negative.** Weight instability *does* generate turnover and trading costs — following shifting targets requires trades that erode realized performance. "Cannot generate turnover" reverses the truth. |
| C | False | Stability alone does not prove the equal-weight portfolio earns higher future returns (though it may reduce estimation/trading risk). |
| D | True | Comparing rolling-window results with genuinely out-of-sample results helps assess whether the historical optima persist (robustness). |
| E | True | Regularization, **shrinkage**, or allocation bounds can reduce the optimizer's extreme response to noisy inputs. |

**Reference:** Weight instability, robustness techniques (shrinkage/regularization/bounds) — Michaud (1989); Ledoit & Wolf; Investopedia "Estimation Error."

## References (domain-level)

1. **Markowitz, H. (1952), "Portfolio Selection," *Journal of Finance*; and *Portfolio Selection: Efficient Diversification of Investments* (1959):** mean-variance optimization, portfolio variance `wTΣw`, the efficient frontier, GMV portfolio, and diversification via covariance.
2. **Grinold, R. & Kahn, R., *Active Portfolio Management*:** practical constraints (long-only, leverage/gross-exposure caps, sector limits, turnover), implementation shortfall/transaction costs, and the gap between mathematically optimal and implementable portfolios.
3. **CFA Institute curriculum, "Portfolio Risk and Return" (Levels I–II):** Sharpe ratio, Capital Allocation Line, capital market line, tangency portfolio, two-fund separation, and inputs to optimization.
4. **Investopedia:** "Efficient Frontier," "Tangency Portfolio," "Capital Allocation Line," "Minimum Variance Portfolio," "Sharpe Ratio," "Gross/Net Exposure," "Portfolio Constraints," "Portfolio Turnover," "Estimation Error," "Look-Ahead Bias," "Backtesting."
5. **Michaud, R. (1989), "The Markowitz Optimization Enigma: Is 'Optimized' Optimal?" *Financial Analysts Journal*; Ledoit & Wolf (2003/2004) covariance shrinkage:** estimation error, error maximization, and robustness remedies (shrinkage, resampling, constraints).
