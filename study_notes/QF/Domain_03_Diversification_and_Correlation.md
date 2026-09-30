# QF Domain 3 — Diversification and Correlation

## Domain cheat-sheet

- **Correlation (ρ)** measures the *strength and direction of linear co-movement*, standardized to **[-1, +1]**. It is unitless. It is a *tendency*, not a period-by-period rule: ρ = -0.60 means the assets have tended to move oppositely, NOT that one gains every time the other loses, and NOT that "60% of losses were offset."
  - **Correlation ≠ causation** — a statistical association alone never establishes that one series drives the other.
  - Correlation is an **estimate** from a finite sample; it varies with the data window and market regime (estimation uncertainty).
  - Near-zero linear ρ means little *linear* association, but does **not** prove independence — nonlinear dependence can remain.
  - Strong positive ρ (e.g., 0.70) still allows individual periods where the two returns have opposite signs.
- **Covariance vs. correlation**: `Cov(A,B) = ρ · σ_A · σ_B`, and equivalently `ρ = Cov(A,B) / (σ_A · σ_B)`. Covariance carries the product of the return units; correlation is the standardized (unitless) version.
  - Doubling *both* volatilities (ρ fixed) multiplies covariance by **4** (2×2), not 2 — covariance scales with the *product* of the standard deviations.
  - Individual variances are always **≥ 0**; a *negative* covariance describes *joint* movement, not a negative stand-alone variance.
- **Two-asset portfolio variance**: `σ_p² = w_A²σ_A² + w_B²σ_B² + 2·w_A·w_B·Cov(A,B)`. Portfolio volatility = `√σ_p²` — NOT the weighted average of the component variances/volatilities. Omitting the cross-covariance term is wrong; it is exactly where diversification lives.
  - With positive weights, a **larger covariance raises** portfolio variance; a **lower/negative covariance lowers** it. This is why two identically-volatile assets can form portfolios with very different risk.
  - **Expected return** of the portfolio is just the weighted average of expected returns — it is unaffected by correlation. So risk can fall via imperfect co-movement *without* a proportional cut in expected return.
- **Specific (idiosyncratic) vs. systematic risk**:
  - **Specific/idiosyncratic**: tied to one issuer/event (a regulatory ruling, an accounting scandal). **Diversifiable** — spreading across many unrelated names dilutes it.
  - **Systematic/market-wide**: recessions, rate shocks, economy-wide deleveraging. Affects most securities and **cannot be diversified away** within that asset class, no matter how many names you hold.
  - Diversification reduces specific risk; it never immunizes against common market declines.
- **Diversification benefits**: combining **imperfectly correlated** (ρ < 1) assets lowers combined risk. Negative correlation acts as a **hedge**; with ρ = -1 and correct weights, paired variability can theoretically be eliminated. A hedge/diversifier need NOT have the highest stand-alone return — value comes from covariance reduction, and giving up some upside in booms is the price of protection.
- **Concentration & position sizing**: a large single weight amplifies both issuer-specific event risk and *estimation error* in the thesis (a 35% weight × 50% loss = 17.5% portfolio hit). Equal *single-name* weights do NOT remove **sector/factor** concentration (e.g., 8 of 10 names being regional banks). Inverse-volatility sizing that ignores correlations can hand a large weight to an asset that is heavily correlated with the rest — risk contribution depends on weight AND covariance, not stand-alone vol alone. Use multi-dimensional limits (single-name, sector, factor, scenario).
- **Diminishing marginal diversification**: the first few independent additions remove the most idiosyncratic risk; later additions help less as the diversifiable component shrinks toward a **floor set by systematic risk**. Adding a **redundant** holding (high ρ, same signals) — regardless of a different manager name — provides little/no benefit and can even raise risk. Marginal benefit must be judged *relative to the existing portfolio*, not in isolation; a higher-vol but genuinely different return driver can beat a low-vol look-alike.
- **Correlation instability / crisis behavior**: correlations are **regime-dependent** and tend to **rise toward 1 during stress** (common deleveraging, funding/liquidity shocks synchronize returns). Calm-period estimates understate crisis co-movement, so full-sample averages can hide tail dependence exactly when protection is needed. **Leverage** magnifies the damage when realized correlations exceed the forecast. Mitigate with stress/scenario analysis, shrinkage, and exposure limits — instability is a reason to *manage* estimates, not to abandon diversification.

