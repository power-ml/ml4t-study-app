# QF Domain 9 — Options & Derivative Payoffs

## Domain cheat-sheet

- **The two building blocks (call / put) and the right-vs-obligation asymmetry.** An option is a *contract*, not a share:
  - A **call** gives its **holder the right, but not the obligation, to buy** the underlying at the strike price *K* on/by expiration. The **writer (short)** has the *obligation* to sell at *K* if assigned. A **put** gives its holder the right to **sell** at *K*; the writer must *buy* at *K* if assigned.
  - The holder *chooses* whether to exercise and will do so only when it is economically favorable; the writer has no choice once assigned. This is the source of every asymmetry in the domain.
  - Standard listed contracts cover **100 shares**, so a per-share payoff of $X translates to $X × 100 per contract.
- **Expiration payoff formulas (memorize; everything else derives from these).**
  - Long call payoff = **max(S_T − K, 0)**; short call payoff = **−max(S_T − K, 0)**.
  - Long put payoff = **max(K − S_T, 0)**; short put payoff = **−max(K − S_T, 0)**.
  - Payoffs are **floored at zero for the long** — an option payoff is *never negative* for the holder (the worst case is "don't exercise," payoff 0). A long and the matching short are mirror images: their expiration payoffs sum to zero *before* premium.
- **Premium, payoff, profit, breakeven (payoff ≠ profit).**
  - **Profit** = payoff − premium (long) or premium − payoff (short). The payoff can be positive while the *profit* is still negative if the payoff is smaller than the premium paid.
  - **Call breakeven = K + premium**; **put breakeven = K − premium** (ignoring interest/commissions). A long option's **maximum loss = the premium**; a *long call's* maximum profit is unbounded; a *long put's* maximum profit = K − premium (floored by S_T = 0).
  - Short premium-sellers: **max profit = premium received**; an **uncovered short call has unbounded loss** (stock has no ceiling); an **uncovered short put's loss is bounded** (worst case S_T = 0, loss = K − premium) because the stock cannot fall below zero.
  - For a single contract with no costs, the buyer's and writer's profits are a **zero-sum** pair (one side's gain is the other's loss).
- **Moneyness and intrinsic vs. time value.**
  - **Call:** ITM when S > K, ATM when S = K, OTM when S < K. **Put:** ITM when S < K, ATM when S = K, OTM when S > K.
  - **Intrinsic value** = max(S − K, 0) for a call, max(K − S, 0) for a put — **floored at zero, never negative**. Raising a put's strike (stock fixed) *raises* its intrinsic value; raising a call's strike *lowers* it.
  - **Time value** = option market price − intrinsic value. An option can trade for a positive price while intrinsic value is zero (an OTM option before expiry) — the price reflects the *chance* of finishing ITM, so a positive price with zero intrinsic value is **not** a pricing error. At expiration there is no time value left: value = the terminal payoff only.
- **Volatility, time decay, and Black–Scholes intuition.**
  - Option value is a function of **S, K, time to expiry T, volatility σ, and the risk-free rate r** — not just today's price and strike. Higher **σ** raises both call and put value because the long payoff benefits from large favorable moves while being floored at zero on the unfavorable side (**asymmetric payoff**); a higher option value signals *uncertainty/optionality*, not knowledge of the terminal direction.
  - **Time decay (theta):** holding all else fixed, a (non-deep-ITM) option generally loses time value as expiry approaches — less time means less chance of a favorable move. Time decay does **not** make intrinsic value negative, and in real markets changes in S and σ can offset or overwhelm the decay, so observed prices need not fall every calendar day.
- **The Greeks (sensitivities of option value).**
  - **Delta (∂V/∂S):** change in option value per $1 move in the underlying. Call delta ∈ [0, 1], put delta ∈ [−1, 0]; delta is the hedge ratio and the local "share-equivalent" exposure.
  - **Gamma (∂²V/∂S², = ∂Delta/∂S):** curvature — how fast delta changes; largest for ATM options near expiry. Gamma is what makes an option's exposure **state-dependent / nonlinear** (the payoff "kinks" at K).
  - **Theta (∂V/∂t):** time decay, typically negative for long positions.
  - **Vega (∂V/∂σ):** sensitivity to volatility, positive for long options.
