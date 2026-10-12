# What Hedge Funds Really Do — Ch. 4: Market-Making Mechanics

*Source: Romero & Balch, What Hedge Funds Really Do, PDF pages 25–28 (no separate printed page
numbers; PDF page labels = PDF page numbers). Sections: (intro: exchanges, brokers, market makers);
Market Spreads; Types of Order (Basic); Types of Order (Intermediate); Matching Orders: The Order Book;
The Advantage of Milliseconds (incl. front running).*

> ML4T exam relevance: bid/ask, spread, liquidity, market vs limit orders, order book walking and
> imbalance, short selling mechanics and risk, stop orders, HFT/co-location/front running → QF D5
> Market Microstructure & Trade Execution (primary); order-book information and arbitrage speed → QF D8.

## Exchanges and Intermediaries (p.25)
- **Markets** = locations (physical or virtual) where sellers and buyers convene to exchange goods / financial
  instruments. Rising prices indicate more buyers than sellers; falling prices the opposite.
- Investors do **not** trade on the exchange themselves; they trade through **intermediaries**:
  - **Brokerage firms** interface with end-buyers and end-sellers.
  - Brokers trade with **market makers**, who facilitate the trades.
  - At the **NYSE**, market makers are called **specialists** — the only entities transacting on the floor.
  - **NASDAQ** has no floor (all electronic) → **no specialists**.

## Market Spreads (p.25)
- Two prices at any moment: **bid** (price at which a buyer may purchase) and **ask** (price at which a
  seller will sell) — the book's wording. Example: IBM "$200.50 ask; $199.75 bid."
- **Market spread** = ask − bid; it is the **profit opportunity** that induces brokerages and specialists to
  make the market.
- High-volume markets attract more market makers who **compete on the spread** → **highly liquid markets
  (large volume, many market makers) tend to have the smallest spreads**.
- **Widening spreads can be an early sign of liquidity freezing up** (fixed income markets, fall 2008).
- Niche/frontier markets (Myanmar, Kazakhstan) → low volume → **wide spreads**.

## Types of Order (Basic) (pp.25–26)
- **Buy** and **sell** orders for a number of shares; **round lot = 100 shares**.
- **Market order** ("at the market"): broker accepts whatever price the market offers.
- **Limit order**: sets a condition before execution.
  - Buy "limit order for 100 IBM at $200" → buy only at **$200 or less**.
  - Equivalent sell limit → sell only at **$200 or higher**.

## Types of Order (Intermediate) (pp.26–27)
- Exchanges only accept/execute **buy and sell** orders in the order book; more complex orders are handled
  by a **broker**. Examples: **selling short** and **stop orders**.
- **Selling short** = bet the price will fall (the conventional bet that price rises = **going long**).
  - Borrow shares from a holder → sell them (receive proceeds) → later buy the same number and return them.
  - Price fell → pocket the difference; price rose → lose the difference.
  - The short seller must also pay **interest to the share owner (the "rebate")** plus **any dividends** the
    owner is entitled to during the borrowing period.
  - Two transactions: **"sell to open"** then **"buy to close"** — reverse time order of a long trade.
- **Why shorts are riskier than longs, on average** (three reasons):
  1. Long-term trend of stock prices is **upward** → a short must bet against it.
  2. **Potential loss is unbounded**: max loss on a long is 100% (price can't go below zero); a short's
     theoretical max loss is **unlimited** (price can rise without bound).
  3. Shorted companies' executives may **retaliate** (e.g., curtail analyst access).
- **Few hedge funds are short-only**, though many use shorts to hedge longs. Shorts need exceptionally deep
  research and contrarian determination.
- **Stop orders**: contingent orders, usually for **risk management**.
  - **Stop loss** (most common): automatically place a **market order** if price falls more than a threshold
    (e.g., 25%) below the purchase price.
  - **Trailing stop**: same, but the reference is the **most recent high** (preserves most gains).
  - **Free ride**: sell **half** a position when it has **doubled** → original capital "off the table," only
    profits at risk.
  - All complex/contingent orders must be placed through a broker. Some investors keep stop-loss rules
    **private** (withhold from broker until execution time) because others can exploit that information.

## Matching Orders: The Order Book (p.27; Figure 4.1 p.28)
- Specialists (or the exchange computer) tabulate an ever-changing **order book**: shares offered (ask) and
  requested (bid) at each price.
- **Figure 4.1 — sample order book for XYZ** (figure is an image; values read from it):

  | Bid size | Price | Ask size |
  |---|---|---|
  |  | $100.10 | 300 |
  |  | $100.05 | 300 |
  |  | $100.00 | 200 |
  | 100 | $99.95 |  |
  | 50 | $99.90 |  |
  | 100 | $99.85 |  |

- **Spread = lowest ask − highest bid** = $100.00 − $99.95 = **5 cents**. The book states this is "0.5
  percent of the midpoint" [arithmetic note: $0.05 / $99.975 ≈ 0.05%; the book's "0.5 percent" appears to
  be a slip — verify against the PDF p.27 if a question hinges on it]. Very small spread → very liquid market.
