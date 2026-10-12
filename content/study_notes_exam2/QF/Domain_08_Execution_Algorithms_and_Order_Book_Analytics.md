# QF Domain 8 — Execution Algorithms & Order Book Analytics

## Domain cheat-sheet

- **The limit order book (LOB) and how trades happen.** An order-driven market matches buyers and sellers through a **limit order book**: a price-ordered queue of resting limit orders on each side. The **best bid** is the highest price a buyer will pay; the **best ask (offer)** is the lowest price a seller will accept. The gap between them is the **bid-ask spread**, and the **midpoint** = (bid + ask)/2 is the usual reference "fair" price. A trade occurs when an incoming order crosses the spread and matches resting liquidity. Depth at each price level is *displayed liquidity* — a snapshot that can change in milliseconds as orders arrive, cancel, or execute.
- **Limit vs. market (marketable) orders — the core tradeoff.**
  - A **market order** (or marketable limit) demands *immediacy*: it crosses the spread and executes against the best available opposing liquidity. A buyer lifts the ask; a seller hits the bid. It maximizes **execution certainty** but pays the spread and risks walking the book (slippage through multiple price levels) when depth is thin.
  - A **limit order** posts passively at or inside the quote and *provides* liquidity. It can earn a better price (buy below the ask / sell above the bid) but faces **non-execution (fill) risk**: it only trades if opposing flow reaches it. A posted order is **never guaranteed to fill**, even at the best bid/ask, because of the queue ahead of it.
  - This is the recurring theme: **price improvement vs. fill probability**, and **patience/cost-of-non-execution vs. urgency/execution certainty**. The right choice depends on urgency, the cost of delay, price risk, and the objective — not the quoted spread alone.
- **Maker/taker and spread capture.** A passive order that rests and gets hit is the **maker** (provides liquidity); the aggressor who crosses is the **taker** (demands liquidity). Many venues rebate makers and charge takers (maker-taker pricing). A maker *hopes* to earn the spread, but **a fill does not guarantee realized spread profit** — see adverse selection.
- **Price-time priority & queue position.** In most order-driven markets, resting orders at the same price execute by **time priority** (first-in, first-out). Two orders at the same limit price do **not** have equal fill probability: the one that arrived earlier (less size ahead) is more likely to fill. **Cancellations by orders ahead** improve a later order's queue position. Repricing to a new level typically **forfeits** the old queue position and creates a new one at the back of the new queue.
- **Order scheduling: market impact vs. timing (exposure) risk.** Splitting a large *parent* order into *child* orders over time is governed by a fundamental tension (Almgren-Chriss):
  - **Trade fast / front-load** → less time exposed to adverse price moves (**lower timing risk**) but concentrated demand consumes book depth and moves price (**higher market impact**).
  - **Trade slow / back-load** → smaller child orders cause less impact, but a larger quantity stays unexecuted longer and exposed to price movement (**higher timing/non-completion risk**).
  - Neither is universally cheaper; the optimal horizon trades **expected impact against variance of cost**. Risk aversion and urgency shift the choice. A **dynamic** schedule adapts child-order size/aggressiveness as liquidity, volatility, and urgency change — reassessing is correct when conditions shift.
- **Benchmark algorithms (VWAP / TWAP / POV / IS).**
  - **VWAP (volume-weighted average price):** allocates child orders in proportion to *forecast* volume per interval, aiming to match the market's volume-weighted average. Needs an accurate **intraday volume curve**; a static forecast misfires on event days (e.g., index rebalance surges).
  - **TWAP (time-weighted average price):** allocates *equal* shares to *equal* time intervals. It is **time-based** and, by definition, does **not** require a volume forecast. VWAP and TWAP coincide only when expected volume is uniform.
  - **Percentage-of-volume (POV / participation):** trades a fixed fraction of *observed* market volume (e.g., 10%). It automatically slows when volume falls and speeds when volume rises, so **completion by a clock time is not guaranteed** — it depends on realized volume and parent size, creating incomplete-execution risk in thin markets.
  - **Implementation shortfall (IS / arrival-price):** minimizes the gap between the decision-time (arrival) price and the realized average execution cost, explicitly trading impact against timing risk; it also charges **opportunity cost** for any unexecuted quantity.