- **Put–call parity (European options, same K and T, no dividends).**
  - **C + K·e^(−rT) = P + S₀**, equivalently **C − P = S₀ − K·e^(−rT)**. A long call plus cash equal to the discounted strike replicates a long put plus the stock; this ties call, put, stock, and a bond together and is the no-arbitrage backbone for every payoff-decomposition argument in this domain. (With discrete dividends *D*, use S₀ − PV(D) in place of S₀.)
- **Hedging and the core strategies.**
  - **Protective put** = long stock + long put: establishes a **floor** at K (before the premium cost); keeps upside less the premium; it does *not* make the position risk-free — you can still lose (purchase price − K) + premium.
  - **Covered call** = long stock + short call: collects a premium that **cushions** small declines but **caps** upside at K (you forgo gains above K). It is "covered" because the owned shares back the delivery obligation.
  - **Strike selection is a tradeoff:** a higher-strike protective put costs more but protects after a smaller decline (higher floor); a lower-strike put is cheaper but only protects against more severe declines. Hedges carry residual risks (basis risk, timing, premium drag when the hedge expires unused).
  - **Straddle** = long call + long put at the same K and T: profits from a **large move in either direction** (V-shaped payoff), breakeven at K ± total premium; max loss = total premium if the stock finishes at K.

## Common traps

- **Inverted-polarity questions (10 of 21 here).** When the body says "each item asserts that its quoted statement is **incorrect** — evaluate the complete A–E items as written," the Answer Key verdict is flipped relative to the plain truth of the quoted statement: **True = the quoted statement is wrong; False = the quoted statement is accurate.** Read the polarity line *first*. Inverted here: **G1Q3, G2Q2, G2Q3, G3Q1, G3Q2, G4Q2, G5Q2, G6Q2, G6Q3, G7Q3.** The remaining 11 are Normal (True = accurate).
- **Payoff vs. profit.** A positive expiration payoff does **not** mean a positive net profit — if the payoff is smaller than the premium paid, the long position still loses money (e.g., a $3 call payoff against a $6 premium is a $3 loss). At the strike itself the payoff is exactly zero, so the premium is *not* recovered.
- **Right vs. obligation.** The holder is **never obligated** to exercise; "the call was purchased, so it must be exercised" is wrong. A rational holder exercises a call only when S > K and a put only when S < K, and otherwise lets it expire.
- **Payoff floored at zero.** A long option's payoff cannot be negative. An OTM call finishing $7 below the strike has a **$0 payoff, not a −$7 payoff** — the $7 "shortfall" is not a payoff to the holder. Intrinsic value is likewise never negative.
- **Uncovered short call loss is unbounded; uncovered short put loss is bounded.** The stock has no price ceiling, so an uncovered written call's loss is **not capped at the strike**. A written put's worst case is S_T = 0, so its loss *is* bounded (K − premium).
- **Owning the stock is not required to buy a put / a put is only a hedge.** A trader may buy a put purely to **speculate** on a decline without owning the underlying; a put can also hedge an owned position. Both uses are legitimate.
- **"Positive price with zero intrinsic value = mispricing."** False — an OTM option legitimately has **time value**; a positive price reflects the probability of finishing ITM.
- **"Higher option value means the market knows the stock will rise/finish ITM."** False — higher value reflects **volatility and asymmetric payoff potential**, i.e., uncertainty, not a directional forecast.
- **Time decay misconceptions.** Time decay does **not** turn intrinsic value negative, and it does **not** guarantee the observed price falls every day — real moves in S and σ can dominate. Only the *time-value* component erodes toward expiry, all else equal.
- **Covered call "keeps unlimited upside."** False — writing the call **gives away gains above the strike** (apart from the premium). The premium is only a limited cushion against declines, not full downside protection.
- **A hedge eliminates all risk.** False — a protective put still leaves (cost − strike) + premium at risk and does not remove basis risk, timing mismatch, or premium drag.
- **Options are "just leveraged stock."** False — the payoff **kinks at the strike** (nonlinear/state-dependent exposure via gamma); a call's downside is bounded to the premium while stock's is linear, so a call is not a constant multiple of the stock.
- **Straddle payoff is linear.** False — long call + long put is **V-shaped**: negative slope below K, positive slope above K; it needs a move larger than the total premium (in either direction) to profit.
- **Garbled symbols flagged.** The source slice contains PDF/OCR **ligature artifacts**: `ﬁ`→"fi" and `ﬂ`→"fl" (e.g., "proﬁt"→profit, "ﬂoored"→floored, "ﬁnishes"→finishes, "speciﬁcally"→specifically, "beneﬁts"→benefits). These are rendering artifacts only; they do not affect any verdict, number, or formula and are written normally below. Repeated page-footer tokens like "Rev:081020261230" are also source artifacts, not content.