## Common traps

- **NO inverted-logic questions in this slice.** Every question uses a standard "Answer Key:" (True = accurate). There is no "True = incorrect; False = accurate" header anywhere in QF-D3. Do NOT assume polarity flips just because many choices sound negative — read each verdict straight.
- **Double-negative "embedded claim" choices are the real trap.** Many choices assert the *negation* of a true fact, so the correct verdict is **False**. The Answer Key flags these with the phrase **"The statement reverses the correct conclusion."** Parse the inner claim, judge its truth, then apply the negation. These occur at: **G1Q1-E, G2Q1-A, G2Q2-D, G2Q2-E, G3Q1-A, G3Q1-B, G3Q3-B, G3Q3-D, G4Q1-C, G4Q2-E, G5Q1-D, G5Q2-C, G5Q3-C, G5Q3-E, G6Q2-D, G7Q1-A, G7Q1-D.**
- **"Cannot / could not / not" framing.** Choices like "diversification cannot reduce…", "correlation cannot rise…", "a limit cannot constrain…" negate a true statement → **False**. When a choice claims something is *impossible* about a real diversification/correlation effect, suspect it is False.
- **Correlation ≠ causation, offset %, or a period-by-period guarantee.** ρ = -0.60 does not mean 60% of losses are offset (G1Q1-B, False) and does not prove causation (G1Q1-D, False). Strong ρ still permits opposite-sign periods (G1Q2-D, False).
- **Stand-alone stats never settle portfolio risk.** "Unchanged individual volatilities ⇒ unchanged portfolio risk" (G1Q3-D) and "equal expected returns ⇒ covariance is irrelevant" (G2Q3-E) are both **False** — covariance is the missing term.
- **Counting names ≠ diversification.** Equal weights, dollar neutrality, or a large position count do not eliminate shared-driver/systematic risk (G3Q3-C, G5Q2-C, G6Q2-E). A different manager label does not make a return stream independent (G6Q2-C).

## Questions

### [QF-D3G1Q1] Interpreting a -0.60 correlation between two strategies
**Scenario:** A family office holds two strategies with similar expected returns and volatilities and a historical return correlation of -0.60. The investment committee asks whether this means one strategy reliably gains whenever the other loses.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Negative correlation summarizes a *tendency* toward opposite co-movement over the sample, not an exceptionless period-by-period rule — some periods can still move together. |
| B | False | Correlation is a standardized measure of *linear* co-movement in [-1, +1]; it is not an "offset percentage." ρ = -0.60 does not mean 60% of one strategy's losses were exactly offset. |
| C | True | Moving ρ from -0.60 to +0.60 (weights and vols fixed) raises the covariance term `2·w_A·w_B·ρ·σ_Aσ_B`; with positive weights that increases portfolio variance and volatility. |
| D | False | A statistical association does not establish causation — correlation alone cannot show that one strategy's moves *cause* the other's. |
| E | False | **Embedded-claim / reverses the conclusion:** standardized correlation is bounded to [-1, +1]; saying it "is not bounded" reverses the correct fact, so the statement is False. |

**Reference:** Correlation definition and bounds — Investopedia "Correlation Coefficient"; Bodie-Kane-Marcus *Investments*, risk & return chapter (correlation vs. causation).

