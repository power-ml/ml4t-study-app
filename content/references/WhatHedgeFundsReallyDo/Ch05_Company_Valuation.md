# What Hedge Funds Really Do — Ch. 5: Introduction to Company Valuation

*Source: Romero & Balch, What Hedge Funds Really Do, PDF pages 29–35 (no separate printed page
numbers; PDF page labels = PDF page numbers). Sections: (intro: value investing, fundamental vs
technical); Asset-Based Valuation: Book Value; Intrinsic Value: Dividend-Based Valuation (Time Value of
Money; The Dividend Discount Model); Long-Term Ownership of an Asset; Growth-Based Valuations;
Integrating Asset-Based and Cash Flow–Based Valuations; What If?*

> ML4T exam relevance: intrinsic value vs market price, book value and P/B, time value of money,
> PV/discounting, dividend discount model, perpetuity = D/DR, growth sensitivity, margin of safety,
> scenario ranges → QF D6 Valuation & Mispricing (primary); compounding/discounting math → QF D1;
> long/short from mispricing → QF D8/D10.

## Introduction: Price vs True Value (p.29)
- A successful investment means the buyer had a **more accurate view of true value** than the seller. A
  share = partial ownership of the company. The **mixture of differing views** is what enables a market.
- Opportunity = current price **diverges** from believed true value. Markets may be quite efficient, but
  hedge funds seek the occasional **inefficiencies**:
  - Price **below** estimated true value → **go long**; **overpriced** → **short**.
- **Benjamin Graham**, *The Intelligent Investor* (cited by Buffett): seek a **margin of safety** — buy only
  well below your estimate of true value ("buying dollar bills for fifty cents"). Only possible if confident
  in your own value estimate.
- **Fundamental analysis**: based on a company's business operations and finances. Distinct from
  **technical analysis** ("charting"), which predicts prices from past price behavior.
- Three fundamental valuation methods:
  1. **Book value** — sum of assets and liabilities.
  2. **Intrinsic value** — based on **future dividends**.
  3. **Earnings growth** — projection of expanded future earnings.

## Asset-Based Valuation: Book Value (pp.29–30)
- Firms report **assets** (tangible: factories; intangible: patents; categorized by how quickly convertible
  to cash) and **liabilities** (debts, raw-material commitments, employment contracts; categorized by
  duration). **Net worth = assets − liabilities**.
- If the firm closed tomorrow, net worth ≈ what owners would be left with. On the balance sheet:
  **stockholders' equity = book value** (value as captured by accountants).
- **Book value vs market value (market capitalization)** diverge because:
  - Accounting is **conservative**: assets carried at **original price less accumulated depreciation**, even
    if they appreciated (e.g., city real estate) → **deflates** book value. So reported book value is
    **usually below** what the company would fetch if actually liquidated.
  - But in a **forced/involuntary sale** (bankruptcy, recession depressing all asset prices) the firm may
    receive far less → **in a recession, book value may overstate true value**.
- **Price-to-book ratio = share price / book value per share**.
  - Mature low-growth or troubled firms may trade **below** book (P/B < 1.0) or barely above it.
  - Conservative value investors are attracted to buying below book; not uncommon when the company, its
    industry, or the economy is in distress.

## Intrinsic Value: Dividend-Based Valuation (pp.30–32)
- Book value **does not reflect future prospects**, one reason it may **underestimate** true value.
### Time Value of Money
- Buyer pays a lump sum for a stream of future cash flows → convert future flows to a lump sum by
  **discounting** (the **time value of money**).
- Bequest example: friend will certainly receive **$10,000 in 1 year**. Even with zero uncertainty you'd pay
  less than $10,000 because of **opportunity cost** — the return sacrificed on the best alternative (e.g.,
  SPY expected to return 10%).
- **PV = FV / (1 + DR)^I**, where DR = discount rate, I = years until payment.
  - $10,000 / (1.1)^1 = **$9,090.91** → pay no more than ~$9,091.
- **Discount rate** = return available from the **best alternative investment**; the book used the stock
  market, but others often use a less risky rate (Treasury bonds). It should reflect the most likely
  alternative's lost opportunity.
- Stocks may provide a **stream** of dividends into the infinite future while the board maintains them —
  but not all companies pay dividends; some suspend them or fail.
- PV of multiple payments = **sum of each payment's PV**:
  - $10,000 in 1 yr: $9,090.91; $10,000 in 2 yrs: $10,000/(1.1)^2 = $8,264.46 → portfolio **$17,355.37**.
- **Intrinsic value of any asset = present value of all future returns** (single or multiple, uniform or
  nonuniform). Estimating future cash flows is outside the book's scope.
### The Dividend Discount Model
- **Divco** (electric utility) pays **$1/yr**; best alternative return **8%**:
  - Yr 1: $1/1.08 = $0.9259; Yr 2: $0.8573; Yr 3: $0.7938 (printed "$.07938" in the PDF — typo);
    … Yr 10: $1/(1.08)^10 = $0.4632.
  - **10-year sum = $6.71** → intrinsic value $6.71 if those were the only returns. Trading at **$7.00 →
    overpriced**; at **$5.00 → a bargain**.
