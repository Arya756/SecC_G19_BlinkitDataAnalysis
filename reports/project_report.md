# The Unplanned Basket — Project Report

**Analyst:** Aryan Patel · Newton School of Technology  
**Programme:** Data Visualization & Analytics — Capstone 2  
**Date:** April 2026

---

## Executive Summary

This report analyses 13,000 Blinkit SKUs across 10 Indian cities to answer: *What share of Blinkit's sales is impulse (unplanned) vs planned, and what premium are users paying for convenience?*

Using a composite **impulse-proxy score** built from pack size, shelf life, category, and promotional status, we classified every SKU into Impulse, Mixed, or Planned baskets. The findings below are derived entirely from the data.

---

## 1 · Revenue Split: Impulse vs Planned

| Basket Type | Revenue (₹) | Share |
|:---|---:|---:|
| **Planned** | 26,07,32,193 | **51.2%** |
| **Mixed** | 13,81,61,656 | **27.1%** |
| **Impulse** | 11,01,33,281 | **21.6%** |
| **Total** | 50,90,27,130 | 100% |

**Key finding:** Over one-fifth (21.6%) of Blinkit's total revenue comes from SKUs that exhibit impulse characteristics — small packs, short shelf life, impulse-prone categories, and active offers. When Mixed baskets (which contain partial impulse signals) are included, **48.8% of revenue has some impulse component.**

---

## 2 · The Convenience Premium ("Tap Tax")

Price-per-100g analysis reveals a stark premium consumers pay for smaller, convenience-sized packs:

| Weight Bucket | Median Price/100g (₹) | Mean Price/100g (₹) |
|:---|---:|---:|
| **Small (<300g)** | **110.44** | **155.86** |
| Mid (300–700g) | 47.93 | 62.83 |
| Bulk (>700g) | 18.32 | 24.46 |

**Statistical validation (Welch t-test):** t = 49.40, **p ≈ 0.0** — the difference is overwhelmingly significant. Small-pack consumers pay **~6× more per gram** than bulk buyers.

This is the "tap tax" — the hidden premium urban India pays for the convenience of 10-minute delivery in impulse-friendly pack sizes.

---

## 3 · Category-Level Impulse Anatomy

Revenue breakdown by basket type per category:

| Category | Impulse % | Mixed % | Planned % |
|:---|---:|---:|---:|
| **Fruits & Vegetables** | **69.8%** | 30.2% | 0.0% |
| **Bakery** | **67.6%** | 32.4% | 0.0% |
| **Dairy** | **62.3%** | 37.7% | 0.0% |
| Snacks | 20.2% | 47.4% | 32.4% |
| Beverages | 10.8% | 49.7% | 39.5% |
| Personal Care | 0.0% | 16.8% | 83.2% |
| Grocery | 0.0% | 18.5% | 81.5% |
| Household | 0.0% | 19.1% | 80.9% |

**Key finding:** Fruits & Vegetables, Bakery, and Dairy are **overwhelmingly impulse-driven** (62–70% impulse revenue). These categories have short shelf lives and are consumed immediately — classic impulse signals. Personal Care, Grocery, and Household are planned purchases (>80% planned).

### Pareto Analysis of Impulse Revenue

| Category | Impulse Revenue (₹) | Cumulative % |
|:---|---:|---:|
| Bakery | 4,27,46,638 | 38.8% |
| Fruits & Vegetables | 3,32,18,529 | 69.0% |
| Dairy | 2,21,69,157 | 89.1% |
| Snacks | 74,63,554 | 95.9% |
| Beverages | 45,35,403 | 100% |

**Just 3 categories (Bakery, F&V, Dairy) drive 89% of all impulse revenue.** These are the "impulse core" that should receive priority in assortment and promotional strategy.

---

## 4 · City-Level Impulse Behaviour

| City | Impulse Revenue Share |
|:---|---:|
| **Ahmedabad** | **24.9%** |
| Chennai | 23.4% |
| Bengaluru | 22.7% |
| Jaipur | 22.4% |
| Lucknow | 21.4% |
| Kolkata | 21.3% |
| Mumbai | 21.1% |
| Delhi | 21.0% |
| Hyderabad | 20.6% |
| Pune | 17.8% |

**Key finding:** Impulse share ranges from 17.8% (Pune) to 24.9% (Ahmedabad) — a **7 percentage-point spread.** However, the Kruskal-Wallis test (H=9.13, p=0.43) shows this city-level variation is **not statistically significant**, suggesting impulse propensity is relatively uniform across India's urban centres at the aggregate level.

---

## 5 · Statistical Hypothesis Testing Summary