### [QF-D3G1Q2] Choosing a diversifier: ρ ≈ 0.05 vs. ρ = 0.70
**Scenario:** A pension fund compares Asset A with two diversifiers: Asset B (ρ = 0.05 with A) and Asset C (ρ = 0.70 with A). The CIO proposes calling B "independent" and C "the same trade."
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | A correlation near zero indicates little *linear* co-movement with A in the observed sample. |
| B | False | Near-zero linear correlation does not prove statistical or economic independence — nonlinear dependence or other relationships can remain. |
| C | True | Lower correlation generally reduces the covariance contribution to combined variance, so B ordinarily offers more diversification relative to A than C does. |
| D | False | A 0.70 correlation is a strong-but-imperfect linear tendency; it still allows periods where A and C returns have different signs. |
| E | True | Correlations are estimates that vary with the sample period and regime, so they should be read with estimation uncertainty in mind. |

**Reference:** Correlation vs. covariance and independence — Investopedia "Covariance vs. Correlation"; CFA curriculum, portfolio risk & return (correlation inputs, estimation uncertainty).

### [QF-D3G1Q3] Correlation rising from 0.10 to 0.80 (equal-weight, equal-vol)
**Scenario:** A multi-asset fund holds equal weights in two assets, each 20% annual volatility. Estimated correlation rose from 0.10 to 0.80 while expected returns and individual volatilities were unchanged; the risk committee must decide whether to cut exposure.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | `Cov = ρ·σ_Aσ_B`; with σ's fixed, raising ρ from 0.10 to 0.80 raises covariance directly. |
| B | False | Portfolio *expected return* is the weighted average of the two expected returns and is unaffected by correlation; only the variance calculation changes. |
| C | False | **Embedded-claim / reverses the conclusion:** the underlying claim (higher ρ raises volatility, all else equal) is correct and should be accepted, so saying a reviewer "would be wrong to accept" it is False. Larger covariance raises portfolio variance for positive weights. |
| D | False | Unchanged stand-alone volatilities are not sufficient — portfolio risk also depends on covariance among holdings, which just rose. |
| E | True | Portfolio risk depends on how holdings move together, not only on individual risk; co-movement determines how much fluctuations offset or reinforce. |

**Reference:** Two-asset portfolio variance formula — Bodie-Kane-Marcus *Investments* (optimal risky portfolios); Markowitz portfolio theory (variance depends on covariance).

### [QF-D3G2Q1] Covariance vs. correlation are not interchangeable
**Scenario:** An asset manager weighs equal positions in Funds X (10% vol) and Y (20% vol) with correlation 0.50. A junior analyst claims their covariance is 0.50 because "covariance and correlation are interchangeable."
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | **Embedded-claim / reverses the conclusion:** in decimals, `Cov = 0.50 × 0.10 × 0.20 = 0.010`. The choice says covariance is *not* 0.010, which reverses the correct arithmetic, so it is False. |
| B | True | Correlation is standardized and unitless; covariance retains the product of the return units — they are not the same object. |
| C | True | `ρ = Cov / (σ_A·σ_B)` recovers correlation when both standard deviations are nonzero — the defining relationship. |
| D | False | Doubling both volatilities multiplies their *product* by 4, so covariance (ρ fixed) is multiplied by 4, not merely doubled. |
| E | True | Positive covariance reflects a tendency for deviations from each mean to share the same sign (co-movement in the same direction). |

**Reference:** Covariance–correlation identity — Investopedia "Covariance vs. Correlation"; CFA curriculum, statistics/portfolio math.