## Questions

### [QF2-D9G1Q1] Long call payoff on an in-the-money European call
**Scenario:** An investor buys one European call with a $50 strike; at expiration the stock closes at $62. Evaluate the option's expiration payoff *before* subtracting the premium.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | A call grants its holder the right, not the obligation, to buy the underlying at the strike ($50). This is the defining feature of a call. |
| B | True | The long call's expiration payoff is max($62 − $50, 0) = **$12** per share — the amount by which the stock exceeds the strike. |
| C | True | At 100 shares per contract, $12 × 100 = **$1,200** total payoff. |
| D | False | Exercising lets the holder buy for $50 an asset worth $62, a $12 gain — a rational holder **exercises** an ITM call rather than abandoning it. |
| E | True | The short call's expiration payoff is the mirror image of the long call's, so the writer owes **$12 per share** to the holder (before premium). |

**Reference:** Hull, *Options, Futures, and Other Derivatives* — "Mechanics of Options Markets" / "Properties of Stock Options" (call payoff, right vs. obligation, long–short mirror); *Options & Futures: A Tutorial* (ML4T week-15 reading), payoff diagrams section; Balch ML4T Options lecture (call payoff at expiration).

### [QF2-D9G1Q2] Out-of-the-money call expires worthless — payoff floored at zero
**Scenario:** A trader buys a $75-strike call; at expiration the stock closes at $68. Ignore the premium except where profit is discussed.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Payoff = max($68 − $75, 0) = **$0** — the call is OTM, so its expiration payoff is zero. |
| B | True | Exercising would mean paying $75 for stock worth only $68; buying in the market at $68 is strictly better, so exercise is economically inferior. |
| C | False | A call is a **right, not an obligation** — a prior purchase does not force exercise; the holder lets a worthless call lapse. |
| D | False | The long payoff is **floored at zero**; the $7 gap is not a negative payoff to the holder. The option simply expires worthless. |
| E | True | A worthless option still cost its premium, so the holder's net result can be a loss (the premium) even though the *payoff* cannot be negative. |

**Reference:** Hull, "Properties of Stock Options" (OTM payoff, payoff floored at zero, exercise decision); *Options & Futures: A Tutorial* (ML4T week-15), long-call profit vs. payoff; Balch ML4T Options lecture (payoff vs. profit).

### [QF2-D9G1Q3] Uncovered short call — unbounded loss above the strike
**Scenario:** A dealer writes an *uncovered* European call with a $40 strike; consider expiration payoffs before premium across stock prices of $30, $40, $55, and increasingly large values. Each item asserts its quoted statement is incorrect.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | The quoted statement is correct: at $30 and $40 the call is OTM/ATM (S ≤ K), so the short call's payoff obligation is zero. Marking it "incorrect" is False. |
| B | False (accurate) | Correct: at $55 the holder's payoff is $55 − $40 = **$15**, which the writer owes. The "incorrect" assertion is False. |
| C | False (accurate) | Correct: above the strike a call's payoff rises **dollar-for-dollar** with the stock, so each $1 rise adds $1 to the writer's obligation. |
| D | True (incorrect) | The quoted "max loss limited to the $40 strike" **is wrong** — a stock has no price ceiling, so an **uncovered short call's loss is unbounded**. The inverted verdict is True. |
| E | False (accurate) | Correct: the long call's upside and the uncovered short call's loss are opposite sides of an exposure that **grows without a fixed bound** as the stock rises. |

**Reference:** Hull, "Properties of Stock Options" and "Trading Strategies Involving Options" (naked/uncovered call risk, unbounded loss); *Options & Futures: A Tutorial* (ML4T week-15), short-call payoff; Balch ML4T Options lecture (writer payoff profiles).