- **Implementation shortfall measurement.** IS = (execution cost relative to the **arrival/decision benchmark**) + explicit costs (commissions/fees) + **opportunity cost** of unfilled shares. For a buy: price shortfall = (avg fill − arrival midpoint) × filled shares; add commissions; add the opportunity cost of shares intended but not bought. **Benchmark choice must match the objective** — arrival price measures execution *after* the investment decision; a *closing* price is relevant only when the mandate targets end-of-day valuation. Subsequent favorable price moves do **not** erase the cost already paid relative to the benchmark.
- **Order-book imbalance & short-term signals.** Imbalance = (bid depth − ask depth) / (bid depth + ask depth), ranging −1 to +1. A positive value means more displayed size at the bid than the ask and *can* (under some conditions) be associated with short-horizon upward pressure — but it **guarantees nothing**: hidden liquidity, cancellations, new orders, and trades can reverse the apparent signal. A snapshot describes *displayed* liquidity at a moment; **fleeting/spoofed quotes** that cancel in milliseconds overstate dependable liquidity. Robust evaluation needs multiple depth levels, **quote persistence**, latency, and realized fills — not a single snapshot.
- **Adverse selection, markouts, and latency.** **Adverse selection** is the risk that passive fills are concentrated right before the price moves *against* the maker — informed or better-timed counterparties trade when the posted quote is stale/favorable to them. A high fill rate can therefore coexist with **poor execution quality**. Measure quality with **post-fill markouts** (price change over the seconds/minutes after the fill), not just the fraction filled or the quoted spread captured. **Latency** matters: in live trading, delay, false signals, and changing behavior make backtested snapshot signals degrade after costs. **Information leakage** — predictable child-order timing/size — lets others trade ahead, raising later execution cost; randomization reduces but cannot eliminate the footprint, and merely *splitting* a parent order does not prevent leakage.

## Common traps

- **Inverted-polarity questions (10 of 21 here).** When the body says "each item asserts that its quoted statement is **incorrect** … evaluate the complete A–E items as written," the Answer Key verdict is flipped relative to the embedded claim's truth: **True = the embedded statement is wrong; False = the embedded statement is accurate.** Read the polarity line *first*. Inverted here: **G1Q2, G2Q1, G3Q1, G3Q3, G4Q1, G4Q2, G5Q1, G6Q1, G7Q1, G7Q2.** The remaining 11 are Normal (True = accurate).
- **"Later appreciation cancels the execution cost."** False — IS is measured against the *arrival/decision* benchmark; a higher close does not undo the price paid above arrival. Negative IS is not created by subsequent portfolio profit.
- **Benchmark = closing price always.** Wrong — the benchmark must match the objective. Arrival price measures post-decision execution; closing price is apt only when the mandate explicitly targets end-of-day ownership/valuation.
- **"Beating VWAP proves every child order was well executed" / "a passive fill earns the full spread."** Both false — aggregate outperformance can hide poorly executed children, and post-fill adverse moves (adverse selection) can exceed any spread captured.
- **"A limit order at the best bid is guaranteed to fill."** False — queue priority, size ahead, and whether opposing flow arrives all determine fills; equal limit prices do **not** imply equal fill probability.
- **Market order "has no cost because it completes immediately."** False — crossing the spread, market impact, and adverse movement are real costs; immediacy is paid for.
- **"Slower is always cheaper" / "faster is always cheaper."** Both false — slowing adds timing/non-completion risk; speeding adds impact. The optimal horizon is a tradeoff, and slowing when volatility rises does **not** always reduce IS.
- **"TWAP needs a volume forecast."** False — TWAP is purely time-based; VWAP and POV are the volume-linked ones.
- **"Fixed participation rate guarantees completion by a clock time."** False — POV completion depends on realized market volume; thin volume → under-trading and incomplete execution.
- **"Imbalance guarantees the next tick is up."** False — it is a transient, probabilistic signal that hidden liquidity, cancellations, and new flow can reverse.
- **Larger displayed depth = more real liquidity.** False — routinely-cancelled (fleeting/spoofed) quotes are not dependable executable liquidity; persistence and realized fills reveal what a snapshot omits.
- **"Backtest profitability proves the live signal is reliable."** False — latency, false signals, changing behavior, and trading frictions make live results differ.
- **"Splitting into child orders / randomizing prevents information leakage."** False — a predictable sequence can reveal the parent precisely because it is split; randomization reduces but cannot guarantee secrecy.
- **"Unfilled shares create no execution concern because no trade occurred."** False — unexecuted quantity carries opportunity cost and mandate/price-movement risk; IS can and should include it.
- **"Static schedule can ignore new information."** False — adaptive execution should reassess when volatility, depth, or urgency change materially.

