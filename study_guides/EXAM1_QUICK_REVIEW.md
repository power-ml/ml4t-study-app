# ML4T Exam 1 — One-Page Quick Review (print me)

_Exam 2026-10-12 · 40 Q (2 per domain × 20 domains) · each Q = 5 choices scored T/F independently._
_Grounded in `study_notes/` (verified A–E verdicts) + `references/INDEX.md`. QF note: the main QF reading "What Hedge Funds Really Do" is **not distilled**; QF concepts below come from the study-notes' CFA / Investopedia / Grinold-Kahn / BKM / Harris citations — treat any WHFRD-specific point as **(verify — WHFRD not distilled)**._

## Exam mechanics & universal traps
- **Per-choice scoring:** each of the 5 choices is marked True or False independently; 1 pt per correct T/F. **Answer every sub-choice** (blanks = 0). **NEVER mark all 5 the same** — every question has ≥1 True and ≥1 False, so all-True/all-False is always wrong and may zero the question.
- **READ THE POLARITY LINE FIRST.** Two modes: **Normal** → "True = the statement is accurate." **Inverted** → "True = incorrect; False = accurate" → you are flagging the WRONG statements, so **mark True if the statement is WRONG**.
- **All 95 inverted-logic questions are in ML; QF has ZERO inverted.** Inverted ML counts: D1=11, D2=12, D3=12, D4=8, D5=8, D6=12, D7=8, D8=7, D9=6, D10=11.
- **Choice-level negation / embedded claim (heavy in QF):** "It is incorrect to conclude that X" / "A reviewer would be wrong to accept X" / "...is not <correct value>". Parse the inner claim, judge its truth, then negate (then re-negate for inverted polarity). If inner claim is accurate, the negated choice is **False** ("reverses the correct conclusion").
- **Data-mined heuristics:** absolute words (always / guarantees / proves / riskless / cannot / eliminates / must) ≈ usually **False**; a negation ≈ often inaccurate; slight A-slot skew. Use only to break ties — compute/reason first.