### [QF2-D9G2Q1] Long put payoff on an in-the-money European put
**Scenario:** An investor buys a European put with a $90 strike; at expiration the stock closes at $72. Consider payoff before subtracting the premium.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | A put grants its holder the right to **sell** the underlying at the strike ($90). |
| B | True | Payoff = max($90 − $72, 0) = **$18** per share — the amount by which the strike exceeds the stock. |
| C | True | At 100 shares, $18 × 100 = **$1,800** total payoff. |
| D | False | A put has **positive** intrinsic payoff when the stock is *below* the strike; it is ITM and worth $18 here, not worthless. |
| E | True | The short put writer takes the opposite side: if exercised, the writer must **buy at the strike**, bearing the obligation matching the holder's right. |

**Reference:** Hull, "Mechanics of Options Markets" / "Properties of Stock Options" (put payoff, right to sell, long–short mirror); *Options & Futures: A Tutorial* (ML4T week-15), put payoff diagrams; Balch ML4T Options lecture (put payoff at expiration).

### [QF2-D9G2Q2] Out-of-the-money put — speculation without owning the stock
**Scenario:** A speculator owns no stock but buys a $35-strike put; the stock finishes at $43; the premium paid was $2 per share. Each item asserts its quoted statement is incorrect.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | The quoted statement is correct: payoff = max($35 − $43, 0) = **$0** (the put is OTM). Marking it "incorrect" is False. |
| B | True (incorrect) | The quoted "should exercise the right to sell for $35 when the market is $43" **is wrong** — selling at $35 is worse than selling at $43 in the market, so the holder does not exercise. Inverted verdict True. |
| C | False (accurate) | Correct: with a $0 payoff, the $2 premium is the position's loss, i.e., a **$2-per-share net loss**. |
| D | True (incorrect) | The quoted "owning the underlying is required to buy a put" **is wrong** — a trader may buy a put with no stock to **speculate** on a decline. Inverted verdict True. |
| E | False (accurate) | Correct: a long put can express a **bearish view** or **hedge** an existing long position — both are valid uses. |

**Reference:** Hull, "Properties of Stock Options" and "Trading Strategies Involving Options" (put payoff, speculation vs. hedging, exercise decision); *Options & Futures: A Tutorial* (ML4T week-15), uses of puts; Balch ML4T Options lecture (speculative vs. protective puts).

### [QF2-D9G2Q3] Uncovered short put — loss bounded at the strike
**Scenario:** A trader writes an uncovered put with a $60 strike and receives a $4 premium; assume the stock cannot fall below zero and the position is held to expiration. Each item asserts its quoted statement is incorrect.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: a put writer's **maximum profit is the $4 premium**, kept when no payoff is owed; no more can be earned from the option. |
| B | False (accurate) | Correct: max($60 − S, 0) = 0 whenever S ≥ $60, so the put expires without an exercise payoff at or above the strike. |
| C | False (accurate) | Correct: at S = 0 the writer bears the holder's payoff of $60 − 0 = **$60 per share** (before premium). |
| D | True (incorrect) | The quoted "maximum possible loss is $64" **is wrong** — the $4 premium **offsets** part of the $60 obligation, so the max net loss is **$56** per share. Inverted verdict True. |
| E | False (accurate) | Correct: unlike an uncovered short call (unbounded), the short put's loss **is bounded** because the stock cannot fall below zero (worst case S = 0). |

**Reference:** Hull, "Trading Strategies Involving Options" (naked put risk, bounded loss at S=0, premium offset); *Options & Futures: A Tutorial* (ML4T week-15), short-put payoff and breakeven; Balch ML4T Options lecture (writer risk profiles).

### [QF2-D9G3Q1] Long call — payoff, net profit, and the $106 breakeven
**Scenario:** An investor pays $6 per share for a $100-strike call and holds to expiration; ignore commissions. Each item asserts its quoted statement is incorrect.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: a long call's expiration payoff is **max(S − $100, 0)**. Marking it "incorrect" is False. |
| B | False (accurate) | Correct: net profit = payoff − $6 premium; profit accounts for both the terminal payoff and the initial cost. |
| C | False (accurate) | Correct: **breakeven = K + premium = $100 + $6 = $106**, where $106 − $100 = $6 exactly offsets the premium. |
| D | False (accurate) | Correct: at $103 the payoff is $3 (positive) but it is less than the $6 paid, leaving a **$3 net loss** — payoff positive, profit negative. |
| E | True (incorrect) | The quoted "at $100 the buyer recovers the entire premium through exercise" **is wrong** — the payoff at the strike is **$0**, so the premium is not recovered. Inverted verdict True. |