### [QF-D3G2Q2] Two-asset portfolio variance calculation (60/40)
**Scenario:** A portfolio holds 60% Asset A and 40% Asset B, with annual variances 0.0225 and 0.0100 and covariance 0.0030. The manager asks the quant team to walk through the portfolio-variance computation.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Correct expression: `(0.60²×0.0225) + (0.40²×0.0100) + (2×0.60×0.40×0.0030)` — weighted variances plus the cross-covariance term. |
| B | True | The terms are 0.00810 + 0.00160 + 0.00144 = **0.01114**, matching the stated value. |
| C | False | Omitting the covariance term ignores whether the assets reinforce or offset each other — it does not correctly measure portfolio variance. |
| D | False | **Embedded-claim / reverses the conclusion:** with positive weights a *lower* covariance reduces the cross term and thus lowers portfolio variance; "would not be lower" reverses this, so False. |
| E | False | **Reverses the conclusion (awkwardly worded):** volatility *is* the square root of portfolio variance and is *not* the weighted average of the variances. The choice's phrasing denies the correct relationship, so it is False. **Note:** the double-"not" wording is confusing; anchor on the verdict — variances combine via the covariance formula, then the square root gives volatility. |

**Reference:** Portfolio variance & volatility — Bodie-Kane-Marcus *Investments* (portfolio math); Markowitz mean-variance framework.

### [QF-D3G2Q3] Comparing 50/50 portfolios with positive vs. negative covariance
**Scenario:** A risk committee compares two 50/50 portfolios built from 15%-vol assets: Portfolio P's pair has covariance 0.0180, Portfolio Q's pair has covariance -0.0045. Expected returns are identical and the committee wants the lower-risk allocation.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | P's positive covariance produces a larger positive cross term than Q's negative covariance, so P contributes more to portfolio variance. |
| B | True | Offsetting (negative) co-movement can lower combined risk even though Q's component assets have the same stand-alone volatility as P's. |
| C | False | A negative *covariance* describes joint movement; individual variances cannot be negative, so it says nothing about negative stand-alone variance. |
| D | True | The portfolios differ in co-movement, which is essential to total variance — evaluating only individual volatilities would miss the principal difference. |
| E | False | With equal expected return, covariance is precisely what distinguishes the two; the lower-risk (lower-covariance) portfolio may be preferred, so covariance does affect the decision. |

**Reference:** Covariance's contribution to portfolio variance — Markowitz portfolio theory; Investopedia "systematic vs. idiosyncratic risk" (co-movement).

### [QF-D3G3Q1] Concentrated pharma position: specific vs. systematic risk
**Scenario:** A long-only equity fund holds nearly all capital in one pharmaceutical company awaiting a regulatory decision. The PM argues the calm broad market makes fund risk low; the CRO asks the team to separate company-specific from market-wide exposure.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | **Embedded-claim / reverses the conclusion:** a ruling tied to one issuer *is* primarily a specific-risk event; the choice denies this, so False. |
| B | False | **Reverses the conclusion:** spreading the position across many unrelated companies *can* reduce exposure to that single idiosyncratic decision; "could not reduce" is False. |
| C | True | A broad recession that depresses most equities is systematic (market-wide) risk that cannot be diversified away within equities. |
| D | False | Holding more companies dilutes specific risk but broad market (systematic) exposure remains — it is not "guaranteed elimination of all equity-market risk." |
| E | True | Low recent market volatility does not remove the concentrated company's event risk; issuer-specific catalysts can move independently of the aggregate market. |

**Reference:** Systematic vs. idiosyncratic risk — Investopedia "Systematic vs. Unsystematic Risk"; Bodie-Kane-Marcus *Investments* (diversification and firm-specific risk).

### [QF-D3G3Q2] Expanding from 20 to 500 stocks (same exposures)
**Scenario:** An index manager grows a portfolio from 20 to 500 stocks while keeping roughly the same market and sector exposures. A client expects this to eliminate both stock-selection risk and losses during market crashes.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | More reasonably diversified holdings give idiosyncratic gains/losses more opportunity to offset, reducing firm-specific risk. |
| B | False | Retaining similar market/sector exposure preserves systematic risk; the expansion does not drive systematic exposure to zero. |
| C | True | A market-wide interest-rate shock is systematic and can still affect many or all 500 holdings. |
| D | True | Diminishing marginal benefit: early additions remove more concentration, later additions add smaller reductions in specific risk. |
| E | False | Diversification does not immunize against economy-wide shocks; a 500-stock portfolio can still post a negative return in a market decline. |

