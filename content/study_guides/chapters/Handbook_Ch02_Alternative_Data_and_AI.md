# Study Guide — Handbook Ch. 2: Alternative Data and AI in Investment Research

**Built from:** `references/Handbook_AI_BigData/Ch02_Alternative_Data_and_AI.md`
(Tierens, I. & Duggan, D. (Goldman Sachs Global Investment Research) — *Handbook of AI and Big Data Applications in Investments*, CFA Institute Research Foundation, 2023).
**Source page range (from ref header):** Book pages **20–26** (PDF pages 41–47).
**Mapped exam domains (per `references/INDEX.md`):** ML **D2** (data & sampling discipline) & ML **D3** (feature engineering, leakage); QF **D9** (financial-data & research bias).

---

## 1. Key concepts

- **Definitions:** **AI** = using computers to mimic human problem solving; **alternative data** = any data in a **nonstructured format**. The "alternative" label is often a **misnomer** — frequently it just delivers legacy information more scalably/timelier.
- **Tools, not ends:** alt-data and AI (ML, NLP) **do not define the investment thesis — they help prove or disprove it.** Impact is **evolutionary, not revolutionary.**
- **Systematic vs. fundamental:** **systematic** (breadth > depth) favors text-extracted factors repeatable across many securities; **fundamental** (depth > breadth) prizes **precision** and uses **niche datasets** to complete the "mosaic."
- **Sourcing in a world of oversupply:** low barriers to entry shift the **due-diligence burden from producer to consumer**; GIR's acquisition is **demand-driven ("pull")**, working backward from a use case. Three alt-data categories: **geospatial, digital/online, text (NLP-addressable)** — they overlap.
- **Data "grunt work" (curation) is the most time-consuming part:**
  - **Do not expect AI insight without understanding the data.**
  - **Algorithmic bias stems from biased training data.**
  - **Data-quality by type:** large/complex data → **missing values bias averages/sums**; small data → **sampling → undersampling / selection bias** ("construction process determines advantages and limitations"); NLP/text → guard against **false positives / false negatives** in sentiment.
- **Analysis spectrum:** prefer simplicity; escalate to complex methods only when simpler ones fail. **Limits:** financial dynamics are unstable/adaptive; **breakpoints** (e.g., COVID-19) break statistical relationships — "**man + machine**."
- **Measuring success (wide lens):** (1) does it create alpha? for **systematic** strategies, **backtest with vs. without** the AI component (usual backtesting caveats apply); (2) unique/more-timely insights? most GIR work is **descriptive** (feeds the thesis) not **prescriptive** (recommends a trade); (3) scalability that saves analyst time.

## 2. Why it matters for Exam 1

This chapter (Weeks 2 & 6 reading) is the data-quality and research-discipline anchor for Exam 1. It reinforces:

- **ML D2 (Data & Sampling Discipline):** missing values and their causes, mean-imputation hazards, sampling/selection bias, and representativeness — the chapter's "data grunt work" section maps directly.
- **ML D3 (Feature Engineering & Leakage):** vendor-feature due diligence, feature construction from text/alt-data, and the leakage/lineage caution behind "too good to be true" signals.
- **QF D9 (Financial Data & Research Bias):** selection/undersampling bias, informative missingness, false positives/negatives, and backtesting caveats for alt-data signals.

## 3. Sample questions (verbatim from mapped-domain verdict tables — not invented)

### Q1 — ML D2, item [ML-D2G1Q4] "Missing volume during liquidity crunches (MNAR)"
**Scenario:** A researcher finds small-cap "Daily Trading Volume" is missing mainly during extreme-volatility periods when liquidity evaporates, and must judge how to treat it. **Answer polarity: Normal (True = accurate).**

> | B | True | Mean imputation of volume artificially reduces variance and erases the "zero-liquidity" signal, so the model underestimates risk. |
> | D | True | Missingness that coincides with liquidity crunches is itself an informative feature: a null in a liquidity field flags untradeability, valuable to a risk model. |
> | E | True | When data is MNAR, any imputation that does not model the *cause* of missingness introduces systematic bias into the backtest. |

*(Source: `study_notes/ML/Domain_02_Data_and_Sampling_Discipline.md`.)*

### Q2 — ML D3, item [ML-D3G7Q1] "53%→99% from an opaque vendor feature"
**Scenario:** A new alt-data "sentiment score" jumps a stock-direction model's test accuracy from 53% to 99%; the vendor won't explain construction, the PM wants to trade, and model-risk wants proof the score is available before each prediction. **Answer polarity: Normal (True = accurate).**

> | A | True | An abrupt, implausibly large accuracy jump is a reason to investigate leakage and data lineage. |
> | B | False | Wrong: confidentiality does not establish causal availability or clean construction — a proprietary feature is not presumed valid. |
> | E | False | Wrong: near-perfect historical accuracy does not guarantee live accuracy — leakage, overfitting, and regime change can destroy it. |

*(Source: `study_notes/ML/Domain_03_Feature_Engineering_and_Leakage.md`.)*

### Q3 — QF D9, item [QF-D9G6Q3] "Informative missingness and mean imputation"
**Scenario:** Firms omit a newly requested disclosure when results are poor; a researcher replaces every missing value with the cross-sectional mean and treats missingness as random. **Answer polarity: Normal (True = accurate).**

> | A | True | Because poor performers are described as more likely to omit the value, the missingness itself carries information about firm performance. |
> | B | True | Replacing systematically poor observations with an average attenuates or hides the relationship between the disclosure and poor outcomes. |
> | C | False | Imputed values are modeling choices, not genuine observations of what the firms would have reported. |

*(Source: `study_notes/QF/Domain_09_Financial_Data_and_Research_Bias.md`.)*