**Reference:** Hull, "Properties of Stock Options" (payoff vs. profit, breakeven = strike + premium); *Options & Futures: A Tutorial* (ML4T week-15), call profit diagrams; Balch ML4T Options lecture (breakeven and net profit).

### [QF2-D9G3Q2] Long put — breakeven, net profit, and limited loss
**Scenario:** An investor pays $5 per share for an $80-strike put and holds to expiration; ignore commissions. Each item asserts its quoted statement is incorrect.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: **put breakeven = K − premium = $80 − $5 = $75**, where a $75 stock creates a $5 payoff equal to the premium. |
| B | False (accurate) | Correct: at $77 the payoff is max($80 − $77, 0) = **$3** per share. |
| C | True (incorrect) | The quoted "a positive put payoff means a positive net profit" **is wrong** — the $3 payoff does not recover the $5 premium, so the net result is a **$2 loss**. Inverted verdict True. |
| D | False (accurate) | Correct: at $70 the payoff is $10; $10 − $5 premium = **$5 net profit**. |
| E | False (accurate) | Correct: at or above $80 the put expires worthless, so the buyer's loss is limited to the **$5 premium** (a long option's max loss). |

**Reference:** Hull, "Properties of Stock Options" (put breakeven = strike − premium, max loss = premium); *Options & Futures: A Tutorial* (ML4T week-15), put profit diagrams; Balch ML4T Options lecture (payoff vs. profit).

### [QF2-D9G3Q3] Zero-sum: call buyer vs. writer on the same contract
**Scenario:** One trader buys a $50-strike call for $4; another writes the same call and receives $4. The stock closes at $61 at expiration; ignore other costs.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The call is $11 ITM: payoff to the buyer = $61 − $50 = **$11** per share. |
| B | True | Buyer's net profit = $11 payoff − $4 premium = **$7** per share. |
| C | False | The writer **owes $11** at expiration, which exceeds the $4 received — the premium alone does not make the writer's result positive. |
| D | True | Writer's net = $4 received − $11 obligation = **−$7** per share. |
| E | True | With identical prices and no costs, the buyer's +$7 and writer's −$7 **sum to zero** — a single option contract is zero-sum between the two sides. |

**Reference:** Hull, "Properties of Stock Options" (long vs. short profit, zero-sum before costs); *Options & Futures: A Tutorial* (ML4T week-15), buyer–writer symmetry; Balch ML4T Options lecture (writer vs. holder P&L).

### [QF2-D9G4Q1] Call moneyness and intrinsic value
**Scenario:** A stock trades at $52; consider a $45-strike call, a $52-strike call, and a $60-strike call with the same expiration.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | A call is **ITM** when S > K: $52 > $45, so the $45 call is in the money. |
| B | True | A call is **ATM** when S = K: $52 = $52. |
| C | True | A call is **OTM** when K > S: $60 > $52, so the $60 call is out of the money. |
| D | True | Call intrinsic value = max($52 − $45, 0) = **$7** per share. |
| E | False | Intrinsic value is **floored at zero** — it cannot be negative; the $60 call's intrinsic value is $0, not −$8. |

**Reference:** Hull, "Properties of Stock Options" (moneyness definitions, intrinsic value floored at zero); *Options & Futures: A Tutorial* (ML4T week-15), moneyness; Balch ML4T Options lecture (intrinsic value).

### [QF2-D9G4Q2] Put moneyness and intrinsic value
**Scenario:** A stock trades at $38; consider puts with strikes of $32, $38, and $45, all same expiration. Each item asserts its quoted statement is incorrect.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: a put is **ITM** when K > S: $45 > $38, so the $45 put is in the money. Marking it "incorrect" is False. |
| B | False (accurate) | Correct: a put is **ATM** when K = S: $38 = $38. |
| C | False (accurate) | Correct: a put is **OTM** when K < S: $32 < $38 (selling at $32 has no value when the stock is $38). |
| D | False (accurate) | Correct: put intrinsic value = max($45 − $38, 0) = **$7** per share. |
| E | True (incorrect) | The quoted "raising the strike from $38 to $45 *decreases* intrinsic value" **is wrong** — for a put, with the stock fixed, a **higher strike raises** intrinsic value (from $0 to $7). Inverted verdict True. |

**Reference:** Hull, "Properties of Stock Options" (put moneyness, intrinsic value increases with strike for puts); *Options & Futures: A Tutorial* (ML4T week-15), moneyness; Balch ML4T Options lecture (intrinsic value).

