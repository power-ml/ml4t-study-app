# QF Domain 4 — Fundamental Law of Active Portfolio Management

## Domain cheat-sheet

- **The simplified Fundamental Law.** The headline result ties forecasting skill and scale to risk-adjusted active performance:
  - **IR ≈ IC · √BR** — the (annualized) **information ratio** equals the **information coefficient** times the **square root of breadth**. Memorize this; most of the domain is applying, rearranging, or stress-testing it.
  - The structure is **linear in IC** and **square-root in BR**. A proportional change in IC passes through *fully* to IR; a proportional change in breadth passes through its *square root*. Doubling IR via skill needs IC to double; doubling IR via scale needs breadth to **quadruple** (√4 = 2).
  - A generalized form adds the **transfer coefficient (TC)**: **IR ≈ TC · IC · √BR**, where TC ∈ [0,1] measures how faithfully forecasts are translated into actual positions. TC < 1 captures the drag from constraints (long-only, leverage/short limits, turnover/liquidity caps). The *simplified* law implicitly assumes TC = 1 (frictionless, efficient implementation).
- **Information coefficient (IC).** The cross-sectional correlation between forecasts and subsequently realized **benchmark-relative (active)** returns.
  - A **positive IC** means higher forecasts are, *on average*, associated with higher active returns — correct *ordering on average*, not certainty for any single asset. Correlation permits many individual forecast errors.
  - ICs are **small by nature** (≈0.02–0.10 for good equity signals). A modest IC can be economically valuable *if* it is stable and applied across many sufficiently independent opportunities.
  - IC is **noisy**: an estimate from a finite, dependent sample can differ from the underlying relationship. More (independent) observations and regime coverage shrink sampling uncertainty; a larger point estimate from a tiny sample is **not** automatically more reliable.
  - A **negative IC** means forecasts have been directionally wrong on average *under the current measurement* — it does not prove the model is information-free (sign, labeling, or timing may be inverted). Negating every forecast flips the sign of the correlation, but a reversal must be validated (data/timing errors vs. genuine inverse signal vs. unstable coincidence) before deployment. An IC near zero rules out *linear* association, not every nonlinear relationship.
- **Information ratio (IR).** Active return per unit of **active risk**: **IR = (active return) / (tracking error)**. Both numerator and denominator are **benchmark-relative**.
  - Distinct from the **Sharpe ratio**, which uses *excess total* return over *total-return volatility*. A portfolio can post a high Sharpe (market exposure performed well) yet a low IR (active decisions added little consistently). The two use different reference returns and risk measures and need not agree.
  - IR depends on the chosen benchmark (it defines active return and tracking error). Equal historical IRs do **not** imply equal future skill — point estimates are noisy; sample length, concentration/factor dependence, costs, and regimes matter.
  - Grinold & Kahn link IR to value added: **VA ≈ IR² / (4λ)** (λ = risk aversion) — higher IR enables more value for a given risk budget. (Dollar profit still depends on capital, leverage, fees, exposures, and horizon.)
- **Breadth (BR) and effective breadth.** BR is the number of **sufficiently independent** opportunities to apply the skill per year — *not* a raw count of forecasts, securities, or trades.
  - Breadth can come from **cross-section** (more assets), **time** (more frequent decisions), or both — **provided the decisions carry independent information and outcomes**.
  - **Independence-of-bets assumption** is central and often the first thing to fail in practice. Dependent decisions (shared factor exposure, highly correlated signals, slowly-changing information re-screened frequently) contribute far less diversification than their count suggests, so **effective breadth ≪ nominal breadth**.
  - Trading *more often* or covering *more names* raises turnover/capacity demands but adds **no** effective breadth unless each decision is a genuinely new, independent bet. Factor/correlation diagnostics (incl. conditional/stress-period correlations) estimate how much nominal breadth overstates effective breadth; **state-dependent** correlations (rising in crises) make effective breadth regime-dependent, and a calm-period estimate can overstate diversification exactly when it is needed.
- **Strategy-design implications (skill vs. scale).** Because IC enters linearly and √BR sublinearly, there is a genuine **tradeoff**:
  - A **weak but broad** process (small IC, large effective breadth) can out-score a **strong but narrow** one (large IC, tiny breadth) on the simplified metric — breadth can compensate for low per-decision skill.
  - But with **zero IC the law predicts zero IR regardless of breadth** — adding skill-free opportunities does nothing. And expanding the universe can *lower* IC (poorer data, unfamiliar assets), so added breadth can be offset by reduced skill; the optimal scalable universe may stop short of the maximum.
  - **Automation adds capacity, not skill**: it lets a process evaluate more candidates but does not guarantee the decisions are independent, that IC transfers to new instruments/horizons, or that they are profitable. Prefer staged out-of-sample validation over mechanically extrapolating an estimate.