**Reference:** Diversification limits / diminishing benefit — Bodie-Kane-Marcus *Investments* (portfolio size vs. risk); Investopedia "diversification."

### [QF-D3G3Q3] Market-neutral fund with a shared funding driver
**Scenario:** A market-neutral fund holds dozens of long and short positions but finds many depend on cheap financing and liquid credit markets. The head of risk asks whether a large position count proves protection from systemic stress.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Many positions do not guarantee diversification if they share the same underlying risk driver — they can be economically redundant despite different tickers. |
| B | False | **Reverses the conclusion:** an issuer-specific scandal *is* more diversifiable than a market-wide funding shock; the choice claims it is "not more diversifiable," so False. |
| C | False | Equal dollar exposure (dollar neutrality) does not ensure neutrality to market, sector, liquidity, or other systematic factors. |
| D | False | **Reverses the conclusion:** a shared dependency on financing *can* cause seemingly distinct positions to lose together under stress; "cannot cause" is False. |
| E | True | Risk analysis should examine factor and scenario exposures, not just count securities — economic drivers reveal hidden concentrations. |

**Reference:** Factor/shared-driver risk, dollar-neutral ≠ factor-neutral — CFA curriculum (factor risk); Investopedia "systematic risk."

### [QF-D3G4Q1] Two zero-correlation risky assets reduce risk (8%/12%)
**Scenario:** A balanced fund considers combining two assets, each 8% expected return and 12% volatility, with zero correlation. The committee asks whether combining two risky assets can genuinely cut risk without lowering expected return.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Expected return is the weighted average: 0.5(8%) + 0.5(8%) = 8% under the stated assumptions. |
| B | True | With ρ = 0 the covariance term is zero, so `σ_p² = 0.5²(0.12²) + 0.5²(0.12²)`. |
| C | False | **Embedded-claim / reverses the conclusion:** variance = 0.0072, whose square root ≈ 0.0849 (8.49%), which is below 12%. The choice says volatility is "not approximately 8.49%," reversing the correct result → False. |
| D | False | Zero *linear* correlation does not prohibit simultaneous losses in the same period. |
| E | True | Expected return stays 8% while volatility falls to ~8.49% — risk reduction need not require a proportional cut in expected return. |

**Reference:** Diversification with imperfect correlation — Markowitz portfolio theory; Bodie-Kane-Marcus *Investments* (two-asset portfolios).

### [QF-D3G4Q2] Adding a defensive strategy with ρ = -0.40
**Scenario:** An endowment holds a growth asset and considers a defensive strategy with -0.40 correlation to it. The defensive strategy has a positive but lower stand-alone expected return; trustees worry any allocation must make the portfolio strictly worse.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Negative correlation creates a negative covariance contribution to portfolio variance, reducing total volatility. |
| B | False | A lower stand-alone expected return does not automatically make the strategy undesirable — portfolio value depends on both return and interaction with existing holdings. |
| C | True | A sufficient reduction in risk can improve the risk-return tradeoff even if expected return falls modestly. |
| D | False | Historical negative correlation does not guarantee protection in every future drawdown — correlations are estimates that shift across regimes. |
| E | False | **Reverses the conclusion (awkward wording):** diversification IS a portfolio-level concept, so the decision *should* consider joint outcomes rather than rank by stand-alone return. The choice's "should not consider joint outcomes" reverses this → False. **Note:** the double-negative phrasing is confusing; the key's point is that joint/portfolio outcomes must be considered. |

**Reference:** Negative correlation as a hedge; portfolio-level evaluation — Markowitz theory; Investopedia "hedge" and "diversification."