### [QF2-D9G4Q3] Moneyness and intrinsic value shift with the stock price
**Scenario:** A $100-strike call and a $100-strike put share the same underlying and expiration. The stock first trades at $94, later rises to $108. Evaluate moneyness and intrinsic value at both moments.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | At $94 (below the common strike) the **call is OTM and the put is ITM** — a low price favors the put. |
| B | True | Put intrinsic value at $94 = $100 − $94 = **$6** per share. |
| C | True | Call intrinsic value at $108 = $108 − $100 = **$8** per share. |
| D | False | At $108 the **call is ITM but the put is OTM** — they cannot both be ITM at the same price with the same strike. |
| E | True | Moneyness describes the **current** relationship between stock and strike, so a price change flips moneyness even with a fixed strike. |

**Reference:** Hull, "Properties of Stock Options" (moneyness depends on current S vs. K); put–call relationship via parity (C − P = S − K·e^(−rT)); *Options & Futures: A Tutorial* (ML4T week-15); Balch ML4T Options lecture (moneyness dynamics).

### [QF2-D9G5Q1] Out-of-the-money call carries time value
**Scenario:** A stock trades at $100; a $110-strike call with three months left trades for $3 even though immediate exercise yields nothing.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | S = $100 < K = $110, so the call is **OTM**. |
| B | True | Intrinsic value = max($100 − $110, 0) = **$0**. |
| C | True | The $3 price is **time value** — it reflects the chance the stock rises above $110 before expiry. |
| D | False | A positive price with zero intrinsic value is **not** an error — an option can have time value even with no intrinsic value. |
| E | True | If the stock is still $100 at expiration, the OTM call has **no exercise payoff** ($0). |

**Reference:** Hull, "Properties of Stock Options" (intrinsic vs. time value) and "The Black–Scholes–Merton Model" (price reflects probability of finishing ITM); *Options & Futures: A Tutorial* (ML4T week-15), time value; Balch ML4T Options lecture (time value and Black–Scholes intuition).

### [QF2-D9G5Q2] Volatility raises option value via asymmetric payoff
**Scenario:** Two identical-priced stocks at $50 — Calm (stays near $50) vs. Volatile (may move widely). Consider $50-strike calls, same expiration, other inputs held constant. Each item asserts its quoted statement is incorrect.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: greater uncertainty makes the call on Volatile **more valuable** — higher σ raises call value (positive vega). |
| B | False (accurate) | Correct: the holder benefits from large upside while the payoff is **floored at zero** on the downside — this asymmetry is why volatility adds value. |
| C | True (incorrect) | The quoted "a large downside move makes the long call's payoff negative" **is wrong** — a long call's payoff **cannot fall below zero**. Inverted verdict True. |
| D | False (accurate) | Correct: option value depends on the **distribution of future prices** (σ), not only today's price and strike, so volatility can matter even at equal spot and strike. |
| E | True (incorrect) | The quoted "higher value implies the market knows Volatile will finish above $50" **is wrong** — higher value reflects **uncertainty/asymmetry**, not a directional certainty. Inverted verdict True. |

**Reference:** Hull, "The Black–Scholes–Merton Model" (volatility input; value rises with σ) and "The Greek Letters" (vega); *Options & Futures: A Tutorial* (ML4T week-15), volatility and option value; Balch ML4T Options lecture (why volatility raises option value).

### [QF2-D9G5Q3] Time decay of an out-of-the-money call
**Scenario:** An OTM call is observed 60 days before expiration and again one day before, with stock price, strike, expected volatility, rates, and all other inputs held unchanged.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Less time remaining means **less opportunity** for the stock to move above the strike. |
| B | True | Holding inputs fixed isolates the usual **loss of time value** (negative theta) as expiry nears. |
| C | False | Time decay erodes **time value**, not intrinsic value — intrinsic value is never negative and is set by S vs. K. |
| D | True | At expiration there is **no time value left**; value equals the terminal payoff only. |
| E | False | Time decay does **not** guarantee a daily price drop — real changes in S and σ can offset or overwhelm it. |

**Reference:** Hull, "The Greek Letters" (theta / time decay) and "Properties of Stock Options" (intrinsic vs. time value); *Options & Futures: A Tutorial* (ML4T week-15), time decay; Balch ML4T Options lecture (theta intuition).