- **Limitations & practical violations.** The simplified law describes **gross forecasting potential under idealized assumptions**; realized IR routinely falls short because:
  - **Costs** (spreads, commissions, market impact) consume active return; **constraints** (long-only, leverage/short/sector/turnover limits) reduce forecast utilization (TC < 1); **capacity** limits bite as capital grows (larger orders move prices).
  - **IC is time-varying** — a positive full-sample average can hide deterioration or a regime shift; **crowding** can erode future returns even if the historical relationship was genuine. Rolling, regime-specific, and out-of-sample IC estimates test persistence.
  - A gap between predicted and realized IR does **not** prove the arithmetic was wrong — a correct calculation under unrealistic assumptions can still diverge from live results. Diagnose with turnover/cost/constraint/dependence/capacity checks.

> **Garbled-symbol flag (source slice).** The source renders the formula in raw LaTeX, e.g. `(IR=IC\sqrt{BR})`, `(0.05\sqrt{100}=0.50)`, `(\sqrt{2})` — read these as IR = IC·√BR, 0.05·√100 = 0.50, and √2. The slice also contains broken `fi`/`fl` ligatures (e.g. "proﬁtability", "ﬁgures", "beneﬁt", "diversiﬁcation", "conﬁrming", "deﬁnitions") — cosmetic PDF-extraction artifacts, no effect on meaning.

## Common traps

- **Inverted-polarity questions (10 of 21 here).** When the body says "each item asserts that its quoted statement is **incorrect** … evaluate the complete A–E items as written," the Answer-Key verdict is flipped relative to the quoted claim's truth: **True = the quoted statement is wrong; False = the quoted statement is accurate.** Read the polarity line *first*. Inverted here: **G1Q2, G1Q3, G2Q3, G3Q1, G4Q2, G4Q3, G5Q1, G6Q2, G7Q1, G7Q2.** The remaining 11 are Normal (True = accurate).
- **Count ≠ breadth.** Raw forecast count, security count, signal-column count, and decision/trade count are *not* effective breadth. Independence of information and outcomes — not timestamps, labels, or issuer identity — determines how many distinct bets exist.
- **"Trading more often always adds an opportunity."** False — re-screening slowly-changing information produces dependent decisions; nominal breadth balloons while effective breadth barely moves (and turnover/costs rise).
- **"More securities ⇒ proportionally more breadth."** False — if the forecasts mostly express one common market/sector/factor view, effective breadth is far below the headcount; a dominant sector trade links many positions through one factor.
- **IC magnitude ⇒ reliability.** A larger point estimate from a small/dependent sample is not more credible than a slightly smaller one from a large, regime-diverse sample. Reliability depends on sampling uncertainty, dependence, stability, and design.
- **Sharpe = information ratio.** They use different reference returns (risk-free vs. benchmark) and different risk measures (total vs. tracking error); high Sharpe can coexist with low IR when the market, not active skill, did the work.
- **Doubling breadth doubles IR.** False — breadth enters through a square root, so doubling BR multiplies IR by √2 ≈ 1.41. Doubling IR via breadth alone requires **quadrupling** it.
- **Negative IC ⇒ no information / just flip the signs.** A persistently negative IC can contain information, but reversing a live strategy demands investigating data labeling, execution timing, stability, and economic rationale first.
- **Simplified law = net result guarantee.** IR = IC·√BR is a gross, assumption-laden estimate. It omits costs, constraints (TC < 1), capacity, estimation error, dependence, and time variation; a predicted-vs-realized gap does not falsify the arithmetic.
- **Zero IC but lots of breadth still helps.** False — with IC = 0 the simplified law gives IR = 0 for any breadth. Breadth amplifies *existing* positive skill; it cannot manufacture it.
- **Automation preserves IC / creates breadth.** Automation adds *capacity* to evaluate more candidates; it does not guarantee IC transfers to new instruments/horizons or that the extra decisions are independent or profitable.
- **Average correlation = independence.** Zero full-sample correlation does not establish regime-independence; correlations that spike in stress make effective breadth state-dependent, so calm-period estimates overstate diversification.

## Questions