### [QF-D3G4Q3] Commodity producer adding an offsetting hedge
**Scenario:** A commodity producer's pension is heavily in commodity-linked securities. An adviser proposes assets that perform well when commodity prices fall; management objects that these may lag during commodity booms.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The sponsor and pension already share commodity sensitivity, so assets with offsetting commodity exposure can reduce aggregate risk. |
| B | False | A hedge need not have the highest stand-alone expected return — it can add value through covariance reduction even with a lower return. |
| C | True | Underperformance during commodity booms is the economic cost of protection — giving up some upside where the original exposure does well. |
| D | True | With ρ = -1 and appropriate sizing, weights can be chosen so the volatile components exactly offset, theoretically eliminating the paired variability. |
| E | False | Adding another commodity producer with nearly identical exposure would *reinforce*, not hedge, commodity risk — it does not provide the same offset. |

**Reference:** Hedging via negative correlation; ρ = -1 risk elimination — Markowitz theory; Bodie-Kane-Marcus *Investments* (perfect hedge case).

### [QF-D3G5Q1] Sizing a 35% high-conviction position
**Scenario:** A hedge fund manager wants 35% of capital in one high-conviction stock. The thesis is strong but the mandate limits severe drawdowns; the risk committee weighs whether conviction justifies the size.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | A 35% weight × a 50% loss ≈ 17.5% fund loss before secondary effects — direct arithmetic of position sizing. |
| B | False | A strong expected-return estimate is uncertain; sizing determines the consequence of being wrong, so it cannot be ignored. |
| C | True | A larger weight amplifies the portfolio impact of forecast errors or omitted risks — concentration raises sensitivity to estimation error. |
| D | False | **Reverses the conclusion:** a position limit *does* cap direct exposure to a single issuer/thesis; "cannot constrain the damage" is False. |
| E | False | Diversifying some capital away balances conviction with uncertainty and portfolio risk — it does not imply the manager has no conviction. |

**Reference:** Position sizing & concentration risk — CFA curriculum (risk management, position limits); Investopedia "concentration risk."

### [QF-D3G5Q2] Ten equal weights but eight regional banks
**Scenario:** A portfolio holds ten stocks at 10% each, but eight are regional banks with similar loan books and funding. The PM cites the equal weights as evidence of no concentration risk; the CRO wants a broader assessment.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Equal weights remove single-name concentration but can leave large *sector* concentration — weight dispersion doesn't remove shared industry exposure. |
| B | True | The eight bank positions share common drivers, so they may behave like a much smaller number of independent bets. |
| C | False | **Reverses the conclusion:** similar loan/funding exposures create vulnerability to the same shock, so a regional credit shock *could* cause correlated losses; "could not" is False. |
| D | False | Aggregate sector and factor concentrations remain despite the 10% single-name cap, so additional limits do serve a purpose. |
| E | True | Position controls can add sector, factor, and scenario limits to catch risks that single-name limits miss. |

**Reference:** Sector/factor concentration beyond single-name limits — CFA curriculum (risk controls); Investopedia "diversification limits."

### [QF-D3G5Q3] Inverse-volatility sizing that ignores correlation
**Scenario:** A systematic fund sizes positions inversely to each asset's volatility but ignores correlations. One low-vol asset gets a very large weight and has become strongly correlated with several other holdings; the PM asks if inverse-vol sizing alone is sufficient.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Risk contribution depends on weight *and* covariance with the full portfolio, so a low stand-alone volatility does not guarantee a small contribution. |
| B | True | A sufficiently large exposure can dominate total risk despite modest stand-alone volatility. |
| C | False | **Reverses the conclusion:** greater positive covariance means the position reinforces more of the portfolio's movement, *raising* its marginal contribution to variance; "cannot raise" is False. |
| D | False | Ignoring correlations can leave major factor/covariance concentrations, so inverse-vol sizing does not automatically produce an optimal portfolio for any covariance matrix. |
| E | False | **Reverses the conclusion:** portfolio-risk and marginal-risk calculations require weights, volatilities, and correlations *together*; "should not consider [them] together" is False. |