---
## ML D1 — Learning Paradigms & Problem Framing (ISLP Ch.1, §2.2; Bishop DL Ch.1; Murphy PML Ch.1)
- Supervised vs. unsupervised is set by **presence of paired targets (labels)**, not by inputs/output format. Post-hoc cluster naming ≠ supervision.
- Regression (continuous target, est. E[Y|X], MSE/MAE) vs. classification (discrete, est. P(Y=j|X), error rate). A probability output is still classification; binning loses magnitude info.
- Training vs. inference costs are **decoupled** (fit-once/apply-many). Eager (linear, trees) = cheap inference; lazy (KNN) = ~0 train, O(N) inference.
- Expected test error = **bias2 + variance + irreducible ε**; U-shaped vs. complexity. More data fixes variance, not bias. Good model = accuracy + robustness + stability, judged vs. the decision.
- **Sample [D1G1Q1, Normal]** "Predict next-day returns from labeled history vs. cluster regimes without returns." → **A True** (labeled next-day return = supervised X→Y); **B False** (clustering w/o labels = unsupervised); **C True** (no targets = unsupervised def.); **D False** (buy/sell output doesn't imply supervised); **E True** (example-target pairs define supervised).

## ML D2 — Data & Sampling Discipline (ISLP §2.2; DL §2.1–2.2)
- Missingness: MCAR (drop OK) / MAR (depends on observed) / MNAR (depends on the missing value itself — informative, often a feature). Imputation is an estimate, not a measurement.
- **Size never cures systematic bias; more features never fix biased rows.** Survivorship (current-constituents) & selection/publication bias skew everything.
- Time is first-class: **chronological / walk-forward splits**, never random shuffle. Look-ahead bias = using info not available at decision time (align by **publication date**, not period covered).
- Leakage hides in preprocessing/imputation/feature-selection fit on pooled or full data, and in repeated holdout reuse — "no test labels used" ≠ clean.
- **Sample [D2G3Q1, Normal]** survivorship: backtest on firms still in the S&P 500 at study end. → **A True** (conditioning on survival = survivorship bias); **B True** (dropping failures inflates performance); **C False** (large count of current members can't fix a biased rule); **D True** (point-in-time constituents avoid it); **E False** (biases learned relationships, not just descriptive stats).

## ML D3 — Feature Engineering & Leakage (ISLP §3.3, §6; Handbook Ch.2)
- Scaling is **learner-dependent**: distance/gradient learners (KNN/NN/SVM) need it; **trees are invariant to monotonic transforms**. Fit scaler on train only.
- Interactions need an explicit term (additive β1x1+β2x2 can't encode conditional/multiplicative effects); added flexibility never *guarantees* OOS gain.
- **A chronological split does NOT fix a forward-looking feature** (centered MA/z-score, same-bar auction). Target leakage = timing/lineage (post-outcome codes), not column name.
- Collinearity: OLS coeffs unstable; tree importances diluted. PCA is unsupervised (can drop low-variance predictive dirs). Non-stationary scaling traps: rolling-z denominator inflation masks shocks.
- **Sample [D3G5Q1, Normal]** post-resolution account-status code → near-perfect accuracy. → **A True** (encodes outcome = target leakage); **B False** (high accuracy says nothing about availability); **C True** (reconstruct point-in-time); **D True** (removing it lowers but makes credible); **E False** (outcome-caused association is why it misleads).

## ML D4 — Linear Models & Regression (ISLP §3.1–3.3)
- Linear = **linear in coefficients**, not necessarily in features (polynomials/interactions still linear). Coeff = conditional effect holding others fixed; **magnitude≠importance unless standardized**; sign≠causation.
- OLS needs no feature independence; uniqueness fails only under **exact** collinearity. Multicollinearity inflates coeff variance only — doesn't bias, doesn't kill R2/F, isn't serial correlation.
- Residuals sum to 0 w/ intercept (near-zero mean proves nothing); patterns → misspecification (curve=nonlinearity, fan=heteroscedasticity, runs=serial corr). MSE punishes outliers more than MAE. R2=0 ≠ residuals zero.
- Ridge (L2) shrinks all, keeps all; Lasso (L1) zeros some. Pick λ by validation, never training error. Gauss-Markov/BLUE needs no normality.
- **Sample [D4G1Q6, Normal]** ŷ = 0.02 + 0.045X1 − 0.012X2 − 0.038X3 (standardized). → **A True** (at means ŷ=intercept=0.02); **B False** (−0.012 is conditional, not causal); **C True** (standardized → |0.045|>|0.038|>|0.012| ranks per-SD effects); **D True** (no interaction → marginal effect of X1 constant); **E False** (only *exact* dependence breaks uniqueness).

## ML D5 — Instance-Based Learning / KNN (ISLP §2.2.3, §3.5; Bishop DL Ch.1)
- Predict from k nearest neighbors; non-parametric, local. Euclidean/Manhattan use raw magnitudes → **large-scale feature dominates**; scale (fit on train). Changing metric ≠ scaling fix.
- Small k = low bias/high variance (jagged, ~0 train err); large k = high bias/low variance; **k=N → global mean/majority**. DoF≈N/k. Pick k by CV; test error U-shaped.
- Outlier influence is **strictly local** (unlike OLS leverage). Curse of dimensionality: sparsity + distance concentration; scaling doesn't cure it.
- Lazy: ~O(1) train, **O(N·p) inference + O(N·p) memory**; trees degrade to O(N) at p≳20–30. Wrong for HFT; use ANN (HNSW/LSH). Large neighbor distance = out-of-distribution signal.
- **Sample [D5G2Q4, Normal]** k=1...250 on 1000 obs. → **A True** (k=1 Voronoi, 100% train acc, high variance); **B False** (k=1 *maximizes* variance); **C True** (k→N smooths, lower var/higher bias); **D True** (k=N predicts global majority, max bias); **E False** (bigger k *reduces* effective DoF≈N/k).

## ML D6 — Decision Trees (ISLP §8.1; ESL §9.2)
- One obs → **one root-to-leaf path → one leaf** (averaging all leaves = ensembles, not a tree). Regression leaf = mean of training targets.
- CART = **greedy, top-down, binary** (local best split, no lookahead; locally≠globally optimal). Gini/entropy = 0 at pure, max at p=0.5; classification error used for pruning.
- Capacity = depth/#leaves; unrestricted → 0 train err + high variance. `min_samples_leaf` bounds leaf size; `min_samples_split` does NOT guarantee leaf size.
- **No scaling needed** (monotonic-invariant). Weaknesses: axis-aligned only (diagonal → staircase), **cannot extrapolate**, piecewise-constant jumps, high variance/instability → motivates bagging/RF.
- **Sample [D6G1Q2, Normal]** regression leaf holds 1%,2%,−1%,2%. → **A True** (mean=1%); **B True** (every obs reaching leaf gets that prediction); **C False** (tree routes by rules, not KNN distances); **D True** (internal nodes split on features); **E False** (a leaf may hold one OR many obs).

## ML D7 — Ensemble Methods (ISLP §8.2; ESL ch.10, §15)
- Averaging/voting helps only with **imperfectly correlated errors**; shared systematic bias survives; no per-observation guarantee.
- Bagging: bootstrap (N draws w/ replacement, ~63% unique, ~37% OOB validation). **Bag deep/high-variance trees** (not shallow). RF adds per-split feature randomness to decorrelate.
- Boosting: **sequential**, each learner fits residuals/hard cases; additive w/ learning rate; **reduces bias**. Bagging reduces variance (parallel).
- Failure modes: correlated learners fail together (count≠diversity); leakage can't be averaged away; boosting overfits (early-stop); averaging low estimates stays low.
- **Sample [D7G2Q1, Normal]** 100 trees, bootstrap of 10,000 days. → **A True** (with-replacement → repeats possible); **B False** (needn't contain all distinct rows, ~37% omitted); **C True** (different samples → different fitted trees); **D True** (averaging reduces variance of unstable base); **E False** (bagging never permutes targets).

## ML D8 — Model Evaluation & Metrics (ISLP §2.2, §5.1; ESL ch.7)
- Three splits: **train** (fit) / **validation** (select) / **test** (single final). Refit on train+val OK if test untouched. Reusing test (even via human decisions) = leakage; "best of many" is optimistic.
- **RMSE ≥ MAE always**; RMSE in target units (MSE squared units); RMSE *more* outlier-sensitive. Wider RMSE–MAE gap = more error dispersion.
- Baselines: regression=train-mean, classification=majority class, trading=buy-and-hold/cash — same period, never from test. A metric alone is meaningless.
- Score all models on **same held-out rows + same metric/units**; fit scaling on train only. Low RMSE ≠ profit (costs/turnover). Report central tendency AND dispersion.
- **Sample [D8G2Q3, Normal]** MAE=$400, MSE=490,000, RMSE=$700. → **A True** (MAE=avg absolute $error); **B False** (MSE is dollars2, not comparable to target); **C True** (RMSE restores $ units); **D True** ($700>$400 reflects error dispersion); **E False** (MAE vs RMSE choice is about cost of large misses, not purely math).

## ML D9 — Overfitting, Underfitting & Generalization (ISLP §2.2, §6.2, ch.8; ESL ch.7)
- Read the **pair**: overfit = low train + high test (high variance); underfit = high+similar (high bias). Small gap alone ≠ good (two poor scores = consistently weak).
- Complexity lowers bias, raises variance (not both). More *representative* data fixes variance, never bias; duplicates add nothing; wrong-regime data doesn't generalize.
- k-fold: separate fit per fold; selecting best-of-many → optimistic (need untouched test). Fit preprocessing inside each fold; **time-series needs forward/rolling splits**.
- "Too good to be true" → suspect **leakage** (next-day close feature, full-dataset normalization) before "inefficiency." Controls: depth↓/leaf↑, larger k, regularization, early stopping — tune on validation.
- **Sample [D9G1Q1, Normal]** near-zero train error, poor on new data. → **A True** (textbook overfitting); **B True** (sample sensitivity = high variance); **C True** (more representative data shrinks gap); **D True** (reduce capacity attacks overfitting); **E False** (not underfitting — train error is near zero).

## ML D10 — Model Selection & Practical Tradeoffs (ISLP §2.1.3, §2.2.3, ch.8)
- **No free lunch** — match model to problem structure (linear≈proportional; trees for thresholds/interactions). Flexibility ≠ better generalization.
- Accuracy vs. interpretability can be a **binding governance constraint**; interpretable ≠ leakage-free. Train vs. inference cost decoupled — judge each against its workflow.
- OLS outlier-sensitive; KNN scale-sensitive & slow at inference; deep trees unstable (bagging reduces variance, not systematic error). More data ≠ fixes complexity; obsolete-regime rows overstate usable info.
- Latency is strategy-specific (measure end-to-end at peak/tail load). Robustness: segment by regime; retraining more often ≠ more stable.
- **Sample [D10G3Q1, Normal]** real-time system, speed vs. complex ensemble. → **A True** (inference time is the operative constraint); **B True** (KNN defers heavy search to inference); **C True** (linear = fast dot-product inference); **D False** (more complex ≠ always better); **E True** (choice depends on system constraints).

---
## QF D1 — Investment Returns & Compounding (DL §2.2 for expectation/variance; CFA/BKM/Investopedia)
- Returns **compound multiplicatively** `Π(1+ri)−1`, not sum. CAGR=(V_end/V_begin)^(1/n)−1 (not total/n). Rule of 72 ≈ doubling time.
- Arithmetic mean = best single-period estimate; **geometric ≤ arithmetic** (volatility drag); equal only if returns identical.
- Returns compound (^periods); **volatility scales with √time**. Portfolio return = Σ wiri (return ≠ contribution=weight×return). Leverage subtracts financing.
- Recovery asymmetry: −x% needs >x% gain. Sequence matters only with cash flows. **This slice has NO inverted Q**; watch "...is not X" double-negatives.
- **Sample [D1G2Q1, Normal]** $100M→$121M over 2 yrs. → **A True** (total return 21%); **B False** (CAGR *is* 10%: √1.21−1); **C False** (10.5% simple avg ignores compounding); **D True** ((1.10)2−1=21%); **E True** (CAGR = constant rate linking endpoints).

## QF D2 — Risk & Risk-Adjusted Performance (Grinold-Kahn for IR; CFA/Investopedia)
- Variance/σ = dispersion (equal mean ≠ equal risk; σ ≠ a guaranteed loss). Drawdown is path-dependent, from the running peak; recovery asymmetric.
- **Sharpe=(r−r_f)/σ** (subtract r_f; higher raw return can have lower Sharpe). Annualize ×√T, not ×T; breaks under autocorrelation/non-normality.
- **Sortino** uses downside deviation only (needs a MAR; unstable with few down months). **IR = active return / tracking error** (vs. benchmark, distinct from Sharpe).
- Metrics are sample-period sensitive and gameable; a high ratio ≠ tail safety. **NO inverted Q in this domain.**
- **Sample [D2G3Q1, Normal]** A: 12%/20%σ; B: 9%/8%σ; r_f=2%. → **A True** (A excess 10% > B's 7%); **B True** (A Sharpe .50, B .875 — B higher); **C False** (raw return ignores risk); **D False** (r_f must be subtracted); **E True** (higher Sharpe = more excess per unit σ).

## QF D3 — Diversification & Correlation (Markowitz; BKM; Investopedia)
- ρ∈[−1,1], unitless **tendency** (not offset %, not causation, not period-by-period). Cov=ρ·σ_Aσ_B (doubling both σ → ×4 cov).
- σ_p2 = w_A2σ_A2+w_B2σ_B2+2w_Aw_B·Cov — the cross term is where diversification lives (NOT weighted avg of vols). Expected return is weight-avg, correlation-independent.
- **Specific/idiosyncratic risk diversifiable; systematic is not.** Diminishing marginal benefit → floor at systematic risk. Count/equal-weights ≠ diversified (sector/factor concentration).
- Correlations **rise toward 1 in stress**; leverage magnifies the damage. **NO inverted Q.**
- **Sample [D3G4Q1, Normal]** two assets 8%ret/12%vol, ρ=0. → **A True** (E[r]=8%); **B True** (ρ=0 → cov term zero); **C False** (vol ≈8.49% *is* <12%, so "not ~8.49%" reverses it); **D False** (ρ=0 doesn't bar joint losses); **E True** (return held at 8% while vol falls — risk cut without return cut).

## QF D4 — Portfolio Optimization (Markowitz; Grinold-Kahn; CFA)
- Σwi=1 budget alone doesn't bar negatives/>100%. Net=Σwi, **gross=Σ|wi|** (100% net can be heavily levered). Bounds reshape the feasible set.
- **GMV** = lowest-variance portfolio (needs covariance matrix, not just vol ranking; diversification can beat any single asset). Max-Sharpe = **tangency** (CAL tangent from r_f); tangency ≠ GMV.
- Changing r_f can flip the Sharpe ranking. Efficient frontier = min risk per return (upper branch above GMV); below-GMV is dominated.
- **Error maximization**: MV hypersensitive to expected returns; extreme weights = noise. Fixes: shrinkage, bounds. Constraints can't raise the modeled optimum; ex-post weights = look-ahead. **NO inverted Q.**
- **Sample [D4G3Q1, Normal]** A: 10%/16%vol; B: 8%/8%vol; r_f=2%. → **A True** (A excess 8%); **B False** (A Sharpe *is* 0.50); **C True** (B Sharpe 0.75); **D False** (A's higher raw return ≠ max-Sharpe); **E True** (B 0.75 > A 0.50).

## QF D5 — Market Microstructure & Trade Execution (Harris; CFA; Investopedia)
- Spread=ask−bid (cost of immediacy); market buy lifts ask, sell hits bid; relative spread > dollar spread for liquidity. Market order=exec certainty/price risk; limit=price control/fill risk.
- Order book depth: best price ≠ total liquidity; large orders **walk the book** (VWAP > quoted). Imbalance = probabilistic, spoofable.
- Slippage=exec−decision price; impact splits **temporary (reverts)** vs. permanent. Liquidity risk scales with size/volume, not dollars (capacity).
- Short: sell-to-open/buy-to-close, profits on fall, **loss unbounded**, borrow fee + owed dividends, squeeze/recall risk. Implementation shortfall + full costs; splitting trades = impact vs. timing risk. **NO inverted Q.**
- **Sample [D5G1Q1, Normal]** bid $49.90 / ask $50.10. → **A True** (spread $0.20); **B False** (midpoint *is* $50.00); **C False** (market buy *does* hit the ask); **D False** (round trip *loses* the $0.20 spread); **E True** (spread = cost of immediacy).

## QF D6 — Valuation & Mispricing (Damodaran; Graham; CFA; Investopedia)
- Market price = observed; intrinsic value = model estimate (reasonable analysts differ; same price over/under under different models). A price-value gap doesn't *guarantee* profit.
- P/B: market can rationally exceed book (intangibles/earning power); high P/B ≠ overvalued. In distress, book overstates recovery (equity is residual).
- TVM: PV=FV/(1+r)n; higher r / longer horizon → lower PV. **Gordon DDM V=D1/(r−g)**, needs g<r; as g→r value explodes. Terminal value often dominates DCF.
- Compound growth > rate×years. Growth/value are labels not guarantees (value trap). Margin of safety cushions but can't guarantee; correct thesis ≠ winning trade (timing/borrow/forced cover). **NO inverted Q.**
- **Sample [D6G4Q2, Normal]** D1=$3.00, g=4%, r=9%. → **A True** (V=3/0.05=$60); **B True** (r=10% → V=3/0.06=$50); **C False** (g=5% *raises* V to $75, not lowers); **D True** (needs g<r for finite value); **E False** ($60 depends on uncertain inputs, not "certain").

## QF D7 — CAPM, Alpha, Beta & Hedging (Sharpe CAPM; BKM; Grinold-Kahn)
- r = α + β·r_mkt + ε (components sum). **β = Cov/Var = ρ·σ_asset/σ_mkt** (sensitivity, not skill; estimate of an average). Zero cov → β=0.
- Correlation ≠ beta: high ρ can pair with low β; high total vol can pair with low β (idiosyncratic). Jensen's α = actual − [r_f+β(r_mkt−r_f)]; one year ≠ skill; statistical ≠ economic (net of cost) significance.
- Portfolio β = weighted avg (longs add, shorts subtract, cash 0). **Dollar-neutral ≠ beta-neutral** (unequal dollars needed; hedge ratio=β_long/β_hedge).
- Index hedge removes systematic, **retains idiosyncratic + alpha**; imperfect (basis/estimation error). **NO inverted Q.**
- **Sample [D7G3Q1, Normal]** fund 14%, mkt 10%, r_f 2%, β 1.2. → **A False** (mkt excess *is* 8%); **B True** (CAPM=2%+1.2×8%=11.6%); **C True** (α=14%−11.6%=2.4%); **D False** (14 vs 10 not risk-adjusted at β 1.2); **E False** (one year ≠ persistent skill).

## QF D8 — Market Efficiency & Arbitrage (Fama; Shleifer & Vishny; CFA)
- EMH nested: **weak** (past price/volume) ⊂ **semi-strong** (public info) ⊂ **strong** (incl. private). Efficiency ≠ perfection (price discovery, runs are compatible).
- Inefficiency test = **does a reliable, tradeable edge survive beyond chance + costs?** In-sample profit = possible data snooping; gross edge < costs = not exploitable.
- Arbitrage/LOOP: identical cash flows → same price; profit from contemporaneous gap, not forecast. Riskless (identical) vs. risky (only correlated). ETF create/redeem → price≈NAV.
- Stat-arb/pairs: z=(spread−mean)/std, large |z| ≠ guaranteed convergence; dollar-neutral ≠ risk-free. **Limits to arbitrage:** horizon, funding/margin (forced liquidation), noise-trader, short-sale constraints, crowding. **NO inverted Q.**
- **Sample [D8G4Q1, Normal]** same stock $50.00 (A) vs $50.40 (B), $0.10 cost, simultaneous. → **A True** (gross spread $0.40); **B False** (net *is* $0.30); **C False** (profit from the discrepancy, not a forecast); **D False** (simultaneous exec *does* reduce leg risk); **E True** (repeated arb → convergence).

## QF D9 — Financial Data & Research Bias (Lopez de Prado; CFA; Investopedia)
- Look-ahead: use only info available at decision time. Random splits break chronology (over-optimistic); centered windows leak the future (use trailing/lagged). Overlapping forward labels leak → **purge** boundary obs.
- **Survivorship** (only survivors → overstates return/understates risk; fix with PIT + dead-fund DB). **Selection** (choosing market/period after seeing results). **Data snooping** (~5% of 1000 nulls look significant; corrections + untouched validation).
- Reusing a holdout = p-hacking (functional use, not the label "test," defines independence); **winner's curse**. PIT data: restatements/revisions; reference period ≠ availability date.
- Corporate actions: split → unadjusted shows spurious −50% (value ~unchanged); dividend → price-only understates total return; delisting → ending at last quote hides real loss. Forward-fill fakes zero returns; informative missingness → add indicator. Nonstationarity: stale beta, regime loss hidden in full-sample avg. **NO inverted Q.**
- **Sample [D9G5Q1, Normal]** $100 stock, 2-for-1 split, opens ~$50; unadjusted → −50%. → **A True** (two $50 shares replace one $100 — not a 50% loss); **B True** (ignoring share count = false signal); **C False** (adjusted series *should* remove the discontinuity); **D False** (position value *is* ~unchanged); **E False** (market cap ~unchanged, not doubled).

## QF D10 — Quantitative Strategy Design & Evaluation (Lopez de Prado; Grinold-Kahn; CFA)
- Need an **economic hypothesis + mechanism**, not just correlation; arbitrary partition searches guarantee a spurious winner. Don't pick the lookback that maximized full-sample performance.
- Forecast ≠ trade: trade only if net edge clears cost (no-trade threshold). **Directional accuracy ≠ P&L** (60% hit rate can lose if wrong on big moves). Dollar-neutral ≠ risk-neutral; volatility-scale positions.
- Benchmark = relevant opportunity cost (investable index, not just cash). In-sample = any data used to specify/tune; OOS = frozen design on untouched later data; walk-forward. Attribution separates tilt from timing.
- Deploy on **net** (turnover×AUM×cost rate, costs not constant). Capacity: impact rises with size, net edge falls; crowding worsens exit liquidity. Leverage magnifies both ways; stops don't guarantee fill price. Regime shift → maybe retire, not just retrain. **NO inverted Q.**
- **Sample [D10G4Q2, Normal]** $10M, 40% daily turnover, 0.10% one-way cost, $3,000 gross/day. → **A True** (40%×$10M=$4M traded/day); **B True** (0.10%×$4M=$4,000 cost); **C False** ($3,000−$4,000 = $1,000 net *loss*); **D True** (turnover-aware rule cuts drag); **E False** (0.10% rate not constant — varies with size/liquidity).