- **Worked example — market sell for 150 shares** walks the bid side from the highest bid:
  100 @ $99.95 + 50 @ $99.90 → average **$99.933** per share.
  - This moves the equilibrium price **down the demand curve**: next buyer bids only **$99.85**.
  - A purchase moves price the opposite way (up the curve). Mostly sales → prices fall; mostly purchases →
    rise; equal shares bought and sold → stable prices.
- **Order imbalance**: Figure 4.1 has more shares on offer (800 ask) than bids (250) → XYZ price **will
  probably decline**. Knowledge of the order book can help predict **short-term** price changes.

## The Advantage of Milliseconds (pp.27–28)
- Trades aren't always cleared on exchanges: a broker holding overlapping client buy/sell orders may
  **clear them internally** — saves exchange fees and lets the broker earn the market maker's spread.
- **Dark pools**: syndicates of brokerage firms forming informal exchanges among themselves (past decade).
  Specialists may likewise clear trades before they reach the formal exchange.
- Because buy/sell volume imbalances predict short-term moves, brokers and market makers hold tradable
  information; the **key is speed**.
  - Firms invest in **automated trading** and in cutting communication time: fiber optic instead of copper;
    **co-locating** trading platforms at the exchange. Advantage can hinge on **milliseconds**.
  - **High-frequency trading (HFT)**; Lewis's *Flash Boys* cited.
- **Front running**: a broker issues trades **in advance of its clients'** orders, knowing the price moves
  those orders will probably cause.
  - Ethics **dubious** when trading against its own clients; "fair game" when the counterparty is another
    broker's client.
  - Reducing time to see and execute (technology / co-location) is **"sanctioned front-running."**
- Processing many trades very fast to exploit evident short-term price trends is at the core of
  **trading-oriented hedge funds'** strategies.

## Exam traps (book-grounded)
- Liquid markets → **smaller** spreads; widening spreads signal **declining** liquidity.
- A market order fills at whatever price is available and can **walk the book** — a 150-share sell got
  $99.933 average, not the best bid of $99.95.
- Buy limit = **maximum** price ($200 or less); sell limit = **minimum** ($200 or higher).
- Short loss is **unlimited**; long loss is capped at 100%. Short seller pays rebate interest **and**
  dividends to the lender.
- Stop/trailing/free-ride orders are handled by **brokers**, not the exchange order book.
- Order-book imbalance suggests a **probable** short-term direction — the book says "probably," not certainly.
- NASDAQ has **no** specialists (no floor).

## ML4T exam relevance
- Bid/ask, spread as market-maker profit, liquidity vs spread width, market vs limit orders, round lots → **QF D5 Market Microstructure & Trade Execution**.
- Order book matching, average fill price when walking the book, price impact moving down/up the demand curve, order imbalance → **QF D5**.
- Short selling mechanics (sell-to-open/buy-to-close, rebate, dividends, unbounded loss), stop loss / trailing stop / free ride → **QF D5** (also QF D2 for risk management).
- Internalization, dark pools, HFT, co-location, front running, speed as competitive edge → **QF D5**, **QF D8 Market Efficiency & Arbitrage**.