**Reference:** Marginal contribution to risk (weight × covariance); risk parity vs. correlation — CFA curriculum (portfolio risk); Markowitz covariance matrix.

### [QF-D3G6Q1] Diminishing returns to adding unrelated stocks
**Scenario:** A wealth manager starts with a single stock and adds equal-sized positions from unrelated industries. A client sees risk fall sharply at first but only slightly after dozens of additions and asks whether the process has stopped working.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The first few independent additions remove the most firm-specific concentration; later ones remove less. |
| B | False | Diminishing marginal benefit means later holdings help by *progressively smaller* amounts, not that they increase risk in every case. |
| C | True | As specific risk is diversified away, systematic (market) risk becomes a larger share of what remains. |
| D | False | Adding infinitely many same-market stocks cannot drive volatility to zero — systematic risk cannot be eliminated by adding names. |
| E | True | The pattern matches diversification benefits approaching a floor set by common (systematic) risks. |

**Reference:** Diminishing marginal diversification, systematic-risk floor — Bodie-Kane-Marcus *Investments* (portfolio size vs. risk curve); Investopedia "diversification."

### [QF-D3G6Q2] Redundant strategy with 0.95 correlation
**Scenario:** A multi-manager fund weighs a new equity strategy with attractive stand-alone stats but a 0.95 correlation to an existing strategy and nearly the same signals/securities. The allocator wants to count it as added diversification.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Near-identical signals and 0.95 correlation imply little new risk-offsetting behavior — limited marginal diversification. |
| B | False | Attractive stand-alone performance is not sufficient; the effect on the existing portfolio depends on covariance. |
| C | True | Diversification follows economic exposures, not labels — a different manager name does not make the return stream independent. |
| D | False | **Reverses the conclusion:** a lower-correlated alternative with similar stand-alone vol generally supplies *more* risk reduction; "could not provide more diversification" is False. |
| E | False | Adding a redundant strategy does not necessarily lower volatility; it can leave risk unchanged or, depending on funding/weights, raise it. |

**Reference:** Redundancy and marginal diversification — Markowitz theory (covariance drives benefit); Investopedia "diworsification."

### [QF-D3G6Q3] Fund M (similar) vs. Fund N (different driver, higher vol)
**Scenario:** A committee can add Fund M (resembles current holdings) or Fund N (genuinely different return driver, modestly higher stand-alone volatility) to a mature 40-holding portfolio, focused on total portfolio risk.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Fund N's low covariance with current holdings can outweigh its somewhat higher stand-alone volatility, giving a larger marginal diversification benefit. |
| B | False | The number of holdings alone is not enough — economic independence and covariance matter more than a raw count. |
| C | True | Fund M's similarity to existing holdings means redundant exposure and small incremental risk reduction. |
| D | True | Marginal diversification must be evaluated relative to the existing portfolio; the same asset can diversify one portfolio well and another poorly. |
| E | False | Choosing the lower-stand-alone-vol candidate does not always minimize portfolio volatility — a low-vol look-alike can reinforce existing risk while a higher-vol diversifier reduces total risk. |

**Reference:** Marginal diversification relative to portfolio; covariance over stand-alone vol — Markowitz theory; Bodie-Kane-Marcus *Investments*.

### [QF-D3G7Q1] Calm-period correlations underpredict crisis losses
**Scenario:** A risk model estimates correlations from five calm years and predicts a max portfolio loss of 8%. During a liquidity crisis several risky assets fall together; the CRO asks why realized diversification is weaker than projected.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False | **Reverses the conclusion:** correlations *can* rise in stress as assets respond to common deleveraging and liquidity shocks; "cannot rise" is False. |
| B | False | Dependence structures can change materially across regimes, so calm-period correlations are not guaranteed valid in crises. |
| C | True | Higher positive correlations reduce offsetting movement among long positions, weakening expected diversification. |
| D | False | **Reverses the conclusion:** a model assuming a stable covariance matrix *can* understate crisis risk because a calm-period matrix may not represent stressed co-movement; "cannot understate" is False. |
| E | True | Stress tests using adverse correlation scenarios complement historical averages by probing relationships absent from calm history. |