## Questions

### [QF2-D8G1Q1] Implementation shortfall on a completed purchase
**Scenario:** A PM decides at 10:00 a.m. to buy 20,000 shares when the midpoint is $40.00. Average execution price is $40.12, commissions are $200, and the stock closes at $40.30. Later portfolio profit is ignored when measuring execution cost.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The arrival (decision-time) midpoint of $40.00 is the stated reference against which post-decision execution cost is measured. |
| B | True | Price shortfall for the buy = (avg fill − arrival) × shares = ($40.12 − $40.00) × 20,000 = $0.12 × 20,000 = $2,400 before commissions. |
| C | True | Implementation shortfall = price shortfall + explicit costs = $2,400 + $200 commission = $2,600 on the completed purchase. |
| D | False | Subsequent appreciation (close at $40.30) does not create negative IS; the cost of $2,600 relative to the arrival benchmark stands regardless of later price moves. |
| E | True | Benchmark choice must match the objective: the close can answer a different evaluation question, but arrival price is the correct benchmark for the cost of implementing this decision. |

**Reference:** Harris, *Trading and Exchanges*, ch. on transaction-cost measurement (implementation shortfall) and on the bid/ask spread as a cost; Almgren-Chriss, *Optimal Execution of Portfolio Transactions* (arrival-price benchmark); Balch ML4T Market Mechanics (02-02).

### [QF2-D8G1Q2] VWAP vs. TWAP benchmark alignment
**Scenario:** A pension fund wants its purchase price to resemble the market's volume-weighted average. The trader reports an average fill of $25.06; market VWAP was $25.10, equal-interval TWAP was $25.04, and the close was $25.30. Each item asserts that its quoted statement is incorrect.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | The quoted claim is correct: VWAP is the benchmark most directly aligned with an objective that explicitly targets the market's volume-weighted average price. Correct → inverted verdict is False. |
| B | False (accurate) | Correct: a buyer prefers a lower price, and $25.06 is $0.04 below the $25.10 VWAP, so the fill beat VWAP for this buy. |
| C | False (accurate) | Correct: the fill of $25.06 is $0.02 above the $25.04 TWAP, so the buy underperformed TWAP by $0.02 per share. |
| D | True (incorrect) | Wrong: beating VWAP in aggregate does not prove every child order was favorably executed — good aggregate performance can coexist with poorly executed children. |
| E | False (accurate) | Correct: the fill beats VWAP but trails TWAP, so whether $25.06 is "favorable" depends on the chosen benchmark. |

**Reference:** Harris, *Trading and Exchanges*, ch. on execution benchmarks and transaction-cost measurement (VWAP/TWAP); Balch ML4T Market Mechanics (02-02) on VWAP/TWAP execution.

### [QF2-D8G1Q3] Closing-price mandate and unfilled quantity
**Scenario:** A fund must own 100,000 shares by today's close (mandate effective at closing valuation). The trader buys 70,000 at an average of $60.10, leaves 30,000 unfilled, and the stock closes at $60.50. Arrival midpoint was $60.00.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | A closing-price benchmark can be relevant here because the mandate specifically targets end-of-day ownership and valuation. |
| B | True | Relative to the $60.50 close, the completed fills at $60.10 were purchased $0.40 per share below that benchmark. |
| C | False | The unfilled 30,000 shares *do* create concern — failure to acquire the required quantity exposes the fund to missed-price-movement and mandate risk. |
| D | True | Implementation shortfall can include the opportunity cost of the intended-but-unexecuted quantity, not just realized trades. |
| E | True | Evaluating only the 70,000 completed shares flatters execution quality by ignoring the consequence of the unfilled portion of the full 100,000-share decision. |

**Reference:** Harris, *Trading and Exchanges*, ch. on transaction-cost measurement (implementation shortfall, opportunity cost of non-execution; benchmark selection); Almgren-Chriss (timing/non-completion risk); Balch ML4T Market Mechanics (02-02).

### [QF2-D8G2Q1] Marketable vs. passive limit for an urgent buy
**Scenario:** A stock is quoted $19.98 bid / $20.02 ask. A trader who urgently needs to buy may submit a marketable order or post a limit buy at $19.98. Each item asserts that its quoted statement is incorrect.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: a marketable buy trades against displayed sell liquidity near the ask — an aggressive buyer consumes ask-side depth. |
| B | False (accurate) | Correct: posting a bid-side limit at $19.98 waits rather than immediately crossing the quoted spread. |
| C | True (incorrect) | Wrong: a passive order at the best bid is *not* guaranteed to fill — other orders may be ahead in the queue, and sellers may never trade at the bid. |
| D | False (accurate) | Correct: crossing the spread normally raises the chance of immediate execution relative to the passive order, subject to available depth. |
| E | False (accurate) | Correct: if the price rises while the passive order waits, the trader faces waiting/opportunity cost — the position may become costlier or remain unfilled. |