### [QF2-D4G1Q1] Interpreting a small positive information coefficient
**Scenario:** A researcher scores 200 stocks daily and compares forecasts with realized benchmark-relative returns; the correlation (IC) is +0.06. The committee debates how to interpret it.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | A positive forecast–outcome correlation (IC > 0) means higher forecasts have *on average* accompanied higher subsequent active returns — correct ordering on average, not certainty for any single stock. |
| B | False | Correlation summarizes a statistical relationship across observations; it permits many individual errors. An IC of +0.06 does **not** imply every positively-forecast stock earned a positive active return. |
| C | True | This is the core lesson of the Fundamental Law: a small but stable IC becomes economically useful when applied across many sufficiently independent opportunities, because IR = IC·√BR scales with effective breadth. |
| D | False | IC measures forecast *quality* only. Net profitability also depends on portfolio construction, risk, turnover, and trading costs — the simplified law is a gross-potential statement, not a net result. |
| E | True | An estimated correlation can differ from the underlying relationship because of finite-sample noise and dependence; sampling uncertainty must be weighed before calling an observed IC persistent skill. |

**Reference:** Grinold & Kahn, *Active Portfolio Management*, 2nd ed., ch. 6 (The Fundamental Law of Active Management — definition and interpretation of IC); Balch ML4T 02-09 (information coefficient and signal evaluation).