| # | Hypothesis | Test | Result | Implication |
|:---|:---|:---|:---|:---|
| H1 | Impulse SKUs sell more than Planned | Mann-Whitney U | **Not significant** (p=0.80) | Impulse and planned SKUs sell similar quantities — the difference is in *price*, not *volume* |
| H2 | Offers increase demand | ANOVA | **Not significant** (p=0.41) | Offers alone do not materially lift volume in this dataset |
| H3 | Cities differ in impulse propensity | Kruskal-Wallis | **Not significant** (p=0.43) | Impulse is a national phenomenon, not city-specific |
| H4 | Small packs cost more per 100g | Welch t-test | **Significant** (p≈0.00) | Small packs charge a **6× premium per gram** — the core monetisation lever |
| H5 | Pareto rule (top 20% → 80% revenue) | Cumulative analysis | **Partially holds** | Top 20% of products drive **60.3%** of revenue |

---

## 6 · Correlation & Regression Insights

### Key Correlations
- `sold_quantity` ↔ `demand_index`: **0.91** (strong) — demand index is a reliable demand proxy
- `sold_quantity` ↔ `revenue_inr`: **0.64** — volume drives revenue
- `price_per_100g` ↔ `impulse_premium_pct`: **0.80** — higher unit price = higher premium
- `impulse_score` ↔ `sold_quantity`: **0.01** — impulse classification does NOT predict volume

### Linear Regression (sold_quantity ~ offers + impulse_score + price + discount)
- **R² ≈ 0.000** — these features do not predict sold quantity
- The model is not significant (F-stat p=0.675)
- **Interpretation:** Impulse behaviour in this dataset manifests through *price premiums* and *category composition*, not through volume differences. The "tap tax" is a pricing phenomenon, not a demand phenomenon.

---

## 7 · Key Insights for Decision-Making

### Insight 1: The impulse basket is real — but it's a pricing story, not a volume story
21.6% of revenue is impulse-driven. Impulse SKUs don't sell *more units* than planned SKUs — they sell at **dramatically higher per-gram prices**. The business opportunity is in price architecture, not demand generation.

### Insight 2: Three categories ARE the impulse business
Bakery, Fruits & Vegetables, and Dairy account for 89% of impulse revenue. These short-shelf-life, immediate-consumption categories are the backbone of the unplanned basket.

### Insight 3: The convenience premium is 6× and it's statistically undeniable
Small packs (<300g) charge ₹110/100g vs ₹18/100g for bulk. This is not noise — it's the single most statistically significant finding (t=49.40). Urban India is paying a massive "tap tax" for convenience.

### Insight 4: Offers are not the impulse trigger they're assumed to be
Offers do not significantly increase sold quantity (ANOVA p=0.41). The impulse decision is driven by category, pack size, and perishability — not by discounts. This challenges the common assumption that promotions drive impulse purchases on quick-commerce.

### Insight 5: Impulse is a national pattern, not a city-specific one
City-level differences in impulse share (17.8%–24.9%) are not statistically significant. A national impulse strategy is more defensible than city-by-city localisation.

### Insight 6: The Pareto principle partially holds
The top 20% of products contribute 60.3% of revenue — concentrated but not as extreme as the classic 80/20. There is a longer tail of moderate-revenue SKUs that still matter for assortment breadth.

---

## 8 · Recommendations for FY26

1. **Rebalance assortment investment** toward Bakery, F&V, and Dairy — these three categories generate 89% of impulse revenue and should receive disproportionate shelf-space and supply-chain priority.

2. **Exploit the convenience premium** — small pack sizes are the primary margin lever. Introduce or expand small-pack SKUs in mid-performing impulse categories (Snacks, Beverages) to capture untapped premium.

3. **Rethink promotional spend** — offers do not significantly lift demand. Redirect discount budgets toward visibility (placement, push notifications) rather than price cuts. The impulse purchase is triggered by *presence*, not *price reduction*.

4. **Apply a national impulse strategy** — since city-level variation is not significant, deploy a uniform impulse-assortment playbook across all 10 cities rather than city-customised approaches.

5. **Focus pricing analytics on per-gram economics** — the strongest signal in the data is the pack-size premium. Build pricing models around price-per-100g rather than absolute price to optimise margin extraction from the convenience economy.

---

## 9 · Limitations

- Impulse is *inferred* from SKU attributes, not observed from customer behaviour. Findings are framed as "statistical signatures consistent with impulse."
- `offer_type` was NaN for ~50% of SKUs (recoded as "No Offer"). The offer analysis may understate promotional impact.
- The dataset is a product-level snapshot, not a transactional log. Time-series trends and customer-level cohort analysis are not possible.
- The impulse-proxy score weights (0.30/0.25/0.25/0.20) are analytically chosen, not learned from data.
- No causal claims are made — only associations.

---

*End of Report*