**Reference:** Harris, *Trading and Exchanges*, ch. 4 on orders and order properties (limit vs. market orders), and ch. on liquidity and the bid/ask spread; Balch ML4T Market Mechanics (02-02).

### [QF2-D8G2Q2] Partial passive fill then adverse price move
**Scenario:** A trader posts a buy limit at $50.00 while the best bid/ask is $50.00/$50.04. Half fills. News arrives, the quote jumps to $50.20/$50.24, and the remainder never fills.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The filled portion executed at $50.00, $0.04 below the original $50.04 ask — a passive price improvement on that half. |
| B | False | A good price on the filled half does not prove superior execution for the whole decision; the missed remainder as the market rose means the complete decision may have performed poorly. |
| C | True | The unfilled portion incurred opportunity cost: the trader lost the chance to buy that quantity near the original price if shares were still wanted. |
| D | True | Replacing the remainder with a marketable order at the new quote raises execution urgency/certainty but likely requires paying a higher price. |
| E | True | Partial-fill (non-execution) risk is a defining difference between passive execution and an immediately marketable order. |

**Reference:** Harris, *Trading and Exchanges*, ch. 4 (order properties, fill risk) and ch. on liquidity; Almgren-Chriss (timing risk from unexecuted inventory); Balch ML4T Market Mechanics (02-02).

### [QF2-D8G2Q3] Urgency and the aggressive/passive choice
**Scenario:** Two traders must sell the same stock. Trader A must liquidate within one minute to meet a risk limit; Trader B has until end of week and expects patient buyers. Both face a $30.00 bid / $30.06 ask.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Trader A's imminent risk deadline makes execution certainty especially valuable, giving a stronger reason to trade aggressively than Trader B. |
| B | True | A marketable sell crosses to the bid side, interacting with liquidity near the $30.00 bid. |
| C | True | Posting a sell limit at the $30.06 ask could earn $0.06 more than hitting the $30.00 bid — if it fills. |
| D | False | A longer horizon does not eliminate all passive-order risk: prices can move, queues persist, and the order may still fail to fill. |
| E | True | The aggressive-passive choice depends on urgency and the cost of non-execution, not only on the quoted spread. |

**Reference:** Harris, *Trading and Exchanges*, ch. 4 (limit vs. market orders) and ch. on liquidity/immediacy; Almgren-Chriss (urgency/risk aversion in execution); Balch ML4T Market Mechanics (02-02).

### [QF2-D8G3Q1] Fast vs. slow schedule — impact vs. exposure
**Scenario:** A trader must buy 500,000 shares. Plan Fast completes in 30 minutes with high participation; Plan Slow spreads it across six hours with smaller child orders. Price is uncertain during the day. Each item asserts that its quoted statement is incorrect.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: completing sooner reduces the duration the unexecuted order is exposed to price movement (lower timing risk). |
| B | False (accurate) | Correct: Plan Fast can create more market impact by demanding liquidity rapidly and consuming book depth. |
| C | True (incorrect) | Wrong: Plan Slow does not necessarily have lower total cost in every condition — adverse price movement over the longer horizon can outweigh impact savings. |
| D | False (accurate) | Correct: Plan Slow generally leaves more timing risk because a larger quantity stays unexecuted and price-sensitive for longer. |
| E | False (accurate) | Correct: choosing an execution horizon trades off market impact against exposure to market movement (the Almgren-Chriss tension). |

**Reference:** Almgren-Chriss, *Optimal Execution of Portfolio Transactions* (impact vs. timing-risk trade-off, efficient frontier of trading); Harris, *Trading and Exchanges*, ch. on transaction costs and market impact; Balch ML4T Market Mechanics (02-02).