- Each later dividend is worth less today; by year 10 a dollar is worth **less than half**. Year 50:
  $1/(1.08)^50 = **$0.0213** (barely 1/50th).

## Long-Term Ownership of an Asset (p.33)
- Far enough out, PV of a payment ≈ 0 → **an infinite horizon does not produce an infinite PV**.
- Owning an income-producing asset = payments **in perpetuity** (any stock, as long as the company survives).
- Uses the infinite sum (shown as an image in the PDF): **Σ_{i=1}^{∞} 1/n^i = 1/(n − 1), where |n| > 1**.
  Substituting n = (1 + DR): PV = FV / ((1 + DR) − 1) → **PV = FV / DR**.
- **Perpetuity value = D / DR** (D = constant annual dividend).
  - Divco forever: **$1.00 / 0.08 = $12.50**.
  - **More than half** the value comes in the first 10 years ($6.71 of $12.50); years 11→∞ are worth **$5.79**.

## Growth-Based Valuations (pp.33–34)
- Fast-growing assets (small growth companies) valued on projected **fast-growing future earnings**, with
  **identical** discounting methods — each year's earnings projected higher than the last; value = sum of
  discounted cash flows.
- In theory could be infinite, but for any reasonable discount rate far-future cash flows discount to ~zero
  → a perpetual cash flow still has a **finite** PV.
- **Valuations depend critically on the assumed growth rate; small differences in growth assumptions lead
  to big disparities in valuations.**

## Integrating Asset-Based and Cash Flow–Based Valuations (p.34)
- "The mathematics is the easy part"; the hard part is the **judgments** behind inputs and assumptions.
- **Asset-based estimates usually produce lower valuations** than long-term DCF, because they reflect past
  prices paid for assets, not value enhanced by their use.
- Book value can still **overestimate** value in a forced liquidation or bad recession. Asset-based values
  are often viewed as **"lower bounds"** but may need downward adjustment; analysts commonly **discount book
  value by 30% or 50%** for a true "worst case."
- Cash-flow projections farther out are more conjectural, but **forecasting errors matter less farther
  out** because they are more heavily discounted.
- **Asset-based ignores future earnings; cash-flow-based focuses exclusively on them → adding the two
  together can produce the most complete valuation.**
- Analysts commonly produce a **range** of valuations (different methods, different assumptions).

## What If? (pp.34–35)
- Scenario example: Divco builds a plant in a fast-growing area.
  - **Base case**: 4% annual population growth for 10 years, tapering to 1%/yr after.
  - **Pessimistic**: 2% for 10 years, 0% after. Optimistic could be **several times** the pessimistic value.
  - Asset-based scenarios: optimistic = assets sold at **full book**; pessimistic = e.g., **50% of book**.
- Which is right? **No way to know until the future unfolds** → consider a **range**. Aggressive investors
  emphasize the high end; conservative the low end; Graham's margin of safety → the low end or lower.
- Single point-estimate **"target price"** = "substituting **precision for accuracy**." Authors: "**better
  to be roughly right than precisely wrong**."
- Authors' margin of safety: rarely buy dollar bills for 50 cents, but "generally aren't tempted unless
  dollars are priced **below 80 cents**."

## Exam traps (book-grounded)
- Book value is **usually below** liquidation value (conservative accounting), **but** can **overstate** true
  value in forced sales / recessions — neither direction is absolute.
- P/B < 1 is possible (mature/troubled firms) and attracts conservative value investors.
- Infinite stream of dividends has a **finite** PV (D/DR); far-future flows → ~0 PV.
- More than half of Divco's perpetual value arrives in the first 10 years.
- Higher discount rate → lower PV; small growth-assumption changes → large valuation changes.
- Far-future forecast errors have **declining** importance (heavier discounting).
- Fundamental analysis ≠ technical analysis (charting from past prices).
- A precise single target price is **not** more accurate — ranges are preferred.

## ML4T exam relevance
- Intrinsic value vs market price, long undervalued / short overvalued, margin of safety → **QF D6 Valuation & Mispricing**; trading on mispricing → **QF D8 Market Efficiency & Arbitrage**.
- Book value, P/B, conservative accounting, distress overstating book → **QF D6**.
- Time value of money, PV = FV/(1+DR)^I, opportunity-cost discount rate, perpetuity D/DR, DDM worked numbers → **QF D6**, **QF D1 Investment Returns & Compounding**.
- Growth-assumption sensitivity, scenario ranges, "precision vs accuracy" → **QF D6**, **QF D10 Quantitative Strategy Design & Evaluation**.
- Fundamental vs technical analysis distinction → **QF D6**, **QF D8** (links to EMH forms in Ch. 8).