**Reference:** Correlation instability / crisis co-movement — CFA curriculum (risk management, stress testing); Investopedia "correlation breakdown."

### [QF-D3G7Q2] Low full-sample correlation hiding tail dependence
**Scenario:** A fund chose three asset classes for low ten-year full-sample correlations. A researcher finds each pair had near-zero correlation in normal months but above 0.75 in the worst market months; the PM must reassess drawdown protection.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Full-sample averages can conceal dependence that is strongest exactly when protection is needed (tail/stress states). |
| B | False | Low *unconditional* correlation does not ensure low correlation *conditional* on severe market losses — conditional dependence can differ sharply. |
| C | True | Stress-period evidence is relevant even if those months are a small share of the sample, since rare stress dominates drawdowns. |
| D | True | Drawdown-focused diversification should examine tail and regime behavior, not only average correlation. |
| E | False | Different asset labels/classes do not prevent common macro, liquidity, or funding exposures, so crisis correlations can be economically meaningful. |

**Reference:** Conditional/tail correlation, regime dependence — CFA curriculum (tail risk, scenario analysis); Investopedia "correlation vs. covariance," "correlation breakdown."

### [QF-D3G7Q3] Leveraged "diversified" portfolio from a forecast covariance matrix
**Scenario:** An ML team forecasts next month's covariance matrix from a rolling window and builds a highly leveraged "diversified" portfolio. The risk committee worries small estimation errors or a regime shift could invalidate the allocation.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Leverage scales losses when realized correlations exceed the forecast — it magnifies the consequences of diversification failing under stronger co-movement. |
| B | False | Even a precisely estimated historical matrix cannot eliminate uncertainty about the future — a structural or regime change can invalidate it. |
| C | False | **Reverses the conclusion:** optimization *can* amplify small input differences into large, concentrated weights, so weights are sensitive to estimation error; "cannot be sensitive" is False. |
| D | True | Combining rolling estimates with shrinkage, exposure limits, or stress scenarios reduces dependence on one noisy forecast and improves robustness. |
| E | False | Correlation instability does not make diversification worthless — it remains valuable but its estimates and limitations must be managed. |

**Reference:** Estimation error in covariance optimization, shrinkage — Ledoit-Wolf shrinkage; CFA curriculum (estimation risk, robust portfolio construction); Markowitz theory (input sensitivity).

## References (domain-level)

1. **Markowitz portfolio theory** (Markowitz, 1952, "Portfolio Selection"): mean-variance framework; portfolio variance `σ_p² = ΣΣ w_i w_j Cov(i,j)`; diversification benefit from imperfect (ρ < 1) and negative correlation; the ρ = -1 risk-elimination case; sensitivity of optimized weights to covariance inputs.
2. **Bodie, Kane & Marcus — *Investments*:** two-asset and multi-asset portfolio math; diversification vs. portfolio size and the systematic-risk floor; firm-specific (diversifiable) vs. market (systematic) risk; the perfect-hedge case.
3. **CFA Institute curriculum — Portfolio Management & Risk:** correlation as an estimated input, estimation uncertainty; factor/shared-driver and sector concentration beyond single-name limits; position sizing and risk controls; stress testing and tail/regime risk; estimation risk in portfolio construction.
4. **Investopedia:** "Covariance vs. Correlation," "Correlation Coefficient," "Systematic vs. Unsystematic (Idiosyncratic) Risk," "Diversification" (and its limits), "Diworsification," "Correlation Breakdown."
5. **Ledoit & Wolf — covariance-matrix shrinkage:** improving robustness of estimated covariance/correlation inputs for portfolio optimization (relevant to G7Q3).