### [QF2-D8G3Q2] Front-loading around a scheduled announcement
**Scenario:** A trader expects an important announcement at noon and must finish a buy by 3:00 p.m. Schedule A executes 70% before noon; Schedule B executes 30% before noon and 70% after.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Schedule A allocates a larger fraction earlier, so it is front-loaded relative to Schedule B. |
| B | True | Executing 70% pre-noon leaves only 30% exposed to the noon announcement. |
| C | False | Front-loading changes exposures but does not determine the direction of prices or guarantee a lower average purchase price. |
| D | True | If pre-noon liquidity is thin, concentrating buying there can produce more impact/price pressure before the announcement. |
| E | True | Schedule B (back-loading) can be attractive if liquidity is expected to improve after noon, at the cost of leaving more shares exposed to announcement risk. |

**Reference:** Almgren-Chriss, *Optimal Execution* (scheduling, exposure vs. impact); Harris, *Trading and Exchanges*, ch. on liquidity and intraday trading patterns; Balch ML4T Market Mechanics (02-02).

### [QF2-D8G3Q3] Dynamic re-scheduling when conditions change
**Scenario:** A sell algorithm planned to execute evenly over four hours. After one hour, volatility rises sharply, displayed depth falls, and the risk manager says the position must be reduced promptly. Each item asserts that its quoted statement is incorrect.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: continuing the original schedule without reassessment ignores new information — market state and the cost of delay have materially changed. |
| B | False (accurate) | Correct: lower displayed depth can increase the impact of aggressive selling, since the same quantity moves through more price levels. |
| C | False (accurate) | Correct: increased urgency can justify accelerating despite higher expected impact when satisfying the risk constraint is worth the cost. |
| D | True (incorrect) | Wrong: slowing the schedule does *not* always reduce implementation shortfall when volatility rises — delay can be costly if prices move adversely or a risk deadline looms. |
| E | False (accurate) | Correct: a dynamic schedule adjusts child-order size and aggressiveness as liquidity, volatility, and urgency change. |

**Reference:** Almgren-Chriss, *Optimal Execution* (adaptive/dynamic trajectories, volatility and risk aversion); Harris, *Trading and Exchanges*, ch. on liquidity and market impact; Balch ML4T Market Mechanics (02-02).

### [QF2-D8G4Q1] VWAP vs. TWAP allocation mechanics
**Scenario:** A stock normally trades 10%, 15%, 20%, 20%, 20%, 15% of daily volume across six equal intervals. A VWAP algorithm uses those forecast percentages; a TWAP algorithm assigns one-sixth of the parent order to each interval. Each item asserts that its quoted statement is incorrect.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: the VWAP schedule allocates more shares to intervals forecast to have greater volume (the 10/15/20/20/20/15 curve). |
| B | False (accurate) | Correct: the TWAP schedule allocates equal shares (one-sixth) to each equal-duration interval. |
| C | True (incorrect) | Wrong: the two schedules do *not* produce the same child-order sizes just because totals match — allocations differ whenever expected volume percentages are non-uniform. |
| D | False (accurate) | Correct: if the volume forecast is accurate, VWAP keeps its trading pattern closer to the market's volume distribution. |
| E | True (incorrect) | Wrong: TWAP does *not* require an accurate intraday volume-curve forecast — a basic TWAP schedule is time-based. |

**Reference:** Harris, *Trading and Exchanges*, ch. on execution benchmarks (VWAP/TWAP) and intraday volume patterns; Balch ML4T Market Mechanics (02-02) on VWAP/TWAP algorithms.

### [QF2-D8G4Q2] Percentage-of-volume participation and completion risk
**Scenario:** A POV algorithm is instructed to buy 10% of observed market volume. Over three intervals, total market volume is 100,000, 300,000, and 50,000 shares. Each item asserts that its quoted statement is incorrect.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: 10% of 100,000 = 10,000 shares targeted in the first interval. |
| B | False (accurate) | Correct: 10% of 300,000 = 30,000 shares in the second interval. |
| C | False (accurate) | Correct: 10% of 50,000 = 5,000 shares in the third interval. |
| D | True (incorrect) | Wrong: a fixed 10% participation rate does *not* guarantee completion by a clock time — completion depends on realized market volume and parent-order size. |
| E | False (accurate) | Correct: when market volume unexpectedly falls, a participation strategy trades fewer shares than planned and risks incomplete execution (it slows automatically). |

**Reference:** Harris, *Trading and Exchanges*, ch. on execution strategies and liquidity (participation/volume-linked trading); Balch ML4T Market Mechanics (02-02).