### [QF2-D9G6Q1] Protective put — a floor, not a free lunch
**Scenario:** An investor owns stock bought at $80 and buys a $75-strike put for $3; both held to expiration. Ignore dividends and other costs.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Long stock + long put on that stock **is a protective put** strategy. |
| B | True | At $50 the right to sell for $75 is worth **$25**, offsetting the stock's decline below $75. |
| C | True | The put establishes a **$75 sale floor** at expiration before counting the $3 insurance cost. |
| D | False | It is **not** risk-free — the investor can still lose ($80 purchase − $75 strike) + $3 premium = $8 per share. |
| E | True | On a strong rally the investor leaves the put unexercised and **keeps the upside, less the premium** paid. |

**Reference:** Hull, "Trading Strategies Involving Options" (protective put: floor at strike, residual loss, upside retained); *Options & Futures: A Tutorial* (ML4T week-15), protective put; Balch ML4T Options lecture (hedging with puts).

### [QF2-D9G6Q2] Covered call — premium cushion, capped upside
**Scenario:** An investor owns stock at $100 and writes a $110-strike call for a $4 premium; both held to expiration. Each item asserts its quoted statement is incorrect.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: owning the shares that may be delivered makes this a **covered call** — the shares cover the written call's obligation. |
| B | False (accurate) | Correct: at $105 the $110 call is OTM, so it expires without exercise and the writer **keeps the premium**. |
| C | False (accurate) | Correct: at $130 the short call's loss grows with the stock's gain above $110, **capping** the combined upside. |
| D | True (incorrect) | The quoted "retains unlimited upside while collecting the premium" **is wrong** — the written call **gives away gains above $110** (apart from the premium). Inverted verdict True. |
| E | False (accurate) | Correct: the $4 premium offsets only the first $4 of decline — a **limited cushion**, not full downside protection. |

**Reference:** Hull, "Trading Strategies Involving Options" (covered call: capped upside, premium cushion, covered vs. naked); *Options & Futures: A Tutorial* (ML4T week-15), covered call; Balch ML4T Options lecture (writing calls against stock).

### [QF2-D9G6Q3] Protective-put strike selection — the protection/cost tradeoff
**Scenario:** A PM compares three-month protective puts: a higher-strike put costs more but protects after a smaller decline; a lower-strike put is cheaper but leaves a larger initial loss unprotected. Each item asserts its quoted statement is incorrect.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: choosing a strike is a **tradeoff between protection level and premium cost** — more/earlier protection costs more. |
| B | False (accurate) | Correct: a higher strike supports a **higher terminal floor** for the same underlying exposure. |
| C | False (accurate) | Correct: a lower-strike put protects only after a **larger decline** — i.e., focused on more severe losses. |
| D | True (incorrect) | The quoted "buying either put eliminates every risk, including basis risk" **is wrong** — mismatched exposure/timing, premium cost, and other risks **remain**. Inverted verdict True. |
| E | False (accurate) | Correct: evaluating the hedge only in down markets ignores the **premium drag** on performance when the put expires unused or insufficiently valuable. |

**Reference:** Hull, "Trading Strategies Involving Options" (strike selection tradeoff) and "The Greek Letters" (hedge residual risk, basis risk); *Options & Futures: A Tutorial* (ML4T week-15), choosing protection; Balch ML4T Options lecture (hedge cost vs. protection).

### [QF2-D9G7Q1] Long stock vs. long call — asymmetric, nonlinear payoff
**Scenario:** Compare buying one share at $50 with buying a $50-strike call for a $5 premium, each held to the call's expiration.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Long stock has a **linear** terminal profit of (terminal price − $50), changing one-for-one across all prices. |
| B | True | The call buyer can abandon the option, so **maximum loss = the $5 premium**. |
| C | True | At $30 the stock loses $50 − $30 = $20, while the worthless call loses only its **$5 premium**. |
| D | False | At $80 the call payoff is $30, but net profit = $30 − $5 = **$25**, not $30 (subtract the premium). |
| E | False | A call has a **kink at the strike** and bounded downside, so it is **not** a constant leveraged multiple of the stock (nonlinear exposure). |

**Reference:** Hull, "Properties of Stock Options" (asymmetric payoff, max loss = premium) and "The Greek Letters" (gamma / nonlinearity); *Options & Futures: A Tutorial* (ML4T week-15), stock vs. option payoff; Balch ML4T Options lecture (nonlinear payoffs).