### [QF2-D4G1Q2] Comparing IC estimates across sample sizes
**Scenario:** Analyst A reports IC +0.04 from 20 independent observations; Analyst B reports IC +0.03 from 5,000 reasonably independent observations across several regimes. Management wants to pick the more credible process from the point estimates alone.
**Answer polarity:** **Inverted (True = the quoted statement is INCORRECT; False = the quoted statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | The quoted statement is correct: numerically +0.04 > +0.03, so Analyst A does have the larger *observed* IC. Nothing wrong to flag. |
| B | True (incorrect) | Wrong: a larger point estimate does **not** automatically make a process more statistically reliable. Reliability depends on sampling uncertainty, dependence, stability, and design — not the point estimate alone. |
| C | False (accurate) | The quoted statement is correct: other things equal, a much larger body of independent evidence (5,000 obs) permits a more *precise* estimate of a small IC — standard error falls with independent sample size. |
| D | False (accurate) | The quoted statement is correct: regime coverage matters because forecast skill can vary through time; a result spanning several environments is more informative about persistence. |
| E | True (incorrect) | Wrong: ICs cannot be compared safely without confirming the forecasts and outcomes use the **same** definitions, horizons, universes, and measurement methods — otherwise the comparison is apples-to-oranges. |

**Reference:** Grinold & Kahn, 2nd ed., ch. 6 (IC as an estimated correlation; sampling and stability) and ch. 5 (information ratio and estimation uncertainty); Balch ML4T 02-09 (evaluating signals; sample size and robustness).

### [QF2-D4G1Q3] Interpreting a persistently negative IC
**Scenario:** A futures model shows IC ≈ −0.05 for twelve months (top bullish forecasts underperform). A trader wants to reverse every signal; the model-risk team suspects inverted labels or execution timing.
**Answer polarity:** **Inverted (True = the quoted statement is INCORRECT; False = the quoted statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | The quoted statement is correct: a persistently negative IC means higher forecasts have, on average, accompanied worse outcomes *under the current measurement* — directionally wrong on average. |
| B | False (accurate) | The quoted statement is correct: multiplying every forecast by −1 reverses the sign of its correlation with the same outcomes. Negating one variable flips the correlation sign. |
| C | True (incorrect) | Wrong: a negative IC does **not** prove the model has no information — a consistently inverse signal can carry information whose direction, measurement, or implementation is wrong. |
| D | False (accurate) | The quoted statement is correct: before deploying a reversed strategy the team should check data, timing, stability, and economic rationale — a historical sign flip may be a genuine inverse signal, an error, or an unstable coincidence. |
| E | False (accurate) | The quoted statement is correct: an IC near zero indicates little *linear* association but does not by itself rule out every possible nonlinear relationship. |

**Reference:** Grinold & Kahn, 2nd ed., ch. 6 (IC sign and interpretation); Balch ML4T 02-09 (signal correlation, overfitting and validation caveats).

### [QF2-D4G2Q1] Computing and interpreting information ratios
**Scenario:** Fund 1 earns 4% active return with 8% tracking error; Fund 2 earns 3% active return with 3% tracking error (measured consistently; ignore estimation uncertainty).
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | IR = active return / tracking error = 4% / 8% = **0.50** for the first fund. |
| B | True | IR = 3% / 3% = **1.00** for the second fund. |
| C | False | Higher active return does *not* mean higher IR. The second fund earns more active return **per unit of tracking error** (1.00 > 0.50), so it has the higher IR despite the lower active return. |
| D | True | By definition IR evaluates active (benchmark-relative) return per unit of active risk — both numerator and denominator are measured relative to the benchmark. |
| E | True | A higher IR need not mean higher total dollar profit for every investor; dollars also depend on capital, leverage, fees, total exposures, and the realized horizon. |

**Reference:** Grinold & Kahn, 2nd ed., ch. 5 (The Information Ratio — definition as active return over active risk); Balch ML4T 02-09 (risk-adjusted performance metrics).

### [QF2-D4G2Q2] Sharpe ratio versus information ratio
**Scenario:** A long-only manager posts a high Sharpe ratio (both benchmark and portfolio rose), but hugged the benchmark and delivered inconsistent active returns. Why do Sharpe and IR tell different stories?
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The Sharpe ratio commonly evaluates excess *total* return (over the risk-free rate) relative to *total-return* volatility. |
| B | True | The information ratio evaluates *active* return relative to *tracking error* — both components are benchmark-relative. |
| C | True | A portfolio can post a high Sharpe but low IR when market (passive) exposure performs well while active decisions add little consistently — strong beta without demonstrated active skill. |
| D | False | The two ratios use different reference returns (risk-free vs. benchmark) and different risk measures (total vs. tracking error), so they need **not** be identical even on the same monthly returns. |
| E | True | The benchmark chosen for active-return measurement affects both active return and tracking error, and therefore the IR. |

**Reference:** Grinold & Kahn, 2nd ed., ch. 5 (information ratio vs. Sharpe ratio; benchmark dependence); Balch ML4T 02-09 (Sharpe ratio and portfolio performance statistics).

### [QF2-D4G2Q3] Equal information ratios, unequal dependability
**Scenario:** Two managers each report a historical IR of 0.8 — Manager X over ten years with a diversified portfolio, Manager Y over one favorable year with a concentrated sector bet. Should they be treated as equally dependable?
**Answer polarity:** **Inverted (True = the quoted statement is INCORRECT; False = the quoted statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | The quoted statement is correct: equal historical IRs do imply equal historical active return per unit of measured active risk *within each stated sample* — that is the ratio's definition. |
| B | True (incorrect) | Wrong: equal point estimates do **not** guarantee equal future skill — historical IRs are noisy and may not persist. |
| C | False (accurate) | The quoted statement is correct: Manager Y's one-year sample supplies less evidence about stability than a ten-year record, so it raises greater estimation-uncertainty concern. |
| D | False (accurate) | The quoted statement is correct: a concentrated factor/sector exposure can make an IR less representative of repeatable security-selection skill, since one rewarded bet can dominate measured performance. |
| E | False (accurate) | The quoted statement is correct: a proper comparison considers sample length, benchmark suitability, exposure stability, costs, and regimes in addition to the reported ratio. |

**Reference:** Grinold & Kahn, 2nd ed., ch. 5 (information ratio — sampling, stability, benchmark suitability) and ch. 6 (breadth/effective bets behind a reported ratio); Balch ML4T 02-09 (overfitting, in-sample vs. out-of-sample performance).

### [QF2-D4G3Q1] Raw forecast count versus effective breadth
**Scenario:** A strategy goes from forecasting 50 stocks monthly to forecasting the same 50 daily and claims ~21× more breadth. The stocks and daily forecast errors are strongly correlated through time.
**Answer polarity:** **Inverted (True = the quoted statement is INCORRECT; False = the quoted statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | The quoted statement is correct: raw forecast count and effective breadth are not necessarily the same — nominal decisions can repeat the same underlying information or exposure. |
| B | False (accurate) | The quoted statement is correct: strong dependence among daily decisions makes the increase in *effective* breadth much smaller than 21×, because correlated decisions add less independent diversification. |
| C | True (incorrect) | Wrong: trading more frequently does **not** always create an independent new opportunity. Independence depends on information and outcomes, not merely the decision timestamp. |
| D | False (accurate) | The quoted statement is correct: breadth concerns the number of *sufficiently independent* opportunities; the simplified law relies on distinct opportunities for skill to compound. |
| E | False (accurate) | The quoted statement is correct: more frequent rebalancing can raise turnover (and costs) even when it adds little effective breadth. |

**Reference:** Grinold & Kahn, 2nd ed., ch. 6 (breadth as the count of independent bets; independence assumption); Balch ML4T 02-09 (turnover vs. independent signal; dependence across time).

### [QF2-D4G3Q2] Security count versus effective breadth
**Scenario:** A quant forecasts 1,000 equities; a discretionary manager makes 20 sector-neutral selections yearly. The quant claims 50× the breadth because it covers 50× as many securities.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Covering more assets can create greater *potential* breadth — a broader universe offers more places to apply a forecasting process. |
| B | False | The number of securities alone is **not** sufficient to establish effective breadth; dependence and constraints determine how many distinct bets actually exist. |
| C | True | If the 1,000 forecasts mainly express the same market/sector view, their effective breadth can be far below 1,000 because common-factor exposure links outcomes. |
| D | True | The 20 discretionary selections could *also* have low effective breadth if several are versions of the same economic bet — small nominal sets can contain even fewer distinct decisions. |
| E | True | Breadth can come from opportunities across assets, time, or both, **provided** the decisions are sufficiently independent. |

**Reference:** Grinold & Kahn, 2nd ed., ch. 6 (effective breadth; common-factor dependence reduces independent bets); Balch ML4T 02-09 (diversification and correlated holdings).

### [QF2-D4G3Q3] Breadth and the scalability of skill
**Scenario:** A market-making model has modest skill but can evaluate many liquid instruments repeatedly; a niche distressed-debt analyst has stronger skill but few suitable investments yearly. The committee compares how breadth affects scalability.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The law shows breadth can amplify consistent positive skill — weak skill applied across many effective opportunities can build useful risk-adjusted performance (IR = IC·√BR). |
| B | False | Greater skill does **not** guarantee a higher IR regardless of breadth; IR depends on *both* IC and effective breadth, so a high-skill, low-breadth process can be out-scored. |
| C | True | A limited opportunity count constrains how widely specialized expertise can be deployed — expertise cannot scale into opportunities that do not exist or cannot absorb capital. |
| D | True | Automation supplies capacity to process more decisions, but it does not guarantee those decisions are independent or profitable — skill and independence remain separate requirements. |
| E | False | Adding opportunities with **no** forecast skill does not increase IR — with IC = 0 the simplified law predicts IR = 0 regardless of breadth. |

**Reference:** Grinold & Kahn, 2nd ed., ch. 6 (skill vs. breadth; IR = 0 when IC = 0); Balch ML4T 02-09 (capacity, scalability, and signal strength).

### [QF2-D4G4Q1] The IR = IC·√BR relationship
**Scenario:** Under the simplified law, a strategy has IC = 0.05 and breadth of 100 independent opportunities/year, with efficient forecast-to-position translation and all simplifying assumptions holding.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | IR = IC·√BR = 0.05·√100 = 0.05·10 = **0.50**. [Source renders this as the garbled LaTeX `(0.05\sqrt{100}=0.50)`.] |
| B | True | Holding breadth fixed, IR is linear in IC, so doubling IC to 0.10 doubles IR to 1.00 (0.10·√100). |
| C | False | Doubling breadth from 100 to 200 multiplies IR by **√2 ≈ 1.41**, not by 2 — breadth enters through a square root. |
| D | True | Going from BR = 100 to 400 quadruples breadth; √400/√100 = 20/10 = 2, so IR exactly doubles. |
| E | True | The structure is a *linear* effect of IC and a *square-root* effect of breadth — the mathematical form of IR = IC·√BR. |

**Reference:** Grinold & Kahn, 2nd ed., ch. 6 (statement of the Fundamental Law IR = IC·√BR; linear-in-IC, square-root-in-breadth); Balch ML4T 02-09 (information ratio arithmetic).

### [QF2-D4G4Q2] Comparing strategies with the Fundamental Law
**Scenario:** Strategy A: IC = 0.04, breadth 400. Strategy B: IC = 0.08, breadth 25. The team compares predicted IRs via the simplified law before costs and dependence.
**Answer polarity:** **Inverted (True = the quoted statement is INCORRECT; False = the quoted statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | The quoted statement is correct: IR_A = 0.04·√400 = 0.04·20 = **0.80**. [Slice shows garbled `(0.04\sqrt{400}=0.04(20)=0.80)`.] |
| B | False (accurate) | The quoted statement is correct: IR_B = 0.08·√25 = 0.08·5 = **0.40**. |
| C | False (accurate) | The quoted statement is correct: Strategy B's IC (0.08) is exactly twice Strategy A's (0.04). |
| D | True (incorrect) | Wrong: B's stronger skill is **not** enough to overcome its much smaller breadth here — its predicted IR (0.40) is lower than A's (0.80) because √25 ≪ √400. |
| E | True (incorrect) | Wrong: this comparison alone does **not** prove A will deliver the higher *realized net* IR — it omits estimation error, dependence, constraints, costs, capacity, and time variation. |

**Reference:** Grinold & Kahn, 2nd ed., ch. 6 (applying IR = IC·√BR; gross vs. realized performance caveats); Balch ML4T 02-09 (comparing strategies on risk-adjusted metrics).

### [QF2-D4G4Q3] Doubling IR through breadth versus skill
**Scenario:** A director wants to double predicted IR without changing IC; current effective breadth is 64. Another team instead proposes a 50% IC improvement at constant breadth.
**Answer polarity:** **Inverted (True = the quoted statement is INCORRECT; False = the quoted statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | The quoted statement is correct: doubling IR via breadth alone needs breadth to go from 64 to **256** (√256/√64 = 16/8 = 2) — doubling the square-root term requires quadrupling breadth. |
| B | True (incorrect) | Wrong: raising breadth from 64 to 128 only multiplies IR by **√2 ≈ 1.41**, not 2 — doubling breadth does not double IR. |
| C | False (accurate) | The quoted statement is correct: with breadth fixed, IR is linear in IC, so a 50% IC increase gives a 50% IR increase. |
| D | False (accurate) | The quoted statement is correct: a proportional IC change passes through fully, while breadth enters via a square root, so improving IC has a stronger proportional payoff than an equal proportional breadth increase. |
| E | True (incorrect) | Wrong: the equation describes a relationship under assumptions; it does **not** guarantee management can create the required independent opportunities (or skill, capacity, implementation) at no cost. |

**Reference:** Grinold & Kahn, 2nd ed., ch. 6 (sensitivity of IR to IC vs. breadth; square-root scaling); Balch ML4T 02-09 (signal-strength vs. diversification tradeoffs).

### [QF2-D4G5Q1] Nominal versus effective breadth under factor exposure
**Scenario:** A 300-stock global portfolio draws most active risk from overweighting tech and underweighting financials; positions within each sector move together. The manager labels every holding an independent active decision.
**Answer polarity:** **Inverted (True = the quoted statement is INCORRECT; False = the quoted statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | The quoted statement is correct: 300 holdings do not necessarily represent breadth of 300 — position count is not the count of economically distinct bets. |
| B | False (accurate) | The quoted statement is correct: a dominant sector trade links many positions through one common factor exposure, so many weights express a single view. |
| C | False (accurate) | The quoted statement is correct: correlated active returns reduce the diversification benefit of treating each position as independent — each adds less unique information. |
| D | True (incorrect) | Wrong: holding stocks in different companies does **not** guarantee independent outcomes — separate issuers can share sector, market, macro, or supply-chain exposures. |
| E | False (accurate) | The quoted statement is correct: factor-exposure and correlation analysis help reveal whether nominal breadth overstates effective breadth by exposing shared drivers. |

**Reference:** Grinold & Kahn, 2nd ed., ch. 6 (effective breadth; common factors shrink independent-bet count) and factor-risk discussion (ch. 3); Balch ML4T 02-09 (correlated positions and diversification).

### [QF2-D4G5Q2] Correlated signals from the same input
**Scenario:** A researcher builds ten signals from the same one-month price trend by varying the lookback 19→28 days; correlations exceed 0.95 and usually select the same positions. The claim is 10× breadth because ten formulas vote.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Highly correlated transformations of the same input may be repeated versions of one underlying bet — minor parameter variations preserve nearly the same economic exposure. |
| B | False | Ten signal columns do **not** necessarily create ten independent opportunities; independence must be supported by distinct information and outcome relationships. |
| C | True | Treating all ten as independent would overstate effective breadth — near-duplicate signals do not provide the diversification a raw count of ten assumes. |
| D | True | Combining the signals can still change forecast scaling or robustness (averaging smooths noise) even if it adds little new breadth. |
| E | False | Distinct formula names are **not** sufficient evidence of independent information — labels do not determine statistical or economic dependence. |

**Reference:** Grinold & Kahn, 2nd ed., ch. 6 (independence of signals; effective breadth); Balch ML4T 02-09 (overfitting via many correlated signals; signal redundancy).

### [QF2-D4G5Q3] State-dependent correlation and effective breadth
**Scenario:** A multi-asset fund trades equities, corporate bonds, commodities, and currencies. In normal periods strategies look weakly correlated, but in liquidity crises they all lose. The risk committee asks whether average correlations capture effective breadth.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Trading different asset classes offers *potential* diversification but does not guarantee independence — different labels can hide common sensitivity to liquidity, growth, inflation, or risk appetite. |
| B | True | Correlations that rise in stress make effective breadth **state-dependent** — dependence changes with the market environment. |
| C | True | A breadth estimate based only on calm periods can overstate diversification exactly when it is needed most, missing joint losses that emerge in crises. |
| D | False | A zero *average* historical correlation does **not** imply independence in every regime — positive and negative regime-specific relationships can average to zero, and zero correlation does not establish full independence. |
| E | True | Scenario and conditional-correlation analysis complements a single full-sample estimate by examining dependence an unconditional average can obscure. |

**Reference:** Grinold & Kahn, 2nd ed., ch. 6 (effective breadth under dependence) and risk/covariance treatment (ch. 3); Balch ML4T 02-09 (correlation instability; stress-period behavior).

### [QF2-D4G6Q1] Concentrated skill versus broad systematic breadth
**Scenario:** A concentrated manager researches ten companies with IC = 0.15; a broad systematic strategy has IC = 0.03 across 1,000 effective opportunities. Assume the simplified law applies and breadth figures are comparable.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | IR ≈ 0.15·√10 = 0.15·3.16 ≈ **0.47**. [Source: garbled `(0.15\sqrt{10})`.] |
| B | True | IR ≈ 0.03·√1000 = 0.03·31.62 ≈ **0.95**. |
| C | False | The higher-IC manager does **not** automatically have the higher IR — breadth also drives IR, and here the broad low-IC strategy (0.95) beats the concentrated high-IC one (0.47). |
| D | True | Broad application of weaker skill can outperform concentrated stronger skill on the simplified metric — sufficient independent breadth compensates for lower per-decision IC. |
| E | False | The calculation does **not** establish superiority for every investor/capital level — objectives, costs, capacity, drawdowns, estimation error, and constraints remain unresolved. |

**Reference:** Grinold & Kahn, 2nd ed., ch. 6 (skill-vs-breadth tradeoff worked through IR = IC·√BR); Balch ML4T 02-09 (concentration vs. diversification and risk-adjusted return).

### [QF2-D4G6Q2] Breadth offset by declining skill
**Scenario:** A credit specialist considers expanding from familiar domestic issuers into hundreds of foreign/lower-quality bonds. Coverage rises sharply, but data are poorer and estimated IC falls as the universe expands.
**Answer polarity:** **Inverted (True = the quoted statement is INCORRECT; False = the quoted statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | The quoted statement is correct: added breadth can be offset by reduced forecast skill — the law contains both IC and √BR, so a falling IC can cancel a rising √BR. |
| B | False (accurate) | The quoted statement is correct: if breadth rises 4× while IC halves, IR is unchanged — √4 = 2 and ½·2 = 1 (offsetting effects). |
| C | True (incorrect) | Wrong: any increase in the number of securities does **not** have to improve predicted IR — nominal count may not raise *effective* breadth, and IC can deteriorate. |
| D | False (accurate) | The quoted statement is correct: expansion can introduce operational, liquidity, and model risks the Fundamental Law does not summarize. |
| E | False (accurate) | The quoted statement is correct: the optimal scalable universe may stop before the maximum if marginal opportunities are low-quality or highly dependent (diminishing or negative net value). |

**Reference:** Grinold & Kahn, 2nd ed., ch. 6 (joint role of IC and breadth; limits to the law); Balch ML4T 02-09 (universe expansion, data quality, and capacity).

### [QF2-D4G6Q3] Automation, breadth, and IC transfer
**Scenario:** A firm automates a discretionary signal to screen 20,000 instruments hourly; analysts had used it only in a small liquid-equity universe with manual context. Executives assume automation preserves IC while creating enormous breadth.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Automation can reduce the cost and time to evaluate many candidate opportunities — it supplies operational capacity for broad, frequent evaluation. |
| B | False | The original IC is **not** guaranteed to transfer unchanged to new instruments and higher decision frequency — skill can change when population, horizon, or implementation changes. |
| C | True | New assets may differ in liquidity, market structure, data quality, and signal mechanism, affecting both forecasts and realizable returns. |
| D | True | Hourly rescreening of slowly-changing information creates many *nominal* decisions without comparable *effective* breadth — repeated decisions on near-unchanged information are dependent. |
| E | True | Staged validation across universes and horizons is more informative than mechanically extrapolating the original estimates — out-of-sample testing checks whether skill and independence survive expansion. |

**Reference:** Grinold & Kahn, 2nd ed., ch. 6 (effective breadth; IC stability assumptions); Balch ML4T 02-09 (out-of-sample validation; signal degradation on new data).

### [QF2-D4G7Q1] Predicted versus realized IR — the implementation gap
**Scenario:** A backtest applies IR = IC·√BR with IC = 0.05 and breadth 400, predicting IR = 1.0. Live trading yields only 0.4 after spreads, commissions, market impact, and constraints. The team investigates the gap.
**Answer polarity:** **Inverted (True = the quoted statement is INCORRECT; False = the quoted statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | The quoted statement is correct: the simplified law describes gross forecasting potential and abstracts from several frictions between forecasts and net performance. |
| B | False (accurate) | The quoted statement is correct: trading costs directly consume active return and therefore reduce realized IR. |
| C | False (accurate) | The quoted statement is correct: portfolio constraints (leverage, shorting, concentration, turnover) can prevent forecasts from becoming the positions the simple calculation assumes — this is the transfer-coefficient (TC < 1) drag. |
| D | True (incorrect) | Wrong: the live shortfall does **not** prove the equation was evaluated incorrectly — a correct calculation under unrealistic assumptions can still differ from live results. |
| E | False (accurate) | The quoted statement is correct: comparing predicted and realized performance should include turnover, cost, constraint, and dependence diagnostics to identify which assumptions failed. |

**Reference:** Grinold & Kahn, 2nd ed., ch. 6 (full law with transfer coefficient IR ≈ TC·IC·√BR; gross vs. implementable performance); Balch ML4T 02-09 (transaction costs, slippage, and backtest-vs-live gaps).

### [QF2-D4G7Q2] Time-varying IC and crowding
**Scenario:** A model's full-sample IC is +0.04, but it was +0.10 in the first half and −0.02 in the second; the strategy has grown popular and faces more crowding. Management proposes using the full-sample IC unchanged for future projections.
**Answer polarity:** **Inverted (True = the quoted statement is INCORRECT; False = the quoted statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | The quoted statement is correct: a full-sample average can conceal deterioration or a regime shift, since it blends periods with materially different forecast behavior (+0.10 vs. −0.02). |
| B | True (incorrect) | Wrong: a negative recent IC is **not** irrelevant just because the full-sample IC is positive — recent inverse performance bears directly on whether the model is still useful. |
| C | False (accurate) | The quoted statement is correct: time-varying IC weakens projections that assume stable skill; the law's IC input should not be treated as constant without evidence. |
| D | False (accurate) | The quoted statement is correct: crowding can reduce future returns or raise costs even if the historical relationship was genuine — competitors accelerate price adjustment and consume liquidity. |
| E | False (accurate) | The quoted statement is correct: rolling, regime-specific, and out-of-sample IC estimates provide useful evidence about stability rather than relying on one pooled number. |

**Reference:** Grinold & Kahn, 2nd ed., ch. 6 (IC stability as an assumption; limits of the law) and ch. 5 (information horizon/decay); Balch ML4T 02-09 (regime change, crowding, and signal decay).

### [QF2-D4G7Q3] Raw decision count, correlation, and capacity
**Scenario:** A small-cap strategy reports 500 annual decisions, but positions are correlated, turnover is high, and the fund plans to deploy 10× more capital. The backtest assumes unlimited liquidity and uses the raw decision count as breadth.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Using 500 as breadth can overstate effective breadth when positions are correlated — correlated decisions contribute fewer independent bets than their raw count. |
| B | True | High turnover makes transaction costs material to net active return — frequent trading repeatedly incurs spreads, commissions, slippage, and impact. |
| C | True | Increasing capital raises market impact and reduces capacity-adjusted performance — larger orders consume more liquidity and can move prices adversely. |
| D | False | Unlimited backtest liquidity is **optimistic**, not conservative — it removes a constraint that can materially harm live execution, especially for a large small-cap strategy. |
| E | True | A practical forecast should adjust for dependence, costs, capacity, and possible instability rather than treating the simplified-law estimate as guaranteed. |

**Reference:** Grinold & Kahn, 2nd ed., ch. 6 (effective breadth, capacity, and the gap to realized IR); Balch ML4T 02-09 (market impact, liquidity, turnover, and capacity constraints).

## References (domain-level)

1. **Grinold & Kahn — *Active Portfolio Management: A Quantitative Approach for Providing Superior Returns and Controlling Risk*, 2nd ed.:** ch. 6 (**The Fundamental Law of Active Management** — the central text for this domain: IR = IC·√BR, information coefficient, breadth as the count of independent bets, the independence-of-bets assumption, skill-vs-breadth tradeoff, the transfer-coefficient generalization IR ≈ TC·IC·√BR, and the law's limitations); ch. 5 (**The Information Ratio** — definition as active return over active risk, IR vs. Sharpe ratio, benchmark dependence, VA ≈ IR²/(4λ), estimation uncertainty and horizon); ch. 3 (risk/covariance and common-factor exposure, used to characterize effective breadth under dependence). Cited at chapter level only — no specific page numbers are asserted.
2. **Balch — ML4T (Georgia Tech), lecture 02-09:** information coefficient and signal evaluation, information/Sharpe ratios, correlated and redundant signals, overfitting and in-sample-vs-out-of-sample performance, turnover/transaction costs, market impact, liquidity, and capacity constraints — the applied counterpart to the Fundamental Law. Cited at lecture/section level only.
3. **Source-slice fidelity note:** All A–E verdicts are transcribed **verbatim** from the authoritative slice `slices/QF2_D04.txt` and are never flipped. For the 10 inverted-polarity questions the slice's "True"/"False" answer-key values are preserved and surfaced as "True (incorrect)" / "False (accurate)" to make the polarity explicit. Garbled artifacts in the source (raw-LaTeX math such as `(IR=IC\sqrt{BR})` and `(0.05\sqrt{100}=0.50)`, and broken `fi`/`fl` ligatures) are flagged inline and in the cheat-sheet; they do not alter any verdict.