### [QF2-D8G4Q3] Static VWAP forecast on an event day
**Scenario:** A VWAP algorithm forecasts heavy trading near the close. An unexpected morning index rebalance instead produces enormous early volume and unusually low afternoon volume. The algorithm does not update its forecast.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Expecting volume later, the static schedule may trade too little during the unexpectedly liquid morning surge. |
| B | True | Low later liquidity plus a completion requirement can force concentrated, aggressive trading later. |
| C | False | Historical volume curves are *not* guaranteed accurate on event days — events can materially change the intraday volume shape. |
| D | True | Updating the schedule using realized volume can improve alignment with the day's actual volume pattern (adaptive VWAP). |
| E | False | TWAP and POV would *not* necessarily produce identical trades — one is time-based and the other tied to realized volume, so their schedules can differ substantially. |

**Reference:** Harris, *Trading and Exchanges*, ch. on execution benchmarks and intraday volume (forecast error, event days); Balch ML4T Market Mechanics (02-02).

### [QF2-D8G5Q1] Limit placement — price improvement vs. fill probability
**Scenario:** A stock is quoted $70.00 bid / $70.05 ask. A trader considers three buy limits: $70.00, $69.95, $69.80; none is marketable when submitted. Each item asserts that its quoted statement is incorrect.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: the $70.00 order is closest to the current ask — it sits at the best bid, only $0.05 below the ask. |
| B | False (accurate) | Correct: the $69.80 order generally needs a larger downward move or deeper sell flow to execute, since sellers must reach well below the best bid. |
| C | True (incorrect) | Wrong: the $69.80 order does *not* have a higher immediate fill probability — moving farther from the market lowers near-term fill probability despite the better price. |
| D | False (accurate) | Correct: a lower bid gives a better price *if filled* while increasing non-execution risk — the favorable price is conditional on a fill. |
| E | False (accurate) | Correct: placement trades off price improvement against fill probability; passive traders must weigh price alongside whether execution occurs. |

**Reference:** Harris, *Trading and Exchanges*, ch. 4 (order properties, limit-order aggressiveness) and ch. on order-driven markets/fill probability; Balch ML4T Market Mechanics (02-02).

### [QF2-D8G5Q2] Queue position and price-time priority
**Scenario:** Two investors each post a 5,000-share buy at the best bid of $15.00. Investor A enters when 2,000 shares are already ahead; Investor B enters later, after another 20,000 shares joined the queue ahead. Assume price-time priority.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Investor A has a better queue position: only 2,000 shares ahead versus substantially more size ahead of Investor B. |
| B | True | If only 10,000 shares sell into the bid with no cancellations, the 2,000 ahead plus A's 5,000 (7,000) trade within the flow, leaving too little to reach B after the 20,000-share intervening queue. |
| C | False | Equal limit prices do *not* imply equal fill probabilities — time priority and quantity ahead materially affect execution. |
| D | True | Cancellations by orders ahead of B reduce the volume that must trade first, improving B's queue position. |
| E | True | Displayed depth alone does not reveal how much of a newly entered order will fill — future opposing flow, cancellations, priority rules, and queue position all matter. |

**Reference:** Harris, *Trading and Exchanges*, ch. on order-driven markets and order precedence rules (price-time priority); Balch ML4T Market Mechanics (02-02) on the order book.

### [QF2-D8G5Q3] Managing the remainder after a partial fill
**Scenario:** A trader needs 12,000 shares. A passive order fills 4,000, then the market moves up. The trader can leave the remaining 8,000 at the old price, reprice to the new best bid, or cross the spread.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Only 4,000 of the 12,000-share parent (one-third) has executed — a partial fill. |
| B | True | Leaving the remainder at the old (now stale, lower) price preserves a favorable limit if reached but reduces the chance of timely completion. |
| C | True | Repricing to the new best bid improves competitiveness but typically forfeits the old queue position (new order joins the back of the new queue). |
| D | True | Crossing the spread increases completion probability but may worsen the purchase price — trading price concession for certainty. |
| E | False | The best choice is *not* determinable without considering urgency and subsequent market movement — it depends on cost of delay, fill probability, price risk, and objectives. |

**Reference:** Harris, *Trading and Exchanges*, ch. 4 (order management, repricing, queue position) and ch. on liquidity; Almgren-Chriss (urgency and cost of delay); Balch ML4T Market Mechanics (02-02).