### [QF2-D9G7Q2] Long straddle — profiting from a large move either way
**Scenario:** A trader buys a $100-strike call and a $100-strike put on the same stock, same expiration, each costing $6; the stock trades at $100 and both are held to expiration.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Total premium = $6 + $6 = **$12** per share (one call + one put). |
| B | True | At $100 both finish ATM with zero payoff, so the position loses the full **$12** premium (the straddle's max loss). |
| C | True | At $125 the call is **$25** ITM and the put is OTM ($0) — the combined payoff comes from the call. |
| D | True | A sufficiently large move either way (beyond K ± total premium) produces a **positive net profit** — the put gains on a large fall, the call on a large rise. |
| E | False | The combined payoff is **V-shaped**: negative slope below $100, positive slope above — not a single linear slope. |

**Reference:** Hull, "Trading Strategies Involving Options" (straddle payoff, breakeven at K ± total premium, V-shaped combined payoff); *Options & Futures: A Tutorial* (ML4T week-15), straddles; Balch ML4T Options lecture (combining options).

### [QF2-D9G7Q3] Risk profiles — long stock vs. long call vs. uncovered short call
**Scenario:** A risk report compares three unhedged positions held to expiration — long stock, a long call, and an uncovered short call (strike $70) — across high and low terminal prices. Each item asserts its quoted statement is incorrect.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: long stock has large downside but it is **bounded** (the stock cannot fall below zero, so loss ≤ initial value on an unlevered position). |
| B | False (accurate) | Correct: the long call is **asymmetric** — loss limited to the premium, upside able to keep growing. |
| C | False (accurate) | Correct: the uncovered short call has **limited profit** (the premium) and **unbounded loss** as the stock rises. |
| D | True (incorrect) | The quoted "below the strike the long call loses an additional dollar per additional dollar decline" **is wrong** — once OTM the call payoff **stays at zero** as the stock falls further. Inverted verdict True. |
| E | False (accurate) | Correct: option payoff **sensitivity differs across regions** of the strike (the slope changes at K), giving nonlinear, state-dependent exposure unlike constant stock. |

**Reference:** Hull, "Properties of Stock Options" and "Trading Strategies Involving Options" (payoff profiles, bounded vs. unbounded loss) and "The Greek Letters" (state-dependent exposure, gamma); *Options & Futures: A Tutorial* (ML4T week-15), payoff comparisons; Balch ML4T Options lecture (risk profiles of stock vs. options).

## References (domain-level)

1. **Hull — *Options, Futures, and Other Derivatives* (cited at section level, no page numbers):**
   - "Mechanics of Options Markets" — contract specifications, calls vs. puts, holders vs. writers, contract multiplier (100 shares).
   - "Properties of Stock Options" — expiration payoffs max(S−K,0) / max(K−S,0), payoff floored at zero, intrinsic vs. time value, moneyness, breakeven, bounds, and **put–call parity** (C + K·e^(−rT) = P + S₀).
   - "Trading Strategies Involving Options" — protective put, covered call, straddle, naked/uncovered writing, strike-selection tradeoffs, bounded vs. unbounded loss.
   - "The Black–Scholes–Merton Model" — value as a function of S, K, T, σ, r; why higher volatility and more time raise option value (time value).
   - "The Greek Letters" — delta, gamma, theta, vega; time decay, nonlinear/state-dependent exposure, hedge residual (basis) risk.
2. **"Options & Futures: A Tutorial" (ML4T week-15 assigned reading):** payoff and profit diagrams for calls/puts (long and short), premium/payoff/breakeven mechanics, moneyness and intrinsic value, protective-put and covered-call hedging, and straddle payoffs.
3. **Balch — ML4T Options lecture (Georgia Tech):** option payoff diagrams at expiration, payoff-vs-profit distinction, writer vs. holder P&L and the zero-sum pairing, intrinsic vs. time value and volatility/time intuition, and hedging with options (protective put, covered call).

<!-- Source fidelity note: all A–E verdicts above are transcribed verbatim from slices/QF2_D09.txt (never flipped). For the 10 inverted-polarity questions the slice verdicts "True – The quoted statement is incorrect." / "False – The quoted statement is correct." are rendered as "True (incorrect)" / "False (accurate)" per the required QF format. Garbled ligatures (ﬁ/ﬂ) in the source are normalized to fi/fl in explanatory text only. -->
