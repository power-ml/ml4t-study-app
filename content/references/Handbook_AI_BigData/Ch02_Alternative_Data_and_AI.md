# Ch. 2 — Alternative Data and AI in Investment Research

**Source:** Tierens, I. & Duggan, D. (Goldman Sachs Global Investment Research) — *Handbook of AI and Big Data Applications in Investments*, CFA Institute Research Foundation (2023).
**Book pages:** 20–26 (PDF pages 41–47).
**ML4T exam relevance:** ML Domain 1–2 (data quality, features, bias, sampling/selection bias, false positives/negatives, NLP/sentiment), QF Domain 9–10 (alpha, alternative data, backtesting caveats, systematic vs. fundamental strategies, descriptive vs. prescriptive analytics). Faithful to source; nothing invented.

---

## 1. Definitions and framing

- **AI (broad):** using computers to mimic human problem solving.
- **Alternative data (broad):** any data in a **nonstructured format**. The "alternative" label may be a **misnomer** — often it just delivers legacy information more scalably/timelier in digital form.
- **Core principle:** alternative data and AI (incl. ML and NLP) are **tools in the research toolkit, not ends in themselves.** They **do not define the investment thesis — they help prove or disprove it.** Value only when aligned with a particular strategy.
- Impact is **evolutionary, not revolutionary**; lines between "traditional" and "alternative" data (and what counts as "AI") are blurring.

## 2. Where AI/alt-data is additive: systematic vs. fundamental strategies

- **Systematic (breadth > depth):** need datasets/techniques applicable across **many securities**. Favor text-extracted factors (NLP repeatable across filings/news), econometric conversion of single alphas into multifactor alphas. Horizon matters — intraday news sentiment helps HFT but adds little for a weeks/months horizon.
- **Fundamental (depth > breadth):** analyst goes **deep**, prizes **precision**; **niche datasets** complete the "mosaic" (e.g., social-media consumer sentiment, brick-and-mortar foot traffic, consumer search trends). Non-obvious wins: app downloads in medical devices, localized market-share for managed care, quarry production.

## 3. Data sourcing in a world of oversupply

- Overabundance of providers; **low barriers to entry.** With alt-data, **due-diligence burden shifts from producer to consumer** (parallel to news fact-checking).
- Costs (onboarding, ingestion, testing, licensing) can outweigh benefits → GIR's acquisition is **demand-driven** ("pull," working backward from a use case), not supply-pushed.
- New data need not be **orthogonal** — value can come from delivering legacy data more scalably/timelier.
- GIR keeps analysts (subject-matter experts) as **co-owners** of identifying data rather than a separate "data scout"; a central **Data Strategy team** helps with analysis (GS Data Works).

### Three alternative-data categories (Exhibit 1)
1. **Geospatial** — mobile foot traffic, satellite imagery, demographics, store/EV-charger locations.
2. **Digital/online** — app downloads, online point-of-sale, website visits, product counts/pricing, search trends.
3. **Text (NLP-addressable)** — earnings-call transcripts, filings, tweets, blogs (e.g., NLP-driven quarterly S&P 500 "Beige Book").
- Categories **overlap**; combining dimensions builds a fuller mosaic (e.g., pricing power from product codes/prices + local market share + earnings-call commentary).

## 4. The most time-consuming part: data "grunt work" (curation)

- **Do not expect AI insight without understanding the data.** Data scientists succeed only by knowing data nuances, strengths, weaknesses.
- **Algorithmic bias** stems from **biased training data**; investment apps aren't immune. Subject-matter experts (even without data-science skills) add real value here.
- Run a **small test case** before sourcing; data can **evolve/degrade** over time (inputs removed/added/edited); derived data needs algorithm transparency.
- **Data-quality questions by type:**
  - **Large/complex data:** how comprehensive? **Missing values** bias averages/sums (e.g., web-scraped pricing). Understand any embedded analysis layer (e.g., auto-fill of missing data). Does the data allow the breakouts your thesis needs (e.g., style-specific SKU counts)?
  - **Small data:** may rely on **sampling** → **undersampling / selection bias.** Examples: opt-in point-of-sale panels skew demographics beyond reweighting; satellite parking counts miss covered parking; mobile foot-traffic imprecise in malls/multitenant buildings. **Construction process determines advantages and limitations.**
  - **NLP/text:** input details matter — paywalled content invisible to aggregators; source-specific biases (Instagram vs. Twitter vs. Reddit); guard against **false positives / false negatives** in sentiment (e.g., distinguish a bad product from out-of-stock frustration).
- **Bottom line:** curation determines success/failure; the AI effort fails (or produces wrong outputs) if data gets less attention than the analysis. GIR keeps curation in-house (with SMEs + data scientists).

## 5. The analysis spectrum

- Also a **"pull" approach:** work backward from the use case; escalate to sophisticated methods only when simpler ones fail (outcomes swing on small assumption changes, outliers dominate).
- **Weigh explainability + effort against AI's promise.** Prefer simplicity when it works — e.g., simply **counting mentions of "inflation"** in earnings calls was a robust proxy for a ~200-term screen. When complex, data scientists must supply enough **intuition** for analysts' comfort.
- **Limits:** financial dynamics are **unstable/adaptive**; limited in-sample/out-of-sample data caps how far techniques can be pushed. **Breakpoints** (e.g., COVID-19) break statistical relationships (GIR "nowcasting" indicators had to be re-adapted; extreme outliers broke them) — **humans are critical** for curating data and continuously assessing algorithm results ("man + machine").
- GIR's NLP focus = **surfacing content scalably** more than interpreting meaning/sentiment (accuracy-critical NLP flagged too many false positives/negatives).

## 6. Measuring success — use a WIDE lens (three questions)

1. **Does it create alpha?** Unlikely from a single dataset/technique. For **systematic** strategies you can **backtest with vs. without** the AI component to measure marginal alpha (usual backtesting caveats apply).
2. **Does it produce unique insights more timely/precise?** For **fundamental** strategies direct alpha is hard to attribute; quantify improvement on specific dimensions. Most GIR AI/alt-data work is **descriptive** (feeds the thesis) rather than **prescriptive** (directly recommends a trade).
3. **Does it create scalability** that saves analyst time or extends a hypothesis across more securities / more often? (e.g., NLP across an entire coverage universe + peers + multiple years.)
- ROI hurdles for AI often unfairly stricter than for traditional data — questioning them is **healthy** and levels the playing field.

## 7. Getting started — "a marathon, not a sprint"

- Hire 1–2 hands-on data scientists genuinely interested in investment problems; pair with 1–2 analysts with a durable use case; start with **simple, non-complicated datasets.**
- **Senior sponsorship** matters (cover to experiment + accountability). Involve **engineering, legal, compliance from Day 1** (storage, firewalls, terms/licensing). Consider **build vs. buy** as use cases mature.
- **Centralized vs. embedded:** GIR chose **centralized** (extension of research teams globally/across asset classes) to connect dots across use cases.
- Goal: **minimize algorithmic and data biases** via integrated, iterative, collaborative "man + machine" — until "big" and "alternative" labels may no longer be relevant.