### [QF2-D8G6Q1] Order-book imbalance computation and interpretation
**Scenario:** At the best quotes a stock shows 80,000 shares bid and 20,000 offered. Imbalance = (bid depth − ask depth)/(bid depth + ask depth). Each item asserts that its quoted statement is incorrect.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: (80,000 − 20,000)/(80,000 + 20,000) = 60,000/100,000 = 0.60. |
| B | False (accurate) | Correct: the positive imbalance means more displayed depth at the best bid than the best ask (bid is 4× the ask size). |
| C | False (accurate) | Correct: under some conditions this imbalance can be read as short-term upward price pressure (scarce ask liquidity / strong bid support). |
| D | True (incorrect) | Wrong: the imbalance does *not* guarantee the next price change is upward — new orders, cancellations, hidden liquidity, and trades can reverse the signal. |
| E | False (accurate) | Correct: the measure describes displayed liquidity at a moment and can change quickly as orders arrive or cancel — a transient snapshot. |

**Reference:** Harris, *Trading and Exchanges*, ch. on order-driven markets, displayed depth, and the limitations of quote information; Balch ML4T Market Mechanics (02-02) on the order book.

### [QF2-D8G6Q2] Fleeting quotes vs. dependable liquidity
**Scenario:** Stock X shows 100,000 bid and 25,000 ask but both are routinely cancelled within milliseconds. Stock Y shows 20,000 bid and 20,000 ask that usually remain and absorb trades.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | X's best-level imbalance is positive (100k vs. 25k), while Y's is zero under the normalized measure — X has the more positive snapshot imbalance. |
| B | False | The larger displayed bid in X does *not* necessarily represent more reliable executable liquidity — rapid cancellation can make it unavailable when traders try to interact. |
| C | True | Cancellation behavior is relevant to interpreting depth: fleeting quotes may overstate dependable liquidity or directional interest. |
| D | False | A balanced book does *not* imply price cannot move — new information, trades, and later order changes can still move Y's price. |
| E | True | Quote persistence and realized fills provide information a single depth snapshot omits, distinguishing stable from transient liquidity. |

**Reference:** Harris, *Trading and Exchanges*, ch. on order-driven markets, quote reliability, and fleeting/hidden liquidity; Balch ML4T Market Mechanics (02-02).

### [QF2-D8G6Q3] Backtested imbalance signal vs. live frictions
**Scenario:** A researcher buys whenever best-level bid depth exceeds ask depth by 5:1. The rule looks profitable in historical snapshots. Live, large bid orders sometimes vanish just before sell orders arrive, and liquidity exists beyond the best quotes.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | Using only the best level ignores depth at deeper price levels, which affects both price pressure and execution. |
| B | True | Vanishing displayed bids make the historical signal overstate genuine buying support — cancelled size cannot absorb incoming selling. |
| C | True | A participant could create a misleading imbalance by displaying and cancelling large orders, though a single snapshot alone does not prove manipulation/intent. |
| D | False | Backtest profitability does *not* prove the signal remains reliable after costs and latency — live performance can differ due to delay, false signals, and frictions. |
| E | True | Testing multiple depth levels, quote persistence, latency, and execution costs addresses the omissions in a snapshot-only, frictionless analysis. |

**Reference:** Harris, *Trading and Exchanges*, ch. on order-driven markets, hidden liquidity, and manipulation; Balch ML4T Market Mechanics (02-02); general backtest-realism / latency caveats.

### [QF2-D8G7Q1] Adverse selection in passive fills
**Scenario:** A market maker repeatedly posts a buy at the best bid. The order fills immediately before negative news-driven trades push the stock lower, but often stays unfilled when the price rises. Each item asserts that its quoted statement is incorrect.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: this fill pattern is consistent with adverse selection — the order fills disproportionately when subsequent information makes the purchase unattractive. |
| B | True (incorrect) | Wrong: a passive fill does *not* always mean the full spread was earned — post-fill adverse movement can exceed any spread captured. |
| C | False (accurate) | Correct: informed or better-timed sellers may be choosing to trade against the bid when the posted price is stale/favorable to them. |
| D | False (accurate) | Correct: the maker should evaluate post-fill price movement (markouts), not merely the fraction of orders filled. |
| E | False (accurate) | Correct: a high fill rate can coexist with poor execution quality when fills cluster before adverse price moves. |

**Reference:** Harris, *Trading and Exchanges*, ch. on informed traders and market efficiency, and ch. on dealers (adverse selection, markouts, spread decomposition); Balch ML4T Market Mechanics (02-02).

### [QF2-D8G7Q2] Information leakage from predictable child orders
**Scenario:** A fund must quietly buy a large position over two days. After it repeatedly submits similarly sized child orders at predictable times, other traders buy ahead and ask prices rise before later child orders arrive. Each item asserts that its quoted statement is incorrect.
**Answer polarity:** **Inverted (True = the statement is INCORRECT; False = the statement is accurate).**

| Choice | Verdict | Why |
|--------|---------|-----|
| A | False (accurate) | Correct: the repeated pattern can leak information about the fund's remaining demand — predictable child orders let observers infer a persistent parent order. |
| B | False (accurate) | Correct: others buying ahead (anticipatory trading) can raise the fund's later execution cost by pushing offers higher. |
| C | False (accurate) | Correct: randomizing timing or size can reduce predictability but cannot guarantee secrecy — some signal always leaks from trading. |
| D | True (incorrect) | Wrong: splitting a parent into child orders does *not* automatically prevent leakage — a detectable, predictable sequence can reveal the parent precisely. |
| E | False (accurate) | Correct: execution quality depends partly on how the algorithm reveals its intentions (information footprint) to the market. |

**Reference:** Harris, *Trading and Exchanges*, ch. on informed traders, order-exposure/front-running, and hiding trading intentions; Almgren-Chriss (impact of trading footprint); Balch ML4T Market Mechanics (02-02).

### [QF2-D8G7Q3] Markouts and the economics of passive vs. aggressive
**Scenario:** For an urgent buy, a passive order may save 4 cents vs. crossing the spread *if* filled, but historical filled passive orders are followed by an average 7-cent price decline over the next minute. An aggressive order generally completes immediately at the ask.
**Answer polarity:** Normal (True = accurate).

| Choice | Verdict | Why |
|--------|---------|-----|
| A | True | The 4-cent quoted improvement alone does not establish better economic execution — quality includes post-fill behavior and whether the full order completes. |
| B | True | A negative post-fill markout (price falls after passive buys fill) is evidence consistent with adverse selection against the passive buyer. |
| C | True | Under the stated averages, the 7-cent adverse move exceeds the 4-cent initial improvement by 3 cents. |
| D | False | The aggressive order is *not* costless — crossing the spread, market impact, and adverse price movement can still impose costs. |
| E | True | Greater urgency can shift the balance toward aggressive execution even when passive orders sometimes receive better quoted prices, because certainty can outweigh possible spread capture. |

**Reference:** Harris, *Trading and Exchanges*, ch. on dealers and informed traders (adverse selection, markouts) and ch. on transaction-cost measurement; Almgren-Chriss (urgency vs. cost); Balch ML4T Market Mechanics (02-02).

## References (domain-level)

1. **Harris — *Trading and Exchanges: Market Microstructure for Practitioners* (Larry Harris):** ch. 4 (orders and order properties — limit vs. market/marketable orders, order aggressiveness, fill risk); ch. on order-driven markets and order-precedence rules (price-time priority, queue position, displayed vs. hidden depth); ch. on liquidity and the bid/ask spread (immediacy, spread as a transaction cost, maker/taker roles); ch. on dealers and on informed traders & market efficiency (adverse selection, markouts, spread decomposition, stale-quote picking-off); ch. on transaction-cost measurement (implementation shortfall, VWAP/TWAP benchmarks, opportunity cost of non-execution); and discussion of order exposure, front-running, and hiding trading intentions. *(Cited at chapter/section level; no page numbers invented.)*
2. **Almgren & Chriss — *Optimal Execution of Portfolio Transactions* (2000):** the market-impact vs. timing-risk trade-off, the trading trajectory/schedule, the efficient frontier of optimal execution, and how risk aversion and urgency determine the optimal horizon and (dynamically) child-order aggressiveness. Used for G1 (arrival benchmark/opportunity cost), G3 (fast vs. slow scheduling, dynamic re-scheduling), G5Q3 (cost of delay), and G7 (trading footprint/urgency).
3. **Balch — ML4T "Market Mechanics" (Georgia Tech lecture 02-02):** the limit order book, how limit and market orders execute, bid/ask/spread, and VWAP/TWAP/participation execution — the course-level grounding for all G1–G7 questions.

<!-- Garbled-symbol note: the source slice QF2_D08.txt renders ligatures as mojibake — "ﬁ"/"ﬂ" ligatures appear in "proﬁt", "ﬁll", "unﬁlled", "proﬁtability", "beneﬁt", "speciﬁc(ally)", "ﬂow", "deﬁnition", etc., and several benchmark labels carry a stray trailing space before punctuation ("VWAP .", "TWAP ,"). These are OCR/encoding artifacts only; all scenarios above are transcribed with corrected spelling. No verdicts were affected. -->
